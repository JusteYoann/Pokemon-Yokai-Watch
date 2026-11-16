// Project-specific AP channel. No species, stats, encounters or maps altered.
#include "global.h"
#include "yokai_ap.h"
#include "main.h"
#include "event_data.h"
#include "item.h"
#include "script.h"
#include "field_control_avatar.h"
#include "palette.h"
#include "blasters_city.h"
#include "terre_heure.h"
#include "yopple_devices.h"
#include "constants/items.h"
#include "constants/flags.h"
#include "overworld.h"
#include "constants/game_stat.h"
#include "constants/vars.h"
#include "yokai_ap_checks.h"
#include "pokedex.h"
#include "quest_log.h"
#include "constants/quest_log.h"

EWRAM_DATA volatile struct YokaiAPMailbox gYokaiAPMailbox = {0};
EWRAM_DATA volatile u8 gYokaiAPChecks[128] = {0};
EWRAM_DATA volatile u16 gYokaiAPOwnedCount = 0;
const u8 gYokaiAPCatalogHash[] = YOKAI_AP_CATALOG_HASH;
const struct YokaiAPRomInfo gYokaiAPRomInfo = {
    YOKAI_AP_MAGIC, YOKAI_AP_VERSION, sizeof(struct YokaiAPMailbox),
    "Pokemon Yo-kai FireRed", "40c59a9f240d29a7b16d1dd299b1125513a280c4"
};
typedef char YokaiAPSaveSize[(sizeof(struct YokaiAPSave) == 64) ? 1 : -1];
typedef char YokaiAPMailboxSize[(sizeof(struct YokaiAPMailbox) == 48) ? 1 : -1];
typedef char YokaiAPAfterParty[(8 + sizeof(struct Pokemon) * PARTY_SIZE <= YOKAI_AP_SAVE_OFFSET) ? 1 : -1];
typedef char YokaiAPBeforeVacuum[(YOKAI_AP_SAVE_OFFSET + sizeof(struct YokaiAPSave) <= 0x380) ? 1 : -1];

static struct YokaiAPSave *Save(void)
{
    return (struct YokaiAPSave *)(gSaveBlock2Ptr->filler_B20 + YOKAI_AP_SAVE_OFFSET);
}

// Called from the native trainer battle end callback only on B_OUTCOME_WON.
// Native gym/Vs Seeker flag bookkeeping must never manufacture a victory.
void YokaiAPTrainerVictory(u16 trainerId)
{
    struct YokaiAPSave *save;
    u16 i,bit;
    if (!gSaveBlock2Ptr || QL_IS_PLAYBACK_STATE) return;
    save=Save();
    if (save->magic!=YOKAI_AP_MAGIC || save->version!=YOKAI_AP_SAVE_VERSION) return;
    for (i=0;i<ARRAY_COUNT(sYokaiAPTrainerSlots);i++)
        if (sYokaiAPTrainerSlots[i][0]==trainerId)
        {
            bit=sYokaiAPTrainerSlots[i][1];
            save->reserved[bit/8] |= 1 << (bit%8);
        }
}

bool8 YokaiAPKeepTrainerAvailable(u16 trainerId)
{
    struct YokaiAPSave *save;
    u16 i,bit;
    if (!gSaveBlock2Ptr || QL_IS_PLAYBACK_STATE) return FALSE;
    save=Save();
    if (save->magic!=YOKAI_AP_MAGIC || save->version!=YOKAI_AP_SAVE_VERSION) return FALSE;
    for (i=0;i<ARRAY_COUNT(sYokaiAPTrainerSlots);i++)
        if (sYokaiAPTrainerSlots[i][0]==trainerId)
        {
            bit=sYokaiAPTrainerSlots[i][1];
            return !(save->reserved[bit/8] & (1 << (bit%8)));
        }
    return FALSE;
}

static bool8 Safe(void)
{
    return !QL_IS_PLAYBACK_STATE && !gPaletteFade.active && !ScriptContext_IsEnabled()
        && !ArePlayerFieldControlsLocked() && !gMain.inBattle
        && !BlastersCityActive() && !TerreHeureActive() && !YoppleAPBusy();
}

static bool8 SameSession(struct YokaiAPSave *save)
{
    u8 i;
    if (save->magic != YOKAI_AP_MAGIC || save->version != YOKAI_AP_SAVE_VERSION
        || save->slot != gYokaiAPMailbox.slot)
        return FALSE;
    for (i = 0; i < 16; i++)
        if (save->seed[i] != gYokaiAPMailbox.seed[i])
            return FALSE;
    return TRUE;
}

// Explicit whitelist: consumables and Surf, whose source is replaced exactly
// once. Other progression sources remain native, outside this first item pool.
static bool8 AllowedItem(u16 item)
{
    u16 i;
    for (i = 0; i < ARRAY_COUNT(sYokaiAPAllowedItems); i++)
        if (item == sYokaiAPAllowedItems[i]) return TRUE;
    return FALSE;
}

// Called only by the seven audited pickup/gift scripts. Original flags are persistent
// and authoritative; collecting a check never touches the bag.
void YokaiAPTryCollect(void)
{
    struct YokaiAPSave *save = Save();
    u16 i;
    gSpecialVar_Result = 0; // not one of our pickups: run original script
    for (i = 0; i < YOKAI_AP_PICKUP_COUNT; i++)
    {
        if (gSpecialVar_0x8004 != sYokaiAPPickupFlags[i])
            continue;
        if (save->magic != YOKAI_AP_MAGIC || save->version != YOKAI_AP_SAVE_VERSION)
        {
            gSpecialVar_Result = 2; // connect before first pickup, keep reward
            return;
        }
        FlagSet(sYokaiAPPickupFlags[i]);
        gSpecialVar_Result = 1;
        return;
    }
}

void YokaiAPUpdate(void)
{
    struct YokaiAPSave *save;
    u8 nextChecks[sizeof(gYokaiAPChecks)];
    u16 i;
    gYokaiAPMailbox.magic = YOKAI_AP_MAGIC;
    gYokaiAPMailbox.version = YOKAI_AP_VERSION;
    gYokaiAPMailbox.ready = Safe();
    if (!gYokaiAPMailbox.ready)
        return;
    save = Save();
    gYokaiAPMailbox.appliedCount = save->magic == YOKAI_AP_MAGIC ? save->appliedCount : 0;
    gYokaiAPMailbox.saveSchema = save->magic == YOKAI_AP_MAGIC ? save->version : 0;
    gYokaiAPMailbox.bound = SameSession(save);
    // EnterHallOfFame sets GAME_CLEAR before the actual record is saved.
    // The native finale resets DEFEATED_CHAMP before entering this screen.
    gYokaiAPMailbox.goal = FlagGet(FLAG_SYS_GAME_CLEAR)
        && GetGameStat(GAME_STAT_ENTERED_HOF) > 0;
    gYokaiAPMailbox.checkBits = 0;
    for (i = 0; i < 8; i++)
        if (FlagGet(FLAG_BADGE01_GET + i))
            gYokaiAPMailbox.checkBits |= 1 << i;
    for (i = 0; i < 7; i++)
        if (FlagGet(sYokaiAPLegacyFlags[i]))
            gYokaiAPMailbox.checkBits |= 1 << (8 + i);
    memset(nextChecks, 0, sizeof(nextChecks));
    for (i = 0; i < YOKAI_AP_CHECK_COUNT; i++)
        if (sYokaiAPCheckData[i][0]==0xFFFE
            ? (save->magic==YOKAI_AP_MAGIC && (save->reserved[sYokaiAPCheckData[i][1]/8] & (1 << (sYokaiAPCheckData[i][1]%8))))
            : sYokaiAPCheckData[i][0]==0xFFFD
            ? GetSetPokedexFlag(sYokaiAPCheckData[i][1],1)
            : sYokaiAPCheckData[i][0] ? FlagGet(sYokaiAPCheckData[i][0])
            : VarGet(sYokaiAPCheckData[i][1]) == sYokaiAPCheckData[i][2])
            nextChecks[i / 8] |= 1 << (i % 8);
    // Build on the stack: an emulator read between frames must never observe
    // a bitmap cleared halfway through the expensive native capture scan.
    memcpy((void *)gYokaiAPChecks, nextChecks, sizeof(nextChecks));
    gYokaiAPOwnedCount = GetKantoPokedexCount(1);
    if (save->magic == YOKAI_AP_MAGIC && save->lastItem)
        gYokaiAPMailbox.lastItemCount = BagGetQuantityByItemId(save->lastItem);
    if (!gYokaiAPMailbox.command)
        return;
    if (gYokaiAPMailbox.command == YOKAI_AP_CMD_BIND)
    {
        bool8 hasSeed = FALSE;
        for (i = 0; i < 16; i++)
            hasSeed |= gYokaiAPMailbox.seed[i] != 0;
        if (!hasSeed || !gYokaiAPMailbox.slot)
            gYokaiAPMailbox.error = YOKAI_AP_ERR_SESSION;
        else if (!save->magic)
        {
            memset(save, 0, sizeof(*save));
            save->magic = YOKAI_AP_MAGIC;
            save->version = YOKAI_AP_SAVE_VERSION;
            save->slot = gYokaiAPMailbox.slot;
            for (i = 0; i < 16; i++)
                save->seed[i] = gYokaiAPMailbox.seed[i];
            gYokaiAPMailbox.error = 0;
        }
        else
            gYokaiAPMailbox.error = SameSession(save) ? 0 : YOKAI_AP_ERR_SESSION;
        gYokaiAPMailbox.command = 0;
        gYokaiAPMailbox.bound = SameSession(save);
        return;
    }
    if (gYokaiAPMailbox.command != YOKAI_AP_CMD_ITEM || !SameSession(save))
        gYokaiAPMailbox.error = YOKAI_AP_ERR_UNBOUND;
    else if (gYokaiAPMailbox.itemIndex <= save->appliedCount)
        gYokaiAPMailbox.error = 0; // replay: acknowledge without giving twice
    else if (gYokaiAPMailbox.itemIndex != save->appliedCount + 1)
        gYokaiAPMailbox.error = YOKAI_AP_ERR_SEQUENCE;
    else if (!AllowedItem(gYokaiAPMailbox.itemId))
        gYokaiAPMailbox.error = YOKAI_AP_ERR_ITEM;
    else if (!AddBagItem(gYokaiAPMailbox.itemId, 1))
    {
        gYokaiAPMailbox.error = YOKAI_AP_ERR_BAG_FULL;
        return; // retain request; try again after the player frees space
    }
    else
    {
        save->appliedCount = gYokaiAPMailbox.itemIndex;
        save->lastItem = gYokaiAPMailbox.itemId;
        gYokaiAPMailbox.appliedCount = save->appliedCount;
        gYokaiAPMailbox.lastItemCount = BagGetQuantityByItemId(save->lastItem);
        gYokaiAPMailbox.error = 0;
    }
    gYokaiAPMailbox.command = 0;
}

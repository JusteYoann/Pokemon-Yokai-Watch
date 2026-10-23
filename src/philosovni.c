#include "global.h"
#include "philosovni.h"
#include "battle.h"
#include "battle_setup.h"
#include "battle_util.h"
#include "constants/opponents.h"
#include "event_data.h"
#include "fieldmap.h"
#include "item.h"
#include "main.h"
#include "overworld.h"
#include "pokemon.h"
#include "random.h"
#include "script.h"
#include "script_pokemon_util.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/species.h"
#include "constants/vars.h"

bool8 PhilosovniIsPartner(u8 battler)
{
    return (gBattleTypeFlags & BATTLE_TYPE_SCRIPTED_PARTNER) && battler == B_POSITION_PLAYER_RIGHT;
}

void PhilosovniPreparePartner(void)
{
    // Slot six is battle-only. All party/save loops retain PARTY_SIZE == 6.
    CreateMon(&gPlayerParty[PARTY_SIZE], SPECIES_VOLTORB, 21, 20, FALSE, 0, OT_ID_PLAYER_ID, 0);
    SetMonMoveSlot(&gPlayerParty[PARTY_SIZE], MOVE_METAL_CLAW, 0);
    SetMonMoveSlot(&gPlayerParty[PARTY_SIZE], MOVE_SHOCK_WAVE, 1);
    SetMonMoveSlot(&gPlayerParty[PARTY_SIZE], MOVE_QUICK_ATTACK, 2);
    SetMonMoveSlot(&gPlayerParty[PARTY_SIZE], MOVE_SWIFT, 3);
}

static void EndDuo(void)
{
    u8 i;
    bool8 playerAlive = FALSE;
    gSpecialVar_Result = gBattleOutcome;
    ZeroMonData(&gPlayerParty[PARTY_SIZE]);
    if (gBattleOutcome == B_OUTCOME_WON)
    {
        VarSet(VAR_PHILOSOVNI_STATE, 2);
        for (i = 0; i < PARTY_SIZE; i++)
            if (GetMonData(&gPlayerParty[i], MON_DATA_HP)) playerAlive = TRUE;
        if (!playerAlive) HealPlayerParty();
    }
    else
        HealPlayerParty();
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

void PhilosovniStartDuo(void)
{
    gTrainerBattleOpponent_A = TRAINER_PHILOSOVNI_DUO;
    gBattleTypeFlags = BATTLE_TYPE_TRAINER | BATTLE_TYPE_DOUBLE | BATTLE_TYPE_SCRIPTED_PARTNER;
    gMain.savedCallback = EndDuo;
    BattleSetup_StartPartnerBattle();
    ScriptContext_Stop();
}

u8 PhilosovniPartnerMove(void)
{
    u8 i, best = 0;
    u16 score, bestScore = 0;
    u32 limitations = CheckMoveLimitations(gActiveBattler, 0, 0xFF);
    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        if (limitations & (1 << i)) continue;
        score = gBattleMoves[gBattleMons[gActiveBattler].moves[i]].power;
        if (score > bestScore) { best = i; bestScore = score; }
    }
    return best;
}

u8 PhilosovniPartnerTarget(void)
{
    u8 t = (Random() & 1) ? 1 : 3;
    if ((gAbsentBattlerFlags & (1 << t)) || !gBattleMons[t].hp) t ^= BIT_FLANK;
    return t;
}

void PhilosovniRefreshHM(void)
{
    // Reconcile a legitimate existing HM before offering a duplicate.
    if (CheckBagHasItem(ITEM_HM01, 1)) FlagSet(FLAG_GOT_HM01);
}

void PhilosovniSyncActors(void)
{
    u16 state = VarGet(VAR_PHILOSOVNI_STATE);
    if (state >= 2) FlagSet(FLAG_PHILOSOVNI_HIDE_GRUNTS);
    else FlagClear(FLAG_PHILOSOVNI_HIDE_GRUNTS);
    if (state >= 3)
    {
        FlagSet(FLAG_PHILOSOVNI_HIDE_CITY);
        FlagSet(FLAG_PHILOSOVNI_HIDE_COMPANIONS);
        FlagClear(FLAG_PHILOSOVNI_HIDE_GYM);
    }
    else
    {
        FlagClear(FLAG_PHILOSOVNI_HIDE_CITY);
        FlagClear(FLAG_PHILOSOVNI_HIDE_COMPANIONS);
        if (!FlagGet(FLAG_BADGE03_GET)) FlagSet(FLAG_PHILOSOVNI_HIDE_GYM);
        else FlagClear(FLAG_PHILOSOVNI_HIDE_GYM);
    }
}

bool8 PhilosovniNeedsTemplateRefresh(void)
{
    s16 group = gSaveBlock1Ptr->location.mapGroup;
    s16 num = gSaveBlock1Ptr->location.mapNum;
    return (group == MAP_GROUP(MAP_ROUTE25) && num == MAP_NUM(MAP_ROUTE25))
        || (group == MAP_GROUP(MAP_VERMILION_CITY) && num == MAP_NUM(MAP_VERMILION_CITY))
        || (group == MAP_GROUP(MAP_VERMILION_CITY_GYM) && num == MAP_NUM(MAP_VERMILION_CITY_GYM))
        || (group == MAP_GROUP(MAP_VERMILION_CITY_PHILOSOVNI_WAREHOUSE) && num == MAP_NUM(MAP_VERMILION_CITY_PHILOSOVNI_WAREHOUSE));
}

// Continue restores a saved 15x14 viewport after loading the base layout.
// Reapply only the new quay cells so an older save cannot paint over this door.
void PhilosovniRefreshQuay(void)
{
    s16 x, y;
    const struct MapLayout *layout = gMapHeader.mapLayout;
    for (x = 35; x <= 37; x++)
        MapGridSetMetatileEntryAt(x + MAP_OFFSET, 17 + MAP_OFFSET, layout->map[17 * layout->width + x]);
    for (y = 25; y <= 28; y++)
        for (x = 28; x <= 31; x++)
            MapGridSetMetatileEntryAt(x + MAP_OFFSET, y + MAP_OFFSET, layout->map[y * layout->width + x]);
}

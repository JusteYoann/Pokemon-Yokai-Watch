#include "global.h"
#include "yokai_champions.h"
#include "battle.h"
#include "battle_anim.h"
#include "battle_setup.h"
#include "pokemon.h"
#include "constants/trainers.h"
#include "constants/opponents.h"
#include "constants/event_objects.h"
#include "constants/maps.h"
#include "constants/moves.h"

// Battle-local presentation only. No SaveBlock or global species entry changes.
static EWRAM_DATA bool8 sColossusAnnounced = FALSE;
static const u8 sKatie[] = _("KATIE");
static const u8 sNathan[] = _("NATHAN");
static const u8 sNathaniel[] = _("NATHANIEL");
static const u8 sMichael[] = _("MICHAEL");
static const u8 sColossus[] = _("Z. COLOSSE");
static const u8 sPierreSeed[] = _("PIERRE");
static const u8 sMorganeSeed[] = _("MORGANE");

// Native party generation hashes the trainer name into each personality/nature.
// Renaming these two trainers must not silently change their approved statistics.
const u8 *YokaiChampionPartySeedName(u16 trainer)
{
    if (trainer == TRAINER_LEADER_BROCK) return sPierreSeed;
    if (trainer == TRAINER_LEADER_KOGA) return sMorganeSeed;
    return gTrainers[trainer].trainerName;
}

const u8 *YokaiChampionName(u16 trainer)
{
    if (trainer == TRAINER_LEADER_MISTY)
        return gSaveBlock2Ptr->playerGender == FEMALE ? sNathan : sKatie;
    if (trainer == TRAINER_LEADER_BLAINE)
        return gSaveBlock2Ptr->playerGender == FEMALE ? sMichael : sNathaniel;
    return gTrainers[trainer].trainerName;
}

u8 YokaiChampionPortrait(u16 trainer)
{
    if (trainer == TRAINER_LEADER_MISTY)
        return gSaveBlock2Ptr->playerGender == FEMALE ? TRAINER_PIC_RED : TRAINER_PIC_LEAF;
    if (trainer == TRAINER_LEADER_BLAINE)
        return gSaveBlock2Ptr->playerGender == FEMALE ? TRAINER_PIC_YOKAI_MICHAEL : TRAINER_PIC_YOKAI_NATHANIEL;
    return gTrainers[trainer].trainerPic;
}

bool8 YokaiChampionFemale(u16 trainer)
{
    if (trainer == TRAINER_LEADER_MISTY)
        return gSaveBlock2Ptr->playerGender != FEMALE;
    return (gTrainers[trainer].encounterMusic_gender & F_TRAINER_FEMALE) != 0;
}

// Resolve at every native graphics lookup, including restored live save objects.
// The native local IDs, coordinates and graphics fields remain save-compatible.
u8 YokaiChampionObjectGfx(u8 graphicsId)
{
    u16 map;
    if (gSaveBlock1Ptr == NULL || gSaveBlock2Ptr == NULL) return graphicsId;
    map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    if (map == MAP_PEWTER_CITY_GYM && graphicsId == OBJ_EVENT_GFX_BROCK)
        return OBJ_EVENT_GFX_YOKAI_WYATT;
    if (map == MAP_CERULEAN_CITY_GYM && graphicsId == OBJ_EVENT_GFX_MISTY)
        return gSaveBlock2Ptr->playerGender == FEMALE ? OBJ_EVENT_GFX_YOKAI_NATHAN : OBJ_EVENT_GFX_YOKAI_KATIE;
    if (map == MAP_VERMILION_CITY_GYM && graphicsId == OBJ_EVENT_GFX_LT_SURGE)
        return OBJ_EVENT_GFX_ARIANE;
    if (map == MAP_SAFFRON_CITY_GYM && graphicsId == OBJ_EVENT_GFX_SABRINA)
        return OBJ_EVENT_GFX_YOKAI_DOMNISCIAN;
    if (map == MAP_FUCHSIA_CITY_GYM && graphicsId == OBJ_EVENT_GFX_KOGA)
        return OBJ_EVENT_GFX_YOKAI_BERENICE;
    if (map == MAP_POKEMON_LEAGUE_LORELEIS_ROOM && graphicsId == OBJ_EVENT_GFX_LORELEI)
        return OBJ_EVENT_GFX_YOKAI_ZAZEL;
    if (map == MAP_POKEMON_LEAGUE_BRUNOS_ROOM && graphicsId == OBJ_EVENT_GFX_BRUNO)
        return OBJ_EVENT_GFX_YOKAI_ENMA_ANCIEN;
    if (map == MAP_POKEMON_LEAGUE_AGATHAS_ROOM && graphicsId == OBJ_EVENT_GFX_AGATHA)
        return OBJ_EVENT_GFX_YOKAI_ORQANOS;
    if (map == MAP_POKEMON_LEAGUE_LANCES_ROOM && graphicsId == OBJ_EVENT_GFX_LANCE)
        return OBJ_EVENT_GFX_YOKAI_NYADA;
    if (map == MAP_CINNABAR_ISLAND_GYM && graphicsId == OBJ_EVENT_GFX_BLAINE)
        return gSaveBlock2Ptr->playerGender == FEMALE ? OBJ_EVENT_GFX_YOKAI_MICHAEL : OBJ_EVENT_GFX_YOKAI_NATHANIEL;
    return graphicsId;
}

u8 YokaiChampionOrderedPartySize(void)
{
    if (!(gBattleTypeFlags & BATTLE_TYPE_TRAINER)) return 0;
    switch (gTrainerBattleOpponent_A)
    {
    case TRAINER_LEADER_MISTY: return 3;
    case TRAINER_LEADER_LT_SURGE:
    case TRAINER_LEADER_ERIKA: return 4;
    case TRAINER_LEADER_BLAINE:
    case TRAINER_ELITE_FOUR_LORELEI:
    case TRAINER_ELITE_FOUR_LORELEI_2:
    case TRAINER_ELITE_FOUR_BRUNO:
    case TRAINER_ELITE_FOUR_BRUNO_2:
    case TRAINER_ELITE_FOUR_AGATHA:
    case TRAINER_ELITE_FOUR_AGATHA_2:
    case TRAINER_ELITE_FOUR_LANCE:
    case TRAINER_ELITE_FOUR_LANCE_2: return 6;
    }
    return 0;
}

void YokaiChampionPrepareParty(u16 trainer)
{
    static const u8 fields[] = {MON_DATA_MAX_HP, MON_DATA_ATK, MON_DATA_DEF, MON_DATA_SPEED, MON_DATA_SPATK, MON_DATA_SPDEF};
    static const u16 stats[] = {140, 80, 80, 25, 36, 54};
    static const u16 moves[] = {MOVE_POUND, MOVE_ROCK_THROW, MOVE_LEER, MOVE_ASTONISH};
    u8 i;
    if (trainer != TRAINER_LEADER_ERIKA) return;
    SetMonData(&gEnemyParty[3], MON_DATA_NICKNAME, sColossus);
    for (i = 0; i < 6; i++) SetMonData(&gEnemyParty[3], fields[i], &stats[i]);
    SetMonData(&gEnemyParty[3], MON_DATA_HP, &stats[0]);
    for (i = 0; i < 4; i++) SetMonMoveSlot(&gEnemyParty[3], moves[i], i);
}

void YokaiChampionResetBattle(void) { sColossusAnnounced = FALSE; }

bool8 YokaiChampionIsColossus(u8 battler)
{
    return (gBattleTypeFlags & BATTLE_TYPE_TRAINER)
        && gTrainerBattleOpponent_A == TRAINER_LEADER_ERIKA
        && battler < gBattlersCount && GetBattlerSide(battler) == B_SIDE_OPPONENT
        && gBattlerPartyIndexes[battler] == 3;
}

bool8 YokaiChampionAnnounceColossus(u8 battler)
{
    if (!YokaiChampionIsColossus(battler) || sColossusAnnounced) return FALSE;
    sColossusAnnounced = TRUE;
    return TRUE;
}

u16 YokaiChampionExpYield(u8 battler, u16 normalYield)
{
    return YokaiChampionIsColossus(battler) ? 156 : normalYield;
}

u8 YokaiChampionFameObjectGfx(u8 graphicsId)
{
    switch (graphicsId)
    {
    case OBJ_EVENT_GFX_BROCK: return OBJ_EVENT_GFX_YOKAI_WYATT;
    case OBJ_EVENT_GFX_MISTY: return gSaveBlock2Ptr->playerGender == FEMALE ? OBJ_EVENT_GFX_YOKAI_NATHAN : OBJ_EVENT_GFX_YOKAI_KATIE;
    case OBJ_EVENT_GFX_LT_SURGE: return OBJ_EVENT_GFX_ARIANE;
    case OBJ_EVENT_GFX_SABRINA: return OBJ_EVENT_GFX_YOKAI_DOMNISCIAN;
    case OBJ_EVENT_GFX_KOGA: return OBJ_EVENT_GFX_YOKAI_BERENICE;
    case OBJ_EVENT_GFX_LORELEI: return OBJ_EVENT_GFX_YOKAI_ZAZEL;
    case OBJ_EVENT_GFX_BRUNO: return OBJ_EVENT_GFX_YOKAI_ENMA_ANCIEN;
    case OBJ_EVENT_GFX_AGATHA: return OBJ_EVENT_GFX_YOKAI_ORQANOS;
    case OBJ_EVENT_GFX_LANCE: return OBJ_EVENT_GFX_YOKAI_NYADA;
    case OBJ_EVENT_GFX_BLAINE: return gSaveBlock2Ptr->playerGender == FEMALE ? OBJ_EVENT_GFX_YOKAI_MICHAEL : OBJ_EVENT_GFX_YOKAI_NATHANIEL;
    }
    return graphicsId;
}

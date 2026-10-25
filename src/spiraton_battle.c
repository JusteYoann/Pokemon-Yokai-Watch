#include "global.h"
#include "gflib.h"
#include "battle.h"
#include "util.h"
#include "battle_main.h"
#include "battle_util.h"
#include "battle_controllers.h"
#include "battle_message.h"
#include "battle_interface.h"
#include "battle_anim.h"
#include "pokemon.h"
#include "decompress.h"
#include "string_util.h"
#include "spiraton_core.h"
#include "spiraton_config.h"
#include "spiraton_battle.h"
#include "constants/opponents.h"
#include "constants/pokemon.h"
#include "constants/moves.h"
#include "constants/battle_string_ids.h"

/* Eight-life adapter; true-form graphics are owned by the opponent battler. */
static EWRAM_DATA struct SpiratonState sBoss = {0};
static EWRAM_DATA bool8 sArmed = FALSE;
static EWRAM_DATA bool8 sRunning = FALSE;
static EWRAM_DATA bool8 sFirst = FALSE;
static EWRAM_DATA u8 sStep = 0;
static EWRAM_DATA u16 sWait = 0;
static EWRAM_DATA u8 sOldAttacker = 0, sOldTarget = 0;
static EWRAM_DATA u16 sOldMove = 0;
static EWRAM_DATA void (*sResume)(void) = NULL;
const u8 gSpiratonBattleName[] = _("DON SPIRATION");
const u8 gSpiratonHealthboxName[] = _("D. SPIRATION");

void SpiratonBattleArmPrototype(void) { sArmed = TRUE; }
bool8 SpiratonBattlePrototypeArmed(void) { return sArmed; }
void SpiratonBattleReset(void)
{
    sRunning = sArmed && gTrainerBattleOpponent_A == TRAINER_DON_SPIRATON_PROTOTYPE
        && (gBattleTypeFlags & BATTLE_TYPE_TRAINER)
        && !(gBattleTypeFlags & (BATTLE_TYPE_LINK | BATTLE_TYPE_DOUBLE));
    sArmed = FALSE;
    sBoss = (struct SpiratonState){0};
    sFirst = sRunning;
    sStep = 0;
}
bool8 SpiratonBattlePresentationIsBoss(u8 battler)
{
    /* Initial HUD tiles can be drawn before BattleInit consumes the arm flag. */
    return battler == 1 && gTrainerBattleOpponent_A == TRAINER_DON_SPIRATON_PROTOTYPE
        && (sArmed || sRunning);
}
bool8 SpiratonBattleIsBoss(u8 battler)
{
    return sRunning && gMain.inBattle && battler == 1
        && gTrainerBattleOpponent_A == TRAINER_DON_SPIRATON_PROTOTYPE;
}
bool8 SpiratonBattlePending(u8 battler)
{
    return SpiratonBattleIsBoss(battler) && sBoss.pending;
}

static void VisibleOpponent(struct SpiratonVisibleOpponent *opponent)
{
    const struct BattlePokemon *mon = &gBattleMons[GetBattlerAtPosition(B_POSITION_PLAYER_LEFT)];
    *opponent = (struct SpiratonVisibleOpponent){0};
    opponent->species = mon->species;
    opponent->level = mon->level;
    opponent->types[0] = mon->type1;
    opponent->types[1] = mon->type2;
    /* Revealed-move tracking is deliberately not inferred from its moves[].
     * The core accepts a public history; the first adapter leaves it empty. */
}

static void ApplyForm(void)
{
    struct BattlePokemon *mon = &gBattleMons[1];
    struct Pokemon *party = &gEnemyParty[gBattlerPartyIndexes[1]];
    u8 i;
    gActiveBattler = 1;
    FaintClearSetData();
    CreateMon(party, sBoss.form.species, sBoss.form.level, SPIRATON_NEUTRAL_IV, TRUE, 0, OT_ID_PRESET, 0x1234);
    mon->species = sBoss.form.species;
    mon->hp = mon->maxHP = sBoss.form.hp;
    mon->attack = sBoss.form.attack;
    mon->defense = sBoss.form.defense;
    mon->speed = sBoss.form.speed;
    mon->spAttack = sBoss.form.spAttack;
    mon->spDefense = sBoss.form.spDefense;
    mon->level = sBoss.form.level;
    mon->type1 = sBoss.form.types[0];
    mon->type2 = sBoss.form.types[1];
    mon->ability = sBoss.form.ability;
    mon->abilityNum = 0;
    mon->item = 0;
    mon->status1 = mon->status2 = 0;
    mon->personality = 0;
    mon->otId = 0x1234; // Hardy, normal palette; 0/0 would accidentally be shiny.
    mon->friendship = GetMonData(party, MON_DATA_FRIENDSHIP, NULL);
    mon->experience = GetMonData(party, MON_DATA_EXP, NULL);
    mon->hpIV = mon->attackIV = mon->defenseIV = SPIRATON_NEUTRAL_IV;
    mon->speedIV = mon->spAttackIV = mon->spDefenseIV = SPIRATON_NEUTRAL_IV;
    mon->ppBonuses = 0;
    for (i = 0; i < 4; i++)
    {
        mon->moves[i] = sBoss.form.moves[i];
        mon->pp[i] = gBattleMoves[mon->moves[i]].pp;
        SetMonMoveSlot(party, mon->moves[i], i);
    }
    GetMonData(party, MON_DATA_NICKNAME, mon->nickname);
    gHitMarker &= ~HITMARKER_FAINTED(1);
    gAbsentBattlerFlags &= ~gBitTable[1];
    gBattleStruct->givenExpMons &= ~gBitTable[gBattlerPartyIndexes[1]];
}

void SpiratonBattleBegin(void)
{
    struct SpiratonVisibleOpponent target;
    if (!sRunning)
        return;
    VisibleOpponent(&target);
    if (!SpiratonCoreStart(&sBoss, SPIRATON_FIRST_SPECIES, &target))
    {
        sRunning = FALSE;
        return;
    }
    ApplyForm();
    UpdateHealthboxAttribute(gHealthboxSpriteIds[1], &gEnemyParty[gBattlerPartyIndexes[1]], HEALTHBOX_ALL);
}

bool8 SpiratonBattleIgnoreFaint(u8 battler)
{
    if (!SpiratonBattleIsBoss(battler))
        return FALSE;
    if (gBattleMons[battler].hp == 0 && !sBoss.pending && !sBoss.defeated)
        SpiratonCoreDamage(&sBoss, sBoss.hp);
    return sBoss.pending;
}

static void TransformStep(void)
{
    if (gBattleControllerExecFlags)
        return;
    if (sWait)
    {
        --sWait;
        return;
    }
    gActiveBattler = gBattlerAttacker = 1;
    gBattlerTarget = 0;
    if (sStep == 0)
    {
        u16 cure = 0;
        u32 status = gBattleMons[1].status1;
        if (status & STATUS1_BURN) cure = STRINGID_SPIRATON_CURE_BURN;
        else if (status & (STATUS1_POISON | STATUS1_TOXIC_POISON)) cure = STRINGID_SPIRATON_CURE_POISON;
        else if (status & STATUS1_PARALYSIS) cure = STRINGID_SPIRATON_CURE_PARALYSIS;
        else if (status & STATUS1_SLEEP) cure = STRINGID_SPIRATON_CURE_SLEEP;
        else if (status & STATUS1_FREEZE) cure = STRINGID_SPIRATON_CURE_FREEZE;
        ++sStep;
        if (cure != 0)
        {
            PrepareStringBattle(cure, 1);
            sWait = 90;
            return;
        }
    }
    if (sStep == 1)
    {
        ApplyForm();
        gBattlerAttacker = 1;
        gBattlerTarget = 0;
        BtlController_EmitMoveAnimation(BUFFER_A, MOVE_TRANSFORM, 0, 0, 0, 0, &gDisableStructs[1]);
        MarkBattlerForControllerExec(1);
        ++sStep;
        return;
    }
    if (sStep == 2)
    {
        // Morphing keeps a white-tinted palette; restore only this boss once its animation ends.
        LoadCompressedPalette(GetMonSpritePalFromSpeciesAndPersonality(sBoss.form.species,
            gBattleMons[1].otId, gBattleMons[1].personality), OBJ_PLTT_ID(1), PLTT_SIZE_4BPP);
        UpdateHealthboxAttribute(gHealthboxSpriteIds[1], &gEnemyParty[gBattlerPartyIndexes[1]], HEALTHBOX_ALL);
        PREPARE_SPECIES_BUFFER(gBattleTextBuff1, sBoss.form.species);
        PrepareStringBattle(STRINGID_SPIRATON_TRANSFORM, 1);
        ++sStep;
        sWait = 100;
        return;
    }
    gBattlerAttacker = sOldAttacker;
    gBattlerTarget = sOldTarget;
    gCurrentMove = sOldMove;
    gBattleMainFunc = sResume;
}

static void BeginTransform(void)
{
    sResume = gBattleMainFunc;
    sOldAttacker = gBattlerAttacker;
    sOldTarget = gBattlerTarget;
    sOldMove = gCurrentMove;
    sStep = 0;
    sWait = 0;
    gBattleMainFunc = TransformStep;
}

bool8 SpiratonBattleFirstTurn(void)
{
    if (!SpiratonBattleIsBoss(1) || !sFirst || gBattleControllerExecFlags)
        return FALSE;
    sFirst = FALSE;
    BeginTransform();
    return TRUE;
}

bool8 SpiratonBattleEndTurn(void)
{
    struct SpiratonVisibleOpponent target;
    if (!SpiratonBattlePending(1) || gBattleOutcome || gBattleControllerExecFlags)
        return FALSE;
    VisibleOpponent(&target);
    if (!SpiratonCoreEndTurn(&sBoss, &target))
        return FALSE;
    BeginTransform();
    return TRUE;
}

u16 SpiratonBattleTransformSpecies(u8 battler)
{
    return SpiratonBattleIsBoss(battler) ? sBoss.form.species : 0;
}
u32 SpiratonBattleInspect(u8 field)
{
    return SpiratonCoreInspect(&sBoss, field);
}

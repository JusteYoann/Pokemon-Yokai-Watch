#include "global.h"
#include "spiraton_core.h"
#include "data/spiraton_catalogue.h"

/* No battle globals: input is the visible active opponent only.
 * Neutral nature, 24 IVs, zero EVs, first native ability for every candidate.
 * Native Generation III physical/special split (type < 9). */
static u16 Stat(u8 base, u8 level)
{
    return ((2 * base + SPIRATON_NEUTRAL_IV) * level) / 100 + 5;
}

static bool8 ValidOpponent(const struct SpiratonVisibleOpponent *opponent)
{
    return opponent != NULL && opponent->species > 0 && opponent->species <= 151
        && opponent->level > 0 && opponent->level <= 100
        && opponent->types[0] < 18 && opponent->types[1] < 18;
}

static bool8 Used(const struct SpiratonState *state, u16 species)
{
    return (state->used[(species - 1) / 8] & (1 << ((species - 1) % 8))) != 0;
}

static void MarkUsed(struct SpiratonState *state, u16 species)
{
    state->used[(species - 1) / 8] |= 1 << ((species - 1) % 8);
}

bool8 SpiratonCoreMoveLegal(u16 species, u8 level, u16 move)
{
    u16 i;
    const struct SpiratonSpecies *entry;
    if (species == 0 || species > 151 || move == 0 || level > 100)
        return FALSE;
    entry = &sSpiratonSpecies[species];
    for (i = 0; i < entry->count; i++)
    {
        const struct SpiratonLegalMove *m = &sSpiratonLegalMoves[entry->start + i];
        if (m->move == move && m->level <= level)
            return TRUE;
    }
    return FALSE;
}

static u32 Effectiveness(u8 type, const u8 *types)
{
    u32 mult = sSpiratonTypeChart[type][types[0]];
    if (types[0] != types[1])
        mult = (mult * sSpiratonTypeChart[type][types[1]] * 205U) >> 11;
    return mult;
}

/* Cache target estimates once, rather than divide for every candidate move.
 * Candidate phase stats are read-only ROM values derived from the original data.
 * The Q16 damage model is deterministic and bounded below 32-bit overflow for
 * levels1..100 and this catalogue; it remains an explicit heuristic, not a
 * claim to reproduce every damage effect, nature, item or hidden ability. */
struct SpiratonEvaluation
{
    u16 defense, spDefense, speed;
    u32 inverseDefense, inverseSpDefense;
    u8 effectiveness[18];
};

static void EvaluateTarget(struct SpiratonEvaluation *result,
                           const struct SpiratonVisibleOpponent *opponent)
{
    const struct SpiratonSpecies *target = &sSpiratonSpecies[opponent->species];
    u8 i;
    result->defense = Stat(target->stats[2], opponent->level);
    result->spDefense = Stat(target->stats[5], opponent->level);
    result->speed = Stat(target->stats[3], opponent->level);
    result->inverseDefense = 65536U / result->defense;
    result->inverseSpDefense = 65536U / result->spDefense;
    for (i = 0; i < 18; i++)
        result->effectiveness[i] = Effectiveness(i, opponent->types);
}

static u32 RankedMoveScore(u16 move, const struct SpiratonForm *form,
                           const struct SpiratonEvaluation *target, const u32 *factors)
{
    const struct SpiratonMove *m = &sSpiratonMoves[move];
    u32 damage;
    if (m->power <= 1)
        return 0;
    damage = (((m->power * factors[m->type < 9 ? 0 : 1]) >> 16) + 2)
           * target->effectiveness[m->type];
    if (m->type == form->types[0] || m->type == form->types[1])
        damage = damage * 3 / 2;
    /* Accuracy is pre-scaled with a bounded reciprocal: no software division
     * in the hot move loop. Rounding differences belong to the scoring model. */
    if (m->accuracy != 0 && m->accuracy != 100)
        damage = (damage * ((m->accuracy * 656U) >> 8)) >> 8;
    if (m->priority > 0)
        damage = (damage * 282U) >> 8;
    return damage;
}

static void BuildRankedForm(struct SpiratonForm *form, u16 species, u8 level,
                            const struct SpiratonEvaluation *target, u32 *bestMoveScore, bool8 selectionOnly)
{
    const struct SpiratonSpecies *entry = &sSpiratonSpecies[species];
    u32 scores[4] = {0};
    u32 factors[2];
    u16 stats[6];
    u16 i;
    u8 j, k;
    *form = (struct SpiratonForm){0};
    form->species = species;
    form->level = level;
    if (level >= 56 && level <= 63)
    {
        for (j = 0; j < 6; j++)
            stats[j] = sSpiratonPhaseStats[level - 56][species][j];
    }
    else
    {
        for (j = 0; j < 6; j++)
            stats[j] = Stat(entry->stats[j], level);
        stats[0] += level + 5;
    }
    form->hp = stats[0];
    form->attack = stats[1];
    form->defense = stats[2];
    form->speed = stats[3];
    form->spAttack = stats[4];
    form->spDefense = stats[5];
    form->types[0] = entry->types[0];
    form->types[1] = entry->types[1];
    form->ability = entry->ability;
    if (level >= 56 && level <= 63)
    {
        factors[0] = (sSpiratonPhaseStats[level - 56][species][6] * target->inverseDefense) >> 8;
        factors[1] = (sSpiratonPhaseStats[level - 56][species][7] * target->inverseSpDefense) >> 8;
    }
    else
    {
        factors[0] = ((2 * level / 5 + 2) * form->attack * 65536U) / (target->defense * 50);
        factors[1] = ((2 * level / 5 + 2) * form->spAttack * 65536U) / (target->spDefense * 50);
    }
#ifndef SPIRATON_BRUTE_SELECTION
    if (selectionOnly && level >= 56 && level <= 63)
    {
        const struct SpiratonThreatRange *range = &sSpiratonThreatRanges[level - 56][species];
        *bestMoveScore = 0;
        for (i = 0; i < range->count; i++)
        {
            u32 score = RankedMoveScore(sSpiratonThreatMoves[range->start + i], form, target, factors);
            if (score > *bestMoveScore)
                *bestMoveScore = score;
        }
        return;
    }
#else
    (void)selectionOnly;
#endif
    for (i = 0; i < entry->count; i++)
    {
        const struct SpiratonLegalMove *m = &sSpiratonLegalMoves[entry->start + i];
        u32 score;
        if (m->level > level)
            continue;
        score = RankedMoveScore(m->move, form, target, factors);
        for (j = 0; j < 4; j++)
        {
            if (form->moves[j] == 0 || score > scores[j]
                || (score == scores[j] && m->move < form->moves[j]))
            {
                for (k = 3; k > j; k--)
                {
                    scores[k] = scores[k - 1];
                    form->moves[k] = form->moves[k - 1];
                }
                scores[j] = score;
                form->moves[j] = m->move;
                break;
            }
        }
    }
    *bestMoveScore = scores[0];
}

void SpiratonCoreBuildForm(struct SpiratonForm *form, u16 species, u8 level,
                          const struct SpiratonVisibleOpponent *opponent)
{
    struct SpiratonEvaluation target;
    u32 bestMoveScore;
    *form = (struct SpiratonForm){0};
    if (species == 0 || species > 151 || level < 1 || level > 100 || !ValidOpponent(opponent))
        return;
    EvaluateTarget(&target, opponent);
    BuildRankedForm(form, species, level, &target, &bestMoveScore, FALSE);
}

u16 SpiratonCoreSelect(const struct SpiratonState *state,
                      const struct SpiratonVisibleOpponent *opponent)
{
    u16 species, best = 0;
    u32 bestScore = 0;
    struct SpiratonEvaluation target;
    if (!state->active || !state->pending || state->phase >= 7 || !ValidOpponent(opponent))
        return 0;
    EvaluateTarget(&target, opponent);
    for (species = 1; species <= 151; species++)
    {
        struct SpiratonForm form;
        u32 threat, pressure, bulk, score;
        u8 i;
        if (Used(state, species))
            continue;
        BuildRankedForm(&form, species, 57 + state->phase, &target, &threat, TRUE);
        pressure = Effectiveness(opponent->types[0], form.types)
                 + Effectiveness(opponent->types[1], form.types);
        for (i = 0; i < 4; i++)
        {
            u16 move = opponent->revealedMoves[i];
            if (move < ARRAY_COUNT(sSpiratonMoves) && sSpiratonMoves[move].power > 1)
                pressure += Effectiveness(sSpiratonMoves[move].type, form.types);
        }
        bulk = (form.hp * (form.defense + form.spDefense) * sSpiratonBulkRecip[pressure]) >> 16;
        score = threat * 16 + bulk;
        if (form.speed > target.speed)
            score += threat * 4;
        if (best == 0 || score > bestScore)
        {
            bestScore = score;
            best = species;
        }
    }
    return best;
}

bool8 SpiratonCoreStart(struct SpiratonState *state, u16 firstSpecies,
                       const struct SpiratonVisibleOpponent *opponent)
{
    *state = (struct SpiratonState){0};
    if (!ValidOpponent(opponent) || firstSpecies == 0 || firstSpecies > 151)
        return FALSE;
    SpiratonCoreBuildForm(&state->form, firstSpecies, 56, opponent);
    state->hp = state->form.hp;
    state->active = TRUE;
    MarkUsed(state, firstSpecies);
    return TRUE;
}

u16 SpiratonCoreDamage(struct SpiratonState *state, u32 damage)
{
    u16 dealt;
    if (!state->active || state->pending || state->defeated)
        return 0;
    dealt = damage > state->hp ? state->hp : damage;
    state->hp -= dealt;
    if (state->hp == 0)
    {
        if (state->phase == 7)
        {
            state->defeated = TRUE;
            state->active = FALSE;
        }
        else
            state->pending = TRUE;
    }
    return dealt;
}

bool8 SpiratonCoreEndTurn(struct SpiratonState *state,
                         const struct SpiratonVisibleOpponent *opponent)
{
    u16 species = SpiratonCoreSelect(state, opponent);
    if (species == 0)
        return FALSE;
    ++state->phase;
    SpiratonCoreBuildForm(&state->form, species, 56 + state->phase, opponent);
    state->hp = state->form.hp;
    state->pending = FALSE;
    MarkUsed(state, species);
    return TRUE;
}

/* Stable scalar diagnostics across agbcc and host struct padding conventions. */
u32 SpiratonCoreInspect(const struct SpiratonState *state, u8 field)
{
    switch (field)
    {
    case 0: return state->form.species;
    case 1: return state->form.level;
    case 2: return state->phase;
    case 3: return state->hp;
    case 4: return state->pending;
    case 5: return state->defeated;
    default: return sizeof(*state);
    }
}

/* Public diagnostic of the default type chart, including Ghost immunities
 * following the native Foresight sentinel. Foresight itself is a future public
 * field-effect input, not an excuse to omit those baseline immunities. */
u32 SpiratonCoreTypeMultiplier(u8 attackingType, u8 type1, u8 type2)
{
    u8 types[2];
    if (attackingType >= 18 || type1 >= 18 || type2 >= 18)
        return 0;
    types[0] = type1;
    types[1] = type2;
    return Effectiveness(attackingType, types);
}

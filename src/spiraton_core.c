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
        mult = mult * sSpiratonTypeChart[type][types[1]] / 10;
    return mult;
}

/* An explicit threat model, not an omniscient damage calculator. It does not
 * inspect the target's IVs, nature, EVs, held item, ability or hidden moves.
 * Power-one special formulas and variable-type attacks are excluded from the
 * offensive score rather than pretending their nominal power is real damage. */
static u32 MoveScore(u16 move, u16 species, u8 level,
                     const struct SpiratonVisibleOpponent *opponent)
{
    const struct SpiratonMove *m = &sSpiratonMoves[move];
    const struct SpiratonSpecies *own = &sSpiratonSpecies[species];
    const struct SpiratonSpecies *target = &sSpiratonSpecies[opponent->species];
    u32 damage, mult;
    u16 attack, defense;
    if (m->power <= 1)
        return 0;
    mult = Effectiveness(m->type, opponent->types);
    attack = Stat(own->stats[m->type < 9 ? 1 : 4], level);
    defense = Stat(target->stats[m->type < 9 ? 2 : 5], opponent->level);
    damage = (((2 * level / 5 + 2) * m->power * attack / defense) / 50 + 2) * mult;
    if (m->type == own->types[0] || m->type == own->types[1])
        damage = damage * 3 / 2;
    damage = damage * (m->accuracy == 0 ? 100 : m->accuracy) / 100;
    if (m->priority > 0)
        damage = damage * 11 / 10;
    return damage;
}

void SpiratonCoreBuildForm(struct SpiratonForm *form, u16 species, u8 level,
                          const struct SpiratonVisibleOpponent *opponent)
{
    const struct SpiratonSpecies *entry;
    u32 scores[4] = {0};
    u16 i;
    u8 j, k;
    *form = (struct SpiratonForm){0};
    if (species == 0 || species > 151 || level < 1 || level > 100 || !ValidOpponent(opponent))
        return;
    entry = &sSpiratonSpecies[species];
    form->species = species;
    form->level = level;
    form->hp = Stat(entry->stats[0], level) + level + 5;
    form->attack = Stat(entry->stats[1], level);
    form->defense = Stat(entry->stats[2], level);
    form->speed = Stat(entry->stats[3], level);
    form->spAttack = Stat(entry->stats[4], level);
    form->spDefense = Stat(entry->stats[5], level);
    form->types[0] = entry->types[0];
    form->types[1] = entry->types[1];
    form->ability = entry->ability;
    for (i = 0; i < entry->count; i++)
    {
        const struct SpiratonLegalMove *m = &sSpiratonLegalMoves[entry->start + i];
        u32 score;
        if (m->level > level)
            continue;
        score = MoveScore(m->move, species, level, opponent);
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
}

u16 SpiratonCoreSelect(const struct SpiratonState *state,
                      const struct SpiratonVisibleOpponent *opponent)
{
    u16 species, best = 0;
    u32 bestScore = 0;
    if (!state->active || !state->pending || state->phase >= 7 || !ValidOpponent(opponent))
        return 0;
    for (species = 1; species <= 151; species++)
    {
        struct SpiratonForm form;
        const struct SpiratonSpecies *target = &sSpiratonSpecies[opponent->species];
        u32 threat, pressure = 0, bulk, score;
        u8 i;
        if (Used(state, species))
            continue;
        SpiratonCoreBuildForm(&form, species, 57 + state->phase, opponent);
        threat = MoveScore(form.moves[0], species, form.level, opponent);
        /* Resistances to the active species' public types; revealed offensive
         * move types add pressure. No inferred access to its full moveset. */
        pressure = Effectiveness(opponent->types[0], form.types)
                 + Effectiveness(opponent->types[1], form.types);
        for (i = 0; i < 4; i++)
        {
            u16 move = opponent->revealedMoves[i];
            if (move < ARRAY_COUNT(sSpiratonMoves) && sSpiratonMoves[move].power > 1)
                pressure += Effectiveness(sSpiratonMoves[move].type, form.types);
        }
        bulk = form.hp * (form.defense + form.spDefense) / (20 + pressure);
        score = threat * 16 + bulk;
        if (form.speed > Stat(target->stats[3], opponent->level))
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

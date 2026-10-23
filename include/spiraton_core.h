#ifndef GUARD_SPIRATON_CORE_H
#define GUARD_SPIRATON_CORE_H

/* Pure, deterministic combat rules. This interface cannot inspect a party,
 * items, unrevealed moves, selected actions or the player's private stats. */
#define SPIRATON_PHASES 8
#define SPIRATON_SPECIES_COUNT 151
#define SPIRATON_NEUTRAL_IV 24

struct SpiratonVisibleOpponent
{
    u16 species;
    u8 level;
    u8 types[2];
    u16 revealedMoves[4];
};

struct SpiratonForm
{
    u16 species;
    u16 moves[4];
    u16 hp, attack, defense, speed, spAttack, spDefense;
    u8 level;
    u8 types[2];
    u8 ability;
};

struct SpiratonState
{
    struct SpiratonForm form;
    u16 hp;
    u8 used[19];
    u8 phase; /* zero based: level = 56 + phase */
    bool8 active, pending, defeated;
};

bool8 SpiratonCoreStart(struct SpiratonState *state, u16 firstSpecies,
                       const struct SpiratonVisibleOpponent *opponent);
u16 SpiratonCoreDamage(struct SpiratonState *state, u32 damage);
bool8 SpiratonCoreEndTurn(struct SpiratonState *state,
                         const struct SpiratonVisibleOpponent *opponent);
bool8 SpiratonCoreMoveLegal(u16 species, u8 level, u16 move);
u16 SpiratonCoreSelect(const struct SpiratonState *state,
                      const struct SpiratonVisibleOpponent *opponent);
void SpiratonCoreBuildForm(struct SpiratonForm *form, u16 species, u8 level,
                          const struct SpiratonVisibleOpponent *opponent);
u32 SpiratonCoreTypeMultiplier(u8 attackingType, u8 type1, u8 type2);
u32 SpiratonCoreInspect(const struct SpiratonState *state, u8 field);
#endif

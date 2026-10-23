#include "global.h"
#include "spiraton_core.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    struct SpiratonState state, copy;
    struct SpiratonVisibleOpponent opponent = {1, 60, {10, 10}, {0}};
    u16 target, species[8];
    unsigned cases = 0;
    assert(SpiratonCoreTypeMultiplier(0, 7, 7) == 0); /* Normal/Ghost */
    assert(SpiratonCoreTypeMultiplier(1, 7, 7) == 0); /* Fighting/Ghost */
    assert(SpiratonCoreTypeMultiplier(13, 4, 4) == 0); /* Electric/Ground */
    assert(SpiratonCoreTypeMultiplier(4, 2, 2) == 0); /* Ground/Flying */
    assert(SpiratonCoreTypeMultiplier(10, 12, 6) == 40); /* Fire/Grass+Bug */
    assert(!SpiratonCoreStart(&state, 0, &opponent));
    opponent.species = 152;
    assert(!SpiratonCoreStart(&state, 52, &opponent));
    opponent.species = 1;
    for (target = 1; target <= 151; target++)
    {
        u8 phase, i, j;
        opponent.species = target;
        opponent.types[0] = target % 18;
        opponent.types[1] = (target / 18) % 18;
        assert(SpiratonCoreStart(&state, 52, &opponent));
        copy = state;
        assert(!SpiratonCoreEndTurn(&state, &opponent));
        assert(memcmp(&copy, &state, sizeof(state)) == 0);
        for (phase = 0; phase < 8; phase++)
        {
            species[phase] = state.form.species;
            assert(state.form.level == 56 + phase);
            assert(state.hp == state.form.hp && state.hp > 0);
            for (i = 0; i < phase; i++) assert(species[i] != species[phase]);
            for (i = 0; i < 4; i++)
            {
                assert(SpiratonCoreMoveLegal(species[phase], 56 + phase, state.form.moves[i]));
                for (j = 0; j < i; j++) assert(state.form.moves[i] != state.form.moves[j]);
            }
            assert(SpiratonCoreDamage(&state, 1) == 1);
            assert(!state.pending && !state.defeated);
            assert(SpiratonCoreDamage(&state, 1000000) == state.form.hp - 1);
            assert(state.hp == 0 && state.phase == phase);
            copy = state;
            assert(SpiratonCoreDamage(&state, 1000000) == 0);
            assert(memcmp(&copy, &state, sizeof(state)) == 0);
            if (phase < 7)
            {
                u16 expected;
                assert(state.pending && !state.defeated);
                expected = SpiratonCoreSelect(&state, &opponent);
                assert(expected && expected == SpiratonCoreSelect(&state, &opponent));
                assert(SpiratonCoreEndTurn(&state, &opponent));
                assert(state.form.species == expected);
            }
            else assert(state.defeated && !state.active && !state.pending);
            ++cases;
        }
        assert(!SpiratonCoreEndTurn(&state, &opponent));
    }
    /* Candidate selection must be responsive to the active opponent, while
     * having no API through which to read any bench or hidden battle action. */
    opponent.species = 1; opponent.types[0] = opponent.types[1] = 10;
    assert(SpiratonCoreStart(&state, 52, &opponent));SpiratonCoreDamage(&state, 9999);
    species[0] = SpiratonCoreSelect(&state, &opponent);
    opponent.species = 7; opponent.types[0] = opponent.types[1] = 11;
    species[1] = SpiratonCoreSelect(&state, &opponent);
    assert(species[0] != species[1]);
    printf("PASS: %u phase cases; 151 targets; legal distinct moves; no repeated forms; deterministic adaptive selection; state=%zu bytes\n", cases, sizeof(state));
    return 0;
}

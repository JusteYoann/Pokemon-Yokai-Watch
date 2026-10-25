#ifndef GUARD_POSTGAME_QUESTS_H
#define GUARD_POSTGAME_QUESTS_H
#include "global.h"
void PostgameSync(void);
void PostgameArmIntro(void);
void PostgameHaveFriends(void);
void PostgameGiveGift(void);
void PostgameGiveTicket(void);
struct Pokemon;
void PostgameMakeScientistShiny(struct Pokemon *mon);
#endif

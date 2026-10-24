#ifndef GUARD_TERRE_HEURE_H
#define GUARD_TERRE_HEURE_H
#include "global.h"
bool8 TerreHeureActive(void);
bool8 TerreHeureTryStep(void);
bool8 TerreHeureBlockWarp(u8 group, u8 num);
void TerreHeureUpdate(void);
void TerreHeurePalette(void);
void TerreHeureReload(void);
void TerreHeureBegin(void);
void TerreHeureRun(void);
void TerreHeureEnd(void);
void TerreHeureBattleResult(void);
void TerreHeureReward(void);
const struct ObjectEventTemplate *TerreHeureTemplate(u8 localId, u8 num, u8 group);

s16 TerreHeureFlashOverride(void);
void TerreHeureTier(void);

bool8 TerreHeureHideOrdinary(void);

void TerreHeureClock(void);

#endif // GUARD_TERRE_HEURE_H

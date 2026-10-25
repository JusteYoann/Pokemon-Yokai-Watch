#ifndef GUARD_TERRE_HEURE_H
#define GUARD_TERRE_HEURE_H
#include "global.h"
bool8 TerreHeureActive(void);
bool8 TerreHeureTryStep(void);
void TerreHeureInputStep(bool8 tookStep);
bool8 TerreHeureTrainerSightAllowed(void);
u8 TerreHeureEncounterChance(void);
bool8 TerreHeureBlockWarp(u8 group, u8 num);
void TerreHeureUpdate(void);
void TerreHeurePalette(void);
void TerreHeureFadeResidents(void);
void TerreHeureReload(void);
void TerreHeureBegin(void);
void TerreHeureRun(void);
void TerreHeureEnd(void);
void TerreHeureBlackout(void);
void TerreHeureBattleResult(void);
void TerreHeureReward(void);
const struct ObjectEventTemplate *TerreHeureTemplate(u8 localId, u8 num, u8 group);

s16 TerreHeureFlashOverride(void);
void TerreHeureTier(void);

bool8 TerreHeureHideOrdinary(void);

void TerreHeureClock(void);

void TerreHeureBattleStarting(void);
bool8 TerreHeureFogVisible(void);
u8 TerreHeureTransitionAmount(void);
void TerreHeureFogUpdate(void);
void TerreHeureFogClear(void);

#endif // GUARD_TERRE_HEURE_H

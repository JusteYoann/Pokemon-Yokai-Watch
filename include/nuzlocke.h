#ifndef GUARD_NUZLOCKE_H
#define GUARD_NUZLOCKE_H
#include "global.h"
#include "pokemon.h"
#define NUZLOCKE_SAVE_MAGIC 0x4E555A31
extern bool8 gNewGameNuzlocke;
bool8 NuzlockeEnabled(void);
void NuzlockeInit(void);
void NuzlockeBeginBattle(void);
bool8 NuzlockeIsDead(struct Pokemon *mon);
void NuzlockeMarkDead(struct Pokemon *mon);
bool8 NuzlockeBattleApplies(void);
bool8 NuzlockeCanCapture(struct Pokemon *mon);
void NuzlockeRecordCapture(struct Pokemon *mon);
void NuzlockeRecordOwned(struct Pokemon *mon);
u8 NuzlockeResolveParty(void);
void NuzlockeGameOver(void);
extern const u8 gText_NuzlockeCaptureBlocked[];
#endif

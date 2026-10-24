#ifndef GUARD_LAVANVILLE_H
#define GUARD_LAVANVILLE_H
#include "global.h"
bool8 IsLavanvilleNight(void);
bool8 LavanvilleNeedsTemplateRefresh(void);
void LavanvilleNightPalette(void);
struct ObjectEvent;
void LavanvilleZombieApproach(void);
u16 LavanvilleZombieStepDelay(struct ObjectEvent *object);
void LavanvilleStartZombieBattle(void);
void LavanvilleZombieImmunity(void);
u16 LavanvilleCheckZombieImmunity(void);
u16 LavanvillePrepareIntro(void);
u16 LavanvilleIntroDepart(void);
u16 LavanvilleRematchReady(void);
bool8 LavanvilleTryZombieSight(void);
bool8 LavanvilleLoadZombieGfx(u8 battler);
#endif

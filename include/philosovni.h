#ifndef GUARD_PHILOSOVNI_H
#define GUARD_PHILOSOVNI_H
#include "global.h"
bool8 PhilosovniIsPartner(u8 battler);
void PhilosovniPreparePartner(void);
void PhilosovniStartDuo(void);
void PhilosovniSyncActors(void);
void PhilosovniRefreshQuay(void);
bool8 PhilosovniNeedsTemplateRefresh(void);
void PhilosovniRefreshHM(void);
u8 PhilosovniPartnerMove(void);
u8 PhilosovniPartnerTarget(void);
#endif

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
u8 PhilosovniFollowerPalette(void);
bool8 PhilosovniFollowing(void);
bool8 PhilosovniIsFollower(const struct ObjectEvent *object);
bool8 PhilosovniFollowerCollision(const struct ObjectEvent *a, const struct ObjectEvent *b);
void PhilosovniFollowerUpdate(void);
void PhilosovniEndFollowing(void);
u16 PhilosovniFollowerDestination(void);
#endif

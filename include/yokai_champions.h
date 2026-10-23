#ifndef GUARD_YOKAI_CHAMPIONS_H
#define GUARD_YOKAI_CHAMPIONS_H
#include "global.h"
const u8 *YokaiChampionName(u16 trainer);
const u8 *YokaiChampionPartySeedName(u16 trainer);
u8 YokaiChampionPortrait(u16 trainer);
bool8 YokaiChampionFemale(u16 trainer);
u8 YokaiChampionObjectGfx(u8 graphicsId);
u8 YokaiChampionFameObjectGfx(u8 graphicsId);
u8 YokaiChampionOrderedPartySize(void);
void YokaiChampionPrepareParty(u16 trainer);
void YokaiChampionResetBattle(void);
bool8 YokaiChampionIsColossus(u8 battler);
bool8 YokaiChampionAnnounceColossus(u8 battler);
u16 YokaiChampionExpYield(u8 battler, u16 normalYield);
#endif

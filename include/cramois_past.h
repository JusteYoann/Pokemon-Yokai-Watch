#ifndef GUARD_CRAMOIS_PAST_H
#define GUARD_CRAMOIS_PAST_H
#include "global.h"
u16 CramoisSepiaColor(u16 color);
u8 CramoisPastStrength(void);
bool8 CramoisIsPastMap(void);
bool8 CramoisIsOverworldView(void);
bool8 CramoisTransferPalette(const u16 *source);
bool8 CramoisTransferBattleAnimPalette(u8 bank);
#endif

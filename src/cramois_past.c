#include "global.h"
#include "gflib.h"
#include "cramois_past.h"
#include "battle_main.h"
#include "battle.h"
#include "battle_anim.h"
#include "data.h"
#include "constants/trainers.h"
#include "main.h"
#include "constants/maps.h"

// ROM only: no permanent EWRAM, no rewritten source palette, no cumulative tint.
static const u16 sSepiaRgb555[] = INCBIN_U16("data/yokai/cramois-sepia-rgb555.bin");

// Shared only by the maritime transition; existing island transfer is unchanged.
u16 CramoisSepiaColor(u16 color)
{
    return sSepiaRgb555[color & 0x7FFF];
}

bool8 CramoisIsPastMap(void)
{
    u16 map;
    if (gSaveBlock1Ptr == NULL) return FALSE;
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_CINNABAR_ISLAND_GYM)) return TRUE;
    map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    switch (map)
    {
    case MAP_CINNABAR_ISLAND:
    case MAP_POKEMON_MANSION_1F:
    case MAP_POKEMON_MANSION_2F:
    case MAP_POKEMON_MANSION_3F:
    case MAP_POKEMON_MANSION_B1F:
        return TRUE;
    }
    return FALSE;
}

bool8 CramoisTransferPalette(const u16 *source)
{
    u32 mask;
    u16 i, bank, pic;
    u8 battler, spriteId;
    vu16 *dest = (vu16 *)PLTT;
    if (gMain.inBattle && gMain.callback2 == BattleMainCB2)
    {
        // BG2-4 are terrain; OBJ0-3 are battler slots. UI stays native.
        mask = 0x000F001C;
        // Front trainers allocate a tagged palette outside the reserved battler
        // banks. Recognize their actual animation table, never a recycled UI sprite.
        for (battler = 0; battler < gBattlersCount && battler < MAX_BATTLERS_COUNT; battler++)
        {
            spriteId = gBattlerSpriteIds[battler];
            if (spriteId >= MAX_SPRITES || !gSprites[spriteId].inUse) continue;
            pic = gSprites[spriteId].oam.affineParam;
            if (pic <= TRAINER_PIC_YOKAI_BERENICE && gSprites[spriteId].anims == gTrainerFrontAnimsPtrTable[pic])
                mask |= 1u << (16 + gSprites[spriteId].oam.paletteNum);
        }
    }
    else if (CramoisIsOverworldView())
        // Field UI uses BG13-15 and allocated OBJ12+. NPCs occupy OBJ0-11.
        mask = 0x0FFF1FFF;
    else
        return FALSE;
    if (!CramoisIsPastMap()) return FALSE;
    for (bank = 0; bank < 32; bank++, mask >>= 1)
        for (i = 0; i < 16; i++, source++, dest++)
            *dest = (mask & 1) ? sSepiaRgb555[*source & 0x7FFF] : *source;
    return TRUE;
}

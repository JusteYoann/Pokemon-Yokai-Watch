#include "field_effect_helpers.h"
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

u8 CramoisPastStrength(void)
{
    u16 map;
    if (gSaveBlock1Ptr == NULL) return 0;
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_CINNABAR_ISLAND_GYM)) return 16;
    map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    switch (map)
    {
    case MAP_CINNABAR_ISLAND:
    case MAP_POKEMON_MANSION_1F:
    case MAP_POKEMON_MANSION_2F:
    case MAP_POKEMON_MANSION_3F:
    case MAP_POKEMON_MANSION_B1F:
        return 16;
    case MAP_ROUTE21_SOUTH:
    case MAP_ROUTE20:
        {
            s16 strength = map == MAP_ROUTE20 ? (10 - gSaveBlock1Ptr->pos.x) * 2 : (gSaveBlock1Ptr->pos.y - 38) * 2;
            return strength < 0 ? 0 : strength > 16 ? 16 : strength;
        }
    }
    return 0;
}

bool8 CramoisIsPastMap(void)
{
    return CramoisPastStrength() != 0;
}

static u16 PastColor(u16 color, u8 strength)
{
    u16 past = sSepiaRgb555[color & 0x7FFF];
    s16 r = color & 31, g = (color >> 5) & 31, b = (color >> 10) & 31;
    if (strength == 16) return past;
    r += (((past & 31) - r) * strength) >> 4;
    g += ((((past >> 5) & 31) - g) * strength) >> 4;
    b += ((((past >> 10) & 31) - b) * strength) >> 4;
    return RGB(r,g,b);
}

bool8 CramoisTransferPalette(const u16 *source)
{
    u32 mask;
    u16 i, bank, pic;
    u8 battler, spriteId, strength = CramoisPastStrength();
    vu16 *dest = (vu16 *)PLTT;
    // Follow the displayed battle screen, including temporary main callbacks.
    if (gMain.inBattle && gMain.vblankCallback == VBlankCB_Battle)
    {
        // BG2-4 are terrain; BG8/9 hold Yo-kai during monbg attacks.
        // Tint both presentations identically; UI banks remain native.
        mask = 0x000F031C;
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
        mask = 0x0FFF1FFF | NativeMountPaletteMask();
    else
        return FALSE;
    if (!strength) return FALSE;
    // Maritime field blending is prepared in the main loop, then DMA-copied.
    if (!gMain.inBattle && CramoisIsOverworldView()
        && gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_ROUTE20)
        && (gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ROUTE20)
            || gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ROUTE21_SOUTH))) return FALSE;
    for (bank = 0; bank < 32; bank++, mask >>= 1)
        for (i = 0; i < 16; i++, source++, dest++)
            *dest = (mask & 1) ? PastColor(*source, strength) : *source;
    return TRUE;
}

// monbg can write a palette straight to hardware after the VBlank transfer.
// Match the battle tint immediately without modifying either source buffer.
bool8 CramoisTransferBattleAnimPalette(u8 bank)
{
    u16 i, offset;
    vu16 *dest = (vu16 *)PLTT;
    if (!gMain.inBattle || !CramoisIsPastMap() || (bank != 8 && bank != 9))
        return FALSE;
    offset = bank * 16;
    for (i = 0; i < 16; i++)
        dest[offset + i] = PastColor(gPlttBufferFaded[offset + i], CramoisPastStrength());
    return TRUE;
}

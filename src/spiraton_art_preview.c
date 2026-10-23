#include "global.h"
#include "gflib.h"
#include "battle.h"
#include "battle_main.h"
#include "battle_anim.h"
#include "spiraton_battle.h"
#include "data/spiraton_art_preview.h"

/* Stage A: explicit QA caller only. No battle/field hook enables this art.
 * Four hardware objects, one logical sprite; no additional EWRAM globals. */
#define PREVIEW_TILE_TAG 0x7D54
#define PREVIEW_PAL_TAG 0x7D55
static const struct SpriteSheet sSheet = { sSpiratonPreviewTiles, sizeof(sSpiratonPreviewTiles), PREVIEW_TILE_TAG };
static const struct SpritePalette sPalette = { sSpiratonPreviewPalette, PREVIEW_PAL_TAG };
static const struct OamData sOam = { .shape = SPRITE_SHAPE(64x64), .size = SPRITE_SIZE(64x64), .priority = 2 };
static const union AnimCmd sAnim[] = { ANIMCMD_FRAME(0, 1), ANIMCMD_END };
static const union AnimCmd *const sAnims[] = { sAnim };
static const struct Subsprite sParts[] = {
    { .x=-64, .y=-48, .shape=SPRITE_SHAPE(64x64), .size=SPRITE_SIZE(64x64), .tileOffset=0, .priority=2 },
    { .x=0, .y=-48, .shape=SPRITE_SHAPE(64x64), .size=SPRITE_SIZE(64x64), .tileOffset=64, .priority=2 },
    { .x=-64, .y=16, .shape=SPRITE_SHAPE(64x32), .size=SPRITE_SIZE(64x32), .tileOffset=128, .priority=2 },
    { .x=0, .y=16, .shape=SPRITE_SHAPE(64x32), .size=SPRITE_SIZE(64x32), .tileOffset=160, .priority=2 },
};
static const struct SubspriteTable sPartTable[] = { { 4, sParts } };
static const struct SpriteTemplate sTemplate = {
    .tileTag=PREVIEW_TILE_TAG, .paletteTag=PREVIEW_PAL_TAG, .oam=&sOam,
    .anims=sAnims, .images=NULL, .affineAnims=gDummySpriteAffineAnimTable,
    .callback=SpriteCallbackDummy,
};

u32 SpiratonArtPreviewShow(void)
{
    u8 sprite;
    u16 tile;
    if (!SpiratonBattleIsBoss(1) || IndexOfSpritePaletteTag(PREVIEW_PAL_TAG) != 0xFF)
        return MAX_SPRITES;
    tile = LoadSpriteSheet(&sSheet);
    if (tile == 0xFFFF)
        return MAX_SPRITES;
    if (LoadSpritePalette(&sPalette) == 0xFF)
    {
        FreeSpriteTilesByTag(PREVIEW_TILE_TAG);
        return MAX_SPRITES;
    }
    sprite = CreateSprite(&sTemplate, 176, 34, 20);
    if (sprite == MAX_SPRITES)
    {
        FreeSpriteTilesByTag(PREVIEW_TILE_TAG);
        FreeSpritePaletteByTag(PREVIEW_PAL_TAG);
        return MAX_SPRITES;
    }
    SetSubspriteTables(&gSprites[sprite], sPartTable);
    gSprites[sprite].subspriteMode = SUBSPRITES_IGNORE_PRIORITY;
    gSprites[sprite].data[0] = gBattlerSpriteIds[1];
    gSprites[sprite].data[1] = gSprites[gBattlerSpriteIds[1]].invisible;
    gSprites[gBattlerSpriteIds[1]].invisible = TRUE;
    return sprite;
}

void SpiratonArtPreviewHide(void)
{
    u8 i;
    for (i=0; i<MAX_SPRITES; i++)
    {
        if (gSprites[i].inUse && gSprites[i].template == &sTemplate)
        {
            u8 original=gSprites[i].data[0];
            if (original<MAX_SPRITES && gSprites[original].inUse)
                gSprites[original].invisible=gSprites[i].data[1];
            DestroySprite(&gSprites[i]);
        }
    }
    FreeSpriteTilesByTag(PREVIEW_TILE_TAG);
    FreeSpritePaletteByTag(PREVIEW_PAL_TAG);
}

#include "global.h"
#include "gflib.h"
#include "battle.h"
#include "battle_anim.h"
#include "spiraton_battle.h"
#include "spiraton_art.h"
#include "data/spiraton_art_preview.h"

/* The existing battler itself owns the four hardware objects. No overlay or
 * second battler, no canvas buffer, and no new palette bank are required. */
#define PREVIEW_TILE_TAG 0x7D54
static const struct SpriteSheet sSheet = { sSpiratonPreviewTiles, sizeof(sSpiratonPreviewTiles), PREVIEW_TILE_TAG };
static const struct Subsprite sParts[] = {
    { .x=-64, .y=-48, .shape=SPRITE_SHAPE(64x64), .size=SPRITE_SIZE(64x64), .tileOffset=0, .priority=2 },
    { .x=0, .y=-48, .shape=SPRITE_SHAPE(64x64), .size=SPRITE_SIZE(64x64), .tileOffset=64, .priority=2 },
    { .x=-64, .y=16, .shape=SPRITE_SHAPE(64x32), .size=SPRITE_SIZE(64x32), .tileOffset=128, .priority=2 },
    { .x=0, .y=16, .shape=SPRITE_SHAPE(64x32), .size=SPRITE_SIZE(64x32), .tileOffset=160, .priority=2 },
};
static const struct SubspriteTable sPartTable[] = { { 4, sParts } };

static EWRAM_DATA u8 sArtSprite = 0;
static EWRAM_DATA bool8 sArtLoaded = FALSE;
static EWRAM_DATA u16 sOriginalTile = 0;

bool8 SpiratonArtIsActive(void)
{
    return sArtLoaded;
}

void SpiratonArtLoad(u8 battler)
{
    struct Sprite *sprite;
    u16 tile;
    if (!SpiratonBattleIsBoss(battler) || SpiratonArtIsActive())
        return;
    tile = LoadSpriteSheet(&sSheet);
    if (GetSpriteTileStartByTag(PREVIEW_TILE_TAG) == TAG_NONE)
        return;
    sArtLoaded = TRUE;
    sArtSprite = gBattlerSpriteIds[battler];
    sprite = &gSprites[sArtSprite];
    sOriginalTile = sprite->oam.tileNum;
    sprite->oam.tileNum = tile;
    sprite->animBeginning = FALSE;
    sprite->animPaused = TRUE;
    sprite->animEnded = TRUE;
    sprite->y = 38; /* Four pixels lower: the complete horns fit, same scale. */
    SetSubspriteTables(sprite, sPartTable);
    sprite->subspriteMode = SUBSPRITES_IGNORE_PRIORITY;
    LoadPalette(sSpiratonPreviewPalette, OBJ_PLTT_ID(battler), PLTT_SIZE_4BPP);
}

void SpiratonArtRelease(void)
{
    if (SpiratonArtIsActive())
    {
        struct Sprite *sprite = &gSprites[sArtSprite];
        sprite->subspriteTables = NULL;
        sprite->subspriteMode = SUBSPRITES_OFF;
        sprite->oam.tileNum = sOriginalTile;
        sprite->oam.mosaic = FALSE;
        sprite->animPaused = FALSE;
        sArtLoaded = FALSE;
        FreeSpriteTilesByTag(PREVIEW_TILE_TAG);
    }
}

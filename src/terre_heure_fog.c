#include "global.h"
#include "gflib.h"
#include "terre_heure.h"
#include "field_weather.h"
#include "main.h"
#include "malloc.h"

#define TH_FOG_TAG 0x12F1
#define TH_FOG_SPRITES 15
#define TH_FOG_CONTROL (BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_EFFECT_BLEND)
#define TH_FOG_ALPHA BLDALPHA_BLEND(3, 13)

// Only 8 fixed bytes; no full palette copy or per-pixel frame processing.
static EWRAM_DATA struct {
    u16 scroll, oldControl, oldAlpha;
    bool8 loaded, visible;
} sThFog = {};

static void Cloud(struct Sprite *sprite)
{
    sprite->x = (sprite->data[0] % 5) * 64 + 32 - ((sThFog.scroll >> 2) & 63);
    sprite->y = (sprite->data[0] / 5) * 64 + 24;
    sprite->invisible = !sThFog.visible;
}

static const struct OamData sOam = {
    .objMode = ST_OAM_OBJ_BLEND, .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64), .priority = 2,
};
static const union AnimCmd sAnim[] = { ANIMCMD_FRAME(0, 16), ANIMCMD_JUMP(0) };
static const union AnimCmd *const sAnims[] = { sAnim };
static const u16 sYellow[16] = {
    RGB(0,0,0), RGB(31,29,7), RGB(31,29,7), RGB(31,29,7),
    RGB(18,17,4), RGB(24,22,5), RGB(26,24,6), RGB(27,25,6),
    RGB(20,19,4), RGB(31,29,7), RGB(31,29,7), RGB(31,29,7),
    RGB(22,20,5), RGB(28,26,6), RGB(30,28,7), RGB(31,29,7)
};
static const struct SpriteTemplate sTemplate = {
    .tileTag=TH_FOG_TAG, .paletteTag=TH_FOG_TAG, .oam=&sOam,
    .anims=sAnims, .images=NULL, .affineAnims=gDummySpriteAffineAnimTable,
    .callback=Cloud,
};

void TerreHeureFogClear(void)
{
    u8 i;
    bool8 ownsPalette = IndexOfSpritePaletteTag(TH_FOG_TAG) != 0xFF;
    for(i=0;i<MAX_SPRITES;i++)
        if(gSprites[i].inUse && gSprites[i].callback==Cloud) DestroySprite(&gSprites[i]);
    if(sThFog.loaded && ownsPalette && GetGpuReg(REG_OFFSET_BLDCNT)==TH_FOG_CONTROL
        && GetGpuReg(REG_OFFSET_BLDALPHA)==TH_FOG_ALPHA) {
        SetGpuReg(REG_OFFSET_BLDCNT,sThFog.oldControl);
        SetGpuReg(REG_OFFSET_BLDALPHA,sThFog.oldAlpha);
    }
    FreeSpriteTilesByTag(TH_FOG_TAG);
    FreeSpritePaletteByTag(TH_FOG_TAG);
    sThFog.loaded=FALSE;sThFog.visible=FALSE;
}

static bool8 CreateClouds(void)
{
    struct SpriteSheet sheet={gWeatherFogHorizontalTiles,0x800,TH_FOG_TAG};
    struct SpritePalette pal={sYellow,TH_FOG_TAG};
    u8 i,id,lo,hi;
    u16 pixel;
    u8 *tiles=Alloc(0x800);
    if(tiles==NULL)return FALSE;
    // Reuse the native cloud relief, with transparent gaps between the wisps.
    // This is prepared once on load, never per frame.
    for(pixel=0;pixel<0x800;pixel++) {
        lo=gWeatherFogHorizontalTiles[pixel]&15;hi=gWeatherFogHorizontalTiles[pixel]>>4;
        if(lo==4 || lo==5 || lo==8 || lo==12)lo=0;
        if(hi==4 || hi==5 || hi==8 || hi==12)hi=0;
        tiles[pixel]=lo|(hi<<4);
    }
    sheet.data=tiles;
    LoadSpriteSheet(&sheet);
    Free(tiles);
    if(GetSpriteTileStartByTag(TH_FOG_TAG)==0xFFFF)return FALSE;
    if(LoadSpritePalette(&pal)==0xFF){FreeSpriteTilesByTag(TH_FOG_TAG);return FALSE;}
    sThFog.oldControl=GetGpuReg(REG_OFFSET_BLDCNT);
    sThFog.oldAlpha=GetGpuReg(REG_OFFSET_BLDALPHA);
    sThFog.loaded=TRUE;
    for(i=0;i<TH_FOG_SPRITES;i++) {
        id=CreateSpriteAtEnd(&sTemplate,0,0,0xFF);
        if(id==MAX_SPRITES){TerreHeureFogClear();return FALSE;}
        gSprites[id].data[0]=i;
        Cloud(&gSprites[id]);
    }
    return TRUE;
}

void TerreHeureFogUpdate(void)
{
    sThFog.visible=TerreHeureFogVisible();
    if(sThFog.loaded && IndexOfSpritePaletteTag(TH_FOG_TAG)==0xFF)sThFog.loaded=FALSE;
    if(!sThFog.visible) {
        if(sThFog.loaded)TerreHeureFogClear();
        return;
    }
    if(!sThFog.loaded && !CreateClouds())return;
    sThFog.scroll++;
    SetGpuReg(REG_OFFSET_BLDCNT,TH_FOG_CONTROL);
    SetGpuReg(REG_OFFSET_BLDALPHA,TH_FOG_ALPHA);
}

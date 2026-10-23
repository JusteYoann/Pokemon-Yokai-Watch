#include "global.h"
#include "gflib.h"
#include "cramois_fog.h"
#include "cramois_past.h"
#include "field_weather.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "main.h"
#include "palette.h"
#include "constants/maps.h"
#include "constants/weather.h"

#define FOG_TAG 0x12F0
#define FOG_SPRITES 15
#define FOG_MAX 12
#define FOG_CONTROL (BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_EFFECT_BLEND)
static EWRAM_DATA struct {
    u16 map, amount, scroll, oldAlpha, oldControl, lastAlpha;
    bool8 loaded;
} sFog = {0};

static void FogSprite(struct Sprite *sprite);
static const struct OamData sOam = {
    .objMode = ST_OAM_OBJ_BLEND, .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64), .priority = 2,
};
static const union AnimCmd sAnim[] = {ANIMCMD_FRAME(0, 16), ANIMCMD_JUMP(0)};
static const union AnimCmd *const sAnims[] = {sAnim};
// Native fog's grayscale relief, with no weather-green or magenta entries.
static const u16 sWhite[16] = {
    RGB(0,0,0),RGB(31,31,31),RGB(31,31,31),RGB(31,31,31),
    RGB(18,18,18),RGB(24,24,24),RGB(26,26,26),RGB(27,27,27),
    RGB(20,20,20),RGB(31,31,31),RGB(31,31,31),RGB(31,31,31),
    RGB(22,22,22),RGB(28,28,28),RGB(30,30,30),RGB(31,31,31)
};
static const struct SpriteTemplate sTemplate = {
    .tileTag=FOG_TAG, .paletteTag=FOG_TAG, .oam=&sOam,
    .anims=sAnims, .images=NULL, .affineAnims=gDummySpriteAffineAnimTable,
    .callback=FogSprite,
};

static bool8 MaritimeView(void)
{
    u16 map;
    if (!CramoisIsOverworldView() || gMain.inBattle || gSaveBlock1Ptr == NULL
        || !(gPlayerAvatar.flags & PLAYER_AVATAR_FLAG_SURFING)) return FALSE;
    map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    if (map != MAP_ROUTE20 && map != MAP_ROUTE21_SOUTH) return FALSE;
    // Do not compete with another weather effect or its blend coefficients.
    return (gWeatherPtr->currWeather == WEATHER_SUNNY || gWeatherPtr->currWeather == WEATHER_NONE)
        && (gWeatherPtr->nextWeather == WEATHER_SUNNY || gWeatherPtr->nextWeather == WEATHER_NONE);
}

u8 CramoisFogTarget(void)
{
    s16 x, y, distance;
    if (!MaritimeView()) return 0;
    PlayerGetDestCoords(&x, &y);
    x -= MAP_OFFSET;
    y -= MAP_OFFSET;
    if (gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ROUTE20))
    {
        distance = x - 1;
        if (19 - x < distance) distance = 19 - x;
    }
    else
    {
        distance = y - 29;
        if (47 - y < distance) distance = 47 - y;
    }
    if (distance <= 0) return 0;
    if (distance >= 6) return FOG_MAX;
    return distance * 2;
}

static void FogSprite(struct Sprite *sprite)
{
    sprite->x = (sprite->data[0] % 5) * 64 + 32 - ((sFog.scroll >> 2) & 63);
    sprite->y = (sprite->data[0] / 5) * 64 + 24;
    sprite->invisible = !MaritimeView() || sFog.amount == 0;
}

static void ReleaseFog(void)
{
    u8 i;
    for (i=0;i<MAX_SPRITES;i++)
        if (gSprites[i].inUse && gSprites[i].callback == FogSprite) DestroySprite(&gSprites[i]);
    FreeSpriteTilesByTag(FOG_TAG);
    FreeSpritePaletteByTag(FOG_TAG);
    // A native transition/menu may already have replaced these registers.
    if (sFog.loaded && GetGpuReg(REG_OFFSET_BLDALPHA) == sFog.lastAlpha
        && GetGpuReg(REG_OFFSET_BLDCNT) == FOG_CONTROL)
    {
        SetGpuReg(REG_OFFSET_BLDALPHA,sFog.oldAlpha);
        SetGpuReg(REG_OFFSET_BLDCNT,sFog.oldControl);
    }
    sFog.loaded=FALSE;
    sFog.amount=0;
}

static bool8 CreateFog(void)
{
    struct SpriteSheet sheet = {gWeatherFogHorizontalTiles,0x800,FOG_TAG};
    struct SpritePalette pal = {sWhite,FOG_TAG};
    u8 i, id, count=0;
    if (LoadSpriteSheet(&sheet) == 0xFFFF) return FALSE;
    if (LoadSpritePalette(&pal) == 0xFF) {FreeSpriteTilesByTag(FOG_TAG);return FALSE;}
    sFog.oldAlpha=GetGpuReg(REG_OFFSET_BLDALPHA);
    sFog.oldControl=GetGpuReg(REG_OFFSET_BLDCNT);
    sFog.lastAlpha=sFog.oldAlpha;
    for (i=0;i<FOG_SPRITES;i++)
    {
        id=CreateSpriteAtEnd(&sTemplate,0,0,0xFF);
        if (id==MAX_SPRITES) break;
        gSprites[id].data[0]=i;
        FogSprite(&gSprites[id]);
        count++;
    }
    sFog.loaded=TRUE;
    if (count != FOG_SPRITES) {ReleaseFog();return FALSE;}
    return TRUE;
}

void CramoisFogUpdate(void)
{
    u16 map, target;
    u8 density;
    map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    // ResetSpriteData on menu/map/battle entry can invalidate all old slots.
    if (sFog.loaded && IndexOfSpritePaletteTag(FOG_TAG)==0xFF)
    {sFog.loaded=FALSE;sFog.amount=0;}
    if (!MaritimeView() || sFog.map != map)
    {
        if (sFog.loaded) ReleaseFog();
        sFog.map=map;
        if (!MaritimeView()) return;
    }
    target=CramoisFogTarget()*16;
    if (!target && !sFog.loaded) return;
    if (!sFog.loaded && !CreateFog()) return;
    if (sFog.amount < target) sFog.amount += 4;
    else if (sFog.amount > target) sFog.amount -= 4;
    if (!sFog.amount && !target) {ReleaseFog();return;}
    sFog.scroll++;
    density=(sFog.amount+8)>>4;
    sFog.lastAlpha=BLDALPHA_BLEND(density,16-density);
    SetGpuReg(REG_OFFSET_BLDCNT,FOG_CONTROL);
    SetGpuReg(REG_OFFSET_BLDALPHA,sFog.lastAlpha);
}

void CramoisFogPalette(void)
{
    u16 i,c,amount,blend,spriteBlend,past;
    s16 r,g,b;
    s16 x,y,tone;
    u32 mask=0x0FFF1FFF;
    vu16 *dest=(vu16 *)PLTT;
    if (!MaritimeView() || gPaletteFade.active || gPaletteFade.bufferTransferDisabled) return;
    PlayerGetDestCoords(&x,&y);
    x-=MAP_OFFSET;y-=MAP_OFFSET;
    // Match the island palette before the connection, while dense fog masks the
    // change. No temporal state is saved and no island palette code is changed.
    tone = gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ROUTE20) ? (10-x)*2 : (y-38)*2;
    if (tone<0) tone=0;
    if (tone>16) tone=16;
    amount=sFog.amount*5/(FOG_MAX*16);
    if (!amount && !tone) return;
    spriteBlend=sFog.amount*9/(FOG_MAX*16);
    for (i=0;i<512;i++)
    {
        if (i && !(i&15)) mask>>=1;
        if (!(mask&1)) continue;
        blend = i < 256 ? amount : spriteBlend;
        c=gPlttBufferFaded[i];r=c&31;g=(c>>5)&31;b=(c>>10)&31;
        if (tone)
        {
            past=CramoisSepiaColor(c);
            r+=(((past&31)-r)*tone)>>4;
            g+=((((past>>5)&31)-g)*tone)>>4;
            b+=((((past>>10)&31)-b)*tone)>>4;
        }
        r+=((31-r)*blend)>>4;g+=((31-g)*blend)>>4;b+=((31-b)*blend)>>4;
        dest[i]=RGB(r,g,b);
    }
}

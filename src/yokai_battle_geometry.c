#include "yokai_champions.h"
#include "global.h"
#include "lavanville.h"
#include "spiraton_art.h"
#include "gflib.h"
#include "battle.h"
#include "data.h"
#include "battle_anim.h"
#include "yokai_battle_geometry.h"
#include "data/yokai_battle_geometry.h"
#include "data/yokai_battle_pictures.h"

extern u32 gOamMatrixAllocBitmap;
extern u8 gOamLimit;

static const struct YokaiBattleGeometry sLavenderZombieGeometry[] = {
    {186,186,-6,-9,-31,-36,62,75},
    {178,178,-3,-10,-38,-32,74,73},
    {186,186,-2,-11,-40,-36,80,75},
    {178,178,-7,-11,-29,-41,57,82},
};

const struct YokaiBattleGeometry *GetYokaiBattleGeometry(u8 battler)
{
    u16 species;
    if (gMain.inBattle && battler < gBattlersCount && GetBattlerSide(battler) == B_SIDE_OPPONENT && (gBattleTypeFlags & BATTLE_TYPE_LAVENDER_ZOMBIE))
        return &sLavenderZombieGeometry[(gBattleTypeFlags >> 21) & 3];
    if (YokaiChampionIsColossus(battler) && gBattleSpritesDataPtr != NULL
        && !gBattleSpritesDataPtr->battlerData[battler].behindSubstitute
        && gBattleSpritesDataPtr->battlerData[battler].transformSpecies == 0)
        return &sLavenderZombieGeometry[2];
    if (battler == 1 && SpiratonArtIsActive())
        return NULL;
    if (!gMain.inBattle || battler >= gBattlersCount || gBattleSpritesDataPtr == NULL
        || gMonSpritesGfxPtr == NULL || gBattleSpritesDataPtr->battlerData[battler].behindSubstitute)
        return NULL;
    if ((gBattleTypeFlags & BATTLE_TYPE_GHOST) && !(gBattleTypeFlags & BATTLE_TYPE_GHOST_UNVEILED))
        return NULL;
    species = gBattleSpritesDataPtr->battlerData[battler].transformSpecies;
    if (species == 0)
    {
        if (GetBattlerSide(battler) == B_SIDE_PLAYER)
            species = GetMonData(&gPlayerParty[gBattlerPartyIndexes[battler]], MON_DATA_SPECIES);
        else
            species = GetMonData(&gEnemyParty[gBattlerPartyIndexes[battler]], MON_DATA_SPECIES);
    }
    if (species == 0 || species > 151)
        return NULL;
    return &sYokaiBattleGeometry[species][GetBattlerSide(battler) == B_SIDE_PLAYER];
}

// Compose only the final hardware OAM buffer. Logical animation matrices and
// sprite state remain untouched. Temporary matrix reservations end this frame.
void ApplyYokaiBattleOam(void)
{
    u32 saved = gOamMatrixAllocBitmap;
    u32 i, b;
    if (!gMain.inBattle || gMonSpritesGfxPtr == NULL)
        return;
    for (b = 0; b < gBattlersCount; ++b)
    {
        const struct YokaiBattleGeometry *p = GetYokaiBattleGeometry(b);
        struct Sprite *sprite;
        if (p == NULL || gBattlerSpriteIds[b] >= MAX_SPRITES)
            continue;
        sprite = &gSprites[gBattlerSpriteIds[b]];
        if (!sprite->inUse || sprite->anims != gAnims_MonPic)
            continue;
        for (i = 0; i < gOamLimit; ++i)
        {
            struct OamData *o = &gMain.oamBuffer[i];
            s16 a = 256, c = 0, d = 256, bb = 0;
            u8 matrix;
            u16 half;
            if (o->affineMode == ST_OAM_AFFINE_ERASE || o->tileNum != sprite->oam.tileNum
                || o->paletteNum != sprite->oam.paletteNum || o->shape != ST_OAM_SQUARE || o->size != 3)
                continue;
            half = o->affineMode == ST_OAM_AFFINE_DOUBLE ? 64 : 32;
            if (o->affineMode & ST_OAM_AFFINE_ON_MASK)
            {
                a = gOamMatrices[o->matrixNum].a; bb = gOamMatrices[o->matrixNum].b;
                c = gOamMatrices[o->matrixNum].c; d = gOamMatrices[o->matrixNum].d;
            }
            else
            {
                if (o->matrixNum & 8) a = -256;
                if (o->matrixNum & 16) d = -256;
            }
            matrix = AllocOamMatrix();
            if (matrix == 0xFF)
                continue; // Bounded fallback, never index past32 hardware matrices.
            o->x = o->x + half - 64;
            o->y = o->y + half - 64;
            o->affineMode = ST_OAM_AFFINE_DOUBLE;
            o->matrixNum = matrix;
            gMain.oamBuffer[matrix * 4 + 0].affineParam = (a * p->inverseX) >> 8;
            gMain.oamBuffer[matrix * 4 + 1].affineParam = (bb * p->inverseX) >> 8;
            gMain.oamBuffer[matrix * 4 + 2].affineParam = (c * p->inverseY) >> 8;
            gMain.oamBuffer[matrix * 4 + 3].affineParam = (d * p->inverseY) >> 8;
        }
    }
    gOamMatrixAllocBitmap = saved;
}

static bool8 SameAnimationTile(const u8 *a, const u8 *b)
{
    u32 i;
    for (i = 0; i < 32; ++i)
        if (a[i] != b[i]) return FALSE;
    return TRUE;
}

// Animation silhouettes use the same indexed pixels and inverse transforms as
// hardware OBJ. Compact tile packing stays inside the existing4096-byte half.
bool8 CopyYokaiBattlerToBg(s32 bgId, u8 battler, u8 pal, u8 *tiles, u16 *map, u16 offset)
{
    const struct YokaiBattleGeometry *p = GetYokaiBattleGeometry(battler);
    const u8 *source;
    u32 x, y, tx, ty, cols, rows, used = 1;
    u8 tile[32];
    if (p == NULL)
        return FALSE;
    cols = (p->width + 7) / 8; rows = (p->height + 7) / 8;
    source = gMonSpritesGfxPtr->sprites[GetBattlerPosition(battler)] + 0x800 * gBattleMonForms[battler];
    CpuFill16(0, tiles, 0x1000);
    /* Deduplicate empty/repeated tiles. Full lower-body silhouettes can occupy
     * a wide rectangle while still fitting the native 128-tile allocation. */
    for (ty = 0; ty < rows; ++ty)
    {
        for (tx = 0; tx < cols; ++tx)
        {
            u32 found;
            memset(tile, 0, sizeof(tile));
            for (y = 0; y < 8; ++y)
            {
                s32 py = ty * 8 + y;
                s32 sy = ((py + p->top) * p->inverseY >> 8) + 32;
                if (py >= p->height || sy < 0 || sy >= 64)
                    continue;
                for (x = 0; x < 8; ++x)
                {
                    s32 px = tx * 8 + x;
                    s32 sx = ((px + p->left) * p->inverseX >> 8) + 32;
                    u32 idx, value;
                    if (px >= p->width || sx < 0 || sx >= 64)
                        continue;
                    idx = (sy / 8 * 8 + sx / 8) * 32 + (sy % 8) * 4 + (sx % 8) / 2;
                    value = (source[idx] >> ((sx & 1) * 4)) & 15;
                    tile[y * 4 + x / 2] |= value << ((x & 1) * 4);
                }
            }
            for (found = 0; found < used; ++found)
                if (SameAnimationTile(tile, tiles + found * 32))
                    break;
            if (found == used)
            {
                if (used >= 128)
                    return FALSE;
                memcpy(tiles + used * 32, tile, 32);
                ++used;
            }
            map[ty * 32 + tx] = (offset + found) | (pal << 12);
        }
    }
    LoadBgTiles(bgId, tiles, used * 32, offset);
    LoadBgTilemap(bgId, map, 0x800, 0);
    if (bgId == 1)
    {
        gBattle_BG1_X += -p->left - 32; gBattle_BG1_Y += -p->top - 32;
        SetGpuReg(REG_OFFSET_BG1HOFS, gBattle_BG1_X); SetGpuReg(REG_OFFSET_BG1VOFS, gBattle_BG1_Y);
    }
    else
    {
        gBattle_BG2_X += -p->left - 32; gBattle_BG2_Y += -p->top - 32;
        SetGpuReg(REG_OFFSET_BG2HOFS, gBattle_BG2_X); SetGpuReg(REG_OFFSET_BG2VOFS, gBattle_BG2_Y);
    }
    return TRUE;
}

// Battle-only textures; menus, storage and summaries retain their prior art.
void TryLoadYokaiBattlePic(void *dest, u16 species, bool8 isFront)
{
    u32 i;
    if (!gMain.inBattle || gMonSpritesGfxPtr == NULL || species == 0 || species > 151)
        return;
    for (i = 0; i < MAX_BATTLERS_COUNT; ++i)
    {
        if (dest == gMonSpritesGfxPtr->sprites[i])
        {
            LZ77UnCompWram(sYokaiBattlePictures[species][!isFront], dest);
            return;
        }
    }
    if (dest == gMonSpritesGfxPtr->multiUseBuffer)
        LZ77UnCompWram(sYokaiBattlePictures[species][!isFront], dest);
}

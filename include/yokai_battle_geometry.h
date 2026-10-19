#ifndef GUARD_YOKAI_BATTLE_GEOMETRY_H
#define GUARD_YOKAI_BATTLE_GEOMETRY_H
struct YokaiBattleGeometry
{
    s16 inverseX, inverseY;
    s8 offsetX, offsetY;
    s8 left, top;
    u8 width, height;
};
const struct YokaiBattleGeometry *GetYokaiBattleGeometry(u8 battler);
void ApplyYokaiBattleOam(void);
void TryLoadYokaiBattlePic(void *dest, u16 species, bool8 isFront);
bool8 CopyYokaiBattlerToBg(s32 bgId, u8 battler, u8 pal, u8 *tiles, u16 *map, u16 offset);
#endif

#ifndef GUARD_COMPACT_LABELS_FR_H
#define GUARD_COMPACT_LABELS_FR_H
#include "characters.h"

// Compact, readable labels for native tile-based badges. Stored in ROM only.
static const u8 sCompactFrAlphabet[26][5] = {
    {2,5,7,5,5},{6,5,6,5,6},{3,4,4,4,3},{6,5,5,5,6},
    {7,4,6,4,7},{7,4,6,4,4},{3,4,5,5,3},{5,5,7,5,5},
    {7,2,2,2,7},{1,1,1,5,2},{5,5,6,5,5},{4,4,4,4,7},
    {5,7,7,5,5},{5,7,7,7,5},{2,5,5,5,2},{6,5,6,4,4},
    {2,5,5,7,3},{6,5,6,5,5},{3,4,2,1,6},{7,2,2,2,2},
    {5,5,5,5,7},{5,5,5,5,2},{5,5,7,7,5},{5,5,2,5,5},
    {5,5,2,2,2},{7,1,2,4,7}
};

static u8 CompactFrPixelGet(const u16 *tiles, u8 tilesWide, u16 x, u16 y)
{
    u32 index = ((y / 8) * tilesWide + x / 8) * 16 + (y % 8) * 2 + (x % 8) / 4;
    return (tiles[index] >> ((x % 4) * 4)) & 15;
}

static void CompactFrPixel(u16 *tiles, u8 tilesWide, u16 x, u16 y, u8 color)
{
    volatile u16 *word = tiles + ((y / 8) * tilesWide + x / 8) * 16 + (y % 8) * 2 + (x % 8) / 4;
    u8 shift = (x % 4) * 4;
    *word = (*word & ~(15 << shift)) | (color << shift);
}

static void CompactFrLabel(u16 *tiles, u8 tilesWide, u16 left, u16 top, u8 width, u8 height, u8 background, u8 foreground, const u8 *text)
{
    u16 x, y;
    u8 n, count = 0;
    while (text[count] != EOS)
        count++;
    if (count * 4 - 1 > width)
        return;
    for (y = top; y < top + height; y++)
        for (x = left; x < left + width; x++)
            CompactFrPixel(tiles, tilesWide, x, y, background);
    left += (width - (count * 4 - 1)) / 2;
    top += (height - 5) / 2;
    for (n = 0; n < count; n++)
    {
        u8 ch = text[n];
        if (ch == CHAR_E_ACUTE || ch == CHAR_E_GRAVE)
        {
            if (top > 0)
                CompactFrPixel(tiles, tilesWide, left + n * 4 + 2, top - 1, foreground);
            ch = CHAR_E;
        }
        for (y = 0; y < 5; y++)
            for (x = 0; x < 3; x++)
            {
                bool8 ink = FALSE;
                if (ch >= CHAR_A && ch <= CHAR_Z)
                    ink = (sCompactFrAlphabet[ch - CHAR_A][y] & (4 >> x)) != 0;
                else if (ch == CHAR_PERIOD)
                    ink = y == 4 && x == 1;
                else if (ch == CHAR_QUESTION_MARK)
                    ink = (y == 0 || y == 2) ? x == 1 : (y == 1 ? x == 2 : y == 4 && x == 1);
                if (ink)
                    CompactFrPixel(tiles, tilesWide, left + n * 4 + x, top + y, foreground);
            }
    }
}
#endif

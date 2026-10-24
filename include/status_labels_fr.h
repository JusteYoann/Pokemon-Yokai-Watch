#ifndef GUARD_STATUS_LABELS_FR_H
#define GUARD_STATUS_LABELS_FR_H

// Tiny status labels are rendered into the native 4bpp tiles after loading.
// Halfword writes work in both RAM and GBA VRAM; no extra persistent RAM.
static void StatusLabelPixel(u16 *tiles, u8 x, u8 y, u8 color)
{
    volatile u16 *word = tiles + (x / 8) * 16 + y * 2 + (x % 8) / 4;
    u8 shift = (x % 4) * 4;
    *word = (*word & ~(15 << shift)) | (color << shift);
}

static void StatusLabelDraw(u16 *tiles, u8 left, u8 right, u8 background, const u8 *letters, u8 count)
{
    u8 x, y, n;
    for (y = 1; y <= 6; y++)
        for (x = left; x <= right; x++)
            StatusLabelPixel(tiles, x, y, background);
    left += (right - left + 1 - (count * 4 - 1)) / 2;
    for (n = 0; n < count; n++)
        for (y = 0; y < 5; y++)
            for (x = 0; x < 3; x++)
                if (letters[n * 5 + y] & (4 >> x))
                    StatusLabelPixel(tiles, left + n * 4 + x, y + 1, 2);
}

static const u8 sStatusSom[] = {7,4,7,1,7, 7,5,5,5,7, 5,7,7,5,5};
static const u8 sStatusGel[] = {7,4,5,5,7, 7,4,6,4,7, 4,4,4,4,7};
static const u8 sStatusBru[] = {6,5,6,5,6, 6,5,6,5,5, 5,5,5,5,7};
static const u8 sStatusKo[] = {5,5,6,5,5, 0,0,0,0,2, 7,5,5,5,7, 0,0,0,0,2};

static void LocalizeStatusSheet(u16 *tiles)
{
    static const u8 *const labels[] = {sStatusSom, sStatusGel, sStatusBru, sStatusKo};
    static const u8 indexes[] = {2, 3, 4, 6};
    u8 i;
    for (i = 0; i < 4; i++)
    {
        u16 *icon = tiles + indexes[i] * 64;
        u8 background = (icon[7] >> 12) & 15; // Original color at (7, 3).
        StatusLabelDraw(icon, 8, 23, background, labels[i], i == 3 ? 4 : 3);
    }
}
#endif

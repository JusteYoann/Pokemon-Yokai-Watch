#include "global.h"
#include "gflib.h"
#include "blend_palette.h"
#include "menu.h"
#include "task.h"
#include "new_menu_helpers.h"
#include "m4a.h"
#include "sound.h"
#include "event_data.h"
#include "overworld.h"
#include "yokai_music.h"
#include "yokai_presentation.h"
#include "constants/songs.h"

struct CreditAssets
{
    const u32 *tiles;
    const u32 *map;
    const u16 *palette;
};
struct CreditSlide
{
    const u8 *text;
    u16 frames;
    u8 textX;
    u8 textY;
    u8 textWidth;
};
#include "data/yokai_credits.h"

static EWRAM_DATA u8 sYokaiCreditsSlide = 0;
static EWRAM_DATA u16 sYokaiCreditsTick = 0;
static EWRAM_DATA u32 sYokaiCreditsTotalFrames = 0;
static EWRAM_DATA u32 sYokaiCreditsStartVBlank = 0;
static const u16 sCreditTextPalette[16] = {RGB_BLACK, RGB_WHITE, RGB(3,3,3)};
static const u8 sCreditTextColors[] = {0,1,2};
static const struct BgTemplate sCreditBgs[] = {
    {.bg=0, .charBaseIndex=0, .mapBaseIndex=28, .screenSize=0, .paletteMode=1, .priority=1},
    {.bg=1, .charBaseIndex=2, .mapBaseIndex=30, .screenSize=0, .paletteMode=0, .priority=0},
};
static const struct WindowTemplate sCreditWindows[] = {
    {.bg=1, .tilemapLeft=0, .tilemapTop=0, .width=30, .height=20, .paletteNum=15, .baseBlock=1},
    DUMMY_WIN_TEMPLATE
};

static void VBlankYokaiCredits(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void LoadCreditSlide(u8 index)
{
    const struct CreditAssets *assets = &sCreditAssets[gSaveBlock2Ptr->playerGender == FEMALE][index];
    const struct CreditSlide *slide = &sCreditSlides[index];
    u8 font = index == 31 ? FONT_NORMAL : FONT_SMALL;
    s16 x = slide->textX;
    if (slide->textWidth >= 200)
        x += (slide->textWidth - GetStringWidth(font, slide->text, 0)) / 2;
    /* Largest image21568B ends below char2; text19232B ends below map28.
     * Pictures and text use disjoint palette ranges and independent fades. */
    LZ77UnCompVram(assets->tiles, (void *)BG_VRAM);
    LZ77UnCompVram(assets->map, (void *)(BG_VRAM + 28 * BG_SCREEN_SIZE));
    /* Keep the transferred buffer black throughout loading. LoadPalette would
     * briefly expose full-brightness colors if VBlank interrupted the load. */
    CpuCopy16(assets->palette, gPlttBufferUnfaded, 240 * sizeof(u16));
    CpuCopy16(sCreditTextPalette, &gPlttBufferUnfaded[BG_PLTT_ID(15)], sizeof(sCreditTextPalette));
    CpuFill16(RGB_BLACK, gPlttBufferFaded, 256 * sizeof(u16));
    FillWindowPixelBuffer(0, 0);
    AddTextPrinterParameterized3(0, font, x, slide->textY, sCreditTextColors, TEXT_SKIP_DRAW, slide->text);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void CB2_RollYokaiCredits(void)
{
    u32 elapsed = gMain.vblankCounter2 - sYokaiCreditsStartVBlank;
    u32 local = elapsed;
    u8 wanted = 0;
    /* VBlank is the music clock too. Image loading may cross a refresh;
     * never add its CPU time to the scripted434/433-frame slide durations. */
    while (wanted < 32 && local >= sCreditSlides[wanted].frames)
        local -= sCreditSlides[wanted++].frames;
    if (wanted != sYokaiCreditsSlide)
    {
        if (wanted < 32)
            LoadCreditSlide(wanted);
        else
        {
            BlendPalette(0, 256, 16, RGB_BLACK);
            ResetMapMusic();
            YokaiDiscardPausedSample(&gMPlayInfo_BGM);
            m4aMPlayStop(&gMPlayInfo_BGM);
        }
        /* Publish only once decompression/map upload has completed. */
        sYokaiCreditsSlide = wanted;
    }
    sYokaiCreditsTotalFrames = elapsed;
    sYokaiCreditsTick = local;
    if (sYokaiCreditsSlide < 32)
    {
        const struct CreditSlide *slide = &sCreditSlides[sYokaiCreditsSlide];
        u16 tick = sYokaiCreditsTick;
        u16 remaining = slide->frames - tick;
        u16 photoFade;
        u16 textFade;
        if (sYokaiCreditsSlide == 31)
        {
            /* Final30s: image0..3s, text3..7s, hold to25s, fade to30s. */
            photoFade = tick < 179 ? 16 - tick * 16 / 179 : remaining < 299 ? 16 - remaining * 16 / 299 : 0;
            textFade = tick < 179 ? 16 : tick < 418 ? 16 - (tick - 179) * 16 / 239 : remaining < 299 ? 16 - remaining * 16 / 299 : 0;
        }
        else
        {
            photoFade = tick < 40 ? 16 - tick * 16 / 40 : remaining < 40 ? 16 - remaining * 16 / 40 : 0;
            textFade = tick < 20 ? 16 : tick < 60 ? 16 - (tick - 20) * 16 / 40 : remaining < 40 ? 16 - remaining * 16 / 40 : 0;
        }
        BlendPalette(0, 240, photoFade, RGB_BLACK);
        BlendPalette(240, 16, textFade, RGB_BLACK);
    }
    else if (sYokaiCreditsTick >= 120)
    {
        SetVBlankCallback(NULL);
        FreeAllWindowBuffers();
        FlagClear(FLAG_DONT_SHOW_MAP_NAME_POPUP);
        gDisableMapMusicChangeOnMapLoad = MUSIC_DISABLE_OFF;
        SoftReset(RESET_ALL);
    }
    RunTasks();
    BuildOamBuffer();
}

void CB2_InitYokaiCredits(void)
{
    u8 i;
    SetMainCallback1(NULL);
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    ResetMapMusic();
    m4aMPlayAllStop();
    InitHeap(gHeap, HEAP_SIZE);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    DmaClear32(3, (void *)OAM, OAM_SIZE);
    DmaClear16(3, (void *)PLTT, PLTT_SIZE);
    ResetBgsAndClearDma3BusyFlags(FALSE);
    InitBgsFromTemplates(0, sCreditBgs, NELEMS(sCreditBgs));
    for (i=0; i<4; i++) { ChangeBgX(i,0,BG_COORD_SET); ChangeBgY(i,0,BG_COORD_SET); }
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    InitWindows(sCreditWindows);
    DeactivateAllTextPrinters();
    sYokaiCreditsSlide = 0;
    sYokaiCreditsTick = 0;
    sYokaiCreditsTotalFrames = 0;
    LoadCreditSlide(0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0);
    ShowBg(0);
    ShowBg(1);
    PlayBGM(MUS_YOKAI_CREDITS);
    sYokaiCreditsStartVBlank = gMain.vblankCounter2;
    SetVBlankCallback(VBlankYokaiCredits);
    SetMainCallback2(CB2_RollYokaiCredits);
}

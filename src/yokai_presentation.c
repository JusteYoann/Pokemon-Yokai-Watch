#include "global.h"
#include "gflib.h"
#include "menu.h"
#include "task.h"
#include "new_menu_helpers.h"
#include "help_system.h"
#include "m4a.h"
#include "sound.h"
#include "load_save.h"
#include "new_game.h"
#include "save.h"
#include "main_menu.h"
#include "clear_save_data_screen.h"
#include "berry_fix_program.h"
#include "yokai_presentation.h"
#include "yokai_music.h"
#include "constants/songs.h"

/* BG0 landscape: char0, maps28/29. BG1 logo: char2, map30.
 * BG2 text: char3 +128tiles, map31. No full-frame EWRAM buffer. */
static const u32 sLandscapeTiles[] = INCBIN_U32("graphics/yokai_title/fresque.4bpp.lz");
static const u16 sLandscapePal[] = INCBIN_U16("graphics/yokai_title/fresque.gbapal");
static const u16 sLandscapeMap[] = INCBIN_U16("graphics/yokai_title/fresque.bin");
static const u32 sLogoTiles[] = INCBIN_U32("graphics/yokai_title/logo.4bpp.lz");
static const u16 sLogoPal[] = INCBIN_U16("graphics/yokai_title/logo.gbapal");
static const u16 sLogoMap[] = INCBIN_U16("graphics/yokai_title/logo.bin");
static const u16 sTextPal[16] = {RGB_BLACK, RGB_WHITE, RGB(2,2,2), RGB_BLACK};
static const u8 sTextColors[] = {0, 1, 2};
static const u8 sBannerColors[] = {3, 1, 2};
static const u8 sSignature[] = _("by Juste Yoann");
static const u8 sPressStart[] = _("PRESS START");
static EWRAM_DATA u32 sPresentationTick = 0;
static EWRAM_DATA bool8 sPresentationLeaving = FALSE;
static EWRAM_DATA bool8 sPresentationTitle = FALSE;
static const struct BgTemplate sBgs[] = {
    {.bg=0, .charBaseIndex=0, .mapBaseIndex=28, .screenSize=1, .paletteMode=0, .priority=2},
    {.bg=1, .charBaseIndex=2, .mapBaseIndex=30, .screenSize=0, .paletteMode=0, .priority=1},
    {.bg=2, .charBaseIndex=3, .mapBaseIndex=31, .screenSize=0, .paletteMode=0, .priority=0},
};
static const struct WindowTemplate sIntroWindows[] = {
    {.bg=2, .tilemapLeft=1, .tilemapTop=8, .width=28, .height=3, .paletteNum=15, .baseBlock=128},
    DUMMY_WIN_TEMPLATE
};
static const struct WindowTemplate sTitleWindows[] = {
    {.bg=2, .tilemapLeft=0, .tilemapTop=17, .width=30, .height=3, .paletteNum=15, .baseBlock=128},
    DUMMY_WIN_TEMPLATE
};
static void VBlankPresentation(void)
{
    LoadOam(); ProcessSpriteCopyRequests(); TransferPlttBuffer();
}
static void StopPresentationMusic(void)
{
    ResetMapMusic();
    YokaiDiscardPausedSample(&gMPlayInfo_BGM);
    m4aMPlayStop(&gMPlayInfo_BGM);
}
static void PrintCentered(u8 font, u8 y, const u8 *text)
{
    s32 x = ((sPresentationTitle ? 240 : 224) - GetStringWidth(font, text, 0)) / 2;
    AddTextPrinterParameterized3(0, font, x < 0 ? 0 : x, y, sPresentationTitle ? sBannerColors : sTextColors, TEXT_SKIP_DRAW, text);
}
static void PresentationCleanup(void)
{
    SetVBlankCallback(NULL); FreeAllWindowBuffers();
    SetGpuReg(REG_OFFSET_BLDCNT, 0); SetGpuReg(REG_OFFSET_DISPCNT, 0);
}
static void EnterMainMenu(void)
{
    StopPresentationMusic(); PresentationCleanup();
    SeedRngAndSetTrainerId(); SetSaveBlocksPointers(); ResetMenuAndMonGlobals();
    Save_ResetSaveCounters(); LoadGameSave(SAVE_NORMAL);
    if (gSaveFileStatus == SAVE_STATUS_EMPTY || gSaveFileStatus == SAVE_STATUS_INVALID)
        Sav2_ClearSetDefault();
    SetPokemonCryStereo(gSaveBlock2Ptr->optionsSound);
    InitHeap(gHeap, HEAP_SIZE); SetMainCallback2(CB2_InitMainMenu);
}
static void CB2_RunYokaiPresentation(void)
{
    sPresentationTick++;
    if (!sPresentationTitle)
    {
        if (sPresentationTick == 104)
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        if (sPresentationTick >= 120 && !gPaletteFade.active)
        {
            PresentationCleanup(); SetMainCallback2(CB2_InitYokaiTitle); return;
        }
    }
    else
    {
        u32 alpha = sPresentationTick < 300 ? sPresentationTick * 16 / 300 : 16;
        /* 11/256px/frame: 2.57px/s at real GBA refresh. Content moves right. */
        ChangeBgX(0, 0u - sPresentationTick * 11, BG_COORD_SET);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(alpha, 16 - alpha));
        if (sPresentationTick >= 300 && (sPresentationTick - 300) % 40 == 0)
        {
            FillWindowPixelBuffer(0, 0x33);
            if ((sPresentationTick - 300) % 80 == 0) PrintCentered(FONT_SMALL, 4, sPressStart);
            CopyWindowToVram(0, COPYWIN_FULL);
        }
        if (!sPresentationLeaving)
        {
            if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_UP) == (B_BUTTON | SELECT_BUTTON | DPAD_UP))
            {
                StopPresentationMusic(); PresentationCleanup();
                SetMainCallback2(CB2_SaveClearScreen_Init); return;
            }
            if (JOY_HELD(B_BUTTON | SELECT_BUTTON) == (B_BUTTON | SELECT_BUTTON) && JOY_NEW(R_BUTTON))
            {
                StopPresentationMusic(); PresentationCleanup();
                SetMainCallback2(CB2_InitBerryFixProgram); return;
            }
            if (JOY_NEW(A_BUTTON | START_BUTTON))
            {
                StopPresentationMusic(); sPresentationLeaving = TRUE;
                BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            }
        }
        if (sPresentationLeaving && !gPaletteFade.active) { EnterMainMenu(); return; }
    }
    RunTasks(); AnimateSprites(); BuildOamBuffer(); UpdatePaletteFade();
}
static void SetupPresentation(bool8 title)
{
    u8 i;
    SetVBlankCallback(NULL); SetGpuReg(REG_OFFSET_DISPCNT, 0);
    StopPresentationMusic();
    if (!title) m4aMPlayAllStop();
    HelpSystem_Disable(); InitHeap(gHeap, HEAP_SIZE); ResetTasks();
    ResetSpriteData(); FreeAllSpritePalettes(); ResetPaletteFade();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    DmaClear32(3, (void *)OAM, OAM_SIZE); DmaClear16(3, (void *)PLTT, PLTT_SIZE);
    ResetBgsAndClearDma3BusyFlags(FALSE); InitBgsFromTemplates(0, sBgs, NELEMS(sBgs));
    for (i=0; i<4; i++) { ChangeBgX(i,0,BG_COORD_SET); ChangeBgY(i,0,BG_COORD_SET); }
    SetGpuReg(REG_OFFSET_BLDCNT, 0); SetGpuReg(REG_OFFSET_BLDY, 0);
    LoadPalette(sTextPal, BG_PLTT_ID(15), sizeof(sTextPal));
    InitWindows(title ? sTitleWindows : sIntroWindows); DeactivateAllTextPrinters();
    FillWindowPixelBuffer(0, 0); PutWindowTilemap(0);
    sPresentationTitle=title; sPresentationTick=0; sPresentationLeaving=FALSE;
    if (title)
    {
        FillWindowPixelBuffer(0, 0x33);
        StartTimer1();
        LoadPalette(sLandscapePal, 0, sizeof(sLandscapePal));
        LoadPalette(sLogoPal, BG_PLTT_ID(1), sizeof(sLogoPal));
        LZ77UnCompVram(sLandscapeTiles, (void *)BG_VRAM);
        CpuCopy16(sLandscapeMap, (void *)(BG_VRAM + 28 * BG_SCREEN_SIZE), sizeof(sLandscapeMap));
        LZ77UnCompVram(sLogoTiles, (void *)(BG_VRAM + 2 * BG_CHAR_SIZE));
        CpuCopy16(sLogoMap, (void *)(BG_VRAM + 30 * BG_SCREEN_SIZE), sizeof(sLogoMap));
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG1 | BLDCNT_TGT2_BG0 | BLDCNT_TGT2_BD | BLDCNT_EFFECT_BLEND);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(0, 16));
        /* Existing music audition candidate; no extra title sample. */
        m4aSongNumStartOrChange(MUS_YOKAI_NATHAN_HOUSE);
    }
    else PrintCentered(FONT_NORMAL, 4, sSignature);
    CopyWindowToVram(0,COPYWIN_FULL); SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0);
    if (title) { ShowBg(0); ShowBg(1); }
    ShowBg(2); BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankPresentation); SetMainCallback2(CB2_RunYokaiPresentation);
}
void CB2_InitYokaiIntro(void) { SetupPresentation(FALSE); }
void CB2_InitYokaiTitle(void) { SetupPresentation(TRUE); }

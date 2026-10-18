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
#include "constants/songs.h"

/* Shared 240x160 composition: 600 8bpp tiles (38400 bytes) below char base3.
 * Text lives at char base3, before screen block28; no framebuffer in EWRAM. */
static const u32 sNightTiles[] = INCBIN_U32("graphics/yokai_presentation/nuit.8bpp.lz");
static const u16 sNightPal[] = INCBIN_U16("graphics/yokai_presentation/nuit.gbapal");
static const u16 sNightMap[] = INCBIN_U16("graphics/yokai_presentation/nuit.bin");
static const u16 sTextPal[16] = {RGB(0,0,0), RGB(31,31,31), RGB(4,12,16), RGB(1,3,8)};
static const u8 sTextColors[] = {0, 1, 2};
static const u8 sFooterColors[] = {3, 1, 2};
static const u8 sNightOne[] = _("La nuit tombe sur Kanto...");
static const u8 sNightTwo[] = _("Les Yo-kai s'éveillent.");
static const u8 sNightThree[] = _("Ouvrez les yeux sur l'invisible.");
static const u8 sTitleOne[] = _("POKÉMON");
static const u8 sTitleTwo[] = _("× YO-KAI WATCH");
static const u8 sTitleBeta[] = _("BÊTA DE DÉVELOPPEMENT");
static const u8 sPressStart[] = _("A / START : JOUER");
static EWRAM_DATA u16 sPresentationTick = 0;
static EWRAM_DATA bool8 sPresentationLeaving = FALSE;
static EWRAM_DATA bool8 sPresentationTitle = FALSE;

static const struct BgTemplate sBgs[] = {
    {.bg=0, .charBaseIndex=0, .mapBaseIndex=28, .screenSize=0, .paletteMode=1, .priority=2},
    {.bg=1, .charBaseIndex=3, .mapBaseIndex=30, .screenSize=0, .paletteMode=0, .priority=0},
};
static const struct WindowTemplate sWindows[] = {
    {.bg=1, .tilemapLeft=1, .tilemapTop=1, .width=28, .height=6, .paletteNum=15, .baseBlock=1},
    {.bg=1, .tilemapLeft=1, .tilemapTop=18, .width=28, .height=2, .paletteNum=15, .baseBlock=169},
    DUMMY_WIN_TEMPLATE
};
static void VBlankPresentation(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}
static void PrintCentered(u8 window, u8 font, u8 y, const u8 *text)
{
    s32 x = (224 - GetStringWidth(font, text, 0)) / 2;
    AddTextPrinterParameterized3(window, font, x < 0 ? 0 : x, y,
        window == 1 ? sFooterColors : sTextColors, TEXT_SKIP_DRAW, text);
}
static void IntroCaption(const u8 *text)
{
    FillWindowPixelBuffer(0, 0);
    PrintCentered(0, FONT_NORMAL, 12, text);
    CopyWindowToVram(0, COPYWIN_FULL);
}
static void PresentationCleanup(void)
{
    SetVBlankCallback(NULL);
    FreeAllWindowBuffers();
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
}
static void EnterMainMenu(void)
{
    PresentationCleanup();
    SeedRngAndSetTrainerId();
    SetSaveBlocksPointers();
    ResetMenuAndMonGlobals();
    Save_ResetSaveCounters();
    LoadGameSave(SAVE_NORMAL);
    if (gSaveFileStatus == SAVE_STATUS_EMPTY || gSaveFileStatus == SAVE_STATUS_INVALID)
        Sav2_ClearSetDefault();
    SetPokemonCryStereo(gSaveBlock2Ptr->optionsSound);
    InitHeap(gHeap, HEAP_SIZE);
    SetMainCallback2(CB2_InitMainMenu);
}
static void CB2_RunYokaiPresentation(void)
{
    sPresentationTick++;
    if (!sPresentationTitle)
    {
        if (sPresentationTick == 30) IntroCaption(sNightOne);
        if (sPresentationTick == 130) IntroCaption(sNightTwo);
        if (sPresentationTick == 235) IntroCaption(sNightThree);
        if (sPresentationTick == 150) BeginNormalPaletteFade(PALETTES_BG, 0, 0, 4, RGB(0,15,18));
        if (sPresentationTick == 175) BeginNormalPaletteFade(PALETTES_BG, 0, 4, 0, RGB(0,15,18));
        if (!sPresentationLeaving && (sPresentationTick >= 350 || JOY_NEW(A_BUTTON | B_BUTTON | START_BUTTON)))
        {
            sPresentationLeaving = TRUE;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        }
        if (sPresentationLeaving && !gPaletteFade.active)
        {
            PresentationCleanup();
            SetMainCallback2(CB2_InitYokaiTitle);
            return;
        }
    }
    else
    {
        if (!sPresentationLeaving && !gPaletteFade.active)
        {
            if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_UP) == (B_BUTTON | SELECT_BUTTON | DPAD_UP))
            {
                PresentationCleanup();
                SetMainCallback2(CB2_SaveClearScreen_Init);
                return;
            }
            if (JOY_HELD(B_BUTTON | SELECT_BUTTON) == (B_BUTTON | SELECT_BUTTON) && JOY_NEW(R_BUTTON))
            {
                PresentationCleanup();
                SetMainCallback2(CB2_InitBerryFixProgram);
                return;
            }
            if (JOY_NEW(A_BUTTON | START_BUTTON))
            {
                sPresentationLeaving = TRUE;
                BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
                FadeOutBGM(4);
            }
            if (sPresentationTick % 40 == 0)
            {
                FillWindowPixelBuffer(1, 0x33);
                if (sPresentationTick % 80 == 0) PrintCentered(1, FONT_SMALL, 1, sPressStart);
                CopyWindowToVram(1, COPYWIN_FULL);
            }
        }
        if (sPresentationLeaving && !gPaletteFade.active)
        {
            EnterMainMenu();
            return;
        }
    }
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}
static void SetupPresentation(bool8 title)
{
    u8 i;
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    HelpSystem_Disable();
    InitHeap(gHeap, HEAP_SIZE);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    DmaClear32(3, (void *)OAM, OAM_SIZE);
    DmaClear16(3, (void *)PLTT, PLTT_SIZE);
    ResetBgsAndClearDma3BusyFlags(FALSE);
    InitBgsFromTemplates(0, sBgs, NELEMS(sBgs));
    for (i=0; i<4; i++) { ChangeBgX(i,0,0); ChangeBgY(i,0,0); }
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    LoadPalette(sNightPal, 0, sizeof(sNightPal));
    LoadPalette(sTextPal, BG_PLTT_ID(15), sizeof(sTextPal));
    LZ77UnCompVram(sNightTiles, (void *)BG_VRAM);
    CpuCopy16(sNightMap, (void *)(BG_VRAM + 28 * BG_SCREEN_SIZE), sizeof(sNightMap));
    InitWindows(sWindows);
    DeactivateAllTextPrinters();
    for (i=0; i<2; i++) { FillWindowPixelBuffer(i,0); PutWindowTilemap(i); }
    sPresentationTitle=title;
    sPresentationTick=0;
    sPresentationLeaving=FALSE;
    if (title)
    {
        StartTimer1();
        PrintCentered(0, FONT_NORMAL, 0, sTitleOne);
        PrintCentered(0, FONT_NORMAL, 16, sTitleTwo);
        PrintCentered(0, FONT_SMALL, 35, sTitleBeta);
        FillWindowPixelBuffer(1,0x33);
        PrintCentered(1, FONT_SMALL, 1, sPressStart);
    }
    CopyWindowToVram(0,COPYWIN_FULL);
    CopyWindowToVram(1,COPYWIN_FULL);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0);
    ShowBg(0);
    ShowBg(1);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    m4aSongNumStartOrChange(MUS_YOKAI_CURIOUS);
    SetVBlankCallback(VBlankPresentation);
    SetMainCallback2(CB2_RunYokaiPresentation);
}
void CB2_InitYokaiIntro(void) { SetupPresentation(FALSE); }
void CB2_InitYokaiTitle(void) { SetupPresentation(TRUE); }

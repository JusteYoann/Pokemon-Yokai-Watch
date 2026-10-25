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
#include "field_weather.h"
#include "constants/songs.h"

/* Title: gradient/head share char0 (head starts at tile128), maps28/29.
 * Logo uses char1/map30; text uses char3/map31. Fog uses OBJ tiles.
 * No full-frame EWRAM buffer, and logo/text remain above the white fog. */
static const u32 sLandscapeTiles[] = INCBIN_U32("graphics/yokai_title/fond_20261025.4bpp.lz");
static const u16 sLandscapePal[] = INCBIN_U16("graphics/yokai_title/fond_20261025.gbapal");
static const u16 sLandscapeMap[] = INCBIN_U16("graphics/yokai_title/fond_20261025.bin");
static const u32 sLogoTiles[] = INCBIN_U32("graphics/yokai_title/logo_20261025.4bpp.lz");
static const u16 sLogoPal[] = INCBIN_U16("graphics/yokai_title/logo_20261025.gbapal");
static const u16 sLogoMap[] = INCBIN_U16("graphics/yokai_title/logo_20261025.bin");
static const u32 sHeadTiles[] = INCBIN_U32("graphics/yokai_title/jibanyan.4bpp.lz");
static const u16 sHeadMap[] = INCBIN_U16("graphics/yokai_title/jibanyan.bin");
static const u16 sHeadPal[] = INCBIN_U16("graphics/yokai_title/jibanyan.gbapal");
static const u32 sPressTiles[] = INCBIN_U32("graphics/yokai_title/press_start.4bpp.lz");
static const u16 sPressMap[] = INCBIN_U16("graphics/yokai_title/press_start.bin");
static const u16 sPressPal[] = INCBIN_U16("graphics/yokai_title/press_start.gbapal");
#define TITLE_RISE_FRAMES 419 // At 59.7275 Hz, the introduction lasts at least 7 s.
#define TITLE_HEAD_TRAVEL 96
#define TITLE_FOG_TAG 0x12F2
static const u16 sTextPal[16] = {RGB_BLACK, RGB_WHITE, RGB(2,2,2), RGB_BLACK};
static const u8 sTextColors[] = {0, 1, 2};
static const u8 sBannerColors[] = {3, 1, 2};
static const u8 sSignature[] = _("par Juste Yoann");
static EWRAM_DATA u32 sPresentationTick = 0;
static EWRAM_DATA bool8 sPresentationLeaving = FALSE;
static EWRAM_DATA bool8 sPresentationTitle = FALSE;
static const struct BgTemplate sBgs[] = {
    {.bg=0, .charBaseIndex=0, .mapBaseIndex=28, .screenSize=1, .paletteMode=0, .priority=2},
    {.bg=1, .charBaseIndex=2, .mapBaseIndex=30, .screenSize=0, .paletteMode=0, .priority=1},
    {.bg=2, .charBaseIndex=3, .mapBaseIndex=31, .screenSize=0, .paletteMode=0, .priority=0},
};
static const struct BgTemplate sTitleBgs[] = {
    {.bg=0, .charBaseIndex=0, .mapBaseIndex=28, .screenSize=0, .priority=3},
    {.bg=1, .charBaseIndex=0, .mapBaseIndex=29, .screenSize=0, .priority=2},
    {.bg=2, .charBaseIndex=1, .mapBaseIndex=30, .screenSize=0, .priority=0},
    {.bg=3, .charBaseIndex=3, .mapBaseIndex=31, .screenSize=0, .priority=0},
};
static const struct WindowTemplate sIntroWindows[] = {
    {.bg=2, .tilemapLeft=1, .tilemapTop=8, .width=28, .height=3, .paletteNum=15, .baseBlock=128},
    DUMMY_WIN_TEMPLATE
};
static const struct WindowTemplate sTitleWindows[] = {
    {.bg=3, .tilemapLeft=0, .tilemapTop=14, .width=30, .height=3, .paletteNum=15, .baseBlock=128},
    DUMMY_WIN_TEMPLATE
};
static void Sprite_TitleFog(struct Sprite *sprite)
{
    sprite->x = (sprite->data[0] % 5) * 64 + 32 - ((sPresentationTick >> 2) & 63);
    sprite->y = (sprite->data[0] / 5) * 64 + 24;
}
static const struct OamData sTitleFogOam = {
    .objMode=ST_OAM_OBJ_BLEND, .shape=SPRITE_SHAPE(64x64),
    .size=SPRITE_SIZE(64x64), .priority=1,
};
static const union AnimCmd sTitleFogAnim[] = { ANIMCMD_FRAME(0, 16), ANIMCMD_JUMP(0) };
static const union AnimCmd *const sTitleFogAnims[] = { sTitleFogAnim };
static const u16 sTitleFogPalette[16] = {
    RGB_BLACK, RGB_WHITE, RGB_WHITE, RGB_WHITE,
    RGB(27,27,27), RGB(29,29,29), RGB(30,30,30), RGB_WHITE,
    RGB(28,28,28), RGB_WHITE, RGB_WHITE, RGB_WHITE,
    RGB(29,29,29), RGB(30,30,30), RGB_WHITE, RGB_WHITE
};
static const struct SpriteTemplate sTitleFogTemplate = {
    .tileTag=TITLE_FOG_TAG, .paletteTag=TITLE_FOG_TAG,
    .oam=&sTitleFogOam, .anims=sTitleFogAnims,
    .images=NULL, .affineAnims=gDummySpriteAffineAnimTable, .callback=Sprite_TitleFog,
};
static void CreateTitleFog(void)
{
    const struct SpriteSheet sheet={gWeatherFogHorizontalTiles,0x800,TITLE_FOG_TAG};
    const struct SpritePalette palette={sTitleFogPalette,TITLE_FOG_TAG};
    u8 i, id;
    LoadSpriteSheet(&sheet);
    LoadSpritePalette(&palette);
    for (i=0; i<15; i++)
    {
        id=CreateSprite(&sTitleFogTemplate,0,0,0);
        if (id==MAX_SPRITES) break;
        gSprites[id].data[0]=i;
        Sprite_TitleFog(&gSprites[id]);
    }
}
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
        u32 elapsed = sPresentationTick < TITLE_RISE_FRAMES ? sPresentationTick : TITLE_RISE_FRAMES;
        ChangeBgY(1, 0u - ((TITLE_HEAD_TRAVEL * 256) * (TITLE_RISE_FRAMES - elapsed) / TITLE_RISE_FRAMES), BG_COORD_SET);
        if (sPresentationTick >= TITLE_RISE_FRAMES && (sPresentationTick - TITLE_RISE_FRAMES) % 40 == 0)
        {
            if ((sPresentationTick - TITLE_RISE_FRAMES) % 80 == 0)
                CpuCopy16(sPressMap, (void *)(BG_VRAM + 31 * BG_SCREEN_SIZE), sizeof(sPressMap));
            else
                CpuFill16(0, (void *)(BG_VRAM + 31 * BG_SCREEN_SIZE), sizeof(sPressMap));
        }
        if (!sPresentationLeaving && sPresentationTick >= TITLE_RISE_FRAMES)
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
    ResetBgsAndClearDma3BusyFlags(FALSE);
    InitBgsFromTemplates(0, title ? sTitleBgs : sBgs, title ? NELEMS(sTitleBgs) : NELEMS(sBgs));
    for (i=0; i<4; i++) { ChangeBgX(i,0,BG_COORD_SET); ChangeBgY(i,0,BG_COORD_SET); }
    SetGpuReg(REG_OFFSET_BLDCNT, 0); SetGpuReg(REG_OFFSET_BLDY, 0);
    LoadPalette(sTextPal, BG_PLTT_ID(15), sizeof(sTextPal));
    InitWindows(title ? sTitleWindows : sIntroWindows); DeactivateAllTextPrinters();
    FillWindowPixelBuffer(0, 0); PutWindowTilemap(0);
    sPresentationTitle=title; sPresentationTick=0; sPresentationLeaving=FALSE;
    if (title)
    {
        FillWindowPixelBuffer(0, 0);
        StartTimer1();
        LoadPalette(sLandscapePal, 0, sizeof(sLandscapePal));
        LoadPalette(sLogoPal, BG_PLTT_ID(1), sizeof(sLogoPal));
        LoadPalette(sHeadPal, BG_PLTT_ID(2), sizeof(sHeadPal));
        LoadPalette(sPressPal, BG_PLTT_ID(15), sizeof(sPressPal));
        LZ77UnCompVram(sLandscapeTiles, (void *)BG_VRAM);
        CpuCopy16(sLandscapeMap, (void *)(BG_VRAM + 28 * BG_SCREEN_SIZE), sizeof(sLandscapeMap));
        LZ77UnCompVram(sHeadTiles, (void *)(BG_VRAM + 0x1000));
        CpuCopy16(sHeadMap, (void *)(BG_VRAM + 29 * BG_SCREEN_SIZE), sizeof(sHeadMap));
        ChangeBgY(1, 0u - TITLE_HEAD_TRAVEL * 256, BG_COORD_SET);
        LZ77UnCompVram(sLogoTiles, (void *)(BG_VRAM + BG_CHAR_SIZE));
        CpuCopy16(sLogoMap, (void *)(BG_VRAM + 30 * BG_SCREEN_SIZE), sizeof(sLogoMap));
        LZ77UnCompVram(sPressTiles, (void *)(BG_VRAM + 3 * BG_CHAR_SIZE));
        CreateTitleFog();
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_BG0 | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BD | BLDCNT_EFFECT_BLEND);
        // Same coefficients as the Terr’heure: fog 3/16, background 13/16.
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(3, 13));
        /* Existing music audition candidate; no extra title sample. */
        m4aSongNumStartOrChange(MUS_YOKAI_NATHAN_HOUSE);
    }
    else PrintCentered(FONT_NORMAL, 4, sSignature);
    CopyWindowToVram(0,COPYWIN_FULL);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | (title ? DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP : 0));
    if (title) { ShowBg(0); ShowBg(1); ShowBg(3); }
    ShowBg(2); BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankPresentation); SetMainCallback2(CB2_RunYokaiPresentation);
}
void CB2_InitYokaiIntro(void) { SetupPresentation(FALSE); }
void CB2_InitYokaiTitle(void) { SetupPresentation(TRUE); }

#include "global.h"
#include "gflib.h"
#include "juste_yoann.h"
#include "event_data.h"
#include "pokedex.h"
#include "script.h"
#include "sound.h"
#include "task.h"
#include "menu.h"
#include "new_menu_helpers.h"
#include "item.h"
#include "constants/flags.h"
#include "constants/items.h"

// Check each owned bit, including Mew/Enma. Native diploma counting excludes
// some mythical species and therefore is not a sufficient quest condition.
bool8 YoannMedalliumComplete(void)
{
    u16 number;
    for (number = 1; number <= 151; number++)
        if (!GetSetPokedexFlag(number, FLAG_GET_CAUGHT))
            return FALSE;
    return TRUE;
}

void YoannCheckCompletion(void)
{
    gSpecialVar_Result = !FlagGet(FLAG_YOANN_INVITED) && YoannMedalliumComplete();
}

void YoannSyncVisibility(void)
{
    if (FlagGet(FLAG_YOANN_INVITED))
        FlagClear(FLAG_HIDE_JUSTE_YOANN);
    else
        FlagSet(FLAG_HIDE_JUSTE_YOANN);
}

void YoannGiveCharm(void)
{
    gSpecialVar_Result = FALSE;
    if (FlagGet(FLAG_YOANN_CHARM_GIVEN))
        return;
    if (CheckBagHasItem(ITEM_SHINY_CHARM, 1) || AddBagItem(ITEM_SHINY_CHARM, 1))
    {
        FlagSet(FLAG_YOANN_CHARM_GIVEN);
        gSpecialVar_Result = TRUE;
    }
}

static void Task_YoannWaitFade(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        DestroyTask(taskId);
        ScriptContext_Enable();
    }
}

void YoannFadeWhite(void)
{
    // Keep both field message/frame palettes readable throughout the speech.
    BeginNormalPaletteFade(PALETTES_ALL & ~((1 << 14) | (1 << 15)), 3,
        gSpecialVar_0x8004, gSpecialVar_0x8005, RGB_WHITE);
    CreateTask(Task_YoannWaitFade, 0);
}

static const u8 sThankForPlay[] = _("THANK FOR PLAY");
static const u8 sThankColors[] = {0, 2, 3};
static const struct WindowTemplate sThankWindow =
{
    .bg = 0, .tilemapLeft = 1, .tilemapTop = 9,
    .width = 28, .height = 3, .paletteNum = 15, .baseBlock = 0x200,
};

static void Task_YoannThank(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    if (gPaletteFade.active)
        return;
    switch (data[0])
    {
    case 0:
        data[1] = AddWindow(&sThankWindow);
        if (data[1] == WINDOW_NONE)
        {
            data[0] = 3;
            break;
        }
        Menu_LoadStdPalAt(BG_PLTT_ID(15));
        FillWindowPixelBuffer(data[1], PIXEL_FILL(0));
        AddTextPrinterParameterized3(data[1], FONT_NORMAL,
            (224 - GetStringWidth(FONT_NORMAL, sThankForPlay, 0)) / 2,
            4, sThankColors, TEXT_SKIP_DRAW, sThankForPlay);
        PutWindowTilemap(data[1]);
        CopyWindowToVram(data[1], COPYWIN_FULL);
        BeginNormalPaletteFade(1 << 15, 2, 16, 0, RGB_WHITE);
        data[0]++;
        break;
    case 1:
        if (++data[2] >= 180)
        {
            BeginNormalPaletteFade(1 << 15, 2, 0, 16, RGB_WHITE);
            data[0]++;
        }
        break;
    case 2:
        ClearWindowTilemap(data[1]);
        CopyWindowToVram(data[1], COPYWIN_MAP);
        RemoveWindow(data[1]);
        data[0]++;
        // fall through
    case 3:
        BeginNormalPaletteFade(PALETTES_ALL, 3, 16, 0, RGB_WHITE);
        FadeInBGM(4);
        data[0]++;
        break;
    case 4:
        DestroyTask(taskId);
        ScriptContext_Enable();
        break;
    }
}

void YoannThankForPlay(void)
{
    // A single short-lived task and a small temporary window. No EWRAM globals,
    // permanent allocations, map changes, or weather/palette callback changes.
    FadeOutBGMTemporarily(4);
    BeginNormalPaletteFade(PALETTES_ALL, 3, 14, 16, RGB_WHITE);
    CreateTask(Task_YoannThank, 0);
}

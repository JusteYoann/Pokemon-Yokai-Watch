#include "global.h"
#include "gflib.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "script.h"
#include "task.h"
#include "constants/event_objects.h"

// No map or destination is assigned here. The caller resumes on a white
// screen, so a future story script can perform its own warp before fading in.
static const u32 sPanelTiles[] = INCBIN_U32("graphics/yokai_characters/porte_terreur/panneau.4bpp");
static const struct SpriteFrameImage sPanelImages[] = {{(const u8 *)sPanelTiles, 512}};
static const struct OamData sPanelOam = {
    .shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 2,
};
static const union AnimCmd sPanelAnim[] = { ANIMCMD_FRAME(0, 16), ANIMCMD_JUMP(0) };
static const union AnimCmd *const sPanelAnims[] = { sPanelAnim };
static const struct SpriteTemplate sPanelTemplate = {
    .tileTag = TAG_NONE, .paletteTag = TAG_NONE,
    .oam = &sPanelOam, .anims = sPanelAnims, .images = sPanelImages,
    .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static void Task_PorteTerreur(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    struct Sprite *panel = &gSprites[data[0]];
    struct Sprite *door = &gSprites[data[1]];
    switch (data[3])
    {
    case 0:
        // The same leaf tiles are translated 12 pixels, one pixel every two
        // frames. The stationary jamb and the player do not move.
        panel->x2 = ++data[2] / 2;
        if (data[2] == 24) { data[2] = 0; data[3]++; }
        break;
    case 1:
        if (++data[2] == 18)
        {
            BeginNormalPaletteFade(PALETTES_ALL, 1, 0, 16, RGB_WHITE);
            data[3]++;
        }
        break;
    case 2:
        if (!gPaletteFade.active)
        {
            // Clean up while white; reopening or a later map reload cannot
            // retain a stray panel sprite or an open collision actor.
            DestroySprite(panel);
            StartSpriteAnim(door, 0);
            DestroyTask(taskId);
            ScriptContext_Enable();
        }
        break;
    }
}

void PorteTerreurOuvrir(void)
{
    u8 objectId, taskId, panelId;
    struct Sprite *door;
    struct Sprite *panel;
    gSpecialVar_Result = FALSE;
    if (FuncIsActiveTask(Task_PorteTerreur))
        return;
    if (TryGetObjectEventIdByLocalIdAndMap(gSpecialVar_LastTalked,
        gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup, &objectId))
        return;
    if (gObjectEvents[objectId].graphicsId != OBJ_EVENT_GFX_PORTE_TERREUR)
        return;
    for (taskId = 0; taskId < NUM_TASKS; taskId++)
        if (!gTasks[taskId].isActive) break;
    if (taskId == NUM_TASKS) return;
    door = &gSprites[gObjectEvents[objectId].spriteId];
    panelId = CreateSprite(&sPanelTemplate, door->x, door->y, 0);
    if (panelId == MAX_SPRITES) return;
    panel = &gSprites[panelId];
    panel->coordOffsetEnabled = door->coordOffsetEnabled;
    panel->oam.paletteNum = door->oam.paletteNum;
    panel->oam.priority = door->oam.priority;
    StartSpriteAnim(door, 1);
    taskId = CreateTask(Task_PorteTerreur, 80);
    gTasks[taskId].data[0] = panelId;
    gTasks[taskId].data[1] = gObjectEvents[objectId].spriteId;
    gSpecialVar_Result = TRUE;
}

#include "global.h"
#include "philosovni.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "main.h"
#include "overworld.h"
#include "palette.h"
#include "script.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/maps.h"
#include "constants/vars.h"

#define FOLLOWER_LOCAL_ID 202
#define TRAIL_LENGTH 16
#define REMINDER_FRAMES 300
extern const u8 Philosovni_IdleReminder[];

// Membership comes from the existing saved quest state. No save layout change.
static EWRAM_DATA struct {
    struct Coords16 trail[TRAIL_LENGTH];
    struct Coords16 player;
    u16 idle;
    u8 head, count, mapGroup, mapNum;
    bool8 initialized, reminded;
    u8 palette;
} sFollower = {0};

u8 PhilosovniFollowerPalette(void)
{
    return sFollower.palette >= 7 && sFollower.palette <= 11 ? sFollower.palette : 7;
}

bool8 PhilosovniFollowing(void)
{
    u16 state = VarGet(VAR_PHILOSOVNI_STATE);
    return state == 1 || state == 2;
}

bool8 PhilosovniIsFollower(const struct ObjectEvent *object)
{
    return object->active && object->graphicsId == OBJ_EVENT_GFX_ARIANE && PhilosovniFollowing();
}

bool8 PhilosovniFollowerCollision(const struct ObjectEvent *a, const struct ObjectEvent *b)
{
    // The player may turn back without becoming trapped by their companion.
    return (a->isPlayer && PhilosovniIsFollower(b)) || (b->isPlayer && PhilosovniIsFollower(a));
}

static struct ObjectEvent *FindFollower(void)
{
    u8 i;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
        if (PhilosovniIsFollower(&gObjectEvents[i])) return &gObjectEvents[i];
    return NULL;
}

void PhilosovniEndFollowing(void)
{
    u8 i;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
        if (gObjectEvents[i].active && (gObjectEvents[i].localId == FOLLOWER_LOCAL_ID
            || gObjectEvents[i].graphicsId == OBJ_EVENT_GFX_ARIANE))
            RemoveObjectEventByLocalIdAndMap(gObjectEvents[i].localId, gObjectEvents[i].mapNum, gObjectEvents[i].mapGroup);
    sFollower.initialized = FALSE;
}

u16 PhilosovniFollowerDestination(void)
{
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_VERMILION_CITY_PHILOSOVNI_WAREHOUSE)
     && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_VERMILION_CITY_PHILOSOVNI_WAREHOUSE)) return 1;
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_VERMILION_CITY)
     && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_VERMILION_CITY)) return 2;
    return 0;
}

static void ResetTrail(const struct ObjectEvent *player)
{
    sFollower.player = player->currentCoords;
    sFollower.head = sFollower.count = sFollower.idle = 0;
    sFollower.reminded = FALSE;
    sFollower.mapGroup = gSaveBlock1Ptr->location.mapGroup;
    sFollower.mapNum = gSaveBlock1Ptr->location.mapNum;
    sFollower.initialized = TRUE;
}

static bool8 PlaceBehind(struct ObjectEvent *follower, const struct ObjectEvent *player)
{
    u8 i, dir;
    s16 x, y;
    for (i = 0; i < 5; i++)
    {
        dir = (i == 0) ? (player->facingDirection == DIR_SOUTH ? DIR_NORTH : player->facingDirection == DIR_NORTH ? DIR_SOUTH : player->facingDirection == DIR_WEST ? DIR_EAST : DIR_WEST) : i;
        if (dir < DIR_SOUTH || dir > DIR_EAST) dir = DIR_SOUTH;
        x = player->currentCoords.x;
        y = player->currentCoords.y;
        if (dir == DIR_SOUTH) y++;
        if (dir == DIR_NORTH) y--;
        if (dir == DIR_WEST) x--;
        if (dir == DIR_EAST) x++;
        if (!(GetCollisionFlagsAtCoords(follower, x, y, dir) & 14))
        {
            ObjectEventClearHeldMovementIfActive(follower);
            MoveObjectEventToMapCoords(follower, x, y);
            follower->currentElevation = player->currentElevation;
            ObjectEventTurn(follower, player->facingDirection);
            return TRUE;
        }
    }
    return FALSE;
}

void PhilosovniFollowerUpdate(void)
{
    struct ObjectEvent *player, *follower;
    struct Coords16 target;
    s16 dx, dy;
    u8 id, dir;
    bool8 changedMap;
    u16 used;
    u8 i, bank;
    if (!PhilosovniFollowing()) { sFollower.initialized = FALSE; return; }
    if (gPlayerAvatar.objectEventId >= OBJECT_EVENTS_COUNT) return;
    player = &gObjectEvents[gPlayerAvatar.objectEventId];
    if (!player->active) return;
    follower = FindFollower();
    changedMap = !sFollower.initialized || sFollower.mapGroup != gSaveBlock1Ptr->location.mapGroup
        || sFollower.mapNum != gSaveBlock1Ptr->location.mapNum;
    if (gPlayerAvatar.flags & PLAYER_AVATAR_FLAG_SURFING)
    {
        if (follower) follower->invisible = TRUE;
        ResetTrail(player);
        return;
    }
    if (!follower)
    {
        id = SpawnSpecialObjectEventParameterized(OBJ_EVENT_GFX_ARIANE, MOVEMENT_TYPE_FACE_DOWN,
            FOLLOWER_LOCAL_ID, player->currentCoords.x, player->currentCoords.y, player->currentElevation);
        if (id >= OBJECT_EVENTS_COUNT) return;
        follower = &gObjectEvents[id];
        PlaceBehind(follower, player);
        changedMap = TRUE;
    }
    if (follower->invisible) { PlaceBehind(follower, player); follower->invisible = FALSE; }
    // Keep the companion's separate palette intact after native NPC spawning.
    used = 0;
    for (i = 0; i < MAX_SPRITES; i++)
        if (gSprites[i].inUse && i != follower->spriteId) used |= 1 << gSprites[i].oam.paletteNum;
    bank = PhilosovniFollowerPalette();
    if (used & (1 << bank))
        for (bank = 7; bank <= 11 && (used & (1 << bank)); bank++);
    if (bank <= 11 && (bank != sFollower.palette || gSprites[follower->spriteId].oam.paletteNum != bank))
    {
        sFollower.palette = bank;
        ObjectEventSetGraphicsId(follower, OBJ_EVENT_GFX_ARIANE);
    }
    if (changedMap) ResetTrail(player);
    if (ArePlayerFieldControlsLocked() || ScriptContext_IsEnabled() || gPaletteFade.active || gPlayerAvatar.preventStep)
    { sFollower.idle = 0; return; }
    follower->frozen = FALSE;
    if (player->currentCoords.x != sFollower.player.x || player->currentCoords.y != sFollower.player.y)
    {
        if (sFollower.count == TRAIL_LENGTH) { PlaceBehind(follower, player); ResetTrail(player); }
        else
        {
            sFollower.trail[(sFollower.head + sFollower.count) % TRAIL_LENGTH] = sFollower.player;
            sFollower.count++;
            sFollower.player = player->currentCoords;
        }
        sFollower.idle = 0;
        sFollower.reminded = FALSE;
    }
    else if (!player->singleMovementActive && (!player->heldMovementActive || player->heldMovementFinished) && !sFollower.reminded)
    {
        if (++sFollower.idle >= REMINDER_FRAMES)
        {
            sFollower.reminded = TRUE;
            LockPlayerFieldControls();
            ScriptContext_SetupScript(Philosovni_IdleReminder);
            return;
        }
    }
    if (ObjectEventIsHeldMovementActive(follower) && !ObjectEventClearHeldMovementIfFinished(follower)) return;
    if (!sFollower.count) return;
    target = sFollower.trail[sFollower.head];
    dx = target.x - follower->currentCoords.x;
    dy = target.y - follower->currentCoords.y;
    if (!dx && !dy) { sFollower.head = (sFollower.head + 1) % TRAIL_LENGTH; sFollower.count--; return; }
    if (dx && dy) { PlaceBehind(follower, player); ResetTrail(player); return; }
    if (dx > 2 || dx < -2 || dy > 2 || dy < -2) { PlaceBehind(follower, player); ResetTrail(player); return; }
    dir = dx ? (dx > 0 ? DIR_EAST : DIR_WEST) : (dy > 0 ? DIR_SOUTH : DIR_NORTH);
    if (GetCollisionFlagsAtCoords(follower, target.x, target.y, dir) & 14) return;
    if (ObjectEventSetHeldMovement(follower, (dx == 2 || dx == -2 || dy == 2 || dy == -2)
        ? GetJump2MovementAction(dir)
        : (sFollower.count > 1 || (gPlayerAvatar.flags & (PLAYER_AVATAR_FLAG_DASH | PLAYER_AVATAR_FLAG_MACH_BIKE | PLAYER_AVATAR_FLAG_ACRO_BIKE)))
            ? GetWalkFastMovementAction(dir) : GetWalkNormalMovementAction(dir))) return;
    sFollower.head = (sFollower.head + 1) % TRAIL_LENGTH;
    sFollower.count--;
}

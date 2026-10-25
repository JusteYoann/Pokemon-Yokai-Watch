#include "global.h"
#include "gflib.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "overworld.h"
#include "script.h"
#include "task.h"
#include "util.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/map_event_ids.h"
#include "constants/maps.h"

#define ENMA_CELLS 1024
#define ENMA_STEPS 128
struct EnmaRoute { u8 actor, departure, count, cursor, waiting, path[ENMA_STEPS]; };
struct EnmaSearch { u16 queue[ENMA_CELLS]; u8 parent[ENMA_CELLS]; };
static const s8 sEnmaDx[] = {0, 0, -1, 1};
static const s8 sEnmaDy[] = {1, -1, 0, 0};
static const u8 sEnmaReverse[] = {1, 0, 3, 2};

static u8 EnmaActor(void)
{
    return GetObjectEventIdByLocalIdAndMap(LOCALID_PG_ENMA_INTRO, MAP_NUM(MAP_PALLET_TOWN), MAP_GROUP(MAP_PALLET_TOWN));
}
static bool8 EnmaFloor(s16 x, s16 y, u8 self)
{
    u8 i, elevation = MapGridGetElevationAt(x + 7, y + 7);
    if (MapGridGetCollisionAt(x + 7, y + 7) || (elevation != 0 && elevation != 3))
        return FALSE;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
        if (i != self && gObjectEvents[i].active
            && gObjectEvents[i].currentCoords.x == x + 7 && gObjectEvents[i].currentCoords.y == y + 7)
            return FALSE;
    return TRUE;
}
static bool8 EnmaPlan(struct EnmaRoute *route, u8 self, s16 sx, s16 sy, s16 gx, s16 gy)
{
    struct EnmaSearch *search;
    u16 width = gMapHeader.mapLayout->width, height = gMapHeader.mapLayout->height;
    u16 head = 0, tail = 1, cell, next, start, goal;
    s16 x, y; u8 d, reverse[ENMA_STEPS], length = 0;
    bool8 found = FALSE;
    if (width * height > ENMA_CELLS || sx < 0 || sy < 0 || gx < 0 || gy < 0
        || sx >= width || gx >= width || sy >= height || gy >= height
        || !EnmaFloor(sx, sy, self) || !EnmaFloor(gx, gy, self))
        return FALSE;
    search = AllocZeroed(sizeof(*search));
    if (search == NULL)
        return FALSE;
    start = sy * width + sx; goal = gy * width + gx;
    search->queue[0] = start; search->parent[start] = 5;
    while (head < tail)
    {
        cell = search->queue[head++];
        if (cell == goal) { found = TRUE; break; }
        for (d = 0; d < 4; d++)
        {
            x = cell % width + sEnmaDx[d]; y = cell / width + sEnmaDy[d];
            if (x < 0 || y < 0 || x >= width || y >= height)
                continue;
            next = y * width + x;
            if (!search->parent[next] && EnmaFloor(x, y, self))
            {
                search->parent[next] = d + 1; search->queue[tail++] = next;
            }
        }
    }
    if (found)
    {
        for (cell = goal; cell != start;)
        {
            if (length == ENMA_STEPS) { found = FALSE; break; }
            d = search->parent[cell] - 1; reverse[length++] = d;
            cell = (cell / width + sEnmaDy[sEnmaReverse[d]]) * width + cell % width + sEnmaDx[sEnmaReverse[d]];
        }
        route->count = 0;
        while (length) route->path[route->count++] = reverse[--length];
    }
    Free(search);
    return found;
}
static void EnmaFinish(u8 taskId, struct EnmaRoute *route, bool8 success)
{
    if (route->departure || !success)
    {
        RemoveObjectEventByLocalIdAndMap(LOCALID_PG_ENMA_INTRO, MAP_NUM(MAP_PALLET_TOWN), MAP_GROUP(MAP_PALLET_TOWN));
        FlagSet(FLAG_PG_HIDE_ENMA_INTRO);
    }
    else
    {
        ObjectEventTurn(&gObjectEvents[gPlayerAvatar.objectEventId], DIR_SOUTH);
        ObjectEventTurn(&gObjectEvents[route->actor], DIR_NORTH);
    }
    Free(route); DestroyTask(taskId); gSpecialVar_Result = success; ScriptContext_Enable();
}
static void Task_EnmaRoute(u8 taskId)
{
    struct EnmaRoute *route; struct ObjectEvent *actor; u32 word;
    LoadWordFromTwoHalfwords((u16 *)gTasks[taskId].data, &word); route = (struct EnmaRoute *)word;
    if (route->actor >= OBJECT_EVENTS_COUNT || !gObjectEvents[route->actor].active)
    { EnmaFinish(taskId, route, FALSE); return; }
    actor = &gObjectEvents[route->actor];
    if (route->waiting)
    {
        if (!ObjectEventClearHeldMovementIfFinished(actor)) return;
        route->waiting = FALSE; route->cursor++;
    }
    if (route->cursor == route->count) { EnmaFinish(taskId, route, TRUE); return; }
    if (ObjectEventIsHeldMovementActive(actor) && !ObjectEventClearHeldMovementIfFinished(actor)) return;
    if (ObjectEventIsMovementOverridden(actor)) return;
    if (!ObjectEventSetHeldMovement(actor, MOVEMENT_ACTION_WALK_NORMAL_DOWN + route->path[route->cursor]))
        route->waiting = TRUE;
}
static void StartEnmaRoute(bool8 departure)
{
    struct EnmaRoute *route; u8 taskId, north, self = EnmaActor();
    s16 sx, sy, gx, gy; bool8 found = FALSE;
    gSpecialVar_Result = FALSE;
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_PALLET_TOWN)
        || gSaveBlock1Ptr->location.mapNum != MAP_NUM(MAP_PALLET_TOWN)) return;
    for (taskId = 0; taskId < NUM_TASKS && gTasks[taskId].isActive; taskId++);
    if (taskId == NUM_TASKS) return;
    route = AllocZeroed(sizeof(*route));
    if (route == NULL) return;
    route->departure = departure;
    if (departure && self >= OBJECT_EVENTS_COUNT) { Free(route); return; }
    for (north = 12; north <= 13 && !found; north++)
    {
        sx = departure ? gObjectEvents[self].currentCoords.x - 7 : north;
        sy = departure ? gObjectEvents[self].currentCoords.y - 7 : 1;
        gx = departure ? north : gSaveBlock1Ptr->pos.x;
        gy = departure ? 1 : gSaveBlock1Ptr->pos.y + 2;
        found = EnmaPlan(route, self, sx, sy, gx, gy);
        if (found && !departure)
        {
            SetObjEventTemplateCoords(LOCALID_PG_ENMA_INTRO, sx, sy);
            FlagClear(FLAG_PG_HIDE_ENMA_INTRO);
            self = TrySpawnObjectEvent(LOCALID_PG_ENMA_INTRO, MAP_NUM(MAP_PALLET_TOWN), MAP_GROUP(MAP_PALLET_TOWN));
        }
    }
    if (!found || self >= OBJECT_EVENTS_COUNT) { Free(route); return; }
    route->actor = self; taskId = CreateTask(Task_EnmaRoute, 8);
    StoreWordInTwoHalfwords((u16 *)gTasks[taskId].data, (u32)route); gSpecialVar_Result = TRUE;
}
void PostgameEnmaArrival(void) { StartEnmaRoute(FALSE); }
void PostgameEnmaDeparture(void) { StartEnmaRoute(TRUE); }

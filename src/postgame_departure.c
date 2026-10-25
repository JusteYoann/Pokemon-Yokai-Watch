#include "global.h"
#include "gflib.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "metatile_behavior.h"
#include "script.h"
#include "task.h"
#include "util.h"
#include "constants/event_object_movement.h"

#define ROUTE_CELLS 4096
#define ROUTE_STEPS 192
struct DepartureRoute { u8 actor, count, cursor, waiting, approach, path[ROUTE_STEPS]; };
struct DepartureSearch { u16 queue[ROUTE_CELLS]; u8 parent[ROUTE_CELLS]; };
static const s8 sDx[] = {0, 0, -1, 1};
static const s8 sDy[] = {1, -1, 0, 0};
static const u8 sReverse[] = {1, 0, 3, 2};

static bool8 Floor(s16 x, s16 y, u8 self)
{
    u8 i, elevation = MapGridGetElevationAt(x + 7, y + 7);
    if (MapGridGetCollisionAt(x + 7, y + 7) || (elevation != 0 && elevation != 3)
        || MetatileBehavior_IsWater(MapGridGetMetatileBehaviorAt(x + 7, y + 7))) return FALSE;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
        if (i != self && gObjectEvents[i].active
            && gObjectEvents[i].currentCoords.x == x + 7 && gObjectEvents[i].currentCoords.y == y + 7) return FALSE;
    return TRUE;
}
static void Finish(u8 taskId, struct DepartureRoute *route, bool8 success)
{
    struct ObjectEvent *actor = &gObjectEvents[route->actor];
    if (success && !route->approach) RemoveObjectEventByLocalIdAndMap(actor->localId, actor->mapNum, actor->mapGroup);
    else if (success) ObjectEventTurn(actor, actor->currentCoords.x < 26 ? DIR_EAST : actor->currentCoords.x > 26 ? DIR_WEST : actor->currentCoords.y < 31 ? DIR_SOUTH : DIR_NORTH);
    Free(route); DestroyTask(taskId); gSpecialVar_Result = success; ScriptContext_Enable();
}
static void Task_Departure(u8 taskId)
{
    struct DepartureRoute *route; struct ObjectEvent *actor; u32 word; s16 x, y; u8 d;
    LoadWordFromTwoHalfwords((u16 *)gTasks[taskId].data, &word); route = (struct DepartureRoute *)word;
    actor = &gObjectEvents[route->actor];
    if (!actor->active) { Finish(taskId, route, FALSE); return; }
    if (route->waiting)
    {
        if (!ObjectEventClearHeldMovementIfFinished(actor)) return;
        route->waiting = FALSE; route->cursor++;
    }
    if (route->cursor == route->count) { Finish(taskId, route, TRUE); return; }
    if (ObjectEventIsHeldMovementActive(actor) && !ObjectEventClearHeldMovementIfFinished(actor)) return;
    if (ObjectEventIsMovementOverridden(actor)) return;
    d = route->path[route->cursor]; x = actor->currentCoords.x - 7 + sDx[d]; y = actor->currentCoords.y - 7 + sDy[d];
    if (!Floor(x, y, route->actor)) { Finish(taskId, route, FALSE); return; }
    if (!ObjectEventSetHeldMovement(actor, MOVEMENT_ACTION_WALK_NORMAL_DOWN + d)) route->waiting = TRUE;
}
// 8004: actor local ID; 8005: 1 = approach the Carmin tree, 0 = leave the screen.
void PostgameScientistDeparture(void)
{
    struct DepartureRoute *route; struct DepartureSearch *search;
    u16 width = gMapHeader.mapLayout->width, height = gMapHeader.mapLayout->height;
    u16 head = 0, tail = 1, cell, next, start, goal = 0;
    s16 x, y, px = gSaveBlock1Ptr->pos.x, py = gSaveBlock1Ptr->pos.y;
    u8 d, length = 0, reverse[ROUTE_STEPS], taskId, self;
    bool8 found = FALSE;
    gSpecialVar_Result = FALSE;
    self = GetObjectEventIdByLocalIdAndMap(gSpecialVar_0x8004, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
    if (self >= OBJECT_EVENTS_COUNT || width * height > ROUTE_CELLS) return;
    for (taskId = 0; taskId < NUM_TASKS && gTasks[taskId].isActive; taskId++);
    if (taskId == NUM_TASKS) return;
    route = AllocZeroed(sizeof(*route)); search = AllocZeroed(sizeof(*search));
    if (!route || !search) { Free(route); Free(search); return; }
    route->actor = self; route->approach = gSpecialVar_0x8005;
    start = (gObjectEvents[self].currentCoords.y - 7) * width + gObjectEvents[self].currentCoords.x - 7;
    search->queue[0] = start; search->parent[start] = 5;
    while (head < tail)
    {
        cell = search->queue[head++]; x = cell % width; y = cell / width;
        if (route->approach ? abs(x - 19) + abs(y - 24) == 1 : (abs(x - px) > 9 || abs(y - py) > 7))
        { found = TRUE; goal = cell; break; }
        for (d = 0; d < 4; d++)
        {
            x = cell % width + sDx[d]; y = cell / width + sDy[d];
            if (x < 0 || y < 0 || x >= width || y >= height) continue;
            next = y * width + x;
            if (!search->parent[next] && Floor(x, y, self)) { search->parent[next] = d + 1; search->queue[tail++] = next; }
        }
    }
    if (found)
        for (cell = goal; cell != start;)
        {
            if (length == ROUTE_STEPS) { found = FALSE; break; }
            d = search->parent[cell] - 1; reverse[length++] = d;
            cell = (cell / width + sDy[sReverse[d]]) * width + cell % width + sDx[sReverse[d]];
        }
    Free(search);
    if (!found) { Free(route); return; }
    while (length) route->path[route->count++] = reverse[--length];
    taskId = CreateTask(Task_Departure, 8); StoreWordInTwoHalfwords((u16 *)gTasks[taskId].data, (u32)route); gSpecialVar_Result = TRUE;
}

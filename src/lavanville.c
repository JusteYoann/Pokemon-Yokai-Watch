#include "yokai_champions.h"
#include "global.h"
#include "gflib.h"
#include "lavanville.h"
#include "battle.h"
#include "battle_main.h"
#include "battle_anim.h"
#include "constants/trainer_types.h"
#include "battle_setup.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "overworld.h"
#include "constants/game_stat.h"
#include "pokemon.h"
#include "script.h"
#include "script_pokemon_util.h"
#include "string_util.h"
#include "constants/maps.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/species.h"
#include "constants/moves.h"
#include "constants/items.h"
#include "malloc.h"
#include "task.h"

static EWRAM_DATA u16 sZombieCooldown = 0;
static EWRAM_DATA bool8 sZombieSightApproach = FALSE;
extern const u8 LavenderZombie_Variant1[];
extern const u8 LavenderZombie_Errant[];
static const u32 sZombiePics[4][512] = {
    INCBIN_U32("graphics/yokai_zombies/errant/battle-front.4bpp"),
    INCBIN_U32("graphics/yokai_zombies/sprinteur/battle-front.4bpp"),
    INCBIN_U32("graphics/yokai_zombies/colosse/battle-front.4bpp"),
    INCBIN_U32("graphics/yokai_zombies/spectral/battle-front.4bpp"),
};
static const u16 sZombiePals[4][16] = {
    INCBIN_U16("graphics/yokai_zombies/errant/battle-front.gbapal"),
    INCBIN_U16("graphics/yokai_zombies/sprinteur/battle-front.gbapal"),
    INCBIN_U16("graphics/yokai_zombies/colosse/battle-front.gbapal"),
    INCBIN_U16("graphics/yokai_zombies/spectral/battle-front.gbapal"),
};
static const u8 sZombieNames[4][11] = {_("Z. ERRANT"), _("Z. RAPIDE"), _("Z. COLOSSE"), _("Z. SPECTRE")};
// hp/attack/defense/speed/spAttack/spDefense, four distinct level-24 opponents.
static const u16 sZombieStats[4][6] = {
    {85, 50, 45, 28, 35, 40}, {70, 54, 34, 72, 32, 36},
    {110, 62, 62, 19, 28, 42}, {78, 30, 35, 48, 55, 62},
};
static const u16 sZombieMoves[4][4] = {
    {MOVE_LICK, MOVE_SCRATCH, MOVE_LEER, MOVE_ASTONISH},
    {MOVE_BITE, MOVE_QUICK_ATTACK, MOVE_LEER, MOVE_LICK},
    {MOVE_POUND, MOVE_ROCK_THROW, MOVE_LEER, MOVE_ASTONISH},
    {MOVE_LICK, MOVE_NIGHT_SHADE, MOVE_SPITE, MOVE_ASTONISH},
};

bool8 IsLavanvilleNight(void)
{
    return gSaveBlock1Ptr != NULL && gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_LAVENDER_TOWN)
        && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_LAVENDER_TOWN);
}

// Visual approach only: keep IsLavanvilleNight town-only for fog and zombies.
// The final 32 route tiles smoothly reach the unchanged town palette in both
// directions, without a timer or persistent state in the saved game.
u8 LavanvilleNightStrength(void)
{
    s32 distance;
    u16 map;
    if (gSaveBlock1Ptr == NULL)
        return 0;
    if (IsLavanvilleNight())
        return 32;
    if (gMapHeader.mapLayout == NULL)
        return 0;
    map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    switch (map)
    {
    case MAP_ROUTE8:
        distance = gMapHeader.mapLayout->width - 1 - gSaveBlock1Ptr->pos.x;
        break;
    case MAP_ROUTE10:
        distance = gMapHeader.mapLayout->height - 1 - gSaveBlock1Ptr->pos.y;
        break;
    case MAP_ROUTE12:
        distance = gSaveBlock1Ptr->pos.y;
        break;
    default:
        return 0;
    }
    if (distance <= 0)
        return 32;
    if (distance >= 32)
        return 0;
    return 32 - distance;
}

// Apply only to hardware output. The source buffers stay unmodified, so fades,
// menus and repeated VBlanks cannot accumulate tint. UI banks 12..15 stay intact.
void LavanvilleNightPalette(void)
{
    u16 i;
    u16 strength;
    u16 redFactor, blueFactor, lightFactor;
    if (!IsFieldPaletteView())
        return;
    strength = LavanvilleNightStrength();
    if (strength == 0)
        return;
    redFactor = 1024 - strength * 14;
    blueFactor = 1024 - strength * 8;
    lightFactor = strength * 4;
    for (i = 0; i < 192; i++)
    {
        u16 c = gPlttBufferFaded[i];
        u16 red = c & 31, green = (c >> 5) & 31, blue = (c >> 10) & 31;
        u16 light = red > green ? red : green;
        u16 r = red * redFactor / 1024;
        u16 g = green * redFactor / 1024;
        u16 b;
        if (blue > light) light = blue;
        b = (blue * blueFactor + light * lightFactor) / 1024;
        ((vu16 *)PLTT)[i] = RGB(r, g, b);
    }
}

void LavanvilleZombieImmunity(void) { sZombieCooldown = 180; }
u16 LavanvilleCheckZombieImmunity(void)
{
    return gSpecialVar_Result = !FlagGet(FLAG_BADGE04_GET) && sZombieCooldown != 0;
}

void LavanvilleStartZombieBattle(void)
{
    u8 v = gSpecialVar_0x8004 & 3;
    u8 i;
    static const u8 fields[] = {MON_DATA_MAX_HP, MON_DATA_ATK, MON_DATA_DEF, MON_DATA_SPEED, MON_DATA_SPATK, MON_DATA_SPDEF};
    CreateScriptedWildMon(SPECIES_NIDORAN_M, 24, ITEM_NONE);
    SetMonData(&gEnemyParty[0], MON_DATA_NICKNAME, sZombieNames[v]);
    for (i = 0; i < 6; i++)
        SetMonData(&gEnemyParty[0], fields[i], &sZombieStats[v][i]);
    SetMonData(&gEnemyParty[0], MON_DATA_HP, &sZombieStats[v][0]);
    for (i = 0; i < 4; i++)
        SetMonMoveSlot(&gEnemyParty[0], sZombieMoves[v][i], i);
    StartScriptedWildBattle();
    gBattleTypeFlags |= BATTLE_TYPE_LAVENDER_ZOMBIE | (v << 21);
    sZombieCooldown = 180;
}

bool8 LavanvilleLoadZombieGfx(u8 battler)
{
    u8 v;
    if ((!(gBattleTypeFlags & BATTLE_TYPE_LAVENDER_ZOMBIE) && !YokaiChampionIsColossus(battler)) || GetBattlerSide(battler) != B_SIDE_OPPONENT)
        return FALSE;
    v = YokaiChampionIsColossus(battler) ? 2 : (gBattleTypeFlags >> 21) & 3;
    if (YokaiChampionIsColossus(battler) && gBattleSpritesDataPtr->battlerData[battler].transformSpecies != SPECIES_NONE) return FALSE;
    CpuCopy32(sZombiePics[v], gMonSpritesGfxPtr->sprites[GetBattlerPosition(battler)], 2048);
    LoadPalette(sZombiePals[v], OBJ_PLTT_ID(battler), 32);
    LoadPalette(sZombiePals[v], BG_PLTT_ID(8 + battler), 32);
    return TRUE;
}

// Called before ordinary trainer sight; no victory flags are allocated for errants.
// Range is deliberately short and directional. Full tile collision and intervening
// actors are checked. All regular trainers keep their native one-time logic.
bool8 LavanvilleTryZombieSight(void)
{
    u8 i, n, dir;
    s16 px, py, x, y, dx, dy;
    if (!IsLavanvilleNight()) return FALSE;
    if (sZombieCooldown) { sZombieCooldown--; return FALSE; }
    if (FlagGet(FLAG_BADGE04_GET)) return FALSE;
    if (!FlagGet(FLAG_LAVENDER_INTRO_DONE)) return FALSE;
    PlayerGetDestCoords(&px, &py);
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *o = &gObjectEvents[i];
        if (!o->active || o->graphicsId != OBJ_EVENT_GFX_LAVENDER_ZOMBIE || o->trainerType != TRAINER_TYPE_NONE
            || o->trainerRange_berryTreeId == 0) continue;
        dir = o->facingDirection;
        dx = dir == DIR_EAST ? 1 : dir == DIR_WEST ? -1 : 0;
        dy = dir == DIR_SOUTH ? 1 : dir == DIR_NORTH ? -1 : 0;
        x = o->currentCoords.x; y = o->currentCoords.y;
        for (n = 1; n <= o->trainerRange_berryTreeId; n++)
        {
            x += dx; y += dy;
            if (MapGridGetCollisionAt(x, y)) break;
            if (x == px && y == py)
            {
                sZombieSightApproach = TRUE;
                gSelectedObjectEvent = i;
                gSpecialVar_LastTalked = o->localId;
                ScriptContext_SetupScript(GetObjectEventScriptPointerByObjectEventId(i));
                return TRUE;
            }
            if (GetObjectEventIdByPosition(x, y, o->currentElevation) != OBJECT_EVENTS_COUNT) break;
        }
    }
    return FALSE;
}

// Patrol period includes the walking animation: ~60 or ~120 field frames.
u16 LavanvilleZombieStepDelay(struct ObjectEvent *object)
{
    if (!IsLavanvilleNight() || object->graphicsId != OBJ_EVENT_GFX_LAVENDER_ZOMBIE)
        return 0;
    return GetObjectEventScriptPointerByObjectEventId(object - gObjectEvents) == LavenderZombie_Variant1 ? 44 : 88;
}

static void Task_ZombieApproach(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    struct ObjectEvent *object = &gObjectEvents[task->data[0]];
    s16 px, py, dx, dy, x, y;
    u8 dir, collision, oldX, oldY;
    if (object->heldMovementActive && !ObjectEventClearHeldMovementIfFinished(object)) return;
    if (!task->data[1] || !object->active || FlagGet(FLAG_BADGE04_GET)) goto finish;
    PlayerGetDestCoords(&px, &py);
    dx = px - object->currentCoords.x; dy = py - object->currentCoords.y;
    if ((dx && dy) || (dx < 0 ? -dx : dx) + (dy < 0 ? -dy : dy) <= 1) goto finish;
    dir = dx > 0 ? DIR_EAST : dx < 0 ? DIR_WEST : dy > 0 ? DIR_SOUTH : DIR_NORTH;
    x = object->currentCoords.x + (dx > 0 ? 1 : dx < 0 ? -1 : 0);
    y = object->currentCoords.y + (dy > 0 ? 1 : dy < 0 ? -1 : 0);
    oldX = object->rangeX; oldY = object->rangeY;
    object->rangeX = object->rangeY = 15;
    collision = GetCollisionAtCoords(object, x, y, dir);
    object->rangeX = oldX; object->rangeY = oldY;
    if (collision) goto finish;
    ObjectEventTurn(object, dir);
    ObjectEventSetHeldMovement(object, GetWalkSlowerMovementAction(dir));
    task->data[1]--;
    return;
finish:
    if (object->active) object->initialCoords = object->currentCoords;
    DestroyTask(taskId);
    ScriptContext_Enable();
}

void LavanvilleZombieApproach(void)
{
    u8 task = CreateTask(Task_ZombieApproach, 8);
    gTasks[task].data[0] = gSelectedObjectEvent;
    gTasks[task].data[1] = sZombieSightApproach ? 4 : 0;
    sZombieSightApproach = FALSE;
}

// Scene adapts to all three entrances, Fly, Teleport and saved positions.
// Choose an unobstructed three-tile ray and its free side tile; never move player.
u16 LavanvillePrepareIntro(void)
{
    s16 px, py, x, y, ax, ay;
    u8 d, n;
    static const s8 dx[] = {0,0,0,-1,1};
    static const s8 dy[] = {0,1,-1,0,0};
    PlayerGetDestCoords(&px, &py);
    gSpecialVar_Result = 0;
    for (d = 1; d <= 4; d++)
    {
        for (n = 1; n <= 3; n++)
        {
            x = px + dx[d]*n; y = py + dy[d]*n;
            if (MapGridGetCollisionAt(x,y) || GetObjectEventIdByPosition(x,y,3) != OBJECT_EVENTS_COUNT) break;
        }
        if (n != 4) continue;
        ax = px + dx[d] - dy[d]; ay = py + dy[d] + dx[d];
        if (MapGridGetCollisionAt(ax,ay) || GetObjectEventIdByPosition(ax,ay,3) != OBJECT_EVENTS_COUNT) continue;
        if (SpawnSpecialObjectEventParameterized(OBJ_EVENT_GFX_LAVENDER_ZOMBIE, MOVEMENT_TYPE_FACE_DOWN, 200, px+3*dx[d], py+3*dy[d], 3) == OBJECT_EVENTS_COUNT) continue;
        if (SpawnSpecialObjectEventParameterized(OBJ_EVENT_GFX_YOKAI_ALYZON, MOVEMENT_TYPE_FACE_DOWN, 201, ax, ay, 3) == OBJECT_EVENTS_COUNT)
        { RemoveObjectEventByLocalIdAndMap(200, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup); continue; }
        ObjectEventTurn(&gObjectEvents[gPlayerAvatar.objectEventId], d);
        gSpecialVar_Result = d;
        return d;
    }
    return 0;
}

// Walk to the Tower using the existing collision map; actors are frozen by the
// script. A bounded breadth-first search prevents walking into walls or doors.
struct IntroWalk { u16 index, length; u8 objectId; u8 steps[480]; };
static void Task_IntroWalk(u8 taskId)
{
    struct IntroWalk *p = (void *)GetWordTaskArg(taskId, 0);
    struct ObjectEvent *o = &gObjectEvents[p->objectId];
    if (o->heldMovementActive && !ObjectEventClearHeldMovementIfFinished(o)) return;
    if (p->index == p->length)
    {
        Free(p); DestroyTask(taskId); ScriptContext_Enable(); return;
    }
    ObjectEventSetHeldMovement(o, GetWalkNormalMovementAction(p->steps[p->index++]));
}
u16 LavanvilleIntroDepart(void)
{
    u16 *prev = AllocZeroed(480 * sizeof(u16));
    u16 *queue = AllocZeroed(480 * sizeof(u16));
    struct IntroWalk *p = AllocZeroed(sizeof(*p));
    u8 oid = GetObjectEventIdByLocalIdAndMap(201, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
    u16 start, goal = 7*24+18, head = 0, tail = 0, at, next, i;
    s16 x,y,nx,ny;
    u8 d, task;
    static const s8 dx[] = {0,0,0,-1,1}, dy[] = {0,1,-1,0,0};
    gSpecialVar_Result = FALSE;
    if (!prev || !queue || !p || oid == OBJECT_EVENTS_COUNT) goto fail;
    x=gObjectEvents[oid].currentCoords.x-7; y=gObjectEvents[oid].currentCoords.y-7;
    if (x<0 || x>=24 || y<0 || y>=20) goto fail;
    start=y*24+x;
    for (i=0;i<480;i++) prev[i]=0xffff;
    queue[tail++]=start;prev[start]=start;
    while (head<tail && prev[goal]==0xffff)
    {
        at=queue[head++];x=at%24;y=at/24;
        for (d=1;d<=4;d++)
        {
            nx=x+dx[d];ny=y+dy[d];
            if(nx<0||nx>=24||ny<0||ny>=20)continue;
            next=ny*24+nx;
            if(prev[next]!=0xffff || MapGridGetCollisionAt(nx+7,ny+7))continue;
            if(GetObjectEventIdByPosition(nx+7,ny+7,3)!=OBJECT_EVENTS_COUNT)continue;
            prev[next]=at;queue[tail++]=next;
        }
    }
    if(prev[goal]==0xffff) goto fail;
    at=goal;
    while(at!=start && p->length<480)
    {
        next=prev[at];x=at%24-next%24;y=at/24-next/24;
        p->steps[p->length++]=x==1?DIR_EAST:x==-1?DIR_WEST:y==1?DIR_SOUTH:DIR_NORTH;at=next;
    }
    for(i=0;i<p->length/2;i++) { d=p->steps[i];p->steps[i]=p->steps[p->length-i-1];p->steps[p->length-i-1]=d; }
    p->objectId=oid;
    task=CreateTask(Task_IntroWalk,8);SetWordTaskArg(task,0,(u32)p);
    Free(prev);Free(queue);return gSpecialVar_Result=TRUE;
fail:
    if(prev)Free(prev);if(queue)Free(queue);if(p)Free(p);
    return gSpecialVar_Result=FALSE;
}

bool8 LavanvilleNeedsTemplateRefresh(void)
{
    u16 i;
    static const u16 maps[][2] = {
        {MAP_GROUP(MAP_LAVENDER_TOWN), MAP_NUM(MAP_LAVENDER_TOWN)},
        {MAP_GROUP(MAP_LAVENDER_TOWN_HOUSE1), MAP_NUM(MAP_LAVENDER_TOWN_HOUSE1)},
        {MAP_GROUP(MAP_LAVENDER_TOWN_HOUSE2), MAP_NUM(MAP_LAVENDER_TOWN_HOUSE2)},
        {MAP_GROUP(MAP_LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE), MAP_NUM(MAP_LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE)},
        {MAP_GROUP(MAP_LAVENDER_TOWN_MART), MAP_NUM(MAP_LAVENDER_TOWN_MART)},
        {MAP_GROUP(MAP_LAVENDER_TOWN_POKEMON_CENTER_1F), MAP_NUM(MAP_LAVENDER_TOWN_POKEMON_CENTER_1F)},
        {MAP_GROUP(MAP_LAVENDER_TOWN_POKEMON_CENTER_2F), MAP_NUM(MAP_LAVENDER_TOWN_POKEMON_CENTER_2F)},
        {MAP_GROUP(MAP_POKEMON_TOWER_1F), MAP_NUM(MAP_POKEMON_TOWER_1F)},
        {MAP_GROUP(MAP_POKEMON_TOWER_2F), MAP_NUM(MAP_POKEMON_TOWER_2F)},
        {MAP_GROUP(MAP_POKEMON_TOWER_3F), MAP_NUM(MAP_POKEMON_TOWER_3F)},
        {MAP_GROUP(MAP_POKEMON_TOWER_4F), MAP_NUM(MAP_POKEMON_TOWER_4F)},
        {MAP_GROUP(MAP_POKEMON_TOWER_5F), MAP_NUM(MAP_POKEMON_TOWER_5F)},
        {MAP_GROUP(MAP_POKEMON_TOWER_6F), MAP_NUM(MAP_POKEMON_TOWER_6F)},
        {MAP_GROUP(MAP_POKEMON_TOWER_7F), MAP_NUM(MAP_POKEMON_TOWER_7F)},
        {MAP_GROUP(MAP_CELADON_CITY_GYM), MAP_NUM(MAP_CELADON_CITY_GYM)},
    };
    for (i = 0; i < NELEMS(maps); i++)
        if (gSaveBlock1Ptr->location.mapGroup == maps[i][0] && gSaveBlock1Ptr->location.mapNum == maps[i][1])
            return TRUE;
    return FALSE;
}

u16 LavanvilleRematchReady(void)
{
    return gSpecialVar_Result = FlagGet(FLAG_SYS_GAME_CLEAR) && GetGameStat(GAME_STAT_ENTERED_HOF) != 0;
}

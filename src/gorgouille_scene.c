#include "global.h"
#include "gflib.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "metatile_behavior.h"
#include "script.h"
#include "sound.h"
#include "task.h"
#include "util.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/songs.h"

// Only this summit's four native Strength boulders participate. Planning uses
// the current object positions, so an already open player path costs no pushes.
#define CELLS 512
#define NODES 1536
#define HASH_SIZE 4096
#define STEPS 192
#define NONE 0xFFFF
struct Node { u16 pos, rock[4], parent; u8 move; };
struct Search {
    struct Node node[NODES];
    u16 hash[HASH_SIZE], queue[CELLS];
    u8 floor[CELLS], reach[CELLS];
    u16 count, width, height;
};
struct Scene {
    u8 mode, stage, actor, rockActor, waiting, parked, count, cursor;
    u8 path[STEPS];
};
static const s8 sDx[4]={0,0,-1,1}, sDy[4]={1,-1,0,0};
static const u8 sOpposite[4]={1,0,3,2};

static u8 Actor(u8 local)
{
    return GetObjectEventIdByLocalIdAndMap(local,MAP_NUM(MAP_MT_EMBER_SUMMIT),MAP_GROUP(MAP_MT_EMBER_SUMMIT));
}
static u16 Position(struct ObjectEvent *obj, u16 width)
{
    return (obj->currentCoords.y-7)*width+obj->currentCoords.x-7;
}
static u16 Next(struct Search *s,u16 cell,u8 dir)
{
    s16 x=cell%s->width+sDx[dir],y=cell/s->width+sDy[dir];
    return x<0 || y<0 || x>=s->width || y>=s->height ? NONE : y*s->width+x;
}
static bool8 RockAt(const struct Node *n,u16 cell)
{
    u8 i;for(i=0;i<4;i++)if(n->rock[i]==cell)return TRUE;return FALSE;
}
static void Flood(struct Search *s,const struct Node *n)
{
    u16 head=0,tail=1,cell,next;u8 d;
    CpuFill16(0,s->reach,sizeof(s->reach));s->queue[0]=n->pos;s->reach[n->pos]=5;
    while(head<tail) {
        cell=s->queue[head++];
        for(d=0;d<4;d++) {
            next=Next(s,cell,d);
            if(next!=NONE && s->floor[next] && !s->reach[next] && !RockAt(n,next)) {
                s->reach[next]=d+1;s->queue[tail++]=next;
            }
        }
    }
}
static bool8 AppendWalk(struct Search *s,struct Scene *scene,u16 from,u16 to)
{
    u8 reverse[STEPS],len=0,d;
    while(to!=from) {
        if(len==STEPS || !s->reach[to])return FALSE;
        d=s->reach[to]-1;reverse[len++]=d;to=Next(s,to,sOpposite[d]);
    }
    if(scene->count+len>=STEPS)return FALSE;
    while(len)scene->path[scene->count++]=reverse[--len];
    return TRUE;
}
static bool8 Same(const struct Node *a,const struct Node *b)
{
    u8 i;if(a->pos!=b->pos)return FALSE;
    for(i=0;i<4;i++)if(a->rock[i]!=b->rock[i])return FALSE;
    return TRUE;
}
static bool8 AddNode(struct Search *s,const struct Node *n)
{
    u32 hash=n->pos;u16 slot;u8 i;
    for(i=0;i<4;i++)hash=(hash*33)^n->rock[i];
    slot=hash&(HASH_SIZE-1);
    while(s->hash[slot]!=NONE) {
        if(Same(&s->node[s->hash[slot]],n))return FALSE;
        slot=(slot+1)&(HASH_SIZE-1);
    }
    if(s->count==NODES)return FALSE;
    s->node[s->count]=*n;s->hash[slot]=s->count++;return TRUE;
}
static bool8 Plan(struct Scene *scene,u8 actor,u8 x,u8 y,bool8 pushes)
{
    struct Search *s=AllocZeroed(sizeof(*s));struct Node next;
    u16 i,j,k,cell,goal,found=NONE,chain[64],depth=0,previous=0,behind,dest;
    u8 id,d,r;bool8 ok=FALSE;
    scene->count=scene->cursor=scene->waiting=0;scene->actor=actor;
    if(!s)return FALSE;
    s->width=gMapHeader.mapLayout->width;s->height=gMapHeader.mapLayout->height;
    if(s->width*s->height>CELLS || actor>=OBJECT_EVENTS_COUNT)goto done;
    goal=y*s->width+x;
    for(j=0;j<s->height;j++)for(i=0;i<s->width;i++) {
        u8 elevation=MapGridGetElevationAt(i+7,j+7);
        s->floor[j*s->width+i]=MapGridGetCollisionAt(i+7,j+7)==0
            && (elevation==0 || elevation==gObjectEvents[actor].currentElevation)
            && !MetatileBehavior_IsSurfable(MapGridGetMetatileBehaviorAt(i+7,j+7));
    }
    s->node[0].pos=Position(&gObjectEvents[actor],s->width);s->node[0].parent=NONE;
    for(r=0;r<4;r++) {id=Actor(r+2);s->node[0].rock[r]=id<OBJECT_EVENTS_COUNT?Position(&gObjectEvents[id],s->width):NONE;}
    for(i=0;i<OBJECT_EVENTS_COUNT;i++)if(gObjectEvents[i].active && i!=actor) {
        bool8 rock=FALSE;
        for(r=0;r<4;r++)if(i==Actor(r+2))rock=TRUE;
        if(!rock) {cell=Position(&gObjectEvents[i],s->width);if(cell<CELLS)s->floor[cell]=FALSE;}
    }
    CpuFill16(NONE,s->hash,sizeof(s->hash));s->count=0;AddNode(s,&s->node[0]);
    for(k=0;k<s->count;k++) {
        Flood(s,&s->node[k]);
        if(s->reach[goal]) {found=k;break;}
        if(!pushes)break;
        for(r=0;r<4;r++)if(s->node[k].rock[r]!=NONE)for(d=0;d<4;d++) {
            cell=s->node[k].rock[r];behind=Next(s,cell,sOpposite[d]);dest=Next(s,cell,d);
            if(behind==NONE || dest==NONE || !s->reach[behind] || !s->floor[dest] || RockAt(&s->node[k],dest))continue;
            next=s->node[k];next.parent=k;next.move=((r+1)<<2)|d;next.pos=cell;next.rock[r]=dest;AddNode(s,&next);
        }
    }
    if(found==NONE)goto done;
    for(k=found;k!=0;k=s->node[k].parent) {if(depth==64)goto done;chain[depth++]=k;}
    while(depth) {
        k=chain[--depth];r=(s->node[k].move>>2)-1;d=s->node[k].move&3;
        Flood(s,&s->node[previous]);behind=Next(s,s->node[previous].rock[r],sOpposite[d]);
        if(!AppendWalk(s,scene,s->node[previous].pos,behind) || scene->count==STEPS)goto done;
        scene->path[scene->count++]=s->node[k].move;previous=k;
    }
    Flood(s,&s->node[found]);ok=AppendWalk(s,scene,s->node[found].pos,goal);
done:
    Free(s);return ok;
}
static bool8 Step(struct Scene *s)
{
    struct ObjectEvent *a=&gObjectEvents[s->actor];u8 move,rock;
    if(s->waiting) {
        if(!ObjectEventClearHeldMovementIfFinished(a))return FALSE;
        if(s->rockActor<OBJECT_EVENTS_COUNT && !ObjectEventClearHeldMovementIfFinished(&gObjectEvents[s->rockActor]))return FALSE;
        s->waiting=FALSE;s->cursor++;
    }
    if(s->cursor==s->count)return TRUE;
    move=s->path[s->cursor];rock=move>>2;s->rockActor=OBJECT_EVENTS_COUNT;
    if(ObjectEventIsHeldMovementActive(a) && !ObjectEventClearHeldMovementIfFinished(a))return FALSE;
    if(ObjectEventIsMovementOverridden(a))return FALSE;
    if(rock) {
        s->rockActor=Actor(rock+1);
        if(ObjectEventIsHeldMovementActive(&gObjectEvents[s->rockActor]) && !ObjectEventClearHeldMovementIfFinished(&gObjectEvents[s->rockActor]))return FALSE;
        if(ObjectEventIsMovementOverridden(&gObjectEvents[s->rockActor]))return FALSE;
        ObjectEventSetHeldMovement(&gObjectEvents[s->rockActor],MOVEMENT_ACTION_WALK_NORMAL_DOWN+(move&3));
        PlaySE(SE_M_STRENGTH);
    }
    ObjectEventSetHeldMovement(a,MOVEMENT_ACTION_WALK_NORMAL_DOWN+(move&3));s->waiting=TRUE;
    return FALSE;
}
static void Finish(u8 task,struct Scene *s,bool8 success)
{
    if(!success && s && !s->mode) {
        RemoveObjectEventByLocalIdAndMap(7,MAP_NUM(MAP_MT_EMBER_SUMMIT),MAP_GROUP(MAP_MT_EMBER_SUMMIT));
        FlagSet(FLAG_HIDE_ONI_ALIZON);
    }
    Free(s);DestroyTask(task);gSpecialVar_Result=success;ScriptContext_Enable();
}
static void Task_Scene(u8 task)
{
    struct Scene *s;u8 player=gPlayerAvatar.objectEventId,id;u32 word;
    LoadWordFromTwoHalfwords((u16 *)gTasks[task].data,&word);s=(struct Scene *)word;
    if(!s) {Finish(task,s,FALSE);return;}
    if(s->waiting || s->cursor<s->count) {if(!Step(s))return;}
    if(!s->mode) {
        switch(s->stage++) {
        case 0:if(!Plan(s,player,9,9,FALSE))goto fail;break;
        case 1:if(!Plan(s,player,9,8,FALSE))goto fail;break;
        case 2:
            FlagClear(FLAG_HIDE_ONI_ALIZON);TrySpawnObjectEvent(7,MAP_NUM(MAP_MT_EMBER_SUMMIT),MAP_GROUP(MAP_MT_EMBER_SUMMIT));id=Actor(7);
            if(id>=OBJECT_EVENTS_COUNT || !Plan(s,id,10,9,TRUE))goto fail;break;
        case 3:if(!Plan(s,player,9,9,FALSE))goto fail;break;
        default:
            ObjectEventTurn(&gObjectEvents[player],DIR_NORTH);id=Actor(7);if(id<OBJECT_EVENTS_COUNT)ObjectEventTurn(&gObjectEvents[id],DIR_NORTH);
            Finish(task,s,TRUE);return;
        }
    } else {
        switch(s->stage++) {
        case 0:
            s->parked=gSaveBlock1Ptr->pos.x==9 && gSaveBlock1Ptr->pos.y==9;
            if(s->parked && !Plan(s,player,9,8,FALSE))goto fail;break;
        case 1:id=Actor(7);if(id>=OBJECT_EVENTS_COUNT || !Plan(s,id,9,15,TRUE))goto fail;break;
        case 2:
            RemoveObjectEventByLocalIdAndMap(7,MAP_NUM(MAP_MT_EMBER_SUMMIT),MAP_GROUP(MAP_MT_EMBER_SUMMIT));FlagSet(FLAG_HIDE_ONI_ALIZON);
            if(s->parked && !Plan(s,player,9,9,FALSE))goto fail;break;
        default:Finish(task,s,TRUE);return;
        }
    }
    return;
fail:Finish(task,s,FALSE);
}
static void Start(u8 mode)
{
    struct Scene *s=AllocZeroed(sizeof(*s));u8 task=CreateTask(Task_Scene,8);
    if(s)s->mode=mode;
    StoreWordInTwoHalfwords((u16 *)gTasks[task].data,(u32)s);
}
void GorgouilleAlizonArrival(void) {Start(0);}
void GorgouilleAlizonDeparture(void) {Start(1);}

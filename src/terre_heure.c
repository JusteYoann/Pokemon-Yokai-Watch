#include "global.h"
#include "gflib.h"
#include "terre_heure.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "field_effect.h"
#include "field_weather.h"
#include "item.h"
#include "main.h"
#include "malloc.h"
#include "overworld.h"
#include "pokemon.h"
#include "random.h"
#include "script.h"
#include "sound.h"
#include "task.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/maps.h"
#include "constants/vars.h"
#include "constants/field_effects.h"
#include "constants/songs.h"
#include "constants/rgb.h"
#include "constants/battle.h"
#include "battle.h"
#include "quest_log.h"
#include "constants/quest_log.h"
#include "text.h"
#include "string_util.h"
#include "window.h"
#include "menu.h"
#include "start_menu.h"
#include "help_system.h"
#include "characters.h"
#include "scanline_effect.h"
#include "field_fadetransition.h"

#define TH_LOCAL 230
#define TH_NONE 255
#define TH_SECONDS 360
#define TH_PATROLS 8
#define TH_EXTRA_PATROL_FIRST (TH_LOCAL+6)

static void MaintainPatrols(bool8 initial);
static u8 PatrolLocal(u8 index) { return index<2?TH_LOCAL+1+index:TH_EXTRA_PATROL_FIRST+index-2; }
struct ThPoint { u8 x, y, component; };
struct ThMap { u8 group, num, width, height, cave, pursuers; const u8 *labels; const struct ThPoint *points; u8 count; };
#include "data/terre_heure_maps.h"

// Small fixed session: survives the native heap reset at every map/menu load.
// Pathfinding work arrays are allocated only for one calculation and then freed.
static const u16 sTimerColors[16]={RGB_BLACK,RGB_WHITE,RGB_BLACK,RGB(31,3,3),RGB(31,26,0)};
static const u16 sRewardItems[]={ITEM_ULTRA_BALL,ITEM_RARE_CANDY,ITEM_MAX_POTION,ITEM_REVIVE};
static EWRAM_DATA struct {
    struct ObjectEventTemplate templates[6];
    struct WarpData origin;
    u32 clock, remaining;
    u16 cooldown, steps;
    u8 picked[7], loot[4];
    u8 active, phase, cave, map, doorMap, doorPoint, flash, tier, freeRoam;
    u8 alerted, seen, direction, aiDelay, patrolClock, window, seconds, helpWasEnabled;
} sTh = {};
extern const u8 TerreHeure_EventScript_Intro[], TerreHeure_EventScript_Door[];
extern const u8 TerreHeure_EventScript_Oni[], TerreHeure_EventScript_Chest[];
extern const u8 TerreHeure_EventScript_Failure[], TerreHeure_EventScript_Timeout[], TerreHeure_EventScript_Blocked[], TerreHeure_EventScript_StoredRewards[];

bool8 TerreHeureActive(void) { return sTh.active; }
static s16 CurrentMap(void)
{
    u8 i;
    for (i = 0; i < ARRAY_COUNT(sThMaps); i++)
        if (sThMaps[i].group == gSaveBlock1Ptr->location.mapGroup && sThMaps[i].num == gSaveBlock1Ptr->location.mapNum) return i;
    return -1;
}
static u8 Component(const struct ThMap *map, s16 x, s16 y)
{
    if (x < 0 || y < 0 || x >= map->width || y >= map->height) return 0;
    return map->labels[y * map->width + x];
}
static u8 Object(u8 local)
{
    u8 id;
    if (TryGetObjectEventIdByLocalIdAndMap(local, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup, &id)) return OBJECT_EVENTS_COUNT;
    return id;
}
const struct ObjectEventTemplate *TerreHeureTemplate(u8 localId, u8 num, u8 group)
{
    if (sTh.active && group == gSaveBlock1Ptr->location.mapGroup && num == gSaveBlock1Ptr->location.mapNum) {
        if(localId==TH_LOCAL+1 || localId==TH_LOCAL+2 || (localId>=TH_EXTRA_PATROL_FIRST && localId<TH_EXTRA_PATROL_FIRST+TH_PATROLS-2)) {
            u8 id=Object(localId);
            if(id<OBJECT_EVENTS_COUNT) {
                // Extra patrols share a script-only template; coordinates live in
                // their native ObjectEvent. No extra persistent RAM is required.
                struct ObjectEventTemplate *t=&sTh.templates[2];
                t->localId=localId;t->graphicsId=OBJ_EVENT_GFX_PATROUILLE_ONI;
                t->x=gObjectEvents[id].currentCoords.x-7;t->y=gObjectEvents[id].currentCoords.y-7;
                t->objUnion.normal.elevation=gObjectEvents[id].currentElevation;
                t->objUnion.normal.movementType=MOVEMENT_TYPE_FACE_DOWN;
                t->script=TerreHeure_EventScript_Blocked;
                return t;
            }
        }
        if(localId>=TH_LOCAL && localId<TH_LOCAL+6)return &sTh.templates[localId-TH_LOCAL];
    }
    return NULL;
}
static bool8 IsFree(s16 x, s16 y)
{
    u8 i;
    x += MAP_OFFSET; y += MAP_OFFSET;
    if (MapGridGetCollisionAt(x,y)) return FALSE;
    for (i=0;i<OBJECT_EVENTS_COUNT;i++)
        if (gObjectEvents[i].active && gObjectEvents[i].currentCoords.x==x && gObjectEvents[i].currentCoords.y==y) return FALSE;
    return TRUE;
}
static void Spawn(u8 slot, u8 gfx, u8 x, u8 y, const u8 *script)
{
    struct ObjectEventTemplate *t=&sTh.templates[slot];
    memset(t,0,sizeof(*t));t->localId=TH_LOCAL+slot;t->graphicsId=gfx;
    t->x=x;t->y=y;t->objUnion.normal.elevation=MapGridGetElevationAt(x+7,y+7);
    t->objUnion.normal.movementType=MOVEMENT_TYPE_FACE_DOWN;t->script=script;
    SpawnSpecialObjectEventParameterized(gfx,MOVEMENT_TYPE_FACE_DOWN,t->localId,x+7,y+7,t->objUnion.normal.elevation);
}
static void RemovePursuers(void)
{
    u8 i;
    for(i=0;i<=TH_PATROLS;i++) {
        u8 local=i?PatrolLocal(i-1):TH_LOCAL;
        if(Object(local)<OBJECT_EVENTS_COUNT)RemoveObjectEventByLocalIdAndMap(local,gSaveBlock1Ptr->location.mapNum,gSaveBlock1Ptr->location.mapGroup);
    }
}
static bool8 WasPicked(u8 slot)
{
    u8 bit=sTh.map*2+slot; return (sTh.picked[bit/8]>>(bit%8))&1;
}
static void Populate(void)
{
    const struct ThMap *map=&sThMaps[sTh.map];
    s16 x,y;u8 component,i,k=0;u8 gfx;
    PlayerGetDestCoords(&x,&y);x-=7;y-=7;component=Component(map,x,y);
    // All ordinary actors are restored from their native map templates on exit.
    // Keep boulders: collision/puzzle state is never changed by this event.
    for(i=0;i<OBJECT_EVENTS_COUNT;i++)
        if(gObjectEvents[i].active && i!=gPlayerAvatar.objectEventId
            && gObjectEvents[i].graphicsId!=OBJ_EVENT_GFX_PUSHABLE_BOULDER)
            RemoveObjectEventByLocalIdAndMap(gObjectEvents[i].localId,gSaveBlock1Ptr->location.mapNum,gSaveBlock1Ptr->location.mapGroup);
    memset(sTh.templates,0,sizeof(sTh.templates));
    if(sTh.map==sTh.doorMap) {
        const struct ThPoint *p=&map->points[sTh.doorPoint];
        Spawn(3,OBJ_EVENT_GFX_PORTE_TERREUR,p->x,p->y,TerreHeure_EventScript_Door);
    }
    gfx=sTh.tier==0?OBJ_EVENT_GFX_YOKAI_GARGAROS:sTh.tier==1?OBJ_EVENT_GFX_OGRALOS:OBJ_EVENT_GFX_ORQANOSTERREUR;
    for(i=0;i<map->count;i++) {
        const struct ThPoint *p=&map->points[i];
        if(p->component!=component || abs(p->x-x)+abs(p->y-y)<6 || !IsFree(p->x,p->y)) continue;
        if(k<3 && map->pursuers && !sTh.freeRoam) {
            Spawn(k,k?OBJ_EVENT_GFX_PATROUILLE_ONI:gfx,p->x,p->y,k?TerreHeure_EventScript_Blocked:TerreHeure_EventScript_Oni);k++;
        } else if(k<5) {
            u8 chest=k<3?0:k-3;
            if(!WasPicked(chest)) Spawn(4+chest,OBJ_EVENT_GFX_ITEM_BALL,p->x,p->y,TerreHeure_EventScript_Chest);
            k=4+chest;
        }
        if(k==5)break;
    }
    MaintainPatrols(TRUE);
    sTh.alerted=FALSE;sTh.seen=FALSE;sTh.direction=0;sTh.aiDelay=0;
    PlayNewMapMusic(MUS_YOKAI_INFINITE_TUNNEL);
}
// Keep patrols spread through open ground near the camera. Distant patrols
// are recycled only when off screen; occupied cells, warps and chokepoints are excluded.
static void MaintainPatrols(bool8 initial)
{
    const struct ThMap *map=&sThMaps[sTh.map];
    s16 px,py,x,y,bx,by,score,best,distance,nearest;
    u8 i,j,id,near=0,neighbors,co;
    if(!map->pursuers || sTh.freeRoam)return;
    PlayerGetDestCoords(&px,&py);px-=7;py-=7;co=Component(map,px,py);
    for(i=0;i<TH_PATROLS;i++)if((id=Object(PatrolLocal(i)))<OBJECT_EVENTS_COUNT)
        if(abs(gObjectEvents[id].currentCoords.x-7-px)<=7 && abs(gObjectEvents[id].currentCoords.y-7-py)<=5)near++;
    for(i=0;i<TH_PATROLS;i++) {
        id=Object(PatrolLocal(i));
        if(id<OBJECT_EVENTS_COUNT) {
            if(initial || near>=2 || (abs(gObjectEvents[id].currentCoords.x-7-px)<=9 && abs(gObjectEvents[id].currentCoords.y-7-py)<=7))continue;
        } else if(!initial && near>=2)continue;
        bx=-1;by=-1;best=-32767;
        for(y=py-5;y<=py+5;y++)for(x=px-7;x<=px+7;x++) {
            distance=abs(x-px)+abs(y-py);
            if(distance<4 || Component(map,x,y)!=co || !IsFree(x,y))continue;
            // During exploration, new patrols enter at the camera edge.
            if(!initial && abs(x-px)<7 && abs(y-py)<5)continue;
            for(j=0;j<gMapHeader.events->warpCount;j++)if(gMapHeader.events->warps[j].x==x && gMapHeader.events->warps[j].y==y)break;
            if(j<gMapHeader.events->warpCount)continue;
            neighbors=0;
            for(j=1;j<=4;j++)if(!MapGridGetCollisionAt(x+7+gDirectionToVectors[j].x,y+7+gDirectionToVectors[j].y))neighbors++;
            if(neighbors<3)continue;
            nearest=20;
            for(j=0;j<TH_PATROLS;j++) {
                u8 other=Object(PatrolLocal(j));
                if(other<OBJECT_EVENTS_COUNT && other!=id) {
                    s16 d=abs(gObjectEvents[other].currentCoords.x-7-x)+abs(gObjectEvents[other].currentCoords.y-7-y);
                    if(d<nearest)nearest=d;
                }
            }
            if(nearest<3)continue;
            score=nearest*4-distance;
            if(score>best){best=score;bx=x;by=y;}
        }
        if(bx<0)continue;
        if(id<OBJECT_EVENTS_COUNT)RemoveObjectEventByLocalIdAndMap(PatrolLocal(i),gSaveBlock1Ptr->location.mapNum,gSaveBlock1Ptr->location.mapGroup);
        id=SpawnSpecialObjectEventParameterized(OBJ_EVENT_GFX_PATROUILLE_ONI,MOVEMENT_TYPE_FACE_DOWN,PatrolLocal(i),bx+7,by+7,MapGridGetElevationAt(bx+7,by+7));
        if(id<OBJECT_EVENTS_COUNT)near++;
    }
}
static bool8 ChooseDoor(s16 mapId,s16 x,s16 y)
{
    u16 *distance=Alloc(512);u8 changed,i,j,co;u16 total=0,pick;
    if(!distance)return FALSE;
    memset(distance,255,512);co=Component(&sThMaps[mapId],x,y);
    if(!co){Free(distance);return FALSE;}distance[co]=sThDiameters[co];
    do {
        changed=0;
        for(i=0;i<ARRAY_COUNT(sThEdges);i++) {
            u8 a=sThEdges[i][0],b=sThEdges[i][1];
            if(distance[a]<=450 && distance[b]>distance[a]+sThDiameters[b]+1){distance[b]=distance[a]+sThDiameters[b]+1;changed=1;}
            if(distance[b]<=450 && distance[a]>distance[b]+sThDiameters[a]+1){distance[a]=distance[b]+sThDiameters[a]+1;changed=1;}
        }
    }while(changed);
    for(i=0;i<ARRAY_COUNT(sThMaps);i++) if(sThMaps[i].cave==sThMaps[mapId].cave)
        for(j=0;j<sThMaps[i].count;j++) if(distance[sThMaps[i].points[j].component]<=450)total++;
    if(!total){Free(distance);return FALSE;}
    pick=Random()%total;
    for(i=0;i<ARRAY_COUNT(sThMaps);i++) if(sThMaps[i].cave==sThMaps[mapId].cave)
        for(j=0;j<sThMaps[i].count;j++) if(distance[sThMaps[i].points[j].component]<=450 && !pick--) {
            sTh.doorMap=i;sTh.doorPoint=j;Free(distance);return TRUE;
        }
    Free(distance);return FALSE;
}
u8 TerreHeureEncounterChance(void)
{
    u8 i,chance=FlagGet(FLAG_SYS_GAME_CLEAR)?10:5;
    for(i=0;i<PARTY_SIZE;i++)
        if(GetMonData(&gPlayerParty[i],MON_DATA_SPECIES)
            && GetMonData(&gPlayerParty[i],MON_DATA_HELD_ITEM)==ITEM_SHORT_ONI) {
            chance*=3;break;
        }
    return chance;
}
static bool8 QuestBlocksTerreHeure(s16 mapId)
{
    u8 i;
    if(sThMaps[mapId].cave!=5)return FALSE;
    // The dedicated Nyada quest is reserved in this branch. Its active flag
    // protects the whole cave; visible Nyada actors also protect their map.
    if(FlagGet(FLAG_NYADA_QUEST_UNLOCKED))return TRUE;
    for(i=0;i<gMapHeader.events->objectEventCount;i++) {
        const struct ObjectEventTemplate *t=&gMapHeader.events->objectEvents[i];
        if(t->graphicsId==OBJ_EVENT_GFX_YOKAI_NYADA && (!t->flagId || !FlagGet(t->flagId)))return TRUE;
    }
    return FALSE;
}
void TerreHeureInputStep(bool8 tookStep)
{
    s16 mapId;u16 visit,pending,roll;bool8 rolledNow=FALSE;
    if(sTh.active || gQuestLogState==QL_STATE_PLAYBACK || gQuestLogState==QL_STATE_PLAYBACK_LAST)return;
    mapId=CurrentMap();
    if(mapId<0) {
        VarSet(VAR_TERRE_HEURE_VISIT,0);VarSet(VAR_TERRE_HEURE_PENDING,0);
        VarSet(VAR_TERRE_HEURE_TRAINER_GUARD,0);return;
    }
    visit=VarGet(VAR_TERRE_HEURE_VISIT);
    if((visit&255)!=sThMaps[mapId].cave) {
        visit=sThMaps[mapId].cave;VarSet(VAR_TERRE_HEURE_VISIT,visit);
        VarSet(VAR_TERRE_HEURE_PENDING,0);VarSet(VAR_TERRE_HEURE_TRAINER_GUARD,0);
    }
    if(QuestBlocksTerreHeure(mapId))return;
    if(!(visit&0x100) && sThMaps[mapId].pursuers) {
        VarSet(VAR_TERRE_HEURE_VISIT,visit|0x100);rolledNow=TRUE;
        do {roll=Random();}while(roll>=65500);
        // Route Victoire guarantees a first encounter late in the adventure.
        // Earlier caves use the normal rates, even before the first encounter.
        if((!FlagGet(FLAG_ONI_FIRST_SEEN) && sThMaps[mapId].cave==4)
            || roll%100<TerreHeureEncounterChance()) {
            do {roll=Random();}while(roll>=65461); // 121 * 541
            VarSet(VAR_TERRE_HEURE_PENDING,30+roll%121);
        }
    }
    pending=VarGet(VAR_TERRE_HEURE_PENDING);
    if(tookStep && !rolledNow && pending && pending<0x100) {
        pending--;VarSet(VAR_TERRE_HEURE_PENDING,pending?pending:0x100);
    }
}
bool8 TerreHeureTrainerSightAllowed(void)
{
    u16 guard=VarGet(VAR_TERRE_HEURE_TRAINER_GUARD);s16 x,y,mapId;
    // Native sight checks use destination coordinates before the walking
    // animation has completed. Let the final scheduled step finish first.
    if(VarGet(VAR_TERRE_HEURE_PENDING)==1 && gPlayerAvatar.runningState==MOVING
        && gPlayerAvatar.tileTransitionState!=T_TILE_CENTER) {
        mapId=CurrentMap();
        if(mapId>=0 && sThMaps[mapId].pursuers && !QuestBlocksTerreHeure(mapId))return FALSE;
    }
    if(!guard)return TRUE;
    PlayerGetDestCoords(&x,&y);x-=7;y-=7;guard--;
    if(x==(guard>>8) && y==(guard&255))return FALSE;
    VarSet(VAR_TERRE_HEURE_TRAINER_GUARD,0);return TRUE;
}
bool8 TerreHeureTryStep(void)
{
    s16 mapId,x,y;u8 i,points=0,component;
    if(sTh.active || gQuestLogState==QL_STATE_PLAYBACK || gQuestLogState==QL_STATE_PLAYBACK_LAST)return FALSE;
    TerreHeureInputStep(FALSE);
    for(i=0;i<4;i++) {
        u16 count=VarGet(VAR_TERRE_HEURE_REWARD_FIRST+i);
        if(count && AddBagItem(sRewardItems[i],count)) {
            VarSet(VAR_TERRE_HEURE_REWARD_FIRST+i,0);ScriptContext_SetupScript(TerreHeure_EventScript_StoredRewards);return TRUE;
        }
    }
    if(VarGet(VAR_TERRE_HEURE_PENDING)!=0x100 || gMain.inBattle
        || ScriptContext_IsEnabled() || ArePlayerFieldControlsLocked() || gPaletteFade.active)return FALSE;
    mapId=CurrentMap();if(mapId<0 || !sThMaps[mapId].pursuers || QuestBlocksTerreHeure(mapId))return FALSE;
    PlayerGetDestCoords(&x,&y);
    // A scheduled event waits on stairs/exit tiles instead of interrupting a
    // map transition. Leaving the cave then cancels it through InputStep.
    for(i=0;i<gMapHeader.events->warpCount;i++)
        if(gMapHeader.events->warps[i].x==x-7 && gMapHeader.events->warps[i].y==y-7)return FALSE;
    component=Component(&sThMaps[mapId],x-7,y-7);
    for(i=0;i<sThMaps[mapId].count;i++)if(sThMaps[mapId].points[i].component==component)points++;
    if(points<5)return FALSE;
    PlayerGetDestCoords(&x,&y);
    if(!ChooseDoor(mapId,x-7,y-7))return FALSE;
    sTh.origin=gSaveBlock1Ptr->location;sTh.origin.warpId=-1;sTh.origin.x=x-7;sTh.origin.y=y-7;
    sTh.flash=gSaveBlock1Ptr->flashLevel;sTh.cave=sThMaps[mapId].cave;
    sTh.tier=FlagGet(FLAG_ONI_OGRALOS_WON)?2:FlagGet(FLAG_ONI_GARGAROS_WON)?1:0;
    sTh.helpWasEnabled=gHelpSystemEnabled;
    sTh.active=TRUE;sTh.phase=0;sTh.freeRoam=FALSE;sTh.map=mapId;sTh.window=TH_NONE;
    sTh.remaining=(TH_SECONDS*262144U+4388)/4389U;sTh.seconds=TH_NONE;
    memset(sTh.picked,0,sizeof(sTh.picked));memset(sTh.loot,0,sizeof(sTh.loot));
    VarSet(VAR_TERRE_HEURE_PENDING,0);
    FlagSet(FLAG_ONI_FIRST_SEEN);
    ScriptContext_SetupScript(TerreHeure_EventScript_Intro);
    return TRUE;
}
bool8 TerreHeureBlockWarp(u8 group,u8 num)
{
    u8 i;if(!sTh.active)return FALSE;
    for(i=0;i<ARRAY_COUNT(sThMaps);i++) if(sThMaps[i].group==group && sThMaps[i].num==num && sThMaps[i].cave==sTh.cave)return FALSE;
    ScriptContext_SetupScript(TerreHeure_EventScript_Blocked);return TRUE;
}
void TerreHeureReload(void)
{
    TerreHeureFogClear();
    if(sTh.active){sTh.window=TH_NONE;sTh.seconds=TH_NONE;gSaveBlock1Ptr->flashLevel=0;}
}
void TerreHeureBegin(void)
{
    HelpSystem_Disable();
    gSaveBlock1Ptr->flashLevel=0;ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_WINOUT,WINOUT_WIN01_BG_ALL|WINOUT_WIN01_OBJ|WINOUT_WINOBJ_BG_ALL|WINOUT_WINOBJ_OBJ);
    sTh.phase=1;sTh.clock=gMain.vblankCounter2;
}
void TerreHeureRun(void)
{
    sTh.phase=2;sTh.clock=gMain.vblankCounter2;
}
static void Timer(void)
{
    // BG0 character base is 0x8000: 0x380 overlapped the terrain map at 0xF000.
    // Reserve 12 tiles at 0xD000, below all three terrain tilemaps.
    static const struct WindowTemplate win={.bg=0,.tilemapLeft=24,.tilemapTop=0,.width=6,.height=2,.paletteNum=14,.baseBlock=0x280};
    u8 str[8],colors[3]={0,1,2},stamp;u16 seconds=(sTh.remaining*4389U+262143U)>>18;
    if(sTh.freeRoam)return;
    if(ArePlayerFieldControlsLocked()){sTh.seconds=TH_NONE;return;}
    if(sTh.window==TH_NONE){sTh.window=AddWindow(&win);sTh.seconds=TH_NONE;if(sTh.window==TH_NONE)return;}
    if(seconds>TH_SECONDS)seconds=TH_SECONDS;
    stamp=seconds%254;
    if(stamp==sTh.seconds)return;sTh.seconds=stamp;
    str[0]=CHAR_0+seconds/60;str[1]=CHAR_COLON;str[2]=CHAR_0+(seconds%60)/10;str[3]=CHAR_0+seconds%10;str[4]=EOS;
    if(seconds<30)colors[1]=3;else if(seconds<=60)colors[1]=4;
    LoadPalette(sTimerColors,14*16,32);
    FillWindowPixelBuffer(sTh.window,0);
    AddTextPrinterParameterized3(sTh.window,0,4,0,colors,0xff,str);
    PutWindowTilemap(sTh.window);CopyWindowToVram(sTh.window,COPYWIN_FULL);
}
static bool8 Sight(struct ObjectEvent *o,s16 x,s16 y,u8 range)
{
    s16 dx=x-o->currentCoords.x,dy=y-o->currentCoords.y,i;
    if(abs(dx)+abs(dy)>range)return FALSE;
    if(Component(&sThMaps[sTh.map],x-7,y-7)!=Component(&sThMaps[sTh.map],o->currentCoords.x-7,o->currentCoords.y-7))return FALSE;
    if((o->facingDirection==DIR_NORTH && dx==0 && dy<0)||(o->facingDirection==DIR_SOUTH && dx==0 && dy>0)||(o->facingDirection==DIR_WEST && dy==0 && dx<0)||(o->facingDirection==DIR_EAST && dy==0 && dx>0)) {
        for(i=1;i<abs(dx)+abs(dy);i++) if(MapGridGetCollisionAt(o->currentCoords.x+(dx?i*(dx>0?1:-1):0),o->currentCoords.y+(dy?i*(dy>0?1:-1):0)))return FALSE;
        return TRUE;
    }return FALSE;
}
static u8 PathDirection(struct ObjectEvent *oni,s16 x,s16 y)
{
    const struct ThMap *map=&sThMaps[sTh.map];
    u16 count=map->width*map->height,head=0,tail=0,a,b,target;
    u16 *queue=Alloc(count*2);u8 *first=AllocZeroed(count);u8 dir,result=0,i,cx,cy,component;
    s16 nx,ny,sx=oni->currentCoords.x-7,sy=oni->currentCoords.y-7;
    if(!queue || !first){if(queue)Free(queue);if(first)Free(first);return 0;}
    target=(y-7)*map->width+x-7;component=Component(map,sx,sy);
    // Snapshot dynamic blockers once; the static ROM mask already excludes
    // water, ledges, walls and original boulders. No collision-engine call or
    // integer division in the inner search loop.
    for(i=0;i<OBJECT_EVENTS_COUNT;i++)if(gObjectEvents[i].active && &gObjectEvents[i]!=oni && i!=gPlayerAvatar.objectEventId) {
        s16 ox=gObjectEvents[i].currentCoords.x-7,oy=gObjectEvents[i].currentCoords.y-7;
        if(ox>=0 && oy>=0 && ox<map->width && oy<map->height)first[oy*map->width+ox]=255;
    }
    queue[tail++]=sx|(sy<<8);first[sy*map->width+sx]=255;
    while(head<tail) {
        a=queue[head++];cx=a&255;cy=a>>8;
        for(dir=1;dir<=4;dir++) {
            nx=cx+gDirectionToVectors[dir].x;ny=cy+gDirectionToVectors[dir].y;
            if(Component(map,nx,ny)!=component || !component)continue;b=ny*map->width+nx;if(first[b])continue;
            first[b]=(cx==sx && cy==sy)?dir:first[cy*map->width+cx];
            if(b==target){result=first[b];goto done;}queue[tail++]=nx|(ny<<8);
        }
    }
done: Free(queue);Free(first);return result;
}
static void Pursuers(void)
{
    s16 x,y;u8 i,id,dir=0;struct ObjectEvent *o;
    if(sTh.freeRoam)return;
    PlayerGetDestCoords(&x,&y);
    if(++sTh.patrolClock>=60) {
        sTh.patrolClock=0;
        MaintainPatrols(FALSE);
        for(i=0;i<TH_PATROLS;i++)if((id=Object(PatrolLocal(i)))<OBJECT_EVENTS_COUNT) {
            o=&gObjectEvents[id];ObjectEventClearHeldMovementIfActive(o);
            ObjectEventSetHeldMovement(o,GetFaceDirectionMovementAction(1+Random()%4));
        }
    }
    for(i=0;i<TH_PATROLS;i++)if((id=Object(PatrolLocal(i)))<OBJECT_EVENTS_COUNT && Sight(&gObjectEvents[id],x,y,5) && !sTh.alerted) {
        sTh.alerted=TRUE;gFieldEffectArguments[0]=PatrolLocal(i);gFieldEffectArguments[1]=gSaveBlock1Ptr->location.mapNum;gFieldEffectArguments[2]=gSaveBlock1Ptr->location.mapGroup;
        FieldEffectStart(FLDEFF_EXCLAMATION_MARK_ICON);PlaySE(SE_PIN);
    }
    id=Object(TH_LOCAL);if(id>=OBJECT_EVENTS_COUNT)return;o=&gObjectEvents[id];
    if(Sight(o,x,y,sTh.tier==2?8:6))sTh.seen=TRUE;
    if(abs(x-o->currentCoords.x)+abs(y-o->currentCoords.y)<=1) {
        ScriptContext_SetupScript(TerreHeure_EventScript_Oni);LockPlayerFieldControls();return;
    }
    if(ObjectEventIsMovementOverridden(o) && !ObjectEventCheckHeldMovementStatus(o))return;
    if(++sTh.aiDelay<(sTh.tier?8:16))return;sTh.aiDelay=0;
    ObjectEventClearHeldMovementIfActive(o);
    if(sTh.alerted || sTh.seen)dir=PathDirection(o,x,y);
    else {
        dir=1+Random()%4;
        if(sTh.tier==2) {
            // Orqanos checks junctions instead of spending a search turn on a wall.
            static const u8 opposite[]={0,2,1,4,3};
            for(i=0;i<4;i++,dir=dir%4+1)
                if(dir!=opposite[sTh.direction] && !GetCollisionAtCoords(o,o->currentCoords.x+gDirectionToVectors[dir].x,o->currentCoords.y+gDirectionToVectors[dir].y,dir))break;
            if(i==4)dir=opposite[sTh.direction];
        }
    }
    sTh.direction=dir;
    if(dir && !GetCollisionAtCoords(o,o->currentCoords.x+gDirectionToVectors[dir].x,o->currentCoords.y+gDirectionToVectors[dir].y,dir))
        ObjectEventSetHeldMovement(o,GetWalkSlowMovementAction(dir));
}
void TerreHeureUpdate(void)
{
    s16 mapId;u32 elapsed;u8 i;
    if(!sTh.active){if(sTh.phase==5)sTh.phase=0;return;}
    if(sTh.phase==1) {
        elapsed=gMain.vblankCounter2-sTh.clock;
        if(elapsed>=300) {Populate();sTh.phase=3;ScriptContext_Enable();}
        return;
    }
    if(sTh.phase!=2)return;
    mapId=CurrentMap();if(mapId<0)return;
    if(sTh.map!=mapId) {sTh.map=mapId;Populate();sTh.clock=gMain.vblankCounter2;}
    if(!sTh.freeRoam && !ScriptContext_IsEnabled() && !ArePlayerFieldControlsLocked() && !gPaletteFade.active) {
        if(!sTh.remaining) {Timer();sTh.phase=4;ScriptContext_SetupScript(TerreHeure_EventScript_Timeout);LockPlayerFieldControls();return;}
        Pursuers();
    }
    Timer();
}
// The GBA has one shared alpha coefficient. Dissolve only resident pixels so
// their disappearance can run alongside an independently growing cloud layer.
// Each resident owns its OBJ tiles; original graphics and the player are untouched.
void TerreHeureFadeResidents(void)
{
    static const u8 bayer[4][4]={{0,8,2,10},{12,4,14,6},{3,11,1,9},{15,7,13,5}};
    u16 masks[4],row,x,i,word;
    u8 amount;
    if(!sTh.active || sTh.phase!=1)return;
    amount=TerreHeureTransitionAmount();
    if(!amount)return;
    for(row=0;row<4;row++) {
        masks[row]=0;
        for(x=0;x<4;x++)if(bayer[row][x]>=amount)masks[row]|=0xF<<(x*4);
    }
    // Called after native animation uploads, once in the field VBlank.
    for(i=0;i<OBJECT_EVENTS_COUNT;i++) {
        struct ObjectEvent *object=&gObjectEvents[i];
        struct Sprite *sprite;
        vu16 *tiles;
        if(!object->active || i==gPlayerAvatar.objectEventId
            || object->graphicsId==OBJ_EVENT_GFX_PUSHABLE_BOULDER)continue;
        sprite=&gSprites[object->spriteId];
        if(!sprite->inUse || sprite->invisible || sprite->images==NULL)continue;
        tiles=(vu16 *)(OBJ_VRAM0+sprite->oam.tileNum*32);
        for(word=0;word<sprite->images[0].size/2;word++)tiles[word]&=masks[(word>>1)&3];
    }
}
void TerreHeurePalette(void)
{
    u16 i,c,r,g,b,v;u8 amount;
    if(!sTh.active || sTh.phase==0 || !IsFieldPaletteView())return;
    if(gPaletteFade.blendColor==RGB_WHITE && gPaletteFade.y==16)return;
    amount=TerreHeureTransitionAmount();
    // Only terrain banks 0..12; NPC, player, UI and effects remain colored.
    for(i=0;i<13*16;i++) {
        c=gPlttBufferFaded[i];r=c&31;g=(c>>5)&31;b=(c>>10)&31;v=(r*5+g*9+b*2)/16;
        // True neutral grayscale. Yellow is a separate moving cloud layer.
        ((vu16 *)PLTT)[i]=RGB((r*(16-amount)+v*amount)/16,(g*(16-amount)+v*amount)/16,(b*(16-amount)+v*amount)/16);
    }
}
void TerreHeureBattleResult(void)
{
    if(!sTh.active)return;
    sTh.phase=2;
    if(gBattleOutcome==B_OUTCOME_WON) {
        FlagSet(sTh.tier==0?FLAG_ONI_GARGAROS_WON:sTh.tier==1?FLAG_ONI_OGRALOS_WON:FLAG_ONI_ORQANOS_WON);
        sTh.freeRoam=TRUE;RemovePursuers();
        if(sTh.window!=TH_NONE){ClearStdWindowAndFrameToTransparent(sTh.window,TRUE);RemoveWindow(sTh.window);sTh.window=TH_NONE;}
        PlayNewMapMusic(MUS_YOKAI_INFINITE_TUNNEL);
    }
    gSpecialVar_Result=sTh.freeRoam;
}
void TerreHeureReward(void)
{
    u8 chest=gSpecialVar_LastTalked-(TH_LOCAL+4),bit,index=(sTh.map+chest)%4;
    if(chest>1 || WasPicked(chest)){gSpecialVar_Result=FALSE;return;}
    if(!CheckBagHasSpace(sRewardItems[index],sTh.loot[index]+1)){gSpecialVar_Result=FALSE;return;}
    bit=sTh.map*2+chest;sTh.picked[bit/8]|=1<<(bit%8);
    StringCopy(gStringVar1,ItemId_GetName(sRewardItems[index]));
    sTh.loot[index]++;RemoveObjectEventByLocalIdAndMap(gSpecialVar_LastTalked,gSaveBlock1Ptr->location.mapNum,gSaveBlock1Ptr->location.mapGroup);
    gSpecialVar_Result=TRUE;
}
void TerreHeureEnd(void)
{
    struct WarpData origin=sTh.origin;u8 flash=sTh.flash,i;bool8 success=gSpecialVar_0x8004;
    if(!sTh.active)return;
    TerreHeureFogClear();
    if(success)for(i=0;i<4;i++)if(sTh.loot[i] && !AddBagItem(sRewardItems[i],sTh.loot[i]) && !AddPCItem(sRewardItems[i],sTh.loot[i]))
        VarSet(VAR_TERRE_HEURE_REWARD_FIRST+i,VarGet(VAR_TERRE_HEURE_REWARD_FIRST+i)+sTh.loot[i]);
    if(sTh.helpWasEnabled)HelpSystem_Enable();
    sTh.active=FALSE;sTh.cooldown=0;sTh.steps=0;sTh.phase=5;
    VarSet(VAR_TERRE_HEURE_TRAINER_GUARD,1+((u16)origin.x<<8)+origin.y);
    SetWarpDestination(origin.mapGroup,origin.mapNum,-1,origin.x,origin.y);
    gSaveBlock1Ptr->flashLevel=flash;
    gSpecialVar_0x8005=flash;
    DoWarp();
    gFieldCallback=FieldCB_ContinueScriptHandleMusic;
}

s16 TerreHeureFlashOverride(void) { if(sTh.active)return 0;if(sTh.phase==5)return sTh.flash;return -1; }
void TerreHeureTier(void) { gSpecialVar_Result=sTh.tier; }

bool8 TerreHeureHideOrdinary(void) { return sTh.active && sTh.phase >= 2; }

void TerreHeureClock(void)
{
    u32 elapsed;
    if(!sTh.active || sTh.phase!=2)return;
    elapsed=gMain.vblankCounter2-sTh.clock;sTh.clock=gMain.vblankCounter2;
    if(!gMain.inBattle && !sTh.freeRoam)HelpSystem_Disable();
    if(!sTh.freeRoam && !gMain.inBattle && !gPaletteFade.active
        && (!IsFieldPaletteView() || !ArePlayerFieldControlsLocked() || FuncIsActiveTask(Task_StartMenuHandleInput)))
        sTh.remaining=sTh.remaining>elapsed?sTh.remaining-elapsed:0;
}

// 300 VBlanks are slightly more than five seconds on real GBA hardware.
u8 TerreHeureTransitionAmount(void)
{
    u32 elapsed;
    if(!sTh.active || sTh.phase==0)return 0;
    if(sTh.phase!=1)return 16;
    elapsed=gMain.vblankCounter2-sTh.clock;
    return elapsed>=300?16:elapsed*16/300;
}
bool8 TerreHeureFogVisible(void) { return sTh.active && (sTh.phase==1 || sTh.phase==2 || sTh.phase==3 || sTh.phase==4) && IsFieldPaletteView() && !gMain.inBattle; }

void TerreHeureBattleStarting(void) { if(sTh.active) { sTh.phase=6; TerreHeureFogClear(); } }

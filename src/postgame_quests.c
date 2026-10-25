#include "global.h"
#include "postgame_quests.h"
#include "event_data.h"
#include "pokemon.h"
#include "pokedex.h"
#include "item.h"
#include "random.h"
#include "script.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/species.h"
#include "constants/maps.h"
#include "constants/pokemon.h"

static bool8 OnMap(u8 group,u8 number)
{
    return gSaveBlock1Ptr->location.mapGroup==group && gSaveBlock1Ptr->location.mapNum==number;
}
static void Visibility(u16 flag,bool8 show)
{
    if(show)FlagClear(flag);else FlagSet(flag);
}
void PostgameArmIntro(void)
{
    if(FlagGet(FLAG_SYS_GAME_CLEAR) && !FlagGet(FLAG_PG_ENMA_INTRO))FlagSet(FLAG_PG_ENMA_INTRO_PENDING);
}
void PostgameSync(void)
{
    bool8 clear=FlagGet(FLAG_SYS_GAME_CLEAR);
    bool8 active=clear && FlagGet(FLAG_NYADA_QUEST_UNLOCKED) && !FlagGet(FLAG_PG_NYADA_II_COMPLETE);
    if(clear && FlagGet(FLAG_PG_TICKET_GIVEN)
        && OnMap(MAP_GROUP(MAP_TRAINER_TOWER_ROOF),MAP_NUM(MAP_TRAINER_TOWER_ROOF))
        && gSaveBlock1Ptr->towerChallengeId<4
        && gSaveBlock1Ptr->trainerTower[gSaveBlock1Ptr->towerChallengeId].floorsCleared>=8)FlagSet(FLAG_PG_TOWER_CLEAR);
    Visibility(FLAG_PG_HIDE_ENMA_INTRO,FALSE);
    Visibility(FLAG_PG_HIDE_NYADA_HOME,clear && !active);
    Visibility(FLAG_PG_HIDE_NYADA_CAVE,active);
    Visibility(FLAG_PG_HIDE_DEMOPHAGE,active);
    Visibility(FLAG_PG_HIDE_SCIENTIST_LAV,clear && !FlagGet(FLAG_PG_SCIENTIST_1));
    Visibility(FLAG_PG_HIDE_SCIENTIST_PORT,clear && FlagGet(FLAG_PG_SCIENTIST_1) && !FlagGet(FLAG_PG_SCIENTIST_2));
    Visibility(FLAG_PG_HIDE_SCIENTIST_YOPPLE,clear && FlagGet(FLAG_PG_SCIENTIST_2) && !FlagGet(FLAG_PG_ROBO_GIVEN));
    Visibility(FLAG_PG_HIDE_NYADA_ROOF,clear && FlagGet(FLAG_PG_TOWER_CLEAR));
    if(OnMap(MAP_GROUP(MAP_SEVEN_ISLAND_HOUSE_ROOM1),MAP_NUM(MAP_SEVEN_ISLAND_HOUSE_ROOM1))
        && FlagGet(FLAG_PG_NYADA_I_COMPLETE) && FlagGet(FLAG_ONI_GORGOUILLE_CAUGHT))FlagSet(FLAG_PG_NYADA_II_LEAVE_OK);
    if(OnMap(MAP_GROUP(MAP_PALLET_TOWN),MAP_NUM(MAP_PALLET_TOWN)))
        VarSet(VAR_TEMP_3,clear && FlagGet(FLAG_PG_ENMA_INTRO_PENDING) && !FlagGet(FLAG_PG_ENMA_INTRO));
    if(OnMap(MAP_GROUP(MAP_SEAFOAM_ISLANDS_B4F),MAP_NUM(MAP_SEAFOAM_ISLANDS_B4F)))
        Visibility(FLAG_HIDE_ARTICUNO,clear && FlagGet(FLAG_PG_NYADA_I_ACTIVE) && !FlagGet(FLAG_PG_KYUBI_CAUGHT));
    if(OnMap(MAP_GROUP(MAP_POWER_PLANT),MAP_NUM(MAP_POWER_PLANT)))
        Visibility(FLAG_HIDE_ZAPDOS,clear && FlagGet(FLAG_PG_NYADA_I_ACTIVE) && !FlagGet(FLAG_PG_OCTORGONE_CAUGHT));
}
void PostgameHaveFriends(void)
{
    gSpecialVar_Result=GetSetPokedexFlag(SpeciesToNationalPokedexNum(SPECIES_PIDGEY),FLAG_GET_CAUGHT)
        && GetSetPokedexFlag(SpeciesToNationalPokedexNum(SPECIES_BEEDRILL),FLAG_GET_CAUGHT);
}
static u32 ShinyPersonality(u32 ot)
{
    u32 hi=Random();
    return (hi<<16)|((ot^(ot>>16)^hi)&0xFFFF);
}
void PostgameMakeScientistShiny(struct Pokemon *mon)
{
    u32 ot=GetMonData(mon,MON_DATA_OT_ID,NULL),pid=ShinyPersonality(ot);
    u16 species=GetMonData(mon,MON_DATA_SPECIES,NULL);
    u8 level=GetMonData(mon,MON_DATA_LEVEL,NULL),iv=GetMonData(mon,MON_DATA_HP_IV,NULL);
    CreateMon(mon,species,level,iv,TRUE,pid,OT_ID_PRESET,ot);
}
void PostgameGiveGift(void)
{
    static const u16 species[]={SPECIES_BULBASAUR,SPECIES_WIGGLYTUFF,SPECIES_DRAGONAIR,SPECIES_RATTATA};
    static const u8 levels[]={10,65,80,70};
    static const u16 flags[]={FLAG_PG_CHEN_JIBANYAN,FLAG_PG_DEMOPHAGE_GIVEN,FLAG_PG_NYADA_GIVEN,FLAG_PG_ROBO_GIVEN};
    struct Pokemon mon;
    u8 gift=gSpecialVar_0x8004,result;
    u16 number;
    gSpecialVar_Result=MON_CANT_GIVE;
    if(!FlagGet(FLAG_SYS_GAME_CLEAR) || gift>=ARRAY_COUNT(species) || FlagGet(flags[gift]))return;
    if(gift==1 && !FlagGet(FLAG_PG_DEMOPHAGE_WON))return;
    if(gift==2 && !FlagGet(FLAG_PG_NYADA_FINAL_WON))return;
    if(gift==3 && !FlagGet(FLAG_PG_SCIENTIST_WON))return;
    if(gift==3) {
        u32 ot=gSaveBlock2Ptr->playerTrainerId[0]|(gSaveBlock2Ptr->playerTrainerId[1]<<8)
            |(gSaveBlock2Ptr->playerTrainerId[2]<<16)|(gSaveBlock2Ptr->playerTrainerId[3]<<24);
        CreateMon(&mon,species[gift],levels[gift],USE_RANDOM_IVS,TRUE,ShinyPersonality(ot),OT_ID_PLAYER_ID,0);
    } else CreateMon(&mon,species[gift],levels[gift],USE_RANDOM_IVS,FALSE,0,OT_ID_PLAYER_ID,0);
    result=GiveMonToPlayer(&mon);
    if(result!=MON_CANT_GIVE) {
        FlagSet(flags[gift]);number=SpeciesToNationalPokedexNum(species[gift]);
        GetSetPokedexFlag(number,FLAG_SET_SEEN);GetSetPokedexFlag(number,FLAG_SET_CAUGHT);
    }
    gSpecialVar_Result=result;
}
void PostgameGiveTicket(void)
{
    gSpecialVar_Result=FALSE;
    if(!FlagGet(FLAG_SYS_GAME_CLEAR) || !FlagGet(FLAG_PG_DEMOPHAGE_GIVEN))return;
    if(CheckBagHasItem(ITEM_TOWER_TICKET,1) || AddBagItem(ITEM_TOWER_TICKET,1)) {
        FlagSet(FLAG_PG_TICKET_GIVEN);gSpecialVar_Result=TRUE;
    }
}

#!/usr/bin/env python3
"""Instantiate all reconstructed parties using the ROM's native trainer routine."""
import csv,hashlib,json,re,struct
from mgba_rpc import Emulator,ROOT
constants={}
for name in ['pokemon','items','moves','abilities','species','opponents']:
    constants.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*(?:$|//)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
teams=json.loads((ROOT/'data/yokai/equipes_appliquees.json').read_text())
# Independent chronology contract, not derived from the generator's stage dictionary.
for suffix,base,mid,final in [('SQUIRTLE',29,30,30),('BULBASAUR',5,6,7),('CHARMANDER',87,88,88)]:
    for stage,required in [('OAKS_LAB',[base]),('ROUTE22_EARLY',[9,base]),('CERULEAN',[9,1,base]),
                           ('SS_ANNE',[10,1,96,base]),('POKEMON_TOWER',[90,1,96,base]),
                           ('SILPH',[17,90,1,96,mid]),('ROUTE22_LATE',[18,90,1,96,mid])]:
        actual=[constants[x['species']] for x in teams['TRAINER_RIVAL_'+stage+'_'+suffix]['party']]
        assert actual==required,(stage,suffix,actual,required)
    actual=[constants[x['species']] for x in teams['TRAINER_CHAMPION_FIRST_'+suffix]['party']]
    assert actual==[19,90,4,89,97,final],(suffix,actual)

r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('NewGameInitData')
mons=0;summary={};locked=json.loads((ROOT/'data/yokai/equipes_boss_validees.json').read_text())
try:
    for trainer,team in teams.items():
        trainer_id=constants[trainer]
        r.w32(r.symbols['gBattleTypeFlags'],8)
        count=r.call('CreateNPCTrainerParty',r.symbols['gEnemyParty'],trainer_id)
        assert count==len(team['party']),(trainer,count)
        summary[team['mode']]=summary.get(team['mode'],0)+1
        for index,expected in enumerate(team['party']):
            mon=r.symbols['gEnemyParty']+100*index
            def get(field):return r.call('GetMonData',mon,constants[field],0)
            assert get('MON_DATA_SPECIES')==constants[expected['species']],(trainer,index,'species')
            assert get('MON_DATA_LEVEL')==expected['level'],(trainer,index,'level')
            assert get('MON_DATA_HELD_ITEM')==constants[expected['held_item']],(trainer,index,'item')
            assert get('MON_DATA_SANITY_IS_BAD_EGG')==0 and get('MON_DATA_HP')>0,(trainer,index,'invalid mon')
            assert [get('MON_DATA_MOVE'+str(i)) for i in range(1,5)]==[constants[x] for x in expected['moves']],(trainer,index,'moves')
            assert get('MON_DATA_ABILITY_NUM')==expected['ability_num'],(trainer,index,'ability slot')
            if trainer in locked:
                assert r.call('GetMonAbility',mon)==constants[expected['ability']],(trainer,index,'ability')
            mons+=1
        if team['items'] is not None:
            # struct Trainer ABI: 40 bytes, item bag at offset 0x10.
            items=struct.unpack('<4H',r.read(r.symbols['gTrainers']+40*trainer_id+16,8))
            assert list(items)==[constants[x] for x in team['items']]+[0]*(4-len(team['items'])),(trainer,'bag',items)
finally:r.close()
report={'engine':'mGBA libretro','scope':'Native party construction, not completion of these battles',
        'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),
        'trainer_parties_tested':len(teams),'pokemon_instances_tested':mons,'categories':summary,
        'species_levels_moves_abilities_held_items_and_bags_match':True,
        'rival_chronology_checked_in_data':True,'all_battles_played':False}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_EQUIPES_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

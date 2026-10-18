#!/usr/bin/env python3
"""Native-function fixtures in mGBA; explicitly not an adventure playthrough."""
import hashlib
import os
import json
import re
import struct
from pathlib import Path

from mgba_rpc import Emulator, ROOT

constants={}
for name in ['pokemon','items','moves']:
    constants.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
r=Emulator()
results=[]
mon=r.symbols['gPlayerParty']
scratch=r.PARAMS+128


def get(field):return r.call('GetMonData',mon,constants[field],0)


def set_value(field,value):
    r.w32(scratch,value)
    r.call('SetMonData',mon,constants[field],scratch)


def create(number,personality=0,level=30):
    r.call('CreateMon',mon,number,level,31,1,personality,1,0)
    assert get('MON_DATA_SPECIES')==number and get('MON_DATA_SANITY_IS_BAD_EGG')==0


try:
    r.call('SetSaveBlocksPointers')
    r.call('NewGameInitData')
    create(82)
    egg=constants['ITEM_LUCKY_EGG']
    for friendship,item,expected in [(219,egg,0),(220,0,0),(220,egg,83),(255,egg,83)]:
        set_value('MON_DATA_FRIENDSHIP',friendship)
        set_value('MON_DATA_HELD_ITEM',item)
        actual=r.call('GetEvolutionTargetSpecies',mon,0,0)
        assert actual==expected,(friendship,item,actual,expected)
        assert get('MON_DATA_HELD_ITEM')==item, 'Evolution consumed the Lucky Egg'
        results.append({'test':'Noko evolution','friendship':friendship,'held_item':item,'result':actual,'passed':True})
    shiny=json.loads((ROOT/'data/yokai/shiny_families.json').read_text())
    eligible={entry['number'] for family in shiny['families'] if family['shiny_allowed'] for entry in family['members']}
    for number in range(1,152):
        create(number)
        personality=get('MON_DATA_PERSONALITY')
        actual=r.call('IsMonShiny',mon)
        assert bool(actual)==(number in eligible),(number,actual)
        assert personality%25==0 and personality&255==0
        if number not in eligible:assert ((personality>>16)^(personality&65535))>=8
    # Upper-word boundary verifies no overflow changes nature/gender during rejection.
    # OT=0, PID=FFFFFFFF is shiny; nature and low bits must survive exclusion.
    create(82,0xFFFFFFFF)
    personality=get('MON_DATA_PERSONALITY')
    assert not r.call('IsMonShiny',mon)
    assert personality%25==0xFFFFFFFF%25 and personality&255==255
    results.append({'test':'151 species shiny eligibility / 67 PID exclusions','eligible':len(eligible),'excluded':151-len(eligible),'forced_pids_tested':152,'nature_gender_preserved':True,'passed':True})
    # All 151 initial movesets must agree with the curated tables actually linked.
    import csv
    moves=list(csv.DictReader((ROOT/'data/yokai/attaques_validees.csv').open(),delimiter=';'))
    for number in range(1,152):
        create(number)
        expected=[]
        for row in moves:
            if int(row['numero_yokai']) != number or row['apprentissage']=='EVOLUTION_PLUS_2' or int(row['niveau'])>30:
                continue
            move=constants[row['move_id']]
            if move not in expected:expected=(expected+[move])[-4:]
        actual=[get('MON_DATA_MOVE'+str(i)) for i in range(1,5)]
        assert actual==expected+[0]*(4-len(expected)),(number,actual,expected)
    results.append({'test':'151 native initial movesets vs curated attack tables','species':151,'passed':True})

    def learn(first):
        learned=[]
        for i in range(25):
            result=r.call('MonTryLearningNewMove',mon,first if i==0 else 0)
            if result==0:return learned
            learned.append(r.u32(r.symbols['gMoveToLearn']) & 0xFFFF)
        raise AssertionError('Learning sequence did not terminate')

    def set_level(level):
        set_value('MON_DATA_EXP',level**3)
        r.call('CalculateMonStats',mon)
        assert get('MON_DATA_LEVEL')==level

    for number,level,immediate,delayed in [(4,36,'METAL_CLAW','SLASH'),(14,50,'DRAGON_CLAW','DRILL_PECK'),(19,60,'LOCK_ON','ZAP_CANNON'),(44,50,'NIGHTMARE','SHADOW_PUNCH')]:
        create(number,level=level)
        for slot in range(4):r.call('SetMonMoveSlot',mon,0,slot)
        r.call('RecordYokaiEvolutionLevel',mon)
        assert constants['MOVE_'+immediate] in learn(2)
        set_level(level+1)
        assert constants['MOVE_'+delayed] not in learn(1)
        set_level(level+2)
        assert constants['MOVE_'+delayed] in learn(1)
        results.append({'test':'Evolution move and exactly +2 levels, including delayed evolution','species':number,'evolution_level':level,'passed':True})
    create(4,level=59)
    for slot in range(4):r.call('SetMonMoveSlot',mon,0,slot)
    r.call('RecordYokaiEvolutionLevel',mon)
    assert constants['MOVE_SLASH'] in learn(2)
    count=r.call('GetMoveRelearnerMoves',mon,scratch)
    reminder=list(struct.unpack('<'+'H'*count,r.read(scratch,count*2)))
    assert constants['MOVE_METEOR_MASH'] in reminder
    results.append({'test':'Very late Shogunyan: immediate Slash and recoverable Meteor Mash','passed':True})
    # Actual native Flash save/load functions, not an emulator save-state roundtrip.
    create(82)
    set_value('MON_DATA_HELD_ITEM',egg)
    set_value('MON_DATA_FRIENDSHIP',220)
    r.write(r.symbols['gPlayerPartyCount'],b'\x01')
    saved=r.call('TrySavingData',0,max_frames=1200)
    assert saved==1,('native save status',saved)
    set_value('MON_DATA_HELD_ITEM',0)
    set_value('MON_DATA_FRIENDSHIP',0)
    loaded=r.call('LoadGameSave',0,max_frames=1200)
    assert loaded==1,('native load status',loaded)
    r.call('LoadPlayerParty')
    assert get('MON_DATA_SPECIES')==82 and get('MON_DATA_HELD_ITEM')==egg and get('MON_DATA_FRIENDSHIP')==220
    assert r.call('GetEvolutionTargetSpecies',mon,0,0)==83
    results.append({'test':'Native Flash save/load restores party and Noko evolution requirements','save_status':saved,'load_status':loaded,'passed':True})
    create(19,level=60)
    r.call('RecordYokaiEvolutionLevel',mon)
    stamp=get('MON_DATA_ENCRYPT_SEPARATOR')
    assert stamp==0x593E,hex(stamp)
    assert r.call('TrySavingData',0,max_frames=1200)==1
    set_value('MON_DATA_ENCRYPT_SEPARATOR',0)
    assert r.call('LoadGameSave',0,max_frames=1200)==1
    r.call('LoadPlayerParty')
    assert get('MON_DATA_ENCRYPT_SEPARATOR')==stamp
    set_level(62)
    assert constants['MOVE_ZAP_CANNON'] in learn(1)
    results.append({'test':'Native Flash persistence of evolution +2 marker and subsequent Zap Cannon','passed':True})

finally:
    r.close()
report={'engine':'mGBA libretro','scope':'native-function fixtures with RAM trampoline; no full story/battle UI playthrough',
        'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'results':results,
        'full_adventure_tested':False,'all_attack_animations_tested':False,'exp_share_in_real_battle_tested':False}
path=Path(os.environ.get('YOKAI_ENGINE_TEST_REPORT',str(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TESTS_MGBA_MOTEUR.json')))
path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Native-function fixtures in mGBA; explicitly not an adventure playthrough."""
import hashlib
import json
import re
import struct
from pathlib import Path

from mgba_rpc import Emulator, ROOT

constants={}
for name in ['pokemon','items']:
    constants.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
r=Emulator()
results=[]
mon=r.symbols['gPlayerParty']
scratch=r.PARAMS+128


def get(field):return r.call('GetMonData',mon,constants[field],0)


def set_value(field,value):
    r.w32(scratch,value)
    r.call('SetMonData',mon,constants[field],scratch)


def create(number,personality=0):
    r.call('CreateMon',mon,number,30,31,1,personality,1,0)
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
finally:
    r.close()
report={'engine':'mGBA libretro','scope':'native-function fixtures with RAM trampoline; no full story/battle UI playthrough',
        'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'results':results,
        'full_adventure_tested':False,'all_attack_animations_tested':False,'exp_share_in_real_battle_tested':False}
path=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TESTS_MGBA_MOTEUR.json'
path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

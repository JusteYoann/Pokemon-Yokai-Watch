#!/usr/bin/env python3
"""Real mGBA battle: native fixture setup, then ordinary controller input only."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
C={k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)',(ROOT/'include/constants/pokemon.h').read_text(),re.M)}
r=Emulator()
proof=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves'
proof.mkdir(exist_ok=True)
try:
    r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
    party=r.symbols['gPlayerParty'];enemy=r.symbols['gEnemyParty'];scratch=r.PARAMS+128
    def get(slot,field):return r.call('GetMonData',party+100*slot,C[field],0)
    def put(slot,field,value):
        r.w32(scratch,value);r.call('SetMonData',party+100*slot,C[field],scratch)
    for slot,(species,level) in enumerate([(1,30),(5,10),(29,10),(87,10),(20,100)]):
        r.call('CreateMon',party+slot*100,species,level,31,1,100,0,0)
    put(2,'MON_DATA_HP',0);put(3,'MON_DATA_IS_EGG',1)
    r.write(r.symbols['gPlayerPartyCount'],b'\x05')
    r.call('CreateMon',enemy,9,2,0,1,100,1,1234)
    r.write(r.symbols['gEnemyPartyCount'],b'\x01')
    r.call('SetMonMoveSlot',party,33,0)
    old=[get(i,'MON_DATA_EXP') for i in range(5)]
    r.frame.save(proof/'terrain-avant-combat.png')
    r.call('StartScriptedWildBattle')
    returned=False
    for frame in range(7200):
        r.keys={8} if frame%16<4 else set();r.run()
        if frame in (400,700,1000):r.frame.save(proof/f'combat-exp-{frame}.png')
        if frame>600 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:
            returned=True;break
    assert returned,'Battle failed to return to overworld within 7200 frames'
    r.keys=set();r.run(30);r.frame.save(proof/'terrain-apres-combat.png')
    delta=[get(i,'MON_DATA_EXP')-old[i] for i in range(5)]
    assert delta==[60,30,0,0,0],delta
    result={'engine':'mGBA libretro','setup':'Native RAM fixtures, valid new-game options; actual battle controller input afterwards',
            'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),
            'battle_returned_to_map':returned,'frames_to_return':frame,'experience_delta':delta,
            'party_roles':['participant','living reserve','fainted reserve','egg','level 100 reserve'],
            'passed':True,'full_adventure_tested':False,'battle_animations_coverage':'One battle with Tackle; all-move coverage still pending'}
finally:r.close()
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_COMBAT_MGBA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))

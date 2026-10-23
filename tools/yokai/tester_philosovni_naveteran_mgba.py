#!/usr/bin/env python3
"""Play the preserved Oceane Naveteran encounter and actual Master Ball capture."""
import os,json,hashlib,traceback
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C,MAPS,warp,strong_party
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';P=ROOT/'docs/pierre-philosovni/validation'/mode;P.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;failure=None
try:
 strong_party(r);r.call('VarSet',0x40f4,3);r.call('AddBagItem',C['ITEM_MASTER_BALL'],1);warp(r,*MAPS['SSAnne_1F_Corridor'],8,8)
 r.call('ScriptContext_SetupScript',r.symbols['SSAnne_1F_Corridor_EventScript_Yokai096'])
 for f in range(12000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.u32(r.symbols['gBattleMainFunc'])==r.symbols['HandleTurnActionSelectionState']|1 and r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:r.keys=set();r.run(100);break
 else:raise AssertionError('Naveteran encounter not reached')
 assert r.call('GetMonData',r.symbols['gEnemyParty'],C['MON_DATA_SPECIES'],0)==96
 assert r.call('GetMonData',r.symbols['gEnemyParty'],C['MON_DATA_LEVEL'],0)==20
 assert not r.u32(r.symbols['gBattleTypeFlags'])&((1<<23)|8)
 r.frame.save(P/'naveteran-oceane.png');r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/'naveteran-oceane-x3.png')
 r.write(r.symbols['gBagMenuState']+6,b'\2\0')
 def pulse(key,n):r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(n)
 pulse(7,15);pulse(8,240);pulse(8,240)
 caught=False
 for f in range(12000):
  caught |= r.read(r.symbols['gBattleOutcome'],1)==b'\7'
  r.keys={0 if caught else 8} if f%16<4 else set();r.run()
  if f>100 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2':break
 else:raise AssertionError('Naveteran capture did not return to field')
 assert caught and r.read(r.symbols['gPlayerPartyCount'],1)==b'\2'
 assert r.call('GetMonData',r.symbols['gPlayerParty']+100,C['MON_DATA_SPECIES'],0)==96
 assert r.call('GetMonData',r.symbols['gPlayerParty']+100,C['MON_DATA_LEVEL'],0)==20
 r.keys=set();r.run(10);r.frame.save(P/'naveteran-capture.png');passed=True
 print('PASS native Naveteran level20, normal wild rules, actual Master Ball capture and field return',flush=True)
except BaseException:failure=traceback.format_exc();print(failure,flush=True)
finally:
 (P/'NAVETERAN_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),fixture='Completed quest, native corridor script entry, level100 QA Jibanyan and one Master Ball; no enemy/outcome changes.',failure=failure),ensure_ascii=False,indent=2)+'\n');r.close()
assert passed,failure

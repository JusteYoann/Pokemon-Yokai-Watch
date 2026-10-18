#!/usr/bin/env python3
"""Native controller capture with the substituted capture BGM and field return."""
import hashlib,json,subprocess
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/AUDIO_COMPLEMENT/capture';P.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;error='Interrupted';seen=False
action_handlers={int(v[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=line.split())==3 and v[2]=='HandleInputChooseAction'}
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,60,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.call('ClearBag');assert r.call('AddBagItem',1,1) # native Master Ball item, access fixture
 r.call('SetWarpDestination',3,0,255,8,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 field=r.u32(r.symbols['gMPlayInfo_BGM']);r.call('CreateMon',r.symbols['gEnemyParty'],9,8,31,1,101,0,0);r.write(r.symbols['gEnemyPartyCount'],b'\x01');r.call('StartWildBattle')
 for f in range(9000):
  r.keys={0} if f%16<2 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in action_handlers:break
 else:raise AssertionError('Action menu not reached')
 expected_species=r.call('GetMonData',r.symbols['gEnemyParty'],11,0)
 r.keys=set();r.run(16);r.write(r.symbols['gBagMenuState']+6,b'\x02\x00')
 r.keys={7};r.run();r.keys=set();r.run(16);assert r.read(r.symbols['gActionSelectionCursor'],1)==b'\x01'
 r.keys={8};r.run();r.keys=set();r.run(240)
 for _ in range(2):r.keys={8};r.run();r.keys=set();r.run(90)
 for f in range(15000):
  r.keys={0} if f%16<2 else set();r.run()
  if r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_22'] and not seen:seen=True;r.frame.save(P/'capture-theme-yokai.png')
  if r.read(r.symbols['gBattleOutcome'],1)==b'\x07' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Capture did not return to exploration')
 r.keys=set();r.run(180);assert seen,'Capture music was not observed';assert r.u32(r.symbols['gMPlayInfo_BGM'])==field
 assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\x02'
 actual_species=r.call('GetMonData',r.symbols['gPlayerParty']+100,11,0);assert actual_species==expected_species,('Captured species mismatch',expected_species,actual_species)
 r.frame.save(P/'retour-exploration.png');passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),capture_music_observed=seen,scope='Real new-game then warp/party/item/wild-species fixtures; native bag input and Master Ball capture, no forced capture outcome. Not an ordinary catch-probability or whole-story test.'),indent=2)+'\n')
print('PASS actual Master Ball capture, Yo-kai capture BGM, native party receipt and field music restoration')

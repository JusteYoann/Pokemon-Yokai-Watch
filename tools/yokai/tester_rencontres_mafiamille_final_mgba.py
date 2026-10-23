#!/usr/bin/env python3
"""Two actual NPC interactions and controller victories after final emblem integration.

Explicit visibility/warp/overpowered-player fixtures; not a campaign/balance test.
"""
import os,json,re,hashlib
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp,strong_party
from tester_cameos_boss_mgba import interact
from pilote_combat_mgba import battle_keys
P=ROOT/os.environ.get('YOKAI_MAFIA_MEET_DIR','QA_RECETTE_FINALE/MAFIAMILLE_KANTO/finalisation/rencontres-public');P.mkdir(parents=True,exist_ok=True)
r=new_game();strong_party(r);results=[];passed=False
try:
 for k in re.findall(r'^    \[(TRAINER_\w+)\] =',(ROOT/'src/data/trainers.h').read_text(),re.M):
  if k in C:r.call('SetTrainerFlag',C[k])
 base=r.snapshot()
 for name,script,key in [('CeladonCity_GameCorner','CeladonCity_GameCorner_EventScript_RocketGrunt','TRAINER_TEAM_ROCKET_GRUNT_7'),('RocketHideout_B4F','RocketHideout_B4F_EventScript_Giovanni','TRAINER_BOSS_GIOVANNI')]:
  r.restore(base);trainer=C[key];r.call('ClearTrainerFlag',trainer)
  data=json.loads((ROOT/'data/maps'/name/'map.json').read_text());target=next(o for o in data['object_events'] if o.get('script')==script)
  if target.get('flag') in C:r.call('FlagClear',C[target['flag']])
  warp(r,*MAPS[name],target['x'],target['y']+1);r.frame.save(P/(key+'-carte.png'));interact(r)
  started=False;first=0;captured=[]
  for f in range(40000):
   battle=r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
   r.keys=battle_keys(r,f) if battle else ({8} if f%16<4 else set());r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
    if not started:
     assert int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')==trainer;started=True;first=f
    if f-first in [45,160,360]:r.frame.save(P/(key+f'-combat-{f-first}.png'));captured.append(f-first)
   if started and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.call('HasTrainerBeenFought',trainer):
    r.keys=set();r.run(90);assert r.read(r.symbols['gBattleOutcome'],1)==b'\x01';r.frame.save(P/(key+'-victoire.png'));break
  else:raise AssertionError(('Unfinished encounter',key))
  results.append(dict(trainer=key,map=name,actual_NPC_interaction=True,native_controller_victory=True,captured_frames=captured,passed=True));print('PASS',key,flush=True)
 passed=True
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=results),indent=2)+'\n')

#!/usr/bin/env python3
"""Actual field interactions for Master Ball, casino switch and warehouse password gate."""
import hashlib,json,re
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp
from tester_cameos_boss_mgba import interact
P=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/recompenses';P.mkdir(parents=True,exist_ok=True)
r=new_game();results=[];passed=False;error='Interrupted'
def finish(stem):
 for f in range(5000):
  r.keys={8} if f%16<4 else set();r.run()
  if f>30 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02':
   r.keys=set();r.run(60);r.frame.save(P/(stem+'.png'));return
 raise AssertionError((stem,'unfinished field event'))
try:
 for k in re.findall(r'^    \[(TRAINER_\w+)\] =',(ROOT/'src/data/trainers.h').read_text(),re.M):
  if k in C:r.call('SetTrainerFlag',C[k])
 base=r.snapshot()
 r.call('FlagSet',C['FLAG_HIDE_SILPH_ROCKETS']);r.call('FlagSet',C['FLAG_SILPH_11F_DOOR']);r.call('VarSet',C['VAR_MAP_SCENE_SILPH_CO_11F'],1)
 warp(r,*MAPS['SilphCo_11F'],9,10);interact(r);finish('master-ball');assert r.call('CheckBagHasItem',C['ITEM_MASTER_BALL'],1) and r.call('FlagGet',C['FLAG_GOT_MASTER_BALL_FROM_SILPH'])
 interact(r);finish('master-ball-deja-recue');assert not r.call('CheckBagHasItem',C['ITEM_MASTER_BALL'],2)
 results.append(dict(event='President after liberated-Silph fixture; native unique Master Ball, second interaction no duplicate',passed=True))
 r.restore(base);r.call('FlagSet',C['FLAG_HIDE_GAME_CORNER_ROCKET']);data=json.loads((ROOT/'data/maps/CeladonCity_GameCorner/map.json').read_text());poster=next(o for o in data['bg_events'] if o.get('script')=='CeladonCity_GameCorner_EventScript_Poster')
 warp(r,*MAPS['CeladonCity_GameCorner'],poster['x'],poster['y']+1);interact(r);finish('casino-interrupteur');assert r.call('FlagGet',C['FLAG_OPENED_ROCKET_HIDEOUT'])
 results.append(dict(event='Original casino poster switch opens stairs after defeated-guard fixture',passed=True))
 r.restore(base);warp(r,*MAPS['FiveIsland_Meadow'],12,22);interact(r);finish('entrepot-un-mot-de-passe');assert not r.call('FlagGet',C['FLAG_UNLOCKED_ROCKET_WAREHOUSE'])
 r.call('FlagSet',C['FLAG_LEARNED_YES_NAH_CHANSEY']);interact(r);finish('entrepot-deux-mots-de-passe');assert r.call('FlagGet',C['FLAG_UNLOCKED_ROCKET_WAREHOUSE'])
 r.keys={4};r.run(16);r.keys=set();r.run(600);assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['FiveIsland_RocketWarehouse'];r.frame.save(P/'entrepot-entree.png')
 results.append(dict(event='Warehouse original gate: second password required, opens with flag, native entry into warehouse after unlocking',passed=True))
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,fixtures='Controller new game; explicit defeated-trainer/liberation/password flags and warps; no claim of traversal between locations.',results=results),indent=2)+'\n')

#!/usr/bin/env python3
"""Independent native Flash fixtures: pre-scene save, post-scene save, revisit and legacy migration."""
import json,hashlib,os
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp
from argenta_qa import drive
P=ROOT/os.environ.get('YOKAI_ARGENTA_SAVE_DIR','QA_RECETTE_FINALE/ARGENTA_MORLEONE/sauvegarde-public');P.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False
try:
 # Fresh instance, no emulator state restore anywhere in the Flash test.
 warp(r,*MAPS['PewterCity'],20,39)
 assert r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_PENDING']) and not r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_DONE'])
 assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('FlagClear',C['FLAG_ARGENTA_MORLEONE_PENDING']);r.call('FlagSet',C['FLAG_ARGENTA_MORLEONE_DONE'])
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 assert r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_PENDING']) and not r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_DONE'])
 r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 r.keys={4};r.run(60);r.keys=set();drive(r);r.frame.save(P/'scene-apres-rechargement.png')
 assert r.call('VarGet',C['VAR_MAP_SCENE_PEWTER_CITY'])==0
 assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('FlagClear',C['FLAG_ARGENTA_MORLEONE_DONE']);r.call('FlagSet',C['FLAG_ARGENTA_MORLEONE_PENDING'])
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 assert r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_DONE']) and not r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_PENDING'])
 warp(r,*MAPS['Route2'],8,1);r.keys={4};r.run(90);r.keys=set();r.run(300)
 assert r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02'
 assert r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_DONE'])
 assert not any(r.read(r.symbols['gObjectEvents']+i*36,1)[0]&1 and 8<=r.read(r.symbols['gObjectEvents']+i*36+8,1)[0]<=13 for i in range(16))
 r.frame.save(P/'retour-sans-repetition.png')
 rows.append(dict(test='Native Flash before scene -> reload -> complete -> save -> reload -> south revisit without repeat',passed=True))
 r.close();r=new_game();r.call('FlagSet',C['FLAG_WORLD_MAP_PEWTER_CITY']);r.call('VarSet',C['VAR_MAP_SCENE_PEWTER_CITY'],2)
 warp(r,*MAPS['PewterCity'],20,39);r.keys={4};r.run(90);r.keys=set();r.run(200)
 assert r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_DONE']) and r.call('VarGet',C['VAR_MAP_SCENE_PEWTER_CITY'])==2
 assert r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02'
 rows.append(dict(test='Legacy visited-town fixture skips new intro; gym/running-shoes var remains2',passed=True))
 passed=True
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),indent=2)+'\n')
print('SAVE PASS')

#!/usr/bin/env python3
"""Native Ariane Fame Checker identity/portrait; book explicitly unlocked as fixture."""
import os,json,hashlib
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
OUT=ROOT/'QA_RECETTE_FINALE/CARMIN_2026_10_22';r=new_game(1)
try:
 assert r.call('GetFameCheckerTrainerId',4)==416
 assert r.call('GetFameCheckerTrainerPic',4)==148
 r.call('FullyUnlockFameChecker');r.call('UseFameChecker',r.symbols['CB2_ReturnToField']|1);r.run(600)
 p=r.u32(r.symbols['gFameChecker_ListMenuTemplate']);count=int.from_bytes(r.read(r.symbols['gFameChecker_ListMenuTemplate']+12,2),'little')
 assert r.symbols['gTrainers']+40*416+4 in [r.u32(p+8*i) for i in range(count)]
 for _ in range(4):r.keys={5};r.run(2);r.keys=set();r.run(20)
 r.run(100);r.frame.save(OUT/'profil-ariane.png')
 report=dict(passed=True,rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),scope=__doc__,trainer=416,portrait=148,native_list_label_correct=True)
 (OUT/'TEST_PROFIL_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print('PROFILE PASS')
finally:r.close()

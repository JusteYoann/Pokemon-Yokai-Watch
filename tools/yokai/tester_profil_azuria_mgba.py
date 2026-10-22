#!/usr/bin/env python3
"""Native Fame Checker identity/portrait for both protagonist choices.

Book entries are unlocked explicitly for this interface fixture; not obtained
through the adventure. All old profiles retain the opposite hero's identity.
"""
import hashlib,json,os,struct
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game
OUT=ROOT/'QA_RECETTE_FINALE/AZURIA_REPRISE_2026_10_22';rows=[]
for gender,name,hero,trainer,pic in [(0,'nathan','Katie',415,136),(1,'katie','Nathan',21,135)]:
 r=new_game(gender)
 try:
  assert r.call('GetFameCheckerTrainerId',3)==trainer
  assert r.call('GetFameCheckerTrainerPic',3)==pic
  assert r.call('GetFameCheckerTrainerId',2)==414
  assert r.call('GetFameCheckerTrainerPic',2)==152
  r.call('FullyUnlockFameChecker');r.call('UseFameChecker',r.symbols['CB2_ReturnToField']|1);r.run(600)
  # Read the native list via its global template, not ambiguously named locals.
  items=r.u32(r.symbols['gFameChecker_ListMenuTemplate'])
  count=int.from_bytes(r.read(r.symbols['gFameChecker_ListMenuTemplate']+12,2),'little')
  labels=[r.u32(items+i*8) for i in range(count)]
  correct=r.symbols['gTrainers']+40*trainer+4
  wrong=r.symbols['gTrainers']+40*(21 if trainer==415 else 415)+4
  assert correct in labels and wrong not in labels
  for _ in range(3):
   r.keys={5};r.run(2);r.keys=set();r.run(20)
  r.run(120);r.frame.save(OUT/(name+'-profil.png'))
  rows.append(dict(player=name,opposite_hero=hero,native_trainer_id=trainer,native_portrait_id=pic,native_list_label_correct=True,wyatt_profile_unchanged=True,passed=True))
 finally:r.close()
(OUT/'TEST_PROFIL_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba')).read_bytes()).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n');print('PROFILE PASS',rows,flush=True)

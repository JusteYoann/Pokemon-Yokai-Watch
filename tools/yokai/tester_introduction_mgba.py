#!/usr/bin/env python3
"""Actual intro UI for both genders: custom player naming and mandatory Matt."""
import hashlib,json,re,os
from pathlib import Path
from mgba_rpc import Emulator,ROOT
OUT=Path(os.environ.get('YOKAI_INTRO_QA_DIR',ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION'))
P=OUT/'preuves';P.mkdir(parents=True,exist_ok=True)
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
results=[]
for gender,person in [(0,'nathan'),(1,'katie')]:
 r=Emulator();rev={v|1:k for k,v in r.symbols.items()};visited=set();naming_templates=set()
 def tasks():
  t={rev.get(r.u32(r.symbols['gTasks']+40*i),'?') for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01'};visited.update(t);return t
 def pulse(key,after=8):
  r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(after)
 def wait_task(task,limit=10000,press_a=True):
  for f in range(limit):
   r.keys={8} if press_a and f%16<4 else set();r.run()
   if task in tasks():r.keys=set();return
  raise AssertionError((person,'Task not reached',task,tasks()))
 try:
  r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('ResetTasks');r.call('SetMainCallback1',0);r.call('StartNewGameScene')
  wait_task('Task_OakSpeech_HandleGenderInput')
  if gender:pulse(5,4)
  pulse(8,0);wait_task('Task_OakSpeech_YourNameWhatIsIt',press_a=False);r.run(60)
  r.frame.save(P/(person+'-introduction.png'))
  assert r.read(r.u32(r.symbols['gSaveBlock2Ptr'])+8,1)==bytes([gender])
  for f in range(5000):
   r.keys={8} if f%16<4 else set();r.run();tasks()
   if 'Naming' in rev.get(r.u32(r.symbols['gMain']+4),''):break
  else:raise AssertionError('Player naming not reached')
  r.keys=set();r.run(180);r.frame.save(P/(person+'-saisie-prenom.png'))
  naming_templates.add(r.read(r.u32(r.symbols['sNamingScreen'])+0x1E2C,1)[0])
  # Real keyboard starts at A: type two As, START moves to OK, A accepts.
  pulse(8,15);pulse(8,15);pulse(3,15);pulse(8,20)
  wait_task('Task_OakSpeech_HandleConfirmNameInput');r.keys=set();r.run(180)
  raw=r.read(r.u32(r.symbols['gSaveBlock2Ptr']),8)
  assert raw.startswith(bytes([glyphs['A'],glyphs['A'],255])),(person,raw.hex())
  r.frame.save(P/(person+'-confirmation-prenom.png'));pulse(8,0)
  saw_matt=False
  for f in range(10000):
   r.keys={8} if f%16<4 else set();r.run();t=tasks()
   cb=rev.get(r.u32(r.symbols['gMain']+4),'?')
   if 'Naming' in cb:
    naming_templates.add(r.read(r.u32(r.symbols['sNamingScreen'])+0x1E2C,1)[0])
   if 'Task_OakSpeech_FadeOutRivalPic' in t and not saw_matt:
    r.keys=set();r.run(180);r.frame.save(P/(person+'-introduction-matt.png'));saw_matt=True
   if cb=='CB2_Overworld':break
  else:raise AssertionError((person,'Intro did not reach actual new-game map',cb,tasks()))
  r.keys=set();r.run(180);r.frame.save(P/(person+'-debut-aventure.png'))
  assert saw_matt
  assert naming_templates=={0},naming_templates
  assert 'Task_OakSpeech_MoveRivalDisplayNameOptions' not in visited
  assert r.read(r.u32(r.symbols['gSaveBlock2Ptr']),3)==bytes([glyphs['A'],glyphs['A'],255])
  assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x3A4C,5)==bytes(glyphs[c] for c in 'Matt')+b'\xff'
  results.append({'person':person,'passed':True,'gender_selected_via_buttons':gender,'custom_player_name_typed':'AA','naming_templates':sorted(naming_templates),'rival_renaming_not_shown':True,'actual_overworld_reached':True})
 finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba')).read_bytes()).hexdigest(),'scope':'Native StartNewGameScene then only controller input for introduction and player naming, both genders; no gameplay progression beyond the initial room','results':results}
(OUT/'TEST_INTRODUCTION_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

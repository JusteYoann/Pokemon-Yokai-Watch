#!/usr/bin/env python3
"""Private beta: intro, native battery save and Continue in a fresh emulator."""
import ctypes as C
import hashlib,json,re,os
from pathlib import Path
from mgba_rpc import Emulator,ROOT
ROM=Path(os.environ['YOKAI_QA_ROM'])
P=ROOT/'QA_RECETTE_FINALE/BETA_13_OST/preuves'
P.mkdir(parents=True,exist_ok=True)
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
results=[]
for gender,person in [(0,'nathan'),(1,'katie')]:
 r=Emulator();r.frame.save(P/(person+'-demarrage.png'));rev={v|1:k for k,v in r.symbols.items()};visited=set();naming_templates=set()
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
  # Real startup/title/New Game, driven by the same A-button input below.
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
  # Use the normal Save menu, export battery RAM, destroy the emulator and
  # reload the battery file in a fresh core. No emulator savestate is used.
  pulse(3,90)
  order=list(r.read(r.symbols['sStartMenuOrder'],r.read(r.symbols['sNumStartMenuItems'],1)[0]))
  assert 4 in order,order
  target=order.index(4)
  for _ in range(len(order)):
   if r.read(r.symbols['sStartMenuCursorPos'],1)[0]==target:break
   pulse(5,12)
  pulse(8,30)
  success=False
  for f in range(5000):
   r.keys={8} if f%24<2 else set();r.run()
   if r.u32(r.symbols['sSaveDialogCB'])==r.symbols['SaveDialogCB_ReturnSuccess']|1:
    success=True;break
  assert success,'Save-menu success callback not reached'
  r.frame.save(P/(person+'-sauvegarde-confirmee.png'))
  r.keys=set();r.run(180)
  r.frame.save(P/(person+'-sauvegarde-menu.png'))
  r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
  r.lib.retro_get_memory_size.argtypes=[C.c_uint];r.lib.retro_get_memory_size.restype=C.c_size_t
  size=r.lib.retro_get_memory_size(0);pointer=r.lib.retro_get_memory_data(0)
  assert pointer and size==131072,(pointer,size)
  battery=C.string_at(pointer,size)
  private_dir=ROM.parent/'beta-test-saves';private_dir.mkdir(exist_ok=True)
  battery_file=private_dir/(person+'.sav');battery_file.write_bytes(battery)
  saved_map=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)
  r.close();r=None
  r=Emulator()
  r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
  C.memmove(r.lib.retro_get_memory_data(0),battery_file.read_bytes(),size)
  r.lib.retro_reset();r.keys=set();r.run(1200)
  for f in range(8000):
   r.keys={3} if f%120<2 else {8} if f%120 in [60,61] else set();r.run()
   if f>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gQuestLogState'],1)[0] not in [2,3]:break
  else:raise AssertionError('Fresh emulator Continue did not reach exploration')
  r.keys=set();r.run(180)
  assert r.read(r.u32(r.symbols['gSaveBlock2Ptr']),3)==bytes([glyphs['A'],glyphs['A'],255])
  assert r.read(r.u32(r.symbols['gSaveBlock2Ptr'])+8,1)==bytes([gender])
  assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)==saved_map
  r.frame.save(P/(person+'-sauvegarde-rechargee.png'))
  assert (P/(person+'-debut-aventure.png')).read_bytes()==(P/(person+'-sauvegarde-rechargee.png')).read_bytes(), 'Rendering differs after Continue'
  results.append({'person':person,'passed':True,'gender_selected_via_buttons':gender,'custom_player_name_typed':'AA','naming_templates':sorted(naming_templates),'rival_renaming_not_shown':True,'actual_overworld_reached':True,'native_flash_save_created':True,'battery_file_bytes':size,'battery_sha256':hashlib.sha256(battery).hexdigest(),'fresh_emulator_continue':True,'name_gender_map_preserved':True})
 finally:
  if r:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest(),'scope':'Existing private ROM, actual startup/title/New Game/intro/custom name via controller for both genders; actual Start/Save menu confirmed by native success callback, 128 KiB battery exported to private .sav, new emulator instance, reset/title/Continue through controller; no save states, no full adventure','results':results}
(ROOT/'QA_RECETTE_FINALE/BETA_13_OST/TEST_BETA_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

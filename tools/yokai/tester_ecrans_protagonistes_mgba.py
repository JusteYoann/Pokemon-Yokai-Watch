#!/usr/bin/env python3
"""Native Surf, Trainer Card, Hall of Fame and credits fixtures; not story progression."""
import hashlib,json,re
from PIL import Image
from mgba_rpc import Emulator,ROOT
P=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves'
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
results=[]
def fixture(gender):
 r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Test')+b'\xff');r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
 r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 return r
def warp(r,group,num,x,y):
 r.call('SetWarpDestination',group,num,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1800):
  r.run()
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Map not loaded')
 r.run(120)
def contact(frames,name):
 out=Image.new('RGB',(960,320),(224,224,224))
 for i in range(8):out.paste(frames[round(i*(len(frames)-1)/7)],((i%4)*240,(i//4)*160))
 out.save(P/(name+'.png'))
for gender,person in [(0,'nathan'),(1,'katie')]:
 r=fixture(gender)
 try:
  warp(r,3,39,12,10)
  obj=r.symbols['gObjectEvents']+r.read(r.symbols['gPlayerAvatar']+5,1)[0]*36
  r.call('ObjectEventTurn',obj,1)
  assert r.call('IsPlayerFacingSurfableFishableWater'),(person,'not facing real water')
  r.w32(r.symbols['gFieldEffectArguments'],0);r.call('FldEff_UseSurf');movie=[]
  for f in range(1500):
   r.run()
   if f%4==0:movie.append(r.frame.copy())
   if f>60 and f%16==0 and r.call('FindTaskIdByFunc',r.symbols['Task_FldEffUseSurf']|1)==255:break
  else:raise AssertionError('Surf transition did not complete')
  assert r.read(r.symbols['gPlayerAvatar'],1)[0]&8
  contact(movie,person+'-entree-surf');r.frame.save(P/(person+'-surf-sur-eau.png'))
  r.call('LockPlayerFieldControls');movie=[]
  for direction in [1,2,3,4]:
   r.call('ObjectEventTurn',obj,direction)
   for f in range(48):
    r.run()
    if f%4==0:movie.append(r.frame.copy())
  contact(movie,person+'-surf-quatre-directions');r.call('UnlockPlayerFieldControls')
  r.keys={4}
  for f in range(100):
   r.run()
   if not r.read(r.symbols['gPlayerAvatar'],1)[0]&8:break
  r.keys=set();r.run(90)
  assert not r.read(r.symbols['gPlayerAvatar'],1)[0]&8,(person,'could not leave water')
  r.frame.save(P/(person+'-sortie-surf.png'));results.append({'person':person,'test':'Native Surf field effect from Route21 North shore (12,10), real surf blob, four facings, UP input to return to land','passed':True,'HM_progression_checked':False})
  r.call('ShowPlayerTrainerCard',r.symbols['CB2_ReturnToField']|1);r.run(180);r.frame.save(P/(person+'-carte-dresseur.png'))
  r.keys={8};r.run(1);r.keys=set();r.run(120);r.frame.save(P/(person+'-carte-dresseur-verso.png'))
  r.keys={0};r.run(1);r.keys=set();r.run(180)
  results.append({'person':person,'test':'Native Trainer Card front and reverse captured','passed':True})
 finally:r.close()
 r=fixture(gender)
 try:
  r.call('SetMainCallback2',r.symbols['CB2_DoHallOfFameScreen']|1)
  rev={v|1:k for k,v in r.symbols.items()};seen=False
  for f in range(6000):
   r.run()
   tasks={rev.get(r.u32(r.symbols['gTasks']+40*i),'?') for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01'}
   if 'Task_Hof_ExitOnKeyPressed' in tasks:
    r.run(60);r.frame.save(P/(person+'-pantheon.png'));seen=True;break
  assert seen,(person,'Hall of Fame player screen not reached')
  results.append({'person':person,'test':'Native Hall of Fame team then player portrait; fresh Flash save fixture, League not played','passed':True})
 finally:r.close()
 r=fixture(gender)
 try:
  r.call('DoCredits');movie=[];seen_scenes=set();last=None;rival_frames=[]
  for f in range(48000):
   r.run()
   mgr=r.u32(r.symbols['sCreditsMgr'])
   if not mgr:break
   state=r.read(mgr,1)[0]
   if f%60==0 and f<1200:movie.append(r.frame.copy())
   if state!=last:last=state
   if state==6 and r.read(mgr+9,1)==b'\x09' and f%4==0:rival_frames.append(r.frame.copy())
   # Save complete scene transitions, including rival and The End.
   if state not in seen_scenes:
    seen_scenes.add(state)
    if f>60:r.frame.save(P/(person+'-credits-etat-'+str(state)+'.png'))
   if r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Credits']|1 and f>1200:break
  contact(movie,person+'-credits-debut')
  assert 17 in seen_scenes and 18 in seen_scenes,(person,'Credits did not reach The End / termination',seen_scenes)
  assert rival_frames,(person,'No rival credits scene captured')
  contact(rival_frames,person+'-credits-matt')
  results.append({'person':person,'test':'Native credits run from DoCredits with player gender fixture; state changes captured','passed':True,'frames_run':f+1,'states':sorted(seen_scenes),'main_callback_at_end':hex(r.u32(r.symbols['gMain']+4))})
 finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Direct entry to native scenes with valid party and gender fixtures; does not prove access to Surf, League or ending during actual adventure','results':results}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_ECRANS_PROTAGONISTES_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

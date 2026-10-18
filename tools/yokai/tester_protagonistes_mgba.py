#!/usr/bin/env python3
"""Native player-actor animation fixtures for both genders; not a full playthrough."""
import hashlib,json,re,subprocess,os
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
REPORT=ROOT/os.environ.get('YOKAI_PROTAGONISTS_REPORT_DIR','QA_RECETTE_FINALE/RECONSTRUCTION')
P=REPORT/'preuves';P.mkdir(parents=True,exist_ok=True)
C={}
for f in ['event_objects','opponents']:
 C.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*$',(ROOT/f'include/constants/{f}.h').read_text(),re.M)})
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
results=[]
def capture(r,name,frames,period=4):
 movie=[]
 for f in range(frames):
  r.run()
  if f%period==0:movie.append(r.frame.copy())
 return movie
def gif(images,name):
 assert len(images)>1
 images[0].save(P/(name+'.gif'),save_all=True,append_images=images[1:],duration=67,loop=0)
 # Opaque PNG contact sheet is independently viewable when GIF previews fail.
 contact=Image.new('RGB',(240*4,160*2),(224,224,224))
 for i in range(8):contact.paste(images[round(i*(len(images)-1)/7)].convert('RGB'),((i%4)*240,(i//4)*160))
 contact.save(P/(name+'.png'))
def warp(r,group,num,x,y):
 r.keys=set();r.call('SetWarpDestination',group,num,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1800):
  r.run()
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Field load did not complete')
 r.run(120)
for gender,person,prefix in [(g,n,p) for g,n,p in [(0,'nathan','RED'),(1,'katie','GREEN')] if n in os.environ.get('YOKAI_PROTAGONISTS','nathan,katie').split(',')]:
 r=new_game(gender)
 try:
  sav=r.u32(r.symbols['gSaveBlock2Ptr']);name=bytes(glyphs[c] for c in 'Test')+b'\xff'
  r.write(sav,name);r.write(sav+8,bytes([gender]))
  r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
  for t in range(317,322):r.call('SetTrainerFlag',t)
  r.call('VarSet',0x4081,1);warp(r,14,2,6,8)
  assert r.read(r.symbols['gPlayerAvatar']+7,1)==bytes([gender])
  def obj():return r.symbols['gObjectEvents']+r.read(r.symbols['gPlayerAvatar']+5,1)[0]*36
  def graphic():return r.read(obj()+5,1)[0]
  assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_NORMAL']
  r.frame.save(P/(person+'-joueur-carte.png'))
  r.call('LockPlayerFieldControls');walk=[];run=[]
  for repeat in range(3):
   for action in range(0x25,0x29):
    r.call('ObjectEventClearHeldMovementIfFinished',obj());r.call('ObjectEventSetHeldMovement',obj(),action)
    walk+=capture(r,person,32)
   for action in range(0x3D,0x41):
    r.call('ObjectEventClearHeldMovementIfFinished',obj());r.call('ObjectEventSetHeldMovement',obj(),action)
    run+=capture(r,person,32)
  gif(walk,person+'-marche-quatre-directions');gif(run,person+'-course-quatre-directions')
  r.call('ObjectEventClearHeldMovementIfFinished',obj())
  r.call('SetPlayerAvatarTransitionFlags',2);r.run(30)
  assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_BIKE'],(person,'bike',graphic())
  bike=[]
  for repeat in range(2):
   for action in range(0x25,0x29):
    r.call('ObjectEventClearHeldMovementIfFinished',obj());r.call('ObjectEventSetHeldMovement',obj(),action);bike+=capture(r,person,32)
  gif(bike,person+'-velo-quatre-directions')
  r.call('ObjectEventClearHeldMovementIfFinished',obj());r.call('StartPlayerAvatarVsSeekerAnim')
  assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_VS_SEEKER_BIKE']
  gif(capture(r,person,160),person+'-cherche-vs-velo')
  r.call('SetPlayerAvatarTransitionFlags',1);r.run(30)
  r.call('StartPlayerAvatarSummonMonForFieldMoveAnim')
  assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_FIELD_MOVE']
  gif(capture(r,person,80),person+'-action-montre')
  r.call('SetPlayerAvatarTransitionFlags',1);r.run(30);r.call('StartPlayerAvatarVsSeekerAnim')
  assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_VS_SEEKER']
  gif(capture(r,person,160),person+'-cherche-vs-a-pied')
  r.call('SetPlayerAvatarTransitionFlags',1);r.run(30);r.call('UnlockPlayerFieldControls')
  for direction,label in [(1,'sud'),(2,'nord'),(3,'ouest'),(4,'est')]:
   r.call('ObjectEventTurn',obj(),direction);r.call('StartFishing',0);movie=[];saw_fishing=False
   for f in range(1600):
    r.keys={0} if f>180 and f%16<4 else set();r.run()
    if f%4==0 and f<240:movie.append(r.frame.copy())
    if f%32==0:
     if graphic()==C['OBJ_EVENT_GFX_'+prefix+'_FISH']:saw_fishing=True
     if f>240 and saw_fishing and graphic()==C['OBJ_EVENT_GFX_'+prefix+'_NORMAL'] and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.call('FindTaskIdByFunc',r.symbols['Task_Fishing']|1)==255:break
   assert saw_fishing,(person,label,'no fishing graphics')
   if graphic()!=C['OBJ_EVENT_GFX_'+prefix+'_NORMAL']:
    r.frame.save(P/(person+'-erreur-peche-'+label+'.png'))
   assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_NORMAL'],(person,label,'fishing did not return')
   assert r.call('FindTaskIdByFunc',r.symbols['Task_Fishing']|1)==255,(person,label,'Fishing task still active')
   r.keys=set();r.run(90);gif(movie,person+'-peche-'+label)
  # Native surf graphics/poses in an isolated rendering fixture. This does not
  # claim HM access, shoreline collision or a real water-route traversal.
  r.call('SetPlayerAvatarTransitionFlags',8);r.run(30)
  assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_SURF'],(person,'surf',graphic())
  surf=[]
  for direction in [1,2,3,4]:
   r.call('ObjectEventTurn',obj(),direction);surf+=capture(r,person,40)
  gif(surf,person+'-surf-quatre-directions')
  r.call('SetPlayerAvatarTransitionFlags',1);r.run(30)
  assert graphic()==C['OBJ_EVENT_GFX_'+prefix+'_NORMAL']
  assert r.read(r.u32(r.symbols['gSaveBlock2Ptr']),len(name))==name
  results.append({'person':person,'test':'Native player actor, three four-direction walk/run cycles, bicycle cycles, field/watch and VS Seeker animations, actual fishing task in four directions and return to normal; native surf graphics/four facings/return in rendering fixture (not HM progression or water traversal)','custom_fixture_name_preserved':True,'passed':True})
  if os.environ.get('YOKAI_PROTAGONISTS_OW_ONLY'):continue
  r.w32(r.symbols['gTrainerBattleOpponent_A'],C['TRAINER_RIVAL_ROUTE22_EARLY_CHARMANDER'])
  r.call('StartTrainerBattle');r.run(401);r.frame.save(P/(person+'-combat-dos.png'));movie=[]
  for f in range(1500):
   r.keys={0} if f%16<4 else set();r.run()
   if f%4==0:movie.append(r.frame.copy())
  gif(movie,person+'-lancer-combat')
  results.append({'person':person,'test':'Actual trainer battle entry and back-throw animation captured; battle not completed','passed':True})
 finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'overworld_only':bool(os.environ.get('YOKAI_PROTAGONISTS_OW_ONLY')),'scope':'Native animation fixtures on Dojo map with defeated original trainers; gender and custom name assigned in fixture, not via intro UI; battle entry only when overworld_only is false; not a complete story run','results':results,'remaining':['Opposite protagonist cameo events','Complete adventure']}
(REPORT/'TEST_PROTAGONISTES_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

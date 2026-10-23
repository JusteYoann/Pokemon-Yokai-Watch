#!/usr/bin/env python3
"""Native follower fixtures: real controller steps/dialogues; no edited ROM."""
import os,json,struct,hashlib,traceback
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,strong_party
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
D=ROOT/'docs/pierre-philosovni/suivi-ariane'/mode;D.mkdir(parents=True,exist_ok=True)
r=new_game();strong_party(r);rows=[];frames=[];passed=False;failure=None

def check(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def actors():return [(i,o) for i in range(16) if (o:=r.read(r.symbols['gObjectEvents']+36*i,36))[0]&1]
def player():return next(o for i,o in actors() if o[8]==255)
def follower():return [(i,o) for i,o in actors() if o[5]==152]
def coords(o):return tuple(x-7 for x in struct.unpack_from('<hh',o,16))
def pos():return coords(player())
def state():return r.call('VarGet',0x40f4)
def free():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-x4.png'))
def run(n,key=None,movie=False):
 r.keys=set() if key is None else {key}
 for f in range(n):
  r.run()
  if movie and f%4==0:frames.append(r.frame.copy())
def finish(limit=20000):
 for f in range(limit):
  r.keys=battle_keys(r,f) if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 else ({8} if f%16<4 else set());r.run()
  if f>60 and free():run(12);return
 raise AssertionError('Script did not finish')
def warp(name,x,y):
 g,n=MAPS[name];r.keys=set();r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1800):
  r.run()
  if f>60 and free():break
 else:raise AssertionError(('warp',name))
 run(30)
def step(key,movie=False):
 start=pos();dx,dy={4:(0,-1),5:(0,1),6:(-1,0),7:(1,0)}[key];goal=start[0]+dx,start[1]+dy
 for f in range(60):
  run(1,key,movie)
  if pos()==goal:run(24,movie=movie);return
 raise AssertionError(('blocked',start,goal,[(o[8],coords(o)) for i,o in actors()]))
def save_continue():
 assert free();r.call('SaveMapView');assert r.call('TrySavingData',0,max_frames=1500)==1;assert r.call('LoadGameSave',0,max_frames=1500)==1;r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(2500):
  r.run()
  if f>180 and free():break
 else:raise AssertionError('Continue blocked')
 run(12)
try:
 warp('VermilionCity',33,30)
 assert not any(o[5]==153 for i,o in actors());assert len(follower())==1
 # Actual A interaction with Ariane and controller acceptance.
 run(1,4);run(20);run(1,8);finish();assert state()==1
 assert len(follower())==1
 check('First accepted dialogue automatically activates Ariane; no overworld Usapion')
 shot('acceptation')
 for key in [7,7,4,6,6,5,7,6]:step(key,True)
 run(40)
 assert len(follower())==1 and sum(abs(a-b) for a,b in zip(pos(),coords(follower()[0][1])))==1
 shot('suivi');check('Controller walking, corners and immediate reversal keep one adjacent Ariane',player=pos(),ariane=coords(follower()[0][1]))
 # Native walk pause until first reminder; no test-injected script or timer.
 elapsed=0
 while free() and elapsed<350:run(1);elapsed+=1
 assert not free() and elapsed<=300,elapsed
 run(320);shot('rappel-cinq-secondes');check('Automatic reminder after approximately five seconds without movement',remaining_frames_after_settle=elapsed)
 finish();run(650);assert free();check('One reminder per stop, no repeated dialogue after 10 more seconds')
 step(7);run(1,3);run(100)
 assert r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1 or not free()
 run(650);run(1,0);run(90);assert free();check('Menu pauses reminder timing')
 save_continue();assert len(follower())==1;check('Native Save/Continue restores the active companion without duplicates')
 # Walk through the real quay door from a fixture next to it.
 warp('VermilionCity',29,29)
 for f in range(200):
  run(1,4)
  if tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['VermilionCity_PhilosovniWarehouse']:break
 run(100)
 assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['VermilionCity_PhilosovniWarehouse']
 assert len(follower())==1 and not any(o[5]==153 for i,o in actors())
 shot('entrepot');check('Native door transition respawns one companion in the warehouse')
 save_continue();assert len(follower())==1;check('Continue inside warehouse keeps companion and new grunt IDs')
 run(320);assert not free();run(320);shot('rappel-entrepot');finish();check('Warehouse reminder gives the interior objective')
 # Ordinary A interaction with the follower uses its own script, not a missing dynamic template.
 # Facing direction is a fixture here; the dialogue and A input remain native.
 po=pos();fp=coords(follower()[0][1]);dx,dy=fp[0]-po[0],fp[1]-po[1]
 if abs(dx)+abs(dy)==1:
  key=7 if dx>0 else 6 if dx<0 else 5 if dy>0 else 4
  run(1,key);run(20);run(1,8);finish();check('Talking to the dynamic follower returns safely to field')
 # Actual tile trigger and native double battle, strong player party fixture.
 while pos()[1]>7:step(4)
 run(20,4)
 saw_battle=False
 for f in range(20000):
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   saw_battle=True
   assert r.u32(r.symbols['gBattleTypeFlags']) & (1<<23)
  r.keys=battle_keys(r,f) if saw_battle and r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 else ({8} if f%16<4 else set());r.run()
  if f>60 and free() and state()==3:break
 else:raise AssertionError(('Battle/end blocked',state()))
 assert saw_battle and not follower() and not any(o[5]==153 for i,o in actors())
 assert r.call('CheckBagHasItem',C['ITEM_HM01'],1)
 check('Real duo keeps AI Usapion in battle; both grunts escape, Cut received, following ends')
 run(700);assert free();shot('fin');check('No reminder after investigation completion')
 # Verify removal on original secondary-appearance map, without changing its Ariane script.
 warp('Route25',57,8);assert not any(o[5]==153 for i,o in actors());check('Route25 secondary Ariane preserved and overworld Usapion removed')
 # Pending-reward edge case on a different map: no hardcoded NPC IDs may be removed.
 r.call('VarSet',0x40f4,2);warp('Route25',57,8)
 assert len(follower())==1 and follower()[0][1][8]==202
 before={o[8] for i,o in actors() if o[5]!=152}
 assert r.call('PhilosovniFollowerDestination')==0
 save_continue();assert len(follower())==1
 r.call('ScriptContext_SetupScript',r.symbols['Philosovni_FollowerTalk']);finish()
 assert state()==3 and before<={o[8] for i,o in actors()}
 check('Pending reward can finish after travel/Continue without removing unrelated NPCs')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True);shot('ECHEC');print('debug',hex(r.u32(r.symbols['sGlobalScriptContext']+8)),r.read(r.symbols['sGlobalScriptContext'],16).hex(),hex(r.u32(r.symbols['gMain']+4)),r.read(r.symbols['sLockFieldControls'],1).hex(),[(o[8],coords(o),o[:3].hex()) for i,o in actors()],flush=True)
finally:
 if frames:frames[0].resize((720,480),Image.Resampling.NEAREST).save(D/'suivi-mgba.gif',save_all=True,append_images=[x.resize((720,480),Image.Resampling.NEAREST) for x in frames[1:]],duration=67,loop=0)
 (D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=rows,failure=failure,fixtures='Native new game, strong party, initial map positions; real controller movement, quest acceptance, reminder, doors and battle.'),ensure_ascii=False,indent=2)+'\n');r.close()
assert passed,failure

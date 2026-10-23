#!/usr/bin/env python3
"""Native party-switch, AI ownership, Cut, full bag and ordinary double regressions.
Initial parties/maps are fixtures. Full-bag fault fixture duplicates TM slots explicitly.
"""
import os,json,hashlib,struct,traceback,subprocess
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C,MAPS,warp,strong_party
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';P=ROOT/'docs/pierre-philosovni/validation'/mode;P.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;rows=[];failure=None
action_callbacks=set()
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines():
 a=line.split()
 if len(a)==3 and a[2]=='HandleInputChooseAction':action_callbacks.add(int(a[0],16)|1)

def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def fieldfree():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2'
def tick(f):r.keys=battle_keys(r,f) if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 else ({8} if f%16<4 else set());r.run()
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
def pulse(k,n=18):r.keys=set();r.run(4);r.keys={k};r.run();r.keys=set();r.run(n)
def script(s):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[s])
def val(i,k):return r.call('GetMonData',r.symbols['gPlayerParty']+100*i,C[k],0)
def setval(i,k,v):r.w32(r.PARAMS+128,v);r.call('SetMonData',r.symbols['gPlayerParty']+100*i,C[k],r.PARAMS+128)
def index(b):return int.from_bytes(r.read(r.symbols['gBattlerPartyIndexes']+b*2,2),'little')
def finish(limit=30000):
 for f in range(limit):
  tick(f)
  if f>50 and fieldfree():r.keys=set();r.run(10);return
 raise AssertionError(('Unfinished battle/script',hex(r.u32(r.symbols['gMain']+4)),hex(r.u32(r.symbols['gBattleMainFunc']))))
def battle_start():
 script('Philosovni_Overhear')
 for f in range(12000):
  tick(f)
  if r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:r.keys=set();r.run(20);return
 raise AssertionError('No action menu')
def has_task(name):return any(r.u32(r.symbols['gTasks']+40*i)==r.symbols[name]|1 and r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' for i in range(16))
def menu_choose(slot):
 # BFS through six cursor positions by real directional inputs, then repeat the found path.
 r.keys=set();r.run(75)
 start=r.snapshot();queue=[(start,[])];seen=set();path=None
 while queue:
  snap,keys=queue.pop(0);r.restore(snap);current=r.read(r.symbols['gPartyMenu']+9,1)[0]
  if current==slot:path=keys;break
  if current in seen:continue
  seen.add(current)
  for k in [4,5,6,7]:
   r.restore(snap);pulse(k);queue.append((r.snapshot(),keys+[k]))
 assert path is not None,('Slot unreachable',slot,seen)
 r.restore(start)
 for k in path:pulse(k)
 assert r.read(r.symbols['gPartyMenu']+9,1)[0]==slot
 shot('menu-six-membres');pulse(8,30);pulse(8,60)
 return path

def save():
 r.call('SaveMapView');assert r.call('TrySavingData',0,max_frames=1500)==1
 assert r.call('LoadGameSave',0,max_frames=1500)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(2000):
  tick(f)
  if f>180 and fieldfree():r.keys=set();return
 raise AssertionError('Continue failed')
def playerpos():
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1 and b[8]==255:return tuple(v-7 for v in struct.unpack_from('<hh',b,16))
def walk(k):
 x,y=playerpos();dx,dy={4:(0,-1),5:(0,1),6:(-1,0),7:(1,0)}[k]
 for _ in range(45):
  r.keys={k};r.run()
  if playerpos()==(x+dx,y+dy):r.keys=set();r.run(18);return
 raise AssertionError(('Blocked',playerpos(),k))
try:
 strong_party(r);r.call('VarSet',0x40f4,1);warp(r,*MAPS['VermilionCity_PhilosovniWarehouse'],6,8);base=r.snapshot()
 # Older city map-view snapshots cannot erase the new hut or keep the old fence.
 import subprocess
 old=struct.unpack('<1920H',subprocess.check_output(['git','show','e1dcd9132:data/layouts/VermilionCity/map.bin']))
 for px,py,check in [(29,29,(29,28)),(36,18,(36,17))]:
  warp(r,*MAPS['VermilionCity'],px,py)
  for x,y in [(x,17) for x in range(35,38)]+[(x,y) for y in range(25,29) for x in range(28,32)]:
   r.call('MapGridSetMetatileEntryAt',x+7,y+7,old[y*48+x])
  save();x,y=check
  now=r.call('MapGridGetMetatileIdAt',x+7,y+7)
  expected=0x29e if y==28 else 0x115
  assert now==expected,(check,hex(now),hex(expected))
 report('Legacy Flash saved map-view restores new warehouse door and open quay passage')
 r.restore(base)
 # Trainer restrictions on the dedicated duo use the native refusal paths.
 r.call('AddBagItem',C['ITEM_MASTER_BALL'],1);battle_start()
 def action(target):
  cur=r.read(r.symbols['gActionSelectionCursor'],1)[0]
  if (cur&1)!=(target&1):pulse(7 if target&1 else 6)
  cur=r.read(r.symbols['gActionSelectionCursor'],1)[0]
  if (cur&2)!=(target&2):pulse(5 if target&2 else 4)
  pulse(8,80)
 action(3)
 for f in range(600):
  tick(f)
  if r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:break
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\0'
 shot('duo-fuite-interdite');r.write(r.symbols['gBagMenuState']+6,b'\2\0');action(1);r.keys=set();r.run(160);pulse(8,240)
 for f in range(1800):
  tick(f)
  if r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:break
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\0' and not r.call('CheckBagHasItem',C['ITEM_MASTER_BALL'],1)
 report('Native flee and Master Ball attempts refused in duo; native blocked-ball consumption preserved')
 r.restore(base)
 # Six-member voluntary switch; no restriction to three or five player members.
 for i in range(1,6):
  r.call('CreateMon',r.symbols['gPlayerParty']+100*i,i+1,50,20,1,100+i,0,0)
  for j,m in enumerate(['MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_SWIFT','MOVE_MAGICAL_LEAF']):r.call('SetMonMoveSlot',r.symbols['gPlayerParty']+100*i,C[m],j)
  for f in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPATK','MON_DATA_SPDEF']:setval(i,f,999)
 r.write(r.symbols['gPlayerPartyCount'],b'\6');pids=[val(i,'MON_DATA_PERSONALITY') for i in range(6)]
 battle_start();pulse(5);pulse(8,100)
 assert has_task('Task_HandleChooseMonInput'),'Party menu not ready'
 path=menu_choose(5)
 for f in range(15000):
  tick(f)
  if index(0)==5 and index(2)==6 and r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:break
 else:raise AssertionError('Sixth member not switched in')
 shot('sixieme-membre-actif');report('Sixth member selected by native menu and switched beside AI Usapion',controller_path=path)
 finish();assert [val(i,'MON_DATA_PERSONALITY') for i in range(6)]==pids and val(6,'MON_DATA_SPECIES')==0
 report('Native switch preserves all six original player members; partner never enters roster')
 # Real forced switch after the weak first member faints.
 r.restore(base);r.call('CreateMon',r.symbols['gPlayerParty'],1,1,0,1,5,0,0)
 for j in range(4):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_GROWL'],j)
 r.call('CreateMon',r.symbols['gPlayerParty']+100,4,100,31,1,6,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\2')
 for f in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPATK','MON_DATA_SPDEF']:setval(1,f,999)
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty']+100,C['MOVE_AERIAL_ACE'],0)
 battle_start()
 for f in range(18000):
  tick(f)
  if has_task('Task_HandleChooseMonInput'):break
 else:raise AssertionError('Forced player replacement not reached')
 assert int.from_bytes(r.read(r.symbols['gPlayerParty']+86,2),'little')==0
 menu_choose(1)
 for f in range(12000):
  tick(f)
  if index(0)==1:break
 else:raise AssertionError('Forced replacement did not finish')
 assert index(2)==6;finish();report('Native forced replacement after player faint preserves partner ownership')
 # Usapion PP must be spent without any ally move menu or cursor input.
 r.restore(base)
 for j in range(4):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_GROWL'],j)
 battle_start();pp=sum(val(6,'MON_DATA_PP1') if i==0 else val(6,'MON_DATA_PP'+str(i+1)) for i in range(4));spent=False;ally_fainted=False
 for f in range(20000):
  tick(f)
  if f%40==0 and r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   cur=sum(r.read(r.symbols['gBattleMons']+2*88+0x24,4));spent |= cur<pp
   if r.read(r.symbols['gAbsentBattlerFlags'],1)[0]&4:ally_fainted=True;break
  if f>60 and fieldfree():break
 assert spent,'Partner never spent PP'
 assert ally_fainted,'Partner faint case not reached naturally'
 assert val(0,'MON_DATA_HP')>0 and not has_task('Task_HandleChooseMonInput')
 shot('usapion-ko-joueur-continue');report('Usapion attacks autonomously, spends PP and can faint without taking a player reserve')
 # Restore ordinary attacking moves on the player's own mon to finish this long-edge fixture.
 for j,m in enumerate(['MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_SWIFT','MOVE_MAGICAL_LEAF']):
  r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C[m],j)
  # Battle representation is explicitly updated for this player-only test fixture.
  r.write(r.symbols['gBattleMons']+0xc+2*j,struct.pack('<H',C[m]));r.write(r.symbols['gBattleMons']+0x24+j,b'\x14')
 finish();report('Player completes duo after ally faint')
 # Full TM pocket fault fixture: all58 occupied by quantity1 TM01 stacks, no HM01.
 r.restore(base);pocket=r.symbols['gBagPockets']+8*(C['POCKET_TM_CASE']-1);slots=r.u32(pocket);capacity=r.read(pocket+4,1)[0]
 for i in range(capacity):
  r.write(slots+4*i,struct.pack('<H',C['ITEM_TM01']));r.call('SetBagItemQuantity',slots+4*i+2,1)
 assert not r.call('CheckBagHasSpace',C['ITEM_HM01'],1)
 battle_start();finish();assert r.call('VarGet',0x40f4)==2 and not r.call('CheckBagHasItem',C['ITEM_HM01'],1)
 save();assert r.call('VarGet',0x40f4)==2;shot('cs-attend-sac-plein');r.call('ClearBag');script('Philosovni_WarehouseAriane');finish()
 assert r.call('VarGet',0x40f4)==3 and r.call('BagGetQuantityByItemId',C['ITEM_HM01'])==1
 report('Full-pocket fault fixture preserves pending reward across Flash Continue; retry grants exactly one Cut',capacity=capacity)
 # Native Cut tree gate and actual traversal into the original Gym.
 strong_party(r);r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_CUT'],0)
 warp(r,*MAPS['VermilionCity'],19,23);pulse(5);pulse(8,1);finish();assert any((b:=r.read(r.symbols['gObjectEvents']+36*i,36))[0]&1 and b[8]==7 for i in range(16))
 report('Cut remains blocked without native badge2 even with HM and learned move')
 r.call('FlagSet',0x821);pulse(8,1);finish();assert not any((b:=r.read(r.symbols['gObjectEvents']+36*i,36))[0]&1 and b[8]==7 for i in range(16))
 shot('coupe-arbre-carmin');walk(5);walk(5);walk(5)
 for _ in range(5):walk(6)
 r.keys={4}
 for _ in range(300):
  r.run()
  if tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['VermilionCity_Gym']:break
 r.keys=set();r.run(180)
 assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['VermilionCity_Gym']
 shot('entree-arene-apres-coupe');report('Actual native Cut animation removes tree and permits walking into Gym with badge2')
 # Ordinary local double: battler2 still asks the human for an action.
 r.restore(base);strong_party(r);r.call('CreateMon',r.symbols['gPlayerParty']+100,4,100,31,1,101,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\2')
 warp(r,*MAPS['VictoryRoad_3F'],6,8);script('VictoryRoad_3F_EventScript_Ray')
 for f in range(14000):
  tick(f)
  if r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:break
 else:raise AssertionError('Ordinary double not reached')
 assert not r.u32(r.symbols['gBattleTypeFlags'])&(1<<23) and index(2)==1
 for f in range(1500):
  tick(f)
  if r.u32(r.symbols['gBattlerControllerFuncs']+8) in action_callbacks:break
 else:raise AssertionError('Ordinary second battler no longer human-controlled')
 shot('double-ordinaire-preserve');report('Ordinary double keeps both player-controlled battlers and native party indexes')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True);shot('ECHEC-LIMITES')
finally:
 (P/'LIMITES_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=rows,failure=failure),ensure_ascii=False,indent=2)+'\n');r.close()
assert passed,failure

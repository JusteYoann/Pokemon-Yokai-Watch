#!/usr/bin/env python3
"""Targeted native field fixtures, not a complete adventure playthrough."""
import os,json,struct,hashlib,traceback,subprocess
from pathlib import Path
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp,strong_party
from mgba_rpc import ROOT
OUT=ROOT/'docs/beta-retours-20261024/terrain';OUT.mkdir(parents=True,exist_ok=True)
C.update(FLAG_LAVENDER_INTRO_DONE=0x322,VAR_LAVENDER_INTRO=0x40f3,FLAG_BADGE04_GET=0x823)
r=new_game();rows=[];error=None
action_callbacks={int(v.split()[0],16)|1 for v in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v.split())==3 and v.split()[2]=='HandleInputChooseAction'}

def record(name,**kw):
 rows.append(dict(test=name,**kw));print(name,kw,flush=True)
def obj(i):return r.symbols['gObjectEvents']+36*i
def oid(lid):
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);return r.call('GetObjectEventIdByLocalIdAndMap',lid,r.read(sb+5,1)[0],r.read(sb+4,1)[0])
def pos(i):return struct.unpack('<hh',r.read(obj(i)+16,4))
def playerpos():return pos(r.read(r.symbols['gPlayerAvatar']+5,1)[0])
def shot(n):r.frame.save(OUT/(n+'.png'))
try:
 strong_party(r);r.call('FlagSet',C['FLAG_LAVENDER_INTRO_DONE']);r.call('VarSet',C['VAR_LAVENDER_INTRO'],1);r.call('FlagSet',C['FLAG_BADGE04_GET'])
 warp(r,*MAPS['LavenderTown'],8,10)
 # Postbadge field must stay interactive even when zombies see the player.
 assert not r.call('LavanvilleTryZombieSight')
 ids={lid:oid(lid) for lid in range(1,5)};events={k:[] for k in ids};previous={k:pos(v) for k,v in ids.items()}
 for f in range(1800):
  r.run()
  for lid,i in ids.items():
   now=pos(i)
   if now!=previous[lid]:events[lid].append(f);previous[lid]=now
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
 periods={k:[b-a for a,b in zip(v,v[1:])] for k,v in events.items()}
 record('No automatic encounter after Alyzon; native patrol timings',moves=events,periods=periods)
 shot('lavanville-apres-badge')
 # Night tint must not color the bag's native UI palette.
 field_snapshot=r.snapshot();r.call('CB2_BagMenuFromStartMenu');r.run(180)
 matched=False
 for _ in range(16):
  r.run()
  if r.read(0x05000000,384)==r.read(r.symbols['gPlttBufferFaded'],384):matched=True;break
 assert matched,'Lavender field tint leaked into bag UI'
 shot('lavanville-sac-palette-native');record('Lavender bag UI retains native hardware palette',passed=True)
 r.restore(field_snapshot);r.keys=set();r.run(4)
 # A deliberate postbadge talk must work immediately after map immunity is set.
 warp(r,*MAPS['LavenderTown'],5,9);z=oid(1)
 assert r.call('LavanvilleCheckZombieImmunity')==0
 r.write(r.symbols['gSelectedObjectEvent'],bytes([z]));r.write(r.symbols['gSpecialVar_LastTalked'],b'\x01\0')
 r.call('ScriptContext_SetupScript',r.symbols['LavenderZombie_Variant0'])
 for f in range(6000):
  r.keys={8} if f%24<2 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:break
 else:raise AssertionError('Voluntary postbadge zombie battle did not start')
 r.keys=set();r.run(24)
 for key in [5,7,8]:
  r.keys={key};r.run(2);r.keys=set();r.run(20)
 for f in range(5000):
  r.keys={8} if f%24<2 else set();r.run()
  if f>30 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
 else:raise AssertionError('Run did not return to unlocked field')
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\x04'
 r.keys=set();r.run(180);assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
 record('Voluntary postbadge talk starts battle despite arrival immunity; controller RUN succeeds',native_outcome=4,no_automatic_rebattle=True)
 shot('zombie-defi-volontaire-fuite')
 # Two-tile sight ray: stop adjacent, display growl, then native zombie battle.
 warp(r,*MAPS['LavenderTown'],5,9);r.call('SetMainCallback2',r.symbols['SpriteCallbackDummy']|1);z=oid(1)
 r.call('MoveObjectEventToMapCoords',obj(z),12,14)
 r.call('ObjectEventTurn',obj(z),1);r.call('FlagClear',C['FLAG_BADGE04_GET']);r.write(r.symbols['sZombieCooldown'],b'\0\0')
 r.write(r.symbols['sZombieSightApproach'],b'\0')
 # Collision-free ray is checked by the actual sight function.
 found=r.call('LavanvilleTryZombieSight');assert found,(pos(z),playerpos(),r.read(obj(z),36).hex())
 r.call('SetMainCallback2',r.symbols['CB2_Overworld']|1)
 start=pos(z);positions=[];frames=[];growl=False
 for f in range(6000):
  r.keys={8} if f%24<2 else set();r.run()
  if f%6==0:frames.append(r.frame.copy())
  if f%4==0 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:positions.append(pos(z))
  if r.read(r.symbols['gStringVar4'],6)==r.read(r.symbols['LavenderZombie_Growl'],6):growl=True
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:break
 else:raise AssertionError('Zombie approach did not reach battle menu')
 shot('zombie-combat');frames[0].save(OUT/'zombie-approche.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
 assert r.call('IsRunningFromBattleImpossible')!=0
 r.call('FlagSet',C['FLAG_BADGE04_GET']);assert r.call('IsRunningFromBattleImpossible')==0
 assert r.call('TryRunFromBattle',0)
 record('Sight approach and native escape restriction follow badge',start=start,positions=sorted(set(positions)),growl_observed=growl,prebadge_escape_denied=True,postbadge_escape_success=True)
 # Return to an isolated field snapshot through a fresh game, not battle RAM.
 r.close();r=new_game();strong_party(r)
 r.call('VarSet',0x40f4,3)
 for route,coords in [('Route21_South',[(18,y) for y in [49,46,44,42,40,38,34]]),('Route20',[(x,9) for x in [1,2,4,6,8,10,18]])]:
  samples=[]
  for index,(x,y) in enumerate(coords):
   warp(r,*MAPS[route],x,y);r.call('VarSet',0x4020,250);r.run(12)
   strength=r.call('CramoisPastStrength');bank=r.call('LoadNativeMountPalette');assert bank<16
   original=r.read(r.symbols['gObjectEventPal_PlayerUnused'],32)
   assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==original
   # Buffer remains untinted, physical palette receives local sepia/fog.
   samples.append(dict(x=x,y=y,sepia_strength=strength,mount_palette_bank=bank,original_mount_palette_preserved=True))
   if index in [0,3,len(coords)-1]:shot(route+'-'+str(index))
  assert [s['sepia_strength'] for s in samples][:1]==[16]
  assert samples[-1]['sepia_strength']==0
  record(route+' graded sepia and independent native mount palette',samples=samples)
except BaseException as e:
 error=traceback.format_exc();print(error,flush=True)
 try:shot('erreur')
 except Exception:pass
finally:
 (OUT/'TEST_MGBA.json').write_text(json.dumps(dict(passed=error is None,error=error,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n');r.close()
if error:raise SystemExit(1)

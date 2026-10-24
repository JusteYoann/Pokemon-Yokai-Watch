#!/usr/bin/env python3
"""Isolated mGBA fixture: Ariane double intro, four textures, move and switch.
Initial party/map and direct native duo start are fixtures. No enemy HP/outcome
is forced. Branch snapshots isolate UI checks, separate from player campaign.
"""
import os,json,struct,hashlib,subprocess
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=Path(os.environ.get('DUO_REPORT',str(ROOT/'docs/ariane-duo-sprites-20261024/apres')));P.mkdir(parents=True,exist_ok=True)
r=new_game(int(os.environ.get('DUO_GENDER',0)));rows=[];movie=[]

def pulse(key,after=60):
 r.keys=set();r.run(4);r.keys={key};r.run(4);r.keys=set();r.run(after)
def callback():return r.u32(r.symbols['gMain']+4)
action_callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
def action():return callback()==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks

def wait_action(limit=10000):
 for f in range(limit):
  if action():r.keys=set();r.run(30);return True
  if callback() in (r.symbols['CB2_ReturnToField']|1,r.symbols['CB2_ReturnToFieldLocal']|1):return False
  r.keys={8} if f%16<3 else set();r.run()
 raise AssertionError('Battle action menu not reached')

def check(label):
 gfx=r.u32(r.symbols['gMonSpritesGfxPtr']);actors=[];used=set()
 assert r.read(r.symbols['gBattlersCount'],1)==b'\4'
 for b in range(4):
  mon=r.symbols['gBattleMons']+88*b;hp=int.from_bytes(r.read(mon+40,2),'little')
  if not hp:continue
  sid=r.read(r.symbols['gBattlerSpriteIds']+b,1)[0];assert sid<64
  s=r.read(r.symbols['gSprites']+68*sid,68);tile=int.from_bytes(s[4:6],'little')&1023
  position=r.read(r.symbols['gBattlerPositions']+b,1)[0]
  form=r.read(r.symbols['gBattleMonForms']+b,1)[0]
  source=r.u32(gfx+4+4*position)+2048*form
  pixels=r.read(source,2048);loaded=r.read(0x06010000+32*tile,2048)
  assert pixels==loaded,(label,b,'VRAM does not contain its own picture')
  occupied=set(range(tile,tile+64));assert not used&occupied,(label,b,'Overlapping battler tiles');used|=occupied
  actors.append(dict(battler=b,species=int.from_bytes(r.read(mon,2),'little'),tile=tile,pixels_sha256=hashlib.sha256(pixels).hexdigest(),vram_matches=True))
 r.frame.save(P/(label+'.png'));rows.append(dict(test=label,passed=True,actors=actors));print('PASS',label,flush=True)
try:
 for i,species in enumerate((93,1)):
  r.call('CreateMon',r.symbols['gPlayerParty']+100*i,species,18,31,1,12345+i,0,0)
  r.call('SetMonMoveSlot',r.symbols['gPlayerParty']+100*i,10,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\2')
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])};g,n=maps['VermilionCity_PhilosovniWarehouse']
 r.call('VarSet',0x40f4,1);r.call('SetWarpDestination',g,n,255,6,8);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(300)
 r.call('PhilosovniStartDuo')
 for f in range(16000):
  r.keys={8} if f%32<3 else set();r.run()
  if callback()==r.symbols['BattleMainCB2']|1:
   if f%12==0:movie.append(r.frame.copy())
   if action():r.keys=set();r.run(30);break
 else:raise AssertionError('No double action menu')
 assert struct.unpack('<4H',r.read(r.symbols['gBattlerPartyIndexes'],8))==(0,0,6,1)
 check('introduction');base=r.snapshot()
 # One native player attack + automatic Usapion move + native opponents.
 pulse(8);pulse(8);pulse(8,180)
 assert wait_action();check('apres-attaque')
 # Independent switch branch, restoring only the isolated test fixture.
 r.restore(base);pulse(5,20);pulse(8,180)
 assert callback()==r.symbols['CB2_UpdatePartyMenu']|1
 pulse(5,30);assert r.read(r.symbols['gPartyMenu']+9,1)==b'\1'
 pulse(8);pulse(8,180)
 assert wait_action();check('apres-changement')
 assert int.from_bytes(r.read(r.symbols['gBattleMons'],2),'little')==1
 assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\2'
 assert int.from_bytes(r.read(r.symbols['gBattlerPartyIndexes']+4,2),'little')==6
 if movie:movie[0].save(P/'introduction.gif',save_all=True,append_images=movie[1:],duration=200,loop=0)
 (P/'TEST.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),gender=int(os.environ.get('DUO_GENDER',0)),cases=rows),indent=2)+'\n')
finally:r.frame.save(P/'dernier.png');r.close()

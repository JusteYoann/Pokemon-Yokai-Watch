#!/usr/bin/env python3
"""Native mGBA Enma approved front/back layout, original textures and animation background checks. Map and parties are explicit fixtures; no sprite OAM or enemy outcome patches."""
import os,json,hashlib,struct,subprocess,traceback
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import warp,MAPS,C
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/dossier-20261023/enma-placement'/mode;D.mkdir(parents=True,exist_ok=True)
r=None;rows=[];passed=False;failure=None;movie=[]
def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-x4.png'))
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def geometry(b):return struct.unpack('<hhbbbbBB',r.read(r.call('GetYokaiBattleGeometry',b),10))
def oam_matrix(b):
 sid=r.read(r.symbols['gBattlerSpriteIds']+b,1)[0];sp=r.symbols['gSprites']+68*sid;attr=int.from_bytes(r.read(sp+4,2),'little')
 hits=[]
 for i in range(128):
  a0,a1,a2=struct.unpack('<HHH',r.read(0x07000000+8*i,6))
  if a2==attr and a0&0x100 and a1>>14==3:
   m=(a1>>9)&31;hits.append(struct.unpack('<h',r.read(0x07000000+32*m+6,2))[0:1]+struct.unpack('<h',r.read(0x07000000+32*m+30,2)))
 assert len(hits)==1,(b,hits,hex(attr))
 return hits[0]
try:
 r=new_game();warp(r,*MAPS['Route1'],10,10)
 for party in ['gPlayerParty','gEnemyParty']:r.call('CreateMon',r.symbols[party],150,70,31,1,100,0,0)
 for count in ['gPlayerPartyCount','gEnemyPartyCount']:r.write(r.symbols[count],b'\1')
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0)
 r.call('StartScriptedWildBattle')
 callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
 for frame in range(6000):
  r.keys={8} if frame%16<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Native action menu not reached')
 r.keys=set();r.run(30);shot('placement-face-dos')
 for b,side,inv in [(1,'front',225),(0,'back',170)]:
  g=geometry(b);assert g[0]==g[1]==inv;
  expected=(225,225,-6,-4,-34,-32,70,65) if b==1 else (170,170,6,17,-40,-43,83,87)
  assert g==expected,(b,g)
  sid=r.read(r.symbols['gBattlerSpriteIds']+b,1)[0];sp=r.symbols['gSprites']+68*sid
  center=struct.unpack('<hh',r.read(sp+32,4));assert center==((170,36) if b==1 else (78,97)),(b,center)
  hardware=oam_matrix(b);assert abs(hardware[0])==abs(hardware[1])==inv,(b,hardware)
  position=r.call('GetBattlerPosition',b);ptr=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*position)
  assert r.read(ptr,2048)==(ROOT/f'graphics/yokai/150/{side}-battle.4bpp').read_bytes()
  report(side+' uniform native hardware matrix and original indexed pixels',inverse_scale=inv,center=list(center),geometry=list(g),hardware_matrix_diagonal=hardware)
 # Exact native animation silhouette conversion; restore untouched battle after each probe.
 state=r.snapshot()
 for b,side in [(1,'front'),(0,'back')]:
  r.restore(state);g=geometry(b);tiles=r.call('AllocZeroed',4096);tilemap=r.call('AllocZeroed',2048);assert tiles and tilemap
  assert r.call('CopyYokaiBattlerToBg',1,b,2,tiles,tilemap,0)==1
  cols=(g[6]+7)//8;rowsn=(g[7]+7)//8;assert cols*rowsn*32<=4096
  raw=r.read(tiles,4096);assert any(raw) and not any(raw[cols*rowsn*32:])
  position=r.call('GetBattlerPosition',b);src=r.read(r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*position),2048);expected=bytearray(4096)
  for y in range(g[7]):
   sy=((y+g[5])*g[1]>>8)+32
   for x in range(g[6]):
    sx=((x+g[4])*g[0]>>8)+32
    if 0<=sx<64 and 0<=sy<64:
     value=(src[(sy//8*8+sx//8)*32+(sy%8)*4+(sx%8)//2]>>((sx&1)*4))&15
     idx=(y//8*cols+x//8)*32+(y%8)*4+(x%8)//2;expected[idx]|=value<<((x&1)*4)
  assert raw==expected;report(side+' native animation background matches uniform silhouette',width=g[6],height=g[7],tile_bytes=cols*rowsn*32)
 r.restore(state);r.keys=set();initial_hp=int.from_bytes(r.read(r.symbols['gBattleMons']+88+0x28,2),'little');returned=False
 for frame in range(1800):
  r.keys=battle_keys(r,frame);r.run()
  if frame%6==0:movie.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
  hp=int.from_bytes(r.read(r.symbols['gBattleMons']+88+0x28,2),'little')
  if frame>60 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks and 0<hp<initial_hp:
   returned=True;break
 assert movie and returned,'Real damaging move must finish and return to the action menu'
 r.keys=set();r.run(16);shot('apres-attaque')
 for b,inv in [(1,225),(0,170)]:
  hardware=oam_matrix(b);assert abs(hardware[0])==abs(hardware[1])==inv,(b,hardware)
 report('Real damaging move completed through controller; uniform layout retained on return to action menu',enemy_hp_before=initial_hp,enemy_hp_after=hp)
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True)
 if r:shot('ECHEC')
finally:
 if movie:movie[0].save(D/'combat-placement.gif',save_all=True,append_images=movie[1:],duration=100,loop=0)
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest() if r else None
 if r:r.close()
 (D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=sha,checks=rows,failure=failure,scope=__doc__),ensure_ascii=False,indent=2)+'\n')
assert passed,failure

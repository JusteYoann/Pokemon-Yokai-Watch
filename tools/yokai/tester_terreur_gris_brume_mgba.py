#!/usr/bin/env python3
"""Rendu natif gris/brume et expiration: combats réellement exécutés par mGBA."""
import os,json,struct,subprocess,hashlib
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-corrections-20261025';P.mkdir(parents=True,exist_ok=True)
r=new_game();checks=[];movie=[];deadline=[];th=r.symbols['sTh'];party=r.symbols['gPlayerParty']
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
actions={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
def passed(s):checks.append(s);print('PASS',s,flush=True)
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def unlocked():return field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0'
def warp(n,x,y):
 g,m=maps[n];r.call('SetWarpDestination',g,m,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
def wait(cond,n=18000,record=False):
 for f in range(n):
  if cond():r.keys=set();return
  r.keys={8} if f%20<2 else set();r.run()
  if record and f%3==0:deadline.append(r.frame.copy().resize((720,480),Image.Resampling.NEAREST))
 r.frame.save(P/'echec.png');raise AssertionError(('Timeout',hex(r.u32(r.symbols['gMain']+4))))
def begin():
 for i in range(16):r.call('TerreHeureTryStep')
 assert r.read(th+175,1)==b'\1';wait(lambda:unlocked() and r.read(th+176,1)==b'\2')
def clouds():
 return [r.symbols['gSprites']+68*i for i in range(64) if r.read(r.symbols['gSprites']+68*i+62,1)[0]&1 and r.u32(r.symbols['gSprites']+68*i+28)==r.symbols['Cloud']|1]
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
try:
 for i in range(1):
  r.call('CreateMon',party+100*i,150-i,100,31,1,12345+i,0,0);r.call('SetMonMoveSlot',party+100*i,89,0)
  for fieldid in (57,58,59,60,61,62,63):r.w32(r.symbols['gStringVar4'],999);r.call('SetMonData',party+100*i,fieldid,r.symbols['gStringVar4'])
 r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96);r.call('VarSet',0x40f9,1);base=r.snapshot()
 warp('MtMoon_1F',24,28);begin();r.call('LockPlayerFieldControls');r.run(4)
 colors=struct.unpack('<208H',r.read(0x05000000,416));assert all(c&31==(c>>5)&31==(c>>10)&31 for c in colors)
 passed('Les 208 couleurs du décor sont réellement en niveaux de gris, sans composante sépia')
 fog=clouds();assert len(fog)==15,len(fog);before=[r.read(p+32,4) for p in fog];shot('gris-nuages-jaunes')
 start=r.frame.copy()
 for f in range(180):
  r.run()
  if f%3==0:movie.append(r.frame.copy().resize((720,480),Image.Resampling.NEAREST))
 assert before!=[r.read(p+32,4) for p in clouds()];assert start.tobytes()!=r.frame.tobytes();passed('Quinze nappes légères se déplacent alors que Nathan reste immobile')
 # Compare colored player pixels with/without cloud layer. Only fixture state is temporarily changed.
 withfog=r.frame.copy();mask=[]
 player=next(r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i+8,1)==b'\xff')
 sp=r.symbols['gSprites']+68*r.read(player+4,1)[0];x,y,x2,y2=struct.unpack('<hhhh',r.read(sp+32,8));cx,cy=struct.unpack('<bb',r.read(sp+40,2))
 ox=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetX'],2))[0];oy=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetY'],2))[0]
 left,top=x+x2+cx+ox,y+y2+cy+oy;tile=int.from_bytes(r.read(sp+4,2),'little')&1023;pixels=r.read(0x06010000+tile*32,256)
 for y in range(32):
  for x in range(16):
   byte=pixels[((y//8)*2+x//8)*32+(y%8)*4+(x%8)//2];index=(byte>>(4*(x%2)))&15
   if index:mask.append((left+x,top+y))
 snapshot=r.snapshot();r.write(th+175,b'\0');r.call('TerreHeureFogClear');r.run(3);without=r.frame.copy()
 differences=[(p,withfog.getpixel(p),without.getpixel(p)) for p in mask if withfog.getpixel(p)!=without.getpixel(p)]
 assert len(mask)>=20 and not differences,(len(mask),differences[:8])
 r.restore(snapshot);r.call('UnlockPlayerFieldControls');passed('Les pixels colorés de Nathan restent identiques: les nuages passent derrière lui')
 # Natural contact still reaches a real battle, and expiry launches the right tier without input.
 for tier in range(3):
  r.restore(base)
  if tier>=1:r.call('FlagSet',0x335)
  if tier>=2:r.call('FlagSet',0x336)
  warp('MtMoon_1F',18,35);begin();r.w32(th+156,120 if tier==0 else 1)
  for f in range(1000):
   r.keys=set();r.run()
   if tier==0 and f%3==0:deadline.append(r.frame.copy().resize((720,480),Image.Resampling.NEAREST))
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
  else:raise AssertionError('Le combat ne démarre pas automatiquement à zéro')
  assert not clouds();wait(lambda:r.u32(r.symbols['gBattlerControllerFuncs']) in actions,record=tier==0)
  assert r.call('GetMonData',r.symbols['gEnemyParty'],11)==(59,85,60)[tier];shot('chrono-zero-combat-'+str(tier+1))
  passed(('Gargaros','Ogralos','Orqanos')[tier]+': combat automatique à zéro, sans confirmation ni sortie de la Terr’heure')
  wait(lambda:unlocked() and r.read(th+183,1)==b'\1',42000);r.run(10);assert len(clouds())==15;shot('chrono-zero-victoire-'+str(tier+1))
  passed(('Gargaros','Ogralos','Orqanos')[tier]+': victoire après expiration, exploration libre et brume restaurées')
 # Deadline must also work on a passage where no Oni object is present.
 r.restore(base);r.call('VarSet',0x40f9,6);
 rows=json.loads((ROOT/'docs/terre-heure-20261025/AUDIT_GROTTES.json').read_text())['maps']
 a=next(row for row in rows if row['map']=='MtEmber_RubyPath_B4F')['candidates'][0];warp('MtEmber_RubyPath_B4F',*a[:2]);begin()
 a=next(row for row in rows if row['map']=='MtEmber_RubyPath_B3F')['candidates'][0];warp('MtEmber_RubyPath_B3F',*a[:2])
 r.w32(th+156,0);wait(lambda:r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1);passed('L’expiration démarre le combat même sur un petit étage sans Oni visible')
finally:
 (P/'TESTS_CORRECTIONS.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':checks},ensure_ascii=False,indent=2)+'\n')
 if deadline:deadline[0].save(P/'chrono-zero-combat-mgba-x3.gif',save_all=True,append_images=deadline[1:],duration=50,loop=0)
 if movie:movie[0].save(P/'gris-brume-mobile-mgba-x3.gif',save_all=True,append_images=movie[1:],duration=50,loop=0)
 r.close()

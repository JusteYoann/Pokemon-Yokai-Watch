#!/usr/bin/env python3
"""Corrected user PNGs: real field and trainer renderer, native tiles/palette checks.
Invitation, map and player team are fixtures; A triggers the actual NPC event.
This is a graphics check, not a repeat of the full quest or balancing tests.
"""
import os,json,hashlib,struct,subprocess
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,warp,strong_party
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/juste-yoann/corrections-sprites-20261024'/mode;D.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False;frames=[]
def shot(n):r.frame.save(D/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(D/(n+'-x3.png'))
def verify(sid,name):
 s=r.symbols['gSprites']+68*sid;attr=int.from_bytes(r.read(s+4,2),'little');tile=attr&1023;pal=attr>>12
 pixels=(ROOT/f'graphics/juste_yoann/{name}.4bpp').read_bytes()
 assert r.read(0x06010000+tile*32,len(pixels))==pixels,(name,'VRAM differs')
 expected=(ROOT/'graphics/juste_yoann/normal.gbapal').read_bytes()
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+pal*32,32)==expected,(name,'palette differs')
 rows.append({'sprite':name,'native_tiles_equal':True,'native_palette_equal':True,'bytes':len(pixels)})
try:
 r.call('FlagSet',0x331);warp(r,*MAPS['PalletTown_PlayersHouse_2F'],6,3);strong_party(r)
 obj=r.call('GetObjectEventIdByLocalIdAndMap',1,MAPS['PalletTown_PlayersHouse_2F'][1],MAPS['PalletTown_PlayersHouse_2F'][0]);assert obj<16
 p=r.symbols['gObjectEvents']+36*obj
 assert struct.unpack('<hh',r.read(p+16,4))==(13,9) and r.read(p+24,1)[0]&15==1
 verify(r.read(p+4,1)[0],'overworld');shot('chambre-corrigee')
 r.keys={4};r.run(8);r.keys=set();r.run(16);r.keys={8};r.run(2);r.keys=set();r.run(8)
 callbacks={int(a[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(a:=line.split())==3 and a[2]=='HandleInputChooseAction'}
 portrait=False;started=False
 for f in range(6000):
  r.keys={8} if f%20<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   started=True
   if f%8==0:frames.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
   sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
   if sid<64 and not portrait:
    sp=r.symbols['gSprites']+68*sid
    if r.read(sp+62,1)[0]&1 and r.read(sp+6,2)==b'\xa7\0' and r.read(sp+36,2)==b'\0\0':
     r.run(1);verify(sid,'battle');shot('portrait-corrige');portrait=True
   if r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Battle action menu not reached')
 assert started and portrait
 passed=True
finally:
 if frames:frames[0].save(D/'introduction-corrigee.gif',save_all=True,append_images=frames[1:],duration=135,loop=0)
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=sha,results=rows),ensure_ascii=False,indent=2)+'\n')

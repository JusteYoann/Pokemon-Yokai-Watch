#!/usr/bin/env python3
"""Actual mGBA rendering: two native OBJ sprites uploaded to temporary RAM/VRAM.
Does not patch the ROM, maps, scripts, progression, or a persistent save.
"""
import sys,os,struct,json,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'tools/yokai'))
from mgba_new_game import new_game
from mafiamille_qa import MAPS,warp
D=Path(__file__).resolve().parents[1]/'prototypes/apercu-deux-zombies-mgba';D.mkdir(exist_ok=True)
def tiles(im):
 data=list(im.getdata());b=bytearray()
 for ty in range(4):
  for tx in range(4):
   for y in range(8):
    for x in range(0,8,2):
     i=(ty*8+y)*32+tx*8+x;b.append(data[i]|data[i+1]<<4)
 return bytes(b)
r=new_game();records=[]
try:
 warp(r,*MAPS['LavenderTown'],15,8)
 # Upload through native sheet/palette allocators, not post-render compositing.
 sid=r.read(r.symbols['gPlayerAvatar']+4,1)[0];a=r.symbols['gSprites']+68*sid
 px,py=struct.unpack('<hh',r.read(a+32,4));priority=struct.unpack('<H',r.read(a+4,2))[0]&0xC00
 for i,name in enumerate(['zombie-1','zombie-2']):
  im=Image.open(D/(name+'.png'));assert im.mode=='P' and im.size==(32,32)
  opaque={c for c in im.getdata() if c};assert len(opaque)<=15
  pal=im.getpalette();gba=struct.pack('<16H',*[((pal[j*3]>>3)|((pal[j*3+1]>>3)<<5)|((pal[j*3+2]>>3)<<10)) for j in range(16)])
  mem=r.call('AllocZeroed',1024);assert mem
  r.write(mem,tiles(im));r.write(mem+512,gba)
  tag=0xF100+i
  r.write(mem+552,struct.pack('<IHH',mem,512,tag));tile=r.call('LoadSpriteSheet',mem+552)
  r.write(mem+560,struct.pack('<IHH',mem+512,tag,0));bank=r.call('LoadSpritePalette',mem+560);assert bank<16
  r.write(mem+568,struct.pack('<4H',0,0x8000,priority,0))
  r.write(mem+576,struct.pack('<HHIIIII',tag,tag,mem+568,r.symbols['gDummySpriteAnimTable'],0,r.symbols['gDummySpriteAffineAnimTable'],r.symbols['SpriteCallbackDummy']|1))
  obj=r.call('CreateSprite',mem+576,px+(-32 if i==0 else 32),py,0x70);assert obj<64
  sp=r.symbols['gSprites']+68*obj+62;r.write(sp,bytes([r.read(sp,1)[0]|2]));r.run(3)
  records.append(dict(name=name,sprite_id=obj,palette_bank=bank,tile_start=tile,canvas=[32,32],silhouette=list(im.convert('RGBA').getbbox())))
 r.run(30);r.frame.save(D/'mgba-jour-natif.png');r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/'mgba-jour-x4.png')
 original=struct.unpack('<512H',r.read(r.symbols['gPlttBufferUnfaded'],1024))
 r.call('SetNextWeather',6);r.run(200);weatherbank=r.call('IndexOfSpritePaletteTag',0x1200)
 native=struct.unpack('<512H',r.read(r.symbols['gPlttBufferUnfaded'],1024));colors=[]
 for c in original:
  red=c&31;green=c>>5&31;blue=c>>10&31;colors.append((red*9//16)|((green*9//16)<<5)|(min(31,blue*12//16+3)<<10))
 for j,c in enumerate(native[256+16*weatherbank:272+16*weatherbank]):
  v=max(c&31,c>>5&31,c>>10&31);colors[256+16*weatherbank+j]=v*5//16|((v*12//16)<<5)|((v*7//16)<<10)
 # Keep eyes/skin readable: same softer OBJ treatment for player and test zombies.
 banks=[r.read(a+5,1)[0]>>4]+[o['palette_bank'] for o in records]
 for bank in banks:
  for j,c in enumerate(original[256+16*bank:272+16*bank]):
   red=c&31;green=c>>5&31;blue=c>>10&31;colors[256+16*bank+j]=red*13//16|((green*13//16)<<5)|(min(31,blue*14//16+1)<<10)
 payload=struct.pack('<512H',*colors);r.call('Weather_SetBlendCoeffs',4,16);frames=[]
 for f in range(360):
  for name in ['gPlttBufferUnfaded','gPlttBufferFaded']:r.write(r.symbols[name],payload)
  r.run()
  if f%6==0:frames.append(r.frame.copy())
 frames[0].save(D/'mgba-nuit-natif.png');frames[0].resize((960,640),Image.Resampling.NEAREST).save(D/'mgba-nuit-x4.png')
 frames[0].resize((720,480),Image.Resampling.NEAREST).save(D/'mgba-nuit.gif',save_all=True,append_images=[f.resize((720,480),Image.Resampling.NEAREST) for f in frames[1:]],duration=100,loop=0)
 for row in records:
  sp=r.symbols['gSprites']+68*row['sprite_id'];assert not r.read(sp+62,1)[0]&4
  assert r.read(sp+5,1)[0]>>4==row['palette_bank'];assert r.read(r.symbols['gPlttBufferUnfaded']+512+row['palette_bank']*32,32)==payload[512+row['palette_bank']*32:544+row['palette_bank']*32]
 result=dict(engine='mGBA libretro',rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_bytes=len(r.rom_buffer.raw)-1,scope='Real emulator frame capture after native LoadSpriteSheet/LoadSpritePalette/CreateSprite RAM fixtures. Not a montage. Static poses only, no NPC events, patrols, collisions or progression integration.',rom_unchanged=True,sprites=records,night_weather_palette=weatherbank,animated_fog=True)
finally:r.close()
(D/'TEST_MGBA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))

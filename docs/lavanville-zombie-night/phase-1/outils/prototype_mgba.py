#!/usr/bin/env python3
"""Prototype RAM ONLY, baseline ROM unmodified. No game source or save writes."""
import sys,os,json,hashlib,struct
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'tools/yokai'))
from mgba_new_game import new_game
from mafiamille_qa import MAPS,warp
P=Path(__file__).resolve().parents[1]/'prototypes';P.mkdir(exist_ok=True)
r=new_game();out={}
try:
 warp(r,*MAPS['LavenderTown'],14,11);r.frame.save(P/'mgba-lavanville-base.png');snap=r.snapshot()
 warp(r,*MAPS['Route8'],50,8);r.frame.save(P/'mgba-route8-temoin.png');ref=r.frame.copy();refpal=r.read(r.symbols['gPlttBufferUnfaded'],512);r.restore(snap)
 # Real engine fog, real native alpha blending. Prototype palettes in RAM.
 original=list(struct.unpack('<512H',r.read(r.symbols['gPlttBufferUnfaded'],1024)))
 r.call('SetNextWeather',6);r.run(200)
 bank=r.call('IndexOfSpritePaletteTag',0x1200);assert bank<16,bank
 native=list(struct.unpack('<512H',r.read(r.symbols['gPlttBufferUnfaded'],1024)))
 colors=[]
 for i,c in enumerate(original):
  red=c&31;green=(c>>5)&31;blue=(c>>10)&31
  # Short-lived demonstration; production must hook palette loads/fades.
  colors.append((red*9//16)|((green*9//16)<<5)|(min(31,blue*12//16+3)<<10))
 for j,c in enumerate(native[256+bank*16:272+bank*16]):
  v=max(c&31,(c>>5)&31,(c>>10)&31);colors[256+bank*16+j]=(v*5//16)|((v*12//16)<<5)|((v*7//16)<<10)
 payload=struct.pack('<512H',*colors);frames=[]
 r.call('Weather_SetBlendCoeffs',4,16)
 for f in range(480):
  for s in ['gPlttBufferUnfaded','gPlttBufferFaded']:r.write(r.symbols[s],payload)
  r.run()
  if f%6==0:frames.append(r.frame.copy())
 frames[0].save(P/'mgba-nuit-brume-ram.png')
 frames[0].resize((960,640),Image.Resampling.NEAREST).save(P/'mgba-nuit-brume-ram-x4.png')
 frames[0].save(P/'mgba-brume-ram.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
 fog_ids=[]
 for i in range(64):
  a=r.symbols['gSprites']+68*i
  if r.u32(a+28)==r.symbols['FogHorizontalSpriteCallback']|1:fog_ids.append(i)
 assert len(fog_ids)==20,fog_ids
 assert frames[0].tobytes()!=frames[-1].tobytes(),'Fog not moving'
 warp(r,*MAPS['Route8'],50,8);r.frame.save(P/'mgba-sortie-route8.png')
 restored=r.frame.tobytes()==ref.tobytes();palette_restored=r.read(r.symbols['gPlttBufferUnfaded'],512)==refpal;weather_after=r.call('GetCurrentWeather')
 # Capture actual ordinary battle as context for labelled ART MOCKUPS.
 r.call('CreateMon',r.symbols['gPlayerParty'],1,25,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.call('CreateMon',r.symbols['gEnemyParty'],9,25,31,1,100,0,0);r.write(r.symbols['gEnemyPartyCount'],b'\x01')
 r.call('StartScriptedWildBattle');r.run(500)
 for f in range(200):r.keys={8} if f%16<4 else set();r.run()
 r.keys=set();r.frame.save(P/'mgba-combat-contexte.png')
 enemy_id=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0];a=r.symbols['gSprites']+68*enemy_id+62;r.write(a,bytes([r.read(a,1)[0]|4]));r.run(3);r.frame.save(P/'mgba-combat-fond-fixture.png')
 out=dict(engine='mGBA libretro',rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_bytes=len(r.rom_buffer.raw)-1,fog_sprites=len(fog_ids),fog_obj_tiles_bytes=2048,weather_palette_bank=bank,animated_fog=True,route8_pixel_identical_to_control=restored,route8_bg_palette_identical_to_control=palette_restored,weather_after_exit=weather_after,scope='Native weather and palette RAM fixture, no installed chapter, no audio modification, no saved progression. Battle screenshot is unchanged ordinary battle context only.',limitations=['No first-entry script or patrol implemented','No public/private chapter build tested','Manual RAM palette tint does not prove production fade/menu/reload hooks','Route8 comparison includes possible NPC animation differences'])
finally:r.close()
(P/'TEST_PROTOTYPE_MGBA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out))

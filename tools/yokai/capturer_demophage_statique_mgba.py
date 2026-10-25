#!/usr/bin/env python3
"""Capture native mGBA: nouveaux objets temporaires, aucune scène d’aventure ajoutée."""
import hashlib,json,struct
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/demophage-statique-20261025';P.mkdir(exist_ok=True)
r=new_game();checks=[]
def passed(s):checks.append(s);print('PASS',s,flush=True)
def sprite(obj):return r.symbols['gSprites']+68*r.read(obj+4,1)[0]
def tiles(obj):return r.read(0x06010000+(int.from_bytes(r.read(sprite(obj)+4,2),'little')&1023)*32,512)
def bounds(obj):
 s=sprite(obj);x,y,x2,y2=struct.unpack('<hhhh',r.read(s+32,8));cx,cy=struct.unpack('<bb',r.read(s+40,2));ox=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetX'],2))[0];oy=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetY'],2))[0]
 return x+x2+ox+cx,y+y2+oy+cy
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],150,85,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());g,n=next((i,groups[key].index('PalletTown')) for i,key in enumerate(groups['group_order']) if 'PalletTown' in groups[key])
 r.call('SetWarpDestination',g,n,255,9,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(400);r.call('LockPlayerFieldControls')
 def spawn(gfx,local,x,y):
  index=r.call('SpawnSpecialObjectEventParameterized',gfx,8,local,x+7,y+7,3);assert index<16
  return r.symbols['gObjectEvents']+36*index
 dem=spawn(188,200,7,16);oni=spawn(182,201,11,16);r.run(30)
 source=(ROOT/'graphics/yokai_characters/demophage_statique/overworld.4bpp').read_bytes();assert len(source)==512
 assert r.read(r.symbols['gObjectEventPic_DemophageStatique'],512)==source and tiles(dem)==source
 passed('Cellule statique 32×32 liée à la ROM et réellement chargée dans la VRAM de Démophage')
 dbank=int.from_bytes(r.read(sprite(dem)+4,2),'little')>>12;obank=int.from_bytes(r.read(sprite(oni)+4,2),'little')>>12;assert dbank!=obank
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+dbank*32,32)==r.read(r.symbols['gObjectEventPal_DemophageStatique'],32)
 passed('Palette propre de Démophage chargée, distincte de celle de Gargaros')
 x,y=bounds(dem);assert 0<=x<=208 and 0<=y<=128
 assert not r.read(sprite(dem)+62,1)[0]&4
 rgb=r.frame.crop((x,y,x+32,y+32));gold=sum(1 for red,green,blue in rgb.get_flattened_data() if red>160 and green>90 and blue<120);assert gold>=100,gold
 passed(f'Démophage entièrement visible à l’écran, avec {gold} pixels dorés dans la vraie capture')
 pos=r.read(dem+16,4);image=tiles(dem)
 for frame in range(120):
  r.run();assert r.read(dem+16,4)==pos and tiles(dem)==image
 passed('Pose de face et position immobiles pendant 120 frames natives')
 r.frame.save(P/'demophage-en-jeu.png');r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/'demophage-en-jeu-x3.png')
 (P/'TESTS.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':checks,'scene':'Bourg Palette, Démophage à gauche, Nathan au centre, Gargaros à droite','demophage_screen_bounds':[x,y,x+32,y+32]},ensure_ascii=False,indent=2)+'\n')
finally:r.close()

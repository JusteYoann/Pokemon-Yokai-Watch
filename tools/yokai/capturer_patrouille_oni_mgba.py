#!/usr/bin/env python3
"""Native four-direction facing preview with one temporary map actor.
Prepared new game/map, no story event or user save modified. Screens are mGBA
frames; the only image processing is nearest-neighbor enlargement / GIF encoding.
"""
import json,hashlib,struct
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/patrouille-oni-20261024/public';P.mkdir(exist_ok=True)
r=new_game();movie=[];checks=[];shots=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 g,n=maps['PalletTown'];r.call('SetWarpDestination',g,n,255,9,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(400)
 r.call('LockPlayerFieldControls');idx=r.call('SpawnSpecialObjectEventParameterized',183,8,200,7+7,16+7,3);assert idx<16
 obj=r.symbols['gObjectEvents']+36*idx;r.run(30);sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
 raw=(ROOT/'graphics/yokai_characters/patrouille_oni/overworld.4bpp').read_bytes();assert len(raw)==2048
 reference=Image.open(ROOT/'graphics/yokai_characters/nathan/normal.png').convert('RGBA').crop((0,0,16,32)).getbbox()
 patrol=Image.open(ROOT/'graphics/yokai_characters/patrouille_oni/overworld.png').convert('RGBA')
 for i in range(4):
  bounds=patrol.crop((i*32,0,i*32+32,32)).getbbox()
  assert bounds[1]==reference[1] and bounds[3]==reference[3],(i,bounds,reference)
 checks.append(dict(test='Four poses match Nathan visible height and baseline',height=reference[3]-reference[1],baseline=reference[3],passed=True))
 assert r.read(r.symbols['gObjectEventPic_PatrouilleOni'],2048)==raw
 bank=int.from_bytes(r.read(sprite+4,2),'little')>>12
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_PatrouilleOni'],32)
 for direction,name in enumerate(('face','dos','gauche','droite')):
  r.call('ObjectEventClearHeldMovementIfActive',obj);assert r.call('ObjectEventSetHeldMovement',obj,direction)==0;r.run(16)
  for sample in range(15):
   r.run(6)
   assert not r.read(obj+1,1)[0]&0x60
   x,y,x2,y2=struct.unpack('<hhhh',r.read(sprite+32,8));cx,cy=struct.unpack('<bb',r.read(sprite+40,2))
   ox=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetX'],2))[0];oy=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetY'],2))[0]
   left,top=x+x2+ox+cx,y+y2+oy+cy;assert 0<=left<=208 and 0<=top<=128
   tile=int.from_bytes(r.read(sprite+4,2),'little')&1023
   assert r.read(0x06010000+tile*32,512)==raw[512*direction:512*(direction+1)], (name,sample,r.read(sprite+42,1)[0],r.read(obj+24,1)[0],[i for i in range(4) if r.read(0x06010000+tile*32,512)==raw[i*512:(i+1)*512]])
   im=r.frame.copy();purple=sum(1 for red,green,blue in im.crop((left,top,left+32,top+32)).get_flattened_data() if blue>red*1.1 and red>40 and blue>green*1.1)
   assert purple>=25,(name,'Patrol not visible',purple)
   movie.append(im)
  r.frame.save(P/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(name+'-x3.png'));shots.append(r.frame.copy())
  checks.append(dict(direction=name,native_frame=direction,visible_screen_rectangle=[left,top,left+32,top+32],samples=15,passed=True))
 for scale,name in [(1,'quatre-directions-mgba.gif'),(3,'quatre-directions-mgba-x3.gif')]:
  frames=movie if scale==1 else [im.resize((720,480),Image.Resampling.NEAREST) for im in movie]
  frames[0].save(P/name,save_all=True,append_images=frames[1:],duration=100,loop=0)
 (P/'TEST.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),captured_frames=len(movie),checks=checks),ensure_ascii=False,indent=2)+'\n')
 print('PASS four native directions, loaded palette, 60 visible captured frames',flush=True)
finally:r.frame.save(P/'dernier.png');r.close()

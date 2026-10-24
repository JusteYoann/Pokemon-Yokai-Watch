#!/usr/bin/env python3
"""Temporary mGBA actors on a real map; native tile movement and VRAM frames.
No map event, story, player save or ROM distribution is added by this fixture.
"""
import json,hashlib,os,struct
from pathlib import Path
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/gargaros-marche-20261024'/os.environ.get('GARGAROS_MODE','public');P.mkdir(parents=True,exist_ok=True)
r=new_game();movie=[];checks=[];visible_positions=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
def spawn(gfx,local,x,y):
 i=r.call('SpawnSpecialObjectEventParameterized',gfx,8,local,x+7,y+7,3);assert i<16
 return r.symbols['gObjectEvents']+36*i

def shot(name):
 r.frame.save(P/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(name+'-x3.png'))
def coords(obj):return struct.unpack('<hh',r.read(obj+16,4))

def capture_visible():
 # Object coordinates alone do not prove that the actor is in the recording.
 assert not (r.read(obj+1,1)[0]&0x60), 'Gargaros is invisible or outside the viewport'
 x,y,x2,y2=struct.unpack('<hhhh',r.read(sprite+32,8))
 cx,cy=struct.unpack('<bb',r.read(sprite+40,2))
 ox=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetX'],2))[0]
 oy=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetY'],2))[0]
 left,top=x+x2+ox+cx,y+y2+oy+cy
 assert 0<=left<=208 and 0<=top<=128,('Sprite clipped',left,top)
 image=r.frame.copy()
 reds=sum(1 for red,green,blue in image.crop((left,top,left+32,top+32)).get_flattened_data() if red>100 and green<80 and blue<100 and red>green*2)
 assert reds>=15,('No visible red Gargaros pixels',left,top,reds)
 visible_positions.append((left,top));movie.append(image)

try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 g,n=maps['PalletTown'];r.call('SetWarpDestination',g,n,255,9,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(400)
 r.call('LockPlayerFieldControls');obj=spawn(182,200,7,16);ref=spawn(179,201,11,16);r.run(30);shot('comparaison-orqanos-nathan')
 sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
 source=(ROOT/'graphics/yokai_characters/gargaros/overworld.4bpp').read_bytes();frames=[source[i*512:(i+1)*512] for i in range(12)];assert len(source)==6144
 assert r.read(r.symbols['gObjectEventPic_YokaiGargaros'],6144)==source
 bank=int.from_bytes(r.read(sprite+4,2),'little')>>12;refSprite=r.symbols['gSprites']+68*r.read(ref+4,1)[0];refbank=int.from_bytes(r.read(refSprite+4,2),'little')>>12
 assert bank!=refbank
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_YokaiGargaros'],32)
 checks.append(dict(test='independent palettes and all twelve linked frames',passed=True))
 r.call('MoveObjectEventToMapCoords',obj,7+7,13+7);r.run(12)
 for _ in range(30):r.run();capture_visible()
 # The rectangle consists of real one-tile walks, not animation in place.
 for label,direction,steps,delta,expected in [('droite',3,4,(1,0),{9,10,11}),('face',0,2,(0,1),{0,1,2}),('gauche',2,4,(-1,0),{6,7,8}),('dos',1,2,(0,-1),{3,4,5})]:
  seen=set()
  for step in range(steps):
   r.call('ObjectEventClearHeldMovementIfActive',obj);before=coords(obj)
   assert r.call('ObjectEventSetHeldMovement',obj,0x10+direction)==0
   for t in range(80):
    r.run();tile=int.from_bytes(r.read(sprite+4,2),'little')&1023;vram=r.read(0x06010000+tile*32,512)
    # Initial DMA still contains the previous facing at a turn. Check the
    # new animation after its tile transfer; preserve every captured video frame.
    if t>=2:seen.update(i for i,frame in enumerate(frames) if frame==vram)
    if t%2==0:capture_visible()
    if r.read(obj,1)[0]&128:break
   else:raise AssertionError(('Walk did not finish',label,coords(obj)))
   assert coords(obj)==(before[0]+delta[0],before[1]+delta[1]),(label,before,coords(obj))
  shot(label);assert expected<=seen,(label,expected,seen)
  assert seen<=expected,(label,'wrong-facing frame',seen)
  checks.append(dict(direction=label,steps=steps,observed_frames=sorted(seen),passed=True))
 for _ in range(30):r.run();capture_visible()
 checks.append(dict(test='Every captured frame shows Gargaros fully on screen with red sprite pixels; at least 48 native pixels of travel',frames=len(visible_positions),screen_bounds=[min(x for x,y in visible_positions),min(y for x,y in visible_positions),max(x for x,y in visible_positions),max(y for x,y in visible_positions)],passed=True))
 assert max(x for x,y in visible_positions)-min(x for x,y in visible_positions)>=48
 # Actual captured emulator frames, encoded without interpolated movement.
 for scale,name in [(1,'marche-mgba.gif'),(3,'marche-mgba-x3.gif')]:
  pictures=movie if scale==1 else [im.resize((720,480),Image.Resampling.NEAREST) for im in movie]
  pictures[0].save(P/name,save_all=True,append_images=pictures[1:],duration=33,loop=0)
 (P/'TEST.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks,captured_frames=len(movie)),ensure_ascii=False,indent=2)+'\n')
 print('PASS native walking in four directions;',len(movie),'captured frames',flush=True)
finally:r.frame.save(P/'dernier.png');r.close()

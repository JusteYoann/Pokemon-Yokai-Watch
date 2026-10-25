#!/usr/bin/env python3
"""GIF d'images mGBA réelles : acteur temporaire, marche native sur les quatre axes.
Maître Nyada sert de référence de taille. Aucun événement permanent n'est ajouté.
"""
import hashlib,json,struct
from pathlib import Path
from PIL import Image
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/'docs/requin-lunettes-overworld-20261025';D.mkdir(exist_ok=True)
q=QA('TEMP.json');r=q.r;movie=[];checks=[];spans=[]
try:
 q.mon();q.warp('PalletTown',10,10);r.run(300);r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents')
 def spawn(gfx,local,x,y):
  i=r.call('SpawnSpecialObjectEventParameterized',gfx,8,local,x+7,y+7,3);assert i<16;return r.symbols['gObjectEvents']+36*i
 obj=spawn(189,200,5,10);ref=spawn(180,201,12,10);r.run(30)
 sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
 source=(ROOT/'graphics/yokai_characters/requin_lunettes/overworld.4bpp').read_bytes();assert len(source)==9*512
 assert all(sum(v!=0 for v in source[i*512:(i+1)*512])>70 for i in range(9))
 frames=[source[i*512:(i+1)*512] for i in range(9)]
 def coords(a):return tuple(v-7 for v in struct.unpack('<hh',r.read(a+16,4)))
 def capture(span=2):
  assert not(r.read(obj+1,1)[0]&0x60),'Requin invisible/hors écran'
  bank=r.read(sprite+5,1)[0]>>4
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_RequinLunettes'],32)
  x,y,x2,y2=struct.unpack('<hhhh',r.read(sprite+32,8));cx,cy=struct.unpack('<bb',r.read(sprite+40,2))
  ox,oy=struct.unpack('<hh',r.read(r.symbols['gSpriteCoordOffsetX'],4));left=x+x2+ox+cx;top=y+y2+oy+cy
  assert 0<=left<=208 and 0<=top<=128,('Sprite coupé',left,top)
  crop=r.frame.crop((left,top,left+32,top+32));assert sum(1 for red,green,blue in crop.get_flattened_data() if blue>red+25 and blue>green+8)>=12,'Sprite non visible dans le GIF'
  movie.append(r.frame.copy());spans.append(span)
 refbank=r.read(r.symbols['gSprites']+68*r.read(ref+4,1)[0]+5,1)[0]>>4
 assert refbank!=(r.read(sprite+5,1)[0]>>4)
 r.frame.save(D/'comparaison-nyada.png')
 for _ in range(30):r.run(2);capture()
 for label,d,steps,delta,expected in [('dos',1,2,(0,-1),{3,4,5}),('droite',3,3,(1,0),{6,7,8}),('face',0,2,(0,1),{0,1,2}),('gauche',2,3,(-1,0),{6,7,8})]:
  seen=set()
  for _ in range(steps):
   before=coords(obj)
   assert r.call('MapGridGetCollisionAt',before[0]+delta[0]+7,before[1]+delta[1]+7)==0
   r.call('ObjectEventClearHeldMovementIfActive',obj);assert r.call('ObjectEventSetHeldMovement',obj,0x10+d)==0
   for t in range(90):
    r.run();tile=int.from_bytes(r.read(sprite+4,2),'little')&1023;raw=r.read(0x06010000+32*tile,512)
    found={i for i,f in enumerate(frames) if f==raw}
    seen.update(found&expected)
    if t>=2:
     assert found and found<=expected,(label,found)
     flip=bool(int.from_bytes(r.read(sprite+2,2),'little')&0x1000);assert flip==(d==3),(label,'miroir',flip)
    capture(1)
    if r.read(obj,1)[0]&128:break
   else:raise AssertionError(('Mouvement bloqué',label))
   assert coords(obj)==(before[0]+delta[0],before[1]+delta[1])
  assert expected<=seen,(label,seen)
  r.frame.save(D/(label+'.png'));checks.append(dict(direction=label,steps=steps,frames_seen=sorted(seen),right_is_hardware_mirror_of_left=d==3))
  for _ in range(18):r.run(2);capture()
 bbox=Image.open(ROOT/'graphics/dossier-20261023/nyada/overworld.png').convert('RGBA').getchannel('A').getbbox()
 sheet=Image.open(ROOT/'graphics/yokai_characters/requin_lunettes/overworld.png').convert('RGBA')
 for i in range(9):
  b=sheet.crop((i*32,0,i*32+32,32)).getchannel('A').getbbox();assert b[3]-b[1]==bbox[3]-bbox[1] and b[3]==bbox[3]
 fps=16777216/280896;durations=[];elapsed=0
 for span in spans:
  durations.append((round((elapsed+span)/fps*100)-round(elapsed/fps*100))*10);elapsed+=span
 for scale,name in [(1,'quatre-directions-mgba.gif'),(3,'quatre-directions-mgba-x3.gif')]:
  pics=movie if scale==1 else [im.resize((720,480),Image.Resampling.NEAREST) for im in movie]
  pics[0].save(D/name,save_all=True,append_images=pics[1:],duration=durations,loop=0,disposal=2)
 (D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),temporary_graphics_id=189,height_native_pixels=bbox[3]-bbox[1],same_height_and_baseline_as_nyada=True,glasses_on_both_eyes=True,right_exact_hardware_mirror=True,distinct_palette_from_nyada=True,frames_recorded=len(movie),directions=checks),ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(movie),'images natives, 4 directions, 9 poses et miroir droit',flush=True)
finally:r.close()

#!/usr/bin/env python3
"""Native ObjectEvent + FRLG anim/movement RAM fixture; no production ROM or map edits.
Uses existing32x32 nine-frame object template172 only as a test shell; replaces instance images/palette in RAM.
"""
from pathlib import Path
import os,sys,struct,json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'tools/yokai'))
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp
D=R/'graphics/yokai_zombies/errant';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/zombie-marche';Q.mkdir(exist_ok=True)
r=new_game();poses=[];steps=[];movie=[];result={}
try:
 warp(r,*MAPS['LavenderTown'],15,8)
 oid=r.call('SpawnSpecialObjectEventParameterized',172,C['MOVEMENT_TYPE_FACE_DOWN'],200,13+7,8+7,3);assert oid<16
 obj=r.symbols['gObjectEvents']+36*oid;sid=r.read(obj+4,1)[0];sp=r.symbols['gSprites']+68*sid;bank=r.read(sp+5,1)[0]>>4
 mem=r.call('AllocZeroed',4800);assert mem
 data=(D/'overworld.4bpp').read_bytes();pal=(D/'overworld.gbapal').read_bytes();assert len(data)==4608
 r.write(mem,data);table=mem+4608
 for i in range(9):r.write(table+8*i,struct.pack('<IHH',mem+512*i,512,0))
 r.write(mem+4680,pal);r.w32(sp+12,table);r.call('LoadPalette',mem+4680,256+16*bank,32)
 # Four standing directions must select the native frames and right-hand flip.
 for d,(direction,label) in enumerate([(1,'face'),(2,'dos'),(3,'gauche'),(4,'droite')]):
  r.call('ObjectEventTurn',obj,direction);r.call('StartSpriteAnim',sp,d);r.run(8)
  assert r.u32(sp+12)==table and not r.read(sp+62,1)[0]&4
  flip=bool(struct.unpack('<H',r.read(sp+2,2))[0]&0x1000);assert flip==(direction==4),(label,flip)
  r.frame.save(Q/f'mgba-{label}-natif.png');r.frame.resize((720,480),Image.Resampling.NEAREST).save(Q/f'mgba-{label}-x3.png')
  poses.append(dict(direction=label,anim_id=d,right_hflip=flip,image_table_in_ram=True))
 # Real held movement translates one map tile per action, around a clear square.
 expected=[(14,8),(14,9),(13,9),(13,8)];actions=['MOVEMENT_ACTION_WALK_NORMAL_RIGHT','MOVEMENT_ACTION_WALK_NORMAL_DOWN','MOVEMENT_ACTION_WALK_NORMAL_LEFT','MOVEMENT_ACTION_WALK_NORMAL_UP']
 for cycle in range(3):
  for action,goal in zip(actions,expected):
   r.call('ObjectEventSetHeldMovement',obj,C[action]);frame_ids=set()
   for f in range(36):
    r.run()
    # The native sprite image commands reference only the nine exported frames.
    anim=r.read(sp+42,1)[0];cmd=r.read(sp+43,1)[0]
    if f%2==0:movie.append(r.frame.copy())
    frame_ids.add((anim,cmd))
   r.call('ObjectEventClearHeldMovementIfFinished',obj)
   xy=struct.unpack('<hh',r.read(obj+16,4));actual=(xy[0]-7,xy[1]-7);assert actual==goal,(action,actual,goal)
   assert r.u32(sp+12)==table,'Image table reset during native movement'
   assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==pal,'Palette clobbered'
   steps.append(dict(cycle=cycle,action=action,arrived=list(actual),anim_commands=sorted(frame_ids),passed=True))
 movie[0].resize((720,480),Image.Resampling.NEAREST).save(Q/'marche-reelle-mgba.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in movie[1:]],duration=34,loop=0)
 board=Image.new('RGB',(480,320))
 for i,label in enumerate(['face','dos','gauche','droite']):board.paste(Image.open(Q/f'mgba-{label}-natif.png'),(240*(i%2),160*(i//2)))
 board.resize((960,640),Image.Resampling.NEAREST).save(Q/'quatre-directions-mgba-x2.png')
 result=dict(passed=True,engine='mGBA libretro',rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_unchanged=True,object_template_id=172,custom_images_bytes=len(data),palette_bank=bank,native_held_walk_steps=len(steps),orientations=poses,steps=steps,scope=__doc__,limits=['Temporary object images in RAM, no permanent gfxID registration','No patrol/detection/collision policy or repeated zombie battles integrated','Movement test uses existing native object engine and visible source-art candidates'])
finally:r.close()
(Q/'TEST_MGBA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))

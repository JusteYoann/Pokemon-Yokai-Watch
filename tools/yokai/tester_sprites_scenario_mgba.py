#!/usr/bin/env python3
"""Native map rendering, nine-frame gait and trainer portrait resource checks.

Temporary object fixtures, not story events or full trainer battles.
"""
import hashlib,json,re
from pathlib import Path
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
OUT=ROOT/'QA_RECETTE_FINALE/SPRITES_SCENARIO_2026';OUT.mkdir(exist_ok=True)
C={k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)\b','\n'.join((ROOT/f'include/constants/{n}.h').read_text() for n in ['event_objects','event_object_movement','trainers']),re.M)}
spec=json.loads((ROOT/'graphics/yokai_characters/scenario_2026/manifest.json').read_text())
actors=[a for a in spec['characters'] if 'graphics_id' in a]+spec.get('adapted_existing',[])
r=new_game();results=[];passed=False
try:
 r.call('VarSet',0x4050,3);r.call('VarSet',0x4055,9)
 r.call('SetWarpDestination',3,0,255,8,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 base=r.snapshot()
 for actor in actors:
  name=actor['id'];r.restore(base)
  oid=r.call('SpawnSpecialObjectEventParameterized',actor['graphics_id'],C['MOVEMENT_TYPE_FACE_DOWN'],200,16,23,3);assert oid<16,(name,oid)
  obj=r.symbols['gObjectEvents']+36*oid;sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
  assert r.read(obj+5,1)[0]==actor['graphics_id']
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+10*32,32)==r.read(r.symbols[actor.get('map_palette_symbol','gObjectEventPal_Scenario')],32)
  trainer=r.call('CreateTrainerPicSprite',actor['trainer_pic_id'],1,206,60,6,0xffff);assert trainer<64,(name,trainer)
  r.run(30);frames=[]
  for direction,label in [(1,'SOUTH'),(2,'NORTH'),(3,'WEST'),(4,'EAST')]:
   r.call('ObjectEventTurn',obj,direction);r.run(30)
   assert r.read(sprite+62,1)[0]&1 and not r.read(sprite+62,1)[0]&4
   assert bool(int.from_bytes(r.read(sprite+2,2),'little')&0x1000)==(direction==4)
   frames.append(r.frame.copy())
  contact=Image.new('RGB',(960,180),(224,224,224));d=ImageDraw.Draw(contact)
  for i,im in enumerate(frames):d.text((240*i+4,2),name+' '+['S','N','W','E'][i],fill='black');contact.paste(im,(240*i,20))
  contact.save(OUT/(name+'-natif.png'))
  # The stationary NPC movement callback otherwise restores its idle pose.
  r.w32(sprite+0x1C,r.symbols['SpriteCallbackDummy']|1)
  movies=[]
  for label in ['SOUTH','NORTH','WEST','EAST']:
   r.call('StartSpriteAnim',sprite,C['ANIM_STD_GO_'+label]);r.write(sprite+44,bytes([r.read(sprite+44,1)[0]&~0x40]));seen=set()
   for f in range(40):
    r.run();seen.add(r.read(sprite+43,1)[0])
    if label=='WEST' and f%4==0:movies.append(r.frame.copy())
   assert len(seen)>=3,(name,label,seen)
  movies[0].save(OUT/(name+'-marche.gif'),save_all=True,append_images=movies[1:],duration=67,loop=0)
  png=Image.open(ROOT/f'graphics/yokai_characters/{name}/overworld.png')
  w=actor.get('frame_width',16)
  assert png.mode=='P' and png.size==(w*9,32) and png.info['transparency']==0
  assert max(png.get_flattened_data())<=15
  # Every source frame has the same visible bounding rectangle as Red.
  red=Image.open(ROOT/'graphics/object_events/pics/people/red_normal.png').convert('RGBA')
  for i in range(9):
   actual=png.crop((w*i,0,w*(i+1),32)).getbbox();target=red.crop((16*i,0,16*(i+1),32)).getchannel('A').getbbox()
   if w==32:target=(0,target[1],32,target[3])
   assert actual and actual[0]>=target[0] and actual[1]>=target[1] and actual[2]<=target[2] and actual[3]<=target[3],(name,i,actual,target)
   assert actual[3]-actual[1]>=17,(name,i,actual)
  results.append({'actor':name,'passed':True,'facings':4,'native_gait_directions':4,'trainer_sprite_loaded':True,'native_bounds_within_red':True})
  print('PASS',name,flush=True)
 passed=True
finally:
 r.close();(OUT/'TEST_MGBA.json').write_text(json.dumps({'passed':passed,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Real intro, fixture warp, temporary map objects and trainer portrait viewer; four facings, animation cycles, palette and native Red bounding boxes. Not story placement, battle victory or artistic approval. All new map characters share one palette; pre-existing special NPC banks require scene palette planning.','results':results},ensure_ascii=False,indent=2)+'\n')

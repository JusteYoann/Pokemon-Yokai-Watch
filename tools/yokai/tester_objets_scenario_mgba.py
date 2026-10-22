#!/usr/bin/env python3
"""Native animated object fixtures and byte-level checks of 128px boss masters."""
import hashlib,json,re
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
OUT=ROOT/'QA_RECETTE_FINALE/SPRITES_SCENARIO_2026'
C={k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)\b','\n'.join((ROOT/f'include/constants/{n}.h').read_text() for n in ['event_objects','event_object_movement']),re.M)}
def unlz(data):
 assert data[0]==0x10
 length=int.from_bytes(data[1:4],'little');out=bytearray();i=4
 while len(out)<length:
  flags=data[i];i+=1
  for bit in range(7,-1,-1):
   if len(out)>=length:break
   if flags&(1<<bit):
    a,b=data[i:i+2];i+=2;n=(a>>4)+3;offset=((a&15)<<8)+b+1
    for _ in range(n):out.append(out[-offset])
   else:out.append(data[i]);i+=1
 return bytes(out[:length])
r=new_game();results=[];passed=False
try:
 r.call('VarSet',0x4050,3);r.call('VarSet',0x4055,9)
 r.call('SetWarpDestination',3,0,255,8,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600);base=r.snapshot()
 for name,count in [('bingo_kai',5),('capsule_souhait',1),('triptic_tac',5)]:
  r.restore(base)
  oid=r.call('SpawnSpecialObjectEventParameterized',C['OBJ_EVENT_GFX_SCENARIO_'+name.upper()],C['MOVEMENT_TYPE_FACE_DOWN'],200,16,23,3);assert oid<16
  obj=r.symbols['gObjectEvents']+36*oid;sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
  r.run(60);r.frame.save(OUT/(name+'-natif.png'))
  r.w32(sprite+0x1c,r.symbols['SpriteCallbackDummy']|1)
  r.call('StartSpriteAnim',sprite,4);r.write(sprite+44,bytes([r.read(sprite+44,1)[0]&~0x40]));seen=set();movie=[]
  for f in range(64):
   r.run();seen.add(r.read(sprite+43,1)[0])
   if f%4==0:movie.append(r.frame.copy())
  assert len(seen)>=count,(name,seen)
  movie[0].save(OUT/(name+'-animation.gif'),save_all=True,append_images=movie[1:],duration=67,loop=0)
  results.append({'object':name,'native_render':True,'native_action_animation':True,'passed':True})
 for name,symbol in [('soranaki_phase1','gScenarioBossPicSoranakiPhase1'),('soranaki_phase2','gScenarioBossPicSoranakiPhase2')]:
  assert unlz(r.read(r.symbols[symbol],10000))==(ROOT/f'graphics/yokai_characters/{name}/battle_large.4bpp').read_bytes()
  results.append({'boss':name,'master_size':[128,128],'compressed_rom_bytes_match_native_resource':True,'passed':True,'scope':'Resource linked and decompression verified; exceptional boss battle renderer/gameplay not implemented here'})
 passed=True
finally:
 r.close();(OUT/'TEST_OBJETS_MGBA.json').write_text(json.dumps({'passed':passed,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Temporary object spawning and native animation playback; not story events or Soranaki gameplay.','results':results},ensure_ascii=False,indent=2)+'\n')
print('PASS three animated objects and two linked 128px boss masters')

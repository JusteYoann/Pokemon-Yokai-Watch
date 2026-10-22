#!/usr/bin/env python3
"""Native compiled NPC graphics in a test-only Route 1 lineup; not story integration."""
import hashlib,json,os
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from mgba_rpc import ROOT
from mgba_new_game import new_game
from scenario_qa_helpers import warp
OUT=ROOT/os.environ.get('YOKAI_TRACE_REPORT','QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/DECALQUES_NATHAN')
OUT.mkdir(parents=True,exist_ok=True)
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={name:(i,j) for i,g in enumerate(groups['group_order']) for j,name in enumerate(groups[g])}
actors=[('laure','YokaiLaure',174),('marge','YokaiMarge',175),('agent_x','YokaiAgentX',176)]
donor=np.array(Image.open(ROOT/'graphics/yokai_characters/nathan/normal.png'))
r=new_game(0);results=[]
try:
 warp(r,*maps['Route1'],6,12);r.call('LockPlayerFieldControls')
 player=r.symbols['gObjectEvents']+36*r.read(r.symbols['gPlayerAvatar']+5,1)[0]
 spawned=[]
 for n,(name,sym,gfx) in enumerate(actors):
  idx=r.call('SpawnSpecialObjectEventParameterized',gfx,0,220+n,8+2*n+7,12+7,3);assert idx<16
  obj=r.symbols['gObjectEvents']+36*idx;sp=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
  p=ROOT/f'graphics/yokai_characters/{name}/overworld.png';im=Image.open(p)
  assert im.mode=='P' and im.size==(144,32) and im.info['transparency']==0
  assert max(im.tobytes())<16
  a=np.array(im);assert np.array_equal(a[24:]>0,donor[24:]>0)
  data=(p.with_suffix('.4bpp')).read_bytes();assert len(data)==2304
  assert r.read(r.symbols['gObjectEventPic_'+sym],2304)==data
  frames=[data[i*256:(i+1)*256] for i in range(9)]
  spawned.append((name,obj,sp,frames,im));results.append(dict(actor=name,native_frame_size=[16,32],frames=9,body_hands_feet_masks_match_nathan=True,rom_graphics_verified=True))
 r.run(60)
 directions=[]
 for direction,label,expected in [(1,'face',{0,3,4}),(2,'dos',{1,5,6}),(3,'gauche',{2,7,8}),(4,'droite',{2,7,8})]:
  for obj in [player]+[v[1] for v in spawned]:
   r.call('ObjectEventClearHeldMovementIfFinished',obj);r.call('ObjectEventTurn',obj,direction)
  r.run(30);r.frame.save(OUT/f'{label}-mgba.png')
  if direction==1:
   cap=r.frame.copy();cap.resize((960,640),Image.Resampling.NEAREST).save(OUT/'comparaison-nathan-x4.png')
   board=Image.new('RGB',(960,720),(232,232,232));board.paste(cap.resize((960,640),Image.Resampling.NEAREST),(0,0));d=ImageDraw.Draw(board)
   font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
   for x,name in [(480,'Nathan'),(608,'Laure'),(736,'Marge'),(864,'Agent X')]:d.text((x,653),name,fill='black',font=font,anchor='mt')
   d.text((16,688),'Capture mGBA ×4 — ressources compilées, scène de test temporaire.',fill='black',font=font)
   board.save(OUT/'comparaison-annotee-x4.png')
  # All three share one deliberate palette; loading one must not recolor peers.
  for name,obj,sp,frames,im in spawned:
   attr=int.from_bytes(r.read(sp+4,2),'little');bank=attr>>12
   pal=im.getpalette();hardware=r.read(0x05000200+bank*32,32)
   for c in set(im.tobytes())-{0}:
    red,green,blue=pal[3*c:3*c+3];v=(red>>3)|((green>>3)<<5)|((blue>>3)<<10)
    assert int.from_bytes(hardware[c*2:c*2+2],'little')==v,(name,label,'palette',c)
   assert bool(int.from_bytes(r.read(sp+2,2),'little')&0x1000)==(direction==4),(name,label,'flip')
  seen={name:set() for name,*_ in spawned};movie=[]
  for repeat in range(4):
   for obj in [player]+[v[1] for v in spawned]:
    r.call('ObjectEventClearHeldMovementIfFinished',obj);r.call('ObjectEventSetHeldMovement',obj,0x24+direction)
   for f in range(40):
    r.run()
    for name,obj,sp,frames,im in spawned:
     attr=int.from_bytes(r.read(sp+4,2),'little');tile=attr&1023;data=r.read(0x06010000+tile*32,256)
     seen[name].update(i for i,pic in enumerate(frames) if data==pic)
    if f%4==0:movie.append(r.frame.copy())
  for name,observed in seen.items():assert expected<=observed,(name,label,observed,expected)
  movie[0].save(OUT/f'marche-{label}.gif',save_all=True,append_images=movie[1:],duration=67,loop=0)
  directions.append(dict(direction=label,expected=sorted(expected),observed={name:sorted(v) for name,v in seen.items()},palette_verified_for_all=True,east_flip_verified=True))
 report=dict(passed=True,engine='mGBA libretro',scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_bytes=len(r.rom_buffer.raw)-1,rom_not_runtime_patched=True,actors=results,directions=directions,limitations=['Temporary spawned test actors, no new story placement','Artistic likeness is not approved by technical tests','No trainer portraits or battles created in this lot'])
 (OUT/'CONTROLE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
finally:r.close()

#!/usr/bin/env python3
"""Real native held movement; temporary RAM graphics, no ROM/save changes."""
from pathlib import Path
import os,sys,struct,json,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'tools/yokai'))
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp
D=R/'graphics/alyzon_bie/calque-pnj';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-calque-pnj';Q.mkdir(exist_ok=True)
g=json.loads((D/'CONSTRUCTION.json').read_text());pal=b''.join(struct.pack('<H',(v[0]//8)|((v[1]//8)<<5)|((v[2]//8)<<10)) for v in g['palette_rgb555'])
def tiles(im):
 out=bytearray()
 for ty in range(4):
  for tx in range(4):
   for y in range(8):
    for x in range(0,8,2):out.append(im.getpixel((tx*8+x,ty*8+y))|im.getpixel((tx*8+x+1,ty*8+y))<<4)
 return bytes(out)
def frame(d,p):
 im=Image.open(D/f'{d}-{["repos","pas-1","pas-2"][p]}.png')
 canvas=Image.new('P',(32,32),0);canvas.putpalette(im.getpalette());canvas.info['transparency']=0;canvas.paste(im,(8,0));return canvas
r=new_game();reports=[];clips=[]
try:
 warp(r,*MAPS['LavenderTown'],15,10)
 oid=r.call('SpawnSpecialObjectEventParameterized',172,C['MOVEMENT_TYPE_FACE_UP'],200,13+7,8+7,3);assert oid<16
 obj=r.symbols['gObjectEvents']+36*oid;sid=r.read(obj+4,1)[0];sp=r.symbols['gSprites']+68*sid;bank=r.read(sp+5,1)[0]>>4
 mem=r.call('AllocZeroed',4800);assert mem;table=mem+4608
 for i in range(9):r.write(table+8*i,struct.pack('<IHH',mem+512*i,512,0))
 r.write(mem+4680,pal);r.w32(sp+12,table);r.call('LoadPalette',mem+4680,256+16*bank,32)
 initial=r.snapshot()
 for label,direction,anim,action,delta in [('face',1,0,'MOVEMENT_ACTION_WALK_NORMAL_DOWN',(0,1)),('gauche',3,2,'MOVEMENT_ACTION_WALK_NORMAL_LEFT',(-1,0)),('dos',2,1,'MOVEMENT_ACTION_WALK_NORMAL_UP',(0,-1)),('droite',4,3,'MOVEMENT_ACTION_WALK_NORMAL_RIGHT',(1,0))]:
  r.restore(initial)
  # Standard FRLG shares left/right images through hardware hFlip. This fixture
  # supplies the appropriate asymmetric profile before each separate test clip.
  side=[frame(label if label in ('gauche','droite') else 'gauche',p) for p in range(3)]
  if label=='droite':side=[ImageOps.mirror(im) for im in side]
  back=[frame('dos',p) for p in range(3)]
  front=[frame('face',p) for p in range(3)]
  imgs=[front[0],back[0],side[0],front[1],front[2],back[1],back[2],side[1],side[2]]
  r.write(mem,b''.join(tiles(im) for im in imgs))
  r.call('ObjectEventTurn',obj,direction);r.call('StartSpriteAnim',sp,anim);r.run(8)
  r.frame.save(Q/f'marche-mgba-{label}-natif.png');r.frame.resize((720,480),Image.Resampling.NEAREST).save(Q/f'marche-mgba-{label}-x3.png')
  clip=[r.frame.copy() for _ in range(6)];steps=[]
  for n in range(3):
   r.call('ObjectEventSetHeldMovement',obj,C[action]);commands=set()
   for f in range(36):
    r.run();commands.add((r.read(sp+42,1)[0],r.read(sp+43,1)[0]))
    if f%2==0:clip.append(r.frame.copy())
   r.call('ObjectEventClearHeldMovementIfFinished',obj)
   xy=struct.unpack('<hh',r.read(obj+16,4));xy=(xy[0]-7,xy[1]-7);expected=(13+(n+1)*delta[0],8+(n+1)*delta[1]);assert xy==expected,(label,xy,expected)
   assert r.u32(sp+12)==table
   assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==pal
   steps.append(dict(arrived=xy,anim_commands=sorted(commands)))
  clip += [r.frame.copy() for _ in range(10)]
  clip[0].resize((720,480),Image.Resampling.NEAREST).save(Q/f'marche-reelle-{label}-mgba.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in clip[1:]],duration=34,loop=0)
  clips.append(clip);reports.append(dict(direction=label,steps=steps,asymmetric_side_switched_in_ram=True))
 # Sequential full-frame clips with a label placed outside the native game image.
 movie=[];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
 for report,clip in zip(reports,clips):
  for im in clip:
   out=Image.new('RGB',(720,512),(232,232,240));out.paste(im.resize((720,480),Image.Resampling.NEAREST),(0,32));ImageDraw.Draw(out).text((12,5),report['direction'].upper()+' — marche réelle mGBA',font=font,fill='black');movie.append(out)
 movie[0].save(Q/'marche-reelle-mgba.gif',save_all=True,append_images=movie[1:],duration=34,loop=0)
 result=dict(passed=True,engine='mGBA libretro',rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_unchanged=True,steps_total=12,reports=reports,limits=['RAM fixture only, not production registration','Asymmetric left/right image tables swapped in RAM before independent clips; native right hFlip retained','Direct paintover of original FRLG Beauty frames; unchanged source body silhouettes and feet; 32x32 padding only for test template','No NPC patrol, persistent progression or gameplay integration'])
finally:r.close()
(Q/'TEST_MGBA_MARCHE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

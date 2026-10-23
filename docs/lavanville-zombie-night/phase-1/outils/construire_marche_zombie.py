#!/usr/bin/env python3
"""Render literal native movement matrices; approved front pixels stay unchanged."""
import json,struct,hashlib,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parents[4];D=R/'graphics/yokai_zombies/errant';O=D/'mouvement';O.mkdir(exist_ok=True);Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/zombie-marche';Q.mkdir(exist_ok=True)
g=json.loads((D/'overworld-grid.json').read_text());keys=list(g['palette_rgb555']);pal=([v for k in keys for v in g['palette_rgb555'][k]]+[0]*768)[:768];frames={};records=[]
original=Image.open(D/'front.png');original_hash=hashlib.sha256((D/'front.png').read_bytes()).hexdigest()
for direction,poses in g['frames'].items():
 frames[direction]=[]
 for i,rows in enumerate(poses):
  f=Image.new('P',(32,32),0);f.putpalette(pal);f.info['transparency']=0
  for y,row in enumerate(rows):
   for x,k in enumerate(row):f.putpixel((9+x,11+y),keys.index(k))
  frames[direction].append(f)
frames['droite']=[ImageOps.mirror(im) for im in frames['gauche']]
assert frames['face'][0].convert('RGBA').tobytes()==original.convert('RGBA').tobytes()
for f in frames['face'][1:]:assert f.crop((0,0,32,25)).tobytes()==original.crop((0,0,32,25)).tobytes(),'Face/head altered'
engine=[frames[d][g['poses'].index(p)] for d,p in (v.split('/') for v in g['engine_frame_order'])]
sheet=Image.new('P',(32*9,32),0);sheet.putpalette(pal);sheet.info['transparency']=0;raw=bytearray()
for i,f in enumerate(engine):
 sheet.paste(f,(32*i,0))
 for ty in range(4):
  for tx in range(4):
   for y in range(8):
    for x in range(0,8,2):raw.append(f.getpixel((tx*8+x,ty*8+y))|f.getpixel((tx*8+x+1,ty*8+y))<<4)
sheet.save(D/'overworld.png',transparency=0);(D/'overworld.4bpp').write_bytes(raw);shutil.copyfile(D/'front.gbapal',D/'overworld.gbapal');assert len(raw)==4608
all_sheet=Image.new('RGBA',(96,128));font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
board=Image.new('RGBA',(96*6+105,128*6+36),(232,232,240,255));draw=ImageDraw.Draw(board)
for i,p in enumerate(g['poses']):draw.text((105+i*192+45,8),p,font=font,fill='black')
for j,direction in enumerate(['face','dos','gauche','droite']):
 draw.text((5,36+j*192+80),direction.upper(),font=font,fill='black')
 for i,f in enumerate(frames[direction]):
  path=O/(direction+'-'+g['poses'][i]+'.png');f.save(path,transparency=0);a=f.convert('RGBA');box=a.getbbox();assert box[3]==31 and box[1]==11
  assert len({v[:3] for v in a.getdata() if v[3]})<=15
  all_sheet.alpha_composite(a,(32*i,32*j));board.alpha_composite(a.resize((192,192),Image.Resampling.NEAREST),(105+192*i,36+192*j))
  black=sum(v[:3]==(0,0,0) and v[3]==255 for v in a.getdata());assert black>0
  records.append(dict(opaque_black_pixels=black,file=str(path.relative_to(R)),direction=direction,pose=g['poses'][i],bbox=list(box),silhouette=[box[2]-box[0],box[3]-box[1]],foot_y=30))
all_sheet.save(Q/'planche-native-transparente.png');board.save(Q/'planche-directions-x6.png')
loops=[]
for phase in g['cycle']:
 p=Image.new('RGBA',(32*4,32),(224,224,232,255))
 for i,d in enumerate(['face','dos','gauche','droite']):p.alpha_composite(frames[d][phase].convert('RGBA'),(32*i,0))
 loops.append(p.convert('RGB').resize((1024,256),Image.Resampling.NEAREST))
loops[0].save(Q/'quatre-directions-marche.gif',save_all=True,append_images=loops[1:],duration=134,loop=0)
manifest=dict(black_outline_index=1,transparent_index=0,black_rgb=[0,0,0],black_is_opaque=True,approved_front_sha256=original_hash,approved_front_pixel_identical=True,front_head_unchanged_during_walk=True,frame_size=[32,32],silhouette_height=20,shared_palette=True,engine_frame_count=9,explicit_direction_pose_exports=12,right_is_native_hflip=True,cycle=g['cycle'],duration_frames=8,bytes_4bpp=len(raw),records=records)
(Q/'CONTROLE_GRAPHIQUE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('Created12poses,9FRLGframes4608bytes; approvedfront and head identical')

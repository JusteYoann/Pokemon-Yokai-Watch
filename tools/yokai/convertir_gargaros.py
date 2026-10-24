#!/usr/bin/env python3
"""Convert imagegen artwork to GBA frames without repainting sprite shapes."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/gargaros';D.mkdir(parents=True,exist_ok=True)
S=D/'source';S.mkdir(exist_ok=True);original=S/'planche-generee.png'
im=Image.open(original).convert('RGBA')
rows=[(80,390),(400,710),(725,1035),(1055,1370)];cols=[(70,355),(410,685),(735,1030)];frames=[];boxes=[]
for y0,y1 in rows:
 for x0,x1 in cols:
  cell=im.crop((x0,y0,x1,y1));cell.putalpha(cell.getchannel('A').point(lambda a:255 if a>=128 else 0));b=cell.getbbox();assert b
  p=cell.crop(b);target=(round(p.width*22/p.height),22);p=p.resize(target,Image.Resampling.NEAREST)
  frame=Image.new('RGBA',(32,32));frame.paste(p,((32-p.width)//2,31-22));frames.append(frame);boxes.append([x0+b[0],y0+b[1],x0+b[2],y0+b[3]])
palette=[(0,0,0),(16,8,16),(64,16,32),(120,8,32),(184,8,40),(224,24,48),(248,56,64),(248,104,72),(104,64,40),(56,32,24),(248,176,16),(192,104,8),(240,232,192),(128,152,168),(56,40,88),(104,64,104)];flat=[v for c in palette for v in c]+[0]*720
sheet=Image.new('P',(32*12,32));sheet.putpalette(flat);sheet.info['transparency']=0
for n,frame in enumerate(frames):
 out=Image.new('P',(32,32));out.putpalette(flat)
 out.putdata([0 if p[3]<128 else min(range(1,16),key=lambda j:sum((p[k]-palette[j][k])**2 for k in range(3))) for p in frame.get_flattened_data()]);sheet.paste(out,(32*n,0))
sheet.save(D/'overworld.png',transparency=0)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
(D/'CONVERSION.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),method='Imagegen artwork only: threshold alpha, crop, nearest-neighbor native conversion, shared 15-color GBA palette; no repainted shapes',frame_size=[32,32],visible_height=22,baseline=31,order='S:left,stand,right; N:left,stand,right; W:left,stand,right; E:left,stand,right',source_boxes=boxes),indent=2)+'\n')
P=R/'docs/gargaros-marche-20261024';P.mkdir(exist_ok=True)
preview=Image.new('RGBA',(96,128))
for n in range(12):preview.paste(sheet.crop((n*32,0,n*32+32,32)).convert('RGBA'),((n%3)*32,(n//3)*32))
preview.save(P/'planche-native.png');preview.resize((576,768),Image.Resampling.NEAREST).save(P/'planche-x6.png')

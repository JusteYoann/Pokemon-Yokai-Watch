#!/usr/bin/env python3
"""Conversion des PNG fournis en couches GBA ; aucun dessin généré ou substitué."""
import argparse,json,struct,hashlib
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'graphics/yokai_title';SRC=OUT/'source_20261025'
p=argparse.ArgumentParser();p.add_argument('--generate',action='store_true');p.add_argument('--pack',choices=['fond_20261025','logo_20261025','jibanyan','press_start']);a=p.parse_args()
def indexed(rgb,mask):
 c=rgb.quantize(colors=15,dither=Image.Dither.NONE);im=Image.new('P',rgb.size);im.putpalette([0,0,0]+c.getpalette()[:45]+[0]*720);im.putdata([v+1 if yes else 0 for v,yes in zip(c.get_flattened_data(),mask.get_flattened_data())]);return im
if a.generate:
 original=Image.open(SRC/'ghbqpb1.png').convert('RGB').resize((240,160),Image.Resampling.LANCZOS)
 gradient=Image.new('RGB',(256,256));headmask=Image.new('L',(256,256));headrgb=Image.new('RGB',(256,256))
 for y in range(160):
  bg=original.getpixel((0,y))
  for x in range(256):gradient.putpixel((x,y),bg)
  for x in range(240):
   color=original.getpixel((x,y))
   if max(abs(v-w) for v,w in zip(color,bg))>8:headmask.putpixel((x,y),255);headrgb.putpixel((x,y),color)
 gradient.quantize(colors=16,dither=Image.Dither.NONE).save(OUT/'fond_20261025.png')
 indexed(headrgb,headmask).save(OUT/'jibanyan.png',transparency=0)
 logo=Image.open(SRC/'Sanfdhs titre.png').convert('RGBA');box=logo.getbbox();logo=logo.crop(box);h=round(172*logo.height/logo.width);logo=logo.resize((172,h),Image.Resampling.LANCZOS)
 small=indexed(logo.convert('RGB'),logo.getchannel('A').point(lambda x:255 if x>=128 else 0));canvas=Image.new('P',(256,256));canvas.putpalette(small.getpalette());canvas.paste(small,(34,13));canvas.save(OUT/'logo_20261025.png',transparency=0)
 reference=Image.open(SRC/'ghhjjb1.png').convert('RGB').crop((328,507,705,537)).resize((88,8),Image.Resampling.NEAREST)
 press=Image.new('P',(256,256));press.putpalette([0,0,0,0,0,0,128,128,128,240,240,240]+[0]*756)
 for y in range(8):
  for x in range(88):
   rgb=reference.getpixel((x,y));lum=sum(rgb)//3
   if max(rgb)-min(rgb)<45:press.putpixel((76+x,119+y),1 if lum<65 else 2 if lum<185 else 3)
 press.save(OUT/'press_start.png',transparency=0)
 rows={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.glob('*.png')}
 (OUT/'CONVERSION_20261025.json').write_text(json.dumps(dict(source_sha256=rows,logo_bbox=box,logo_native_size=[172,h],logo_position=[34,13],head_mask='Difference avec le dégradé de chaque ligne du fond fourni',press_start='Glyphes extraits de la maquette fournie',hardware='RGB555, 16 couleurs par couche, sans tramage'),ensure_ascii=False,indent=2)+'\n')
if a.pack:
 n=a.pack;im=Image.open(OUT/(n+'.png'));tiles=[bytes(32)];lookup={tiles[0]:0};mapping=[0]*1024;bank={'fond_20261025':0,'logo_20261025':1,'jibanyan':2,'press_start':15}[n];base=128 if n=='jibanyan' else 0
 for y in range(32):
  for x in range(32):
   px=list(im.crop((x*8,y*8,x*8+8,y*8+8)).get_flattened_data());t=bytes(px[i]|(px[i+1]<<4) for i in range(0,64,2))
   if t not in lookup:lookup[t]=len(tiles);tiles.append(t)
   mapping[y*32+x]=bank<<12|base+lookup[t]
 limit=128 if n in ('fond_20261025','press_start') else 384 if n=='jibanyan' else 512
 assert len(tiles)<=limit,(n,len(tiles),limit)
 (OUT/(n+'.4bpp')).write_bytes(b''.join(tiles));(OUT/(n+'.bin')).write_bytes(struct.pack('<1024H',*mapping))
 pal=(im.getpalette()+[0]*48)[:48];(OUT/(n+'.gbapal')).write_bytes(b''.join(struct.pack('<H',(r>>3)|(g>>3)<<5|(b>>3)<<10) for r,g,b in zip(pal[::3],pal[1::3],pal[2::3])))
 print(n,len(tiles),'tiles')

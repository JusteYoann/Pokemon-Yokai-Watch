#!/usr/bin/env python3
"""Archived, unintegrated draft conversion; NOT the current Session2 renderer assets."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
# Retired by the user: prevent a historical conversion from restoring old art.
_policy = Path(__file__).resolve().parents[2]/'data/yokai/shiny_artwork_policy.json'
if _policy.exists() and not json.loads(_policy.read_text())['dedicated_bitmaps_enabled']:
 raise SystemExit('Dedicated shiny drawings retired; use appliquer_shiny_couleurs_seules.py')

R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_shiny_artwork/019';p=D/'source/generated-sheet.png';source=Image.open(p).convert('RGBA');parts=[];rects=[]
for i in range(2):
 rect=(i*source.width//2,0,(i+1)*source.width//2,source.height);rects.append(rect);c=source.crop(rect);a=c.getchannel('A').point(lambda x:255 if x>=128 else 0);assert a.getbbox();c.putalpha(a);parts.append(c.crop(a.getbbox()))
raw=[(0,0,0),(8,8,16),(24,24,32),(48,48,56),(80,80,88),(128,128,144),(192,192,200),(232,232,240),(128,88,16),(200,144,24),(248,200,56),(248,232,120),(96,16,112),(184,48,200),(240,40,152),(232,24,24)]
colors=[tuple((v>>3)*255//31 for v in c) for c in raw];flat=[v for c in colors for v in c]+[0]*720;scale=min(60/max(c.width for c in parts),60/max(c.height for c in parts));frames=[]
for name,c in zip(['front','back'],parts):
 c=c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.NEAREST);f=Image.new('RGBA',(64,64));f.alpha_composite(c,((64-c.width)//2,63-c.height));out=Image.new('P',(64,64));out.putpalette(flat);out.putdata([0 if px[3]<128 else min(range(1,16),key=lambda i:sum((v-p)**2 for v,p in zip(px[:3],colors[i]))) for px in f.get_flattened_data()]);out.info['transparency']=0;out.save(D/(name+'.png'),bits=4,transparency=0);frames.append(out)
(D/'shiny.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
view=Image.new('RGB',(512,280));draw=ImageDraw.Draw(view)
for y in range(0,280,16):
 for x in range(0,512,16):draw.rectangle((x,y,x+15,y+15),fill=(224,224,224) if (x//16+y//16)%2 else (176,176,176))
draw.text((6,4),'019 Robonyan 28 / shiny only / black-gold + horns',fill=(0,0,0))
for i,f in enumerate(frames):a=f.convert('RGBA').resize((256,256),Image.Resampling.NEAREST);view.paste(a,(i*256,24),a)
view.save(D/'preview-checkerboard.png');(D/'conversion.json').write_text(json.dumps({'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rectangles':rects,'dimensions':[64,64],'transparent_index':0,'palette_colors':16,'design':'Black/gold, red eyes, purple details, mandatory head horns; normal files untouched','reference':'019_Robonyan_28.webp + current native front/back, all opened before generation','integrated':False},ensure_ascii=False,indent=2)+'\n')

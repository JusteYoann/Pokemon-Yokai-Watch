#!/usr/bin/env python3
"""Technical crops/nearest-neighbor/RGB555 indexing; no redraw of artwork."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'graphics/yokai_characters/static_yokai';source=D/'source/generated-atlas.png'
im=Image.open(source).convert('RGBA');rows=[]
for index,(slug,num) in enumerate([('misterre',33),('octorgone',15),('mademoaiselle',147)]):
 cell=im.crop((im.width*index//3,0,im.width*(index+1)//3,im.height));alpha=cell.getchannel('A').point(lambda v:255 if v>=128 else 0);cell.putalpha(alpha);box=alpha.getbbox();assert box
 crop=cell.crop(box);scale=min(31/crop.width,31/crop.height);crop=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.NEAREST)
 frame=Image.new('RGBA',(32,32));frame.alpha_composite(crop,((32-crop.width)//2,32-crop.height));pixels=list(frame.getdata());colors=[p[:3] for p in pixels if p[3]];assert colors
 atlas=Image.new('RGB',(len(colors),1));atlas.putdata(colors);pal=atlas.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette();palette=[(0,0,0)]+[tuple((v>>3)*255//31 for v in pal[i:i+3]) for i in range(0,45,3)]
 indexed=Image.new('P',(32,32));indexed.putpalette([v for rgb in palette for v in rgb]+[0]*720);indexed.putdata([0 if not a else min(range(1,16),key=lambda k:sum((v-p)**2 for v,p in zip((r,g,b),palette[k]))) for r,g,b,a in pixels]);indexed.info['transparency']=0
 dest=D/slug;dest.mkdir(exist_ok=True);indexed.save(dest/'overworld.png',bits=4,transparency=0);(dest/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
 rows.append(dict(name=slug,species=num,dimensions=[32,32],opaque_pixels=sum(v!=0 for v in indexed.getdata()),transparent_index=0,source_cell=index,crop=list(box),palette_colors=16,animation='Stationary inanimate pose, matches original encounter object animation'))
preview=Image.new('RGB',(3*256,256));px=preview.load()
for y in range(256):
 for x in range(3*256):px[x,y]=(224,224,224) if (x//16+y//16)%2 else (176,176,176)
for i,row in enumerate(rows):
 sp=Image.open(D/row['name']/'overworld.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);preview.paste(sp,(i*256,0),sp)
preview.save(D/'preview-checkerboard.png');(D/'conversion.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='New static overworld art only; approved normal/shiny battle graphics untouched',sprites=rows),ensure_ascii=False,indent=2)+'\n')

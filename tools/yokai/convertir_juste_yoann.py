#!/usr/bin/env python3
"""Technical conversion of the user-authorized reproduction, near-white skin.
Nearest-neighbor scaling and RGB555 indexing only, one stationary facing pose.
"""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/juste_yoann';src=D/'source/reproduction-peau-claire.png';im=Image.open(src).convert('RGBA');w,h=im.size
frames=[];results=[]
for name,box,size,height in [('battle',(0,0,w*3//5,h),(64,64),60),('overworld',(w*3//5,0,w,h),(32,32),19)]:
 crop=im.crop(box);crop.putalpha(crop.getchannel('A').point(lambda a:255 if a>=128 else 0));bbox=crop.getbbox();assert bbox;crop=crop.crop(bbox)
 scale=min((size[0]-2)/crop.width,height/crop.height);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
 f=Image.new('RGBA',size);f.alpha_composite(crop,((size[0]-crop.width)//2,size[1]-1-crop.height));frames.append(f);results.append(dict(name=name,frame=size,opaque=crop.size))
colors=[c[:3] for f in frames for c in f.get_flattened_data() if c[3]];atlas=Image.new('RGB',(len(colors),1));atlas.putdata(colors);raw=atlas.quantize(colors=14,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).getpalette()
palette=[(0,0,0),(0,0,0)]+[tuple((v>>3)*255//31 for v in raw[i:i+3]) for i in range(0,42,3)]
for f,row in zip(frames,results):
 out=Image.new('P',f.size);out.putpalette([v for c in palette for v in c]+[0]*720)
 out.putdata([0 if not c[3] else min(range(1,16),key=lambda i:sum((a-b)**2 for a,b in zip(c[:3],palette[i]))) for c in f.get_flattened_data()]);out.save(D/(row['name']+'.png'),bits=4,transparency=0)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
(D/'conversion.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source='User-authorized generated reproduction; near-white skin requested afterwards. Not a pixel-exact copy of the inline original.',frames=results,palette_colors=16,transparent_index=0),ensure_ascii=False,indent=2)+'\n')
print(results)

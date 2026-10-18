#!/usr/bin/env python3
"""Technical 64x64/indexed4bpp conversion of separately generated shiny art.

No normal art is read, rewritten or painted. Nearest sampling, explicit common
16-entry RGB555 palette, fixed foot baselines; generated input kept for review.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_shiny/019'
p=D/'source/horns-black-gold.png';src=Image.open(p).convert('RGBA')
raw=[(0,0,0),(8,8,16),(24,24,32),(48,48,56),(80,80,88),(128,128,144),(192,192,200),(240,240,232),(128,88,16),(200,144,24),(248,200,56),(248,232,120),(96,16,112),(184,48,200),(240,40,152),(232,24,24)]
colors=[tuple((v>>3)*255//31 for v in c) for c in raw]
frames=[];records=[]
for i,(name,bottom) in enumerate([('front',50),('back',54)]):
 f=src.crop((i*src.width//2,0,(i+1)*src.width//2,src.height));alpha=f.getchannel('A').point(lambda a:255 if a>=128 else 0);f.putalpha(alpha);box=alpha.getbbox();assert box
 f=f.crop(box);h=round(f.height*56/f.width);assert 32<=h<=50,(name,h)
 f=f.resize((56,h),Image.Resampling.NEAREST);canvas=Image.new('RGBA',(64,64));canvas.alpha_composite(f,(4,bottom-h))
 out=Image.new('P',(64,64));out.putpalette([v for c in colors for v in c]+[0]*720)
 out.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((v-p)**2 for v,p in zip((r,g,b),colors[i]))) for r,g,b,a in canvas.get_flattened_data()]);out.info['transparency']=0;out.save(D/(name+'.png'),bits=4,transparency=0);frames.append(out)
 records.append(dict(view=name,source_crop=box,target_bbox=[4,bottom-h,60,bottom],visible_pixels=sum(v!=0 for v in out.get_flattened_data())))
(R/'graphics/yokai/019/shiny.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
view=Image.new('RGB',(512,280));d=ImageDraw.Draw(view)
for y in range(0,280,16):
 for x in range(0,512,16):d.rectangle((x,y,x+15,y+15),fill=(224,224,224) if (x//16+y//16)%2 else (176,176,176))
d.text((6,4),'019 shiny only - native 64x64 x4 - common 16 colors',fill='black')
for i,f in enumerate(frames):a=f.convert('RGBA').resize((256,256),Image.Resampling.NEAREST);view.paste(a,(i*256,24),a)
view.save(D/'preview.png');(D/'conversion.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),records=records,palette_colors=16,transparent_index=0,normal_art_untouched=True),indent=2)+'\n')

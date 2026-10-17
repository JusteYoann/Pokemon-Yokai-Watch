#!/usr/bin/env python3
"""Native format conversion for Matt's original credits art and intro portrait."""
import hashlib,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/matt'
colors=[tuple(map(int,l.split())) for l in (D/'normal.pal').read_text().splitlines()[3:19]]
flat=[v for c in colors for v in c]+[0]*(768-48)
def cut(im,rect):
 c=im.crop(rect).convert('RGBA');a=c.getchannel('A').point(lambda x:255 if x>=128 else 0);c.putalpha(a);assert a.getbbox();return c.crop(a.getbbox())
def convert(c,size,scale=None):
 scale=scale or min((size[0]-2)/c.width,(size[1]-2)/c.height)
 c=c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.NEAREST);f=Image.new('RGBA',size);f.alpha_composite(c,((size[0]-c.width)//2,size[1]-c.height-1))
 out=Image.new('P',size);out.putpalette(flat);out.putdata([0 if p[3]<128 else min(range(1,16),key=lambda i:sum((a-b)**2 for a,b in zip(p[:3],colors[i]))) for p in f.get_flattened_data()]);out.info['transparency']=0;return out
im=Image.open(D/'source/credits-sheet.png');rects=[(x*512,y*512,(x+1)*512,(y+1)*512) for y in range(2) for x in range(3)];parts=[cut(im,r) for r in rects]
scale=min(58/max(p.width for p in parts),54/max(p.height for p in parts));out=Image.new('P',(64,384));out.putpalette(flat)
for i,c in enumerate(parts):out.paste(convert(c,(64,64),scale),(0,i*64))
out.save(D/'credits.png',bits=4,transparency=0)
original=Image.open(D/'source/generated-sheet.png');core=json.loads((D/'conversion.json').read_text());c=cut(original,core['audited_crop_rectangles'][0]);native=convert(c,(64,96));intro=Image.new('P',(64,96));ip=[0]*768;ip[:3]=[115,197,164]
for i,color in enumerate(colors):ip[(96+i)*3:(97+i)*3]=[115,197,164] if i==0 else color
intro.putpalette(ip);intro.putdata([0 if x==0 else 96+x for x in native.get_flattened_data()]);intro.save(D/'intro.png',bits=8)
(D/'intro.pal').write_text('JASC-PAL\n0100\n32\n'+'\n'.join(' '.join(map(str,c)) for c in [(115,197,164)]+colors[1:]+[(0,0,0)]*16)+'\n')
(D/'complements.json').write_text(json.dumps({'credits_source_sha256':hashlib.sha256((D/'source/credits-sheet.png').read_bytes()).hexdigest(),'credits_rectangles':rects,'credits_native_size':[64,64,6],'intro_size':[64,96],'intro_bank':6,'palette':'Existing Matt palette retained, no changes to existing battle or overworld art','integrated':'graphics/yokai_characters/matt/credits.4bpp' in (R/'src/credits.c').read_text()},ensure_ascii=False,indent=2)+'\n')

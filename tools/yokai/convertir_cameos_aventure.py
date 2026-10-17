#!/usr/bin/env python3
"""Technical cropping/palette conversion of original Nathaniel/Michael/Wyatt art."""
import hashlib,json
from collections import deque
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];G=R/'graphics/yokai_characters';source=G/'cameos_aventure/source/generated-sheet.png';im=Image.open(source).convert('RGBA')
specs={
 'nathaniel':{'rects':[(145,0,445,337),(580,80,785,330),(870,80,1070,330),(1170,80,1360,330)],'palette':[(0,0,0),(16,16,24),(56,40,32),(96,64,40),(136,96,64),(192,128,80),(248,192,136),(248,232,208),(248,248,240),(32,40,72),(48,64,112),(80,104,160),(112,104,72),(176,152,104),(216,192,144),(240,216,168)],'reference':'Nathaniel Adams.webp'},
 'michael':{'rects':[(200,334,415,660),(580,390,785,640),(875,390,1060,640),(1175,390,1345,640)],'palette':[(0,0,0),(24,24,24),(104,56,32),(160,88,48),(208,128,72),(208,136,88),(248,200,144),(248,232,208),(248,248,240),(144,136,112),(200,192,160),(232,224,192),(32,56,88),(72,112,160),(168,32,24),(232,64,32)],'reference':'Michael Forester.webp'},
 'wyatt':{'rects':[(165,655,420,1024),(570,720,790,1000),(870,720,1065,1000),(1170,720,1350,1000)],'palette':[(0,0,0),(16,24,24),(40,40,48),(72,72,88),(120,56,32),(184,80,40),(232,120,56),(200,136,88),(248,200,144),(248,248,232),(32,80,64),(56,128,96),(104,192,144),(160,224,168),(120,64,24),(40,136,192)],'reference':'Wyatt Cardamom.webp'}
}
def main_component_bbox(alpha):
 # Neighboring cell fragments must not affect native sizing. Only tight crop;
 # no drawing or deletion of character pixels inside its bounding rectangle.
 w,h=alpha.size;mask=bytearray(1 if v else 0 for v in alpha.get_flattened_data());best=(0,None)
 for start,v in enumerate(mask):
  if not v:continue
  mask[start]=0;q=deque([start]);count=0;x0=w;y0=h;x1=y1=0
  while q:
   k=q.popleft();x=k%w;y=k//w;count+=1;x0=min(x0,x);y0=min(y0,y);x1=max(x1,x);y1=max(y1,y)
   for n,valid in [(k-1,x>0),(k+1,x+1<w),(k-w,y>0),(k+w,y+1<h)]:
    if valid and mask[n]:mask[n]=0;q.append(n)
  if count>best[0]:best=(count,(x0,y0,x1+1,y1+1))
 assert best[0]>1000
 return best[1]
for person,spec in specs.items():
 d=G/person;d.mkdir(exist_ok=True);pal=[tuple((v>>3)*255//31 for v in c) for c in spec['palette']];flat=[v for c in pal for v in c]+[0]*720;parts=[]
 for rect in spec['rects']:
  c=im.crop(rect);alpha=c.getchannel('A').point(lambda x:255 if x>=128 else 0);assert alpha.getbbox();c.putalpha(alpha);c=c.crop(main_component_bbox(alpha));parts.append(c)
 frames=[];owscale=min(16/max(c.width for c in parts[1:]),24/max(c.height for c in parts[1:]))
 for i,c in enumerate(parts):
  size=(64,64) if i==0 else (16,32);scale=min(60/c.width,60/c.height) if i==0 else owscale
  c=c.resize((max(1,round(c.width*scale)),max(1,round(c.height*scale))),Image.Resampling.NEAREST);f=Image.new('RGBA',size);f.alpha_composite(c,((size[0]-c.width)//2,size[1]-c.height-1));out=Image.new('P',size);out.putpalette(flat)
  out.putdata([0 if p[3]<128 else min(range(1,16),key=lambda k:sum((a-b)**2 for a,b in zip(p[:3],pal[k]))) for p in f.get_flattened_data()]);out.info['transparency']=0;assert set(out.get_flattened_data())<set(range(16)) or max(out.get_flattened_data())<=15;frames.append(out)
 frames[0].save(d/'battle.png',bits=4,transparency=0);ow=Image.new('P',(48,32));ow.putpalette(flat)
 for i,f in enumerate(frames[1:]):ow.paste(f,(16*i,0))
 ow.save(d/'overworld.png',bits=4,transparency=0);(d/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in pal)+'\n')
 p=Image.new('RGB',(576,288));draw=ImageDraw.Draw(p)
 for y in range(0,p.height,16):
  for x in range(0,p.width,16):draw.rectangle((x,y,x+15,y+15),fill=(224,224,224) if (x//16+y//16)%2 else (176,176,176))
 draw.text((8,4),person+' / original art / native 64x64 + 3x16x32 / 15 RGB555 colors',fill=(0,0,0))
 for i,f in enumerate(frames):
  scale=4 if i==0 else 6;a=f.convert('RGBA').resize((f.width*scale,f.height*scale),Image.Resampling.NEAREST);p.paste(a,(0,24) if i==0 else (272+(i-1)*96,80),a)
 p.save(d/'preview-checkerboard.png');(d/'conversion.json').write_text(json.dumps({'source':str(source.relative_to(R)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_dimensions':im.size,'reference_opened':spec['reference'],'rectangles':spec['rects'],'dimensions':{'battle':[64,64],'overworld':[16,32,3]},'palette':'15 opaque RGB555 colors, transparent index0; per-character palette','animation_policy':'Stationary cameos only; south/north/west plus native east mirror, no walk cycle claimed','integrated':('TRAINER_PIC_YOKAI_'+person.upper()) in (R/'include/constants/trainers.h').read_text()},ensure_ascii=False,indent=2)+'\n')

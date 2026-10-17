#!/usr/bin/env python3
"""Technical format conversion of original Domniscian, Morleone and five employee sprites."""
import hashlib,json
from collections import deque
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];G=R/'graphics/yokai_characters'
DOM=[(0,0,0),(24,16,32),(32,32,64),(104,32,112),(176,48,112),(232,40,64),(136,16,40),(248,152,168),(248,192,192),(248,240,208),(40,96,184),(112,216,224),(120,80,40),(224,168,64),(208,232,64),(248,248,248)]
DON=[(0,0,0),(16,16,24),(32,32,40),(72,64,80),(240,240,216),(184,184,176),(112,16,40),(200,32,64),(136,80,104),(232,152,168),(8,72,88),(16,128,144),(80,112,64),(160,192,112),(128,64,152),(192,112,192)]
specs={
 'domniscian':{'rects':[(55,0,500,395),(580,70,860,390),(880,70,1150,390),(1220,70,1470,390)],'group':'domniscian','owwidth':32,'palette':DOM,'reference':'Dominiscian.webp'},
 'employe_rouge':{'rects':[(55,395,500,715),(610,430,840,700),(900,430,1130,700),(1220,430,1460,700)],'group':'domniscian','owwidth':16,'palette':DOM,'reference':'Employé1.png / Employé3.jpg, red'},
 'employe_bleu':{'rects':[(55,715,500,1024),(600,725,850,1010),(900,725,1140,1010),(1220,725,1470,1010)],'group':'domniscian','owwidth':16,'palette':DOM,'reference':'Employé1.png / Employé2.png, blue'},
 'don_morleone':{'rects':[(40,0,390,340),(440,70,665,340),(690,70,900,340),(950,70,1200,340)],'group':'morleone','owwidth':16,'palette':DON,'reference':'Don Morleone.webp'},
 'mafiamille_1':{'rects':[(45,338,390,630),(430,380,665,630),(690,380,900,630),(950,380,1200,630)],'group':'morleone','owwidth':16,'palette':DON,'reference':'Mafiamille3.webp /4.webp, stocky moustache'},
 'mafiamille_2':{'rects':[(45,625,400,960),(430,650,665,955),(690,650,900,955),(950,650,1200,955)],'group':'morleone','owwidth':16,'palette':DON,'reference':'Mafiamille1.webp /4.webp, slender'},
 'mafiamille_3':{'rects':[(45,950,390,1278),(430,980,665,1278),(690,980,900,1278),(950,980,1200,1278)],'group':'morleone','owwidth':16,'palette':DON,'reference':'Mafiamille2.png /4.webp, broad shoulders'}
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
 source=G/('cameos_boss/source/'+spec['group']+'-sheet.png');im=Image.open(source).convert('RGBA');owwidth=spec['owwidth'];d=G/person;d.mkdir(exist_ok=True);pal=[tuple((v>>3)*255//31 for v in c) for c in spec['palette']];flat=[v for c in pal for v in c]+[0]*720;parts=[]
 for rect in spec['rects']:
  c=im.crop(rect);alpha=c.getchannel('A').point(lambda x:255 if x>=128 else 0);assert alpha.getbbox();c.putalpha(alpha);c=c.crop(main_component_bbox(alpha));parts.append(c)
 frames=[];owscale=min(owwidth/max(c.width for c in parts[1:]),(28 if owwidth==32 else 24)/max(c.height for c in parts[1:]))
 for i,c in enumerate(parts):
  size=(64,64) if i==0 else (owwidth,32);scale=min(60/c.width,60/c.height) if i==0 else owscale
  c=c.resize((max(1,round(c.width*scale)),max(1,round(c.height*scale))),Image.Resampling.NEAREST);f=Image.new('RGBA',size);f.alpha_composite(c,((size[0]-c.width)//2,size[1]-c.height-1));out=Image.new('P',size);out.putpalette(flat)
  out.putdata([0 if p[3]<128 else min(range(1,16),key=lambda k:sum((a-b)**2 for a,b in zip(p[:3],pal[k]))) for p in f.get_flattened_data()]);out.info['transparency']=0;assert set(out.get_flattened_data())<set(range(16)) or max(out.get_flattened_data())<=15;frames.append(out)
 frames[0].save(d/'battle.png',bits=4,transparency=0);ow=Image.new('P',(owwidth*3,32));ow.putpalette(flat)
 for i,f in enumerate(frames[1:]):ow.paste(f,(owwidth*i,0))
 ow.save(d/'overworld.png',bits=4,transparency=0);(d/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in pal)+'\n')
 p=Image.new('RGB',(880,288));draw=ImageDraw.Draw(p)
 for y in range(0,p.height,16):
  for x in range(0,p.width,16):draw.rectangle((x,y,x+15,y+15),fill=(224,224,224) if (x//16+y//16)%2 else (176,176,176))
 draw.text((8,4),person+' / original art / 64x64 + 3x'+str(owwidth)+'x32 / 15 RGB555 colors',fill=(0,0,0))
 for i,f in enumerate(frames):
  scale=4 if i==0 else 6;a=f.convert('RGBA').resize((f.width*scale,f.height*scale),Image.Resampling.NEAREST);p.paste(a,(0,24) if i==0 else (272+(i-1)*192,80),a)
 p.save(d/'preview-checkerboard.png');(d/'conversion.json').write_text(json.dumps({'source':str(source.relative_to(R)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_dimensions':im.size,'reference_opened':spec['reference'],'rectangles':spec['rects'],'dimensions':{'battle':[64,64],'overworld':[owwidth,32,3]},'palette':'15 opaque RGB555 colors, transparent index0; per-character palette','animation_policy':'Stationary cameos only; south/north/west plus native east mirror, no walk cycle claimed','integrated':('TRAINER_PIC_YOKAI_'+person.upper()) in (R/'include/constants/trainers.h').read_text()},ensure_ascii=False,indent=2)+'\n')

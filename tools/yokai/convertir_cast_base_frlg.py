#!/usr/bin/env python3
"""Convert imagegen source figures to fixed native OW frames; no painting/palette edits."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
D=R/'graphics/yokai_characters'; S=D/'overworld_frlg_v2/source'
if (D/'overworld_red_v3/manifest.json').exists():
 raise SystemExit('Red strict v3 supersedes this map-art converter. Use tools/yokai/convertir_overworld_red_strict.py; do not overwrite the approved shared Mafia/employee revision.')
Q=R/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/CAST_GABARIT_FRLG';Q.mkdir(parents=True,exist_ok=True)

def runs(bits,gap=6):
 out=[];start=last=None
 for i,v in enumerate(bits):
  if not v:continue
  if start is None:start=i
  if last is not None and i-last>gap+1:out.append((start,last+1));start=i
  last=i
 if start is not None:out.append((start,last+1))
 return out

def figures(path,count):
 im=Image.open(path).convert('RGBA');a=np.asarray(im)[:,:,3]>=128;boxes=[]
 for y,b in runs(a.sum(1)>3):
  if b-y<=30:continue
  for x,r in runs(a[y:b].sum(0)>3):
   if r-x<=20:continue
   p=im.crop((x,y,r,b));alpha=p.getchannel('A').point(lambda v:255 if v>=128 else 0);bb=alpha.getbbox()
   if bb:boxes.append((x+bb[0],y+bb[1],x+bb[2],y+bb[3]))
 assert len(boxes)==count,(path.name,len(boxes),count,boxes)
 return im,boxes

report=[];preview=[]
def convert(actor,asset,path,boxes,im,w,hcap,wcap,base=None):
 colors=[tuple(map(int,l.split())) for l in (D/actor/'normal.pal').read_text().splitlines()[3:19]]
 flat=[v for c in colors for v in c]+[0]*720
 sheet=Image.new('P',(w*len(boxes),32));sheet.putpalette(flat);sheet.info['transparency']=0;details=[]
 # Shared scale avoids posture-dependent enlargement of a head/body.
 scale=min(wcap/max(b[2]-b[0] for b in boxes),hcap/max(b[3]-b[1] for b in boxes))
 if base:
  raw=Image.open(base).convert('RGBA');bw=raw.width//len(boxes)
  scale=min([scale]+[raw.crop((bw*i,0,bw*(i+1),32)).getbbox()[3]/(b[3]-b[1]) for i,b in enumerate(boxes)])
 for i,box in enumerate(boxes):
  p=im.crop(box);size=(max(1,round(p.width*scale)),max(1,round(p.height*scale)))
  p=p.resize(size,Image.Resampling.NEAREST)
  bottom=31;center=w/2
  if base:
   raw=Image.open(base).convert('RGBA');bw=raw.width//len(boxes);bb=raw.crop((bw*i,0,bw*(i+1),32)).getbbox()
   assert bb;bottom=bb[3];center=(bb[0]+bb[2])/2+(w-bw)/2
  x=max(0,min(w-size[0],round(center-size[0]/2)));y=bottom-size[1];assert y>=0,(actor,asset,i,size)
  out=Image.new('P',(w,32));out.putpalette(flat);out.info['transparency']=0
  quant=[0 if a<128 else min(range(1,16),key=lambda j:sum((v-c)**2 for v,c in zip((r,g,b),colors[j]))) for r,g,b,a in p.get_flattened_data()]
  small=Image.new('P',p.size);small.putpalette(flat);small.putdata(quant);out.paste(small,(x,y));sheet.paste(out,(w*i,0))
  assert out.getbbox();assert max(out.getdata())<16
  preview.append((actor,asset,i,out));details.append(dict(frame=i,source_bbox=box,target_bbox=out.getbbox()))
 sheet.save(D/actor/(asset+'.png'),bits=4,transparency=0)
 report.append(dict(actor=actor,asset=asset,source=str(path.relative_to(R)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),frames=len(boxes),width=w,height=32,palette_sha256=hashlib.sha256((D/actor/'normal.pal').read_bytes()).hexdigest(),transparent_index=0,poses=details))

groups={'a':[('ariane',20,15),('enma',22,15),('nathaniel',21,15),('michael',21,15)],'b':[('wyatt',20,15),('don_morleone',20,15),('mafiamille_1',20,16),('mafiamille_2',22,14)],'c':[('mafiamille_3',20,16),('employe_rouge',21,15),('employe_bleu',21,15),('domniscian',28,28)]}
for group,actors in groups.items():
 path=S/f'group-{group}.png';im,boxes=figures(path,12)
 for row,(actor,h,cap) in enumerate(actors):convert(actor,'overworld',path,boxes[row*3:row*3+3],im,32 if actor=='domniscian' else 16,h,cap)
path=S/'matt.png';im,boxes=figures(path,9);convert('matt','overworld',path,boxes,im,16,20,15,R/'graphics/object_events/pics/people/blue.png')
specs={'normal':(16,9,19,15),'surf_run':(16,14,19,15),'bike':(32,9,22,23),'vs_seeker_bike':(32,6,23,22),'fish':(32,12,30,30),'item':(32,9,23,23)}
for pack,(w,n,h,cap) in specs.items():
 path=S/f'katie-{pack}.png'
 if not path.exists():continue
 im,boxes=figures(path,n);convert('katie',pack,path,boxes,im,w,h,cap,R/f'graphics/object_events/pics/people/green_{pack}.png')
sheet=Image.new('RGB',(960,((len(preview)+9)//10)*142),(224,224,224));draw=ImageDraw.Draw(sheet)
for k,(actor,asset,i,im) in enumerate(preview):
 x=k%10*96;y=k//10*142;draw.text((x+2,y+2),actor[:12],fill='black');draw.text((x+2,y+14),asset[:9]+' '+str(i),fill='black')
 p=im.convert('RGBA').resize((im.width*3,96),Image.Resampling.NEAREST);sheet.paste(p,(x+(96-p.width)//2,y+34),p)
sheet.save(Q/'CAST_NATIF_X3.png');(Q/'CONVERSION.json').write_text(json.dumps(dict(palette_changes=0,assets=report),indent=2)+'\n')
print('Converted',sum(v['frames'] for v in report),'native frames;',len(report),'assets')

#!/usr/bin/env python3
"""Technical GBA conversion of Nathan-only overworld artwork based on Red poses.

Art is generated separately with imagegen from source Red/reference Nathan.
No painting, no normal/battle palette edits. Native dimensions, indices and tile
frame order are preserved. Conservative source-rectangle overrides are recorded.
"""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/nathan';Q=R/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/NATHAN_GABARIT_RED'
Q.mkdir(parents=True,exist_ok=True)
colors=[tuple(map(int,l.split())) for l in (D/'normal.pal').read_text().splitlines()[3:19]];flat=[v for c in colors for v in c]+[0]*720

def runs(bits,gap=0):
 parts=[];start=None;last=None
 for i,value in enumerate(bits):
  if value:
   if start is None:start=i
   if last is not None and i-last>gap+1:parts.append((start,last+1));start=i
   last=i
 if start is not None:parts.append((start,last+1))
 return parts

def rectangles(path,count):
 im=Image.open(path).convert('RGBA');a=np.asarray(im)[:,:,3]>=128
 ys=[(y,b) for y,b in runs(a.sum(1)>3,gap=6) if b-y>30];boxes=[]
 for y,b in ys:
  xs=[(x,r) for x,r in runs(a[y:b,:].sum(0)>3,gap=6) if r-x>20]
  for x,right in xs:
   crop=im.crop((x,y,right,b));alpha=crop.getchannel('A').point(lambda v:255 if v>=128 else 0);crop.putalpha(alpha);box=alpha.getbbox();assert box
   boxes.append((x+box[0],y+box[1],x+box[2],y+box[3]))
 assert len(boxes)==count,(path.name,'source figures',len(boxes),count,ys)
 return im,boxes

def index(im):
 out=Image.new('P',im.size);out.putpalette(flat)
 out.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((v-p)**2 for v,p in zip((r,g,b),colors[i]))) for r,g,b,a in im.get_flattened_data()]);out.info['transparency']=0;return out

specs={'normal':(16,9),'surf_run':(16,14),'bike':(32,9),'vs_seeker_bike':(32,6),'fish':(32,12),'item':(32,9)}
report=[];allframes=[]
for name,(w,n) in specs.items():
 source=D/'source/red-base'/f'{name}.png'
 if not source.exists():continue
 im,boxes=rectangles(source,n);parts=[im.crop(b) for b in boxes]
 mapping=list(range(n))
 if name=='bike':mapping=[0,1,2,3,8,4,6,5,7] # generator reordered directional gait frames
 if name=='item':mapping=[3,5,5,0,2,0,1,4,2] # original field/VS scripts turn west->front, never back
 if name=='surf_run':mapping[6]=1 # clean north neutral; reject star erroneously drawn on back
 red=Image.open(R/f'graphics/object_events/pics/people/red_{name}.png').convert('RGBA');rw=16 if name in ['normal','surf_run','item'] else 32
 native=[];frames=[]
 for i,j in enumerate(mapping):
  p=parts[j];frame_source=source;frame_box=boxes[j];figure=j
  if name=='bike' and i in [0,3,4]:
   frame_source=D/'source/red-base/bike-front.png';alt,rects=rectangles(frame_source,3);figure=[0,3,4].index(i);frame_box=rects[figure];p=alt.crop(frame_box)
  box=red.crop((rw*i,0,rw*(i+1),32)).getbbox();assert box
  if name=='normal':scale=min(14/p.width,19/p.height)
  elif name=='surf_run':scale=min(15/p.width,(18 if i<3 else 19)/p.height)
  elif name=='bike':scale=min(22/p.width,22/p.height)
  elif name=='vs_seeker_bike':scale=min(22/p.width,(box[3]-box[1])/p.height)
  elif name=='item':scale=min(23/p.width,19/p.height)
  else:scale=min((box[2]-box[0]+2)/p.width,(box[3]-box[1]+1)/p.height)
  size=(max(1,round(p.width*scale)),max(1,round(p.height*scale)));p=p.resize(size,Image.Resampling.NEAREST)
  out=Image.new('RGBA',(w,32));center=(box[0]+box[2])/2+(w-rw)/2
  ox=max(0,min(w-size[0],round(center-size[0]/2)));bottom=box[3];oy=bottom-size[1]
  assert oy>=0 and ox+size[0]<=w,(name,i,size,ox,oy)
  out.alpha_composite(p,(ox,oy));out=index(out);frames.append(out);allframes.append((name,i,out))
  native.append(dict(frame=i,source_file=str(frame_source.relative_to(R)),source_figure=figure,source_bbox=frame_box,red_visible_bbox=box,target_bbox=[ox,oy,ox+size[0],bottom]))
 sheet=Image.new('P',(w*n,32));sheet.putpalette(flat)
 for i,out in enumerate(frames):sheet.paste(out,(w*i,0))
 sheet.info['transparency']=0;sheet.save(D/f'{name}.png',bits=4,transparency=0)
 report.append(dict(asset=name,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frames=n,frame_width=w,frame_height=32,transparent_index=0,palette_sha256=hashlib.sha256((D/'normal.pal').read_bytes()).hexdigest(),native=native))
preview=Image.new('RGB',(768,((len(allframes)+7)//8)*160),(224,224,224));draw=ImageDraw.Draw(preview)
for k,(name,i,im) in enumerate(allframes):
 x=k%8*96;y=k//8*160;draw.text((x+2,y+2),name[:9]+' '+str(i),fill='black');rgba=im.convert('RGBA').resize((im.width*3,96),Image.Resampling.NEAREST);preview.paste(rgba,(x+(96-rgba.width)//2,y+22),rgba)
preview.save(Q/'NATHAN_NATIF_X3.png');(Q/'CONVERSION.json').write_text(json.dumps(dict(source_base='Original Red overworld pose order/anchors, actual source drawing by imagegen',palette_unchanged=True,assets=report),indent=2)+'\n')
print('Converted',sum(x['frames'] for x in report),'frames in',len(report),'overworld packs; palettes and battle art untouched')

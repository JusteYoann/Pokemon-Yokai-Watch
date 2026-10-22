#!/usr/bin/env python3
"""Technical Nathan-template projection of imagegen artwork, at the creator's request.
Body/hands/feet masks are copied from existing native frames; head contour is
character-specific. Native indexed palettes and all source art remain available.
This does not claim manual pixel authorship or artistic approval.
"""
from pathlib import Path
import numpy as np,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters'
base=Image.open(D/'nathan/normal.png');donor=np.array(base)
source=Image.open(D/'nathan_trace/source/couleurs-imagegen.png').convert('RGB');W,H=source.size
def runs(bits):
 a=np.flatnonzero(bits);groups=[]
 if not len(a):return groups
 start=last=int(a[0])
 for v in a[1:]:
  if v-last>6:groups.append((start,last+1));start=int(v)
  last=int(v)
 groups.append((start,last+1));return groups
a=np.array(source);fg=~((a[:,:,0]>180)&(a[:,:,1]<90)&(a[:,:,2]>180))
fg_all=fg.copy();rows=runs(fg_all.sum(1)>10);assert len(rows)==3,rows
specs=['laure','marge','agent_x']
shared=[(255,0,255),(24,24,32),(48,48,56),(232,224,200),(216,176,152),(144,152,120),(208,168,216),(240,200,64),(192,200,200),(184,32,56),(32,168,192),(112,40,144),(72,104,56),(160,112,40),(112,112,120),(48,48,72)]
views=[]
for row,actor in enumerate(specs):
 pal=shared
 folder=D/actor;folder.mkdir(exist_ok=True);(folder/'source').mkdir(exist_ok=True)
 colors=np.array(pal);frames=[];boxes=[]
 for col in range(3):
  sy,ey=rows[row];columns=runs(fg_all[sy:ey].sum(0)>5);assert len(columns)==3,columns
  sx,ex=columns[col];tile=source.crop((sx,sy,ex,ey));a=np.array(tile)
  fg=~((a[:,:,0]>180)&(a[:,:,1]<90)&(a[:,:,2]>180));ys,xs=np.where(fg)
  box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));boxes.append(box)
  # Color source is fitted into the actual native donor frame; masks below
  # preserve donor geometry instead of treating this resized art as final.
  b=base.crop((16*col,0,16*col+16,32)).getbbox();f=np.zeros((32,16),np.uint8)
  sample=np.array(tile.crop(box).resize((b[2]-b[0],b[3]-b[1]),Image.Resampling.NEAREST)).astype(np.int32)
  indices=((sample[:,:,None,:]-colors[None,None,1:,:])**2).sum(3).argmin(2)+1
  bg=(sample[:,:,0]>180)&(sample[:,:,1]<90)&(sample[:,:,2]>180)
  indices[bg]=0
  f[b[1]:b[3],b[0]:b[2]]=indices
  frames.append(f)
 sheet=Image.new('P',(144,32));sheet.putpalette([v for c in pal for v in c]+[0]*720)
 stats=[]
 for num,direction in enumerate([0,1,2,0,0,1,1,2,2]):
  shape=donor[:,16*num:16*num+16]
  f=frames[direction].copy()
  if num in (3,4,5,6):f[13:24]=frames[direction][12:23]
  mask=f>0
  mask[24:]=shape[24:]>0
  f[~mask]=0
  # Body, hand and foot silhouettes come from Nathan. Head contour differs.
  # Uncovered color-source pixels inherit the nearest valid color from the
  # same direction. Body mask must remain identical; the hair/hat has its own head contour.
  yy,xx=np.where(mask&(f==0));valid=np.argwhere(f>0)
  for y,x in zip(yy,xx):
   nearest=valid[((valid-[y,x])**2).sum(1).argmin()];f[y,x]=f[tuple(nearest)]
  pad=np.pad(mask,1)
  edge=mask&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
  f[edge]=1
  # Keep native clothing/limb separators and the actual donor shoe pixels.
  for y in range(24,32):
   for x in range(16):
    if not mask[y,x]:continue
    if shape[y,x]==1:f[y,x]=1
    elif y>=28:f[y,x]=15
    elif (x<=4 or x>=11) and shape[y,x] in (4,5,6,7):f[y,x]=2 if actor=='agent_x' else 4 if actor=='laure' else 5
  assert np.array_equal(f[24:]>0,shape[24:]>0)
  frame=Image.fromarray(f).convert('P');frame.putpalette(sheet.getpalette());sheet.paste(frame,(num*16,0))
  stats.append(dict(frame=num,nathan_body_mask_identical=True,bounds=frame.getbbox()))
 sheet.info['transparency']=0
 sheet.save(folder/'overworld.png',bits=4,transparency=0)
 (folder/'overworld.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in pal)+'\n')
 (folder/'trace-nathan.json').write_text(json.dumps(dict(method='Imagegen design color layer projected onto the native Nathan masks; no gameplay modification.',donor='graphics/yokai_characters/nathan/normal.png',donor_sha256=hashlib.sha256((D/'nathan/normal.png').read_bytes()).hexdigest(),source='graphics/yokai_characters/nathan_trace/source/couleurs-imagegen.png',frame_count=9,head='Same native head envelope, individual hair/hat contour; body, hands and feet use exact Nathan masks',frames=stats,production_status='Native tracing draft, art fidelity to review in engine; not yet story-bound'),indent=2)+'\n')
 views.append((actor,Image.open(folder/'overworld.png')))
plate=Image.new('RGB',(1152,4*288),(220,220,220));d=ImageDraw.Draw(plate)
for row,(name,im) in enumerate([('Nathan - calque natif',base)]+views):
 d.text((8,row*288+4),name,fill='black');rgba=im.convert('RGBA');p=rgba.resize((1152,256),Image.Resampling.NEAREST);plate.paste(p,(0,row*288+24),p)
plate.save(D/'nathan_trace/comparaison-native-x8.png')
(D/'nathan_trace/overworld.pal').write_bytes((D/'laure/overworld.pal').read_bytes())

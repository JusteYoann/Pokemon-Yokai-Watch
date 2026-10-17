#!/usr/bin/env python3
"""Detect source-figure bounds from alpha, without altering artist pixels.

The generator did not obey regular grids. Only updates explicitly inventoried
packs with expected counts; review the native previews before integration.
"""
import json
from pathlib import Path
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parents[2]
def components(path):
 im=Image.open(path).convert('RGBA');mask=im.getchannel('A').point(lambda n:255 if n>=128 else 0).filter(ImageFilter.MaxFilter(3));w,h=mask.size;a=bytearray(mask.tobytes());boxes=[]
 for i in range(len(a)):
  if not a[i]:continue
  a[i]=0;stack=[i];count=0;x0=w;y0=h;x1=y1=0
  while stack:
   q=stack.pop();x=q%w;y=q//w;count+=1;x0=min(x0,x);x1=max(x1,x);y0=min(y0,y);y1=max(y1,y)
   for z in [q-1 if x else -1,q+1 if x<w-1 else -1,q-w if y else -1,q+w if y<h-1 else -1]:
    if z>=0 and a[z]:a[z]=0;stack.append(z)
  if count>1000:boxes.append([max(0,x0-1),max(0,y0-1),min(w,x1+2),min(h,y1+2)])
 # Feet/waist baselines distinguish rows, including unequal row heights.
 groups=[]
 for box in sorted(boxes,key=lambda b:b[3]):
  if not groups or box[3]-groups[-1][0][3]>75:groups.append([])
  groups[-1].append(box)
 return [b for g in groups for b in sorted(g,key=lambda b:b[0])]
for name in ['nathan','katie']:
 p=R/f'graphics/yokai_characters/{name}/production.json';spec=json.loads(p.read_text())
 for pack,count in [('core',16),('equipment',16),('motion',16),('actions',22 if name=='nathan' else 25),('supplement',12),('north_fishing',4)]:
  entry=spec[pack];bounds=components(p.parent/entry['source']);assert len(bounds)==count,(name,pack,len(bounds),count)
  entry['rectangles']=bounds;entry['rectangle_provenance']='Alpha >=128, 3px dilation for connectivity only, connected components>1000 pixels, baseline row grouping; source pixels unchanged.'
 p.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
 print(name,'all source-figure bounds detected; native previews must be reviewed')

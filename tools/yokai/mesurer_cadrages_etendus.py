#!/usr/bin/env python3
"""Measure actual captured sprite outlines, separate from source geometry predictions."""
import csv,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/COMBATS_ETENDUS';old=R/'QA_RECETTE_FINALE/CADRAGE_COMBATS_151';refs=json.loads((old/'sources/MESURES_REFERENCES_BRUTES.json').read_text())['results'];rows=[]
for n,ref in enumerate(refs,1):
 im=Image.open(Q/f'apres/{n:03}.png').convert('RGB')
 for side,roi in [('front',(118,2,240,74)),('back',(0,48,124,112))]:
  pts=[]
  for y in range(roi[1],roi[3]):
   for x in range(roi[0],roi[2]):
    c=im.getpixel((x,y))
    if max(c)<115 or (max(c)-min(c)>40 and min(c)<120):pts.append((x,y))
  b=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts)+1,max(y for x,y in pts)+1];target=ref[side];errors=[a-b for a,b in zip(b,target)]
  rows.append(dict(number=n,side=side,reference_bbox=target,captured_bbox=b,edge_errors=errors,max_absolute_error=max(map(abs,errors))))
(Q/'MESURES_CAPTURES.json').write_text(json.dumps(dict(scope='Dark/colored visible outline measured on actual mGBA screenshots, same ROIs as reference. White pixels and old-vs-current artwork differences can affect outline edges; this is a framing metric, not artistic equality.',maximum_edge_error=max(r['max_absolute_error'] for r in rows),within_two_pixels=sum(r['max_absolute_error']<=2 for r in rows),results=rows),indent=2)+'\n')
with (Q/'MESURES_CAPTURES.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(rows[0]);w.writerows([r.values() for r in rows])
print('NATIVE OUTLINE MEASURES',len(rows),'within2px',sum(r['max_absolute_error']<=2 for r in rows),'exceptions',[(r['number'],r['side'],r['edge_errors']) for r in rows if r['max_absolute_error']>2])

#!/usr/bin/env python3
"""Native conversion of generated oni sheets, same 22px height as Gargaros.
These are new assets only; existing Orqanos game resources are preserved.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];OUT=R/'docs/ogralos-orqanos-sans-massue-20261025';OUT.mkdir(exist_ok=True)
reference=Image.open(R/'graphics/yokai_characters/gargaros/overworld.png').convert('RGBA').crop((32,0,64,32)).getbbox();height=reference[3]-reference[1];baseline=reference[3]
assert height==22
palettes={
 'ogralos':[(0,0,0),(16,8,24),(8,24,64),(8,72,136),(16,112,192),(56,160,224),(112,192,232),(136,0,48),(208,8,72),(248,48,112),(248,184,16),(176,112,8),(248,232,176),(0,80,64),(8,144,112),(88,48,120)],
 'orqanos':[(0,0,0),(8,8,16),(32,32,40),(56,56,64),(88,88,96),(144,136,144),(240,224,192),(64,24,72),(112,32,104),(184,64,144),(120,0,32),(192,8,48),(248,48,72),(248,184,16),(168,104,8),(80,40,104)]}
def runs(bits):
 ids=np.flatnonzero(bits);assert len(ids);out=[];start=last=int(ids[0])
 for i in ids[1:]:
  if i-last>10:out.append((start,int(last)+1));start=int(i)
  last=int(i)
 out.append((start,last+1));return out
reports=[]
for actor,colors in palettes.items():
 D=R/f'graphics/yokai_characters/{actor}_sans_massue';src=D/'source/planche-generee.png';im=Image.open(src).convert('RGBA');a=np.array(im)[:,:,3]>=128
 rows=runs(a.sum(1)>6);assert len(rows)==4;boxes=[]
 flat=[v for c in colors for v in c]+[0]*720;sheet=Image.new('P',(384,32));sheet.putpalette(flat);sheet.info['transparency']=0
 for row,(y0,y1) in enumerate(rows):
  cols=runs(a[y0:y1].sum(0)>6);assert len(cols)==3,(actor,row,cols)
  for col,(x0,x1) in enumerate(cols):
   p=im.crop((x0,y0,x1,y1));p.putalpha(p.getchannel('A').point(lambda x:255 if x>=128 else 0));p=p.crop(p.getbbox());p=p.resize((round(p.width*height/p.height),height),Image.Resampling.NEAREST)
   p=p.crop(p.getbbox())
   if p.height!=height:p=p.resize((p.width,height),Image.Resampling.NEAREST)
   q=Image.new('P',p.size);q.putpalette(flat);q.putdata([0 if alpha<128 else min(range(1,16),key=lambda i:sum((v-colors[i][k])**2 for k,v in enumerate((red,green,blue)))) for red,green,blue,alpha in p.get_flattened_data()]);sheet.paste(q,((row*3+col)*32+(32-p.width)//2,baseline-height));boxes.append([x0,y0,x1,y1])
 sheet.save(D/'overworld.png',transparency=0);(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
 preview=Image.new('RGBA',(96,128));bounds=[]
 for n in range(12):
  f=sheet.crop((32*n,0,32*n+32,32)).convert('RGBA');b=f.getbbox();assert b[1]==reference[1] and b[3]==reference[3];bounds.append(b);preview.paste(f,((n%3)*32,(n//3)*32))
 assert sheet.info.get('transparency',0)==0 and max(sheet.tobytes())<16
 preview.save(OUT/(actor+'-planche-native.png'));preview.resize((576,768),Image.Resampling.NEAREST).save(OUT/(actor+'-planche-x6.png'))
 report=dict(actor=actor,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),frame_size=[32,32],visible_height=height,baseline=baseline,poses=12,order='front x3, back x3, left x3, right x3; step, stand, opposite step',source_boxes=boxes,native_bounds=bounds,existing_game_assets_replaced=False)
 (D/'CONVERSION.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report)
(OUT/'CONVERSIONS.json').write_text(json.dumps(dict(passed=True,scope=__doc__,reference='gargaros',actors=reports),indent=2)+'\n')
print('PASS 24 native poses, all 22 pixels tall, same baseline as Gargaros')

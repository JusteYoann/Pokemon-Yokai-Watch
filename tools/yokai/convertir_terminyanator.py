#!/usr/bin/env python3
"""Conversion GBA des créations imagegen. Conserve la géométrie native de la moto."""
from pathlib import Path
from PIL import Image
import json,shutil,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/terminyanator';S=D/'source';S.mkdir(parents=True,exist_ok=True)
for src,dst in [('/workspace/generated_images/exec-4c821719-3e5b-49f9-8d6d-5d51aed31a0a.png','concept-portrait.png'),('/workspace/generated_images/exec-64253828-5b24-4830-a9b8-7c98397e26b7.png','overworld-edit.png')]:
 if Path(src).exists():shutil.copyfile(src,S/dst)
 assert (S/dst).exists(),dst
# Fifteen opaque GBA colors; reserved index 0 is transparent.
colors=[(0,0,0),(8,8,16),(32,32,40),(57,57,74),(74,74,90),(106,123,139),(139,139,148),(197,197,213),(255,255,255),(230,238,238),(230,24,40),(49,74,90),(0,180,180),(115,238,222),(0,74,180),(139,115,49)]
flat=sum((list(c) for c in colors),[])+[0]*720
def indexed(im):
 out=Image.new('P',im.size);out.putpalette(flat);out.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((rgb[k]-colors[i][k])**2 for k in range(3))) for *rgb,a in im.convert('RGBA').get_flattened_data()]);return out
native=Image.open(R/'graphics/object_events/pics/people/biker.png').convert('RGBA');gen=Image.open(S/'overworld-edit.png').convert('RGBA');strip=Image.new('RGBA',(320,32));boxes=[]
# Crop evenly spaced generated poses, fit each into the source biker's footprint.
for i in range(10):
 original=native.crop((i*32,0,i*32+32,32));bbox=original.getbbox();tile=gen.crop((round(i*gen.width/10),0,round((i+1)*gen.width/10),gen.height));tile.putalpha(tile.getchannel('A').point(lambda a:255 if a>=128 else 0));tile=tile.crop(tile.getbbox()).resize((bbox[2]-bbox[0],bbox[3]-bbox[1]),Image.Resampling.NEAREST);frame=Image.new('RGBA',(32,32));frame.paste(tile,bbox[:2]);side=i in (2,7,8)
 # Restore the source motorcycle, including tires, frame, footrests and handlebars.
 # Pixel positions/alpha are copied, so native bike scale and collision footprint stay exact.
 for y in range(32):
  for x in range(32):
   if y>=23 or (side and y>=20 and (x<12 or x>20)):
    frame.putpixel((x,y),original.getpixel((x,y)))
 strip.paste(frame,(i*32,0));boxes.append(bbox)
indexed(strip).save(D/'overworld.png',transparency=0,bits=4)
portrait=Image.open(S/'concept-portrait.png').convert('RGBA').crop((300,705,950,1210));portrait.putalpha(portrait.getchannel('A').point(lambda a:255 if a>=128 else 0));portrait=portrait.crop(portrait.getbbox());red=[(x,y) for y in range(portrait.height) for x in range(portrait.width) if (lambda c:c[3]>128 and c[0]>140 and c[0]>c[1]*2 and c[0]>c[2]*2)(portrait.getpixel((x,y)))];accent=(sum(x for x,y in red)/len(red)/portrait.width,sum(y for x,y in red)/len(red)/portrait.height) if red else None;portrait=portrait.resize((60,round(portrait.height*60/portrait.width)),Image.Resampling.NEAREST);frame=Image.new('RGBA',(64,64));frame.paste(portrait,((64-portrait.width)//2,63-portrait.height));
# Preserve the tiny red optical sensor when downsampling to the GBA grid.
if accent:frame.putpixel(((64-portrait.width)//2+int(accent[0]*portrait.width),63-portrait.height+int(accent[1]*portrait.height)),(230,24,40,255))
indexed(frame).save(D/'battle.png',transparency=0,bits=4)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
(D/'CONVERSION.json').write_text(json.dumps(dict(frame=[32,32],frames=10,original_footprints=boxes,motorcycle_restored_region='y>=23; side y>=20 outside x12..20',battle=[64,64],palette=colors),indent=2)+'\n')
P=R/'docs/postgame-corrections-terminyanator-20261025';indexed(strip).convert('RGBA').resize((1280,128),Image.Resampling.NEAREST).save(P/'terminyanator-planche-x4.png');indexed(frame).convert('RGBA').resize((512,512),Image.Resampling.NEAREST).save(P/'terminyanator-portrait-x8.png')

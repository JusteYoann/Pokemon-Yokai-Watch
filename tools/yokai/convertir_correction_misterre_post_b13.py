#!/usr/bin/env python3
"""Technical masked/indexed conversion of imagegen face correction.

Only the specified facial regions use generated bark. All other original pixels,
transparent silhouette, original palette and original dimensions remain exact.
"""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'graphics/yokai_characters/static_yokai'
original=Image.open(D/'source/misterre-b13.png');generated=Image.open(D/'source/misterre-face-correction.png').convert('RGBA')
alpha=generated.getchannel('A').point(lambda x:255 if x>=128 else 0);box=alpha.getbbox();assert box
# Use generated bark as the source, while preserving the original outer art.
ob=original.convert('RGBA');ob.putalpha(original.point(lambda i:255 if i else 0).convert('L'))
# The transparency mask must be built from indices, independent of palette colors.
mask=Image.new('L',original.size);mask.putdata([255 if i else 0 for i in original.getdata()]);ob.putalpha(mask);original_box=ob.getbbox()
patch=generated.crop(box).resize((original_box[2]-original_box[0],original_box[3]-original_box[1]),Image.Resampling.NEAREST)
palette=original.getpalette();colors=[tuple(palette[3*i:3*i+3]) for i in range(16)]
regions=[(10,15,14,18),(16,15,21,18),(9,19,14,22),(17,19,22,22),(11,22,21,26)]
result=original.copy();touched=set()
for x0,y0,x1,y1 in regions:
 for y in range(y0,y1):
  for x in range(x0,x1):
   if original.getpixel((x,y))==0:continue
   rgb=patch.getpixel((x-original_box[0],y-original_box[1]))[:3]
   index=min(range(2,13),key=lambda i:sum((a-b)**2 for a,b in zip(rgb,colors[i])))
   result.putpixel((x,y),index);touched.add((x,y))
for y in range(32):
 for x in range(32):
  if (x,y) not in touched:assert original.getpixel((x,y))==result.getpixel((x,y))
  assert (original.getpixel((x,y))==0)==(result.getpixel((x,y))==0)
assert result.getpalette()==original.getpalette()
assert not any(result.getpixel((x,y))==1 for y in range(15,26) for x in range(8,24))
result.save(D/'misterre/overworld.png',bits=4,transparency=0)
report={'source_generated_sha256':hashlib.sha256((D/'source/misterre-face-correction.png').read_bytes()).hexdigest(),'regions':regions,'modified_pixels':sum(a!=b for a,b in zip(original.getdata(),result.getdata())),'outside_regions_byte_indices_unchanged':True,'palette_unchanged':True,'silhouette_transparency_unchanged':True,'dimensions':[32,32],'artwork_process':'Imagegen removes face; only masked bark regions transferred and quantized to existing brown palette. Whole generated silhouette not integrated.'}
(ROOT/'QA_RECETTE_FINALE/POST_B13/sprites/MISTERRE_CORRECTION.json').write_text(json.dumps(report,indent=2)+'\n')
result.resize((256,256),Image.Resampling.NEAREST).save('/tmp/misterre-post-b13-x8.png')

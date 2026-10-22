#!/usr/bin/env python3
"""Compare actual enlarged OBJ and animation BG silhouettes in mGBA."""
import hashlib,json,os
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import tester_animations_attaques_mgba as t
Q=t.ROOT/'QA_RECETTE_FINALE/COMBATS_ETENDUS/masques';Q.mkdir(exist_ok=True)
rows=[];frames=[]
for n in [19,29,30,1,100,150,114,119,149]:
 r,base,actual=t.setup((n,n),False)
 try:
  for side in [0,1]:
   for bg in [1,2]:
    r.restore(base);r.run(2);before=r.frame.copy();sp=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+side,1)[0]
    r.call('MoveBattlerSpriteToBG',side,bg-1);r.run(8);after=r.frame.copy()
    # Comparison includes actual complete screen: differences outside the
    # sprite region are counted, never dismissed as invisible by a mockup.
    d=ImageChops.difference(before.convert('RGB'),after.convert('RGB'));pixels=sum(any(c) for c in d.get_flattened_data());box=d.getbbox()
    name=f'{n:03}-cote-{side}-bg-{bg}';out=Image.new('RGB',(720,160));out.paste(before,(0,0));out.paste(after,(240,0));out.paste(d,(480,0));out.save(Q/f'{name}.png')
    rows.append(dict(species=n,side=side,bg=bg,different_pixels=pixels,difference_bbox=box,exact_match=pixels==0))
 finally:r.close()
print(json.dumps(rows),flush=True)
(Q/'TEST_MGBA.json').write_text(json.dumps(dict(passed=all(v['exact_match'] for v in rows),rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),scope='Real battle OBJ before / native MoveBattlerSpriteToBG after / RGB difference. Both BG targets and both sides. Explicit stopped animation-controller fixture.',results=rows),indent=2)+'\n')

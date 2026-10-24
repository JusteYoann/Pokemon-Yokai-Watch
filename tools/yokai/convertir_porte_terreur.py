#!/usr/bin/env python3
"""Convert generated door artwork to a closed frame, open jamb and rigid leaf."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/porte_terreur';P=R/'docs/porte-terreur-20261024';P.mkdir(exist_ok=True)
source=D/'source/planche-generee.png';im=Image.open(source).convert('RGBA')
def figure(box):
 p=im.crop(box);p.putalpha(p.getchannel('A').point(lambda a:255 if a>=128 else 0));return p.crop(p.getbbox())
reference=Image.open(R/'graphics/yokai_characters/nathan/normal.png').convert('RGBA').crop((0,0,16,32)).getbbox()
nathan_height=reference[3]-reference[1];height=nathan_height+5
width=round(18*height/26);left=(32-width)//2;top=reference[3]-height
closed=figure((30,130,380,610)).resize((width,height),Image.Resampling.NEAREST)
# The same jamb is retained in every pose. Only this exact leaf rectangle is
# exposed, so compositing the leaf at offset zero reproduces CLOSED byte-for-byte.
bounds=(left+round(3*width/18),top+round(4*height/26),left+round(16*width/18),top+round(25*height/26));distance=bounds[2]-bounds[0]
colors=[(0,0,0),(24,8,24),(56,32,64),(88,56,104),(128,104,144),(184,160,192),(248,248,248),(248,240,168),(248,208,32),(208,152,16),(128,88,8),(248,248,192),(248,224,80),(96,48,24),(176,160,184),(8,0,8)]
flat=[v for c in colors for v in c]+[0]*720
canvas=Image.new('RGBA',(32,32));canvas.paste(closed,(left,top))
closed=Image.new('P',(32,32));closed.putpalette(flat)
# Pure white belongs only to the revealed opening, never a closed corner.
closed.putdata([0 if a<128 else min([i for i in range(1,16) if i!=6],key=lambda i:sum((v-colors[i][j])**2 for j,v in enumerate((r,g,b)))) for r,g,b,a in canvas.get_flattened_data()])
opened=closed.copy();opened.paste(6,bounds)
leaf=Image.new('P',(32,32));leaf.putpalette(flat);leaf.paste(closed.crop(bounds),bounds[:2])
mask=Image.new('L',(32,32));mask.putdata([255 if i else 0 for i in leaf.get_flattened_data()])
sealed=opened.copy();sealed.paste(leaf,(0,0),mask)
assert sealed.tobytes()==closed.tobytes(), 'Leaf/frame gap in the closed composition'
assert closed.getbbox()[3]-closed.getbbox()[1]==height
assert height-nathan_height==5
assert 6 not in set(closed.tobytes()), 'White pixel leaked into the closed door'
assert set(opened.crop(bounds).tobytes())=={6}, 'Portal is not uniformly white'
assert not any(g>r and g>b for r,g,b in colors), 'Green entry remains'
sheet=Image.new('P',(64,32));sheet.putpalette(flat);sheet.paste(closed,(0,0));sheet.paste(opened,(32,0))
sheet.save(D/'overworld.png',transparency=0);leaf.save(D/'panneau.png',transparency=0)
sheet.convert('RGBA').resize((384,192),Image.Resampling.NEAREST).save(P/'fermee-ouverte-x6.png')
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
(D/'CONVERSION.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frame_size=[32,32],visible_height=height,nathan_height=nathan_height,leaf_bounds=bounds,translation_pixels=distance,closed_composition_exact=True,portal_uniform_white=True,green_palette_entries=0,method='generated artwork converted to native frame; same frame retained, exact rigid leaf rectangle replaced with white'),indent=2)+'\n')

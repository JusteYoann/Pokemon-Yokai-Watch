#!/usr/bin/env python3
"""Convert generated door artwork to a closed frame, open jamb and rigid leaf."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/porte_terreur';P=R/'docs/porte-terreur-20261024';P.mkdir(exist_ok=True)
source=D/'source/planche-generee.png';im=Image.open(source).convert('RGBA')
def figure(box):
 p=im.crop(box);p.putalpha(p.getchannel('A').point(lambda a:255 if a>=128 else 0));return p.crop(p.getbbox())
closed=figure((40,130,340,610)).resize((18,26),Image.Resampling.NEAREST)
opened=figure((1550,130,1935,610));opened=opened.crop((0,0,round(opened.width*.68),opened.height)).resize((18,26),Image.Resampling.NEAREST)
colors=[(0,0,0),(24,8,24),(56,32,64),(88,56,104),(128,104,144),(184,160,192),(24,88,56),(16,160,72),(56,232,112),(144,248,184),(248,248,232),(248,240,168),(248,208,32),(208,152,16),(128,88,8),(248,248,192)]
flat=[v for c in colors for v in c]+[0]*720
frames=[]
for p in [closed,opened]:
 canvas=Image.new('RGBA',(32,32));canvas.paste(p,(7,5));frames.append(canvas)
# The leaf is cut from the same closed image. Its artwork never changes while
# the engine translates it horizontally. No intermediate poses are redrawn.
leaf=Image.new('RGBA',(32,32));leaf.paste(frames[0].crop((10,9,23,31)),(10,9))
def indexed(frame):
 q=Image.new('P',frame.size);q.putpalette(flat);q.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((v-colors[i][j])**2 for j,v in enumerate((r,g,b)))) for r,g,b,a in frame.get_flattened_data()]);return q
sheet=Image.new('P',(64,32));sheet.putpalette(flat)
for i,p in enumerate(frames):sheet.paste(indexed(p),(i*32,0))
sheet.save(D/'overworld.png',transparency=0);indexed(leaf).save(D/'panneau.png',transparency=0)
sheet.convert('RGBA').resize((384,192),Image.Resampling.NEAREST).save(P/'fermee-ouverte-x6.png')
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
(D/'CONVERSION.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frame_size=[32,32],visible_height=26,nathan_height=19,leaf_bounds=[10,9,23,31],translation_pixels=16,method='crop generated artwork, nearest-neighbor native conversion, shared GBA palette; rigid leaf reused'),indent=2)+'\n')

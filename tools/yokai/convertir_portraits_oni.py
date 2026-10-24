#!/usr/bin/env python3
"""Convert generated front battle artwork to native 64px, no game-table edits."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'docs/oni-portraits-combat-20261025';P.mkdir(exist_ok=True)
colors={
'gargaros':[(0,0,0),(16,8,24),(48,48,56),(96,96,112),(168,168,184),(120,0,32),(200,8,40),(248,48,64),(248,112,120),(176,112,8),(248,200,32),(248,240,184),(64,32,8),(128,80,32),(64,24,80),(128,48,112)],
'ogralos':[(0,0,0),(16,8,24),(40,48,56),(104,112,120),(192,192,192),(8,48,104),(16,112,200),(64,184,240),(120,0,40),(224,24,88),(248,192,24),(248,240,184),(104,40,112),(32,88,80),(88,152,136),(128,200,176)]}
results=[]
for actor,palette in colors.items():
 D=R/'graphics/oni_battle'/actor;src=D/'source/portrait-genere.png';im=Image.open(src).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));bbox=im.getbbox();im=im.crop(bbox);scale=60/max(im.size);size=(round(im.width*scale),round(im.height*scale));im=im.resize(size,Image.Resampling.NEAREST)
 def index(red,green,blue,alpha):
  if alpha<128:return 0
  # Keep neutral metal/ivory clusters in their neutral ramps rather than
  # mapping cool gray highlights to the blue oni's teal clothing palette.
  choices=[1,2,3,4,11] if max(red,green,blue)-min(red,green,blue)<=24 else range(1,16)
  return min(choices,key=lambda i:sum((v-palette[i][j])**2 for j,v in enumerate((red,green,blue))))
 flat=[v for c in palette for v in c]+[0]*720;q=Image.new('P',size);q.putpalette(flat);q.putdata([index(*pixel) for pixel in im.get_flattened_data()]);frame=Image.new('P',(64,64));frame.putpalette(flat);frame.info['transparency']=0;frame.paste(q,((64-size[0])//2,62-size[1]));frame.save(D/'front.png',transparency=0);frame.save(P/(actor+'-combat.png'),transparency=0);frame.convert('RGBA').resize((384,384),Image.Resampling.NEAREST).save(P/(actor+'-combat-x6.png'))
 assert max(frame.tobytes())<16 and frame.convert('RGBA').getbbox()
 (D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
 results.append(dict(actor=actor,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source_bounds=bbox,native_size=[64,64],visible_bounds=frame.convert('RGBA').getbbox(),transparent_index=0,opaque_color_limit=15,game_tables_changed=False))
(P/'CONVERSIONS.json').write_text(json.dumps(dict(passed=True,scope=__doc__,portraits=results),indent=2)+'\n')
print('PASS two transparent 64x64 battle portraits, max15 opaque colors each')

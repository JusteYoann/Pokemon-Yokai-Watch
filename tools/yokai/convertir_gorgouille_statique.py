#!/usr/bin/env python3
"""Convert the generated front-only Gorgouille artwork; no playable-mon changes."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/gorgouille_statique';P=R/'docs/gorgouille-face-20261025';P.mkdir(exist_ok=True)
src=D/'source/face-generee.png';im=Image.open(src).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));source_bounds=im.getbbox();im=im.crop(source_bounds)
ref=Image.open(R/'graphics/yokai_characters/gargaros/overworld.png').convert('RGBA').crop((32,0,64,32)).getbbox();h=ref[3]-ref[1]
im=im.resize((round(im.width*h/im.height),h),Image.Resampling.NEAREST);im=im.crop(im.getbbox())
if im.height!=h:im=im.resize((im.width,h),Image.Resampling.NEAREST)
colors=[(0,0,0),(16,8,16),(72,32,8),(128,64,0),(184,104,0),(232,144,0),(248,192,8),(248,224,48),(248,248,128),(120,0,32),(200,8,48),(248,32,72),(56,24,88),(112,48,152),(168,96,192),(248,240,192)]
flat=[v for c in colors for v in c]+[0]*720;small=Image.new('P',im.size);small.putpalette(flat);small.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((v-colors[i][k])**2 for k,v in enumerate((r,g,b)))) for r,g,b,a in im.get_flattened_data()])
frame=Image.new('P',(32,32));frame.putpalette(flat);frame.info['transparency']=0;frame.paste(small,((32-im.width)//2,ref[3]-h))
b=frame.convert('RGBA').getbbox();assert b[1]==ref[1] and b[3]==ref[3] and max(frame.tobytes())<16
frame.save(D/'overworld.png',transparency=0);frame.save(P/'gorgouille-face.png',transparency=0);frame.convert('RGBA').resize((256,256),Image.Resampling.NEAREST).save(P/'gorgouille-face-x8.png')
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
(D/'CONVERSION.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source_bounds=source_bounds,frame_size=[32,32],visible_height=h,baseline=ref[3],visible_bounds=b,poses=1,direction='face',existing_playable_assets_changed=False),indent=2)+'\n')
print('PASS one static front frame, transparent, 22px high like Gargaros')

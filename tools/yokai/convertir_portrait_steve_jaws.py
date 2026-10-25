#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/steve_jaws';S=D/'source/portrait-reference.png'
im=Image.open(S).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0));box=im.getbbox();body=im.crop(box);body=body.resize((round(body.width*60/body.height),60),Image.Resampling.NEAREST)
palette=json.loads((R/'graphics/yokai_characters/requin_lunettes/CONVERSION.json').read_text())['colors'];flat=[v for c in palette for v in c]+[0]*720
out=Image.new('P',(64,64));out.putpalette(flat);piece=Image.new('P',body.size);piece.putpalette(flat)
piece.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((rgb[k]-palette[i][k])**2 for k in range(3))) for *rgb,a in body.get_flattened_data()]);out.paste(piece,((64-body.width)//2,63-60));out.save(D/'battle.png',transparency=0,bits=4)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
P=R/'docs/steve-jaws-sevii-jadielle-20261025';out.convert('RGBA').resize((512,512),Image.Resampling.NEAREST).save(P/'portrait-combat-x8.png')
(D/'CONVERSION.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(S.read_bytes()).hexdigest(),source_bbox=box,native_frame=[64,64],visible_height=60,method='imagegen based on original illustration; alpha threshold, nearest-neighbor conversion and shared GBA palette'),indent=2)+'\n')

#!/usr/bin/env python3
"""Three standalone native front proposals; never writes integrated game art."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/atelier-personnages/propositions/agent-x-frlg-abc'
red=Image.open(OUT/'red-reference.png');images=[red];results=[]
for key in 'ABC':
 s=json.loads((OUT/f'agent-x-{key.lower()}-source.json').read_text());assert s['size']==[16,32] and len(s['rows'])==32
 colors=[tuple(bytes.fromhex(c[1:])) for c in s['palette']];data=[]
 for row in s['rows']:
  assert len(row)==16
  data.extend(0 if c=='.' else int(c,16) for c in row)
 assert max(data)<len(colors)<=16
 im=Image.frombytes('P',(16,32),bytes(data));im.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3));path=OUT/f'agent-x-{key.lower()}.png';im.save(path,bits=4,transparency=0)
 reloaded=Image.open(path);assert reloaded.tobytes()==bytes(data) and reloaded.info['transparency']==0
 assert all(im.getpixel((x,30))==0 or red.getpixel((x,30))>0 for x in range(16))
 assert [x for x in range(16) if im.getpixel((x,30))]==[4,5,10,11]
 box=im.getbbox();assert box[1]==12 and box[3]==31
 if key=='A':assert all((im.getpixel((x,y))>0)==(red.getpixel((x,y))>0) for y in range(32) for x in range(16))
 results.append(dict(version=key,frame=[16,32],visible_bounds=list(box),visible_size=[box[2]-box[0],box[3]-box[1]],foot_row=30,foot_bottom_x=[4,5,10,11],visible_colors=len(set(data)-{0}),source_cells_match_png=True,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 images.append(reloaded)
# Native comparison: artwork is pasted 1:1, no source resizing.
board=Image.new('RGB',(80,44),(232,232,232));d=ImageDraw.Draw(board)
for n,im in enumerate(images):
 rgba=im.convert('RGBA');board.paste(rgba,(n*20+2,0),rgba)
 d.line((n*20,31,n*20+19,31),fill=(160,160,160))
 d.text((n*20+3,33),['Red','A','B','C'][n],fill='black',font=ImageFont.load_default(size=8))
board.save(OUT/'comparaison-native.png')
board.resize((960,528),Image.Resampling.NEAREST).save(OUT/'comparaison-x12.png')
report=dict(method=__doc__,proposals=results,foot_alignment='All last opaque pixels on native y30; gray baseline on y31',resampling_of_sprite_art=False,preview_only_enlarged_by=12,integrated=False,animations_created=False,emulator_tested=False)
(OUT/'CONTROLE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))

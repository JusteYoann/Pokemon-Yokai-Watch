#!/usr/bin/env python3
"""One/two native pixel additions to proposal A; no other sprite is changed."""
from pathlib import Path
import copy,hashlib,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/atelier-personnages/propositions/agent-x-frlg-abc'
base=json.loads((OUT/'agent-x-a-source.json').read_text());original=Image.open(OUT/'agent-x-a.png')
pictures=[Image.open(OUT/'red-reference.png'),original];reports=[]
for count,edits in [(1,[(5,21,'a')]),(2,[(5,21,'a'),(6,20,'a')])]:
 spec=copy.deepcopy(base);rows=[list(row) for row in base['rows']]
 for x,y,color in edits:
  assert rows[y][x]=='4', 'Expected original mauve face pixel before eye adjustment'
  rows[y][x]=color
 spec['rows']=[''.join(row) for row in rows];spec['version']=f'A+{count}';spec['description']=f'Only {count} native face pixels changed to extend the existing yellow eye';spec['pixel_edits']=[dict(x=x,y=y,before='4',after=c) for x,y,c in edits]
 (OUT/f'agent-x-a-yeux-{count}-source.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
 colors=[tuple(bytes.fromhex(c[1:])) for c in spec['palette']];data=bytes(0 if c=='.' else int(c,16) for row in spec['rows'] for c in row)
 im=Image.frombytes('P',(16,32),data);im.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3));path=OUT/f'agent-x-a-yeux-{count}.png';im.save(path,bits=4,transparency=0)
 diff=[(x,y) for y in range(32) for x in range(16) if im.getpixel((x,y))!=original.getpixel((x,y))]
 assert len(diff)==count and set(diff)=={(x,y) for x,y,c in edits}
 assert im.getbbox()==original.getbbox()==(1,12,15,31)
 assert all((im.getpixel((x,y))>0)==(original.getpixel((x,y))>0) for y in range(32) for x in range(16))
 assert im.getpalette()[:48]==original.getpalette()[:48]
 pictures.append(Image.open(path));reports.append(dict(version=spec['version'],changed_pixels=count,coordinates=diff,visible_size=[14,19],palette_unchanged=True,silhouette_unchanged=True,other_pixels_identical=True,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
board=Image.new('RGB',(80,44),(232,232,232));draw=ImageDraw.Draw(board)
for n,(im,label) in enumerate(zip(pictures,['Red','A','A+1','A+2'])):
 rgba=im.convert('RGBA');board.paste(rgba,(2+n*20,0),rgba);draw.line((n*20,31,n*20+19,31),fill=(160,160,160));draw.text((2+n*20,33),label,fill='black',font=ImageFont.load_default(size=8))
board.save(OUT/'comparaison-yeux-native.png');board.resize((960,528),Image.Resampling.NEAREST).save(OUT/'comparaison-yeux-x12.png')
(OUT/'CONTROLE_YEUX.json').write_text(json.dumps(dict(variants=reports,original_A_B_C_unchanged=True,integrated=False,animations_created=False),indent=2)+'\n')

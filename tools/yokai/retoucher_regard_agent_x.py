#!/usr/bin/env python3
"""Native eye and hat-shadow proposal. Does not alter integrated game art."""
import copy, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/atelier-personnages/propositions/agent-x-frlg-abc'
base = json.loads((OUT/'agent-x-a-yeux-1-source.json').read_text())
spec = copy.deepcopy(base)
rows = [list(r) for r in base['rows']]
# A three-cell iris with the upper-right pupil cut into it; asymmetrical brim shadow.
edits = [(5,20,'a'), (6,20,'1'), (7,20,'5'), (8,20,'5'), (9,21,'5')]
changes = []
for x,y,c in edits:
    changes.append(dict(x=x,y=y,before=rows[y][x],after=c))
    rows[y][x] = c
spec.update(version='A-regard', description='Three-cell yellow iris, dark pupil, asymmetric hat shadow; native pixel edits only.', rows=[''.join(r) for r in rows], pixel_edits=changes)
(OUT/'agent-x-a-regard-source.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
colors = [tuple(bytes.fromhex(c[1:])) for c in spec['palette']]
im = Image.frombytes('P',(16,32),bytes(0 if c=='.' else int(c,16) for r in spec['rows'] for c in r))
im.putpalette([v for c in colors for v in c]+[0]*(768-3*len(colors)))
path = OUT/'agent-x-a-regard.png'
im.save(path,bits=4,transparency=0)
im = Image.open(path)
old = Image.open(OUT/'agent-x-a-yeux-1.png')
diff = [(x,y) for y in range(32) for x in range(16) if im.getpixel((x,y)) != old.getpixel((x,y))]
assert set(diff)=={(x,y) for x,y,c in edits}
assert im.getbbox()==old.getbbox()==(1,12,15,31)
assert all(bool(a)==bool(b) for a,b in zip(im.tobytes(),old.tobytes()))
assert im.getpalette()[:48]==old.getpalette()[:48]
board = Image.new('RGB',(72,44),(232,232,232))
draw = ImageDraw.Draw(board)
for n,(pic,label) in enumerate([(Image.open(OUT/'red-reference.png'),'Red'),(old,'Avant'),(im,'Regard')]):
    rgba=pic.convert('RGBA');board.paste(rgba,(4+24*n,0),rgba)
    draw.line((n*24,31,min(n*24+23,71),31),fill=(160,160,160))
    draw.text((1+24*n,34),label,fill='black',font=ImageFont.load_default(size=7))
board.save(OUT/'comparaison-regard-native.png')
board.resize((864,528),Image.Resampling.NEAREST).save(OUT/'comparaison-regard-x12.png')
(OUT/'CONTROLE_REGARD.json').write_text(json.dumps(dict(changed_pixels_vs_A1=len(diff),edits=changes,visible_size=[14,19],palette_unchanged=True,silhouette_unchanged=True,integrated=False,sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2)+'\n')

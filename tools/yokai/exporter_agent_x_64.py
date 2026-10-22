#!/usr/bin/env python3
"""Export a standalone native64x64 prototype from explicit pixel cells."""
import hashlib,json,struct
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/atelier-personnages/propositions/agent-x-64'
spec=json.loads((OUT/'agent-x-64-source.json').read_text())
assert spec['size']==[64,64] and len(spec['rows'])==64
palette=[tuple(bytes.fromhex(c[1:])) for c in spec['palette']]
assert len(palette)<=16
indices=[]
for row in spec['rows']:
 assert len(row)==64
 indices.extend(0 if c=='.' else int(c,16) for c in row)
assert min(indices)==0 and max(indices)<len(palette)
im=Image.frombytes('P',(64,64),bytes(indices));im.putpalette([v for c in palette for v in c]+[0]*(768-len(palette)*3))
im.save(OUT/'agent-x-64.png',bits=4,transparency=0)
# Independently replay the native integer drawing commands and compare every cell.
replay=Image.new('P',(64,64));draw=ImageDraw.Draw(replay)
for cmd in spec['commands']:
 if cmd['op']=='polygon':draw.polygon([tuple(p) for p in cmd['points']],fill=cmd['color'])
 else:draw.rectangle(tuple(cmd['box']),fill=cmd['color'])
assert replay.tobytes()==im.tobytes(),'Source cells and drawing commands diverge'
png=Image.open(OUT/'agent-x-64.png');png.verify();png=Image.open(OUT/'agent-x-64.png')
assert png.mode=='P' and png.size==(64,64) and png.info['transparency']==0 and png.tobytes()==bytes(indices)
raw=(OUT/'agent-x-64.png').read_bytes();assert raw[24]==4 and raw[25]==3
# Opaque previews only: native pixels are never rescaled during export.
bg=Image.new('RGBA',(64,64));d=ImageDraw.Draw(bg)
for y in range(0,64,4):
 for x in range(0,64,4):d.rectangle((x,y,x+3,y+3),fill=(232,232,232,255) if (x//4+y//4)%2==0 else (208,208,208,255))
bg.alpha_composite(png.convert('RGBA'))
preview=bg.convert('RGB').resize((512,512),Image.Resampling.NEAREST);preview.save(OUT/'agent-x-64-apercu-x8.png')
grid=preview.copy();d=ImageDraw.Draw(grid)
for n in range(65):
 q=min(n*8,511);d.line((q,0,q,511),fill=(152,152,152));d.line((0,q,511,q),fill=(152,152,152))
grid.save(OUT/'agent-x-64-grille-x8.png')
(OUT/'agent-x-64.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette+[(0,0,0)]*(16-len(palette)))+'\n')
alpha=png.convert('RGBA').getchannel('A');bounds=alpha.getbbox()
report=dict(native_png='agent-x-64.png',dimensions=[64,64],mode='P',png_bit_depth=4,visible_colors=len(set(indices)-{0}),palette_colors_used=len(set(indices)),transparent_pixels=indices.count(0),opaque_pixels=4096-indices.count(0),visible_bounds=list(bounds),occupied_size=[bounds[2]-bounds[0],bounds[3]-bounds[1]],all_source_cells_verified=True,commands_replayed_identically=True,illustration_resizing=False,sha256=hashlib.sha256(raw).hexdigest(),native_gba_4bpp_size=2048,emulator_tested=False,integrated_in_game=False,source_workflow='ModRetro Chromatic pixel-art skill: native cell authoring fallback after grid-generation tool error')
(OUT/'CONTROLE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))

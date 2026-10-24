#!/usr/bin/env python3
"""Restore existing lower back pixels without moving their upper body; no redraw."""
import json, math, re
from pathlib import Path
from presentation_4bpp import decode, transform
ROOT = Path(__file__).resolve().parents[2]
pth = ROOT / 'data/yokai/sprite_presentation.json'
data = json.loads(pth.read_text())
geo_path = ROOT / 'src/data/yokai_battle_geometry.h'
geo = geo_path.read_text()
rows = {}
for m in re.finditer(r'\[(\d+)\] = \{ \{ (.*?) \}, \{ (.*?) \} \}', geo):
    rows[int(m[1])] = [list(map(int, m[i].split(','))) for i in [2, 3]]
changed = []
for p in data['profiles']:
    if p['id'] == '150/icon':
        p.update(scale_q8=256, center_x=16, top=3, reason='Gold/red sword Enma icon; center within the native 32-pixel cell, not a 64-pixel battle cell.')
    if not p['id'].endswith('/battle-back') or 'crop_source_bottom' not in p:
        continue
    n = int(p['id'].split('/')[0])
    raw = (ROOT / p['source']).read_bytes()
    pixels = decode(raw, 64, 64)
    pts = [(x,y) for y in range(64) for x in range(64) if pixels[y][x]]
    cut = p.pop('crop_source_bottom')
    old = [(x,y) for x,y in pts if y < cut]
    left, top = min(x for x,y in pts), min(y for x,y in pts)
    width = max(x for x,y in pts) - left + 1
    oldleft, oldtop = min(x for x,y in old), min(y for x,y in old)
    oldwidth = max(x for x,y in old) - oldleft + 1
    p['center_x'] = p['center_x'] - oldwidth//2 + left-oldleft + width//2
    p['top'] += top-oldtop
    p['restored_source_bottom'] = cut
    p['reason'] = 'Restore existing lower rows for movement animations; preserve the previous head/shoulder pixel coordinates.'
    tex = decode(transform(raw, p), 64, 64)
    coords = [(x,y) for y in range(64) for x in range(64) if tex[y][x]]
    ix,iy,dx,dy,_,_,_,_ = rows[n][1]
    l = math.ceil((min(x for x,y in coords)-32)*256/ix)
    t = math.ceil((min(y for x,y in coords)-32)*256/iy)
    r = math.ceil((max(x for x,y in coords)+1-32)*256/ix)
    b = math.ceil((max(y for x,y in coords)+1-32)*256/iy)
    assert -64<=l<r<=64 and -64<=t<b<=64
    rows[n][1] = [ix,iy,dx,dy,l,t,r-l,b-t]
    changed.append(n)
# Fit every restored source row inside 64 pixels. Compensate the native world
# anchor when texture padding moves upward; scale and animation remain intact.
for p in data['profiles']:
    if 'restored_source_bottom' not in p:
        continue
    n = int(p['id'].split('/')[0])
    raw = (ROOT / p['source']).read_bytes()
    source = decode(raw, 64, 64)
    pts = [(x,y) for y in range(64) for x in range(64) if source[y][x]]
    fullheight = max(y for x,y in pts)-min(y for x,y in pts)+1
    newtop = min(p['top'],64-fullheight)
    if newtop != p['top']:
        compensation = round((p['top']-newtop)*256/rows[n][1][1])
        rows[n][1][3] += compensation
        p['world_y_compensation'] = compensation
        p['top'] = newtop
    tex = decode(transform(raw,p),64,64)
    coords = [(x,y) for y in range(64) for x in range(64) if tex[y][x]]
    assert len(coords) == len(pts), (n,'source pixels clipped')
    ix,iy,dx,dy,_,_,_,_ = rows[n][1]
    l = math.ceil((min(x for x,y in coords)-32)*256/ix)
    t = math.ceil((min(y for x,y in coords)-32)*256/iy)
    r = math.ceil((max(x for x,y in coords)+1-32)*256/ix)
    b = math.ceil((max(y for x,y in coords)+1-32)*256/iy)
    assert -64<=l<r<=64 and -64<=t<b<=64
    rows[n][1] = [ix,iy,dx,dy,l,t,r-l,b-t]
# Emperor: same inverse scale in both axes, vertical anchor unchanged.
v=rows[101][0];oldix=v[0];v[0]=v[1]
v[4]=math.ceil(v[4]*oldix/v[0]);v[6]=math.ceil((v[6]*oldix)/v[0])
def replace(m):
    n=int(m[1]);return '['+str(n)+'] = { '+', '.join('{ '+', '.join(map(str,v))+' }' for v in rows[n])+' }'
geo = re.sub(r'\[(\d+)\] = \{ \{ (.*?) \}, \{ (.*?) \} \}', replace, geo)
geo_path.write_text(geo)
pth.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Restored lower back textures:',changed)

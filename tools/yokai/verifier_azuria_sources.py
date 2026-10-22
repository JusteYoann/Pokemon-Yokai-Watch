#!/usr/bin/env python3
"""Independent layout graph and historical source preservation contracts."""
import json,struct
from collections import deque
from mgba_rpc import ROOT
out=ROOT/'QA_RECETTE_FINALE/AZURIA_SCENARIO_2026';out.mkdir(exist_ok=True)
l=next(x for x in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if x.get('id')=='LAYOUT_CERULEAN_CITY_GYM')
w,h=l['width'],l['height'];a=struct.unpack('<'+'H'*(w*h),(ROOT/l['blockdata_filepath']).read_bytes());d=json.loads((ROOT/'data/maps/CeruleanCity_Gym/map.json').read_text())
free={(x,y) for y in range(h) for x in range(w) if not (a[y*w+x]>>10&3)}-{(o['x'],o['y']) for o in d['object_events']}
def reach(start,opened):
 f=free.copy()
 if not opened:f.discard((8,7))
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if p in f and p not in seen:seen.add(p);q.append(p)
 return seen
closed=reach((8,17),False);opened=reach((8,17),True)
for p in [(5,11),(11,11),(8,10),(7,18),(8,18),(9,18)]:assert p in closed,p
assert (8,5) not in closed and (8,5) in opened
assert (8,17) in reach((8,5),True)
attrs=(ROOT/'data/tilesets/secondary/azuria_hearths/metatile_attributes.bin').read_bytes()
for x in [7,8,9]:
 t=a[18*w+x]&1023;assert attrs[(t-640)*4]==0x65
assert len(d['object_events'])+1<=16
assert [(o['x'],o['y']) for o in d['object_events'] if o['graphics_id'] in ['OBJ_EVENT_GFX_YOKAI_NATHAN','OBJ_EVENT_GFX_YOKAI_KATIE']]==[(8,4),(8,4)]
s=(ROOT/'src/data/trainer_parties.h').read_text()
for name in ['sYokaiParty_LEADER_MISTY','sParty_YokaiKatie','sParty_YokaiNathan','sParty_YokaiKatiePost','sParty_YokaiNathanPost']:assert name+'[]' in s,name
r={'passed':True,'scope':'Source graph only, complements runtime walks','checks':['All three hearths and original exits reachable before gate','Champion unreachable before gate and reachable afterwards','Champion has a path back to exits','All three door metatiles retain native south-arrow warp behavior','Mutually exclusive leaders share one location within object capacity','Historical locked and cameo party source arrays retained']}
(out/'CONTROLE_SOURCES.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

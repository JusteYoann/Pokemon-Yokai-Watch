#!/usr/bin/env python3
"""Independent native-layout accessibility and resource migration contracts."""
import json,struct
from collections import deque
from pathlib import Path
from mgba_rpc import ROOT
layout=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'];l=next(x for x in layout if x.get('id')=='LAYOUT_PEWTER_CITY_GYM')
w,h=l['width'],l['height'];raw=(ROOT/l['blockdata_filepath']).read_bytes();cells=struct.unpack('<'+'H'*(w*h),raw)
walkable={(x,y) for y in range(h) for x in range(w) if not((cells[y*w+x]>>10)&3)}
mapdata=json.loads((ROOT/'data/maps/PewterCity_Gym/map.json').read_text())
objects={(o['x'],o['y']) for o in mapdata['object_events']}
def reach(start,gate):
 free=walkable-objects
 if not gate:free.discard((6,5))
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for t in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if t in free and t not in seen:seen.add(t);q.append(t)
 return seen
closed=reach((6,13),False);opened=reach((6,13),True)
assert (6,4) not in closed and (6,4) in opened
for p in [(3,7),(9,7),(5,14),(6,14),(7,14)]:assert p in closed,p
assert (6,13) in reach((6,4),True)
# Every normal northern Route2 exit crosses the four actual coordinate triggers.
city=json.loads((ROOT/'data/maps/PewterCity/map.json').read_text())
assert {(c['x'],c['y']) for c in city['coord_events'] if c['script']=='PewterCity_EventScript_MorleoneSpeech'}=={(x,35) for x in range(20,24)}
assert len(city['object_events'])+1<=16
assert (ROOT/'data/yokai/equipes_boss_validees.json').exists()
assert 'sYokaiParty_LEADER_BROCK[]' in (ROOT/'src/data/trainer_parties.h').read_text()
report={'passed':True,'checks':['Both relics and all three exits accessible before gate opens','Champion reachable only after central gate','Return to exit remains possible','All four Route2 entrance columns trigger speech','At most16objects including player','Original team source retained'],'scope':'Static source graph, complements real native walks; not a replacement for runtime tests'}
(ROOT/'QA_RECETTE_FINALE/ARGENTA_SCENARIO_2026/CONTROLE_SOURCES.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

#!/usr/bin/env python3
"""Static feasibility on original collision grid. Not a dynamic gameplay test."""
from pathlib import Path
import struct,json,itertools
R=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1]
b=struct.unpack('<480H',(R/'data/layouts/LavenderTown/map.bin').read_bytes());free={(x,y) for y in range(20) for x in range(24) if not ((b[y*24+x]>>10)&3)}
paths={'errant':[(5,7),(6,7),(7,7),(7,8),(6,8),(5,8)],'sprinteur':[(x,12) for x in range(12,17)],'colosse':[(x,8) for x in range(17,21)],'spectral':[(14,17),(15,17),(16,17),(16,18),(15,18),(14,18)]}
portals=[(10,0),(0,9),(11,19),(6,6),(18,7),(10,12),(5,17),(10,17),(20,16)]
for p in paths.values():assert all(x in free for x in p)
assert all(x in free for x in portals)
failed=[];count=0
for actors in itertools.product(*paths.values()):
 count+=1;blocked=set(actors);todo=[portals[0]];seen=set(todo)
 while todo:
  x,y=todo.pop()
  for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if v in free and v not in blocked and v not in seen:seen.add(v);todo.append(v)
 if not all(p in seen for p in portals):failed.append(actors)
assert not failed,failed[:1]
(D/'patrouilles-faisabilite.json').write_text(json.dumps(dict(paths=paths,portals=portals,combinations_tested=count,all_portals_connected_with_four_occupied_tiles=True,scope='Static original tile collision connectivity only; no trainer sight cones, NPC movement, elevation/behavior edge cases, entry scripts, or real-time dodge test implemented.'),ensure_ascii=False,indent=2)+'\n')
print(count,'static placements preserve portal connectivity')

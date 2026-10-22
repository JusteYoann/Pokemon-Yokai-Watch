#!/usr/bin/env python3
"""Independent station collision/warp graph and fourth-trophy source contracts."""
import json,struct,subprocess
from collections import deque
from mgba_rpc import ROOT
out=ROOT/'QA_RECETTE_FINALE/SAFRANIA_SCENARIO_2026';out.mkdir(exist_ok=True)
d=json.loads((ROOT/'data/maps/SaffronCity_Gym/map.json').read_text());l=next(l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if l.get('id')==d['layout']);w,h=l['width'],l['height'];a=struct.unpack('<'+'H'*(w*h),(ROOT/l['blockdata_filepath']).read_bytes())
f={(x,y) for y in range(h) for x in range(w) if not(a[y*w+x]>>10&3)}-{(o['x'],o['y']) for o in d['object_events']}
edges={}
for e in d['warp_events'][3:]:
 target=d['warp_events'][int(e['dest_warp_id'])];edges[(e['x'],e['y'])]=[(target['x'],target['y'])]
 assert target['dest_warp_id']==str(d['warp_events'].index(e)),e
 attrs=(ROOT/'data/tilesets/secondary/saffron_orbit/metatile_attributes.bin').read_bytes();assert attrs[((a[e['y']*w+e['x']]&1023)-640)*4]==0x67

def reach(start,gate,teleports=True):
 free=f.copy()
 if not gate:free.discard((14,8))
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]+(edges.get((x,y),[]) if teleports else []):
   if p in free and p not in seen:seen.add(p);q.append(p)
 return seen
closed=reach((14,22),False);opened=reach((14,22),True)
for p in [(4,5),(24,5),(23,20),(14,9),(13,23),(14,23),(15,23)]:assert p in closed,p
assert (14,5) not in closed and (14,5) in opened
assert (4,5) not in reach((14,22),True,False) and (24,5) not in reach((14,22),True,False)
for p in [(4,5),(24,5),(14,5)]:assert (14,22) in reach(p,True),p
for x in [13,14,15]:assert attrs[((a[23*w+x]&1023)-640)*4]==0x65
assert len(d['object_events'])+1<=16
route=json.loads((ROOT/'data/maps/Route25/map.json').read_text());assert all(o['flag']=='FLAG_SCENARIO_HIDE_ROUTE25_ARIANE' for o in route['object_events'] if o['graphics_id'] in ['OBJ_EVENT_GFX_ARIANE','OBJ_EVENT_GFX_USAPION_CAMEO'])
assert 'setflag FLAG_BADGE04_GET' not in (ROOT/'data/maps/CeladonCity_Gym/scripts.inc').read_text()
s=(ROOT/'data/maps/SaffronCity_Gym/scripts.inc').read_text();assert 'setflag FLAG_BADGE04_GET' in s and 'setflag FLAG_BADGE06_GET' not in s
for n in ['sYokaiParty_LEADER_SABRINA','sParty_YokaiAriane','sParty_YokaiArianePost']:assert n+'[]' in (ROOT/'src/data/trainer_parties.h').read_text()
# No new map or layout IDs, and no previous IDs shifted.
for path,key in [('data/maps/map_groups.json',None),('data/layouts/layouts.json','layouts')]:
 old=json.loads(subprocess.check_output(['git','show','617eeed4b:'+path],cwd=ROOT,text=True));new=json.loads((ROOT/path).read_text())
 if key:assert [l.get('id') for l in old[key]]==[l.get('id') for l in new[key]]
 else:assert old==new
r={'passed':True,'scope':'Independent map/warp graph and source contracts, complements runtime playtests','checks':['All systems reachable before gate; boss reachable only with gate open','Teleports required to reach side modules; all three pairs reciprocal and native pad behavior retained','All modules and boss have a path back to real city exits','All three native exit behaviors retained','Old Route25 actors hidden, no object capacity overflow','Celadon awards no badge; new Ariane awards fourth and never sixth','Historic teams and every map/layout ID retained']}
(out/'CONTROLE_SOURCES.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

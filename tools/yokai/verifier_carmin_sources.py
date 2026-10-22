#!/usr/bin/env python3
"""Layout accessibility, native pad pair and stable legacy map/layout IDs."""
import hashlib,json,struct,subprocess
from collections import deque
from mgba_rpc import ROOT
out=ROOT/'QA_RECETTE_FINALE/CARMIN_SCENARIO_2026';out.mkdir(exist_ok=True)
layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
def mapgraph(name):
 d=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());l=next(x for x in layouts if x.get('id')==d['layout']);w,h=l['width'],l['height'];a=struct.unpack('<'+'H'*(w*h),(ROOT/l['blockdata_filepath']).read_bytes())
 free={(x,y) for y in range(h) for x in range(w) if not(a[y*w+x]>>10&3)}-{(o['x'],o['y']) for o in d['object_events']}
 return d,free,a,w
def reach(f,start,edges={}):
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]+edges.get((x,y),[]):
   if p in f and p not in seen:seen.add(p);q.append(p)
 return seen
m,f,_,_=mapgraph('VermilionCity_Gym');closed=reach(f-{(5,7)},(5,18));opened=reach(f,(5,18))
for p in [(2,12),(5,12),(8,12),(5,19)]:assert p in closed,p
assert (5,4) not in closed and (5,4) in opened and (5,18) in reach(f,(5,4))
for name,entry,goal in [('Dream',(7,12),(12,2)),('Memory',(7,12),(7,5)),('Vigil',(3,12),(11,3))]:
 d,f,_,_=mapgraph('VermilionCity_Mystery'+name)
 edges={(3,5):[(11,5)],(11,5):[(3,5)]} if name=='Vigil' else {}
 seen=reach(f,entry,edges);assert goal in seen,(name,goal)
 for e in d['bg_events']:
  if e['script'].endswith('_EventScript_Return'):assert (e['x'],e['y']+1) in seen,(name,e)
 if name=='Vigil':
  assert goal not in reach(f,entry)
  assert d['warp_events']==[dict(x=x,y=5,elevation=3,dest_map='MAP_VERMILION_CITY_MYSTERY_VIGIL',dest_warp_id=v) for x,v in [(3,'1'),(11,'0')]]
 assert not d['allow_escaping'] and not d['allow_cycling'] and d['map_type']=='MAP_TYPE_INDOOR'
# Prior chapter is an explicit permanent compatibility reference.
base='65b62bd88'
for path in ['data/maps/map_groups.json','data/layouts/layouts.json']:
 old=json.loads(subprocess.check_output(['git','show',base+':'+path],cwd=ROOT,text=True));new=json.loads((ROOT/path).read_text())
 if 'map_groups' in path:
  assert new['group_order']==old['group_order']
  for g in old['group_order']:assert new[g][:len(old[g])]==old[g],g
 else:assert [x.get('id') for x in new['layouts'][:len(old['layouts'])]]==[x.get('id') for x in old['layouts']]
assert 'sYokaiParty_LEADER_LT_SURGE[]' in (ROOT/'src/data/trainer_parties.h').read_text()
report={'passed':True,'scope':'Independent collision graph and source contracts; not a substitute for native runtime checks','checks':['Hub doors and exit reachable before gate, boss only afterwards and return route exists','All three distinct dimension objectives and return terminals reachable','Vigil objective requires actual pad pair between disconnected chambers','No escape/cycling or exterior map types in dimensions','Every previous map/layout ID retained; new IDs appended','Historical Surge boss party source retained'],'legacy_reference':base}
(out/'CONTROLE_SOURCES.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

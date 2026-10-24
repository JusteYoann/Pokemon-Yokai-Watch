#!/usr/bin/env python3
"""Audit reproductible des zones et de leurs composantes accessibles à pied.
Les échelles/escaliers normaux sont reliés; chutes, courants, eau et rochers
initiaux sont exclus des emplacements. Aucun événement original n'est modifié.
"""
import json,struct,re,sys
sys.setrecursionlimit(10000)
from collections import deque
from pathlib import Path
R=Path(__file__).resolve().parents[2]
layouts={x['id']:x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if 'id' in x}
names=[]
for prefix in ('MtMoon','RockTunnel','SeafoamIslands','VictoryRoad','CeruleanCave','MtEmber'):
 for p in sorted((R/'data/maps').glob(prefix+'*/map.json')):
  if p.parent.name in ('MtEmber_Exterior','MtEmber_Summit'):continue
  names.append(p.parent.name)
allmaps={n:json.loads((R/f'data/maps/{n}/map.json').read_text()) for n in names}
attrs={}
def loadattrs(label,primary=False):
 name=re.sub(r'(?<!^)(?=[A-Z])','_',label.removeprefix('gTileset_')).lower()
 p=R/'data/tilesets'/('primary' if primary else 'secondary')/name/'metatile_attributes.bin'
 b=p.read_bytes();return struct.unpack('<'+'I'*(len(b)//4),b)
# Native attribute low nine bits are metatile behavior; collision bits10..11.
walktypes={0,2,8,10,11,12,0x20,0x21,0x23,0x2a,0x2b,0x60,0x61,0x67,0x69,0x6c,0x6d,0x6e,0x6f}
compid=1;rows=[];out=[];edges=set();info={}
for name,d in allmaps.items():
 l=layouts[d['layout']];w,h=l['width'],l['height'];raw=(R/l['blockdata_filepath']).read_bytes();tiles=struct.unpack('<'+'H'*(len(raw)//2),raw)
 pri=loadattrs(l['primary_tileset'],True);sec=loadattrs(l['secondary_tileset']);beh=[]
 for t in tiles:
  v=t&1023;beh.append((pri[v] if v<640 else sec[v-640])&511)
 walk={i for i,t in enumerate(tiles) if (t>>10)&3==0 and beh[i] in walktypes}
 for o in d['object_events']:
  if o['graphics_id']=='OBJ_EVENT_GFX_PUSHABLE_BOULDER':walk.discard(o['y']*w+o['x'])
 labels=[0]*(w*h);comps={}
 for start in sorted(walk):
  if labels[start]:continue
  q=deque([start]);labels[start]=compid;cells=[]
  while q:
   a=q.popleft();cells.append(a)
   for b in (a-w,a+w,a-1,a+1):
    if b in walk and not labels[b] and abs(b%w-a%w)+abs(b//w-a//w)==1 and ((tiles[a]>>12)==(tiles[b]>>12) or not tiles[a]>>12 or not tiles[b]>>12):labels[b]=compid;q.append(b)
  comps[compid]=cells;compid+=1
 # Articulation cells are never occupied by the door, patrols or rewards.
 visited={};low={};parent={};articulation=set();counter=[0]
 def articulation_visit(a):
  counter[0]+=1;visited[a]=low[a]=counter[0];children=0
  for b in (a-w,a+w,a-1,a+1):
   if b not in walk or labels[b]!=labels[a] or abs(b%w-a%w)+abs(b//w-a//w)!=1:continue
   if b not in visited:
    parent[b]=a;children+=1;articulation_visit(b);low[a]=min(low[a],low[b])
    if a not in parent and children>1:articulation.add(a)
    if a in parent and low[b]>=visited[a]:articulation.add(a)
   elif parent.get(a)!=b:low[a]=min(low[a],visited[b])
 for a in sorted(walk):
  if a not in visited:articulation_visit(a)
 candidates=[];warps={(o['x'],o['y']) for o in d['warp_events']}
 for co,cells in comps.items():
  if len(cells)<40:continue
  choices=[]
  for a in cells:
   if a in articulation:continue
   x,y=a%w,a//w
   if beh[a] not in (0,2,8,10,11,12,0x21,0x2b):continue
   if any(abs(x-u)+abs(y-v)<3 for u,v in warps):continue
   ns=sum(b in walk and abs(b%w-x)+abs(b//w-y)==1 for b in (a-w,a+w,a-1,a+1))
   if ns>=3:choices.append((x,y,co))
  # Well spaced, finite reviewed candidate set, at most eight per component.
  chosen=[]
  for pt in choices:
   if all(abs(pt[0]-p[0])+abs(pt[1]-p[1])>=6 for p in chosen):chosen.append(pt)
   if len(chosen)==8:break
  candidates+=chosen
 # Exact finite component diameter: conservative door travel bound.
 diameters={}
 for co,cells in comps.items():
  diameter=0
  for source in cells:
   distance={source:0};queue=deque([source])
   while queue:
    a=queue.popleft()
    for b in (a-w,a+w,a-1,a+1):
     if 0<=b<w*h and labels[b]==co and b not in distance and abs(b%w-a%w)+abs(b//w-a//w)==1:
      distance[b]=distance[a]+1;queue.append(b)
   diameter=max(diameter,max(distance.values()))
  diameters[co]=diameter
 info[name]={'w':w,'h':h,'labels':labels,'comps':comps,'candidates':candidates,'tiles':tiles,'diameters':diameters}
 rows.append({'map':name,'width':w,'height':h,'walkable':len(walk),'components':[len(c) for c in comps.values()],'candidates':candidates,'pursuers':max(map(len,comps.values()))>=120 and len(candidates)>=5 and w>=12 and h>=12,'warps':d['warp_events']})
# Warp edges are only bidirectional, safe walking staircases. Dropping holes do not count.
for name,d in allmaps.items():
 a=info[name]
 for warp in d['warp_events']:
  dest=warp['dest_map'].removeprefix('MAP_');target=next((n for n,dd in allmaps.items() if dd['id']==warp['dest_map']),None)
  if not target:continue
  dd=allmaps[target];idx=int(warp['dest_warp_id'])
  if idx>=len(dd['warp_events']):continue
  back=dd['warp_events'][idx]
  if back['dest_map']!=d['id']:continue
  b=info[target];ca=a['labels'][warp['y']*a['w']+warp['x']];cb=b['labels'][back['y']*b['w']+back['x']]
  if ca and cb:edges.add(tuple(sorted((ca,cb))))
# Require short paths across the component graph; each edge represents an explored staircase.
assert compid<256,compid
caves={p:i+1 for i,p in enumerate(('MtMoon','RockTunnel','SeafoamIslands','VictoryRoad','CeruleanCave','MtEmber'))}
for name in names:
 a=info[name];ident=re.sub(r'[^a-zA-Z0-9]','_',name)
 out.append(f'static const u8 sThLabels_{ident}[] = {{'+','.join(map(str,a['labels']))+'};')
 out.append(f'static const struct ThPoint sThPoints_{ident}[] = {{'+(','.join('{%d,%d,%d}'%p for p in a['candidates']) or '{0,0,0}')+'};')
out.append('static const struct ThMap sThMaps[] = {')
for i,name in enumerate(names):
 a=info[name];d=allmaps[name];row=rows[i];cave=next(v for k,v in caves.items() if name.startswith(k))
 out.append('{MAP_GROUP('+d['id']+'),MAP_NUM('+d['id']+'),%d,%d,%d,%d,sThLabels_%s,sThPoints_%s,%d},'%(a['w'],a['h'],cave,int(row['pursuers']),name,name,len(a['candidates'])))
out.append('};')
diameters=[0]*compid
for a in info.values():
 for co,diameter in a['diameters'].items():diameters[co]=diameter
out.append('static const u16 sThDiameters[] = {'+','.join(map(str,diameters))+'};')
out.append('static const u8 sThEdges[][2] = {'+','.join('{%d,%d}'%e for e in sorted(edges))+'};')
(R/'src/data/terre_heure_maps.h').write_text('// Generated by tools/yokai/auditer_grottes_terreur.py\n'+'\n'.join(out)+'\n')
p=R/'docs/terre-heure-20261025';p.mkdir(exist_ok=True)
(p/'AUDIT_GROTTES.json').write_text(json.dumps({'maps':rows,'components':compid-1,'stair_edges':sorted(edges),'excluded':['DiglettsCave','MtEmber_Exterior','MtEmber_Summit']},ensure_ascii=False,indent=2)+'\n')
print(len(rows),'cartes;',compid-1,'composantes;',len(edges),'liaisons réciproques')

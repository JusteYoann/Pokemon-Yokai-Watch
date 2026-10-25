#!/usr/bin/env python3
"""Vérifie les choix natifs de portes contre un BFS Python indépendant et le rattrapage à trois pas."""
import hashlib,json,struct
from collections import deque
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-nathan-patrouilles-20261025';graph=json.loads((P/'GRAPHE_DISTANCES.json').read_text());rows=json.loads((ROOT/'docs/terre-heure-20261025/AUDIT_GROTTES.json').read_text())['maps'];ms=graph['maps'];ss={(a,x,y):(b,u,v) for a,x,y,b,u,v in graph['stairs']}
safe_keys={(a,x,y) for a,x,y,b,u,v in graph['safe_stairs']}
r=new_game();checks=[];th=r.symbols['sTh'];samples=[]
def passed(s):checks.append(s);print('PASS',s,flush=True)
def distances(start,safe=False):
 q=deque([start]);d={start:0}
 while q:
  m,x,y=q.popleft();row=ms[m];e=row['edges'][y*row['width']+x]
  for i,(dx,dy) in enumerate(((0,1),(0,-1),(-1,0),(1,0))):
   if not e>>i&1:continue
   if safe and (m,x+dx,y+dy) in ss and (m,x+dx,y+dy) not in safe_keys:continue
   if safe and not row['safe_labels'][(y+dy)*row['width']+x+dx]:continue
   n=ss.get((m,x+dx,y+dy),(m,x+dx,y+dy))
   if n[0]==255 or n in d:continue
   if safe and not ms[n[0]]['safe_labels'][n[2]*ms[n[0]]['width']+n[1]]:continue
   d[n]=d[(m,x,y)]+1;q.append(n)
 return d
try:
 for m,row in enumerate(rows):
  if not row['pursuers'] or not row['candidates']:continue
  x,y,_=row['candidates'][0];d=distances((m,x,y));safe=distances((m,x,y),True)
  eligible={(n,u,vv):d.get((n,u,vv),65535) for n,v in enumerate(ms) if n!=m for u,vv in v['door_candidates'] if d.get((n,u,vv),65535)!=65535 and safe.get((n,u,vv),65535)<65534}
  best=max(eligible.values(),default=0)
  for seed in range(3):
   r.call('SeedRng',seed);ok=r.call('ChooseDoor',m,x,y)
   assert bool(ok)==bool(eligible),(row['map'],len(eligible),ok)
   if ok:
    dm=r.read(th+179,1)[0];u,v=r.read(th+192,2);assert eligible[(dm,u,v)]==best
    samples.append({'depart':row['map'],'porte':rows[dm]['map'],'distance_minimale':d[(dm,u,v)]})
  passed(row['map']+(': porte la plus éloignée sur un autre étage, vérifiée sur tous les emplacements viables' if eligible else ': aucun autre étage accessible, déclenchement reporté'))
 # Actual exit approach: favorable timer still running must never be anticipated.
 r.call('CreateMon',r.symbols['gPlayerParty'],1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96)
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());g=groups['group_order'].index('gMapGroup_Dungeons');n=groups['gMapGroup_Dungeons'].index('MtMoon_1F')
 r.call('VarSet',0x40fa,0x101);r.call('VarSet',0x40fb,73);r.call('SetWarpDestination',g,n,255,18,34);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
 assert r.call('ThreeStepsFromExit',0,18,34)
 assert not r.call('ThreeStepsFromExit',0,18,35)
 assert not r.call('TerreHeureTryStep') and r.call('VarGet',0x40fb)==73
 passed('Trois pas avant la sortie: un tirage favorable avec 73 pas restants ne provoque aucune anticipation')
 r.call('VarSet',0x40fb,0x100);r.write(th+162,b'\xff\xff');r.write(th+178,b'\0');r.write(th+160,struct.pack('<H',18|(34<<8)))
 assert r.call('TerreHeureTryStep') and r.read(th+175,1)==b'\1'
 dm=r.read(th+179,1)[0];u,v=r.read(th+192,2);d=distances((0,18,34));assert dm!=0 and d[(dm,u,v)]>0
 passed('Seuil déjà atteint et essai précédemment bloqué: nouvelle tentative prioritaire à trois pas, avec porte sur un autre étage, la plus éloignée disponible')
finally:
 (P/'TESTS_DISTANCES.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':checks,'portes_tirees':samples},ensure_ascii=False,indent=2)+'\n');r.close()

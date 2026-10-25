#!/usr/bin/env python3
"""Retours de combats isolés : routes natives, obstacles, Coupe, acteurs/palettes et crédits."""
import json,struct,hashlib
from PIL import Image
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/'docs/postgame-corrections-terminyanator-20261025';D.mkdir(exist_ok=True);checks=[]
base=[(1,'LavenderTown','PG_ScientistWin1','LOCALID_PG_SCIENTIST_LAV'),(2,'VermilionCity','PG_ScientistWin2','LOCALID_PG_SCIENTIST_PORT'),(3,'SaffronCity','PG_ScientistWin3','LOCALID_PG_SCIENTIST_YOPPLE')]
for index,mp,script,local,dx,dy,cut_before in [(*row,dx,dy,False) for row in base for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]]+[(*base[1],0,1,True)]:
 q=QA('TEMP.json');r=q.r
 try:
  q.mon();q.f(0x82c);q.f(0x322);r.call('VarSet',0x40f3,1);r.call('VarSet',0x40f4,3)
  for flag in ['FLAG_PG_SCIENTIST_1','FLAG_PG_SCIENTIST_2'][:index-1]:q.f(flag)
  target=next(o for o in json.loads((ROOT/f'data/maps/{mp}/map.json').read_text())['object_events'] if o.get('local_id')==local);x,y=target['x'],target['y'];q.warp(mp,x+dx,y+dy);r.run(120)
  if r.call('MapGridGetCollisionAt',x+dx+7,y+dy+7):continue
  if cut_before:r.call('RemoveObjectEventByLocalIdAndMap',7,q.maps[mp][1],q.maps[mp][0]);q.f(0x12)
  w,h,v=struct.unpack('<III',r.read(r.symbols['VMap'],12));tiles=struct.unpack('<'+'H'*(w*h),r.read(v,w*h*2));actor=q.local(local)
  q.script(script);steps=[];last=None;removed=False;frames=[]
  for f in range(20000):
   actors=q.actors()
   if actor in actors:
    a=actors[actor];xy=struct.unpack('<hh',r.read(a+16,4))
    if xy!=last:
     assert tiles[xy[1]*w+xy[0]]>>10&3==0,(mp,'wall',xy)
     if last:assert abs(xy[0]-last[0])+abs(xy[1]-last[1])==1,(mp,'teleport',last,xy)
     assert all(xy!=struct.unpack('<hh',r.read(b+16,4)) for k,b in actors.items() if k!=actor),(mp,'actor collision',xy)
     steps.append([xy[0]-7,xy[1]-7]);last=xy
   else:removed=True
   if f%6==0:frames.append(r.frame.resize((480,320),Image.Resampling.NEAREST))
   if removed and q.idle():break
   r.keys={8} if f%16<2 else set();r.run()
  else:raise AssertionError((mp,'departure timeout',steps))
  assert len(steps)>3 and (abs(steps[-1][0]-(x+dx))>9 or abs(steps[-1][1]-(y+dy))>7),(mp,'not offscreen',steps)
  if index==2:assert 7 not in q.actors() and q.fg(0x12),(mp,'tree not cut')
  if (dx,dy)==(0,1) and not cut_before:frames[0].save(D/f'scientifique-{index}-depart.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
  checks.append(dict(scene=mp,player_approach=[dx,dy],tree_already_cut=cut_before,steps=steps,all_floor=True,no_actor_overlap=True,removed_only_offscreen=True,cut_tree=index==2));print('PASS',mp,len(steps),flush=True)
 finally:r.close()
(D/'TESTS_DEPARTS.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks),ensure_ascii=False,indent=2)+'\n')

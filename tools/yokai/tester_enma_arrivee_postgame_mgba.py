#!/usr/bin/env python3
"""Sorties réelles de la maison, scène et trajet natifs, deux protagonistes.
La Ligue terminée et l'équipe sont préparées ; aucun PNJ ou déplacement imposé
pendant la cinématique. Observation des collisions et cases bloquées par image.
"""
import hashlib,json,struct
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/'docs/enma-arrivee-postgame-20261025';D.mkdir(exist_ok=True)
rows=[]
for gender in (0,1):
 q=QA('TEMP.json');r=q.r;original=r.run;trace=[];collisions=[];walls=[];visible=False;talk=False;previous=None;facings=set();stopped=0
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));q.mon();q.f(0x82c)
  q.warp('PalletTown_PlayersHouse_1F',4,7);r.run(240)
  assert q.fg('FLAG_PG_ENMA_INTRO_PENDING')
  def flag(name):
   f=q.flags[name];return bool(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+f//8,1)[0]&(1<<(f%8)))
  def position(a):return tuple(v-7 for v in struct.unpack('<hh',r.read(a+16,4)))
  def observed(n=1):
   global visible,talk,previous,stopped
   for _ in range(n):
    original()
    if tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))!=q.maps['PalletTown'] or q.callback()!='CB2_Overworld':continue
    actors=q.actors();enma=actors.get(4)
    if enma is None:continue
    visible=True;p=position(enma)
    if not trace:
     trace.append(tuple(v-7 for v in struct.unpack('<hh',r.read(enma+12,4))))
     r.frame.save(D/f'{gender}-depart-nord.png')
    facings.add(r.read(enma+24,1)[0]&15)
    bank=r.read(r.symbols['gSprites']+68*r.read(enma+4,1)[0]+5,1)[0]>>4
    assert r.read(r.symbols['gPlttBufferUnfaded']+512+bank*32,32)==r.read(r.symbols['gObjectEventPal_YokaiEnma'],32)
    if not trace or p!=trace[-1]:trace.append(p)
    for local,a in actors.items():
     if local!=4 and p==position(a):collisions.append((p,local))
    w,h,ptr=struct.unpack('<III',r.read(r.symbols['VMap'],12));tile=int.from_bytes(r.read(ptr+2*((p[1]+7)*w+p[0]+7),2),'little')
    if tile>>10&3:walls.append(p)
    
    player=position(actors[255]);expected=(player[0],player[1]+2)
    if p==expected and not talk:
     talk=True
    stopped=stopped+1 if p==expected and r.read(enma+24,1)[0]&15==2 else 0
    if stopped==360:r.frame.save(D/f'{gender}-devant-maison.png')
    previous=p
  r.run=observed
  r.keys={5};r.run(48);r.keys=set()
  for f in range(18000):
   if flag('FLAG_PG_ENMA_INTRO') and q.idle():break
   r.keys={8} if f%20<2 and not (0<stopped<360) else set();r.run()
  else:raise AssertionError(('Scène bloquée',trace[-6:],q.callback()))
  assert facings=={1,2,3,4},facings
  assert visible and talk and not collisions and not walls,(visible,talk,collisions,walls)
  assert trace[0] in ((12,1),(13,1)) and trace[-1] in ((12,1),(13,1)),trace
  assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in zip(trace,trace[1:])),trace
  assert 4 not in q.actors() and not flag('FLAG_PG_ENMA_INTRO_PENDING')
  r.frame.save(D/f'{gender}-scene-terminee.png')
  # Revisit: native completed flag suppresses a second arrival.
  q.warp('PalletTown_PlayersHouse_1F',4,7);r.keys={5};r.run(48);r.keys=set();r.run(600)
  assert 4 not in q.actors() and q.idle()
  row=dict(gender=gender,from_house_by_controller=True,north_start=trace[0],route=trace,zero_actor_collisions=True,zero_blocked_tiles=True,stops_in_front=True,all_four_facings=True,royal_palette_preserved=True,walks_back_north=True,hidden_after_departure=True,not_repeated=True)
  rows.append(row);print('PASS',gender,len(trace),flush=True)
 finally:r.run=original;r.close()
(D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256((ROOT/'pokefirered_audio.gba').read_bytes()).hexdigest(),scope=__doc__,cases=rows),ensure_ascii=False,indent=2)+'\n')

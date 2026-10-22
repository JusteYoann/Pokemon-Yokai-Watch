#!/usr/bin/env python3
"""Real present/past doors, counterpart champion, bridges, era return and travel guards."""
import hashlib,json,re
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_lavanville_scenario_mgba as lv
from tester_safrania_scenario_mgba import warp,walk,pos,location,face_a,finish,save_continue,flag,C
OUT=ROOT/'QA_RECETTE_FINALE/CRAMOIS_SCENARIO_2026';OUT.mkdir(exist_ok=True);lv.s.t.az.a.OUT=OUT
MAPS=lv.MAPS;rows=[];TM=int(re.search(r'#define FLAG_GOT_TM38_FROM_BLAINE\s+(0x[\dA-Fa-f]+)',(ROOT/'include/constants/flags.h').read_text())[1],16)
def party(r,weak=False):
 members=[(5,1)] if weak else [(7,49),(88,49),(8,48),(10,48)]
 for i,(sp,level) in enumerate(members):
  p=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',p,sp,level,15,1,100+i,0,0)
  moves=[r.call('GetMonData',p,13+j,0) for j in range(4)];prefer=['MOVE_THUNDERBOLT','MOVE_SILVER_WIND','MOVE_BRICK_BREAK','MOVE_WATER_PULSE','MOVE_FLAMETHROWER','MOVE_NIGHT_SHADE','MOVE_SIGNAL_BEAM','MOVE_FLAME_WHEEL','MOVE_SHADOW_BALL','MOVE_BUBBLE_BEAM','MOVE_WATER_GUN']
  moves.sort(key=lambda m:next((j for j,k in enumerate(prefer) if m==C[k]),100 if m else 101))
  for j,m in enumerate(moves):r.call('SetMonMoveSlot',p,m,j)
 r.write(r.symbols['gPlayerPartyCount'],bytes([len(members)]));r.call('SetLastHealLocationWarp',9)
def route(r,name,target):
 # Island water has elevation7; ordinary paths use3. Never plan a walking route over it.
 old=lv.actors
 try:
  # Independent route search using native collision + water predicates, not engine warps.
  from collections import deque
  from pathlib import Path
  import struct
  d=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());l=next(l for l in lv.LAY if l.get('id')==d['layout']);w,h=l['width'],l['height'];a=struct.unpack('<'+'H'*(w*h),(ROOT/l['blockdata_filepath']).read_bytes());free={(x,y) for y in range(h) for x in range(w) if not(a[y*w+x]>>10&3) and a[y*w+x]>>12!=7}
  # Include both alternate champion templates as blockers, even if off camera.
  for o in d['object_events']:free.discard((o['x'],o['y']))
  for e in d['warp_events']:
   if (e['x'],e['y'])!=target:free.discard((e['x'],e['y']))
  q=deque([pos(r)]);prev={pos(r):None}
  while q:
   p=q.popleft()
   if p==target:break
   for key,dx,dy in [('U',0,-1),('D',0,1),('L',-1,0),('R',1,0)]:
    v=(p[0]+dx,p[1]+dy)
    if v in free and v not in prev:prev[v]=(p,key);q.append(v)
  assert target in prev,(name,pos(r),target)
  moves=[];p=target
  while prev[p] is not None:p,key=prev[p];moves.append(key)
  for key in moves[::-1]:walk(r,key)
  r.run(180)
 finally:lv.actors=old
def enter_present(r):
 warp(r,3,8,8,4);walk(r,'U');r.run(600);assert location(r)==MAPS['PokemonMansion_1F']
 if pos(r)==(8,33):walk(r,'U')
 assert pos(r)==(8,32),pos(r)
def leave_down(r,expected):
 r.keys={5};r.run(100);r.keys=set();r.run(600);assert location(r)==MAPS[expected],(location(r),pos(r))
def main():
 for gender,name in [(0,'nathan'),(1,'katie')]:
  r=new_game(gender)
  try:
   party(r);enter_present(r);face_a(r,'U');finish(r);assert not flag(r,0x347)
   r.call('FlagSet',0x345);r.call('FlagSet',0x344);r.call('FlagSet',0x33D)
   face_a(r,'U');lv.s.decline(r);assert location(r)==MAPS['PokemonMansion_1F']
   face_a(r,'U');finish(r);assert location(r)==MAPS['CinnabarPast_Mansion'] and pos(r)==(7,6) and flag(r,0x347)
   face_a(r,'U');finish(r);assert location(r)==MAPS['CinnabarPast_Mansion'] and not flag(r,0x346)
   save_continue(r);assert pos(r)==(7,6)
   walk(r,'D',6);leave_down(r,'CinnabarPast');assert pos(r) in [(8,4),(8,5)],pos(r)
   r.frame.save(OUT/(name+'-ile-passee.png'))
   route(r,'CinnabarPast',(20,5));walk(r,'U');r.run(600);assert location(r)==MAPS['CinnabarPast_Gym']
   if pos(r)==(7,17):walk(r,'U')
   assert pos(r)==(7,16),pos(r)
   walk(r,'L',4);walk(r,'U',6);face_a(r,'U');finish(r);assert flag(r,0x348)
   # Actually cross the newly opened west shortcut and back.
   walk(r,'D');walk(r,'R',4);walk(r,'D',2);walk(r,'U',2)
   save_continue(r);assert flag(r,0x348) and not flag(r,0x349)
   walk(r,'R',4);walk(r,'U',7);face_a(r,'U');finish(r);assert flag(r,0x349)
   walk(r,'L',4);walk(r,'D',3);save_continue(r);walk(r,'U',4);assert pos(r)==(7,3),pos(r)
   r.frame.save(OUT/(name+'-champion.png'))
   if not gender:assert r.call('AddBagItem',C['ITEM_TM38'],999)
   face_a(r,'U');frames=lv.s.t.az.a.fight(r,name,expected=[(21,44),(67,44),(85,45),(32,45),(149,46)])
   assert flag(r,0x346) and flag(r,0x826) and not flag(r,0x827) and r.call('HasTrainerBeenFought',748 if gender else 747)
   assert not r.call('HasTrainerBeenFought',747 if gender else 748)
   if not gender:
    assert not flag(r,TM);r.call('RemoveBagItem',C['ITEM_TM38'],1);face_a(r,'U');finish(r)
   assert flag(r,TM);before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
   save_continue(r);assert pos(r)==(7,3) and flag(r,0x346)
   walk(r,'D',13);leave_down(r,'CinnabarPast');assert pos(r) in [(20,5),(20,6)],pos(r)
   route(r,'CinnabarPast',(8,4));walk(r,'U');r.run(600);assert location(r)==MAPS['CinnabarPast_Mansion']
   if pos(r)==(7,13):walk(r,'U')
   walk(r,'U',6);assert pos(r)==(7,6),pos(r)
   face_a(r,'U');lv.s.decline(r);assert location(r)==MAPS['CinnabarPast_Mansion']
   face_a(r,'U');finish(r);assert location(r)==MAPS['PokemonMansion_1F'] and pos(r)==(8,32) and flag(r,0x34E)
   save_continue(r);assert pos(r)==(8,32)
   face_a(r,'U');finish(r);assert location(r)==MAPS['CinnabarPast_Mansion']
   face_a(r,'U');finish(r);assert location(r)==MAPS['PokemonMansion_1F']
   rows.append({'test':name+' real present Mansion entrance, sixth/bell requirement, No/Yes time travel, initial return refused, past island/arena doors, both valves and actual shortcut crossings, native five-partner counterpart battle, seventh only, pending/unique TM, Flash/Continue and voluntary free era revisits','passed':True,'battle_frames':frames})
  finally:r.close()
 (OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Explicit ordinary Komastar49/Appak49/Whisper48/Cigallard48, IV15/native stats, learned moves reordered; prior sixth/bell fixtures, not continuous adventure or exhaustive balance','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

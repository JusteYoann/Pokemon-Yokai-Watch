#!/usr/bin/env python3
"""Zombie contact, unchanged real Tower ascent, Alyzon, bell and Flash persistence."""
import hashlib,json,struct
from collections import deque
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_safrania_scenario_mgba as s
from tester_safrania_scenario_mgba import warp,walk,pos,location,face_a,finish,save_continue,flag,C
OUT=ROOT/'QA_RECETTE_FINALE/LAVANVILLE_SCENARIO_2026';OUT.mkdir(exist_ok=True);s.t.az.a.OUT=OUT
D=json.loads((ROOT/'data/maps/map_groups.json').read_text());MAPS={m:(D['group_order'].index(g),i) for g in D['group_order'] for i,m in enumerate(D[g])};LAY=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'];rows=[]
def party(r,weak=False):
 for i,(sp,lv) in enumerate([(5,1)] if weak else [(6,44),(8,43),(10,43)]):
  p=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',p,sp,lv,15,1,100+i,0,0)
  moves=[r.call('GetMonData',p,13+j,0) for j in range(4)];prefer=['MOVE_FLAMETHROWER','MOVE_FLAME_WHEEL','MOVE_NIGHT_SHADE','MOVE_SHADOW_BALL','MOVE_SIGNAL_BEAM','MOVE_EMBER']
  moves.sort(key=lambda m:next((j for j,k in enumerate(prefer) if m==C[k]),100 if m else 101))
  for j,m in enumerate(moves):r.call('SetMonMoveSlot',p,m,j)
 r.write(r.symbols['gPlayerPartyCount'],bytes([1 if weak else 3]));r.call('SetLastHealLocationWarp',5)
def actors(r):
 return [(r.read(r.symbols['gObjectEvents']+36*i+8,1)[0],r.read(r.symbols['gObjectEvents']+36*i+5,1)[0],struct.unpack('<hh',r.read(r.symbols['gObjectEvents']+36*i+16,4))) for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1]
def route(r,name,target):
 d=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());l=next(l for l in LAY if l.get('id')==d['layout']);w,h=l['width'],l['height'];a=struct.unpack('<'+'H'*(w*h),(ROOT/l['blockdata_filepath']).read_bytes());free={(x,y) for y in range(h) for x in range(w) if not(a[y*w+x]>>10&3)}
 for local,gfx,xy in actors(r):
  if local!=255:free.discard((xy[0]-7,xy[1]-7))
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
 r.run(600)
def main():
 # A real contact from the side opposite the zombie's facing direction.
 r=new_game()
 try:
  party(r);warp(r,3,4,18,7);finish(r);assert not flag(r,0x340)
  assert not any(g==185 for _,g,_ in actors(r))
  r.call('FlagSet',0x824);warp(r,3,4,13,10);finish(r)
  assert flag(r,0x340) and flag(r,0x341) and r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x2E,1) is not None
  # Position one native wandering object for a deterministic contact check.
  r.call('RemoveObjectEventByLocalIdAndMap',5,4,3);r.call('RemoveObjectEventByLocalIdAndMap',6,4,3)
  r.call('TryMoveObjectEventToMapCoords',4,4,3,13,8)
  actor=next(r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1 and r.read(r.symbols['gObjectEvents']+36*i+8,1)[0]==4)
  r.call('OverrideMovementTypeForObjectEvent',actor,7);r.call('ObjectEventTurn',actor,2)
  assert not any(g in [16,32,10] for local,g,_ in actors(r) if local!=255)
  r.frame.save(OUT/'nuit-zombies.png')
  # The first zombie must engage without pressing A.
  r.keys={4};r.run(20);r.keys=set()
  frames=s.t.az.a.fight(r,'zombie-contact',expected=[(42,34)])
  assert r.call('HasTrainerBeenFought',744) and flag(r,0x340) and not flag(r,0x345)
  save_continue(r);assert flag(r,0x340) and r.call('HasTrainerBeenFought',744)
  rows.append({'test':'Before fifth: ordinary humans/no zombies; after fifth: night and contact trainer without A, native battle and persisted calm state','passed':True,'battle_frames':frames})
 finally:r.close()
 for gender,name in [(0,'nathan'),(1,'katie')]:
  r=new_game(gender)
  try:
   party(r);r.call('FlagSet',0x824);r.call('FlagSet',0x32F);r.call('FlagSet',0x823)
   warp(r,3,4,18,7);finish(r);r.call('VarSet',0x4020,1000)
   # Real Tower door and all six native stair transitions, not a summit warp.
   walk(r,'U');r.run(600);assert location(r)==MAPS['PokemonTower_1F']
   for floor in range(1,7):
    mapname=f'PokemonTower_{floor}F';d=json.loads((ROOT/f'data/maps/{mapname}/map.json').read_text());e=next(e for e in d['warp_events'] if e['dest_map']==f'MAP_POKEMON_TOWER_{floor+1}F')
    route(r,mapname,(e['x'],e['y']));r.keys={7 if floor%2 else 6};r.run(45);r.keys=set();r.run(600);assert location(r)==MAPS[f'PokemonTower_{floor+1}F'],(floor,location(r),pos(r))
   route(r,'PokemonTower_7F',(11,7));save_continue(r);assert pos(r)==(11,7)
   r.frame.save(OUT/(name+'-alyzon.png'));face_a(r,'U');frames=s.t.az.a.fight(r,name,expected=[(42,39),(121,39),(70,40),(115,41)])
   assert flag(r,0x345) and flag(r,0x825) and flag(r,0x340) and not flag(r,0x33D)
   save_continue(r);assert flag(r,0x345) and flag(r,0x340)
   route(r,'PokemonTower_7F',(11,3));face_a(r,'U');s.decline(r);assert flag(r,0x340)
   face_a(r,'U');finish(r);assert location(r)==(3,4) and pos(r)==(18,7)
   assert flag(r,0x344) and flag(r,0x33D) and not flag(r,0x340) and flag(r,0x33F)
   assert not any(g==185 for _,g,_ in actors(r))
   save_continue(r);assert flag(r,0x345) and not flag(r,0x340)
   warp(r,3,4,12,13);assert any(g!=185 and local!=255 for local,g,_ in actors(r))
   r.frame.save(OUT/(name+'-retour-habitants.png'))
   rows.append({'test':name+' actual entrance and all six Tower stair transitions, native four-partner Alyzon battle and sixth trophy, no automatic night ending; bell No then Yes, return of humans, persistent completed night','passed':True,'battle_frames':frames})
  finally:r.close()
 (OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Explicit fifth-trophy and ordinary Komaous44/Whisper43/Cigallard43 fixtures, IV15; native battles/controls/Flash, not a continuous adventure or exhaustive balance','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

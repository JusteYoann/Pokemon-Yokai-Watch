#!/usr/bin/env python3
"""Carmin/Ariane native chapter, switches, gifts, rematch and engineered legacy saves.

New games plus explicit warps, badge/trainer flags and parties. Chapter victories
use ordinary generated stats/learned moves; the postgame fixture is boosted.
Not a continuous adventure or global balance test.
"""
import hashlib,json,os,struct,re
from pathlib import Path
from collections import deque
from mgba_new_game import new_game
from mgba_rpc import ROOT
import scenario_qa_helpers as a
from scenario_qa_helpers import warp,walk,pos,location,face_a,finish,idle,C
OUT=ROOT/'QA_RECETTE_FINALE/CARMIN_2026_10_22';OUT.mkdir(exist_ok=True);a.OUT=OUT
B2=0x821;B3=0x822;TM=0x231;WON=0x300;GIFT=0x301;POST=0x302;OPEN=0x264
rows=[];basekeys=a.battle_keys

def battle_keys(r,f):
 if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gMPlayInfo_BGM'])==r.carmin_theme:r.carmin_music_seen=True
 if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_UpdatePartyMenu']|1:
  if f%16>=4:return set()
  living=[i for i in range(r.read(r.symbols['gPlayerPartyCount'],1)[0]) if r.call('GetMonData',r.symbols['gPlayerParty']+100*i,57,0)>0]
  if not living:return {8}
  target=living[0];cur=r.read(r.symbols['gPartyMenu']+9,1)[0]
  return {8} if cur==target else ({7} if cur==0 else ({6} if target==0 else {5 if cur<target else 4}))
 result=basekeys(r,f)
 if f%16==0 and r.u32(r.symbols['gBattlerControllerFuncs']) in r.qa_move_callbacks:
  mask=r.call('CheckMoveLimitations',0,0,255)&15
  own=set(r.read(r.symbols['gBattleMons']+0x21,2));foe=set(r.read(r.symbols['gBattleMons']+88+0x21,2))
  scored=[]
  for slot in range(4):
   if mask&(1<<slot):continue
   move=int.from_bytes(r.read(r.symbols['gBattleMons']+12+slot*2,2),'little')
   if not move:continue
   _,power,kind,accuracy=r.read(r.symbols['gBattleMoves']+12*move,4)
   if not power:continue
   score=power*(1.5 if kind in own else 1)*(accuracy or 100)/100
   for j in range(0,336,3):
    attack,defend,scale=r.read(r.symbols['gTypeEffectiveness']+j,3)
    if attack>=254:break
    if attack==kind and defend in foe:score*=scale/10
   if move==252:score=-1 # Fake Out is unsuitable for repeated mid-battle selection.
   scored.append((score,-slot))
  if scored:
   target=-max(scored)[1];cur=r.read(r.symbols['gMoveSelectionCursor'],1)[0]
   r.qa_next_keys={8} if cur==target else ({7 if target&1 else 6} if (target&1)!=(cur&1) else {5 if target&2 else 4})
 return r.qa_next_keys if f%16<4 else set()
a.battle_keys=battle_keys

def flag(r,n):return bool(r.call('FlagGet',n))
def theme(r):
 r.carmin_theme=r.call('YokaiGetSongHeader',377,r.u32(r.symbols['gSongTable']+377*8));r.carmin_music_seen=False

def prepare(r,weak=False,post=False):
 for trainer in [141,220,423]:r.call('SetTrainerFlag',trainer) # isolate chapter from optional gym trainers
 members=[(5,1)] if weak else [(149,100)] if post else [(1,24),(5,24),(87,23)]
 for i,(species,level) in enumerate(members):
  mon=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',mon,species,level,15,1,100+i,0,0)
  moves=[r.call('GetMonData',mon,13+j,0) for j in range(4)]
  order=[C[x] for x in ['MOVE_EMBER','MOVE_FLAME_WHEEL','MOVE_WATER_GUN','MOVE_BUBBLE','MOVE_QUICK_ATTACK','MOVE_SCRATCH','MOVE_TACKLE']]
  moves=sorted(moves,key=lambda v:order.index(v) if v in order else 50 if v else 99)
  for j,v in enumerate(moves):r.call('SetMonMoveSlot',mon,v,j)
 if post:
  r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0)
  for name in ['HP','MAX_HP','ATK','DEF','SPATK','SPDEF']:
   r.w32(r.PARAMS+128,999);r.call('SetMonData',r.symbols['gPlayerParty'],C['MON_DATA_'+name],r.PARAMS+128)
 r.write(r.symbols['gPlayerPartyCount'],bytes([len(members)]));r.call('SetLastHealLocationWarp',5);theme(r)

def navigate(r,target):
 # Observe the actual buffered collision map and actor positions, no map writes.
 start=pos(r);w=r.u32(r.symbols['VMap']);h=r.u32(r.symbols['VMap']+4);p=r.u32(r.symbols['VMap']+8)
 grid=struct.unpack('<'+'H'*(w*h),r.read(p,w*h*2));free={(x,y) for x in range(11) for y in range(20) if not (grid[(y+7)*w+x+7]>>10&3)}
 for i in range(16):
  o=r.symbols['gObjectEvents']+36*i
  if r.read(o,1)[0]&1 and not(r.read(o+2,1)[0]&1):
   x,y=struct.unpack('<hh',r.read(o+16,4));free.discard((x-7,y-7))
 todo=deque([start]);prev={start:None}
 while todo:
  p=todo.popleft()
  if p==target:break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   nxt=(p[0]+dx,p[1]+dy)
   if nxt in free and nxt not in prev:prev[nxt]=p;todo.append(nxt)
 assert target in prev,('No native route',start,target)
 path=[];p=target
 while prev[p] is not None:path.append(p);p=prev[p]
 for nxt in reversed(path):
  x,y=pos(r);dx,dy=nxt[0]-x,nxt[1]-y;walk(r,{(1,0):'R',(-1,0):'L',(0,1):'D',(0,-1):'U'}[(dx,dy)])

def bin_press(r,n):
 x=1+2*((n-1)%5);y=10+2*((n-1)//5)
 navigate(r,(x,y+1));face_a(r,'U');finish(r)

def save_continue(r):
 assert r.call('TrySavingData',0,max_frames=1200)==1
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);r.keys=set();r.run(900);assert idle(r)

def solve(r):
 first=r.call('VarGet',0x4000);second=r.call('VarGet',0x4001);assert 1<=first<=15 and 1<=second<=15 and first!=second
 bin_press(r,first);assert flag(r,1) and not flag(r,OPEN)
 wrong=next(n for n in range(1,16) if n not in [first,second]);bin_press(r,wrong)
 assert not flag(r,1) and not flag(r,OPEN)
 first=r.call('VarGet',0x4000);second=r.call('VarGet',0x4001)
 bin_press(r,first);assert flag(r,1);bin_press(r,second);assert flag(r,OPEN)
 assert r.call('MapGridGetCollisionAt',12,13)==0 and r.call('MapGridGetCollisionAt',12,14)==0
 before=pos(r);save_continue(r);assert flag(r,OPEN) and pos(r)==before

def victory(r,stem,expected,loss=False):
 r.carmin_music_seen=False;face_a(r,'U');f=a.fight(r,stem,loss=loss,limit=35000,expected=expected)
 assert r.carmin_music_seen,'Dedicated Ariane BGM not observed during native battle'
 return f

for gender,name in [(0,'nathan'),(1,'katie')]:
 r=new_game(gender)
 try:
  prepare(r);warp(r,9,6,5,3)
  assert [r.read(r.symbols['gObjectEvents']+36*i+5,1)[0] for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1].count(152)==1
  assert r.call('MapGridGetCollisionAt',13,9)==0 # companion's floor at(6,2)
  face_a(r,'U');finish(r);assert not flag(r,B3) and not flag(r,WON)
  r.call('FlagSet',0x820);r.call('FlagSet',B2)
  warp(r,3,5,14,26);walk(r,'U');r.run(600);assert location(r)==(9,6)
  r.frame.save(OUT/(name+'-entree.png'));field_music=r.u32(r.symbols['gMPlayInfo_BGM'])
  solve(r);navigate(r,(5,3));r.frame.save(OUT/(name+'-ariane-usapyon.png'))
  if gender==0:assert r.call('AddBagItem',C['ITEM_TM34'],999)
  else:assert r.call('AddBagItem',C['ITEM_MOON_STONE'],999)
  frames=victory(r,name,[(96,18),(17,19),(51,21),(100,23)])
  assert flag(r,B3) and flag(r,0x4B2) and flag(r,WON)
  if gender==0:
   assert not flag(r,TM) and not flag(r,GIFT);r.call('RemoveBagItem',C['ITEM_TM34'],999)
   face_a(r,'U');finish(r)
  else:
   assert flag(r,TM) and not flag(r,GIFT);r.call('RemoveBagItem',C['ITEM_MOON_STONE'],999)
   face_a(r,'U');finish(r)
  assert flag(r,TM) and flag(r,GIFT) and r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],1)
  assert not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],2)
  if gender==0:assert r.call('CheckBagHasItem',C['ITEM_TM34'],1) and not r.call('CheckBagHasItem',C['ITEM_TM34'],2)
  before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
  save_continue(r);assert flag(r,B3) and flag(r,GIFT) and flag(r,TM)
  r.frame.save(OUT/(name+'-trophee.png'));r.run(240);assert r.u32(r.symbols['gMPlayInfo_BGM'])==field_music
  navigate(r,(5,18));walk(r,'D');r.keys={5};r.run(90);r.keys=set();r.run(600);assert location(r)==(3,5),(location(r),pos(r))
  rows.append(dict(test=name+' door, second-trophy guard, actual wrong/correct native switches, ordinary-party victory, third trophy, unique CT34/Moon Stone with saturated-stack retry, Continue, exit and exploration BGM return',passed=True,battle_frames=frames,dedicated_battle_theme=True))
 finally:r.close()

r=new_game()
try:
 prepare(r,weak=True);r.call('FlagSet',B2);r.call('FlagSet',OPEN);warp(r,9,6,5,3)
 frames=victory(r,'defaite',[(96,18),(17,19),(51,21),(100,23)],loss=True)
 assert not any(flag(r,f) for f in [B3,TM,WON,GIFT]) and flag(r,B2)
 rows.append(dict(test='Actual defeat awards no trophy/TM/gift; retry available',passed=True,battle_frames=frames))
finally:r.close()

r=new_game()
try:
 prepare(r);r.call('FlagSet',B2);r.call('FlagSet',B3);r.call('SetTrainerFlag',416)
 warp(r,9,6,5,3);r.call('FlagClear',0x32C);save_continue(r)
 assert pos(r)==(5,17) and flag(r,0x32C) and flag(r,B3)
 assert r.call('MapGridGetCollisionAt',12,13)==0
 navigate(r,(5,3));before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
 assert flag(r,TM) and flag(r,GIFT) and r.call('GetGameStat',9)==before
 save_continue(r);assert pos(r)==(5,3) and flag(r,GIFT)
 warp(r,3,44,57,8);r.call('FlagClear',0x32B);r.call('FlagClear',0x32A);before=pos(r);save_continue(r)
 assert pos(r)==before and flag(r,0x32B) and flag(r,0x32A)
 assert all(r.read(r.symbols['gObjectEvents']+36*i+5,1)[0] not in [152,153] for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1)
 r.frame.save(OUT/'route25-apres-migration.png')
 rows.append(dict(test='Engineered legacy Surge/Route25 saves: first Continue refreshes safe gym entry/hidden relocated actors, preserves badge and pending gifts; later Continue preserves position',passed=True))
finally:r.close()

r=new_game(1)
try:
 prepare(r,post=True)
 for f in [B2,B3,TM,GIFT,0x82C]:r.call('FlagSet',f)
 warp(r,9,6,5,3);before=r.call('GetGameStat',9);face_a(r,'U')
 for f in range(3000):
  r.keys={0} if f%16<4 else set();r.run()
  if f>60 and idle(r):break
 else:raise AssertionError('Rematch decline blocked')
 assert r.call('GetGameStat',9)==before and not flag(r,POST)
 frames=victory(r,'revanche',[(101,56),(28,57),(110,58),(30,59),(145,60)])
 assert flag(r,POST) and flag(r,WON) and not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],1)
 save_continue(r);assert flag(r,POST) and flag(r,GIFT)
 rows.append(dict(test='Optional postgame rematch: No declines; original five-member team, dedicated theme, no duplicate earned Moon Stone and Flash persistence',passed=True,battle_frames=frames,fixture='Hovernyan100 with stats999: event flow only'))
finally:r.close()
report=dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba')).read_bytes()).hexdigest(),results=rows)
(OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2),flush=True)

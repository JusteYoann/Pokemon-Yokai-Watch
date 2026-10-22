#!/usr/bin/env python3
"""Second-trophy chapter via actual inputs; progression/ordinary party fixtures."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_argenta_scenario_mgba as a
from tester_argenta_scenario_mgba import warp,walk,pos,location,face_a,finish,idle,C
OUT=ROOT/'QA_RECETTE_FINALE/AZURIA_SCENARIO_2026';OUT.mkdir(exist_ok=True);a.OUT=OUT
P=0x40F4;B1=0x820;B2=0x821;TM=0x297
rows=[]
_native_battle_keys=a.battle_keys
def battle_keys(r,frame):
 if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_UpdatePartyMenu']|1:
  if frame%16>=4:return set()
  living=[i for i in range(r.read(r.symbols['gPlayerPartyCount'],1)[0]) if r.call('GetMonData',r.symbols['gPlayerParty']+100*i,57,0)>0]
  if not living:return {8}
  target=living[0];current=r.read(r.symbols['gPartyMenu']+9,1)[0]
  if current==target:return {8}
  return {7} if current==0 else ({6} if target==0 else {5 if current<target else 4})
 return _native_battle_keys(r,frame)
a.battle_keys=battle_keys
def flag(r,n):return bool(r.call('FlagGet',n))
def tile(r,x,y):return r.call('MapGridGetMetatileIdAt',x+7,y+7)
def save_continue(r):
 assert r.call('TrySavingData',0,max_frames=1200)==1
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);r.keys=set();r.run(900);assert idle(r)
def party(r):
 members=[(87,20),(8,18),(45,18)]
 for i,(s,l) in enumerate(members):
  mon=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',mon,s,l,15,1,100+i,0,0)
  existing=[r.call('GetMonData',mon,13+j,0) for j in range(4)]
  preferred=['MOVE_WATER_GUN','MOVE_BUBBLE','MOVE_LICK','MOVE_SLUDGE','MOVE_SCRATCH','MOVE_TACKLE','MOVE_ASTONISH']
  moves=sorted(existing,key=lambda m:next((j for j,n in enumerate(preferred) if C[n]==m),100 if m else 101))
  for j,m in enumerate(moves):r.call('SetMonMoveSlot',mon,m,j)
 r.write(r.symbols['gPlayerPartyCount'],b'\x03');r.call('SetLastHealLocationWarp',4)
def gate(r):
 # Starts below the center hearth at (8,10); walk around it, not through it.
 walk(r,'R');walk(r,'U',2);walk(r,'L');walk(r,'U');finish(r)
 assert pos(r)==(8,8),pos(r)
def enter(r):
 warp(r,3,3,31,22);walk(r,'U');r.run(600);assert location(r)==(7,5),location(r)
 walk(r,'U');assert pos(r)==(8,17),pos(r)
def active_champions(r):
 result=[]
 for i in range(16):
  q=r.symbols['gObjectEvents']+36*i
  if r.read(q,1)[0]&1 and r.read(q+5,1)[0] in [156,157]:result.append(r.read(q+5,1)[0])
 return result
def main():
 for gender,name in [(0,'nathan'),(1,'katie')]:
  r=new_game(gender)
  try:
   party(r);enter(r);r.frame.save(OUT/(name+'-entree.png'))
   # Direct interaction also enforces access, independently of physical gate.
   warp(r,7,5,8,5);face_a(r,'U');finish(r)
   assert not flag(r,B2) and not r.call('HasTrainerBeenFought',415) and not r.call('HasTrainerBeenFought',21)
   assert active_champions(r)==[156 if gender else 157],active_champions(r)
   r.call('FlagSet',B1);face_a(r,'U');finish(r);assert not flag(r,B2)
   enter(r);walk(r,'U',7);gate(r) # zero hearths rejected
   walk(r,'R');walk(r,'D',2);walk(r,'L');face_a(r,'U');finish(r);assert r.call('VarGet',P)==0 # center too early
   walk(r,'D',2);walk(r,'L',3);walk(r,'U');face_a(r,'L');finish(r)
   assert r.call('VarGet',P)==1 and tile(r,4,11)==0x2E1
   before=pos(r);save_continue(r);assert pos(r)==before and r.call('VarGet',P)==1 and tile(r,4,11)==0x2E1
   # Genuine exit/re-entry retains the symbolic fire sequence.
   walk(r,'D',6);walk(r,'R',2);r.keys={5};r.run(100);r.keys=set();r.run(600)
   assert location(r)==(3,3),location(r)
   walk(r,'U');r.run(600);walk(r,'U',6);walk(r,'R',3);walk(r,'U')
   face_a(r,'R');finish(r);assert r.call('VarGet',P)==2 and tile(r,12,11)==0x2E1
   walk(r,'D');walk(r,'L',3);walk(r,'U',2);face_a(r,'U');finish(r)
   assert r.call('VarGet',P)==3 and tile(r,8,9)==0x2E1
   r.frame.save(OUT/(name+'-foyers.png'))
   walk(r,'R');walk(r,'U',2);walk(r,'L');walk(r,'U',3);assert pos(r)==(8,5)
   assert active_champions(r)==[156 if gender else 157]
   r.frame.save(OUT/(name+'-champion.png'))
   if not gender:assert r.call('AddBagItem',C['ITEM_TM03'],999)
   face_a(r,'U');frames=a.fight(r,name,expected=[(28,16),(8,16),(1,18)])
   assert flag(r,B2) and flag(r,B1) and flag(r,0x4B1)
   assert r.call('HasTrainerBeenFought',415) and r.call('HasTrainerBeenFought',21)
   assert flag(r,TM)==bool(gender)
   if not gender:
    assert r.call('RemoveBagItem',C['ITEM_TM03'],1)
    before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
    assert r.call('GetGameStat',9)==before and flag(r,TM) and r.call('CheckBagHasItem',C['ITEM_TM03'],999)
   else:assert r.call('CheckBagHasItem',C['ITEM_TM03'],1) and not r.call('CheckBagHasItem',C['ITEM_TM03'],2)
   before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
   save_continue(r);assert flag(r,B2) and flag(r,TM) and r.call('VarGet',P)==3
   r.frame.save(OUT/(name+'-trophee.png'))
   # All exit paths remain available after victory.
   walk(r,'D',3);walk(r,'R');walk(r,'D',4);walk(r,'L');walk(r,'D',5)
   r.keys={5};r.run(100);r.keys=set();r.run(600);assert location(r)==(3,3)
   rows.append({'test':name+' actual door/exit, opposite protagonist exclusively visible, first-trophy and hearth guards, wrong order, native Flash/Continue and re-entry persistence, actual battle/trophy/TM with full-bag retry and no duplication','passed':True,'battle_frames':frames})
  finally:r.close()
 (OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Actual controls inside chapter. Explicit first-trophy and ordinary party fixtures (Kappacap20, Whisper18, Nihilistik18; IV15; learned moves reordered). Not a continuous whole adventure or all-starter balancing.','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

if __name__=="__main__":main()

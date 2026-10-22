#!/usr/bin/env python3
"""Real door entry, three dimensions, native internal pads and third trophy."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_azuria_scenario_mgba as az
from tester_argenta_scenario_mgba import warp,walk,pos,location,face_a,finish,idle,C
OUT=ROOT/'QA_RECETTE_FINALE/CARMIN_SCENARIO_2026';OUT.mkdir(exist_ok=True);az.a.OUT=OUT
F=[0x32B,0x32C,0x32D];B1=0x820;B2=0x821;B3=0x822;TM=0x231
rows=[]
_native_finish=finish
def finish(r,*args,**kwargs):
 result=_native_finish(r,*args,**kwargs)
 # The callback can be idle before the warp fade has released field controls.
 r.keys=set();r.run(180)
 return result
def flag(r,n):return bool(r.call('FlagGet',n))
def party(r,weak=False):
 members=[(87,1)] if weak else [(87,26),(8,25),(45,24)]
 for i,(s,l) in enumerate(members):
  mon=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',mon,s,l,15,1,100+i,0,0)
  existing=[r.call('GetMonData',mon,13+j,0) for j in range(4)]
  preferred=['MOVE_WATER_PULSE','MOVE_WATER_GUN','MOVE_SHADOW_BALL','MOVE_LICK','MOVE_SLUDGE','MOVE_SCRATCH','MOVE_TACKLE','MOVE_ASTONISH']
  moves=sorted(existing,key=lambda m:next((j for j,n in enumerate(preferred) if C[n]==m),100 if m else 101))
  for j,m in enumerate(moves):r.call('SetMonMoveSlot',mon,m,j)
 r.write(r.symbols['gPlayerPartyCount'],bytes([len(members)]));r.call('SetLastHealLocationWarp',6)
def save_continue(r):
 # The native save menu captures the current camera view before writing Flash.
 r.call('SaveMapView')
 assert r.call('TrySavingData',0,max_frames=1200)==1
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);r.keys=set();r.run(900);assert idle(r)
def enter(r):
 warp(r,3,5,14,26);walk(r,'U');r.run(600);assert location(r)==(9,6)
 if pos(r)==(5,19):walk(r,'U')
 assert pos(r)==(5,18),pos(r)
def portal(r,x):
 # From a hub return point at y12 or initial entrance: normal floor routes.
 cx,cy=pos(r)
 if cy==18:
  walk(r,'R');walk(r,'U',6);cx,cy=pos(r)
 if cx!=x:walk(r,'R' if x>cx else 'L',abs(x-cx))
 face_a(r,'U');finish(r)
def return_sign(r,x=7):
 walk(r,'D');walk(r,'L');face_a(r,'U');finish(r);assert location(r)==(9,6),location(r)
def gate(r):
 # A fixed fixture for refusal checks, separately from the real route to victory.
 warp(r,9,6,5,8);walk(r,'U');finish(r);assert pos(r)==(5,8)
def main():
 for gender,name in [(0,'nathan'),(1,'katie')]:
  r=new_game(gender)
  try:
   party(r);enter(r);r.frame.save(OUT/(name+'-laboratoire.png'))
   portal(r,2);assert location(r)==(9,6) and not any(flag(r,f) for f in F)
   warp(r,9,6,5,4);face_a(r,'U');finish(r);assert not flag(r,B3)
   r.call('FlagSet',B1);r.call('FlagSet',B2);gate(r)
   enter(r);portal(r,2);assert location(r)==(9,8) and pos(r)==(7,12)
   before=pos(r);save_continue(r);assert location(r)==(9,8) and pos(r)==before
   r.frame.save(OUT/(name+'-songes.png'))
   # Leave unfinished through the actual fixed return sign, then re-enter.
   return_sign(r);assert not flag(r,F[0])
   portal(r,2);walk(r,'R',5);walk(r,'U',4);walk(r,'L',10);walk(r,'U',3);walk(r,'R',10);walk(r,'U',3)
   face_a(r,'U');finish(r);assert location(r)==(9,6) and flag(r,F[0]) and pos(r)==(2,12)
   # Cave clue and a genuinely wrong choice, then the correct central tablet.
   portal(r,5);assert location(r)==(9,9);walk(r,'U',2);face_a(r,'U');finish(r)
   walk(r,'L',2);walk(r,'U',5);walk(r,'L',2);face_a(r,'U');finish(r)
   assert location(r)==(9,9) and not flag(r,F[1])
   r.frame.save(OUT/(name+'-memoire.png'))
   walk(r,'R',4);before=pos(r);save_continue(r);assert pos(r)==before
   face_a(r,'U');finish(r);assert location(r)==(9,6) and flag(r,F[1]) and pos(r)==(5,12)
   # Native warp pad pair joins physically disconnected chambers, in both directions.
   portal(r,8);assert location(r)==(9,10) and pos(r)==(3,12)
   walk(r,'U',6);walk(r,'U');r.run(600);assert pos(r)==(11,5),pos(r)
   walk(r,'U');before=pos(r);save_continue(r);assert pos(r)==before
   r.frame.save(OUT/(name+'-veille.png'))
   walk(r,'D');r.run(600);assert pos(r)==(3,5),pos(r)
   walk(r,'D');walk(r,'U');r.run(600);assert pos(r)==(11,5),pos(r)
   walk(r,'U',2);face_a(r,'U');finish(r)
   assert location(r)==(9,6) and all(flag(r,f) for f in F) and pos(r)==(8,12)
   save_continue(r);assert all(flag(r,f) for f in F)
   # Actual route around the center console to Berenice.
   walk(r,'L',2);walk(r,'U',4);walk(r,'L');walk(r,'U',4);assert pos(r)==(5,4)
   r.frame.save(OUT/(name+'-berenice.png'))
   if not gender:assert r.call('AddBagItem',C['ITEM_TM34'],999)
   face_a(r,'U');frames=az.a.fight(r,name,expected=[(49,22),(56,22),(71,24)])
   assert flag(r,B3) and flag(r,0x4B2) and r.call('HasTrainerBeenFought',416)
   if not gender:
    assert not flag(r,TM);r.call('RemoveBagItem',C['ITEM_TM34'],1)
    before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
    assert flag(r,TM) and r.call('GetGameStat',9)==before and r.call('CheckBagHasItem',C['ITEM_TM34'],999)
   else:assert flag(r,TM) and r.call('CheckBagHasItem',C['ITEM_TM34'],1) and not r.call('CheckBagHasItem',C['ITEM_TM34'],2)
   before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
   save_continue(r);assert flag(r,B3) and flag(r,TM) and all(flag(r,f) for f in F)
   r.frame.save(OUT/(name+'-trophee.png'))
   walk(r,'D',4);walk(r,'R');walk(r,'D',10);walk(r,'L');r.keys={5};r.run(100);r.keys=set();r.run(600)
   assert location(r)==(3,5),location(r)
   rows.append({'test':name+' actual city door; missing second-trophy guards; three distinct dimensions reached via map interactions; wrong memory choice; fixed unfinished return; Flash/Continue inside every dimension and hub; native pad pair both directions; real ordinary-party boss victory, third trophy, unique TM/full-bag retry and exit','passed':True,'battle_frames':frames})
  finally:r.close()
 (OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Real chapter inputs with explicit first-two-trophy and ordinary party fixtures. Kappacap26, Whisper25, Nihilistik24; IV15, learned moves reordered. Not a continuous adventure or all-starter balance test.','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

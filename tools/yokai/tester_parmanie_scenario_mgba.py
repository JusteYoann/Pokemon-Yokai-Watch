#!/usr/bin/env python3
"""Native investigation, actual fourth/fifth gates, rewards and legacy Continue."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_safrania_scenario_mgba as s
from tester_safrania_scenario_mgba import warp,walk,pos,location,face_a,finish,idle,save_continue,flag,C
OUT=ROOT/'QA_RECETTE_FINALE/PARMANIE_SCENARIO_2026';OUT.mkdir(exist_ok=True);s.t.az.a.OUT=OUT
F=[0x338,0x339,0x33A,0x33B];B5=0x824;TM=0x259;rows=[]
def party(r,weak=False):
 members=[(5,1)] if weak else [(49,38),(6,38),(8,37)]
 for i,(sp,lv) in enumerate(members):
  p=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',p,sp,lv,15,1,100+i,0,0)
  moves=[r.call('GetMonData',p,13+j,0) for j in range(4)]
  preferred=['MOVE_PSYBEAM','MOVE_PSYCHIC','MOVE_CONFUSION','MOVE_FLAME_WHEEL','MOVE_FLAMETHROWER','MOVE_NIGHT_SHADE','MOVE_EMBER']
  moves.sort(key=lambda m:next((j for j,k in enumerate(preferred) if m==C[k]),100 if m else 101))
  for j,m in enumerate(moves):r.call('SetMonMoveSlot',p,m,j)
 r.write(r.symbols['gPlayerPartyCount'],bytes([len(members)]));r.call('SetLastHealLocationWarp',8)
def enter(r):
 warp(r,3,7,9,33);walk(r,'U');r.run(600);assert location(r)==(11,3)
 if pos(r)==(7,21):walk(r,'U')
 assert pos(r)==(7,20),pos(r)
def main():
 for gender,name in [(0,'nathan'),(1,'katie')]:
  r=new_game(gender)
  try:
   party(r);enter(r);r.frame.save(OUT/(name+'-commissariat.png'))
   walk(r,'L',4);walk(r,'U',4);face_a(r,'U');finish(r);assert not flag(r,F[0])
   r.call('FlagSet',0x32F);r.call('FlagSet',0x823)
   face_a(r,'U');finish(r);assert flag(r,F[0])
   walk(r,'L');walk(r,'U',5);walk(r,'R');face_a(r,'U');finish(r);assert flag(r,F[1])
   walk(r,'L');walk(r,'U',3);walk(r,'R',10);walk(r,'D',3);walk(r,'L');face_a(r,'U');finish(r);assert flag(r,F[2])
   walk(r,'R');walk(r,'D',6);walk(r,'L',5);face_a(r,'U');finish(r);assert not flag(r,F[3]) # Wrong YES answer.
   face_a(r,'U');s.decline(r);assert flag(r,F[3]);save_continue(r);assert all(flag(r,f) for f in F)
   r.frame.save(OUT/(name+'-rapport.png'))
   walk(r,'L');walk(r,'U',9);walk(r,'R');walk(r,'U',3);assert pos(r)==(7,5)
   if not gender:assert r.call('AddBagItem',C['ITEM_TM06'],999)
   face_a(r,'U');frames=s.t.az.a.fight(r,name,expected=[(116,34),(106,34),(119,35),(99,36)])
   assert flag(r,B5) and not flag(r,0x825) and r.call('HasTrainerBeenFought',418)
   if not gender:
    assert not flag(r,TM);r.call('RemoveBagItem',C['ITEM_TM06'],1);face_a(r,'U');finish(r)
   assert flag(r,TM);before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
   save_continue(r);assert pos(r)==(7,5) and flag(r,B5) and flag(r,TM)
   r.frame.save(OUT/(name+'-trophee.png'))
   walk(r,'D',10);walk(r,'L');walk(r,'D',5);walk(r,'R');r.keys={5};r.run(100);r.keys=set();r.run(600);assert location(r)==(3,7)
   rows.append({'test':name+' real entrance, clue/fourth guard, two witnesses, wrong/correct conclusion, Flash/Continue, four-partner battle, fifth trophy only, pending/unique TM and actual exit','passed':True,'battle_frames':frames})
  finally:r.close()
 r=new_game()
 try:
  party(r);warp(r,11,3,7,8);walk(r,'U');finish(r);assert pos(r)==(7,8)
  warp(r,11,3,7,5);face_a(r,'U');finish(r);assert not flag(r,B5)
  r.call('FlagSet',0x32F);face_a(r,'U');finish(r);assert not flag(r,B5)
  r.call('FlagSet',B5);r.call('FlagClear',0x337);r.call('SetObjEventTemplateCoords',1,12,16);save_continue(r)
  assert pos(r)==(7,20) and flag(r,B5) and flag(r,0x337)
  rows.append({'test':'No report: physical gate and direct champion interaction refused; engineered pre-chapter save rebuilt at safe entry retaining historical fifth trophy','passed':True})
 finally:r.close()
 (OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Explicit ordinary Baku38/Komaous38/Whisper37 party and prior trophy fixtures, IV15, native stats; actual controls and Flash/Continue, not continuous adventure or exhaustive balance','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Station inputs, native pad pairs, system order and fourth-trophy provenance."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_carmin_scenario_mgba as t
from tester_carmin_scenario_mgba import warp,walk,pos,location,face_a,finish,idle,save_continue,flag,C
OUT=ROOT/'QA_RECETTE_FINALE/SAFRANIA_SCENARIO_2026';OUT.mkdir(exist_ok=True);t.az.a.OUT=OUT
POWER=0x332;NAV=0x333;COMMS=0x334;TROPHY=0x32F;B3=0x822;B4=0x823;B6=0x825;TM=0x29A
rows=[]
def party(r,weak=False):
 members=[(5,1)] if weak else [(6,33),(8,32),(10,32)]
 for i,(s,l) in enumerate(members):
  mon=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',mon,s,l,15,1,100+i,0,0)
  moves=[r.call('GetMonData',mon,13+j,0) for j in range(4)]
  preferred=['MOVE_FLAME_WHEEL','MOVE_EMBER','MOVE_FLAMETHROWER','MOVE_NIGHT_SHADE','MOVE_SIGNAL_BEAM','MOVE_FURY_CUTTER','MOVE_SHADOW_PUNCH','MOVE_LICK','MOVE_SCRATCH','MOVE_TACKLE']
  moves.sort(key=lambda m:next((j for j,k in enumerate(preferred) if m==C[k]),100 if m else 101))
  for j,m in enumerate(moves):r.call('SetMonMoveSlot',mon,m,j)
 r.write(r.symbols['gPlayerPartyCount'],bytes([len(members)]));r.call('SetLastHealLocationWarp',11)
def decline(r):
 for f in range(5000):
  r.keys={0} if f%16<4 else set();r.run()
  if f>60 and idle(r):r.keys=set();r.run(180);return
 raise AssertionError('No option did not return')
def enter(r):
 warp(r,3,10,46,13);assert flag(r,0x335) # Only the gym entrance guard is removed.
 walk(r,'U');r.run(600);assert location(r)==(14,3)
 if pos(r)==(14,23):walk(r,'U')
 assert pos(r)==(14,22),pos(r)
def pad_up(r,x,start_y,dest):
 walk(r,'U');r.run(600);assert pos(r)==dest,(pos(r),dest)
def main():
 for gender,name in [(0,'nathan'),(1,'katie')]:
  r=new_game(gender)
  try:
   party(r)
   # Guards remain effective even if a fixture places the player past the gate.
   warp(r,14,3,14,5);face_a(r,'U');finish(r);assert not flag(r,TROPHY)
   for f in [0x820,0x821,B3]:r.call('FlagSet',f)
   enter(r);r.frame.save(OUT/(name+'-station.png'))
   walk(r,'U',4);walk(r,'R',10);pad_up(r,24,18,(24,10))
   # Navigation before energy is refused; native pad permits an immediate return.
   walk(r,'R');walk(r,'U',5);walk(r,'L');face_a(r,'U');finish(r);assert not flag(r,NAV)
   walk(r,'R');walk(r,'D',5);walk(r,'L');r.run(600);assert pos(r)==(24,17),pos(r)
   walk(r,'D');walk(r,'L',20);pad_up(r,4,18,(4,10))
   walk(r,'R',2);walk(r,'U',5);walk(r,'L',2);face_a(r,'U');finish(r)
   assert flag(r,POWER) and not flag(r,NAV)
   p=pos(r);save_continue(r);assert pos(r)==p and flag(r,POWER)
   r.frame.save(OUT/(name+'-energie.png'))
   walk(r,'R',2);walk(r,'D',5);walk(r,'L',2);r.run(600);assert pos(r)==(4,17)
   walk(r,'D');walk(r,'R',20);pad_up(r,24,18,(24,10))
   walk(r,'R');walk(r,'U',5);walk(r,'L');face_a(r,'U');finish(r);assert flag(r,NAV)
   r.frame.save(OUT/(name+'-navigation.png'))
   save_continue(r);assert flag(r,POWER) and flag(r,NAV)
   walk(r,'R');walk(r,'D',5);walk(r,'L');r.run(600);assert pos(r)==(24,17)
   walk(r,'R',2);walk(r,'D',3);walk(r,'L',3);face_a(r,'U');decline(r);assert not flag(r,COMMS)
   face_a(r,'U');finish(r);assert flag(r,COMMS)
   r.frame.save(OUT/(name+'-radio.png'))
   # Real city exit and re-entry keep all station systems, not just Flash flags.
   walk(r,'D',2);walk(r,'L',9);r.keys={5};r.run(100);r.keys=set();r.run(600);assert location(r)==(3,10)
   walk(r,'U');r.run(600)
   if pos(r)==(14,23):walk(r,'U')
   assert pos(r)==(14,22) and all(flag(r,f) for f in [POWER,NAV,COMMS])
   walk(r,'U',4);pad_up(r,14,18,(14,12));walk(r,'U',7);assert pos(r)==(14,5)
   # Ariane and her signature partner must coexist in the actual field.
   active=[r.read(r.symbols['gObjectEvents']+i*36+5,1)[0] for i in range(16) if r.read(r.symbols['gObjectEvents']+i*36,1)[0]&1]
   assert 152 in active and 153 in active,active
   r.frame.save(OUT/(name+'-ariane-usapion.png'))
   if not gender:assert r.call('AddBagItem',C['ITEM_TM04'],999)
   face_a(r,'U');frames=t.az.a.fight(r,name,expected=[(96,28),(17,28),(51,29),(100,30)])
   assert flag(r,TROPHY) and flag(r,B4) and not flag(r,B6) and flag(r,0x4B5) and r.call('HasTrainerBeenFought',420)
   if not gender:
    assert not flag(r,TM);r.call('RemoveBagItem',C['ITEM_TM04'],1);before=r.call('GetGameStat',9)
    face_a(r,'U');finish(r);assert flag(r,TM) and r.call('GetGameStat',9)==before and r.call('CheckBagHasItem',C['ITEM_TM04'],999)
   else:assert flag(r,TM) and r.call('CheckBagHasItem',C['ITEM_TM04'],1) and not r.call('CheckBagHasItem',C['ITEM_TM04'],2)
   before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
   save_continue(r);assert pos(r)==(14,5) and flag(r,TROPHY) and flag(r,B4) and not flag(r,B6) and flag(r,TM)
   r.frame.save(OUT/(name+'-trophee.png'))
   walk(r,'D',7);r.run(600);assert pos(r)==(14,17),pos(r)
   walk(r,'D',5);r.keys={5};r.run(100);r.keys=set();r.run(600);assert location(r)==(3,10)
   rows.append({'test':name+' real city gym entrance with only local guard moved; native pads both directions; rejected early navigation; persistent energy/nav/radio and No/Yes choice; actual exit/re-entry; both Ariane/Usapion sprites; native four-member battle, fourth trophy and unique TM, no sixth badge; save/Continue and safe exit','passed':True,'battle_frames':frames})
  finally:r.close()
 (OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Actual station controls with explicit first-three-trophy and ordinary party fixtures. Komaous33, Whisper32, Cigallard32; IV15; learned moves reordered. No stat boosts or forced wins, not a continuous adventure or exhaustive balance.','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

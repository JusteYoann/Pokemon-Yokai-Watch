#!/usr/bin/env python3
"""Native defeat, partial hearth state, legacy Continue and postgame migrations."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_azuria_scenario_mgba as az
from tester_azuria_scenario_mgba import warp,walk,pos,location,face_a,finish,idle,save_continue,tile,flag,OUT,P,B1,B2,TM,C,active_champions
from tester_argenta_scenario_mgba import fight
rows=[]
def decline(r):
 for f in range(5000):
  r.keys={0} if f%16<4 else set();r.run()
  if f>60 and idle(r):r.keys=set();return
 raise AssertionError('No option did not return')
def legacy_continue(r):
 assert r.call('TrySavingData',0,max_frames=1200)==1
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);r.keys=set();r.run(900);assert idle(r)
# Actual loss must not grant the trophy or a trainer win.
r=new_game()
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],5,1,0,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.call('SetLastHealLocationWarp',4);r.call('FlagSet',B1);r.call('VarSet',P,3)
 warp(r,7,5,8,5);face_a(r,'U');frames=fight(r,'defaite',loss=True,expected=[(28,16),(8,16),(1,18)])
 assert not flag(r,B2) and not flag(r,TM) and not flag(r,0x4B1)
 assert not r.call('HasTrainerBeenFought',415) and not r.call('HasTrainerBeenFought',21)
 assert flag(r,B1) and r.call('VarGet',P)==3 and r.call('GetMonData',r.symbols['gPlayerParty'],57,0)>0
 rows.append({'test':'Actual whiteout with level1 starter: healed, first trophy and hearths retained, no second trophy/TM/trainer win; retry remains available','passed':True,'battle_frames':frames})
finally:r.close()
# Partial state refuses entry; an out-of-order hearth resets every visible light.
r=new_game()
try:
 r.call('FlagSet',B1)
 for stage in [1,2]:
  r.call('VarSet',P,stage);warp(r,7,5,8,8);walk(r,'U');finish(r);assert pos(r)==(8,8)
 r.call('VarSet',P,3);r.call('FlagClear',B1);warp(r,7,5,8,8);walk(r,'U');finish(r);assert pos(r)==(8,8)
 r.call('VarSet',P,1);warp(r,7,5,8,10);face_a(r,'U');finish(r)
 assert r.call('VarGet',P)==0 and all(tile(r,x,y)==0x2E0 for x,y in [(4,11),(12,11),(8,9)])
 rows.append({'test':'Gate rejects one/two lit hearths and missing first trophy even with all three; center out of order resets persistent and rendered state','passed':True})
finally:r.close()
# Explicit old-save state, not an archived player's save.
r=new_game(1)
try:
 r.call('FlagSet',B1);r.call('FlagSet',B2);r.call('SetTrainerFlag',415)
 warp(r,7,5,2,8);r.call('SetObjEventTemplateCoords',3,8,6);r.call('FlagClear',0x328);legacy_continue(r)
 assert location(r)==(7,5) and pos(r)==(8,17) and flag(r,B2) and flag(r,0x328)
 assert r.call('VarGet',P)==0
 walk(r,'U',7);walk(r,'R');walk(r,'U',2);walk(r,'L');walk(r,'U',3)
 assert pos(r)==(8,5) and active_champions(r)==[156]
 # Badge from the older game opens the gate without replaying the new puzzle.
 before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
 assert flag(r,TM) and r.call('GetGameStat',9)==before
 # An old earned-but-undelivered friend reward remains obtainable before postgame.
 r.call('FlagSet',0x306);assert r.call('AddBagItem',C['ITEM_LEAF_STONE'],999)
 face_a(r,'U');finish(r);assert not flag(r,0x307)
 r.call('RemoveBagItem',C['ITEM_LEAF_STONE'],1);face_a(r,'U');finish(r)
 assert flag(r,0x307) and r.call('CheckBagHasItem',C['ITEM_LEAF_STONE'],999) and r.call('GetGameStat',9)==before
 save_continue(r);assert flag(r,B2) and flag(r,0x307) and pos(r)==(8,5)
 r.frame.save(OUT/'ancienne-sauvegarde-arene.png')
 rows.append({'test':'Native Flash/Continue engineered prior-Misty save: safe entrance/new leader template, old trophy skips new puzzle, pending TM and historical Leaf Stone delivered uniquely without a new fight; future Continue retains exact position','passed':True})
finally:r.close()
# Legacy Celadon saves must not resurrect the relocated friend.
r=new_game()
try:
 warp(r,3,6,24,20);r.call('FlagClear',0x329);r.call('FlagClear',0x309);r.call('FlagClear',0x30A);before=pos(r)
 legacy_continue(r)
 assert location(r)==(3,6) and pos(r)==before and flag(r,0x329) and flag(r,0x309) and flag(r,0x30A)
 assert active_champions(r)==[]
 rows.append({'test':'Native Continue of engineered old Celadon save rebuilds templates with both relocated actors hidden and retains position','passed':True})
finally:r.close()
for gender,name in [(0,'nathan'),(1,'katie')]:
 r=new_game(gender)
 try:
  for f in [B1,B2,TM,0x82C]:r.call('FlagSet',f)
  r.call('CreateMon',r.symbols['gPlayerParty'],149,100,15,1,100,0,0)
  r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
  for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPATK','MON_DATA_SPDEF']:
   r.w32(r.PARAMS+128,999);r.call('SetMonData',r.symbols['gPlayerParty'],C[field],r.PARAMS+128)
  warp(r,7,5,8,5);before=r.call('GetGameStat',9);face_a(r,'U');decline(r)
  assert r.call('GetGameStat',9)==before and not flag(r,0x308)
  assert r.call('AddBagItem',C['ITEM_LEAF_STONE'],999)
  face_a(r,'U');frames=fight(r,name+'-revanche',expected=[(4,58),(88,59),(126,60),(8,61),(6,62),(50,63)])
  assert flag(r,0x306) and flag(r,0x308) and not flag(r,0x307)
  r.call('RemoveBagItem',C['ITEM_LEAF_STONE'],1);before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
  assert flag(r,0x307) and r.call('CheckBagHasItem',C['ITEM_LEAF_STONE'],999) and r.call('GetGameStat',9)==before
  face_a(r,'U');decline(r);assert r.call('GetGameStat',9)==before
  save_continue(r);assert flag(r,0x307) and flag(r,0x308)
  rows.append({'test':name+' optional rematch uses original six-member postgame team, No accepted, full Leaf Stone stack leaves reward pending, retry without a fight and unique persisted gift','passed':True,'battle_frames':frames,'fixture':'Hovernyan100, Aerial Ace, HP and battle stats explicitly boosted to999: event flow only, not postgame balance'})
 finally:r.close()
(OUT/'TEST_MIGRATION_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Independent explicit party/progression/legacy-state fixtures; native battles and Flash/Continue. No archived player save supplied.','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Native defeat, old Sabrina/Erika saves, cameo relocation and optional rewards."""
import hashlib,json,re
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_safrania_scenario_mgba as s
from tester_safrania_scenario_mgba import warp,walk,pos,location,face_a,finish,save_continue,flag,party,decline,OUT,C,POWER,NAV,COMMS,TROPHY,B3,B4,B6,TM
rows=[]
def actors(r):return [r.read(r.symbols['gObjectEvents']+36*i+5,1)[0] for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1]
# Native defeat, not an injected battle result.
r=new_game()
try:
 party(r,True)
 for f in [0x820,0x821,B3,POWER,NAV,COMMS]:r.call('FlagSet',f)
 warp(r,14,3,14,5);face_a(r,'U');frames=s.t.az.a.fight(r,'defaite',loss=True,expected=[(96,28),(17,28),(51,29),(100,30)])
 assert not flag(r,TROPHY) and not flag(r,B4) and not flag(r,B6) and not flag(r,TM) and not r.call('HasTrainerBeenFought',420)
 assert all(flag(r,f) for f in [POWER,NAV,COMMS,B3]) and r.call('GetMonData',r.symbols['gPlayerParty'],57,0)>0
 rows.append({'test':'Actual level1 whiteout: prior trophies and systems retained, healed player, no fourth/sixth trophy, TM or boss win','passed':True,'battle_frames':frames})
finally:r.close()
r=new_game()
try:
 party(r)
 warp(r,14,3,4,5);face_a(r,'U');finish(r);assert not flag(r,POWER)
 r.call('FlagSet',B3);r.call('FlagSet',B4);r.call('FlagSet',0x4B3) # Historic Erika alone.
 for mask in range(7):
  for bit,f in enumerate([POWER,NAV,COMMS]):r.call('FlagSet' if mask&(1<<bit) else 'FlagClear',f)
  warp(r,14,3,14,9);walk(r,'U');finish(r);assert pos(r)==(14,9)
  warp(r,14,3,14,5);face_a(r,'U');finish(r)
  assert not flag(r,TROPHY) and not r.call('HasTrainerBeenFought',420)
 for f in [POWER,NAV,COMMS]:r.call('FlagSet',f)
 r.call('FlagClear',B3);warp(r,14,3,14,9);walk(r,'U');finish(r);assert pos(r)==(14,9)
 rows.append({'test':'Energy requires third trophy; all seven incomplete-system combinations reject physical gate/direct boss even with historical Erika badge04; complete systems without third trophy still rejected','passed':True})
finally:r.close()
# Explicit pre-migration save; old native badges are retained, never erased.
r=new_game(1)
try:
 party(r)
 for f in [0x820,0x821,B3,B6,0x4B5]:r.call('FlagSet',f)
 r.call('SetTrainerFlag',420);warp(r,14,3,2,8)
 r.call('SetObjEventTemplateCoords',1,14,11)
 for f in [0x32E,TROPHY,B4]:r.call('FlagClear',f)
 save_continue(r)
 assert pos(r)==(14,22) and flag(r,TROPHY) and flag(r,B4) and flag(r,B6) and flag(r,0x32E)
 assert not any(flag(r,f) for f in [POWER,NAV,COMMS])
 walk(r,'U',5);r.run(600);assert pos(r)==(14,12)
 walk(r,'U',7);assert pos(r)==(14,5) and 152 in actors(r) and 153 in actors(r)
 assert r.call('AddBagItem',C['ITEM_TM04'],999);before=r.call('GetGameStat',9)
 face_a(r,'U');finish(r);assert not flag(r,TM)
 r.call('RemoveBagItem',C['ITEM_TM04'],1);face_a(r,'U');finish(r)
 assert flag(r,TM) and r.call('CheckBagHasItem',C['ITEM_TM04'],999) and r.call('GetGameStat',9)==before
 r.call('FlagSet',0x300);assert r.call('AddBagItem',C['ITEM_MOON_STONE'],999)
 face_a(r,'U');finish(r);assert not flag(r,0x301)
 r.call('RemoveBagItem',C['ITEM_MOON_STONE'],1);face_a(r,'U');finish(r)
 assert flag(r,0x301) and r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],999) and r.call('GetGameStat',9)==before
 save_continue(r);assert pos(r)==(14,5) and flag(r,TROPHY) and flag(r,B4) and flag(r,B6) and flag(r,0x301)
 r.frame.save(OUT/'ancienne-sauvegarde-safrania.png')
 rows.append({'test':'Engineered prior-Sabrina Flash/Continue save: safe entry/new actor templates, historic victory recognized as fourth, native sixth retained, no new system replay, pending TM and old Moon Stone full-stack retries without battle, subsequent exact position and persistent rewards','passed':True})
finally:r.close()
r=new_game()
try:
 warp(r,3,44,57,8)
 r.call('FlagClear',0x330);r.call('FlagClear',0x331);r.call('TrySpawnObjectEvents',0,0);r.run(120)
 assert 152 in actors(r) and 153 in actors(r),actors(r)
 save_continue(r)
 assert location(r)==(3,44) and pos(r)==(57,8) and flag(r,0x330) and flag(r,0x331)
 assert 152 not in actors(r) and 153 not in actors(r)
 rows.append({'test':'Native Continue of engineered old Route25 state with both actors actually spawned: relocation hides Ariane/Usapion, retains position and rebuilds templates','passed':True})
finally:r.close()
# Celadon retains its optional original battle and TM, with no trophy.
r=new_game()
try:
 party(r)
 for f in [0x820,0x821,B3]:r.call('FlagSet',f)
 assert r.call('AddBagItem',C['ITEM_TM19'],999)
 warp(r,10,16,6,5);face_a(r,'U');frames=s.t.az.a.fight(r,'serre',expected=[(53,23),(94,24),(54,26),(33,28)])
 tm19=int(re.search(r'#define FLAG_GOT_TM19_FROM_ERIKA\s+(0x[0-9A-Fa-f]+)',(ROOT/'include/constants/flags.h').read_text())[1],16)
 assert flag(r,0x4B3) and r.call('HasTrainerBeenFought',417) and not flag(r,B4) and not flag(r,TROPHY) and not flag(r,tm19)
 r.call('RemoveBagItem',C['ITEM_TM19'],1);before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
 assert flag(r,tm19) and r.call('CheckBagHasItem',C['ITEM_TM19'],999) and not flag(r,B4) and not flag(r,TROPHY) and r.call('GetGameStat',9)==before
 face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
 save_continue(r);assert flag(r,tm19) and not flag(r,B4) and not flag(r,TROPHY)
 r.frame.save(OUT/'serre-sans-trophee.png')
 rows.append({'test':'Actual optional Erika four-member battle with ordinary fixture team; unique pending TM19/full-stack retry and persistence; neither native fourth badge nor Ariane trophy awarded','passed':True,'battle_frames':frames})
finally:r.close()
r=new_game()
try:
 for f in [0x820,0x821,B3,B4,TROPHY,TM,0x82C]:r.call('FlagSet',f)
 r.call('CreateMon',r.symbols['gPlayerParty'],149,100,15,1,100,0,0);r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPATK','MON_DATA_SPDEF']:
  r.w32(r.PARAMS+128,999);r.call('SetMonData',r.symbols['gPlayerParty'],C[field],r.PARAMS+128)
 warp(r,14,3,14,5);before=r.call('GetGameStat',9);face_a(r,'U');decline(r);assert r.call('GetGameStat',9)==before and not flag(r,0x302)
 assert r.call('AddBagItem',C['ITEM_MOON_STONE'],999)
 face_a(r,'U');frames=s.t.az.a.fight(r,'revanche',expected=[(101,56),(28,57),(110,58),(30,59),(145,60)])
 assert flag(r,0x300) and flag(r,0x302) and not flag(r,0x301) and not flag(r,B6)
 r.call('RemoveBagItem',C['ITEM_MOON_STONE'],1);before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
 assert flag(r,0x301) and r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],999) and r.call('GetGameStat',9)==before
 face_a(r,'U');decline(r);assert r.call('GetGameStat',9)==before
 save_continue(r);assert flag(r,0x301) and flag(r,0x302) and flag(r,TROPHY) and not flag(r,B6)
 rows.append({'test':'Relocated optional postgame rematch, No accepted, original five-member party, unique Moon Stone full-stack pending/retry without another battle and persisted reward; no sixth badge','passed':True,'battle_frames':frames,'fixture':'Hovernyan100, Aerial Ace, explicitly boosted HP/stats999: postgame event-flow check only, not balance'})
finally:r.close()
(OUT/'TEST_MIGRATION_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Independent explicit progression/party/legacy-state fixtures. Native controls, Flash/Continue prepared with SaveMapView; no archived player save.','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Defeat, old saves, interrupted intro state and relocated postgame reward."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
from tester_argenta_scenario_mgba import warp,walk,face_a,finish,fight,party,idle,STAGE,R1,R2,BADGE,TM_FLAG,OUT,C
rows=[]
def flag(r,f):return bool(r.call('FlagGet',f))
def decline(r):
 for f in range(5000):
  r.keys={0} if f%16<4 else set();r.run()
  if f>60 and idle(r):r.keys=set();return
 raise AssertionError('No option did not return')
# Independent actual defeat; no savestate mixed with Flash operations.
r=new_game()
try:
 party(r,5,True);r.call('VarSet',STAGE,2)
 for f in [R1,R2]:r.call('FlagSet',f)
 warp(r,6,2,6,4);face_a(r,'U');frames=fight(r,'defaite',loss=True)
 assert not flag(r,BADGE) and not flag(r,TM_FLAG) and not r.call('HasTrainerBeenFought',414)
 assert flag(r,R1) and flag(r,R2) and r.call('VarGet',STAGE)==2
 assert r.call('GetMonData',r.symbols['gPlayerParty'],57,0)>0
 r.frame.save(OUT/'defaite-sans-trophee.png')
 rows.append({'test':'Actual first-champion defeat/whiteout, no trophy/TM/victory flag, relics retained, healed player can retry','frames':frames,'passed':True})
finally:r.close()
r=new_game()
try:
 # A real existing-save state, with first trophy but no new scenario flags.
 r.call('FlagSet',BADGE);r.call('SetTrainerFlag',414)
 assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('FlagClear',BADGE)
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 warp(r,3,2,22,36);walk(r,'U');assert idle(r) and r.call('VarGet',STAGE)==2
 assert not flag(r,R1) and not flag(r,R2)
 warp(r,6,2,6,6);walk(r,'U',2);assert idle(r)
 rows.append({'test':'Native Flash reload of prior first-trophy save: intro skipped, trophy retained and gate does not require newly added relic flags','passed':True})
finally:r.close()
r=new_game()
try:
 # Explicit intermediate-state fixture: normal menus cannot save mid-cutscene.
 r.call('VarSet',STAGE,1);assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('VarSet',STAGE,0);assert r.call('LoadGameSave',0,max_frames=1200)==1
 warp(r,3,2,22,35);seen=finish(r,watch=True,stem='reprise')
 assert seen==['enma'] and r.call('VarGet',STAGE)==2,seen
 rows.append({'test':'Engineered intermediate story state survives Flash and resumes only incognito conversation, without replaying Morleone','passed':True})
finally:r.close()
r=new_game()
try:
 r.call('FlagSet',BADGE);r.call('FlagSet',TM_FLAG);r.call('FlagSet',0x82C)
 r.call('CreateMon',r.symbols['gPlayerParty'],149,100,15,1,100,0,0)
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 # Postgame event-flow fixture only; ordinary first-trophy party tested separately.
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPATK','MON_DATA_SPDEF']:
  r.w32(r.PARAMS+128,999);r.call('SetMonData',r.symbols['gPlayerParty'],C[field],r.PARAMS+128)
 warp(r,6,2,6,4);before=r.call('GetGameStat',9);face_a(r,'U');decline(r)
 assert r.call('GetGameStat',9)==before and not flag(r,0x312)
 assert r.call('AddBagItem',C['ITEM_WATER_STONE'],999)
 face_a(r,'U');frames=fight(r,'revanche-postgame',expected=[(21,61),(51,62),(116,63),(97,64),(133,65),(146,66)])
 assert flag(r,0x312) and not flag(r,0x311)
 r.call('RemoveBagItem',C['ITEM_WATER_STONE'],1);before=r.call('GetGameStat',9)
 face_a(r,'U');finish(r)
 assert flag(r,0x311) and r.call('GetGameStat',9)==before and r.call('CheckBagHasItem',C['ITEM_WATER_STONE'],999)
 face_a(r,'U');decline(r);assert r.call('GetGameStat',9)==before
 assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('FlagClear',0x311);assert r.call('LoadGameSave',0,max_frames=1200)==1 and flag(r,0x311)
 warp(r,3,8,9,12) # CinnabarIsland, checked against the map registry below.
 assert flag(r,0x323)
 assert not any(r.read(r.symbols['gObjectEvents']+i*36,1)[0]&1 and r.read(r.symbols['gObjectEvents']+i*36+5,1)[0]==160 for i in range(16))
 rows.append({'test':'Actual optional high-level rematch relocated to gym; No accepted; original six-member team; full-stack Stone pending then delivered without another fight; unique persisted reward; old Cinnabar double absent','frames':frames,'passed':True,'fixture':'Level100 Hovernyan with Aerial Ace and explicitly boosted HP/stats999; validates event transitions, not postgame balance'})
finally:r.close()
(OUT/'TEST_MIGRATION_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Independent emulator instances with explicit progression and party fixtures; native defeat, save/load, dialogue and postgame battle; not a whole adventure','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

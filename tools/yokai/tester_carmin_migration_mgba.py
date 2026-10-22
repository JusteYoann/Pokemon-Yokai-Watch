#!/usr/bin/env python3
"""Native defeat, legacy Continue, partial calibration guards and safe returns."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_carmin_scenario_mgba as t
from tester_carmin_scenario_mgba import warp,walk,pos,location,face_a,finish,idle,save_continue,party,flag,portal,return_sign,OUT,F,B1,B2,B3,TM,C
rows=[]
def decline(r):
 for f in range(5000):
  r.keys={0} if f%16<4 else set();r.run()
  if f>60 and idle(r):r.keys=set();r.run(180);return
 raise AssertionError('No option did not return')
r=new_game()
try:
 party(r,weak=True)
 for f in [B1,B2]+F:r.call('FlagSet',f)
 warp(r,9,6,5,4);face_a(r,'U');frames=t.az.a.fight(r,'defaite',loss=True,expected=[(49,22),(56,22),(71,24)])
 assert not flag(r,B3) and not flag(r,TM) and not flag(r,0x4B2) and not r.call('HasTrainerBeenFought',416)
 assert all(flag(r,f) for f in F) and flag(r,B2) and r.call('GetMonData',r.symbols['gPlayerParty'],57,0)>0
 rows.append({'test':'Actual level1 whiteout: healed player, prior trophies/calibrations retained, no third trophy/TM/trainer victory; retry possible','passed':True,'battle_frames':frames})
finally:r.close()
r=new_game()
try:
 party(r)
 for x in [2,5,8]:
  warp(r,9,6,x,12);face_a(r,'U');finish(r);assert location(r)==(9,6)
 r.call('FlagSet',B1);r.call('FlagSet',B2)
 for done in [1,2]:
  for f in F:r.call('FlagClear',f)
  for f in F[:done]:r.call('FlagSet',f)
  warp(r,9,6,5,8);walk(r,'U');finish(r);assert pos(r)==(5,8)
  warp(r,9,6,5,4);face_a(r,'U');finish(r);assert not r.call('HasTrainerBeenFought',416)
 # Both remaining rooms can be left unfinished, including far side of native pad.
 for f in F:r.call('FlagClear',f)
 warp(r,9,6,5,12);portal(r,5);assert location(r)==(9,9);return_sign(r);assert not flag(r,F[1])
 portal(r,8);assert location(r)==(9,10);return_sign(r);assert not flag(r,F[2])
 portal(r,8);walk(r,'U',7);r.run(600);assert pos(r)==(11,5)
 walk(r,'D',8);walk(r,'L');face_a(r,'U');finish(r)
 assert location(r)==(9,6) and not flag(r,F[2])
 # Native healing station, both choices. HP1 is an explicit damage fixture.
 mon=r.symbols['gPlayerParty'];r.w32(r.PARAMS+128,1);r.call('SetMonData',mon,57,r.PARAMS+128)
 warp(r,9,6,2,16);face_a(r,'U');decline(r);assert r.call('GetMonData',mon,57,0)==1
 face_a(r,'U');finish(r);assert r.call('GetMonData',mon,57,0)==r.call('GetMonData',mon,58,0)
 rows.append({'test':'All doors require second trophy; gate/direct boss reject partial calibrations; unfinished Memory/Vigil and far pad chamber have actual safe returns; optional native healing accepts No and restores HP on Yes','passed':True})
finally:r.close()
r=new_game(1)
try:
 for f in [B1,B2,B3]:r.call('FlagSet',f)
 r.call('SetTrainerFlag',416);warp(r,9,6,2,8)
 r.call('SetObjEventTemplateCoords',1,5,2);r.call('FlagClear',0x32A)
 save_continue(r);assert location(r)==(9,6) and pos(r)==(5,18) and flag(r,0x32A) and flag(r,B3)
 assert not any(flag(r,f) for f in F)
 walk(r,'R');walk(r,'U',10);walk(r,'L');walk(r,'U',4);assert pos(r)==(5,4)
 assert r.call('AddBagItem',C['ITEM_TM34'],999)
 before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert not flag(r,TM)
 r.call('RemoveBagItem',C['ITEM_TM34'],1);face_a(r,'U');finish(r)
 assert flag(r,TM) and r.call('CheckBagHasItem',C['ITEM_TM34'],999) and r.call('GetGameStat',9)==before
 save_continue(r);assert pos(r)==(5,4) and flag(r,B3) and flag(r,TM)
 r.frame.save(OUT/'ancienne-sauvegarde-laboratoire.png')
 rows.append({'test':'Engineered prior-Surge Flash/Continue save: safe entrance/current templates, old third trophy bypasses new calibrations, full-stack pending TM delivered without another battle, subsequent Continue retains position and unique reward','passed':True})
finally:r.close()
(OUT/'TEST_MIGRATION_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Independent explicit damage/progression/legacy-state fixtures, native controls and Flash/Continue with SaveMapView as in native save menu; not an archived player save.','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

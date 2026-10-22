#!/usr/bin/env python3
"""Native Continue migration of explicitly engineered pre-chapter map saves."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
from tester_argenta_scenario_mgba import warp,walk,pos,location,idle,OUT,STAGE,BADGE
rows=[]
def resume(r):
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 r.keys=set();r.run(900)
 assert idle(r),(location(r),pos(r))
def save(r):assert r.call('TrySavingData',0,max_frames=1200)==1
r=new_game()
try:
 r.call('FlagSet',BADGE);warp(r,6,2,2,4)
 # Old champion stood at (6,5); old saved position is now enclosed by rocks.
 r.call('SetObjEventTemplateCoords',1,6,5);r.call('FlagClear',0x325);save(r)
 resume(r);assert location(r)==(6,2) and pos(r)==(6,13) and r.call('FlagGet',0x325)
 r.frame.save(OUT/'ancienne-sauvegarde-arene.png')
 # Native template loader must restore the new champion position, not saved (6,5).
 walk(r,'U',3);walk(r,'L');walk(r,'U',4);walk(r,'R');walk(r,'U',2)
 active=[]
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i
  if r.read(p,1)[0]&1 and r.read(p+8,1)[0]==1:
   active.append(tuple(int.from_bytes(r.read(p+16+j*2,2),'little')-7 for j in range(2)))
 assert (6,3) in active,active
 save(r);resume(r);assert pos(r)==(6,4)
 rows.append({'test':'Native Continue of engineered old gym save on newly blocked tile with old champion template: rebuilt layout/objects, safe entrance; subsequent Continue retains exact position','passed':True})
finally:r.close()
r=new_game()
try:
 r.call('FlagSet',BADGE);warp(r,3,2,22,32)
 r.call('FlagClear',0x324);r.call('VarSet',STAGE,0);save(r)
 resume(r);assert location(r)==(3,2) and pos(r)==(22,36)
 assert r.call('FlagGet',0x324) and r.call('VarGet',STAGE)==2
 walk(r,'U');save(r);resume(r);assert pos(r)==(22,35)
 rows.append({'test':'Native Continue of engineered old city save: first trophy retained, intro skipped, templates rebuilt; subsequent Continue retains exact position','passed':True})
finally:r.close()
(OUT/'TEST_CONTINUE_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Explicit legacy-state fixtures; actual native Flash and Continue callbacks, not an archived player save','results':rows},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(rows,ensure_ascii=False,indent=2))

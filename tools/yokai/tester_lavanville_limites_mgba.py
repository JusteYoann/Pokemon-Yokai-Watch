#!/usr/bin/env python3
"""Night guards, actual defeat, human filtering, self-care and legacy interiors."""
import hashlib,json,subprocess
from pathlib import Path
from mgba_new_game import new_game
from tester_lavanville_scenario_mgba import *
rows=[]
r=new_game()
try:
 party(r);r.call('FlagSet',0x825) # Historic Sabrina badge is not this chapter.
 warp(r,1,94,11,7);face_a(r,'U');finish(r);assert not flag(r,0x345)
 warp(r,1,94,11,3);face_a(r,'U');finish(r);assert not flag(r,0x344)
 rows.append({'test':'Historic native sixth badge without fifth/chapter victory cannot bypass Alyzon or ring bell','passed':True})
finally:r.close()
r=new_game()
try:
 party(r,True);r.call('FlagSet',0x824);warp(r,1,94,11,7)
 face_a(r,'U');frames=s.t.az.a.fight(r,'defaite-alyzon',loss=True,expected=[(42,39),(121,39),(70,40),(115,41)])
 assert not flag(r,0x345) and not flag(r,0x825) and flag(r,0x340)
 rows.append({'test':'Actual defeat: prior fifth trophy/night retained, no sixth trophy, healed respawn','passed':True,'battle_frames':frames})
finally:r.close()
r=new_game()
try:
 party(r);warp(r,8,0,7,4);assert any(g==64 for _,g,_ in actors(r)) # Actual native nurse before night.
 r.call('FlagSet',0x824);r.call('FlagClear',0x343);save_continue(r)
 assert location(r)==(8,0) and pos(r)==(7,4) and flag(r,0x340)
 assert len(actors(r))==1 and actors(r)[0][0]==255 # Humans disappear, player retained.
 mon=r.symbols['gPlayerParty'];r.write(r.PARAMS+100,(1).to_bytes(2,'little'));r.call('SetMonData',mon,57,r.PARAMS+100)
 assert r.call('GetMonData',mon,57,0)==1
 face_a(r,'U');finish(r);assert r.call('GetMonData',mon,57,0)==r.call('GetMonData',mon,58,0)
 save_continue(r);assert pos(r)==(7,4) and len(actors(r))==1
 r.frame.save(OUT/'soins-autonomes.png')
 rows.append({'test':'Engineered old interior Flash/Continue: player retained, humans hidden, exact position; actual counter interaction restores HP without nurse; persistence','passed':True})
finally:r.close()
# This chapter must not change any geographic block data or warp destinations.
for name in ['LavenderTown',*[f'PokemonTower_{f}F' for f in range(1,8)]]:
 p=f'data/layouts/{name}/map.bin'
 assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show','6a515fe3a:'+p],cwd=ROOT)
 p=f'data/maps/{name}/map.json';old=json.loads(subprocess.check_output(['git','show','6a515fe3a:'+p],cwd=ROOT));new=json.loads((ROOT/p).read_text());assert old['warp_events']==new['warp_events'] and old['connections']==new['connections']
rows.append({'test':'Lavender and all seven Tower floors: geographic block data, connections and warp destinations byte/data-identical to previous chapter','passed':True})
(OUT/'TEST_LIMITES_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Explicit legacy/progression/party fixtures and native engine callbacks, not archived player saves','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

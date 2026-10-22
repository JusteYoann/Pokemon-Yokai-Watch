#!/usr/bin/env python3
"""Native era confinement, all five actual doors, defeat and old-save safety."""
import hashlib,json,struct,subprocess
from mgba_new_game import new_game
from tester_cramois_scenario_mgba import *
rows=[]
def face(r,d):
 r.keys={dict(U=4,D=5,L=6,R=7)[d]};r.run(4);r.keys=set();r.run(12)
def coast():
 l=next(l for l in lv.LAY if l.get('id')=='LAYOUT_CINNABAR_ISLAND');w,h=l['width'],l['height'];a=struct.unpack('<'+'H'*(w*h),(ROOT/l['blockdata_filepath']).read_bytes())
 for y in range(1,h-1):
  for x in range(1,w-1):
   if a[y*w+x]>>12==3 and not(a[y*w+x]>>10&3):
    for d,dx,dy in [('U',0,-1),('D',0,1),('L',-1,0),('R',1,0)]:
     if a[(y+dy)*w+x+dx]>>12==1:return x,y,d
 raise AssertionError('No ordinary coast approach')
r=new_game()
try:
 party(r);r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_SURF'],3);r.call('FlagSet',0x824)
 x,y,d=coast();warp(r,*MAPS['CinnabarIsland'],x,y);face(r,d)
 assert r.call('SetUpFieldMove_Surf')==1 and r.call('SetUpFieldMove_Fly')==1 and r.call('SetUpFieldMove_Teleport')==1
 r.w32(r.symbols['gFieldCallback2'],0);r.w32(r.symbols['gPostMenuFieldCallback'],0)
 warp(r,*MAPS['PokemonMansion_1F'],8,32);assert r.call('CanUseEscapeRopeOnCurrMap')==1 and r.call('SetUpFieldMove_Dig')==1
 r.w32(r.symbols['gFieldCallback2'],0);r.w32(r.symbols['gPostMenuFieldCallback'],0)
 for name,p in [('CinnabarPast',(x,y)),('CinnabarPast_Mansion',(7,6)),('CinnabarPast_Gym',(7,16)),('CinnabarPast_Lab',(8,10)),('CinnabarPast_Center',(7,4)),('CinnabarPast_Mart',(3,5))]:
  warp(r,*MAPS[name],*p)
  assert r.call('IsScenarioPastCinnabar')==1
  for f in ['SetUpFieldMove_Surf','SetUpFieldMove_Fly','SetUpFieldMove_Teleport','SetUpFieldMove_Dig','CanUseEscapeRopeOnCurrMap']:assert r.call(f)==0,(name,f)
  save_continue(r);assert location(r)==MAPS[name] and pos(r)==p
  rows.append({'test':name+': Surf-equipped party and native Surf/Fly/Teleport/Dig/Rope setup refused; Flash/Continue retains epoch and exact position','passed':True})
 # Real coast interaction, no Surf field effect, no crossing to a neighbor.
 warp(r,*MAPS['CinnabarPast'],x,y);face_a(r,d);finish(r);assert not r.call('TestPlayerAvatarFlags',8) and pos(r)==(x,y)
 rows.append({'test':'Positive travel controls in present; actual past coast A interaction cannot launch Surf or leave island','passed':True})
finally:r.close()
r=new_game()
try:
 party(r)
 for target,door,inside,exitpos in [('CinnabarPast_Mansion',(8,4),(7,12),(7,12)),('CinnabarPast_Gym',(20,5),(7,16),(7,16)),('CinnabarPast_Lab',(8,10),(8,10),(8,10)),('CinnabarPast_Center',(14,12),(7,7),(7,7)),('CinnabarPast_Mart',(19,12),(4,6),(4,6))]:
  warp(r,*MAPS['CinnabarPast'],*door);walk(r,'U');r.run(600);assert location(r)==MAPS[target],(target,location(r),pos(r))
  # The normal loader can finish one tile inside the arrival threshold.
  if pos(r)!=inside:
   assert pos(r)==(inside[0],inside[1]+1),(target,pos(r),inside);walk(r,'U')
  leave_down(r,'CinnabarPast')
  rows.append({'test':target+': genuine past island door and genuine return exit, no present-world destination','passed':True})
finally:r.close()
r=new_game()
try:
 party(r,True);r.call('FlagSet',0x345);r.call('FlagSet',0x348);r.call('FlagSet',0x349)
 warp(r,*MAPS['CinnabarPast_Gym'],7,3);face_a(r,'U');frames=lv.s.t.az.a.fight(r,'defaite-passe',loss=True,expected=[(21,44),(67,44),(85,45),(32,45),(149,46)])
 assert location(r)==MAPS['CinnabarPast_Center'] and not flag(r,0x346) and not flag(r,0x826)
 assert r.call('GetMonData',r.symbols['gPlayerParty'],57,0)>0
 save_continue(r);assert location(r)==MAPS['CinnabarPast_Center']
 rows.append({'test':'Actual past champion defeat: no seventh trophy; healed native whiteout and subsequent Continue remain at past Center','passed':True,'battle_frames':frames})
finally:r.close()
r=new_game()
try:
 party(r);r.call('FlagSet',0x826);r.call('FlagSet',0x345)
 warp(r,*MAPS['CinnabarPast_Gym'],7,3);face_a(r,'U');finish(r);assert not flag(r,0x346)
 r.call('FlagSet',0x348);face_a(r,'U');finish(r);assert not flag(r,0x346)
 warp(r,*MAPS['CinnabarIsland_Gym'],7,6);r.call('FlagClear',0x34C);save_continue(r)
 assert pos(r)==(7,12) and flag(r,0x826) and flag(r,0x34C)
 rows.append({'test':'Historic Blaine native seventh badge cannot replace temporal chapter or skip zero/one-valve conditions; old present gym Flash/Continue rebuilds at safe entrance retaining badge','passed':True})
finally:r.close()
# All old IDs remain in the same order, and exterior geography is literally shared.
old=json.loads(subprocess.check_output(['git','show','bc40efd7a:data/maps/map_groups.json'],cwd=ROOT));new=json.loads((ROOT/'data/maps/map_groups.json').read_text())
for g in old['group_order']:assert new[g][:len(old[g])]==old[g]
oldlayouts=json.loads(subprocess.check_output(['git','show','bc40efd7a:data/layouts/layouts.json'],cwd=ROOT))['layouts'];assert [l.get('id') for l in lv.LAY[:len(oldlayouts)]]==[l.get('id') for l in oldlayouts]
d=json.loads((ROOT/'data/maps/CinnabarPast/map.json').read_text());present=json.loads((ROOT/'data/maps/CinnabarIsland/map.json').read_text());assert d['layout']==present['layout'] and not d['connections']
past=set(json.loads((ROOT/'data/yokai/scenario_cramois.json').read_text())['maps'])
for name in past:
 d=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());assert not d['allow_escaping'] and not d['connections']
 assert all(e['dest_map'].startswith('MAP_CINNABAR_PAST') for e in d['warp_events']),name
rows.append({'test':'All old map/layout IDs retained; exact same island layout; entire six-map past warp graph closed within era, no outside connection/escape flag','passed':True})
(OUT/'TEST_LIMITES_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Explicit field-move/party/progression/legacy fixtures; native APIs, actual doors/coast/defeat/Flash; not full adventure or archived player save','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Démonstration continue : chemin préparé avant capture vidéo, puis touches seules.
Arrivée à 3 cases, Alizon à droite, capture native, départ et passage suivi.
"""
import struct
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
from film_cible_mgba import Film
import parcours_navigation as nav
D=ROOT/'docs/gorgouille-alizon-20261025';D.mkdir(exist_ok=True)
nav.ROOT=D;nav.CACHE=Path('/workspace/artifacts/gorgouille-film-carte.json')
q=QA('TEMP.json');r=q.r
try:
 q.mon();q.f(0x82c)
 for flag in (0x335,0x336,0x337,0x33a):q.f(flag)
 r.call('ClearBag');r.call('AddBagItem',1,1);r.write(r.symbols['gBagMenuState']+6,b'\2\0')
 q.warp('MtEmber_Summit',8,9);r.run(300)
 for local,x,y in ((2,10,11),(3,8,12),(4,7,11),(5,11,9)):
  r.call('MoveObjectEventToMapCoords',q.actors()[local],x+7,y+7)
 assert 7 not in q.actors()
 film=Film(r,D/'gorgouille-arrivee-capture-depart-mgba.mp4');r.keys={7};r.run(20);r.keys=set()
 for f in range(12000):
  r.keys=film.controls();r.run()
  if q.idle() and int.from_bytes(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x1008,2),'little')==2:break
 else:raise AssertionError('Arrivée incomplète')
 assert 7 in q.actors();film.events.append({'seconds':film.frames/film.fps,'scene':'Alizon à droite du joueur'})
 r.keys={4};r.run(32);r.keys=set();r.run(40)
 caught=None
 for f in range(18000):
  cb=film.callback();ctrl=film.rev.get(r.u32(r.symbols['gBattlerControllerFuncs']),'')
  if r.read(r.symbols['gBattleOutcome'],1)==b'\7' and caught is None:
   caught=film.frames;film.events.append({'seconds':film.frames/film.fps,'scene':'Gorgouille capturé'})
  if caught is not None:
   if cb=='CB2_Overworld':r.keys=film.controls()
   elif film.frames-caught<180:r.keys=set()
   else:r.keys={0} if f%16<2 else set()
  elif cb=='BattleMainCB2' and ctrl=='HandleInputChooseAction':
   cur=r.read(r.symbols['gActionSelectionCursor'],1)[0];key=4 if cur&2 else 7 if not cur&1 else 8;r.keys={key} if f%16<2 else set()
  else:r.keys=film.controls()
  r.run()
  if caught is not None and q.idle() and 7 not in q.actors():break
 else:raise AssertionError(('Capture/départ incomplet',film.callback(),caught))
 film.events.append({'seconds':film.frames/film.fps,'scene':'Alizon a quitté le sommet'})
 r.keys=set();r.run(180)
 def pulse(keys,hold=1,after=20):
  r.keys=set();r.run(4);r.keys=set(keys);r.run(hold);r.keys=set();r.run(after)
 result=nav.navigate(r,[9,15],pulse,100);assert result['reason'] in ('arrived','map transition'),result
 if result['reason']=='arrived':r.keys={5};r.run(32)
 r.keys=set();r.run(240)
 film.finish(native_capture=True,prepared_inventory='Une Master Ball',prepared_party_level=100,prepared_rock_positions='Passage déjà dégagé, avant le début du film',arrival_and_departure=True,player_follows_same_path=True)
finally:r.close()

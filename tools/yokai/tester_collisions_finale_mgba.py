#!/usr/bin/env python3
"""Cinématique finale complète, combats gagnés avec équipe de QA renforcée.
Pas de vidéo. Vérification des déplacements image par image, puis du Panthéon.
"""
from postgame_qa_common import QA
from mafiamille_qa import strong_party
from observer_collisions_cinematiques import Observer
import json,hashlib
q=QA('TEMP_COLLISIONS.json');r=q.r;monitor=None
try:
 strong_party(r)
 for i,sp in enumerate((150,149,65,123,87),1):q.mon(i,sp,100)
 # Real destination warp of the last Council room, not an arbitrary tile.
 r.call('SetWarpDestination',*q.maps['PokemonLeague_ChampionsRoom'],0,65535,65535);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 monitor=Observer(r,'finale');original_observe=monitor.observe;stages=set()
 def verify():
  original_observe()
  if q.callback()!='CB2_Overworld':return
  if tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))!=q.maps['PokemonLeague_ChampionsRoom']:return
  stage=int.from_bytes(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x1004,2),'little')
  actors=q.actors();xy=lambda lid:tuple(v-7 for v in __import__('struct').unpack('<hh',r.read(actors[lid]+16,4)))
  if stage==1 and stage not in stages:
   assert xy(255)==(6,10) and xy(3)==(6,8),(xy(255),xy(3))
   assert [xy(i) for i in (4,5,6)]==[(4,7),(8,7),(6,6)]
  if stage==3 and stage not in stages:assert xy(1)==(5,10) and xy(255)==(6,10)
  if stage==8 and stage not in stages:
   assert xy(2)==(6,9) and xy(255)==(6,10) and xy(1)==(5,10)
  if stage==6:
   assert not {4,5,6}&actors.keys(),actors
  if stage in (1,3,6,8) and stage not in stages:r.frame.save(monitor.out/('finale-etape-'+str(stage)+'.png'));stages.add(stage)
 monitor.observe=verify;r.run(180)
 q.wait(lambda:q.callback()=='CB2_RollYokaiCredits',120000)
 result=monitor.finish();monitor=None
 assert not result['suspects'],result['suspects']
 assert not result['blocked_tiles_entered'],result['blocked_tiles_entered']
 assert stages=={1,3,6,8},stages
 result.update(stages_verified=sorted(stages),passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__)
 (q.P.parent/'cinematiques-collisions-20261025/FINALE_MGBA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('PASS finale complète: arrivée Matt, fusion, départs Mafiamille, arrivée Chen et sortie joueur sans traversée',flush=True)
finally:
 if monitor:monitor.finish()
 r.close()

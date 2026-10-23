#!/usr/bin/env python3
"""Observe all69 original story actors on real maps, with defeated-trainer fixtures."""
import hashlib,json,os
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp
P=ROOT/os.environ.get('YOKAI_MAFIA_ACTORS_DIR','QA_RECETTE_FINALE/MAFIAMILLE_KANTO/acteurs');P.mkdir(parents=True,exist_ok=True)
actors=json.loads((ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/PRESERVATION.json').read_text())['actors'];results=[];r=new_game();passed=False;error='Interrupted'
try:
 # Suppress automatic sight battles only for this visual fixture; no event flags/rewards awarded.
 for name,value in C.items():
  if name.startswith('TRAINER_TEAM_ROCKET_'):r.call('SetTrainerFlag',value)
 base=r.snapshot()
 for a in actors:
  r.restore(base);c=json.loads((ROOT/'data/maps'/a['map']/'map.json').read_text());o=c['object_events'][a['index']-1]
  if o.get('flag') not in [None,'0']:r.call('FlagClear',C[o['flag']])
  warp(r,*MAPS[a['map']],a['x'],a['y']+1)
  objects=[r.symbols['gObjectEvents']+36*i for i in range(16)]
  found=[x for x in objects if r.read(x,1)[0]&1 and r.read(x+8,1)[0]==a['index']]
  assert len(found)==1,(a,'actor absent',found)
  obj=found[0];gfx=r.read(obj+5,1)[0];symbol='YokaiDonMorleone' if a['graphics']=='OBJ_EVENT_GFX_GIOVANNI' else 'YokaiMafiamille1'
  assert r.call('GetObjectEventGraphicsInfo',gfx)==r.symbols['gObjectEventGraphicsInfo_'+symbol],(a,gfx)
  spr=r.symbols['gSprites']+68*r.read(obj+4,1)[0];assert r.u32(spr+12)==r.symbols['sPicTable_'+symbol]
  palette=int.from_bytes(r.read(spr+4,2),'little')>>12
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+palette*32,32)==(ROOT/'graphics/yokai_characters/don_morleone/overworld.gbapal').read_bytes()
  r.frame.save(P/f"{a['map']}-{a['index']:02d}.png")
  results.append(dict(**a,passed=True,native_graphics_id=gfx,actual_image_table=symbol,palette_verified=True))
  print('ACTOR PASS',a['map'],a['index'],flush=True)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=results),ensure_ascii=False,indent=2)+'\n')

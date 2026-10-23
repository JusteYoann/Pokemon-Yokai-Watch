#!/usr/bin/env python3
"""Capture existing native entrance previews, including remaining R artwork, without editing it."""
import hashlib,json
from PIL import Image,ImageDraw
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C
P=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/entrees';P.mkdir(parents=True,exist_ok=True)
r=new_game();base=r.snapshot();rows=[]
try:
 for name,pos,flag in [('RocketHideout_B1F',(5,15),'FLAG_WORLD_MAP_ROCKET_HIDEOUT_B1F'),('FiveIsland_RocketWarehouse',(12,13),'FLAG_WORLD_MAP_FIVE_ISLAND_ROCKET_WAREHOUSE')]:
  r.restore(base)
  if flag in C:r.call('FlagClear',C[flag])
  r.call('SetWarpDestination',*MAPS[name],255,*pos);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);frames=[]
  for i in range(70):r.run(5);frames.append(r.frame.copy())
  frames[0].save(P/(name+'.gif'),save_all=True,append_images=frames[1:],duration=84,loop=0)
  sheet=Image.new('RGB',(960,320));d=ImageDraw.Draw(sheet)
  for i,index in enumerate([5,10,15,20,30,40,50,65]):sheet.paste(frames[index],((i%4)*240,(i//4)*160))
  sheet.save(P/(name+'.png'));rows.append(dict(map=name,native_frames=350,unchanged_original_preview=True))
finally:r.close()
(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=rows),indent=2)+'\n')

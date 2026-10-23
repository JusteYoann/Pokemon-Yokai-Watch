#!/usr/bin/env python3
"""Short excerpts cut from genuine mGBA GIFs; no drawn or simulated frames."""
from pathlib import Path
from PIL import Image,ImageSequence
ROOT=Path(__file__).resolve().parents[2]
for mode in ['public','prive']:
 p=ROOT/'docs/cramois-ile-passe/phase-c'/mode
 for source,target,where in [('rencontre-nathaniel-et-defi','rencontre-nathaniel-courte','start'),('rencontre-michael-et-defi','rencontre-michael-courte','start'),('revanche-et-don-hovernyan','victoire-et-don-court','end')]:
  with Image.open(p/(source+'.gif')) as im:
   frames=[(f.convert('RGBA').copy(),f.info.get('duration',100)) for f in ImageSequence.Iterator(im)]
  chosen=frames[:140] if where=='start' else frames[-140:]
  chosen[0][0].save(p/(target+'.gif'),save_all=True,append_images=[f for f,d in chosen[1:]],duration=[d for f,d in chosen],loop=0,disposal=2)
  print(mode,target,len(chosen),sum(d for f,d in chosen)/1000,flush=True)

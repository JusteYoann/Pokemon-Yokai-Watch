#!/usr/bin/env python3
"""Native decompression of legacy portrait IDs still used by facility lookup tables."""
import hashlib,json
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C
P=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO';r=new_game();rows=[]
try:
 dest=r.call('AllocZeroed',2048);assert dest
 for old,new,actor in [('TRAINER_PIC_LEADER_GIOVANNI','TRAINER_PIC_YOKAI_DONMORLEONE','don_morleone'),('TRAINER_PIC_ROCKET_GRUNT_M','TRAINER_PIC_YOKAI_MAFIAMILLE1','mafiamille_1'),('TRAINER_PIC_ROCKET_GRUNT_F','TRAINER_PIC_YOKAI_MAFIAMILLE2','mafiamille_2')]:
  x,y=C[old],C[new]
  for table in ['gTrainerFrontPicTable','gTrainerFrontPicPaletteTable']:assert r.u32(r.symbols[table]+8*x)==r.u32(r.symbols[table]+8*y),(old,table)
  r.call('LZ77UnCompWram',r.u32(r.symbols['gTrainerFrontPicTable']+8*x),dest);assert r.read(dest,2048)==(ROOT/f'graphics/yokai_characters/{actor}/battle.4bpp').read_bytes()
  r.call('LZ77UnCompWram',r.u32(r.symbols['gTrainerFrontPicPaletteTable']+8*x),dest);assert r.read(dest,32)==(ROOT/f'graphics/yokai_characters/{actor}/normal.gbapal').read_bytes()
  rows.append(dict(legacy_picture_id=x,replacement_id=y,actor=actor,native_pixels_and_palette_match=True))
finally:r.close()
(P/'COMPAT_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=rows),indent=2)+'\n');print('COMPAT PASS3')

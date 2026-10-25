#!/usr/bin/env python3
"""Vérifie le souvenir Terr’heure dans les crédits natifs des deux personnages."""
import json,hashlib
from mgba_new_game import new_game
from mgba_rpc import ROOT
out=ROOT/'docs/cinematiques-collisions-20261025';results=[]
for gender,label in enumerate(('garcon','fille')):
 r=new_game(gender)
 try:
  r.call('DoCredits');r.run(10);visited=set();photos=set()
  for f in range(16000):
   if r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_RollYokaiCredits']|1:break
   slide=r.read(r.symbols['sYokaiCreditsSlide'],1)[0];tick=int.from_bytes(r.read(r.symbols['sYokaiCreditsTick'],2),'little')
   if slide<32:visited.add(slide)
   if slide in (15,17,26,27,31) and tick==180:
    stem=ROOT/f'graphics/yokai_credits/{label}-{slide:02}'
    tiles=stem.with_suffix('.8bpp').read_bytes();assert r.read(0x06000000,len(tiles))==tiles
    assert r.read(r.symbols['gPlttBufferUnfaded'],480)==stem.with_suffix('.gbapal').read_bytes()[:480]
    r.frame.save(out/'credits'/('credit-'+str(slide)+'-'+label+'.png'));photos.add(slide)
   r.run()
  assert visited==set(range(32)) and photos=={15,17,26,27,31}
  results.append({'personnage':label,'photos_corrigees_tiles_palette_natifs':sorted(photos),'32_scenes':True,'duree_frames':15239});print('PASS crédits',label,flush=True)
 finally:r.close()
(out/'TESTS_CREDITS_CORRIGES.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'checks':results},ensure_ascii=False,indent=2)+'\n')

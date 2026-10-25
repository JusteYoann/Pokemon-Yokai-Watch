#!/usr/bin/env python3
"""Contrôle ciblé des photos 3, 29 et 31 dans le moteur de crédits mGBA.
Horloge du générique avancée dans ces seules fixtures ; aucun film d'aventure.
"""
import json,hashlib,struct
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
D=ROOT/'docs/credits-souvenirs-20261025';rows=[]
board=json.loads((ROOT/'data/yokai/credits_storyboard.json').read_text())['slides']
for gender,label in enumerate(('garcon','fille')):
 for postgame in (False,True):
  r=new_game(gender)
  try:
   r.call('YoannPostgameCredits' if postgame else 'DoCredits')
   for _ in range(120):
    r.run()
    if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_RollYokaiCredits']|1:break
   else:raise AssertionError('Credits initialization timeout')
   for index in (3,29,31):
    elapsed=sum(a['frames'] for a in board[:index])+180
    # Main.vblankCounter2 is at 0x24 (include/main.h).
    r.write(r.symbols['sYokaiCreditsStartVBlank'],struct.pack('<I',(r.u32(r.symbols['gMain']+0x24)-elapsed)&0xffffffff))
    r.run(12)
    if r.read(r.symbols['sYokaiCreditsSlide'],1)[0]!=index:
     raise AssertionError(('Wrong slide clock',index,r.read(r.symbols['sYokaiCreditsSlide'],1)))
    stem=ROOT/'graphics/yokai_credits'/((f'postgame-{label}-{index}') if postgame and 27<=index<=30 else f'{label}-{index:02}')
    tiles=stem.with_suffix('.8bpp').read_bytes();assert r.read(0x6000000,len(tiles))==tiles
    assert r.read(r.symbols['gPlttBufferUnfaded'],480)==stem.with_suffix('.gbapal').read_bytes()[:480]
    r.frame.save(D/(f'{label}-credit-{index}-'+('postgame' if postgame else 'ligue')+'.png'))
    rows.append(dict(gender=label,postgame=postgame,index=index,native_tiles_and_palette=True))
  finally:r.close()
im=Image.open(ROOT/'graphics/yokai_characters/domniscian/overworld.png');heights=[]
for i in range(3):
 b=im.crop((32*i,0,32*(i+1),32)).point(lambda v:255 if v else 0).getbbox();heights.append(b[3]-b[1])
assert heights==[19,19,19]
(D/'TESTS_PHOTOS_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),photos=rows,domniscian_visible_heights=heights,final_group_source='docs/nyada-espace-domniscian-20261025/groupe'),ensure_ascii=False,indent=2)+'\n')
print('PASS twelve native photo checks, Domniscian 19px',flush=True)

#!/usr/bin/env python3
"""Compiled final credit slide in mGBA; explicit accelerated elapsed-clock fixture."""
import json,hashlib
from mgba_new_game import new_game
from mgba_rpc import ROOT
OUT=ROOT/'docs/beta-retours-20261024/photo-finale';OUT.mkdir(parents=True,exist_ok=True)
r=new_game();base=r.snapshot();rows=[]
try:
 for gender,label in [(0,'garcon'),(1,'fille')]:
  r.restore(base);r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));r.call('DoCredits');r.run(120)
  slides=json.loads((ROOT/'data/yokai/credits_storyboard.json').read_text())['slides'];target=sum(s['frames'] for s in slides[:31])+700
  oldstart=r.u32(r.symbols['sYokaiCreditsStartVBlank']);elapsed=r.u32(r.symbols['sYokaiCreditsTotalFrames']);r.w32(r.symbols['sYokaiCreditsStartVBlank'],(oldstart-target+elapsed)&0xffffffff);r.run(12)
  assert r.read(r.symbols['sYokaiCreditsSlide'],1)==b'\x1f';r.frame.save(OUT/(label+'.png'));assert max(r.frame.convert('RGB').getextrema()[1])>40
  rows.append(dict(gender=gender,native_slide=31,tick=int.from_bytes(r.read(r.symbols['sYokaiCreditsTick'],2),'little'),compiled_final_photo_rendered=True))
finally:
 (OUT/'TEST_MGBA.json').write_text(json.dumps(dict(scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),indent=2)+'\n');r.close()
print('PASS both compiled final credit photos')

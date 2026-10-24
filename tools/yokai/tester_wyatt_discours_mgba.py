#!/usr/bin/env python3
"""Native first-arrival scene: Wyatt visibility, independent palette and collisions."""
import os
from mgba_rpc import ROOT
os.environ['YOKAI_ARGENTA_REPORT_DIR']='docs/wyatt-discours-20261024/'+('fille' if os.environ.get('YOKAI_ARGENTA_GENDER')=='1' else 'garcon')
p=ROOT/'tools/yokai/tester_argenta_mgba.py';s=p.read_text()
replacement='''base=r.snapshot();passed=False
wyatt_frames=0
original_run=r.run
def observe_run(frames=1):
 global wyatt_frames
 for _ in range(frames):
  original_run(1)
  sb=r.u32(r.symbols['gSaveBlock1Ptr'])
  if not sb or tuple(r.read(sb+4,2))!=MAPS['PewterCity']:continue
  actors={}
  for i in range(16):
   raw=r.read(r.symbols['gObjectEvents']+36*i,36)
   if raw[0]&1 and raw[9:11]==bytes(reversed(MAPS['PewterCity'])) and raw[8]!=127:
    actors[raw[8]]=(struct.unpack('<hh',raw[16:20]),raw[4])
  if 14 in actors:
   wyatt_frames+=1
   pos,sid=actors[14]
   bank=int.from_bytes(r.read(r.symbols['gSprites']+68*sid+4,2),'little')>>12
   assert bank==7,('Wyatt palette bank',bank)
   assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_YokaiWyatt'],32)
   assert all(at!=pos for lid,(at,_) in actors.items() if lid!=14),('Wyatt overlaps actor',actors)
r.run=observe_run
'''
s=s.replace('base=r.snapshot();passed=False',replacement).replace('{8,9,10,11,12,13} <= set(ids)','{8,9,10,11,12,13,14} <= set(ids)')
s=s.replace("assert {'rassemblement','discours','dispersion'}<=seen,seen", "assert {'rassemblement','discours','dispersion'}<=seen,seen\n  assert wyatt_frames>0\n  assert r.call('GetObjectEventIdByLocalIdAndMap',14,MAPS['PewterCity'][1],MAPS['PewterCity'][0])==16\n  warp(r,*MAPS['PewterCity_Gym'],6,7)\n  wyatt_id=r.call('GetObjectEventIdByLocalIdAndMap',1,MAPS['PewterCity_Gym'][1],MAPS['PewterCity_Gym'][0]);assert wyatt_id<16\n  stored_graphics=r.read(r.symbols['gObjectEvents']+36*wyatt_id+5,1)[0]\n  assert r.call('GetObjectEventGraphicsInfo',stored_graphics)==r.symbols['gObjectEventGraphicsInfo_YokaiWyatt']\n  r.frame.save(P/f'{entry}-wyatt-arene.png')")
s=s.replace('results=rows),indent=2)','results=rows,wyatt_frames_checked=wyatt_frames,wyatt_palette_bank=7,wyatt_overlaps=0),indent=2)')
exec(compile(s,str(p),'exec'))

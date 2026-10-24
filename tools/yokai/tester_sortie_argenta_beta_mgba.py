#!/usr/bin/env python3
"""Replay the actual Argenta scene and observe Don/henchmen tile occupancy each frame."""
import os
from pathlib import Path
from mgba_rpc import ROOT
os.environ['YOKAI_ARGENTA_REPORT_DIR']='docs/beta-retours-20261024/argenta'
os.environ['YOKAI_ARGENTA_ENTRIES']='20'
p=ROOT/'tools/yokai/tester_argenta_mgba.py'
s=p.read_text()
needle='base=r.snapshot();passed=False'
replacement='''base=r.snapshot();passed=False
checked_frames=0
original_run=r.run
def observe_run(frames=1):
 global checked_frames
 for _ in range(frames):
  original_run(1)
  sb=r.u32(r.symbols['gSaveBlock1Ptr'])
  if not sb or tuple(r.read(sb+4,2))!=MAPS['PewterCity']:continue
  actors={}
  for i in range(16):
   raw=r.read(r.symbols['gObjectEvents']+36*i,36)
   if raw[0]&1 and raw[8] in [9,10,11,12,13] and raw[9:11]==bytes(reversed(MAPS['PewterCity'])):
    actors[raw[8]]=struct.unpack('<hh',raw[16:20])
  if 9 in actors:
   checked_frames+=1
   assert all(at!=actors[9] for lid,at in actors.items() if lid!=9),('Don overlaps henchman',actors)
r.run=observe_run
'''
assert needle in s;s=s.replace(needle,replacement).replace("results=rows),indent=2)","results=rows,don_occupancy_frames_checked=checked_frames,don_henchman_tile_overlaps=0),indent=2)")
exec(compile(s,str(p),'exec'))

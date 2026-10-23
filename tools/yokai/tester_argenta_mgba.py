#!/usr/bin/env python3
"""Actual first-arrival scene via Route2, four entrances; controller dialogue, no ROM patches."""
import os,json,hashlib,struct
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp
P=ROOT/os.environ.get('YOKAI_ARGENTA_REPORT_DIR','QA_RECETTE_FINALE/ARGENTA_MORLEONE/public');P.mkdir(parents=True,exist_ok=True)
C['FLAG_WORLD_MAP_PEWTER_CITY']=0x892
rows=[];r=new_game();base=r.snapshot();passed=False
try:
 for entry in map(int,os.environ.get('YOKAI_ARGENTA_ENTRIES','20,21,22,23').split(',')):
  r.restore(base);r.call('FlagClear',C['FLAG_WORLD_MAP_PEWTER_CITY']);r.call('FlagClear',C['FLAG_ARGENTA_MORLEONE_DONE']);r.call('FlagClear',C['FLAG_ARGENTA_MORLEONE_PENDING'])
  # Real connection: Route2 x8..11 maps to Argenta x20..23.
  warp(r,*MAPS['Route2'],entry-12,1);r.keys={4};r.run(90);r.keys=set()
  movie=[];seen=set();music=[];banks=[];first_done=None;don_start=None;peak_objects=0
  for f in range(20000):
   r.keys={8} if f%16<4 else set();r.run()
   if f%8==0 and entry==20:movie.append(r.frame.copy())
   if f%30==0:
    callback=r.u32(r.symbols['gMain']+4);obj=r.symbols['gObjectEvents'];actors=[]
    for i in range(16):
     a=obj+36*i
     if r.read(a,1)[0]&1 and r.read(a+9,2)==bytes([MAPS['PewterCity'][1],MAPS['PewterCity'][0]]):actors.append((r.read(a+8,1)[0],r.read(a+4,1)[0]))
    ids=dict(actors)
    if 8 in ids and 9 in ids:
     mm=int.from_bytes(r.read(r.symbols['gSprites']+ids[8]*68+4,2),'little')>>12
     dm=int.from_bytes(r.read(r.symbols['gSprites']+ids[9]*68+4,2),'little')>>12
     banks.append((mm,dm));assert mm==6 and dm==10,(entry,'palette banks',mm,dm)
    if r.read(r.symbols['gStringVar4'],8)==r.read(r.symbols['Argenta_DonSpeech'],8):
     if don_start is None:don_start=f
    if don_start is not None and f-don_start>=60 and 'rassemblement' not in seen:
     assert {8,9,10,11,12,13} <= set(ids), ('Missing scene actor',ids)
     r.keys=set();r.run(120);r.frame.save(P/f'{entry}-rassemblement.png');seen.add('rassemblement')
    if don_start is not None and f-don_start>=240 and 'discours' not in seen:
     r.keys=set();r.run(120);r.frame.save(P/f'{entry}-discours.png');seen.add('discours')
    peak_objects=max(peak_objects,len(ids));assert len(ids)<=15
    if not any(k>=9 and k<=13 for k in ids) and 'rassemblement' in seen and 'dispersion' not in seen:
     r.frame.save(P/f'{entry}-dispersion.png');seen.add('dispersion')
    song=r.u32(r.symbols['gMPlayInfo_BGM'])
    if not music or music[-1]!=song:music.append(song)
   if f%600==0:print('SCENE',entry,f,flush=True)
   if r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_DONE']) and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02':
    first_done=f;r.keys=set();r.run(90);
    break
  else:
   r.frame.save(P/f'{entry}-timeout.png');raise AssertionError((entry,'Scene timeout',r.read(r.symbols['sGlobalScriptContextStatus'],1).hex()))
  assert {'rassemblement','discours','dispersion'}<=seen,seen
  assert not r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_PENDING'])
  assert r.call('VarGet',C['VAR_MAP_SCENE_PEWTER_CITY'])==0, 'Gym/running-shoes progression changed'
  assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
  r.frame.save(P/f'{entry}-fin.png')
  if movie:movie[0].save(P/'scene.gif',save_all=True,append_images=movie[1:],duration=134,loop=0)
  rows.append(dict(entry=entry,completed_frames=first_done,simultaneous_palette_banks=sorted(set(banks)),music_headers=[hex(v) for v in music],captured=list(seen),peak_active_objects=peak_objects,passed=True))
 passed=True
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=rows),indent=2)+'\n')

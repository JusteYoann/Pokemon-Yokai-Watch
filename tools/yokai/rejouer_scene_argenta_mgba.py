#!/usr/bin/env python3
"""Development-only isolated replay, optionally from a COPY of a user's .sav.

Never writes the supplied save. No debug menu or progression bypass in release
ROM. Replay flags/warp live only in a temporary emulator, then are rolled back.
"""
import argparse,ctypes,hashlib,json,subprocess
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp
from argenta_qa import drive
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--save-file',type=Path);p.add_argument('--output',type=Path,default=ROOT/'QA_RECETTE_FINALE/ARGENTA_MORLEONE/rejeu-developpement');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;source_hash=None
try:
 if a.save_file:
  data=a.save_file.read_bytes();source_hash=hashlib.sha256(data).hexdigest()
  r.lib.retro_get_memory_size.argtypes=[ctypes.c_uint];r.lib.retro_get_memory_size.restype=ctypes.c_size_t
  r.lib.retro_get_memory_data.argtypes=[ctypes.c_uint];r.lib.retro_get_memory_data.restype=ctypes.c_void_p
  size=r.lib.retro_get_memory_size(0);ptr=r.lib.retro_get_memory_data(0);assert ptr and size==len(data),'Need the exact raw save size for this ROM'
  ctypes.memmove(ptr,data,size);assert r.call('LoadGameSave',0,max_frames=1200)==1
 else:
  r.call('FlagSet',C['FLAG_WORLD_MAP_PEWTER_CITY']);r.call('FlagSet',C['FLAG_BADGE01_GET']) if 'FLAG_BADGE01_GET' in C else None
  r.call('VarSet',C['VAR_MAP_SCENE_PEWTER_CITY'],2)
 snapshot=r.snapshot()
 def blocks():return r.read(r.u32(r.symbols['gSaveBlock1Ptr']),0x3D68)+r.read(r.u32(r.symbols['gSaveBlock2Ptr']),0xF24)
 original=blocks()
 r.call('FlagClear',C['FLAG_ARGENTA_MORLEONE_DONE']);r.call('FlagSet',C['FLAG_ARGENTA_MORLEONE_PENDING'])
 warp(r,*MAPS['PewterCity'],20,39);r.keys={4};r.run(60);r.keys=set();drive(r);r.frame.save(a.output/'rejeu-termine.png')
 r.restore(snapshot);assert blocks()==original,'Replay must roll back all save-block bytes'
 if a.save_file:assert hashlib.sha256(a.save_file.read_bytes()).hexdigest()==source_hash
 passed=True
finally:
 r.close();(a.output/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),input_save_sha256=source_hash,input_save_never_written=True,all_save_blocks_restored=True if passed else False),indent=2)+'\n')
print('DEVELOPMENT REPLAY PASS: original save blocks restored')

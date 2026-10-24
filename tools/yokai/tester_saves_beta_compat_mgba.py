#!/usr/bin/env python3
import ctypes,os,sys,json,struct,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/yokai'))
from mgba_rpc import Emulator
OUT=ROOT/'docs/beta-retours-20261024/sauvegardes-existantes';OUT.mkdir(parents=True,exist_ok=True)
rows=[]
for name in ['fin-jeu-151-garcon','fin-jeu-151-fille']:
 path=Path('/workspace/artifacts/sauvegardes-test-maison-v2')/name/'Pokemon_Yokai_Watch_Beta_0.1_Audio_Test.sav';r=Emulator()
 try:
  r.lib.retro_get_memory_data.argtypes=[ctypes.c_uint];r.lib.retro_get_memory_data.restype=ctypes.c_void_p
  ctypes.memmove(r.lib.retro_get_memory_data(0),path.read_bytes(),131072);r.lib.retro_reset();r.run(600);r.keys={3};r.run(3);r.keys=set();r.run(180)
  for f in range(5000):
   r.keys={8} if f%20<2 else set();r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
  else:raise AssertionError('Existing save Continue failed')
  r.keys=set();r.run(120);sb=r.u32(r.symbols['gSaveBlock1Ptr']);before=struct.unpack('<hh',r.read(sb,4));r.frame.save(OUT/(name+'-continue.png'));assert not r.call('ArePlayerFieldControlsLocked')
  pc=r.call('GetBoxedMonPtr',0,0);pc_hash=hashlib.sha256(r.read(pc,151*80)).hexdigest()
  r.keys={7};r.run(24);r.keys=set();r.run(30);after=struct.unpack('<hh',r.read(sb,4));assert before!=after
  assert hashlib.sha256(r.read(pc,151*80)).hexdigest()==pc_hash
  r.frame.save(OUT/(name+'-deplacement.png'))
  rows.append(dict(save=name,passed=True,save_bytes=path.stat().st_size,source_save_unchanged=True,start=before,end=after,pc151_hash=pc_hash,pc151_unchanged_by_walk=True))
 finally:r.close()
(OUT/'TEST_MGBA.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),scope='Previously delivered V2 battery saves, fresh core Continue and controller movement; no source save writes, no whole-adventure flag validation',results=rows),indent=2)+'\n');print('PASS',rows)

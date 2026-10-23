#!/usr/bin/env python3
"""Private music identity, whole-track repetition and byte preservation in mGBA.
Measures rendered samples; does not claim human listening or a seamless musical seam.
No audio recordings are written to Git or redistributed.
"""
import ctypes,json,hashlib,struct,os,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mgba_new_game import new_game
from mgba_rpc import ROOT,BATCH
from mafiamille_qa import MAPS,warp
r=new_game();P=ROOT/'docs/lavanville-zombie-night/finalisation/prive';P.mkdir(parents=True,exist_ok=True);passed=False;energy={};count={};frame=[0];rms={}
def samples(ptr,n):
 a=np.frombuffer(ctypes.string_at(ptr,n*4),dtype='<i2').astype(np.float64);bucket=frame[0]//300;energy[bucket]=energy.get(bucket,0)+float(a@a);count[bucket]=count.get(bucket,0)+len(a);return n
cb=BATCH(samples)
try:
 assert r.call('YokaiGetPrivateAudioMask')==(1<<31)-1
 src=Path(os.environ.get('LAVANVILLE_AUDIO_DIR','/workspace/private-audio/lavanville-integration'));old=Path(os.environ.get('LAVANVILLE_AUDIO_BASE','/workspace/private-audio/argenta-integration'))
 preserved=[]
 for n in range(1,32):
  data=(src/f'{n:02d}.dpcm').read_bytes();assert r.read(r.symbols[f'yokai_wave_{n:02d}'],len(data))==data
  base=(old/f'{n:02d}.dpcm').read_bytes()
  if n!=14:assert data==base;preserved.append(n)
  else:assert data[16:]==base[16:] and struct.unpack('<HHIII',data[:16])==(1,0x4000,13379*1024,0,1318984)
 r.call('FlagSet',0x322);r.call('VarSet',0x40f3,1);warp(r,*MAPS['LavenderTown'],14,9)
 assert r.call('GetCurrentMapMusic')==360
 header=r.u32(r.symbols['gMPlayInfo_BGM']);assert header==r.symbols['mus_yokai_14']
 r.lib.retro_set_audio_sample_batch(cb)
 for f in range(19500):frame[0]=f;r.run()
 assert r.u32(r.symbols['gMPlayInfo_BGM'])==header
 rms={str(k):round((energy[k]/count[k])**.5,3) for k in energy}
 # Samples well inside four successive passes; pauses at the original fade are expected.
 for sec in [15,115,215,315]:assert float(rms[str(sec//5)])>5,(sec,rms.get(str(sec//5)))
 passed=True
finally:
 report=dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),active_slots=31,unchanged_streams=preserved,zombie_original_compressed_blocks_preserved=True,zombie_wave_loop=[0,1318984],native_frames=19500,rms_per_300_frames=rms,scope=__doc__,human_listening=False,seamless_loop_claimed=False,limitation='Complete source repeats with its original fade-out and leading silence; musical seam still requires listening')
 (P/'AUDIO_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');r.close()
print(json.dumps(dict(passed=passed,active_slots=31,unchanged_streams=len(preserved),frames=19500)))

#!/usr/bin/env python3
import os,sys,ctypes,struct,json,hashlib,wave
from pathlib import Path
import numpy as np
from scipy.signal import correlate
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/yokai'))
from mgba_rpc import Emulator,BATCH
OUT=ROOT/'docs/beta-retours-20261024/audio-reference-b13';OUT.mkdir(parents=True,exist_ok=True)
rows=[];signals={}
for name,rom,elf in [('b13','/workspace/private-builds/b13-repair-verification/output/pokemon-yokai-BETA-B13-20261018.gba','/workspace/private-builds/b13-repair-verification/b13-repair-bqkzx4ij/beta.elf'),('candidate',str(ROOT/'pokefirered_audio.gba'),str(ROOT/'pokefirered_audio.elf'))]:
 os.environ['YOKAI_QA_ELF']=elf;r=Emulator(rom=Path(rom));chunks=[];cb=BATCH(lambda p,n:(chunks.append(ctypes.string_at(p,n*4)) or n));r.lib.retro_set_audio_sample_batch(cb)
 try:
  r.call('ResetMapMusic');r.call('m4aMPlayAllStop');r.run(120);r.call('SetMainCallback2',r.symbols['SpriteCallbackDummy']|1);base=r.snapshot()
  for slot in [1,11,23,26]:
   r.restore(base);header=r.u32(r.symbols['gYokaiPrivateHeaders']+4*(slot-1));assert header
   r.write(r.symbols['gSoundInfo']+80,bytes(64*12));r.call('MPlayStart',r.symbols['gMPlayInfo_BGM'],header);r.run(6);chunks.clear();r.run(360)
   raw=b''.join(chunks);x=np.frombuffer(raw,dtype='<i2').reshape(-1,2).mean(axis=1)/32768;signals[name,slot]=x
   with wave.open(str(OUT/f'{name}-{slot:02}.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(65536);f.writeframes(raw)
   ptr=r.u32(r.u32(header+4)+4);codec,flags,rate,loop,count=struct.unpack('<HHIII',r.read(ptr,16));nbytes=((count+63)//64)*33+16
   rows.append(dict(version=name,slot=slot,rom_sha256=hashlib.sha256(Path(rom).read_bytes()).hexdigest(),reverb=r.read(r.symbols['gSoundInfo']+5,1)[0],sample_hash=hashlib.sha256(r.read(ptr,nbytes)).hexdigest(),rate=rate/1024,rms=float(np.sqrt(np.mean(x*x))),peak=float(abs(x).max())))
 finally:r.close()
comparisons=[]
for slot in [1,11,23,26]:
 x,y=signals['b13',slot],signals['candidate',slot];lag=np.argmax(correlate(x[:200000],y[:200000],method='fft'))-199999
 xx=x[max(0,lag):min(len(x),len(y)+lag)];yy=y[max(0,-lag):min(len(y),len(x)-lag)]
 comparisons.append(dict(slot=slot,alignment_samples=int(lag),residual_db=float(10*np.log10(max(1e-20,np.mean((xx-yy)**2))/np.mean(xx**2))),same_source=rows[[v['version']+str(v['slot']) for v in rows].index('b13'+str(slot))]['sample_hash']==rows[[v['version']+str(v['slot']) for v in rows].index('candidate'+str(slot))]['sample_hash']))
(OUT/'COMPARAISON.json').write_text(json.dumps(dict(scope='Native mGBA captures, source identity and old B13 mixer parity; no human listening or physical hardware assertion',rows=rows,comparisons=comparisons),indent=2)+'\n');print(comparisons)

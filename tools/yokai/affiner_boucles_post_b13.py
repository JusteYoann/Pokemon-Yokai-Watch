#!/usr/bin/env python3
"""Refine five approved recurrence periods; pin source positions, no audio in Git.

Nate/Blossom excluded: short recurring motifs do not establish a full-song loop.
This is numerical loop construction, never a claim of perceptual approval.
"""
import argparse,hashlib,json,wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
ROOT=Path(__file__).resolve().parents[2]
CANDIDATES={27:(72.,20),28:(68.5715,20),29:(82.388,20),30:(44.2105,30),31:(52.6635,15)}
def refine(folder):
 rows=[];proof=[];fs=13379
 for n,(lag,anchor) in CANDIDATES.items():
  path=folder/f'{n:02d}.wav'
  with wave.open(str(path)) as f:
   assert (f.getframerate(),f.getnchannels(),f.getsampwidth())==(fs,1,2)
   x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
  a=round(anchor*fs);k=3*fs;delta=round(fs*.025);guess=round(lag*fs);v=x[a:a+k];region=x[a+guess-delta:a+guess+delta+k]
  c=fftconvolve(region,v[::-1],'valid')/np.sqrt(np.maximum(1e-12,fftconvolve(region**2,np.ones(k),'valid')*sum(v*v)))
  period=guess-delta+int(np.argmax(c));corr=[]
  for sec in range(min(60,int((len(x)-period)/fs)-1)):
   v=x[sec*fs:(sec+1)*fs];w=x[sec*fs+period:(sec+1)*fs+period];corr.append(float(v@w/max(1,np.linalg.norm(v)*np.linalg.norm(w))))
  candidates=[s for s in range(len(corr)-5) if min(corr[s:s+6])>.76 and np.mean(corr[s:s+6])>.87]
  assert candidates,(n,'No stable 6 second recurrence',corr)
  # Keep original intro once. Shift within 100ms at most, without silence/crossfade.
  sec=candidates[0];start=sec*fs;radius=round(fs*.1)
  lo=max(0,start-radius);hi=min(len(x)-period-1,start+radius)
  positions=np.arange(lo,hi);values=np.rint(x/256).clip(-128,127)
  jump=np.abs(values[positions+period-1]-values[positions]);slope=np.abs((values[positions+1]-values[positions])-(values[positions+period]-values[positions+period-1]))
  score=jump*10+slope+np.abs(positions-start)/max(1,radius)
  loop=int(positions[np.argmin(score)])
  rows.append({'number':n,'pcm_wav_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_start_samples':0,'source_loop_start_samples':loop,'source_end_samples':loop+period,'period_waveform_correlation':float(max(c)),'derivation':'Approved allocation, 3s waveform period refined at 13379Hz, >=6s stable recurrence, <=100ms phase alignment, original intro retained once; no time stretch or crossfade','perceptual_listening_validated':False})
  proof.append({'number':n,'period_samples':period,'period_seconds':period/fs,'first_stable_second':sec,'initial_window_correlations':corr,'pcm8_boundary_step':int(abs(values[loop+period-1]-values[loop]))})
 return rows,proof
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--private-sources',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();rows,proof=refine(a.private_sources);a.output.write_text(json.dumps({'tracks':rows,'evidence':proof},indent=2)+'\n');print(json.dumps({'tracks':rows,'evidence':proof},indent=2))

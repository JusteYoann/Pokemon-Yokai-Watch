#!/usr/bin/env python3
"""Private waveform recurrence study. Candidate positions, not listening approval."""
import argparse,hashlib,json,wave
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly,fftconvolve,find_peaks

def study(path):
 with wave.open(str(path)) as f:fs=f.getframerate();x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
 y=resample_poly(x,2000,fs);rate=2000;duration=len(y)/rate;rows=[]
 for sec in [.5,2,5,10,15,20,30,40,50]:
  if sec+4>duration*.65:continue
  a=y[round(sec*rate):round((sec+4)*rate)];power=sum(a*a)
  if power<1e6:continue
  c=fftconvolve(y,a[::-1],'valid')/np.sqrt(np.maximum(1e-12,fftconvolve(y*y,np.ones(len(a)),'valid')*power))
  peaks,_=find_peaks(c,distance=rate*3);best=sorted([int(p) for p in peaks if p>(sec+12)*rate and p<(duration-5)*rate],key=lambda p:c[p],reverse=True)[:3]
  for p in best:rows.append({'anchor_seconds':sec,'repeat_seconds':p/rate,'period_seconds':p/rate-sec,'score':float(c[p])})
 return {'number':int(path.stem),'duration_seconds':len(x)/fs,'pcm_wav_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'recurrences':sorted(rows,key=lambda a:a['score'],reverse=True)}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--private-sources',type=Path,required=True);p.add_argument('--numbers',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 rows=[]
 for n in map(int,a.numbers.split(',')):
  row=study(a.private_sources/f'{n:02d}.wav');rows.append(row);print(json.dumps({**row,'recurrences':row['recurrences'][:8]}),flush=True)
 a.output.write_text(json.dumps(rows,indent=2)+'\n')

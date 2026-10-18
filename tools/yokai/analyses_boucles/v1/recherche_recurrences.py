import json,wave
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly,fftconvolve,find_peaks,stft
out=[]
for n in [3,5,21,22,23,24,25,26]:
 with wave.open(f'/workspace/private-audio/v1-full-sources/{n:02d}.wav','rb') as f:x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
 y=resample_poly(x,2000,13379);fs=2000;dur=len(y)/fs;rows=[]
 for sec in [5,10,20,35,50]:
  if sec+6>dur*.6:continue
  a=y[sec*fs:(sec+6)*fs];c=fftconvolve(y,a[::-1],'valid');c/=np.sqrt(np.maximum(1e-15,fftconvolve(y*y,np.ones(len(a)),'valid')*sum(a*a)))
  peaks,_=find_peaks(c,distance=fs*3);peaks=sorted([p for p in peaks if p>(sec+20)*fs and p<(dur-7)*fs],key=lambda p:c[p],reverse=True)[:3]
  rows += [dict(at=sec,lag=p/fs-sec,score=float(c[p])) for p in peaks]
 # Log-frequency/time sequence matching tolerates naturally varying performances.
 freq,t,z=stft(y,fs=fs,nperseg=1024,noverlap=824);power=abs(z)**2
 bins=np.arange(24,109);midi=69+12*np.log2(np.maximum(freq,1)/440);features=np.zeros((len(bins),len(t)))
 for i,b in enumerate(bins):features[i]=power[(midi>=b-.5)&(midi<b+.5)].sum(axis=0)
 features=np.log1p(features/np.maximum(1e-6,np.median(features,axis=1)[:,None]));features-=features.mean(axis=1)[:,None];features/=np.maximum(1e-9,np.linalg.norm(features,axis=0))
 lags=[]
 for lag in range(200,min(int(dur*10)-100,2000)):
  c=(features[:,20:-lag]*features[:,lag+20:]).sum(axis=0)
  if len(c)>=80:lags.append((lag/10,float(np.mean(c))))
 scores=np.array([v for _,v in lags]);peaks,_=find_peaks(scores,distance=20);best=sorted(peaks,key=lambda p:scores[p],reverse=True)[:8]
 row=dict(number=n,duration=dur,waveform_candidates=sorted(rows,key=lambda r:r['score'],reverse=True)[:9],spectral_candidates=[lags[p] for p in best]);out.append(row);print(json.dumps(row),flush=True)
Path('/workspace/private-audio/v1-loop-research.json').write_text(json.dumps(out,indent=2))

import wave,numpy as np
from scipy.signal import fftconvolve,resample_poly,find_peaks
for n in [3,5,25]:
 with wave.open(f'/workspace/private-audio/v1-full-sources/{n:02d}.wav','rb') as f:x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
 y=resample_poly(x,2000,13379);print('TRACK',n,'duration',len(y)/2000,flush=True)
 for sec in [0.5,1,2,3,5,7,9,12,15]:
  a=y[round(sec*2000):round((sec+1)*2000)];c=fftconvolve(y,a[::-1],'valid');c/=np.sqrt(np.maximum(1e-15,fftconvolve(y*y,np.ones(len(a)),'valid')*sum(a*a)));peaks,_=find_peaks(c,distance=2000*2);peaks=sorted([p for p in peaks if p>(sec+20)*2000],key=lambda p:c[p],reverse=True)[:3]
  print(sec,[(p/2000, p/2000-sec,round(float(c[p]),3)) for p in peaks],flush=True)

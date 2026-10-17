import numpy as np,wave,json
from scipy.signal import resample_poly,stft,find_peaks
from pathlib import Path
rows=[]
for n in [3,5,7,8,12]:
 with wave.open(f'/workspace/private-audio/dpcm-full-sources/{n:02d}.wav','rb') as f:x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
 x=resample_poly(x,4000,13379);_,times,Z=stft(x,fs=4000,nperseg=1024,noverlap=824)
 powers=abs(Z);edges=np.geomspace(3,512,49).astype(int);feat=np.array([np.log1p(np.mean(powers[edges[i]:max(edges[i]+1,edges[i+1])],axis=0)) for i in range(48)])
 feat-=feat.mean(axis=1,keepdims=True);feat/=np.maximum(np.linalg.norm(feat,axis=0),1e-8);scores=[]
 # Compare complete substantial passage10..end-lag, avoiding intro-only phrases.
 for lag in range(15*20,min(int(times[-1]*.65),145)*20):
  a=feat[:,10*20:len(times)-lag-10*20];b=feat[:,10*20+lag:len(times)-10*20]
  scores.append(float(np.mean(np.sum(a*b,axis=0))))
 peaks,_=find_peaks(scores,distance=2*20);peaks=sorted(peaks,key=lambda p:scores[p],reverse=True)[:8]
 result={'number':n,'spectral_period_candidates':[{'lag_s':(p+15*20)/20,'score':scores[p]} for p in peaks]};rows.append(result);print(result,flush=True)
Path('/workspace/private-audio/spectral-periods.json').write_text(json.dumps(rows,indent=2))

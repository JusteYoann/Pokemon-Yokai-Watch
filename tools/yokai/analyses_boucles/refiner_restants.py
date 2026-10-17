import json,wave,numpy as np
from pathlib import Path
from scipy.signal import fftconvolve
out=[];rate=13379
for n,periods in {3:[120,112,114,108],5:[53.3333,66.6667,40],7:[76.8,96,57.6,19.2],8:[88.8],12:[72,21.6,79.2,82.8]}.items():
 with wave.open(f'/workspace/private-audio/dpcm-full-sources/{n:02d}.wav','rb') as f:x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
 for lag in periods:
  row={'number':n,'approx_lag':lag,'matches':[]}
  for second in [10,25,40,55]:
   t=second*rate;k=3*rate;delta=round(rate*.15);approx=round(lag*rate)
   if t+approx+k+delta>=len(x):continue
   template=x[t:t+k];region=x[t+approx-delta:t+approx+k+delta];c=fftconvolve(region,template[::-1],mode='valid');c/=np.sqrt(np.maximum(1e-15,fftconvolve(region**2,np.ones(k),mode='valid')*sum(template**2)));shift=int(np.argmax(c));period=approx-delta+shift;row['matches'].append({'at':second,'period_samples':period,'score':float(max(c))})
  out.append(row);print(row,flush=True)
Path('/workspace/private-audio/refine-restants.json').write_text(json.dumps(out,indent=2))

import json,wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
lags={1:75.1305,2:52.5665,4:104.681,6:113.143,9:83.479,10:76.8,11:98.182,13:98.63,14:61.715,15:52.4005,16:86,17:106.23,18:58.2525,19:33.112,20:94.4265};out=[];rate=13379
for n,lag in lags.items():
 with wave.open(f'/workspace/private-audio/dpcm-full-sources/{n:02d}.wav','rb') as f:x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
 t=20*rate;k=3*rate;delta=1200;approx=round(lag*rate);template=x[t:t+k];region=x[t+approx-delta:t+approx+k+delta];c=fftconvolve(region,template[::-1],mode='valid');c/=np.sqrt(np.maximum(1e-15,fftconvolve(region**2,np.ones(k),mode='valid')*sum(template**2)));shift=int(np.argmax(c));period=approx-delta+shift
 corr=[]
 for sec in range(min(30,int((len(x)-period)/rate)-1)):
  a=x[sec*rate:(sec+1)*rate];b=x[period+sec*rate:period+(sec+1)*rate];corr.append(float(np.dot(a,b)/max(1e-9,np.linalg.norm(a)*np.linalg.norm(b))))
 starts=[sec for sec in range(len(corr)-6) if min(corr[sec:sec+6])>.82 and np.mean(corr[sec:sec+6])>.90]
 start=starts[0] if starts else None
 print(n,period/rate,'start',start,'corr',[round(v,2) for v in corr[:20]],flush=True)
 out.append({'number':n,'period_samples':period,'loop_start_samples':None if start is None else start*rate,'match_score':float(max(c)),'initial_window_correlations':corr})
Path('/workspace/private-audio/refined-loops.json').write_text(json.dumps(out,indent=2))

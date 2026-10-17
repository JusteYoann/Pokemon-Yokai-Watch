import json,wave
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly,fftconvolve,find_peaks
rows=[]
for number in range(1,21):
 with wave.open(f'/workspace/private-audio/dpcm-full-sources/{number:02d}.wav','rb') as f:raw=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)/32768
 x=resample_poly(raw,2000,13379);fs=2000;duration=len(x)/fs;segment=x[10*fs:18*fs];n=len(segment)
 score=fftconvolve(x,segment[::-1],mode='valid');ener=np.sqrt(np.maximum(1e-15,fftconvolve(x*x,np.ones(n),mode='valid')*sum(segment*segment)));score/=ener
 peaks,_=find_peaks(score,distance=fs*2);peaks=sorted((p for p in peaks if p>30*fs and p< (duration-9)*fs),key=lambda p:score[p],reverse=True)[:6]
 rows.append({'number':number,'duration':duration,'candidates':[{'repeat_start':round(p/fs,5),'lag':round(p/fs-10,5),'score':round(float(score[p]),5)} for p in peaks]})
 print(number,rows[-1]['candidates'][:3],flush=True)
Path('/workspace/private-audio/repetition-candidates.json').write_text(json.dumps(rows,indent=2))

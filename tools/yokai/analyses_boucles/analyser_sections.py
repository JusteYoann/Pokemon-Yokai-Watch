import json,wave
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly,fftconvolve,find_peaks
rows=[]
for number in range(1,21):
 with wave.open(f'/workspace/private-audio/dpcm-full-sources/{number:02d}.wav','rb') as f:raw=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)/32768
 x=resample_poly(raw,2000,13379);fs=2000;duration=len(x)/fs;out=[]
 for start in [10,25,40,55]:
  if start+8>duration*.55:continue
  segment=x[start*fs:(start+8)*fs];n=len(segment);score=fftconvolve(x,segment[::-1],mode='valid');energy=np.sqrt(np.maximum(1e-15,fftconvolve(x*x,np.ones(n),mode='valid')*sum(segment*segment)));score/=energy
  peaks,_=find_peaks(score,distance=fs*2);peaks=sorted((p for p in peaks if p>(start+15)*fs and p<(duration-9)*fs),key=lambda p:score[p],reverse=True)[:2]
  out.extend({'template_start':start,'lag':float(p/fs-start),'score':float(score[p])} for p in peaks)
 rows.append({'number':number,'candidates':sorted(out,key=lambda r:r['score'],reverse=True)})
 print(number,rows[-1]['candidates'][:3],flush=True)
Path('/workspace/private-audio/section-candidates.json').write_text(json.dumps(rows,indent=2))

#!/usr/bin/env python3
"""Verify the long 86.4s Nathan cycle, not the recurring 19.2s motif."""
import argparse
import hashlib
import json
import wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--private-sources',type=Path,required=True)
parser.add_argument('--apply',action='store_true')
a=parser.parse_args();path=a.private_sources/'07.wav';fs=13379
with wave.open(str(path)) as f:
    assert (f.getframerate(),f.getnchannels(),f.getsampwidth())==(fs,1,2)
    x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)
assert hashlib.sha256(path.read_bytes()).hexdigest()=='03d53e8d1af808f018bdc2adcb39e9ba2e8652de14bb54d596b15a5cc9be4e5b'
start=2*fs;k=3*fs;guess=round(86.4*fs);delta=round(.05*fs)
v=x[start:start+k];region=x[start+guess-delta:start+guess+delta+k]
c=fftconvolve(region,v[::-1],'valid')/np.sqrt(np.maximum(1e-12,fftconvolve(region**2,np.ones(k),'valid')*sum(v*v)))
period=guess-delta+int(np.argmax(c));checks=[]
for sec in range(0,28):
    v=x[sec*fs:(sec+1)*fs];w=x[sec*fs+period:(sec+1)*fs+period]
    checks.append(float(v@w/max(1,np.linalg.norm(v)*np.linalg.norm(w))))
assert min(checks[1:9])>.78 and np.mean(checks[1:9])>.85
# Sample-aligned seam, within 100ms of the first full downbeat used here.
positions=np.arange(start-round(.1*fs),start+round(.1*fs));values=np.rint(x/256).clip(-128,127)
jump=np.abs(values[positions+period-1]-values[positions])
slope=np.abs((values[positions+1]-values[positions])-(values[positions+period]-values[positions+period-1]))
score=jump*10+slope+np.abs(positions-start)/(.1*fs)
loop=int(positions[np.argmin(score)])
track=dict(number=7,pcm_wav_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
           source_start_samples=0,source_loop_start_samples=loop,source_end_samples=loop+period,
           period_waveform_correlation=float(max(c)),
           derivation='86.4s long cycle, 28 consecutive one-second recurrence windows examined; first8 matched windows mean>.85/min>.78, original intro once, <=100ms seam phase alignment. 19.2s recurring motif rejected as incomplete. Native five-wrap and perceptual checks tracked separately.',
           perceptual_listening_validated=False)
report=dict(track=track,period_samples=period,period_seconds=period/fs,
            one_second_correlations=checks,pcm8_boundary_step=int(jump[np.argmin(score)]),
            human_listening=False,scope='Numerical structure/seam evidence, not subjective musical acceptance.')
out=ROOT/'QA_RECETTE_FINALE/SESSION_1_AUDIO/NATHAN_BOUCLE_SOURCE.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if a.apply:
    p=ROOT/'data/yokai/audio_loops.json';d=json.loads(p.read_text())
    d['tracks']=[r for r in d['tracks'] if r['number']!=7]+[track];d['tracks'].sort(key=lambda r:r['number'])
    d['active_tracks']=sorted(set(d['active_tracks']+[7]));d['pending_tracks']=[n for n in d['pending_tracks'] if n!=7]
    d['status']='Session1 audio: 19 active; Enma5, Blossom12 and Final25 await reliable full-section loops'
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

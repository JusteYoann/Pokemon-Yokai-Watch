#!/usr/bin/env python3
"""Reproducible recurrence study on hash-pinned private WAV sources.

Exhaustive six-second waveform anchors, then native-rate phase and spectral
comparisons for the observed long-cycle hints. Scores are evidence for audition,
not a general threshold that approves musical loops. No ROM or audio is written.
"""
import argparse, hashlib, json, wave
from pathlib import Path
import numpy as np
from scipy.fft import rfft, irfft, next_fast_len
from scipy.signal import resample_poly, find_peaks, fftconvolve, stft

ROOT=Path(__file__).resolve().parents[2]
def study(row, path):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==row['pcm_wav_sha256'], 'Wrong source WAV'
    with wave.open(str(path)) as w:
        assert w.getframerate()==13379 and w.getsampwidth()==2 and w.getnchannels()==1
        x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)
    y=resample_poly(x,2000,13379);fs=2000;k=6*fs
    fft_size=next_fast_len(len(y)+k-1);transform=rfft(y,fft_size)
    cumulative=np.r_[0,np.cumsum(y*y)];energy=cumulative[k:]-cumulative[:-k]
    candidates=[]
    for second in range(0,int(len(y)/fs)-26,2):
        offset=second*fs;template=y[offset:offset+k]
        dot=irfft(transform*rfft(template[::-1],fft_size),fft_size)[k-1:len(y)]
        score=dot/np.sqrt(np.maximum(1,energy*sum(template*template)))
        low=offset+16*fs;high=len(score)-2*fs
        if low>=high:continue
        peaks,_=find_peaks(score[low:high],distance=fs*2)
        for i in sorted(peaks+low,key=lambda i:score[i],reverse=True)[:2]:
            candidates.append(dict(start_seconds=second,repeat_seconds=i/fs,
                period_seconds=i/fs-second,waveform_correlation=float(score[i])))
    candidates.sort(key=lambda r:r['waveform_correlation'],reverse=True)
    # These hints were independently isolated by pitch-distribution comparison;
    # use sample-rate phase refinement and inspect their full available overlap.
    anchor,period={5:(84,26.6666666667),8:(18,88.8),25:(32,150.4)}[row['number']]
    a=round(anchor*13379);k=4*13379;centre=round(a+period*13379)
    low=centre-1338;region=x[low:centre+1338+k];template=x[a:a+k]
    dot=fftconvolve(region,template[::-1],mode='valid')
    power=fftconvolve(region*region,np.ones(k),mode='valid')
    score=dot/np.sqrt(np.maximum(1,power*sum(template*template)))
    lag=low+int(score.argmax())-a
    windows=[]
    for second in range(int((len(x)-lag)/13379)-2):
        start=second*13379;u=x[start:start+2*13379];v=x[start+lag:start+lag+2*13379]
        _,_,U=stft(u,13379,nperseg=2048,noverlap=1536)
        _,_,V=stft(v,13379,nperseg=2048,noverlap=1536)
        U=abs(U);V=abs(V)
        cosine=np.sum(U*V,axis=0)/np.maximum(1e-8,np.linalg.norm(U,axis=0)*np.linalg.norm(V,axis=0))
        windows.append(dict(at_seconds=second,waveform_correlation=float(np.corrcoef(u,v)[0,1]),
            spectral_cosine=float(np.mean(cosine)),rms_ratio=float(np.linalg.norm(v)/max(1,np.linalg.norm(u)))))
    return dict(number=row['number'],title=row['title'],wav_sha256=row['pcm_wav_sha256'],
        duration_seconds=len(x)/13379,search_window_seconds=6,search_anchor_step_seconds=2,
        best_waveform_candidates=candidates[:12],examined_lag_samples=lag,
        examined_period_seconds=lag/13379,aligned_two_second_windows=windows,
        perceptual_listening_validated=False)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-sources',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();config=json.loads((ROOT/'data/yokai/audio_loops.json').read_text())
    rows=[]
    for row in config['gap_tracks']:
        if row['number'] not in (5,8,25):continue
        result=study(row,a.private_sources/f"{row['number']:02d}.wav")
        rows.append(result);print('STUDIED',row['number'],result['examined_period_seconds'],flush=True)
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(dict(scope=__doc__,results=rows),indent=2)+'\n')

if __name__=='__main__':main()

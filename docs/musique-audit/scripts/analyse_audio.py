#!/usr/bin/env python3
"""Reference-only audio analysis; no game resources or audio arrangements written."""
from pathlib import Path
import json,subprocess,hashlib,re,concurrent.futures
import numpy as np
import librosa
from scipy import signal
R=Path(__file__).resolve().parents[3];D=R/'docs/musique-audit';W=R.parent/'scratch/music-analysis'
rows=json.loads((W/'archive-members.json').read_text())
def analyze(entry):
 p=Path(entry['local_path']);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]));stream=next(s for s in probe['streams'] if s['codec_type']=='audio');sr=11025
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar',str(sr),'-f','f32le','-']);y=np.frombuffer(raw,dtype='<f4').copy();assert len(y)>sr
 rms=librosa.feature.rms(y=y,frame_length=2048,hop_length=512)[0];S=np.abs(librosa.stft(y,n_fft=2048,hop_length=512));centroid=librosa.feature.spectral_centroid(S=S,sr=sr)[0];onset=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S+1e-12),sr=sr,hop_length=512)
 tempo=float(np.asarray(librosa.feature.tempo(onset_envelope=onset,sr=sr,hop_length=512)).flat[0]);acf=signal.correlate(onset-onset.mean(),onset-onset.mean(),mode='full',method='fft')[len(onset)-1:];lag=round(sr*60/512/tempo);confidence=float(acf[lag]/max(acf[0],1e-9)) if lag<len(acf) else 0
 chroma=librosa.feature.chroma_stft(S=S**2,sr=sr).mean(axis=1);major=np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]);minor=np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17]);keys=sorted([(float(np.corrcoef(chroma,np.roll(profile,i))[0,1]),i,mode) for mode,profile in [('major',major),('minor',minor)] for i in range(12)],reverse=True)
 # Recurrence on chroma + normalized spectral shape: an approximate repeated
 # section offset, NOT edit-ready sample/measure loop boundaries.
 C=librosa.feature.chroma_stft(S=S**2,sr=sr);C=C/(np.linalg.norm(C,axis=0,keepdims=True)+1e-9);lags=range(round(15*sr/512),min(C.shape[1]//2,round(150*sr/512)))
 best=max(((float(np.mean(np.sum(C[:,l:]*C[:,:-l],axis=0))),l) for l in lags),default=(0,0))
 def db(v):return float(20*np.log10(max(float(v),1e-12)))
 out={**entry,'id':{'YW1':'YW1-','BUSTERS2':'B2-','BLASTERS':'BL-','SANGOKUSHI':'SG-','YW2':'YW2-','YW4':'YW4-','YW3':'YW3-'}[entry['game']]+hashlib.sha256(entry['member'].encode()).hexdigest()[:8],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'decoded_mono_11025_sha256':hashlib.sha256(raw).hexdigest(),'duration_seconds':len(y)/sr,'probe_duration_seconds':float(probe['format']['duration']),'codec':stream['codec_name'],'sample_rate':int(stream['sample_rate']),'channels':stream['channels'],'bit_rate':int(probe['format'].get('bit_rate',0)),'tags':probe['format'].get('tags',{}),'tempo_estimate_bpm':tempo,'tempo_acf_confidence':confidence,'tempo_half_double_ambiguity':True,'rms_dbfs':db(np.sqrt(np.mean(y*y))),'peak_dbfs':db(np.max(np.abs(y))),'rms_p10_db':db(np.percentile(rms,10)),'rms_p90_db':db(np.percentile(rms,90)),'spectral_centroid_hz':float(np.mean(centroid)),'silence_fraction_below_minus50db':float(np.mean(rms<10**(-50/20))),'head_5s_rms_db':db(np.sqrt(np.mean(y[:sr*5]**2))),'tail_5s_rms_db':db(np.sqrt(np.mean(y[-sr*5:]**2))),'tonal_profile_hypothesis':str(keys[:3]),'tonality_confidence':'Low: global chroma correlation, not a verified key signature','recurrence_offset_seconds':best[1]*512/sr,'recurrence_cosine':best[0],'loop_status':'NON VALIDÉ : repérage statistique de répétition, pas une frontière musicale ou un raccord audio','full_decode_passed':True,'analysis_scope':'Entire decoded MP3, mono11025Hz analysis copy only; source MP3 untouched. No human/perceptual listening claimed.'}
 out['rms_envelope_1s']=[float(np.sqrt(np.mean(y[i:i+sr]**2))) for i in range(0,len(y),sr)]
 # Diagnostic figure is data, never an audio replacement.
 import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
 fig,axes=plt.subplots(2,1,figsize=(10,4));axes[0].plot(np.arange(len(out['rms_envelope_1s'])),out['rms_envelope_1s']);axes[0].set_ylabel('RMS');axes[0].set_title(p.name,fontsize=8);axes[1].imshow(librosa.amplitude_to_db(S+1e-9,ref=np.max),origin='lower',aspect='auto',extent=[0,len(y)/sr,0,sr/2],vmin=-70,vmax=0);axes[1].set_xlabel('Secondes');axes[1].set_ylabel('Hz');fig.tight_layout();fig.savefig(D/'preuves'/(out['id']+'.png'));plt.close(fig)
 print('ANALYZED',p.name,round(out['duration_seconds'],1),round(tempo,1),round(confidence,2),flush=True);return out
if __name__=='__main__':
 # Matplotlib state is process-local; audio remains outside the repository.
 target=D/'preuves/ANALYSE_AUDIO.json';previous=json.loads(target.read_text()) if target.exists() else [];cache={(e['game'],e['member'],e['sha256']):e for e in previous};entries=[e for e in rows if e['member'].lower().endswith('.mp3')];todo=[e for e in entries if (e['game'],e['member'],hashlib.sha256(Path(e['local_path']).read_bytes()).hexdigest()) not in cache]
 with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:new=list(pool.map(analyze,todo))
 cache.update({(e['game'],e['member'],e['sha256']):e for e in new});result=[cache[(e['game'],e['member'],hashlib.sha256(Path(e['local_path']).read_bytes()).hexdigest())] for e in entries]
 (D/'preuves/ANALYSE_AUDIO.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

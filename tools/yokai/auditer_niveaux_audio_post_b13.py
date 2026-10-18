#!/usr/bin/env python3
"""Record native mGBA mixer output privately; measure EBU R128 after DC rejection.

Finite windows, not a listening verdict or whole-composition loudness claim.
"""
import argparse,ctypes,hashlib,json,re,subprocess,tempfile,wave
from pathlib import Path
import numpy as np
from mgba_rpc import Emulator,ROOT,BATCH
P=ROOT/'QA_RECETTE_FINALE/POST_B13'
CONSTANTS={k:int(v) for k,v in re.findall(r'^#define\s+((?:MUS|SE)_\w+)\s+(\d+)\b',(ROOT/'include/constants/songs.h').read_text(),re.M)}

def measure(path):
 command=['ffmpeg','-hide_banner','-nostdin','-i',str(path),'-af','highpass=f=20,ebur128=peak=true','-f','null','-']
 result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True).stderr
 summary=result.rsplit('Summary:',1)[-1]
 def number(pattern):
  m=re.search(pattern,summary);return float(m[1]) if m else None
 with wave.open(str(path)) as f:audio=np.frombuffer(f.readframes(f.getnframes()),'<i2')
 return {'integrated_lufs':number(r'I:\s+(-?[\d.]+) LUFS'),'loudness_range_lu':number(r'LRA:\s+([\d.]+) LU'),'true_peak_dbfs':number(r'Peak:\s+(-?[\d.]+) dBFS'),'raw_clipped_samples':int(np.count_nonzero((audio==32767)|(audio==-32768))),'pcm_samples_stereo_interleaved':len(audio),'dc_offset_pcm16':round(float(audio.mean()),3),'analysis_filter':'20 Hz highpass, EBU R128 true-peak; filter for measurement only'}

def run(stage,private,kinds,only=None):
 private=private.resolve();assert not private.is_relative_to(ROOT)
 private.mkdir(parents=True,exist_ok=True)
 r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180);base=r.snapshot()
 rows=[]
 try:
  chosen=[(k,v) for k,v in CONSTANTS.items() if (k.startswith('MUS_') and v and 'bgm' in kinds) or (k.startswith('SE_') and 'sfx' in kinds)]
  chosen+= [('CRY_JIBANYAN',1),('CRY_CIGALOPIN',9),('CRY_AMBIENT_CIGALOPIN',9)] if 'cry' in kinds else []
  if only:chosen=[row for row in chosen if row[0] in only]
  assert chosen, 'No requested cues matched'
  for index,(name,number) in enumerate(chosen):
   r.restore(base);r.call('m4aMPlayAllStop');chunks=[]
   cb=BATCH(lambda ptr,n:(chunks.append(ctypes.string_at(ptr,n*4)) or n))
   r.lib.retro_set_audio_sample_batch(cb)
   is_music=name.startswith('MUS_');is_cry=name.startswith('CRY_');frames=720 if is_music else 180
   if is_music:r.call('m4aSongNumStart',number)
   elif is_cry:
    r.call('PlayCry_NormalNoDucking',number,0,65 if 'AMBIENT' in name else 120,10)
   # Repeat short SFX over the measurement window to get a meaningful loudness gate.
   for f in range(frames):
    if not is_music and not is_cry and f%30==0:r.call('PlaySE',number)
    r.run()
   path=private/f'{name}.wav'
   with wave.open(str(path),'wb') as w:w.setparams((2,2,65536,0,'NONE',''));w.writeframes(b''.join(chunks))
   row={'constant':name,'number':number,'emulated_frames':frames,'mixer_hz':65536,**measure(path)};rows.append(row)
   if index%20==0:print('MEASURED',index+1,len(chosen),name,row['integrated_lufs'],flush=True)
 finally:r.close()
 report={'stage':stage,'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'method':'Actual libretro mGBA mixer captured privately, EBU R128 via ffmpeg after 20 Hz DC rejection; 720 frames BGM, 180 frames repeating SFX/isolated cries. No subjective listening claim; finite-window measures, not entire compositions','recordings_public':False,'results':rows}
 out=P/'audio';out.mkdir(parents=True,exist_ok=True);(out/f'niveaux-{stage}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('PASS measurements',len(rows),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage',default='baseline-b13');p.add_argument('--private-output',type=Path,required=True);p.add_argument('--kinds',default='bgm,sfx,cry');p.add_argument('--constants',help='Optional comma-separated exact constants');a=p.parse_args();run(a.stage,a.private_output,a.kinds.split(','),a.constants.split(',') if a.constants else None)

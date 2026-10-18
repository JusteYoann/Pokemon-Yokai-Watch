#!/usr/bin/env python3
"""Build optional native m4a songs from pinned private source sections.

Only metadata/configuration belongs in Git. All output remains outside checkout.
The source sample points are pinned; no automatic cut/tempo guess at build time.
Consult each track's derivation: a phrase assembly is not full-source recurrence.
"""
import argparse,concurrent.futures,hashlib,json,struct,wave
from pathlib import Path
import numpy as np
from dpcm_m4a import wave_data,decode
ROOT=Path(__file__).resolve().parents[2]
def encode_track(job):
 row,full,output=job;n=row['number'];wav=full/f'{n:02d}.wav'
 assert hashlib.sha256(wav.read_bytes()).hexdigest()==row['pcm_wav_sha256'],(n,'Wrong private source WAV')
 with wave.open(str(wav),'rb') as f:
  assert f.getframerate()==13379 and f.getnchannels()==1 and f.getsampwidth()==2
  x=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(np.float64)
 start=row['source_start_samples'];end=row['source_end_samples'];loop=row['source_loop_start_samples']
 assert 0<=start<=loop<end<=len(x)
 samples=np.clip(np.rint(x[start:end]/256),-128,127).astype(np.int16).tolist();blob=wave_data(samples,13379,loop-start);path=output/f'{n:02d}.dpcm';path.write_bytes(blob)
 decoded=decode(blob[16:],len(samples));jump=abs(decoded[-1]-decoded[loop-start]);normal_steps=np.abs(np.diff(np.array(decoded,dtype=np.int16)))
 return {'number':n,'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'source_start_samples':start,'source_end_samples':end,'loop_start_samples':loop-start,'loop_length_samples':end-loop,'loop_boundary_step_pcm8':jump,'max_adjacent_step_pcm8':int(max(normal_steps)),'native_loop_tested':False,'perceptual_listening_validated':False}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--full-source-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);a=p.parse_args();output=a.output.resolve();assert not output.is_relative_to(ROOT);output.mkdir(parents=True,exist_ok=True)
 config=json.loads((ROOT/'data/yokai/audio_loops.json').read_text());rows=config['tracks']
 with concurrent.futures.ProcessPoolExecutor(max_workers=a.jobs) as pool:results=list(pool.map(encode_track,[(r,a.full_source_dir,output) for r in rows]))
 active=set(config['active_tracks']);available={r['number'] for r in rows};assert active<=available
 lines=['.section .rodata','.align 2','.global gYokaiPrivateHeaders','gYokaiPrivateHeaders:']
 lines.extend(f'.4byte '+(f'mus_yokai_{n:02d}' if n in active else '0') for n in range(1,config.get('slot_count',20)+1))
 lines+=['.global gYokaiPrivateSlotCount','gYokaiPrivateSlotCount:',f'.4byte {config.get("slot_count",20)}']
 lines+=['.global gYokaiPrivateAudioMask','gYokaiPrivateAudioMask:',f'.4byte {sum(1<<(n-1) for n in active)}']
 for n in sorted(active):
  lines += ['.align 2',f'.global mus_yokai_{n:02d}',f'mus_yokai_{n:02d}:','.byte 1,0,0,0',f'.4byte yokai_voice_{n:02d}, yokai_track_{n:02d}',f'yokai_voice_{n:02d}:','.byte 0x28,60,0,0',f'.4byte yokai_wave_{n:02d}','.byte 255,0,255,0',f'yokai_track_{n:02d}:','.byte 0xbb,75,0xbd,0,0xbe,80,0xcf,60,100',f'yokai_wait_{n:02d}:','.byte 0xb0,0xb2',f'.4byte yokai_wait_{n:02d}','.align 2',f'.global yokai_wave_{n:02d}',f'yokai_wave_{n:02d}:',f'.incbin "{output/n.__format__("02d")}.dpcm"']
 (output/'yokai_music.s').write_text('\n'.join(lines)+'\n');metadata={'active_tracks':sorted(active),'active_sample_bytes':sum(r['bytes'] for r in results if r['number'] in active),'prepared_tracks':results,'scope':'Measured repeating source sections; not a claim of perceptual listening or actual in-game validation'};(output/'manifest.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata,indent=2))
if __name__=='__main__':main()

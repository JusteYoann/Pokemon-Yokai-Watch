#!/usr/bin/env python3
"""Build optional native m4a songs from pinned private source sections.

Only metadata/configuration belongs in Git. All output remains outside checkout.
The source sample points are pinned; no automatic cut/tempo guess at build time.
Consult each track's derivation: a phrase assembly is not full-source recurrence.
"""
import argparse,concurrent.futures,hashlib,json,struct,wave,shutil
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
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--full-source-dir',type=Path);p.add_argument('--reuse-26-dir',type=Path,help='Reuse only byte-pinned original 26 DPCM files');p.add_argument('--gap-source-dir',type=Path,help='Private original full 05/08/13/14/25.dpcm');p.add_argument('--output',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);a=p.parse_args();output=a.output.resolve();assert not output.is_relative_to(ROOT);output.mkdir(parents=True,exist_ok=True)
 config=json.loads((ROOT/'data/yokai/audio_loops.json').read_text());rows=config['tracks']
 if config.get('gap_tracks') and not a.gap_source_dir:p.error('31 OST require --gap-source-dir; protected full DPCM files are external')
 if a.reuse_26_dir:
  results=json.loads((ROOT/'QA_RECETTE_FINALE/AUDIO_30MIO/PROVENANCE_26_OST.json').read_text())['prepared_tracks']
  assert {r['number'] for r in results}=={r['number'] for r in rows}
  for row in results:
   source=a.reuse_26_dir/f"{row['number']:02d}.dpcm"
   assert source.stat().st_size==row['bytes'] and hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],(source,'Original 26 integrity mismatch')
   shutil.copyfile(source,output/source.name)
 else:
  if not a.full_source_dir:p.error('Use --full-source-dir or --reuse-26-dir')
  with concurrent.futures.ProcessPoolExecutor(max_workers=a.jobs) as pool:results=list(pool.map(encode_track,[(r,a.full_source_dir,output) for r in rows]))
 for row in config.get('gap_tracks',[]):
  n=row['number'];blob=(a.gap_source_dir/f'{n:02d}.dpcm').read_bytes()
  assert len(blob)==row['input_bytes'] and hashlib.sha256(blob).hexdigest()==row['input_sha256'],(n,'Wrong full private source')
  assert struct.unpack_from('<HHIII',blob)==(1,0,row['rate']*1024,0,row['input_samples'])
  start=row['loop_start_samples'];end=row['loop_end_samples']
  if start is not None:
   assert 0<=start<end<=row['input_samples']
   blob=struct.pack('<HHIII',1,0x4000,row['rate']*1024,start,end)+blob[16:16+((end+63)//64)*33]
  (output/f'{n:02d}.dpcm').write_bytes(blob)
  results.append(dict(number=n,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),loop_start_samples=start,source_start_samples=0,source_end_samples=end,loop_length_samples=None if start is None else end-start,playback='one-shot' if start is None else 'loop',perceptual_listening_validated=False))
 active=set(config['active_tracks']);available={r['number'] for r in results};assert active<=available
 gap_numbers={r['number'] for r in config.get('gap_tracks',[])}
 gap_lines=['.section .yokai_audio_gap,"a",%progbits']
 lines=['.section .rodata','.align 2','.global gYokaiPrivateHeaders','gYokaiPrivateHeaders:']
 lines.extend(f'.4byte '+(f'mus_yokai_{n:02d}' if n in active else '0') for n in range(1,config.get('slot_count',20)+1))
 lines+=['.global gYokaiPrivateSlotCount','gYokaiPrivateSlotCount:',f'.4byte {config.get("slot_count",20)}']
 lines+=['.global gYokaiPrivateAudioMask','gYokaiPrivateAudioMask:',f'.4byte {sum(1<<(n-1) for n in active)}']
 for n in sorted(active):
  target=gap_lines if n in gap_numbers else lines
  target += ['.align 2',f'.global mus_yokai_{n:02d}',f'mus_yokai_{n:02d}:','.byte 1,0,0,0',f'.4byte yokai_voice_{n:02d}, yokai_track_{n:02d}',f'yokai_voice_{n:02d}:','.byte 0x28,60,0,0',f'.4byte yokai_wave_{n:02d}','.byte 255,0,255,0',f'yokai_track_{n:02d}:','.byte 0xbb,75,0xbd,0,0xbe,80,0xcf,60,100',f'yokai_wait_{n:02d}:','.byte 0xb0,0xb2',f'.4byte yokai_wait_{n:02d}','.align 2',f'.global yokai_wave_{n:02d}',f'yokai_wave_{n:02d}:',f'.incbin "{output/n.__format__("02d")}.dpcm"']
 (output/'yokai_music.s').write_text('\n'.join(lines)+'\n')
 gap_path=output/'yokai_music_gap.s'
 if gap_numbers:gap_path.write_text('\n'.join(gap_lines)+'\n')
 elif gap_path.exists():gap_path.unlink()
 metadata={'active_tracks':sorted(active),'active_sample_bytes':sum(r['bytes'] for r in results if r['number'] in active),'prepared_tracks':results,'scope':'Original 26 pinned. Additional gap tracks include explicit one-shot exceptions. No claim of perceptual listening.'};(output/'manifest.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata,indent=2))
if __name__=='__main__':main()

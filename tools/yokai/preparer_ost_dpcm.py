#!/usr/bin/env python3
"""Private full-reference encoding for accurate storage estimates, NOT final loops.

Requires the user-supplied extracted archive manifest and ffmpeg. All WAV/DPCM
remain in the specified private directory; only metadata may be committed.
"""
import argparse,concurrent.futures,hashlib,json,struct,subprocess,wave
from pathlib import Path
from dpcm_m4a import wave_data
ROOT=Path(__file__).resolve().parents[2]
def prepare(job):
 track,reference,output,rate=job;stem=output/f'{track["number"]:02d}';wav=stem.with_suffix('.wav');target=stem.with_suffix('.dpcm')
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',reference['private_path'],'-ac','1','-ar',str(rate),'-c:a','pcm_s16le',str(wav)],check=True)
 with wave.open(str(wav),'rb') as stream:
  assert stream.getnchannels()==1 and stream.getsampwidth()==2 and stream.getframerate()==rate
  raw=stream.readframes(stream.getnframes())
 samples=[max(-128,min(127,round(x[0]/256))) for x in struct.iter_unpack('<h',raw)]
 data=wave_data(samples,rate,None);target.write_bytes(data)
 return {**track,'source_sha256':reference['sha256'],'sample_rate_hz':rate,'samples':len(samples),'duration_seconds':len(samples)/rate,'wave_data_bytes':len(data),'encoded_sha256':hashlib.sha256(data).hexdigest(),'loop_start':None,'status':'FULL SOURCE ENCODED PRIVATELY FOR SIZE ONLY; natural loop and playback not validated; not active in game'}
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--extracted-manifest',type=Path,required=True);parser.add_argument('--private-output',type=Path,required=True);parser.add_argument('--jobs',type=int,default=2);args=parser.parse_args()
 config=json.loads((ROOT/'data/yokai/audio_candidates.json').read_text());references=json.loads(args.extracted_manifest.read_text());jobs=[]
 output=args.private_output.resolve();assert not output.is_relative_to(ROOT),'Private audio must stay outside checkout';output.mkdir(parents=True,exist_ok=True)
 for track in config['tracks']:
  matches=[r for r in references if Path(r['member']).stem==track['source_stem']];assert len(matches)==1,(track['title'],len(matches))
  reference=matches[0];assert hashlib.sha256(Path(reference['private_path']).read_bytes()).hexdigest()==reference['sha256']
  jobs.append((track,reference,output,config['sample_rate_hz']))
 with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
  rows=[]
  for row in pool.map(prepare,jobs):rows.append(row);print(f"Encoded {row['number']:02d}: {row['wave_data_bytes']} bytes",flush=True)
 report={'tracks':rows,'total_wave_data_bytes':sum(r['wave_data_bytes'] for r in rows),'private_output':str(output),'production_tracks_integrated':0,'scope':'Uncut source recordings encoded without loop points, for exact measured storage cost; not natural-loop or listening validation'}
 (output/'encoding-metadata.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()

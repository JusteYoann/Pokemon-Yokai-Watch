#!/usr/bin/env python3
"""Re-decode verified private MP3s and require exact locked PCM hashes; no ROM build."""
import argparse,concurrent.futures,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--extracted-manifest',type=Path,required=True);p.add_argument('--private-output',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);a=p.parse_args();dst=a.private_output.resolve();assert not dst.is_relative_to(ROOT);dst.mkdir(parents=True,exist_ok=True)
 ref={Path(r['member']).stem:r for r in json.loads(a.extracted_manifest.read_text())};cat={r['number']:r for r in json.loads((ROOT/'data/yokai/audio_candidates.json').read_text())['tracks']};loops=json.loads((ROOT/'data/yokai/audio_loops.json').read_text())['tracks'];locked={r['number']:r for r in json.loads((ROOT/'QA_RECETTE_FINALE/POST_B13/audio/PROVENANCE_18_OST.json').read_text())['selected22_sources']}
 def check(row):
  n=row['number'];source=ref[cat[n]['source_stem']];assert hashlib.sha256(Path(source['private_path']).read_bytes()).hexdigest()==source['sha256']==locked[n]['mp3_sha256'];out=dst/f'{n:02d}.wav'
  subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',source['private_path'],'-ac','1','-ar','13379','-c:a','pcm_s16le',str(out)],check=True)
  sha=hashlib.sha256(out.read_bytes()).hexdigest();assert sha==row['pcm_wav_sha256'],(n,'Decoded WAV differs; investigate source/decoder, do not change lock',sha,row['pcm_wav_sha256']);return dict(number=n,mp3_sha256=source['sha256'],wav_sha256=sha,passed=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:rows=list(pool.map(check,loops))
 report={'passed':True,'tracks_redecoded_from_verified_private_mp3':len(rows),'ffmpeg_version':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],'results':rows};(dst/'verification-decodage.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'fresh WAVs match pinned hashes')
if __name__=='__main__':main()

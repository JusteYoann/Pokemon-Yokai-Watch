#!/usr/bin/env python3
"""Clone an existing private31 pack, changing only Zombie Night's WaveData loop flag.
No audio is imported into Git. The other30 streams and every Zombie Night encoded
block remain byte-identical. Whole-track repetition retains the original fade and
silence; this is not a seamless-loop or human-listening approval.
"""
import argparse,hashlib,json,struct
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();src=a.source_dir.resolve();out=a.output.resolve();root=Path(__file__).resolve().parents[2]
assert src!=out and not out.is_relative_to(root),'Keep private output external and source intact'
m=json.loads((src/'manifest.json').read_text());assert len(m['active_tracks'])==31
original={r['number']:r for r in m['prepared_tracks']};out.mkdir(parents=True,exist_ok=True)
for n in range(1,32):
 blob=(src/f'{n:02d}.dpcm').read_bytes();r=original[n];assert hashlib.sha256(blob).hexdigest()==r['sha256']
 if n==14:
  config=json.loads((root/'data/yokai/audio_loops.json').read_text());row=next(r for r in config['gap_tracks'] if r['number']==14)
  assert len(blob)==row['input_bytes'] and hashlib.sha256(blob).hexdigest()==row['input_sha256']
  typ,status,freq,start,size=struct.unpack('<HHIII',blob[:16]);assert (typ,status,start,size)==(1,0,0,row['input_samples'])
  blob=struct.pack('<HHIII',typ,0x4000,freq,0,size)+blob[16:]
  r.update(bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),loop_start_samples=0,source_end_samples=size,loop_length_samples=size,playback='whole-track repetition; original fade and silence preserved',perceptual_listening_validated=False)
 (out/f'{n:02d}.dpcm').write_bytes(blob)
for name in ['yokai_music.s','yokai_music_gap.s']:
 text=(src/name).read_text();assert str(src) in text;(out/name).write_text(text.replace(str(src),str(out)))
m['scope']='Existing30 byte-identical; only track14 original one-shot WaveData header gains full-source repetition. Musical seam not approved by listening.'
(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(dict(output=str(out),changed_track=14,other_streams_identical=30,compressed_zombie_blocks_unchanged=True,seam='Original fade-out and leading silence retained'),indent=2))

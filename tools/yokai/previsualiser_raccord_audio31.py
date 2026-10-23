#!/usr/bin/env python3
"""Private A/B audition from original DPCM; never enables a proposed ROM loop.

Positions are native source sample indices. No crossfade, volume normalization
or time stretch. Generated audio stays outside every Git checkout.
"""
import argparse, hashlib, json, struct, subprocess, wave
from pathlib import Path
import numpy as np
from dpcm_m4a import decode

ROOT = Path(__file__).resolve().parents[2]
def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--number', type=int, required=True)
    p.add_argument('--full-dpcm-dir', type=Path, required=True)
    p.add_argument('--loop-start', type=int, required=True)
    p.add_argument('--loop-end', type=int, required=True)
    p.add_argument('--private-output', type=Path, required=True)
    a = p.parse_args()
    out = a.private_output.resolve()
    assert not out.is_relative_to(ROOT), 'Private audio must stay outside checkout'
    # Also reject another Git checkout, including sibling worktrees.
    check = next((v for v in (out, *out.parents) if v.exists()), None)
    assert check is not None
    assert subprocess.run(['git','-C',str(check),'rev-parse','--is-inside-work-tree'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0
    config = json.loads((ROOT/'data/yokai/audio_loops.json').read_text())
    row = next(r for r in config['gap_tracks'] if r['number']==a.number)
    blob = (a.full_dpcm_dir/f'{a.number:02d}.dpcm').read_bytes()
    assert hashlib.sha256(blob).hexdigest() == row['input_sha256'], 'Wrong private original'
    count = struct.unpack_from('<I',blob,12)[0]
    assert 0 <= a.loop_start < a.loop_end <= count
    rate = row['rate']; margin = 4*rate
    assert a.loop_start >= margin and a.loop_end+margin <= count, 'Need four seconds of source context on both sides'
    pcm = np.array(decode(blob[16:],count),dtype=np.int16)*256
    original = pcm[a.loop_end-margin:a.loop_end+margin]
    proposed = np.r_[pcm[a.loop_end-margin:a.loop_end],pcm[a.loop_start:a.loop_start+margin]]
    head = pcm[a.loop_start-margin:a.loop_start+margin]
    out.mkdir(parents=True,exist_ok=True)
    for label, samples in [('A-continuation-originale',original),('B-raccord-propose-x3',np.tile(proposed,3)),('C-contexte-retour',head)]:
        with wave.open(str(out/f'{a.number:02d}-{label}.wav'),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(samples.astype('<i2').tobytes())
    (out/f'{a.number:02d}-proposition.json').write_text(json.dumps(dict(number=a.number,
        loop_start_samples=a.loop_start,loop_end_samples=a.loop_end,
        loop_start_seconds=a.loop_start/rate,loop_end_seconds=a.loop_end/rate,
        source_sha256=row['input_sha256'],status='AUDITION PROPOSAL ONLY, NOT AN APPROVED LOOP',
        A='Original continuation: seam at 4s',B='Proposed return: seams at 4/12/20s; 8s A/B excerpts repeated for comparison, not a full musical loop',
        C='Context around proposed return, centre at 4s',perceptual_listening_validated=False),indent=2)+'\n')
    print('Private audition generated:',out)

if __name__=='__main__':main()

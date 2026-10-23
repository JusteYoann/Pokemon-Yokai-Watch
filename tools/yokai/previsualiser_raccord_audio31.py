#!/usr/bin/env python3
"""Private A/B audition from original DPCM; never enables a proposed ROM loop.

Positions are native source sample indices. No crossfade, volume normalization
or time stretch. Generated audio stays outside every Git checkout.
"""
import argparse, hashlib, json, struct, subprocess, wave, re
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
    p.add_argument('--long-comparison', action='store_true', help='10s before/15s after and two true returns separated by a complete cycle')
    p.add_argument('--label', default=None, help='Filename label for comparison variants, e.g. A-ancienne')
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
    rate = row['rate']; before = (10 if a.long_comparison else 4)*rate
    after = (15 if a.long_comparison else 4)*rate
    assert a.loop_start >= before and a.loop_end+after <= count, 'Insufficient original context around these points'
    assert a.loop_end-a.loop_start >= max(before,after), 'Cycle shorter than audition context'
    assert a.label is None or re.fullmatch(r'[A-Za-z0-9_-]+',a.label), 'Unsafe filename label'
    pcm = np.array(decode(blob[16:],count),dtype=np.int16)*256
    original = pcm[a.loop_end-before:a.loop_end+after]
    proposed = np.r_[pcm[a.loop_end-before:a.loop_end],pcm[a.loop_start:a.loop_start+after]]
    head = pcm[a.loop_start-before:a.loop_start+after]
    out.mkdir(parents=True,exist_ok=True)
    prefix = a.label or f'{a.number:02d}'
    if a.long_comparison:
        twice = np.r_[pcm[a.loop_end-before:a.loop_end],pcm[a.loop_start:a.loop_end],pcm[a.loop_start:a.loop_start+after]]
        outputs=[('raccord-25s',proposed),('deux-retours-reels',twice),('continuation-originale-25s',original),('contexte-retour-25s',head)]
        period=(a.loop_end-a.loop_start)/rate
        timing=dict(first_return_seconds=10,second_return_seconds=10+period,
                    second_return_minutes_seconds=f'{int((10+period)//60)}:{(10+period)%60:06.3f}',
                    montage='10s source tail + one complete cycle + 15s after second return. No artificial excerpt repetition.')
    else:
        outputs=[('A-continuation-originale',original),('B-raccord-propose-x3',np.tile(proposed,3)),('C-contexte-retour',head)]
        timing=dict(A='Original continuation: seam at 4s',B='Proposed return: seams at 4/12/20s; 8s A/B excerpts repeated for comparison, not a full musical loop',C='Context around proposed return, centre at 4s')
    for label, samples in outputs:
        with wave.open(str(out/f'{prefix}-{label}.wav'),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(samples.astype('<i2').tobytes())
    (out/f'{prefix}-proposition.json').write_text(json.dumps(dict(number=a.number,
        loop_start_samples=a.loop_start,loop_end_samples=a.loop_end,
        loop_start_seconds=a.loop_start/rate,loop_end_seconds=a.loop_end/rate,
        source_sha256=row['input_sha256'],status='AUDITION PROPOSAL ONLY, NOT AN APPROVED LOOP',
        **timing,perceptual_listening_validated=False),indent=2)+'\n')
    print('Private audition generated:',out)

if __name__=='__main__':main()

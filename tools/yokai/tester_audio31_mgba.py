#!/usr/bin/env python3
"""Real mGBA mixer regression for 31 songs, including full one-shot endings.

Uses a controller-started new game, then explicit isolated music calls. This is
not event traversal, subjective listening or hardware testing. Audio stays private.
"""
import ctypes, hashlib, json, os, struct, wave
from pathlib import Path

import numpy as np
from scipy.signal import fftconvolve, resample_poly
from dpcm_m4a import decode
from mgba_new_game import new_game
from mgba_rpc import BATCH, ROOT
from tester_musiques_integrees_mgba import channel

P = ROOT / os.environ.get('YOKAI_AUDIO31_REPORT_DIR', 'QA_RECETTE_FINALE/AUDIO_31_OST/lecture')
P.mkdir(parents=True, exist_ok=True)
private = Path(os.environ['YOKAI_AUDIO_DIR'])
r = new_game()
base = r.snapshot()
results = []
passed = False
error = 'Interrupted'
try:
    for n in map(int, os.environ.get('YOKAI_AUDIO31_TEST_NUMBERS', ','.join(map(str, range(1,32)))).split(',')):
        assert 1 <= n <= 31
        r.restore(base)
        r.call('m4aMPlayAllStop')
        r.call('m4aSongNumStart', 346 + n)
        r.run(30)
        ptr = channel(r, n)
        assert ptr, (n, 'Native sample channel absent')
        first = r.u32(ptr + 40)
        chunks = []
        def capture(data, frames):
            chunks.append(ctypes.string_at(data, frames * 4))
            return frames
        callback = BATCH(capture)
        r.lib.retro_set_audio_sample_batch(callback)
        for frame in range(480):
            if frame == 120: r.call('PlaySE', 5)
            if frame == 240: r.call('PlayCry_Normal', 1, 0)
            r.run()
        r.lib.retro_set_audio_sample_batch(r.callbacks[3])
        blob = (private / f'{n:02d}.dpcm').read_bytes()
        _, flags, _, loop, count = struct.unpack_from('<HHIII', blob)
        decoded = np.array(decode(blob[16:], count), dtype=float)
        signal = np.frombuffer(b''.join(chunks), '<i2').reshape(-1, 2).mean(axis=1)
        actual = resample_poly(resample_poly(signal, 125, 2048), 4, 1)
        reference = resample_poly(resample_poly(decoded[first:first+8*13379], 4000, 13379), 4, 1)
        scores = []
        for second in (.5, 6):
            template = reference[round(second*16000):round((second+1)*16000)]
            template = template - template.mean()
            search = actual[round((second-.25)*16000):round((second+1.25)*16000)]
            cross = fftconvolve(search, template[::-1], mode='valid')
            variance = fftconvolve(search**2, np.ones(len(template)), mode='valid') - fftconvolve(search, np.ones(len(template)), mode='valid')**2 / len(template)
            scores.append(float(max(cross / np.sqrt(np.maximum(1e-12, variance * sum(template**2))))))
        assert min(scores) > .85, (n, 'Actual mixer/source mismatch', scores)
        assert r.call('IsCryFinished') != 0
        row = dict(number=n, passed=True, mixer_source_correlations=scores,
                   native_SFX_and_cry_calls=True, perceptual_listening_validated=False)
        if flags == 0:
            # Actually play through the original ending, without seeking or
            # rewriting sample counters. Record the natural stop and no restart.
            frames = 0
            while channel(r, n) and frames < count//224+180:
                r.run(); frames += 1
            assert channel(r, n) is None, (n, 'One-shot did not finish')
            r.run(180)
            assert channel(r, n) is None, (n, 'Unexpected automatic restart')
            row.update(full_one_shot_end_observed=True, ending_frames_after_excerpt=frames,
                       known_limitation='Silence after natural ending until another BGM request; loop not validated')
        r.frame.save(P / f'ost-{n:02d}.png')
        results.append(row)
        print('MIXER PASS', n, scores, flush=True)
    # Native fanfare must resume the same compressed BGM, not restart it.
    r.restore(base); r.call('m4aSongNumStart', 351); r.run(120)
    before = r.u32(channel(r, 5) + 40)
    r.call('PlayFanfare', 258)
    for frames in range(1800):
        r.run()
        if frames > 120 and r.call('IsFanfareTaskInactive'): break
    else: raise AssertionError('Item fanfare never finished')
    r.run(30)
    assert r.u32(r.symbols['gMPlayInfo_BGM']) == r.symbols['mus_yokai_05']
    assert channel(r, 5) and r.u32(channel(r, 5) + 40) >= before
    results.append(dict(native_item_fanfare_completed=True, compressed_music_resumed_without_restart=True))
    passed = True
    error = None
except BaseException as exc:
    error = str(exc)
    raise
finally:
    r.close()
    (P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed, error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(), results=results,
        scope='Real mGBA audio callback/source correlation, SFX and cry calls, complete one-shot endings and item fanfare. Isolated starts after real new game. Not subjective listening.'), indent=2)+'\n')

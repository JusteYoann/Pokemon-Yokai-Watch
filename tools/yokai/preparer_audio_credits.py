#!/usr/bin/env python3
"""Preserve the existing private31 pack and add the supplied full credits OST.

Everything produced by this script stays outside the repository. No sequence
transcription is claimed: mono native DPCM, original duration, no forced loop.
"""
import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import wave
from pathlib import Path
from dpcm_m4a import wave_data

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source-dir', type=Path, required=True)
p.add_argument('--mp3', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--rate', type=int, default=12000)
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
src, out = a.source_dir.resolve(), a.output.resolve()
assert src != out and not out.is_relative_to(root)
assert hashlib.sha256(a.mp3.read_bytes()).hexdigest() == 'd5fc7b40873b4ccba91e28098270aa818095fd7789c7ab2b032d0f15af1a3512'
out.mkdir(parents=True, exist_ok=True)
for f in src.glob('*.dpcm'):
    shutil.copy2(f, out / f.name)
for name in ['yokai_music.s', 'yokai_music_gap.s']:
    (out / name).write_text((src / name).read_text().replace(str(src), str(out)))
wav = out / 'credits-mono.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(a.mp3), '-ac', '1', '-ar', str(a.rate), '-c:a', 'pcm_s16le', str(wav)], check=True)
with wave.open(str(wav), 'rb') as f:
    pcm = f.readframes(f.getnframes())
samples = [max(-128, min(127, round(x[0] / 256))) for x in struct.iter_unpack('<h', pcm)]
blob = wave_data(samples, a.rate)
(out / 'credits.dpcm').write_bytes(blob)
(out / 'credits_music.s').write_text('''.section .rodata
.align 2
.global mus_yokai_credits
mus_yokai_credits:
.byte 1,0,0,0
.4byte yokai_voice_credits, yokai_track_credits
yokai_voice_credits:
.byte 0x20,60,0,0
.4byte yokai_wave_credits
.byte 255,0,255,0
yokai_track_credits:
.byte 0xbb,75,0xbd,0,0xbe,80,0xcf,60,100
yokai_wait_credits:
.byte 0xb0,0xb2
.4byte yokai_wait_credits
.align 2
.global yokai_wave_credits
yokai_wave_credits:
.incbin "''' + str(out / 'credits.dpcm') + '"\n')
report = dict(rate=a.rate, samples=len(samples), duration_seconds=len(samples)/a.rate, bytes=len(blob), source_sha256=hashlib.sha256(a.mp3.read_bytes()).hexdigest(), encoded_sha256=hashlib.sha256(blob).hexdigest(), other31_streams_identical=all((out / f.name).read_bytes() == f.read_bytes() for f in src.glob('*.dpcm')), perceptual_listening_validated=False)
manifest = json.loads((src / 'manifest.json').read_text())
manifest['credits'] = report
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(report, indent=2))

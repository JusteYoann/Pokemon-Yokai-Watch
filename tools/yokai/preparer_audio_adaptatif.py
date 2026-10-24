#!/usr/bin/env python3
"""Re-encode selected private streams from pinned PCM16 originals, never decoded DPCM.

The private source map lists number (1..31 or 'credits'), path, source_start_samples,
samples and source_wav_sha256. All sources and generated audio stay outside Git.
Keep SDK encoding when adaptive encoding gains less than 1 dB over the full stream.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import wave

import numpy as np
from adpcm_m4a import decode
from dpcm_m4a import decode as decode_sdk

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-pack', type=Path, required=True)
    parser.add_argument('--source-map', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    source, output = args.source_pack.resolve(), args.output.resolve()
    assert source != output and not output.is_relative_to(ROOT)
    assert not source.is_relative_to(ROOT)
    rows = json.loads(args.source_map.read_text())
    assert {row['number'] for row in rows} == {*range(1,32), 'credits'}
    assert len(rows) == 32
    shutil.copytree(source, output, dirs_exist_ok=True)
    for file in output.glob('*.s'):
        file.write_text(file.read_text().replace(str(source), str(output)))
    with tempfile.TemporaryDirectory(prefix='yokai-adaptive-') as directory:
        temporary = Path(directory)
        encoder = temporary/'encoder'
        subprocess.run(['c++', '-O3', '-std=c++17', str(ROOT/'tools/yokai/encode_ima.cpp'),
                        '-o', str(encoder)], check=True)

        def convert(row):
            number = row['number']
            stem = f'{number:02d}' if isinstance(number, int) else number
            original = (source/(stem+'.dpcm')).read_bytes()
            kind, flags, frequency, loop, count = struct.unpack('<HHIII', original[:16])
            assert kind == 1 and count == row['samples']
            wav = Path(row['path'])
            assert hashlib.sha256(wav.read_bytes()).hexdigest() == row['source_wav_sha256']
            with wave.open(str(wav)) as stream:
                assert stream.getnchannels() == 1 and stream.getsampwidth() == 2
                assert stream.getframerate()*1024 == frequency
                stream.setpos(row['source_start_samples'])
                raw = stream.readframes(count)
            assert len(raw) == count*2
            raw_path, payload_path = temporary/(stem+'.raw'), temporary/(stem+'.ima')
            raw_path.write_bytes(raw)
            subprocess.run([str(encoder), str(raw_path), str(payload_path)], check=True)
            header = bytearray(original[:16])
            struct.pack_into('<H', header, 0, 2)
            adaptive = bytes(header) + payload_path.read_bytes()
            assert adaptive[2:16] == original[2:16]
            reference = np.frombuffer(raw, dtype='<i2').astype(float)/256
            before = np.asarray(decode_sdk(original[16:], count), dtype=float)
            after = np.asarray(decode(adaptive[16:], count), dtype=float)

            def snr(samples):
                error = reference-samples
                return float(10*np.log10(np.dot(reference,reference)/np.dot(error,error)))

            old_snr, new_snr = snr(before), snr(after)
            selected = new_snr >= old_snr+1
            chosen, decoded = (adaptive, after) if selected else (original, before)
            (output/(stem+'.dpcm')).write_bytes(chosen)
            report = dict(number=number, source_wav_sha256=row['source_wav_sha256'],
                          source_start_samples=row['source_start_samples'], samples=count,
                          rate_hz=frequency/1024, loop_start=loop if flags & 0x4000 else None,
                          before_bytes=len(original), after_bytes=len(chosen),
                          before_sha256=hashlib.sha256(original).hexdigest(),
                          after_sha256=hashlib.sha256(chosen).hexdigest(),
                          before_snr_db=old_snr, candidate_snr_db=new_snr,
                          after_snr_db=new_snr if selected else old_snr,
                          adaptive_selected=selected,
                          before_loop_step=float(abs(before[-1]-before[loop])) if flags & 0x4000 else None,
                          after_loop_step=float(abs(decoded[-1]-decoded[loop])) if flags & 0x4000 else None,
                          header_fields_except_type_preserved=True,
                          perceptual_listening_validated=False)
            print(stem, 'adaptive' if selected else 'SDK retained', old_snr, new_snr, flush=True)
            return report

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(convert, rows))
    manifest = json.loads((source/'manifest.json').read_text())
    manifest['adaptive_conversion'] = results
    for row in manifest['prepared_tracks']:
        result = next(item for item in results if item['number'] == row['number'])
        row.update(bytes=result['after_bytes'], sha256=result['after_sha256'])
    manifest['active_sample_bytes'] = sum(item['after_bytes'] for item in results if item['number'] != 'credits')
    credits = next(item for item in results if item['number'] == 'credits')
    manifest['credits'].update(bytes=credits['after_bytes'],
                               encoded_sha256=credits['after_sha256'],
                               other31_streams_identical=False,
                               codec='WaveData type2 adaptive IMA')
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (output/'adaptive-conversion.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()

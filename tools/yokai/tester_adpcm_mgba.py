#!/usr/bin/env python3
"""Verify ARM dispatch/cache against independent host decoders; synthetic audio only.

Set YOKAI_QA_ROM/ELF and YOKAI_ADPCM_QA_DIR. This uses temporary RAM fixtures;
it never edits a ROM, a saved game or production samples.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import random
import struct
import subprocess
import tempfile

from adpcm_m4a import decode
from dpcm_m4a import decode as decode_sdk, wave_data
from mgba_rpc import Emulator, ROOT


def main():
    output = Path(os.environ['YOKAI_ADPCM_QA_DIR'])
    output.mkdir(parents=True, exist_ok=True)
    r = Emulator()
    results = []
    try:
        r.call('ResetMapMusic')
        r.call('m4aMPlayAllStop')
        channel = r.call('AllocZeroed', 64)
        waves = [r.call('AllocZeroed', 4096) for _ in range(2)]
        wrapper = r.call('AllocZeroed', 128)
        assert channel and all(waves) and wrapper
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            assembly = f'''.syntax unified
.text
.thumb
push {{r4,lr}}
movs r4,r0
movs r3,r1
adr r2, arm_call
bx r2
.align 2
.arm
arm_call:
ldr r2, ={r.symbols['SoundMainRAM_Unk2'] & ~1}
mov lr,pc
bx r2
adr r0, returned+1
bx r0
.thumb
returned:
movs r0,r1
pop {{r4,pc}}
.pool
'''
            (p/'wrapper.s').write_text(assembly)
            subprocess.run(['arm-none-eabi-as', '-mcpu=arm7tdmi', str(p/'wrapper.s'),
                            '-o', str(p/'wrapper.o')], check=True)
            subprocess.run(['arm-none-eabi-objcopy', '-O', 'binary', str(p/'wrapper.o'),
                            str(p/'wrapper.bin')], check=True)
            r.write(wrapper, (p/'wrapper.bin').read_bytes())
            encoder = p/'encoder'
            subprocess.run(['c++', '-O3', '-std=c++17', str(ROOT/'tools/yokai/encode_ima.cpp'),
                            '-o', str(encoder)], check=True)
            vectors = {
                'silence': [0]*513,
                'extremes': [-32768,32767,0,-1,1,32000,-32000]*74,
                'sine': [round(30000*math.sin(2*math.pi*440*i/13379)) for i in range(777)],
                'ramp': list(range(-32768,32768,73)),
            }
            for name, samples in vectors.items():
                raw = struct.pack('<'+'h'*len(samples), *samples)
                (p/'input.raw').write_bytes(raw)
                subprocess.run([str(encoder), str(p/'input.raw'), str(p/'output.ima')], check=True)
                payload = (p/'output.ima').read_bytes()
                expected = decode(payload, len(samples))
                blob = struct.pack('<HHIII', 2, 0, 13379*1024, 0, len(samples)) + payload
                for pointer in waves:
                    r.write(pointer, blob)
                r.w32(r.symbols['gYokaiImaCache'], 0)
                positions = list(range(min(len(samples), 270)))
                positions += [len(samples)-1, 0, 255, 256, 511, 512]
                positions += random.Random(121).choices(range(len(samples)), k=100)
                for j, sample in enumerate(positions):
                    # Alternate identical data at different addresses to force cache ownership checks.
                    r.w32(channel+36, waves[j % 2])
                    actual = r.call(wrapper, channel, sample)
                    actual = struct.unpack('<i', struct.pack('<I', actual))[0]
                    assert actual == expected[sample], (name, sample, actual, expected[sample])
                results.append(dict(vector=name, checked_samples=len(positions), passed=True))
            # SDK type1 remains bit exact, including signed wrapping and 64-sample blocks.
            samples = [-128,127,0,-1,1,126,-127]*39
            blob = wave_data(samples, 13379)
            r.write(waves[0], blob)
            r.w32(channel+36, waves[0])
            expected = decode_sdk(blob[16:], len(samples))
            for sample in range(len(samples)):
                # xpi/xpc are the last word of the native 64-byte SoundChannel.
                r.w32(channel+60, 0xFFFFFFFF)
                actual = r.call(wrapper, channel, sample) & 255
                assert actual == (expected[sample] & 255), (sample, actual, expected[sample])
            results.append(dict(vector='original_sdk_type1', checked_samples=len(samples), passed=True))
    finally:
        r.close()
    report = dict(passed=True, native_decoder='SoundMainRAM_Unk2 ARM dispatcher + Thumb IMA',
                  rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(), results=results,
                  limitations='Synthetic decoding/cache verification, not listening or hardware profiling.')
    (output/'DECODER.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

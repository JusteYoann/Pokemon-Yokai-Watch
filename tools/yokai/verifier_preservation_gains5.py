#!/usr/bin/env python3
"""Verify the five approved private gain words are the only changed ROM bytes."""
import argparse
import hashlib
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = '0e7ff7f6096e5b52932e1e1cf090eaee3c53ee7ebe182ebbd5302feee2a2bfce'
PUBLIC = 'a00527774542439e1ab0976a45421911c8b067d8bd11730de183c453581b3b3c'
APPROVED = {351: (77, 423), 354: (109, 333), 359: (108, 315),
            360: (101, 302), 371: (64, 279)}


def symbols(path):
    return {f[2]: int(f[0], 16) for line in subprocess.check_output(
        ['arm-none-eabi-nm', '--defined-only', str(path)], text=True).splitlines()
        if len(f := line.split()) == 3}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reference-rom', type=Path, required=True)
    p.add_argument('--reference-elf', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    old = a.reference_rom.read_bytes()
    new = (ROOT/'pokefirered_audio.gba').read_bytes()
    public = (ROOT/'pokefirered.gba').read_bytes()
    digest = lambda data: hashlib.sha256(data).hexdigest()
    assert digest(old) == BASELINE
    assert digest(public) == PUBLIC
    assert len(old) == len(new) <= 33554432
    before = symbols(a.reference_elf)
    after = symbols(ROOT/'pokefirered_audio.elf')
    assert before == after, 'No symbol relocation is permitted for a gain-only change'
    offset = after['sYokaiSongGain'] - 0x08000000
    config = json.loads((ROOT/'data/yokai/mixer_calibration.json').read_text())
    overrides = {r['song_id']: r['gain_q8'] for r in config['private_gain_overrides']}
    assert overrides == {k: v[1] for k, v in APPROVED.items()}
    allowed = set()
    for song_id, (previous, current) in APPROVED.items():
        address = offset + 2*song_id
        assert struct.unpack_from('<H', old, address)[0] == previous
        assert struct.unpack_from('<H', new, address)[0] == current
        allowed.update((address, address+1))
    changed = {i for i, (x, y) in enumerate(zip(old, new)) if x != y}
    assert changed == allowed, sorted(changed ^ allowed)
    result = dict(passed=True, baseline_sha256=BASELINE,
        private_sha256=digest(new), public_sha256=digest(public),
        public_byte_identical=True, rom_bytes=len(new),
        remaining_to_32MiB=33554432-len(new),
        changed_bytes=len(changed), changed_offsets=[hex(i) for i in sorted(changed)],
        approved_gain_words=APPROVED, all_symbols_unchanged=True,
        all_audio_samples_loop_headers_code_graphics_gameplay_and_other_26_gains_byte_identical=True)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

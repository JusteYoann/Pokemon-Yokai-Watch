#!/usr/bin/env python3
"""Require every reference ROM byte preserved except gap, table and veneers.

Adding an object changes GNU ld's ordering of seven existing Thumb veneers.
Check their exact bytes by name, and decode every changed Thumb BL to require
the same original veneer destination. No allowance for arbitrary code changes.
"""
import argparse, hashlib, json, struct, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def symbols(path):
    return {f[2]: int(f[0], 16) for line in subprocess.check_output(
        ['arm-none-eabi-nm', '--defined-only', str(path)], text=True).splitlines()
        if len(f := line.split()) == 3}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reference-rom', type=Path, required=True)
    p.add_argument('--reference-elf', type=Path, required=True)
    p.add_argument('--report', type=Path, default=ROOT/'QA_RECETTE_FINALE/AUDIO_31_OST/MESURES.json')
    a = p.parse_args()
    old = a.reference_rom.read_bytes()
    new = (ROOT/'pokefirered_audio.gba').read_bytes()
    public = (ROOT/'pokefirered.gba').read_bytes()
    before = symbols(a.reference_elf)
    after = symbols(ROOT/'pokefirered_audio.elf')
    assert hashlib.sha256(old).hexdigest() == '6368e2c28cae2eeddf1d6439fcd279693fc67b8270d3f1b1bc5d75e3dd71c65c'
    assert hashlib.sha256(public).hexdigest() == 'a00527774542439e1ab0976a45421911c8b067d8bd11730de183c453581b3b3c'
    assert len(new) == len(old) <= 33554432
    origin = 0x08000000
    start = after['__yokai_audio_gap_start'] - origin
    end = after['__yokai_audio_gap_end'] - origin
    assert 0 <= start < end <= 0xd00000
    assert set(old[start:0xd00000]) == {255}
    assert set(new[end:0xd00000]) == {255}
    allowed = set()
    table = after['gYokaiPrivateHeaders'] - origin
    for n in (5, 8, 13, 14, 25): allowed.update(range(table+(n-1)*4, table+n*4))
    mask = after['gYokaiPrivateAudioMask'] - origin
    allowed.update(range(mask, mask+4))
    moved = [k for k in before.keys() & after.keys() if before[k] != after[k]]
    assert all(k.startswith('__Yokai') and k.endswith('_veneer') for k in moved), moved
    for name in moved:
        x, y = before[name]-origin, after[name]-origin
        assert old[x:x+16] == new[y:y+16], name
        allowed.update(range(x, x+16)); allowed.update(range(y, y+16))
    old_targets = {before[k]: k for k in moved}
    new_targets = {after[k]: k for k in moved}
    def target(blob, offset):
        hi, lo = struct.unpack_from('<HH', blob, offset)
        if hi & 0xf800 != 0xf000 or lo & 0xf800 != 0xf800: return None
        delta = ((hi & 0x7ff) << 12) | ((lo & 0x7ff) << 1)
        if delta & 0x400000: delta -= 0x800000
        return origin + offset + 4 + delta
    differences = [i for i, (x, y) in enumerate(zip(old, new)) if x != y and not start <= i < end]
    calls = set()
    for i in differences:
        if i in allowed: continue
        for offset in (i & ~1, (i & ~1)-2):
            x, y = old_targets.get(target(old, offset)), new_targets.get(target(new, offset))
            if x is not None and x == y:
                calls.add(offset); allowed.update(range(offset, offset+4)); break
        else: raise AssertionError(('Unexpected ROM change', hex(i+origin)))
    report = dict(passed=True, rom_before_bytes=len(old), rom_after_bytes=len(new),
        rom_after_sha256=hashlib.sha256(new).hexdigest(), public_bytes=len(public),
        public_sha256=hashlib.sha256(public).hexdigest(), public_byte_identical_to_reference=True,
        gap_start=hex(start+origin), gap_used_end=hex(end+origin),
        gap_used_bytes=end-start, gap_remaining_bytes=0xd00000-end,
        remaining_to_32MiB=33554432-len(new), differences_outside_gap_bytes=len(differences),
        permitted_changes='Five header pointers, mask, same-destination linker veneers and BL relocations only',
        relocated_original_veneers=moved, verified_same_destination_BL_calls=len(calls),
        original_26_samples_and_all_other_resources_preserved=True)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__': main()

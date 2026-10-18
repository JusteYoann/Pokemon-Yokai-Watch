#!/usr/bin/env python3
"""Pin agbcc runtime archive member order; preserve every member's bytes.

No ROM patch and no compiler/game-source change. Validate allocated ELF sections
against B13 before modifying an archive; keep an on-disk copy of prior archives.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile


def allocated_sections(data):
    if data[:6] != b'\x7fELF\x01\x01': raise ValueError('Expected little-endian ELF32')
    offset = struct.unpack_from('<I', data, 32)[0]
    size, count, strings_index = struct.unpack_from('<HHH', data, 46)
    rows = [struct.unpack_from('<10I', data, offset + size*i) for i in range(count)]
    string_row = rows[strings_index]
    names = data[string_row[4]:string_row[4]+string_row[5]]
    result = {}
    for name_offset, kind, flags, address, start, length, *_ in rows:
        if kind == 8 or not flags & 2 or not length: continue
        name = names[name_offset:].split(b'\0', 1)[0].decode('ascii')
        result[name] = {'bytes': length, 'sha256': hashlib.sha256(data[start:start+length]).hexdigest()}
    return result


def run(ar, *args):
    return subprocess.check_output([ar, *map(str, args)])


def normalise(directory, lock, ar):
    verified = []
    # Validate both libraries entirely before writing either one.
    for name, config in lock['libraries'].items():
        if Path(name).name != name: raise ValueError('Unsafe archive name')
        archive = (directory/name).resolve(strict=True)
        order = run(ar, 't', archive).decode().splitlines()
        wanted = [member['name'] for member in config['members']]
        if len(order) != len(set(order)) or set(order) != set(wanted):
            raise ValueError(f'{name}: archive members differ from B13; no modification')
        members = {}
        for member in config['members']:
            member_name = member['name']
            if Path(member_name).name != member_name: raise ValueError('Unsafe member name')
            data = run(ar, 'p', archive, member_name)
            if allocated_sections(data) != member['allocated_sections']:
                raise ValueError(f'{name}:{member_name}: compiled code differs from B13; no modification')
            members[member_name] = data
        verified.append((archive, order, wanted, members))
    result = []
    for archive, order, wanted, members in verified:
        before = hashlib.sha256(archive.read_bytes()).hexdigest()
        backup = None
        if order != wanted:
            # Same filesystem, atomic archive replacement; preserve the old archive.
            with tempfile.TemporaryDirectory(prefix='b13-order-', dir=directory) as temporary:
                temp = Path(temporary)
                for name, data in members.items(): (temp/name).write_bytes(data)
                rebuilt = temp/archive.name
                run(ar, 'rcsD', rebuilt, *[temp/name for name in wanted])
                if run(ar, 't', rebuilt).decode().splitlines() != wanted:
                    raise ValueError('Archive order verification failed')
                for name, original in members.items():
                    if run(ar, 'p', rebuilt, name) != original:
                        raise ValueError('Archive member bytes changed')
                backup = Path(tempfile.mkdtemp(prefix='b13-original-', dir=directory))/archive.name
                shutil.copy2(archive, backup)
                rebuilt.replace(archive)
        result.append({'archive': archive.name, 'members_verified': len(wanted),
                       'order_changed': order != wanted, 'member_bytes_preserved': True,
                       'before_sha256': before, 'after_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                       'backup': str(backup) if backup else None})
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lib-dir', type=Path, required=True)
    p.add_argument('--lock', type=Path, required=True)
    p.add_argument('--ar', default='arm-none-eabi-ar')
    args = p.parse_args()
    lock = json.loads(args.lock.read_text())
    if lock['agbcc_commit'] != 'da598c1d918402c42c0c0d7128ba14567f3175e9':
        raise ValueError('Unexpected B13 compiler lock')
    print(json.dumps(normalise(args.lib_dir.resolve(strict=True), lock, args.ar), indent=2))


if __name__ == '__main__': main()

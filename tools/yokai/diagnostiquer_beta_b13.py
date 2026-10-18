#!/usr/bin/env python3
"""Read-only B13 build diagnostics. Reports hashes, never ROM/audio contents."""
import argparse
import hashlib
import json
import importlib.metadata
from pathlib import Path
import shutil
import struct
import subprocess

EXPECTED = '36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def command(args, cwd=None):
    try:
        result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=30)
        return {'exit': result.returncode, 'output': result.stdout.strip(),
                'error': result.stderr.strip()[:1000]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'error': str(e)}


def elf_sections(path):
    data = path.read_bytes()
    if data[:6] != b'\x7fELF\x01\x01':
        raise ValueError(f'Expected little-endian ELF32: {path.name}')
    offset = struct.unpack_from('<I', data, 32)[0]
    size, count, strings_index = struct.unpack_from('<HHH', data, 46)
    rows = [struct.unpack_from('<10I', data, offset + size * i) for i in range(count)]
    strings_row = rows[strings_index]
    names = data[strings_row[4]:strings_row[4] + strings_row[5]]
    result = {}
    for row in rows:
        name_offset, kind, flags, address, start, length = row[:6]
        if kind == 8 or not flags & 2 or not length:  # exclude BSS/debug/path metadata
            continue
        name = names[name_offset:].split(b'\0', 1)[0].decode('ascii', 'replace')
        result[name] = {'bytes': length, 'sha256': digest(data[start:start + length])}
    return result


def collect(repo, audio=None, full=None):
    rom = repo / 'pokefirered_audio.gba'
    data = rom.read_bytes()
    objects = {str(p.relative_to(repo / 'build/firered_audio')): elf_sections(p)
               for p in sorted((repo / 'build/firered_audio').rglob('*.o'))}
    generated = {}
    for name in ['src/data/items.h', 'src/data/region_map/region_map_entry_strings.h']:
        p = repo / name
        if p.exists(): generated[name] = digest(p.read_bytes())
    audio_hashes = {}
    if audio:
        for p in sorted(audio.glob('*.dpcm')):
            audio_hashes[p.name] = {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
    wave_hashes = {}
    if full:
        for p in sorted(full.glob('*.wav')):
            wave_hashes[p.name] = {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
    mp3 = {}
    extracted = full.parent / 'extracted/manifest-private.json' if full else None
    if extracted and extracted.exists():
        entries = json.loads(extracted.read_text())
        candidates = json.loads((repo / 'data/yokai/audio_candidates.json').read_text())
        for track in candidates['tracks']:
            if not track.get('selected_v1', True): continue
            matches = [entry for entry in entries if Path(entry['member']).stem == track['source_stem']]
            values = []
            for entry in matches:
                source = Path(entry['private_path'])
                values.append({'manifest_sha256': entry['sha256'],
                               'actual_sha256': digest(source.read_bytes()) if source.exists() else None})
            mp3[f"{track['number']:02d}"] = values
    libraries = {}
    for name in ['numpy', 'scipy', 'Pillow']:
        try: libraries[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: libraries[name] = 'NOT INSTALLED IN THIS PYTHON'
    binaries = {}
    for name in ['agbcc', 'old_agbcc', 'agbcc_arm']:
        p = repo / 'tools/agbcc/bin' / name
        if p.exists(): binaries[name] = digest(p.read_bytes())
    tools = {}
    for name in ['gcc', 'g++', 'make', 'ffmpeg', 'python3', 'arm-none-eabi-as', 'arm-none-eabi-ld', 'arm-none-eabi-objcopy']:
        executable = shutil.which(name)
        tools[name] = command([executable, '-version' if name == 'ffmpeg' else '--version']) if executable else {'missing_from_PATH': True}
        if 'output' in tools[name]: tools[name]['output'] = tools[name]['output'].splitlines()[:2]
    return {'rom_sha256': digest(data), 'rom_bytes': len(data),
            'rom_64k_blocks': [digest(data[i:i+65536]) for i in range(0, len(data), 65536)],
            'rom_allocated_sections': elf_sections(repo / 'pokefirered_audio.elf'),
            'object_allocated_sections': objects, 'generated_headers': generated,
            'dpcm': audio_hashes, 'wav': wave_hashes, 'compiler_binaries': binaries,
            'source_mp3': mp3, 'python_libraries': libraries, 'tools': tools, 'commit': command(['git', 'rev-parse', 'HEAD'], repo),
            'git_status': command(['git', 'status', '--short'], repo),
            'packages': command(['dpkg-query', '-W', '-f=${Package} ${Version}\n', 'gcc', 'g++', 'cpp', 'libc6', 'libstdc++6', 'ffmpeg', 'python3']),
            'scope': 'Hashes and version metadata only; no ROM, audio bytes, credentials or environment dump'}


def compare(actual, reference):
    result = {'exact_expected_rom': actual['rom_sha256'] == EXPECTED}
    for key in ['generated_headers', 'source_mp3', 'dpcm', 'wav', 'object_allocated_sections', 'rom_allocated_sections', 'compiler_binaries']:
        a, b = actual[key], reference[key]
        result[key] = {'different': [k for k in sorted(a.keys() & b.keys()) if a[k] != b[k]],
                       'missing': sorted(b.keys() - a.keys()), 'extra': sorted(a.keys() - b.keys())}
    result['different_rom_64k_blocks'] = [i for i, (a, b) in enumerate(zip(actual['rom_64k_blocks'], reference['rom_64k_blocks'])) if a != b]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--work', type=Path, help='Existing WSL diagnostic directory containing sources/, outils/, audio-prive/')
    group.add_argument('--repo', type=Path, help='Existing checkout (reference generation)')
    parser.add_argument('--audio', type=Path)
    parser.add_argument('--full-sources', type=Path)
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo or args.work / 'sources'
    audio = args.audio or (args.work / 'audio-prive/integration' if args.work else None)
    full = args.full_sources or (args.work / 'audio-prive/sources' if args.work else None)
    report = collect(repo, audio, full)
    if args.reference:
        reference = json.loads(args.reference.read_text())
        if reference['rom_sha256'] != EXPECTED: raise ValueError('Reference B13 incorrecte')
        report['comparison'] = compare(report, reference)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(args.output), 'rom_sha256': report['rom_sha256'],
                      'comparison': report.get('comparison')}, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Repair only agbcc archive ordering and relink existing B13 objects, no compile."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from diagnostiquer_beta_b13 import collect, compare, EXPECTED
from normaliser_bibliotheques_b13 import normalise

DIVERGENT = '505eabc4470f967aa2d6c6441f923dfa0ea530a16008de8b41a1bcfda1287b79'
CHECKPOINT = 'ff1cb36b2ecbe7b8ce167e375a6bff378df31347'
NAME = 'pokemon-yokai-BETA-B13-20261018.gba'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def repair(work, output, reference, lock):
    repo = work/'sources'
    rom = repo/'pokefirered_audio.gba'
    initial = sha(rom)
    if initial not in [DIVERGENT, EXPECTED] or rom.stat().st_size != 24400776:
        raise ValueError('This is not the diagnosed B13 ROM; stop without modifying it')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip() != CHECKPOINT:
        raise ValueError('Unexpected source checkpoint; stop')
    if subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=repo, text=True).strip():
        raise ValueError('Tracked source changes present; stop without overwriting them')
    target = output/NAME
    output.mkdir(parents=True, exist_ok=True)
    if target.exists() and sha(target) != EXPECTED:
        raise ValueError(f'Existing different output not overwritten: {target}')
    run = Path(tempfile.mkdtemp(prefix='b13-repair-', dir=work))
    before = collect(repo, work/'audio-prive/integration', work/'audio-prive/sources')
    differences = compare(before, reference)
    raw_objects = {name: sha(repo/'build/firered_audio'/name) for name in reference['object_allocated_sections']}
    (run/'diagnostic-before.json').write_text(json.dumps(before, indent=2)+'\n')
    for key in ['generated_headers', 'source_mp3', 'dpcm', 'wav', 'object_allocated_sections']:
        if any(differences[key].values()): raise ValueError(f'{key} differs; no repair attempted')
    sections = differences['rom_allocated_sections']
    if sections['missing'] or sections['extra'] or sections['different'] not in [[], ['lib_text']]:
        raise ValueError('Difference outside diagnosed library section; stop')
    if initial == EXPECTED:
        candidate = rom
        changes = []
    else:
        # Use exactly the original linker inputs, not make or a new compilation.
        build = repo/'build/firered_audio'
        objects = []
        libraries = []
        for line in (repo/'pokefirered_audio.map').read_text().splitlines():
            if not line.startswith('LOAD '): continue
            name = line[5:]
            if name == 'linker stubs': continue
            p = (build/name).resolve(strict=True)
            if not p.is_relative_to(repo.resolve()): raise ValueError('Link input outside checkout')
            if name.endswith('.o'): objects.append(name)
            elif name in ['../../tools/agbcc/lib/libgcc.a', '../../tools/agbcc/lib/libc.a']:
                libraries.append(name)
            else: raise ValueError(f'Unexpected linker input: {name}')
        if len(objects) != len(set(objects)) or set(objects) != set(reference['object_allocated_sections']):
            raise ValueError('Linker object list differs from reference')
        if libraries != ['../../tools/agbcc/lib/libgcc.a', '../../tools/agbcc/lib/libc.a']:
            raise ValueError('Unexpected runtime library order')
        changes = normalise(repo/'tools/agbcc/lib', lock, 'arm-none-eabi-ar')
        elf = run/'beta.elf'
        subprocess.run(['arm-none-eabi-ld', '-Map', str(run/'beta.map'), '-T', '../../ld_script.ld',
                        '--print-memory-usage', '-o', str(elf), *objects, '-L', '../../tools/agbcc/lib', '-lgcc', '-lc'], cwd=build, check=True)
        subprocess.run([str(repo/'tools/gbafix/gbafix'), str(elf), '-tPOKEMON FIRE', '-cBPRE', '-m01', '-r0', '--silent'], check=True)
        candidate = run/NAME
        subprocess.run(['arm-none-eabi-objcopy', '-O', 'binary', '--gap-fill', '0xFF', '--pad-to', '0x9000000', str(elf), str(candidate)], check=True)
    if sha(candidate) != EXPECTED or candidate.stat().st_size != 24400776:
        raise ValueError(f'Relinked ROM does not match B13: {sha(candidate)}; nothing exported')
    # Every original .o remains byte-for-byte unchanged in all allocated sections.
    after = collect(repo, work/'audio-prive/integration', work/'audio-prive/sources')
    if before['object_allocated_sections'] != after['object_allocated_sections']:
        raise ValueError('Original compiled objects changed; nothing exported')
    if raw_objects != {name: sha(repo/'build/firered_audio'/name) for name in raw_objects}:
        raise ValueError('An original object file changed; nothing exported')
    if sha(rom) != initial: raise ValueError('Original ROM changed; nothing exported')
    if not target.exists(): shutil.copyfile(candidate, target)
    report = {'version': 'BETA-B13-20261018', 'checkpoint': CHECKPOINT, 'original_sha256': initial,
              'rom_sha256': sha(target), 'rom_bytes': target.stat().st_size, 'active_ost': 13,
              'game_recompiled': False, 'original_rom_preserved': True,
              'compiled_objects_preserved': True, 'libraries': changes, 'output': str(target),
              'cause': 'libc.a member order from unsorted filesystem traversal changes ARM/Thumb veneer ordering'}
    target.with_suffix('.manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    (run/'repair.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--lock', type=Path, required=True)
    args = p.parse_args()
    reference = json.loads(args.reference.read_text())
    if reference['rom_sha256'] != EXPECTED: raise ValueError('Invalid ROM reference')
    lock = json.loads(args.lock.read_text())
    if lock['agbcc_commit'] != 'da598c1d918402c42c0c0d7128ba14567f3175e9': raise ValueError('Invalid runtime lock')
    repair(args.work.resolve(strict=True), args.output_dir.resolve(), reference, lock)

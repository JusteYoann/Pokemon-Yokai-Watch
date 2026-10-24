#!/usr/bin/env python3
"""Compare linked assets against pre-cleanup ROMs, including all 151 Yo-kai.

Baseline ROM/ELF files are local test inputs, never published in the repository.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from nettoyer_ressources_pokemon import ROOT, OUT, HEADER, audit


def symbols(path):
    found = {}
    for line in subprocess.check_output(['arm-none-eabi-nm', '-S', '--defined-only', str(path)], text=True).splitlines():
        if m := re.fullmatch(r'([0-9a-f]+) ([0-9a-f]+) \w (\S+)', line):
            addr, size, name = m.groups()
            if name in found:
                found[name] = None
            else:
                found[name] = (int(addr, 16), int(size, 16))
    return {k: v for k, v in found.items() if v is not None}


generated, inventory = audit()
assert (ROOT / HEADER).read_text() == generated, 'Generated cleanup differs from conservative audit'
removed = {r['symbol']: r for r in inventory['removed_resources']}
assert len(removed) == 168
assets = set()
for filename in subprocess.check_output(['git', 'ls-files', 'src'], cwd=ROOT, text=True).splitlines():
    p = ROOT / filename
    if p.suffix in {'.c', '.h'}:
        assets.update(re.findall(r'\b(\w+)\s*\[[^\]\n]*\]\s*=\s*(?:\{\s*)?INCBIN_', p.read_text(errors='replace')))

results = []
for stem in ['pokefirered', 'pokefirered_audio']:
    before = Path('/tmp/yokai-nettoyage-avant') / stem
    after = ROOT / stem
    old = symbols(before.with_suffix('.elf'))
    new = symbols(after.with_suffix('.elf'))
    old_rom = before.with_suffix('.gba').read_bytes()
    new_rom = after.with_suffix('.gba').read_bytes()

    def data(rom, entry):
        addr, size = entry
        assert 0x08000000 <= addr < 0x0A000000
        return rom[addr - 0x08000000:addr - 0x08000000 + size]

    unchanged = []
    for name in sorted(assets & old.keys() & new.keys() - removed.keys()):
        if not 0x08000000 <= old[name][0] < 0x0A000000:
            continue
        assert data(old_rom, old[name]) == data(new_rom, new[name]), ('retained asset changed', stem, name)
        unchanged.append(name)
    for name, row in removed.items():
        assert new[name][0] == new[row['fallback']][0], ('placeholder alias', name)
        assert old[name][0] != old[row['fallback']][0]
    # Fixed IDs, complete tables, tags and all unaffected table entries retained.
    entries = 0
    for table, stride in [('gMonFrontPicTable', 8), ('gMonBackPicTable', 8), ('gMonPaletteTable', 8), ('gMonShinyPaletteTable', 8), ('gMonIconTable', 4), ('gMonFootprintTable', 4)]:
        assert old[table][1] == new[table][1], ('table size', table)
        old_data = data(old_rom, old[table])
        new_data = data(new_rom, new[table])
        for off in range(0, len(old_data), stride):
            old_ptr = int.from_bytes(old_data[off:off+4], 'little')
            new_ptr = int.from_bytes(new_data[off:off+4], 'little')
            removed_entry = next((r for n, r in removed.items() if old[n][0] == old_ptr), None)
            if removed_entry:
                assert new_ptr == new[removed_entry['fallback']][0]
            elif old_ptr:
                candidates = [n for n in assets & old.keys() & new.keys() if old[n][0] == old_ptr]
                assert candidates, ('unidentified table pointer', table, off // stride)
                assert any(new[n][0] == new_ptr and data(old_rom, old[n]) == data(new_rom, new[n]) for n in candidates), ('table entry changed', table, off // stride)
            else:
                assert new_ptr == 0
            assert old_data[off+4:off+stride] == new_data[off+4:off+stride], ('table tags changed', table, off // stride)
            entries += 1
    results.append(dict(version=stem, unchanged_linked_assets=len(unchanged), aliases_verified=len(removed), table_entries_verified=entries, rom_sha256=hashlib.sha256(new_rom).hexdigest()))
OUT.mkdir(exist_ok=True, parents=True)
(OUT / 'TESTS_BINAIRES.json').write_text(json.dumps({'passed': True, 'results': results}, indent=2) + '\n')
print(json.dumps(results, indent=2))

#!/usr/bin/env python3
"""Conservative, reproducible removal of unused legacy graphics from the ROM.

Keep source originals for recovery. Keep species IDs/table sizes and safe aliases
for out-of-catalogue slots. Any runtime/script reference or direct graphics user
retains the original resource. This does not remove game mechanics or metadata.
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = '296055aab'
HEADER = 'src/data/graphics/pokemon.h'
OUT = ROOT / 'docs/nettoyage-pokemon-20261024'


def audit():
    original = subprocess.check_output(['git', 'show', f'{BASE}:{HEADER}'], cwd=ROOT, text=True)
    species = {name: int(n) for name, n in re.findall(r'#define SPECIES_(\w+) (\d+)\b', (ROOT / 'include/constants/species.h').read_text())}
    mapping = dict((stem, name) for name, stem in re.findall(r'SPECIES_SPRITE\((\w+), gMonFrontPic_(\w+)\)', (ROOT / 'src/data/pokemon_graphics/front_pic_table.h').read_text()))
    tracked = subprocess.check_output(['git', 'ls-files', 'src', 'data', 'include', 'asm'], cwd=ROOT, text=True).splitlines()
    runtime = {}
    direct = {}
    table_files = {HEADER, 'include/graphics.h', 'src/pokemon_icon.c'}
    table_files.update(str(p.relative_to(ROOT)) for p in (ROOT / 'src/data/pokemon_graphics').glob('*.h'))
    for filename in tracked:
        p = ROOT / filename
        if p.suffix not in {'.c', '.h', '.inc', '.s', '.json'}:
            continue
        text = p.read_text(errors='replace')
        # Indexed base-data tables describe all engine species, not encounters.
        metadata = (filename.startswith('src/data/pokemon/') and filename != 'src/data/pokemon/evolution.h') or filename.startswith('src/data/pokemon_graphics/') or filename in {'include/constants/species.h', 'src/data/text/species_names.h'} or filename.startswith('src/data/easy_chat/')
        if not metadata:
            if filename in {'src/pokemon_icon.c', 'src/menu2.c'}:
                text = re.sub(r'^\s*\[SPECIES_.*$', '', text, flags=re.M)
            for name in set(re.findall(r'\bSPECIES_(\w+)\b', text)):
                runtime.setdefault(name, []).append(filename)
        if filename not in table_files:
            for sym in set(re.findall(r'\bgMon(?:FrontPic|BackPic|Palette|ShinyPalette|Icon|Footprint)_\w+', text)):
                direct.setdefault(sym, []).append(filename)
    declarations = re.compile(r'const (u32|u8) (gMon(FrontPic|BackPic|Palette|ShinyPalette|Icon|Footprint)_(\w+))\[\] = INCBIN_\w+\("(graphics/pokemon/[^"\n]+)"\);')
    records = []
    keep = []
    for m in declarations.finditer(original):
        typ, sym, kind, stem, path = m.groups()
        name = mapping.get(stem)
        if name is None or not 152 <= species.get(name, 0) <= 411 or name in runtime or sym in direct:
            keep.append({'symbol': sym, 'species': name, 'runtime_references': runtime.get(name, []), 'direct_references': direct.get(sym, [])})
            continue
        fallback = {'FrontPic': 'gMonFrontPic_CircledQuestionMark', 'BackPic': 'gMonBackPic_CircledQuestionMark', 'Palette': 'gMonPalette_CircledQuestionMark', 'ShinyPalette': 'gMonShinyPalette_CircledQuestionMark', 'Icon': 'gMonIcon_QuestionMark', 'Footprint': 'gMonFootprint_QuestionMark'}[kind]
        records.append({'symbol': sym, 'type': typ, 'species': name, 'id': species[name], 'path': path, 'fallback': fallback})
    selected = {r['symbol']: r for r in records}

    def replace(m):
        if (r := selected.get(m.group(2))) is None:
            return m.group()
        return f'extern const {r["type"]} {r["symbol"]}[1] __attribute__((alias("{r["fallback"]}")));'

    generated = declarations.sub(replace, original)
    generated = '/* Unused legacy graphics share safe placeholders; see tools/yokai/nettoyer_ressources_pokemon.py. */\n' + generated
    return generated, {'baseline': BASE, 'removed_resources': records, 'retained_legacy_resources': keep, 'removed_resource_count': len(records), 'removed_species_count': len({r['id'] for r in records})}


if __name__ == '__main__':
    generated, report = audit()
    (ROOT / HEADER).write_text(generated)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'INVENTAIRE.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k.endswith('_count')}))

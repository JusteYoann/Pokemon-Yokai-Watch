#!/usr/bin/env python3
"""Contrôle hors ROM des ressources récupérées ; aucune intégration au moteur."""
import csv
import hashlib
import json
import re
import struct
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'RECUPERATION_PROJET'
SOURCES = OUT / 'sources_validees'
APPROVED = [17, 22, 41, 71, 84, 86, 100, 112, 114, 117, 124, 128, 133, 149]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def csv_rows(name):
    with (SOURCES / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter=';'))


def indices(raw, width, height):
    assert len(raw) == width * height // 2
    return bytes((raw[((y // 8) * (width // 8) + x // 8) * 32
                       + (y % 8) * 4 + (x % 8) // 2] >> (4 * (x % 2))) & 15
                 for y in range(height) for x in range(width))


report = {'scope': 'integrite des fichiers recuperes, pas validation du jeu',
          'custom_yokai_game_build_executed': False, 'emulator_executed': False}
for filename in ['PROVENANCE_GITHUB.json', 'PROVENANCE_DOCUMENTS.json']:
    rows = json.loads((OUT / filename).read_text())
    for row in rows:
        path = row.get('path', row.get('file'))
        assert sha((ROOT / path).read_bytes()) == row['sha256'], path
    report[filename] = {'verified_files': len(rows)}

manifest = json.loads((ROOT / 'docs/yokai-gallery/source-manifest.json').read_text())
canonical = csv_rows('NOMS_CANONIQUES_151_YOKAI_CODEX(1).csv')
assert len(canonical) == 151
assert [int(row['numero_yokai']) for row in canonical] == list(range(1, 152))
assert len({row['species_constant'] for row in canonical}) == 151
assert len({row['nom_yokai'] for row in canonical}) == 151
resources = 0
renames = []
with zipfile.ZipFile(ROOT / 'docs/yokai-gallery/sources/gba-graphics.zip') as archive:
    assert archive.testzip() is None
    assert json.loads(archive.read('manifest.json')) == manifest
    assert len(manifest['species']) == 151
    for entry, name in zip(manifest['species'], canonical):
        assert entry['index'] == int(name['numero_yokai'])
        assert entry['constant'] == name['species_constant']
        assert entry['species_id'] == int(name['species_id'])
        if entry['name'] != name['nom_yokai']:
            renames.append({'number': entry['index'], 'snapshot_name': entry['name'],
                            'canonical_name': name['nom_yokai']})
        for kind, asset in entry['resources'].items():
            raw = archive.read(asset['snapshot'])
            assert sha(raw) == asset['sha256'], asset['snapshot']
            if kind in ['front', 'back']:
                pixels = indices(raw, 64, 64)
                assert any(pixels), asset['snapshot']
            elif kind == 'icon':
                assert len(raw) == 1024
                assert any(indices(raw, 32, 64)), asset['snapshot']
            elif kind == 'footprint':
                assert len(raw) == 32
            else:
                assert len(raw) == 32
                assert all(value < 32768 for value, in struct.iter_unpack('<H', raw))
            resources += 1
    assert resources == 906
    for palette in range(3):
        assert len(archive.read(f'icons/palette-{palette}.gbapal')) == 32
report['gallery'] = {'species': 151, 'hashed_resources': resources,
                     'nonempty_combat_sprites': 302, 'shared_icon_palettes': 3,
                     'mapping_matches_canonical_151': True,
                     'snapshot_predates_final_names_and_shiny_art': True,
                     'name_differences_from_snapshot': renames}

proposals = []
for number in APPROVED:
    folder = ROOT / f'docs/yokai-sprite-rework/proposals/{number:03}'
    record = {'number': number, 'canonical_name': canonical[number - 1]['nom_yokai'],
              'approval_source': 'liste blanche explicite du createur dans la conversation',
              'applied_to_game': False, 'files': {}}
    for side in ['front', 'back']:
        path = folder / f'{side}.png'
        with Image.open(path) as image:
            image.load()
            assert image.mode == 'P' and image.size == (64, 64), str(path)
            pixels = image.get_flattened_data() if hasattr(image, 'get_flattened_data') else image.getdata()
            assert max(pixels) < 16 and any(pixels), str(path)
        record['files'][side] = {'path': str(path.relative_to(ROOT)),
                                 'sha256': sha(path.read_bytes())}
    for palette in ['normal', 'shiny']:
        path = folder / f'{palette}.pal'
        lines = path.read_text().splitlines()
        assert lines[:3] == ['JASC-PAL', '0100', '16']
        assert len(lines[3:19]) == 16
        for line in lines[3:19]:
            values = list(map(int, line.split()))
            assert len(values) == 3 and all(0 <= value <= 255 for value in values)
        record['files'][palette] = {'path': str(path.relative_to(ROOT)),
                                   'sha256': sha(path.read_bytes())}
    proposals.append(record)
(OUT / 'REDESIGNS_APPROUVES_RECUPERES.json').write_text(
    json.dumps(proposals, ensure_ascii=False, indent=2) + '\n')
report['approved_proposals'] = {'species': len(proposals), 'indexed_64x64_pngs': 28,
                                'normal_and_historical_shiny_palettes': 28,
                                'engine_integration_or_final_shiny_approval_implied': False}

stats = csv_rows('02_STATS_TYPES_TALENTS.csv')
assert len(stats) == 151
keys = ['pv', 'attaque', 'defense', 'attaque_speciale', 'defense_speciale', 'vitesse']
for row, name in zip(stats, canonical):
    assert row['numero_yokai'] == name['numero_yokai']
    assert row['species_constant'] == name['species_constant']
    assert all(1 <= int(row[key]) <= 255 for key in keys)
    assert sum(int(row[key]) for key in keys) == int(row['bst'])
    assert row['ability_1'].startswith('ABILITY_')
evolutions = csv_rows('03_EVOLUTIONS.csv')
learnsets = csv_rows('04_ATTAQUES_NIVEAU.csv')
tm = (SOURCES / 'Yokai_151_CT_CS_patch_Codex.txt').read_text()
tm_species = set(re.findall(r'^\s*\[(SPECIES_\w+)\]\s*=\s*TMHM_LEARNSET', tm, re.M))
assert tm_species == {name['species_constant'] for name in canonical}
report['validated_design_inputs'] = {
    'stats_species_with_valid_bst_sum': 151,
    'evolution_rows': len(evolutions),
    'initial_learnset_rows': len(learnsets),
    'initial_learnset_species': len({row['numero_yokai'] for row in learnsets}),
    'tm_hm_species_entries': len(tm_species),
    'obtaining_rows': len(csv_rows('REPARTITION_OBTENTION_151_YOKAI_CODEX.csv')),
    'implemented_in_game': False}

game_files = ['src/data/text/species_names.h', 'src/data/pokemon/species_info.h',
              'src/data/pokemon/evolution.h', 'src/data/trainers.h',
              'src/data/wild_encounters.json', 'src/battle_script_commands.c']
report['game_files_unchanged_from_original'] = []
import subprocess
for name in game_files:
    original = subprocess.check_output(['git', 'show', f'037335f4c:{name}'], cwd=ROOT)
    assert (ROOT / name).read_bytes() == original, name
    report['game_files_unchanged_from_original'].append(name)
report['verdict'] = 'RECUPERATION PARTIELLE ; BASE COMPLETE NON RETROUVEE'
(OUT / 'CONTROLES_EXECUTES.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))

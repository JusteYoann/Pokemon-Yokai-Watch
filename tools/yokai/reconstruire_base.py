#!/usr/bin/env python3
"""Reconstruction déterministe depuis les sources validées, sans retoucher les dessins."""
import csv
import hashlib
import json
import re
import shutil
import struct
import subprocess
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'RECUPERATION_PROJET/sources_validees'
OUTPUT = ROOT / 'QA_RECETTE_FINALE/RECONSTRUCTION'
OUTPUT.mkdir(parents=True, exist_ok=True)
BASE = '037335f4c725d7c9aecdac87066f2002b4bd7e14'
APPROVED = {17, 22, 41, 71, 84, 86, 100, 112, 114, 117, 124, 128, 133, 149}


def rows(name):
    with (INPUT / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def original(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT).decode()


def write(path, text):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')


def abbrev(name, limit):
    if len(name) <= limit:
        return name
    special = {'Robonyan 28': 'Robony.28.', 'Castelius III': 'Cast. III.',
               'Castelius II': 'Cast. II.', 'Castelius I': 'Cast. I.',
               'Castelius Max': 'Cast. Max.', 'Sergent Rampant': 'Serg.Ramp.',
               'Coach Antonic': 'C.Antonic.'}
    value = special.get(name, name[:limit - 1].rstrip() + '.')
    assert len(value) <= limit and value.endswith('.'), value
    return value


canonical = rows('NOMS_CANONIQUES_151_YOKAI_CODEX(1).csv')
stats = rows('02_STATS_TYPES_TALENTS.csv')
evos = rows('03_EVOLUTIONS.csv')
by_id = {int(row['numero_yokai']): row for row in canonical}
constants = {row['species_constant'] for row in canonical}
assert len(canonical) == len(stats) == len(constants) == 151
names = original('src/data/text/species_names.h')
display_names = []
for row in canonical:
    short = abbrev(row['nom_yokai'], 10)
    pattern = r'(\[' + row['species_constant'] + r'\]\s*=\s*_)\("[^"]*"\)'
    names, count = re.subn(pattern, lambda m: m[1] + '("' + short + '")', names)
    assert count == 1, row
    display_names.append({**row, 'nom_affiche_gba': short})
assert len({r['nom_affiche_gba'] for r in display_names}) == 151
write('src/data/text/species_names.h', names)
write('data/yokai/noms_affiches.json', json.dumps(display_names, ensure_ascii=False, indent=2) + '\n')

types = dict(zip(['Normal','Combat','Vol','Poison','Sol','Roche','Insecte','Spectre','Acier','Feu','Eau','Plante','Électrik','Psy','Glace','Dragon','Ténèbres'],
                 ['NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL','FIRE','WATER','GRASS','ELECTRIC','PSYCHIC','ICE','DRAGON','DARK']))
data = original('src/data/pokemon/species_info.h')
for row in stats:
    constant = row['species_constant']
    pattern = r'(\[' + constant + r'\]\s*=\s*\{)(.*?)(\n    \},)'
    match = re.search(pattern, data, re.S)
    assert match, constant
    body = match[2]
    for key, column in [('baseHP','pv'),('baseAttack','attaque'),('baseDefense','defense'),('baseSpeed','vitesse'),('baseSpAttack','attaque_speciale'),('baseSpDefense','defense_speciale')]:
        body, count = re.subn(r'\.' + key + r' = \d+,', '.' + key + ' = ' + row[column] + ',', body)
        assert count == 1
    second = row['type_2'] or row['type_1']
    body = re.sub(r'\.types = \{[^}]+\}', '.types = {TYPE_' + types[row['type_1']] + ', TYPE_' + types[second] + '}', body)
    body = re.sub(r'\.abilities = \{[^}]+\}', '.abilities = {' + row['ability_1'] + ', ' + (row['ability_2'] or 'ABILITY_NONE') + '}', body)
    # Uniform family growth prevents total experience changing level on evolution.
    body = re.sub(r'\.growthRate = \w+', '.growthRate = GROWTH_MEDIUM_FAST', body)
    data = data[:match.start()] + match[1] + body + match[3] + data[match.end():]
write('src/data/pokemon/species_info.h', data)

edges = defaultdict(list)
evolution_moves = defaultdict(list)
for row in evos:
    method = row['methode']
    if method == 'NIVEAU': method, param = 'EVO_LEVEL', row['niveau']
    elif method == 'PIERRE': method, param = 'EVO_ITEM', row['item_evolution']
    elif method == 'BONHEUR_ET_OBJET': method, param = 'EVO_FRIENDSHIP_HOLD', row['item_tenu']
    else: raise ValueError(row)
    edges[row['species_depart']].append('{' + f"{method}, {param}, {row['species_arrivee']}" + '}')
    if row['move_id_a_evolution']:
        evolution_moves[row['species_arrivee']].append(row['move_id_a_evolution'])
lines = ['// Generated from the validated 56-relation CSV. No legacy cross-dex evolutions.',
         'const struct Evolution gEvolutionTable[NUM_SPECIES][EVOS_PER_MON] =', '{']
for constant in sorted(constants):
    if constant in edges: lines.append('    [' + constant + '] = {' + ', '.join(edges[constant]) + '},')
lines.append('};\n')
write('src/data/pokemon/evolution.h', '\n'.join(lines))

tm = original('src/data/pokemon/tmhm_learnsets.h')
patch = (INPUT / 'Yokai_151_CT_CS_patch_Codex.txt').read_text()
for line in patch.splitlines():
    match = re.match(r'\s*\[(SPECIES_\w+)\]\s*=\s*(TMHM_LEARNSET\(.*\)),', line)
    if not match: continue
    constant, value = match.groups()
    tm, count = re.subn(r'(\[' + constant + r'\]\s*=\s*)TMHM_LEARNSET\(.*?\),', lambda m: m[1] + value + ',', tm, flags=re.S)
    assert count == 1, constant
write('src/data/pokemon/tmhm_learnsets.h', tm)

# Decode the historical tile snapshot into maintainable, indexed PNG sources.
def colors(raw):
    return [tuple(((v >> s) & 31) * 255 // 31 for s in (0,5,10)) for v, in struct.iter_unpack('<H', raw)]


def decode(raw, width, height, bits=4):
    pixels = []
    for y in range(height):
        for x in range(width):
            offset = ((y // 8) * (width // 8) + x // 8) * (8 * bits) + (y % 8) * bits + (x % 8) * bits // 8
            shift = (x % 2) * 4 if bits == 4 else x % 8
            pixels.append((raw[offset] >> shift) & ((1 << bits) - 1))
    return bytes(pixels)


def save_png(path, pixels, width, height, palette, bits=4):
    image = Image.frombytes('P', (width,height), pixels)
    image.putpalette([v for color in palette for v in color] + [0] * (768 - 3 * len(palette)))
    image.save(path, bits=bits, transparency=0)


graphics = original('src/data/graphics/pokemon.h')
icons = original('src/pokemon_icon.c')
coords = {side: original(f'src/data/pokemon_graphics/{side}_pic_coordinates.h') for side in ['front','back']}
elevation = original('src/data/pokemon_graphics/enemy_mon_elevation.h')
graphic_rows = []
with zipfile.ZipFile(ROOT / 'docs/yokai-gallery/sources/gba-graphics.zip') as archive:
    manifest = json.loads(archive.read('manifest.json'))
    for entry in manifest['species']:
        n, constant = entry['index'], entry['constant']
        folder = ROOT / f'graphics/yokai/{n:03}'
        folder.mkdir(parents=True, exist_ok=True)
        raw = {key: archive.read(value['snapshot']) for key,value in entry['resources'].items()}
        pal = colors(raw['normal'])
        for kind in ['normal','shiny']:
            p = colors(raw[kind]); (folder / f'{kind}.pal').write_text('JASC-PAL\n0100\n16\n' + ''.join(' '.join(map(str,c)) + '\n' for c in p))
        for side in ['front','back']:
            save_png(folder / f'{side}.png', decode(raw[side],64,64),64,64,pal)
        icon_pal = colors(archive.read(f'icons/palette-{entry["icon_palette_index"]}.gbapal'))
        save_png(folder/'icon.png',decode(raw['icon'],32,64),32,64,icon_pal)
        save_png(folder/'footprint.png',decode(raw['footprint'],16,16,1),16,16,[(255,255,255),(0,0,0)],1)
        if n in APPROVED:
            for name in ['front.png','back.png','normal.pal','shiny.pal']:
                shutil.copyfile(ROOT / f'docs/yokai-sprite-rework/proposals/{n:03}/{name}', folder / name)
        for kind, asset in entry['resources'].items():
            name = {'normal':'normal.gbapal.lz','shiny':'shiny.gbapal.lz','front':'front.4bpp.lz','back':'back.4bpp.lz','icon':'icon.4bpp','footprint':'footprint.1bpp'}[kind]
            symbol = asset['symbol']
            graphics, count = re.subn(r'(' + symbol + r'\[\] = INCBIN_\w+\(\s*")[^"]+("\);)', lambda m: m[1] + f'graphics/yokai/{n:03}/{name}' + m[2], graphics)
            assert count == 1, symbol
        icons, count = re.subn(r'(\['+constant+r'\]\s*=\s*)\d+(,)', lambda m:m[1]+str(entry['icon_palette_index'])+m[2],icons)
        assert count == 1, constant
        for side in ['front','back']:
            value = entry['positions'][side]
            coords[side], count = re.subn(r'(\['+constant+r'\]\s*=\s*\{).*?(\n    \},)',lambda m:m[1]+'\n        '+value+m[2],coords[side],flags=re.S)
            assert count == 1
        elevation = re.sub(r'\s*\['+constant+r'\]\s*=\s*\d+,', '', elevation)
        graphic_rows.append({'number':n,'constant':constant,'path':str(folder.relative_to(ROOT)),'approved_redesign':n in APPROVED,'final_shiny_restored':False})
    # Snapshot icons used their own three shared palettes; restore those exact colors.
    for i in range(3):
        p=colors(archive.read(f'icons/palette-{i}.gbapal'))
        write(f'graphics/pokemon/icon_palettes/icon_palette_{i}.pal', 'JASC-PAL\n0100\n16\n'+''.join(' '.join(map(str,c))+'\n' for c in p))
write('src/data/graphics/pokemon.h',graphics)
write('src/pokemon_icon.c',icons)
for side,text in coords.items():write(f'src/data/pokemon_graphics/{side}_pic_coordinates.h',text)
write('src/data/pokemon_graphics/enemy_mon_elevation.h',elevation)
write('data/yokai/graphics.json',json.dumps(graphic_rows,ensure_ascii=False,indent=2)+'\n')
write('data/yokai/evolution_moves.json',json.dumps(dict(evolution_moves),indent=2)+'\n')
print('Integrated 151 names/stats/graphics, 56 evolution edges, 151 TM/HM entries, 14 approved redesigns.')

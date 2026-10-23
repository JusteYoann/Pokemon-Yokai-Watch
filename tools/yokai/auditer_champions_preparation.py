#!/usr/bin/env python3
"""Read-only gameplay audit; writes only the Champions preparation dossier."""
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/champions-yokai-watch/preparation'
BASE = 'd32774305cc02651ea976f04c6a1174aabf42a05'
SCENARIO = '2647bc1627050f193cc9606f8c0f5f1151986047'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def read(path):
    return (ROOT / path).read_text()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def block(source, pattern):
    return re.search(pattern + r'\s*\{(.*?)\n    \}', source, re.S)[1]


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    names = {n['species_constant']: n for n in json.loads(read('data/yokai/noms_affiches.json'))}
    stats = read('src/data/pokemon/species_info.h')
    learns = read('src/data/pokemon/level_up_learnsets.h')
    pointers = read('src/data/pokemon/level_up_learnset_pointers.h')
    parties = read('src/data/trainer_parties.h')
    trainers = read('src/data/trainers.h')
    abilities = read('src/data/yokai_trainer_abilities.h')
    move_names = dict(re.findall(r'\[(MOVE_\w+)\]\s*= _\("([^"]+)"\)', read('src/data/text/move_names.h')))

    def member(sp, level, moves, iv=200, item='ITEM_NONE', slot=0):
        body = block(stats, r'\[' + sp + r'\] =')
        ptr = re.search(r'\[' + sp + r'\] = (\w+)', pointers)[1]
        learn = re.search(r'static const u16 ' + ptr + r'\[\] = \{(.*?)\n\};', learns, re.S)[1]
        legal = [(int(lv), m) for lv, m in re.findall(r'LEVEL_UP_MOVE\((\d+), (MOVE_\w+)\)', learn) if int(lv) <= level]
        legal_set = {m for lv, m in legal} | {'MOVE_NONE'}
        return dict(name=names[sp]['nom_yokai'], display_name=names[sp]['nom_affiche_gba'],
                    species=int(names[sp]['species_id']), constant=sp, level=level, iv_byte=iv,
                    actual_iv=iv * 31 // 255, held_item=item, ability_slot=slot,
                    types=re.search(r'\.types = \{([^}]+)\}', body)[1].split(', '),
                    base_stats={k: int(v) for k, v in re.findall(r'\.(base\w+) = (\d+)', body)},
                    base_abilities=re.search(r'\.abilities = \{([^}]+)\}', body)[1].split(', '),
                    exp_yield=int(re.search(r'\.expYield = (\d+)', body)[1]),
                    moves=[dict(constant=m, name=move_names.get(m, m), legal_by_level=m in legal_set) for m in moves],
                    legal_level_moves=[dict(level=lv, constant=m, name=move_names[m]) for lv, m in legal])

    current = {}
    for key in ['LEADER_BROCK', 'LEADER_MISTY', 'LEADER_LT_SURGE', 'LEADER_ERIKA', 'LEADER_KOGA', 'LEADER_SABRINA', 'LEADER_BLAINE', 'LEADER_GIOVANNI']:
        trainer = 'TRAINER_' + key
        body = block(trainers, r'\[' + trainer + r'\] =')
        party = re.search(r'\.party = ITEM_CUSTOM_MOVES\((\w+)\)', body)[1]
        pbody = re.search(r'static const struct TrainerMonItemCustomMoves ' + party + r'\[\] = \{(.*?)\n\};', parties, re.S)[1]
        slots = [int(n) for n in re.search(r'\[' + trainer + r'\] = \{([^}]+)\}', abilities)[1].split(',')]
        mons = []
        for i, row in enumerate(re.findall(r'\{\.iv = .*?\}', pbody)):
            vals = dict(re.findall(r'\.(\w+) = ([^,{}]+)', row))
            moves = re.search(r'\.moves = \{([^}]+)\}', pbody[pbody.index(row):])[1].split(', ')
            mons.append(member(vals['species'], int(vals['lvl']), moves, int(vals['iv']), vals['heldItem'], slots[i]))
        current[trainer] = dict(name=re.search(r'\.trainerName = _\("([^"]+)"\)', body)[1], party_symbol=party,
                                trainer_source_sha256=sha(body.encode()), party_source_sha256=sha(pbody.encode()),
                                items=re.search(r'\.items = \{([^}]*)\}', body)[1], members=mons)

    proposals = {}

    def propose(key, rows):
        team = [member('SPECIES_' + sp, lv, ['MOVE_' + m for m in moves]) for sp, lv, moves in rows]
        assert all(m['legal_by_level'] for mon in team for m in mon['moves']), key
        proposals[key] = team

    propose('azuria', [
        ('MAGNETON', 14, ['QUICK_ATTACK', 'GROWL', 'TAIL_WHIP', 'NONE']),
        ('NIDOQUEEN', 16, ['HEADBUTT', 'BITE', 'LEER', 'FOCUS_ENERGY']),
        ('BULBASAUR', 21, ['EMBER', 'QUICK_ATTACK', 'FURY_SWIPES', 'SMOKESCREEN']),
    ])
    propose('carmin', [
        ('GEODUDE', 18, ['THUNDER_SHOCK', 'THUNDER_WAVE', 'TACKLE', 'GROWL']),
        ('NIDORAN_F', 19, ['SPARK', 'QUICK_ATTACK', 'CHARGE', 'GROWL']),
        ('GRAVELER', 21, ['THUNDER_SHOCK', 'THUNDER_WAVE', 'GROWL', 'NONE']),
        ('VOLTORB', 23, ['METAL_CLAW', 'QUICK_ATTACK', 'SWIFT', 'SHOCK_WAVE']),
    ])
    propose('cramois', [
        ('NIDOKING', 40, ['WEATHER_BALL', 'RAIN_DANCE', 'HEADBUTT', 'SANDSTORM']),
        ('MACHOKE', 41, ['MUDDY_WATER', 'AURORA_BEAM', 'SING', 'RAIN_DANCE']),
        ('CHANSEY', 41, ['FAINT_ATTACK', 'BITE', 'YAWN', 'TORMENT']),
        ('GOLBAT', 42, ['SHADOW_PUNCH', 'NIGHT_SHADE', 'WILL_O_WISP', 'PROTECT']),
        ('RATICATE', 43, ['MUDDY_WATER', 'MUD_SHOT', 'FAKE_OUT', 'AGILITY']),
        ('DRAGONITE', 45, ['DRILL_PECK', 'QUICK_ATTACK', 'SLASH', 'FEATHER_DANCE']),
    ])

    refs = git('for-each-ref', '--format=%(refname)', 'refs/heads', 'refs/remotes/origin').decode().splitlines()
    needle = re.compile(r'wyat|cardamom|kati|nathan|arian|celestin|célestin|beren|bérén|belier|bélier|michael|hailey|inaho|fumi|keita', re.I)
    branches = []
    for ref in refs:
        commit = git('rev-parse', ref).decode().strip()
        paths = git('ls-tree', '-r', '--name-only', ref).decode().splitlines()
        hits = [p for p in paths if needle.search(p) and (p.startswith('graphics/') or p.endswith('.json'))]
        branches.append(dict(ref=ref, commit=commit, candidate_paths=hits))

    resources = []
    for who in ['wyatt', 'katie', 'nathan', 'ariane', 'nathaniel', 'michael']:
        for file in (['normal.png', 'front.png'] if who in ['katie', 'nathan'] else ['overworld.png', 'battle.png']):
            path = f'graphics/yokai_characters/{who}/{file}'
            content = (ROOT / path).read_bytes()
            im = Image.open(io.BytesIO(content))
            resources.append(dict(character=who, path=path, source_commit=BASE, sha256=sha(content),
                                  dimensions=list(im.size), mode=im.mode, colors=len(im.getcolors()), transparency=im.info.get('transparency'),
                                  identical_refs=[r['ref'] for r in branches if path in r['candidate_paths'] and git('show', r['commit'] + ':' + path) == content]))

    # Archive exact candidate bytes only inside docs. No runtime assets are installed.
    for ref, path in [(SCENARIO, 'graphics/yokai_characters/berenice/preview.png'),
                      (SCENARIO, 'graphics/yokai_characters/berenice/overworld.png'),
                      (SCENARIO, 'graphics/yokai_characters/berenice/battle.png'),
                      (SCENARIO, 'graphics/yokai_characters/berenice/overworld.pal'),
                      (SCENARIO, 'graphics/yokai_characters/berenice/normal.pal'),
                      (SCENARIO, 'graphics/yokai_characters/berenice/conversion.json'),
                      ('origin/art/personnages-production', 'graphics/yokai_characters/berenice_belier/battle.png')]:
        content = git('show', ref + ':' + path)
        target = OUT / 'ressources' / path.split('/')[-2] / Path(path).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        item = dict(character='berenice_candidate', path=path, archived_path=str(target.relative_to(ROOT)),
                    source_commit=git('rev-parse', ref).decode().strip(), sha256=sha(content), approval='not_established')
        if path.endswith('.png'):
            im = Image.open(io.BytesIO(content)); item.update(dimensions=list(im.size), mode=im.mode, transparency=im.info.get('transparency'))
        resources.append(item)

    baseline = {}
    for path in git('ls-tree', '-r', '--name-only', BASE).decode().splitlines():
        if path.startswith(('src/', 'include/', 'data/', 'graphics/', 'sound/')):
            baseline[path] = sha((ROOT / path).read_bytes())
    assert git('diff', BASE, '--', 'src', 'include', 'data', 'graphics', 'sound') == b''
    candidate_mons = []
    for sp in names:
        body = block(stats, r'\[' + sp + r'\] =')
        if re.search(r'TYPE_NORMAL|TYPE_ELECTRIC', re.search(r'\.types = \{([^}]+)\}', body)[1]):
            candidate_mons.append(member(sp, 23, []))
    payload = dict(stage='audit_only_awaiting_user_approval', base_commit=BASE, current_teams=current,
                   proposed_teams=proposals, resources=resources, branches=branches,
                   normal_and_electric_candidates=candidate_mons,
                   colossus_proposal=dict(level=31, party_index=3, type='TYPE_GHOST', nickname='Z. COLOSSE',
                       ability='ABILITY_LEVITATE', exp_yield=156,
                       final_stats=dict(hp=140, attack=80, defense=80, speed=25, sp_attack=36, sp_defense=54),
                       moves=['MOVE_POUND', 'MOVE_ROCK_THROW', 'MOVE_LEER', 'MOVE_ASTONISH'],
                       approach='runtime trainer+party-slot descriptor; no global species edits; no wandering-zombie battle flag'),
                   gameplay_unchanged=True)
    (OUT / 'AUDIT.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'PRESERVATION.json').write_text(json.dumps(dict(base=BASE, gameplay_files=baseline), indent=2) + '\n')

    def table(team, full=False):
        result = ['| # | Yo-kai | Niv. | Type réel | Attaques |', '|---|---|---|---|---|']
        for i, mon in enumerate(team, 1):
            types = '/'.join(dict.fromkeys(t.removeprefix('TYPE_') for t in mon['types']))
            moves = ', '.join(m['name'] + (' †' if not m['legal_by_level'] else '') for m in mon['moves'])
            result.append(f"| {i} | {mon['name']} ({mon['species']}) | {mon['level']} | {types} | {moves} |")
        if full:
            result += ['', '| Yo-kai | PV / Atq / Déf / Vit / AtqSp / DéfSp de base | IV réel | Talent | Objet tenu |', '|---|---|---|---|---|']
            for mon in team:
                base = '/'.join(str(mon['base_stats'][key]) for key in ['baseHP', 'baseAttack', 'baseDefense', 'baseSpeed', 'baseSpAttack', 'baseSpDefense'])
                slot = mon['ability_slot'] or 0
                result.append(f"| {mon['name']} | {base} | {mon['actual_iv']} | {mon['base_abilities'][slot]} | {mon['held_item']} |")
        return '\n'.join(result)

    lines = ['# Équipes réellement actives et propositions', '',
             'Lecture de `gTrainers` → véritable tableau de partie → types/statistiques globaux → pointeur actif d’apprentissage. Les anciens JSON seuls ne font pas autorité : celui d’Érika décrit encore son équipe Plante, déjà remplacée dans Lavanville.', '',
             '† Attaque actuellement imposée par une ancienne équipe, absente de son apprentissage par niveau à ce niveau. Ce constat ne prouve pas une illégalité par CT/tuteur ; ces anciennes équipes ne sont pas corrigées dans cet audit. Toutes les propositions ci-dessous sont vérifiées par apprentissage de niveau.', '']
    for trainer, data in current.items():
        lines += ['## ' + data['name'] + ' — ' + trainer, '', 'Table : `' + data['party_symbol'] + '`. Objets du Dresseur : `' + (data['items'] or 'aucun') + '`.', '', table(data['members'], True), '']
    for name, team in proposals.items():
        lines += ['## Proposition — ' + name, '', table(team, True), '']
    lines += ['Les propositions emploient des IV bruts 200, soit 24 réels, comme les équipes remplacées, et le premier talent existant de chaque espèce (slot 0, indiqué ci-dessus). Aucun objet tenu, aucun changement des données globales, aucun talent supplémentaire.', '',
              'Les attaques, types, talents disponibles, statistiques, identifiants et apprentissages complets au niveau retenu figurent aussi dans [AUDIT.json](AUDIT.json).', '']
    (OUT / 'EQUIPES.md').write_text('\n'.join(lines))
    print('PASS:', len(branches), 'refs,', len(resources), 'resource records,', len(baseline), 'unchanged gameplay sources/assets; all proposed moves legal by level.')
    for key, team in proposals.items():
        print(key, ', '.join(f"{mon['name']} {mon['level']}" for mon in team))


if __name__ == '__main__':
    run()

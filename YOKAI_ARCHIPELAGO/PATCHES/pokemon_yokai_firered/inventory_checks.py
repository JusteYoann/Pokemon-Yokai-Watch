#!/usr/bin/env python3
"""Inventaire depuis les vraies sources ; un candidat n'est jamais activé implicitement."""
from __future__ import annotations
import argparse
import ast
import json
import re
from pathlib import Path

LOCATION_BASE = 0x594B2000  # + native flag, never array ordinal
ACTIVE_FLAGS = {
    'FLAG_HIDE_VIRIDIAN_FOREST_POKE_BALL': 'Forêt de Jade — Poké Ball',
    'FLAG_HIDE_VIRIDIAN_FOREST_ANTIDOTE': 'Forêt de Jade — Antidote',
    'FLAG_HIDE_VIRIDIAN_FOREST_POTION': 'Forêt de Jade — Potion ouest',
    'FLAG_HIDE_VIRIDIAN_FOREST_POTION_2': 'Forêt de Jade — Potion est',
    'FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION': 'Forêt de Jade — Potion cachée',
    'FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE': 'Forêt de Jade — Antidote caché',
}

def constants(path):
    texts=[path.read_text()]
    if path.name=='flags.h':texts.insert(0,path.with_name('opponents.h').read_text())
    expressions = dict(re.findall(r'^#define\s+(\w+)\s+([^\n/]+)', '\n'.join(texts), re.M))
    found = {}
    def evaluate(name):
        if name in found: return found[name]
        def visit(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, int): return node.value
            if isinstance(node, ast.Name): return evaluate(node.id)
            if isinstance(node, ast.BinOp):
                a, b = visit(node.left), visit(node.right)
                if isinstance(node.op, ast.Add): return a + b
                if isinstance(node.op, ast.Sub): return a - b
                if isinstance(node.op, ast.BitOr): return a | b
                if isinstance(node.op, ast.LShift): return a << b
            raise ValueError(name)
        found[name] = visit(ast.parse(expressions[name].strip(), mode='eval').body)
        return found[name]
    for name in expressions:
        try: evaluate(name)
        except (KeyError, ValueError, SyntaxError, RecursionError): pass
    return found

def inventory(source):
    flags = constants(source / 'include/constants/flags.h')
    scripts = {}
    for p in sorted((source / 'data').rglob('*.inc')):
        label = None
        for line, text in enumerate(p.read_text(errors='replace').splitlines(), 1):
            m = re.match(r'^(\w+)::?', text)
            if m: label = m[1]
            m = re.match(r'\s*finditem\s+(ITEM_\w+)(?:,\s*(\d+))?', text)
            if m and label:
                scripts[label] = (m[1], int(m[2] or 1), f'{p.relative_to(source)}:{line}')
    checks = []
    for p in sorted((source / 'data/maps').glob('*/map.json')):
        data = json.loads(p.read_text()); map_name = data['name']
        # Region names are evidence for exclusions, never proof of accessibility.
        postgame = map_name.startswith(('OneIsland','TwoIsland','ThreeIsland','FourIsland',
            'FiveIsland','SixIsland','SevenIsland','NavelRock','BirthIsland','CeruleanCave',
            'Limbes','BattleTower'))
        for kind, events in [('ball', data.get('object_events', [])), ('hidden', data.get('bg_events', []))]:
            for index, event in enumerate(events):
                if kind == 'ball':
                    if event.get('script') not in scripts: continue
                    item, quantity, script_source = scripts[event['script']]
                    flag = event.get('flag', '0')
                else:
                    if 'item' not in event or 'flag' not in event: continue
                    flag = event['flag']; item = event['item']; quantity = event.get('quantity', 1)
                    script_source = 'data/scripts/obtain_item.inc:EventScript_HiddenItemScript'
                value = flags.get(flag)
                active = flag in ACTIVE_FLAGS
                checks.append({
                    'id': LOCATION_BASE + value if value is not None else None,
                    'name_fr': ACTIVE_FLAGS.get(flag, f'{map_name} — {item} ({kind}, {index + 1})'),
                    'map': map_name, 'x': event['x'], 'y': event['y'], 'kind': kind,
                    'flag': flag, 'flag_value': value, 'original_item': item, 'quantity': quantity,
                    'source': f'{p.relative_to(source)}:{kind}[{index}]', 'script_source': script_source,
                    'script': event.get('script'),
                    'validation': f'FlagGet({flag})', 'mandatory': False,
                    'prerequisites': ['Accès à la Forêt de Jade, aucun badge/CS'] if active else ['À tracer dans le fangame ; non validé'],
                    'status': 'active' if active else 'excluded_postgame' if postgame else 'candidate_review_required',
                    'original_reward': 'replaced' if active else 'unchanged',
                    'risks': [] if active else ['Accès réel, flag réutilisé/renouvelable, scénario et récompense à examiner'],
                })
    # NPC gifts are an explicit audit queue, not fabricated check IDs.
    gifts = []
    for p in sorted((source / 'data').rglob('*.inc')):
        label = None
        for line, text in enumerate(p.read_text(errors='replace').splitlines(), 1):
            m = re.match(r'^(\w+)::?', text)
            if m: label = m[1]
            m = re.match(r'\s*(?:giveitem\s+|(?:giveitem_msg|msgreceiveditem)\s+\w+,\s*)(ITEM_\w+)', text)
            if m: gifts.append({'item': m[1], 'label': label, 'source': f'{p.relative_to(source)}:{line}',
                'status': 'review_required', 'id': None,
                'risks': ['Tracer flag anti-répétition, cinématique, prérequis et éventuel appel C alternatif']})
    active = [c for c in checks if c['status'] == 'active']
    if {c['flag'] for c in active} != set(ACTIVE_FLAGS): raise ValueError('Les six sources attendues ne sont pas présentes')
    if len({c['id'] for c in active}) != len(active): raise ValueError('Collision des checks actifs')
    # Individually traced gift: collection flag is separate from possession.
    surf_source=source/'data/maps/SafariZone_SecretHouse/scripts.inc'
    if 'giveitem_msg SafariZone_SecretHouse_Text_ReceivedHM03FromAttendant, ITEM_HM03' not in surf_source.read_text():
        raise ValueError('Source de Surf différente de RC1')
    value=flags['FLAG_GOT_HM03']
    checks.append({'id':LOCATION_BASE+value,'name_fr':'Parc Safari — récompense de la Maison Secrète',
        'map':'SafariZone_SecretHouse','kind':'gift','flag':'FLAG_GOT_HM03','flag_value':value,
        'original_item':'ITEM_HM03','quantity':1,'source':'data/maps/SafariZone_SecretHouse/scripts.inc:SafariZone_SecretHouse_EventScript_Attendant',
        'script_source':'data/maps/SafariZone_SecretHouse/scripts.inc:11','script':'SafariZone_SecretHouse_EventScript_Attendant',
        'validation':'FlagGet(FLAG_GOT_HM03)','mandatory':False,
        'prerequisites':['Accès à Parmanie et au Parc Safari ; pas de Surf requis pour cette maison'],
        'status':'active','original_reward':'replaced','risks':['Grille logique Kanto simplifiée ; chemin natif jusqu’à Parmanie conservé']})
    badges=[]
    gyms=[('PewterCity_Gym','Wyatt'),('CeruleanCity_Gym','Nathan/Katie'),('VermilionCity_Gym','Ariane'),
          ('PokemonTower_7F','Alizon Bie'),('FuchsiaCity_Gym','Bérénice'),('SaffronCity_Gym','Domniscian'),
          ('CinnabarIsland_Gym','Nathaniel/Michael'),('ViridianCity_Gym','Steve Jaws')]
    for index,(map_name,boss) in enumerate(gyms):
        path=source/f'data/maps/{map_name}/scripts.inc';flag=f'FLAG_BADGE{index+1:02d}_GET'
        lines=path.read_text().splitlines();line=next(i for i,s in enumerate(lines,1) if re.search(r'\bsetflag\s+'+flag+r'\b',s))
        badges.append({'id':0x594B1000+index,'name_fr':'Badge '+('d’' if boss[0] in 'AEIOU' else 'de ')+boss,
            'map':map_name,'validation':f'FlagGet({flag})','flag':flag,'source':f'{path.relative_to(source)}:{line}',
            'mandatory':True,'prerequisites':['Progression native jusqu’à cette arène, combat gagné']+(['CS03 Surf reçue'] if index>=6 else []),
            'original_reward':'badge_native_preserved_separate_AP_reward','risks':['Un seul combat (Wyatt) joué dans les tests actuels']})
    return {'schema': 1, 'base_source_commit': 'a589cf0057fd0f579d003d8dd58616b3f4649ea2',
            'id_formula': '0x594B2000 + native_flag_value', 'checks': checks, 'badge_checks':badges,'npc_gifts_review_queue': gifts,
            'limits': ['Inventaire des macros finditem/événements cachés et giveitem uniquement ; les dons C et scripts indirects exigent un audit séparé.',
                       'Les candidats ne sont pas des checks jouables. Hors forêt, les prérequis restent à vérifier.',
                       'Îles 1–3 exclues prudemment de ce premier périmètre malgré certains accès possibles avant la Ligue.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();result=inventory(a.source);a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"{len(result['checks'])} sources inventoriées, {sum(c['status']=='active' for c in result['checks'])} actives, {len(result['npc_gifts_review_queue'])} dons recensés")

if __name__ == '__main__': main()

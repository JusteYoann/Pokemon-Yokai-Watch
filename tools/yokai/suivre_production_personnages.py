#!/usr/bin/env python3
"""Trace every map actor and trainer portrait without inferring story identities."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/atelier-personnages/production'


def csv_file(path, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True, parents=True)
    uses = []
    for path in sorted((ROOT/'data/maps').glob('*/map.json')):
        info = json.loads(path.read_text())
        for index, event in enumerate(info.get('object_events', []), 1):
            uses.append(dict(map=path.parent.name, local_id=event.get('local_id', index),
                             graphics_id=event.get('graphics_id', ''),
                             movement=event.get('movement_type', ''),
                             x=event.get('x', ''), y=event.get('y', ''),
                             script=event.get('script', ''), flag=event.get('flag', ''),
                             source=str(path.relative_to(ROOT))))
    csv_file(OUT/'TOUS_LES_ACTEURS_CARTES.csv', uses)
    grouped = Counter(row['graphics_id'] for row in uses)
    csv_file(OUT/'IDENTIFIANTS_GRAPHIQUES_CARTES.csv', [dict(graphics_id=k, map_uses=v,
             dynamic=str(str(k).startswith('OBJ_EVENT_GFX_VAR_')),
             identity_policy='Identite a lire dans le script ; ne pas deduire du seul sprite')
             for k, v in sorted(grouped.items(), key=lambda x: str(x[0]))])
    trainers = []
    text = (ROOT/'src/data/trainers.h').read_text()
    for match in re.finditer(r'^    \[(\w+)\] = \{(.*?)^    \},', text, re.M | re.S):
        body = match[2]
        def field(name):
            value = re.search(r'\.'+name+r'\s*=\s*([^\n]+)', body)
            return value[1].rstrip(',').strip() if value else ''
        trainers.append(dict(trainer_id=match[1], name_expression=field('trainerName'),
                             portrait_id=field('trainerPic'), trainer_class=field('trainerClass')))
    csv_file(OUT/'TOUS_LES_DRESSEURS.csv', trainers)
    # Scripted actor spawns/graphic changes need separate review from map templates.
    script_refs = []
    for path in sorted((ROOT/'data').rglob('*.inc')):
        for line_no, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
            if re.search(r'\b(?:addobject|setobjectgraphics)\b|\bsetvar\s+VAR_OBJ_GFX_ID_', line):
                script_refs.append(dict(source=str(path.relative_to(ROOT)), line=line_no,
                                        instruction=line.strip()))
    if script_refs:
        csv_file(OUT/'ACTEURS_DYNAMIQUES_SCRIPTS.csv', script_refs)
    summary = dict(map_actor_templates=len(uses), graphics_ids_in_maps=len(grouped),
                   trainer_entries=len(trainers), scripted_actor_references=len(script_refs),
                   method='All data/maps/*/map.json object_events; all trainer entries; scripted spawn/graphics references',
                   limitations=['Map templates include creatures and objects, not only people',
                                'One generic graphic can represent many named NPCs',
                                'No identity or new gym assignment inferred automatically'])
    (OUT/'COUVERTURE.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()

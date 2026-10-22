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
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
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
    catalog = OUT.parent/'PERSONNAGES_ET_BESOINS.csv'
    if catalog.exists():
        tested_path = ROOT/'QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/MARCHE/TEST_MGBA.json'
        tested = {t['actor'] for t in json.loads(tested_path.read_text()).get('tests', []) if t.get('passed')} if tested_path.exists() else set()
        classic = {'ariane', 'wyatt', 'nathaniel', 'michael', 'enma', 'domniscian', 'don_morleone', 'mafiamille_1', 'mafiamille_2', 'mafiamille_3', 'employe_rouge', 'employe_bleu'}
        progress = []
        for row in csv.DictReader(catalog.open(encoding='utf-8')):
            actor = row['id']
            produced = ROOT/f'graphics/yokai_characters/{actor}/walk-production.json'
            if actor in tested:
                state = 'LOT_MARCHE_INTEGRE_ET_TESTE_MGBA'
                remaining = 'Autres variantes/actions seulement si necessaires ; validation artistique globale non deduite des tests'
            elif actor in ('nathan', 'katie'):
                state = 'RESSOURCES_EXISTANTES_PRESERVEES_ET_ANIMATIONS_TESTEES_AVANT_LOT'
                remaining = 'Relire les autres representations ; ne pas remplacer les series valides'
            elif actor == 'dr_jobard':
                state = 'EN_PAUSE_DECISION_CREATEUR'
                remaining = 'Revenir sur la ressemblance plus tard'
            elif row['fichiers_presents']:
                state = 'FICHIERS_PRESENTS_A_VERIFIER_SELON_USAGE'
                remaining = 'Verifier les ressources et leur activation ; ne pas deduire termine de leur presence'
            else:
                state = 'RESSOURCES_DEDIEES_A_PRODUIRE_OU_REUTILISATION_A_IDENTIFIER'
                remaining = 'Retrouver reference et usage ; ne pas inventer une identite'
            if actor == 'wyatt':
                remaining = 'Marche supplementaire refusee par controle de grille ; dessin actif et portrait conserves'
            if actor == 'coach_antonic':
                remaining = 'Proposition refusee, non integree ; retouche native necessaire, pas de nouvel evenement'
            if actor == 'enma':
                remaining = 'Ancien design conserve ; proposition de pas non conforme, non integree'
            if actor == 'domniscian':
                remaining = 'Ancien design fixe a son appareil conserve ; ne pas inventer des pieds pour ce dessin'
            reference = 'Protagoniste.rar (fourni par createur)' if actor in ('nathan', 'katie', 'matt') else 'Reference_CAMEOS_YOKAI_WATCH.rar (fourni par createur)' if actor in classic else 'Images de conversation du createur' if actor == 'dr_jobard' else 'Reference dediee a retrouver ou ressource existante a confirmer'
            if actor in ('lady_perpetua', 'mckraken'):
                reference = 'Reference en pied fournie par le createur dans la conversation'
                state = 'PROPOSITIONS_NON_INTEGREES_GRILLE_NON_CONFORME'
                remaining = 'Deux essais archives sous propositions/perpetua-mckraken ; dessin natif et portraits a produire, integration et tests non effectues'
            if actor in ('laure', 'marge', 'agent_x'):
                reference = 'Reference fournie par le createur dans la conversation'
                state = 'BROUILLON_FACE_NON_INTEGRE_GRILLE_NON_CONFORME'
                remaining = 'Propositions sous propositions/laure-marge-agent-x ; reprise dans un editeur natif necessaire, orientations et marche a produire, aucun test moteur'
            progress.append(dict(personnage=row['nom'], id=actor, ressources_necessaires=row['ressources_attendues'],
                                 ressources_existantes=row['fichiers_presents'], ressources_manquantes=row['fichiers_a_retrouver_ou_creer'],
                                 reference_visuelle=reference, etat=state, nouvelles_images_de_pas=6 if produced.exists() else 0,
                                 portrait_personnel='Existant et entree en combat testee' if actor in tested else 'A verifier selon role',
                                 reste=remaining))
        csv_file(OUT/'ETAT_PAR_PERSONNAGE.csv', progress)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()

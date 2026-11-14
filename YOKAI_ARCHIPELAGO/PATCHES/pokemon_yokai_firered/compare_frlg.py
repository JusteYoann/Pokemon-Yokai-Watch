#!/usr/bin/env python3
"""Compare MIT FRLG metadata to real RC1 sources; never applies its binary patch."""
import argparse
from collections import Counter,defaultdict
import json
from pathlib import Path
import re
from inventory_checks import inventory,constants

COMMIT='3d1359cf0606cee11eebfecc0d820063bef7c2a2'

def compare(upstream,source):
    root=upstream/'worlds/pokemon_frlg/data'
    locations=json.loads((root/'locations.json').read_text())
    extracted=json.loads((root/'extracted_data.json').read_text())['locations']
    regions={}
    for p in sorted((root/'regions').glob('*.json')):regions.update(json.loads(p.read_text()))
    parents={loc:(key,region) for key,region in regions.items() for loc in region.get('locations',[])}
    inv=inventory(source);native={c['flag']:c for c in inv['checks']};flags=constants(source/'include/constants/flags.h')
    refs=defaultdict(list)
    for path in list((source/'data').rglob('*.inc'))+list((source/'src').glob('*.c')):
        for line,text in enumerate(path.read_text(errors='replace').splitlines(),1):
            for flag in re.findall(r'(?:\bsetflag\s+|\bFlagSet\(\s*)(FLAG_\w+)',text):
                refs[flag].append(f'{path.relative_to(source)}:{line}')
    rows=[]
    for key,data in locations.items():
        category=data['category'];region_key,region=parents.get(key,('',{}));flag=None
        if key.startswith('HIDDEN_ITEM_'):flag='FLAG_'+key
        elif key.startswith('ITEM_'):flag='FLAG_HIDE_'+key[5:]
        elif key.startswith('NPC_GIFT_'):flag='FLAG_'+key[9:]
        badge=re.fullmatch(r'BADGE_([1-8])',key)
        candidate=native.get(flag)
        if badge:
            candidate=inv['badge_checks'][int(badge[1])-1];flag=candidate['flag']
        kanto='Kanto' in data.get('tags',[])
        status='not_imported_category';reason='Catégorie optionnelle du port ; aucune activation automatique.'
        if not kanto and category in ('OVERWORLD_ITEM','HIDDEN_ITEM','NPC_GIFT'):
            status='disabled_postgame_or_sevii';reason='Hors périmètre pré-Ligue conservateur ; accès réel à examiner.'
        elif candidate:
            status='retained_candidate';reason='Source présente ; règles et détection à valider avant activation.'
            if candidate.get('status')=='excluded_postgame':status='disabled_postgame_or_sevii'
            if candidate.get('status')=='active' or badge:status='retained_active'
            if badge and badge[1]=='4':status='modified';reason='Badge déplacé au sommet de la Tour de Lavanville.'
        elif flag and refs.get(flag):
            status='modified_or_gift_review';reason='Flag de remise présent ; cinématique et conditions à comparer.'
        elif category in ('OVERWORLD_ITEM','HIDDEN_ITEM','NPC_GIFT'):
            status='absent_or_unresolved';reason='Pas de source de remise correspondante identifiée ; désactivé.'
        if key=='NPC_GIFT_GOT_HM01':status='modified';reason='Coupe dans la quête Philosovni, plus à sa remise vanilla.'
        if key=='NPC_GIFT_GOT_POKE_FLUTE':status='modified';reason='Flûte déplacée au repaire Mafiamille ; restauration si absente.'
        if key=='ITEM_SILPH_SCOPE':status='modified';reason='Le script nommé SilphScope remet maintenant la Poké Flûte.'
        rows.append({'upstream_key':key,'upstream_ap_id':extracted.get(key,{}).get('flag'),
            'name_original':data['name'],'category':category,'tags':data.get('tags',[]),
            'upstream_region':region_key,'upstream_map':region.get('parent_map'),
            'native_flag':flag,'native_sources':([candidate.get('script_source',candidate['source'])] if candidate else refs.get(flag,[])),
            'native_map':candidate.get('map') if candidate else None,
            'yokai_id':candidate.get('id') if candidate else (0x594B2000+flags[flag] if flag in flags else None),
            'status':status,'reason':reason})
    additions=[{'name':'Bingo-kai — accueil du steward','source':'src/bingo_kai.c:BingoWelcomeGift',
        'condition':'VAR_BINGO_GIFTS == 3','decision':'deterministic_candidate','reason':'Pièces d’accueil garanties, résultat du tirage indépendant.'},
        {'name':'Jibanyan — amitié','source':'data/scripts/bingo_kai.inc:JibanyanQuest','condition':'VAR_JIBANYAN_FRIEND == 3',
         'decision':'deterministic_candidate','reason':'Quête et cadeau natifs à conserver ; check séparé.'},
        {'name':'Terr’heure — première apparition','source':'src/terre_heure.c','condition':'FLAG_ONI_FIRST_SEEN',
         'decision':'optional_filler_only','reason':'Déclenchement aléatoire : aucun objet indispensable autorisé.'},
        {'name':'Terr’heure — enquête Alyzon / Gorgouille','source':'data/maps/PokemonTower_7F/scripts.inc:25',
         'condition':'FLAG_SYS_GAME_CLEAR','decision':'disabled_postgame','reason':'Le seul appel à la quête est après le Panthéon ; pas un check pré-Ligue.'}]
    return {'upstream_repository':'https://github.com/vyneras/Archipelago','upstream_commit':COMMIT,
        'license':'MIT; notice fournie dans THIRD_PARTY/FRLG_LICENSE.txt',
        'limits':['Port communautaire maintenu et étudié dans le code ; fonctionnement natif du port vanilla non testé ici.',
                  'Réutilisation des clés symboliques, catégories, régions et identifiants de référence ; aucun offset ou patch vanilla appliqué.',
                  'Les quinze IDs Yo-kai existants sont conservés. La présence d’un flag ne prouve pas un accès pré-Ligue.'],
        'summary':dict(Counter(c['status'] for c in rows)),'rows':rows,'fangame_additions':additions}

def markdown(report):
    lines=['# Comparaison Rouge Feu Archipelago → fangame Yo-kai','',
        f"Référence : Vyneras `frlg-stable`, `{COMMIT}`, licence MIT. Aucun patch binaire vanilla importé.",'',
        '| Catégorie de comparaison | Nombre |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in report['summary'].items()]
    lines += ['', 'Les candidats restent désactivés jusqu’à l’audit. Les IDs historiques Yo-kai sont inchangés ; l’ID upstream est conservé dans la correspondance.', '',
        '| Check original | Clé originale / ID | Décision | Source et adaptation |','|---|---|---|---|']
    for r in report['rows']:
        if r['category'] not in ('OVERWORLD_ITEM','HIDDEN_ITEM','NPC_GIFT'):continue
        source=', '.join(r['native_sources'][:2]) or 'non identifiée'
        lines.append(f"| {r['name_original']} | `{r['upstream_key']}` / {r['upstream_ap_id']} | {r['status']} | `{source}` ; {r['reason']} |")
    lines+=['','## Ajouts propres au fangame','','| Événement | Décision | Justification |','|---|---|---|']
    lines += [f"| {r['name']} | {r['decision']} | {r['reason']} |" for r in report['fangame_additions']]
    return '\n'.join(lines)+'\n'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('upstream','source','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();report=compare(a.upstream,a.source);a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'FRLG_COMPARAISON.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (a.out/'FRLG_COMPARAISON.md').write_text(markdown(report));print(json.dumps(report['summary']))

if __name__=='__main__':main()

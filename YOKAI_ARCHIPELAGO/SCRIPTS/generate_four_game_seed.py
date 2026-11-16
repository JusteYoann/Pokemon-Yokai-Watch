#!/usr/bin/env python3
"""Generate and audit the actual four-game seed; refuse missing/placeholder worlds."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest  # official AP_TEST_WORLDS selection
import zipfile

PROJECT=Path(__file__).resolve().parents[1]
WORLDS={'pokemon_yokai_firered':'Pokemon Yo-kai FireRed',
        'pokemon_yokai_emerald':'Pokemon Yo-kai Emerald',
        'yokaiwatch2':'Yo-kai Watch 2','mkwii':'Mario Kart Wii'}

def preflight(ap,players):
    import yaml
    settings=[yaml.safe_load(p.read_text()) for p in sorted(players.iterdir()) if p.is_file()]
    if len(settings)!=4 or {s.get('game') for s in settings}!=set(WORLDS.values()):
        raise ValueError('Le dossier joueurs doit contenir uniquement les quatre YAML FR/Emerald/YW2/MKW, un par jeu.')
    if len({s['name'] for s in settings})!=4:raise ValueError('Noms de slots non uniques.')
    missing=[];packages={}
    for package,game in WORLDS.items():
        path=ap/'custom_worlds'/f'{package}.apworld'
        if not path.is_file():missing.append(str(path));continue
        with zipfile.ZipFile(path) as z:
            md=json.loads(z.read(f'{package}/archipelago.json'))
            if md['game']!=game:raise ValueError(f'Mauvais monde dans {path.name}')
            if package=='pokemon_yokai_emerald':
                if md.get('world_version')!='0.2.1':
                    raise ValueError('Emerald : fournir la version française0.2.1 validée par le joueur.')
                constants=z.read(f'{package}/constants.py').decode('utf-8')
                if 'pokemon emerald / yokai ap fr2' not in constants:
                    raise ValueError('Emerald : signature fr2 absente ; ne pas remplacer par une ancienne build.')
            if package=='pokemon_yokai_firered':
                profile=json.loads(z.read(f'{package}/build.json'))
                catalog=json.loads((PROJECT/'APWORLDS/pokemon_yokai_firered/checks.json').read_text())
                if profile['catalog_sha256']!=catalog['catalog_sha256']:raise ValueError('Recompiler le package FR avec le catalogue actuel.')
        packages[package]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'metadata':md}
    if missing:raise FileNotFoundError('APWorlds validés manquants : '+', '.join(missing)+'. Fournir le package réellement utilisé ; aucun substitut vanilla ne sera installé.')
    return packages

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archipelago',type=Path,required=True)
    p.add_argument('--players',type=Path,default=PROJECT/'CONFIG/createurs/quatre_jeux')
    p.add_argument('--out',type=Path,required=True);p.add_argument('--seed',type=int,default=1611202604)
    a=p.parse_args();ap=a.archipelago.resolve();players=a.players.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    report={'passed':False,'kind':'official_four_world_generation_and_logic','seed':a.seed,
            'four_native_games_tested':False,'games':list(WORLDS.values())}
    try:
        report['packages']=preflight(ap,players)
        os.environ.update(SKIP_REQUIREMENTS_UPDATE='1',AP_TEST_WORLDS=','.join(WORLDS))
        os.chdir(ap);sys.path.insert(0,str(ap))
        import Generate
        from Main import main as generate
        sys.argv=['Generate.py','--player_files_path',str(players),'--outputpath',str(out),
                  '--seed',str(a.seed),'--spoiler','3']
        args,actual_seed=Generate.main();mw=generate(args,actual_seed)
        assert len(mw.worlds)==4 and {w.game for w in mw.worlds.values()}==set(WORLDS.values())
        assert mw.can_beat_game(),'Seed impossible selon la logique des quatre APWorlds'
        routes=Counter();spheres=[];incoming=set();outgoing=set()
        for sphere in mw.get_spheres():
            assert sphere,'Checks inaccessibles selon la logique courante'
            counts=Counter(l.player for l in sphere if l.address is not None)
            spheres.append({mw.player_name[i]:counts[i] for i in mw.player_ids})
            for loc in sphere:
                if loc.item and loc.item.advancement and loc.player!=loc.item.player:
                    routes[f'{mw.player_name[loc.player]} -> {mw.player_name[loc.item.player]}']+=1
                    outgoing.add(loc.player);incoming.add(loc.item.player)
        assert incoming==outgoing==set(mw.player_ids),'Chaque slot doit participer aux échanges de progression'
        from BaseClasses import CollectionState
        fr=next(w for w in mw.worlds.values() if w.game=='Pokemon Yo-kai FireRed')
        goal=mw.get_location('Panthéon',fr.player)
        keys=('CS01 Coupe','CS03 Surf','CS04 Force','CS05 Flash')
        for missing in keys:
            state=CollectionState(mw)
            for key in keys:
                if key!=missing:state.collect(fr.create_item(key),True)
            assert not goal.can_reach(state),f'Panthéon accessible sans {missing}'
        report.update(passed=True,beatable_by_logic=True,server_seed_name=mw.seed_name,
            slots=[{'name':mw.player_name[i],'slot':i,'game':mw.worlds[i].game,
                    'checks':sum(l.address is not None for l in mw.get_locations(i))} for i in mw.player_ids],
            spheres=spheres,remote_progression_routes=dict(routes))
        report['output_files']=[{'name':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in out.glob('*.zip')]
    except Exception as e:
        report['error']=str(e);print(str(e),file=sys.stderr)
    (out/'RESULTAT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())

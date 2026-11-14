#!/usr/bin/env python3
"""Génère vraiment plusieurs seeds et relève les sphères (pas des durées)."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import runpy
import sys
import unittest  # enables official AP_TEST_WORLDS scoping

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('archipelago','players','out'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--seeds',nargs='+',type=int,default=[14112029,14112030,14112031])
    a=p.parse_args();ap=a.archipelago.resolve();players=a.players.resolve();out=a.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    os.environ.update(SKIP_REQUIREMENTS_UPDATE='1',AP_TEST_WORLDS='yokaiwatch2,mkwii,pokemon_yokai_firered')
    os.chdir(ap);sys.path.insert(0,str(ap))
    report={'kind':'actual_AP_generate_and_spheres','tested_games':3,'native_gameplay_tested':False,
            'caution':['FireRed randomise Surf ; les autres objets de progression restent natifs.',
                       'Ce modèle ne mesure pas les checks immédiatement accessibles au personnage : les étapes natives pré-Surf restent regroupées ; six objets ordinaires précoces sont activés.',
                       'Aucune équivalence sphère/minutes et aucune garantie sur cinq jeux.'], 'seeds':[]}
    for seed in a.seeds:
        sys.argv=['Generate.py','--player_files_path',str(players),'--outputpath',str(out/str(seed)),
                  '--seed',str(seed),'--spoiler','3']
        import Generate
        from Main import main as generate_world
        args,actual_seed=Generate.main()
        mw=generate_world(args,actual_seed)
        assert mw.can_beat_game(), 'Seed impossible selon la logique courante'
        assert len(mw.worlds)==3, 'Ne pas annoncer cinq mondes'
        spheres=[];crossworld=Counter();last={p:0 for p in mw.player_ids};gaps={p:0 for p in mw.player_ids}
        forest_progression=0
        for number,sphere in enumerate(mw.get_spheres(),1):
            assert sphere, 'Emplacements inaccessibles'
            counts=Counter(l.player for l in sphere if l.address is not None)
            for player in mw.player_ids:
                if counts[player]:gaps[player]=max(gaps[player],number-last[player]-1);last[player]=number
            spheres.append({mw.player_name[p]:counts[p] for p in mw.player_ids})
            for loc in sphere:
                if loc.item and loc.item.advancement and loc.item.player!=loc.player:
                    crossworld[f'{mw.player_name[loc.player]} -> {mw.player_name[loc.item.player]}']+=1
                    if loc.name.startswith('Forêt de Jade'):forest_progression+=1
        world=mw.worlds[next(p for p,w in mw.worlds.items() if w.game=='Pokemon Yo-kai FireRed')]
        assert len(world.location_name_to_id)==15
        assert all('Forêt de Jade' in name or name.startswith(('Badge','Parc Safari')) for name in world.location_name_to_id)
        from BaseClasses import CollectionState
        state=CollectionState(mw)
        assert not mw.get_location('Panthéon',world.player).can_reach(state)
        state.collect(world.create_item('CS03 Surf'),True)
        assert mw.get_location('Panthéon',world.player).can_reach(state)
        report['seeds'].append({'seed':seed,'beatable_by_logic':True,'spheres':spheres,
            'max_internal_gap_spheres':{mw.player_name[p]:gaps[p] for p in mw.player_ids},
            'remote_progression_routes':dict(crossworld),'forest_remote_progression_count':forest_progression})
    (out/'RESULTAT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(out/'RESULTAT.json')

if __name__=='__main__':main()

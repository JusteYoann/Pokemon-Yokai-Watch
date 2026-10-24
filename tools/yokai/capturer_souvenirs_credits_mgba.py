#!/usr/bin/env python3
"""Real current-ROM screenshots for credits; isolated map/progression fixtures.

No illustrated/reconstructed screenshots. These shots establish native visuals,
not an uninterrupted adventure or proof that the entire story was played.
"""
import hashlib
import json
import os
import re
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS, C, warp, strong_party

gender = int(os.environ.get('YOKAI_QA_GENDER', '0'))
label = ['garcon', 'fille'][gender]
out = ROOT / 'docs/ecran-titre-credits-20261024/souvenirs' / label
out.mkdir(parents=True, exist_ok=True)
cases = [
    (1, 'PalletTown_ProfessorOaksLab', 9, 6),
    (2, 'PalletTown', 6, 8),
    (3, 'ViridianForest', 12, 12),
    (4, 'PewterCity_Gym', 6, 6),
    (5, 'MtMoon_B2F', 13, 9),
    (6, 'Route25_SeaCottage', 7, 6),
    (7, 'SSAnne_Deck', 10, 7),
    (8, 'VermilionCity', 33, 30),
    (9, 'CeladonCity_GameCorner', 8, 8),
    (10, 'CeladonCity_Condominiums_RoofRoom', 7, 4),
    (11, 'PokemonTower_3F', 10, 10),
    (12, 'SilphCo_7F', 2, 7),
    (13, 'SaffronCity_Dojo', 6, 6),
    (14, 'SilphCo_3F', 8, 8),
    (17, 'CeruleanCity_Gym', 8, 7),
    (18, 'SafariZone_Center', 20, 20),
    (19, 'Route20', 20, 9),
    (20, 'PowerPlant', 5, 12),
    (21, 'SeafoamIslands_B4F', 9, 3),
    (22, 'Route20', 10, 9),
    (23, 'CinnabarIsland', 12, 11),
    (24, 'PokemonMansion_1F', 5, 24),
    (25, 'CinnabarIsland_Gym', 5, 5),
    (26, 'Route22', 24, 5),
    (27, 'VictoryRoad_3F', 29, 10),
    (28, 'PokemonLeague_LoreleisRoom', 5, 7),
    (29, 'PokemonLeague_LancesRoom', 5, 7),
    (31, 'PalletTown', 6, 7),
]
r = new_game(gender)
base = r.snapshot()
results = []
try:
    for n, name, x, y in cases:
        r.restore(base)
        strong_party(r)
        r.call('FlagSet', 0x827)
        # Explicit staging, not permanent progression in a user's save.
        r.call('VarSet', 0x40F4, 3 if n >= 19 else 0)
        map_data = json.loads((ROOT / f'data/maps/{name}/map.json').read_text())
        for actor in map_data.get('object_events', []):
            flag = actor.get('flag')
            if flag in C:
                r.call('FlagClear', C[flag])
        if n == 6:
            r.call('FlagSet', C['FLAG_HIDE_BILL_CLEFAIRY'])
            r.call('FlagClear', C['FLAG_HIDE_BILL_HUMAN_SEA_COTTAGE'])
        if n in [13, 17, 27]:
            script = (ROOT / f'data/maps/{name}/scripts.inc').read_text()
            for trainer in set(re.findall(r'\bTRAINER_[A-Z0-9_]+\b', script)):
                if trainer in C:
                    r.call('SetTrainerFlag', C[trainer])
        warp(r, *MAPS[name], x, y)
        if n == 18:
            noko = next(int(row['species_id']) for row in json.loads((ROOT / 'data/yokai/noms_affiches.json').read_text()) if row['nom_yokai'] == 'Noko')
            r.call('CreateMon', r.symbols['gEnemyParty'], noko, 25, 31, 1, 100, 0, 0)
            r.write(r.symbols['gEnemyPartyCount'], b'\x01')
            r.call('StartScriptedWildBattle')
            for f in range(4000):
                r.keys = {0} if f % 16 < 2 else set()
                r.run()
                if f > 400 and r.u32(r.symbols['gMain'] + 4) == r.symbols['BattleMainCB2'] | 1:
                    # Hold long enough for native entrance/menus, no attacks.
                    r.keys = set()
                    r.run(240)
                    break
        r.keys = set()
        r.frame.save(out / f'{n:02}.png')
        results.append(dict(scene=n, map=name, x=x, y=y, gender=gender, source='current-ROM native mGBA', fixture='map warp, actor visibility, chapter state; scene18 species fixture'))
        print(label, n, name, flush=True)
    (out / 'CAPTURES.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(), scope=__doc__, results=results), indent=2, ensure_ascii=False) + '\n')
finally:
    r.close()

#!/usr/bin/env python3
"""Prologue scenes on the real lab, with explicit progression fixtures."""
import hashlib
import os
import json
import re
from mgba_rpc import ROOT
from mgba_new_game import new_game

OUT = ROOT / 'QA_RECETTE_FINALE/RAPPROCHEMENT_2026_10_22' / 'prologue'
OUT.mkdir(parents=True, exist_ok=True)
glyphs = {m[1]: int(m[2], 16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$", (ROOT / 'charmap.txt').read_text(), re.M)}
glyphs["'"] = glyphs['’']

def encoded(text):
    return bytes(glyphs[c] for c in text)

def warp(r, x, y):
    r.keys = set()
    r.call('SetWarpDestination', 4, 3, 255, x, y)
    r.call('WarpIntoMap')
    r.call('SetMainCallback2', r.symbols['CB2_LoadMap'] | 1)
    r.run(180)

results = []
for gender, name in [(0, 'nathan'), (1, 'katie')]:
    r = new_game(gender)
    try:
        # New/rewritten lab lines, expanded at the full seven-character name limit.
        labels = {'RivalGrampsIsntAround', 'RivalFedUpWithWaiting', 'RivalNoFairWhatAboutMe',
                  'RivalMyMonLooksTougher', 'RivalDefeat', 'RivalGramps', 'RivalLeaveItToMeGramps',
                  'RivalTellSisNotToGiveYouMap', 'OakPokedexOnDesk', 'ReceivedPokedexFromOak',
                  'ReceiveWatch', 'WatchTutorial'}
        source = (ROOT / 'data/maps/PalletTown_ProfessorOaksLab/text.inc').read_text()
        checked = 0
        for label, body in re.findall(r'^PalletTown_ProfessorOaksLab_Text_(\w+)::\n((?:    \.string .*\n)+)', source, re.M):
            if label not in labels:
                continue
            for piece in re.findall(r'\.string "(.*)"', body):
                for line in re.split(r'\\[nlp]', piece):
                    line = line.rstrip('$').replace('{PLAYER}', 'WWWWWWW').replace('{RIVAL}', 'Matt')
                    if line:
                        r.write(r.PARAMS + 128, encoded(line) + b'\xff')
                        width = r.call('GetStringWidth', 2, r.PARAMS + 128, 0)
                        assert width <= 208, (label, line, width)
                        checked += 1
        assert checked > 30, checked
        results.append({'test': name + ': rewritten lab dialogue fits native font with widest player name', 'lines': checked, 'passed': True})
        r.call('VarSet', 0x4055, 1)
        r.call('FlagClear', 0x2B)
        r.call('FlagClear', 0x2D)
        warp(r, 6, 12)
        seen = False
        for f in range(12000):
            r.keys = {8} if f % 16 < 4 else set()
            r.run()
            if not seen and encoded('dernière génération.') in r.read(r.symbols['gStringVar4'], 1000):
                r.keys = set()
                r.run(360)
                r.frame.save(OUT / f'{name}-remise-montre.png')
                seen = True
            if f % 64 == 0 and r.call('VarGet', 0x4055) == 2:
                break
        else:
            raise AssertionError((name, 'starter scene never completed'))
        assert seen, 'Watch reception text never displayed'
        assert r.call('VarGet', 0x4055) == 2
        results.append({'test': name + ': automatic lab scene displays latest Watch, tutorial, then enables starter choice', 'passed': True})
        # Parcel-return progression fixture; the starter fight is not claimed here.
        r.call('VarSet', 0x4055, 4)
        r.call('VarSet', 0x4057, 1)
        r.call('AddBagItem', 349, 1)
        r.call('CreateMon', r.symbols['gPlayerParty'], 5, 10, 31, 1, 100, 0, 0)
        r.write(r.symbols['gPlayerPartyCount'], b'\x01')
        r.call('FlagSet', 0x2D)
        warp(r, 6, 4)
        r.keys = {4}
        r.run(8)
        r.keys = set()
        r.run(16)
        r.keys = {8}
        r.run(2)
        r.keys = set()
        seen_medallium = False
        for f in range(18000):
            r.keys = {8} if f % 16 < 4 else set()
            r.run()
            if not seen_medallium and encoded('ancien du Professeur Chen!') in r.read(r.symbols['gStringVar4'], 1000):
                r.keys = set()
                r.run(360)
                r.frame.save(OUT / f'{name}-medallium.png')
                seen_medallium = True
            if f % 64 == 0 and r.call('VarGet', 0x4055) == 6:
                break
        else:
            raise AssertionError((name, 'parcel scene never completed', r.call('VarGet', 0x4055)))
        assert seen_medallium
        assert r.call('FlagGet', 0x829)
        assert not r.call('CheckBagHasItem', 349, 1)
        assert r.call('CheckBagHasItem', 4, 5)
        assert r.call('TrySavingData', 0, max_frames=1200) == 1
        r.call('VarSet', 0x4055, 0)
        r.call('FlagClear', 0x829)
        assert r.call('LoadGameSave', 0, max_frames=1200) == 1
        assert r.call('VarGet', 0x4055) == 6 and r.call('FlagGet', 0x829)
        results.append({'test': name + ': actual A interaction with Chen, old Medallium text, menu unlock, parcel consumed, five balls; scene and unlock persist in Flash', 'passed': True})
    finally:
        r.close()
report = {'rom_sha256': hashlib.sha256(__import__('pathlib').Path(os.environ.get('YOKAI_QA_ROM', ROOT / 'pokefirered.gba')).read_bytes()).hexdigest(), 'scope': 'Real intro then fixture warps and lab story variables; watch scene, parcel scene via A interaction, Flash save/load. Not full journey, starter fight or complete campaign.', 'results': results}
(OUT / 'TEST_PROLOGUE_MGBA.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))

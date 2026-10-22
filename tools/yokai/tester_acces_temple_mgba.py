#!/usr/bin/env python3
"""Eight-trophy gate: native scripts, actual tile crossing and Flash persistence.

Fixture creates a game and warps to the existing entrance; no full-route claim.
"""
import hashlib
import json
import struct
from mgba_rpc import ROOT
from mgba_new_game import new_game

OUT = ROOT / 'QA_RECETTE_FINALE/SCENARIO_2026'
OUT.mkdir(exist_ok=True)

def position(r):
    return struct.unpack('<hh', r.read(r.u32(r.symbols['gSaveBlock1Ptr']), 4))

def warp(r, x=4, y=3):
    r.keys = set()
    r.call('SetWarpDestination', 13, 0, 255, x, y)
    r.call('WarpIntoMap')
    r.call('SetMainCallback2', r.symbols['CB2_LoadMap'] | 1)
    r.run(500)

def trophies(r, mask):
    # Provenance of the fourth scenario trophy, independent of old Erika badge04.
    r.call('FlagSet' if mask & (1 << 3) else 'FlagClear', 0x32F)
    r.call('FlagSet' if mask & (1 << 5) else 'FlagClear', 0x345)
    r.call('FlagSet' if mask & (1 << 6) else 'FlagClear', 0x346)
    for i in range(8):
        r.call('FlagSet' if mask & (1 << i) else 'FlagClear', 0x820 + i)

def advance(r, frames=500):
    for f in range(frames):
        r.keys = {0} if f % 16 < 4 else set()
        r.run()
    r.keys = set()

r = new_game()
results = []
try:
    warp(r)
    # Native script execution, exhaustive: no direct writes into VAR_RESULT.
    for mask in range(256):
        trophies(r, mask)
        r.call('ScriptContext_SetupScript', r.symbols['IndigoPlateau_EventScript_CheckEightTrophies'])
        r.run(6)
        assert r.call('VarGet', 0x800D) == (mask == 255), mask
    results.append({'test': 'All 256 trophy combinations, native script result', 'passed': True})
    # All native badges, including old Erika's badge04, do not replace Ariane.
    trophies(r,255)
    r.call('FlagClear',0x32F)
    r.call('ScriptContext_SetupScript',r.symbols['IndigoPlateau_EventScript_CheckEightTrophies']);r.run(6)
    assert r.call('VarGet',0x800D)==0
    # Actual historic Sabrina defeat with native badge06 is recognized idempotently.
    r.call('FlagSet',0x4B5)
    r.call('ScriptContext_SetupScript',r.symbols['IndigoPlateau_EventScript_CheckEightTrophies']);r.run(8)
    assert r.call('VarGet',0x800D)==1 and r.call('FlagGet',0x32F)
    r.call('FlagClear',0x4B5)
    results.append({'test':'Native badge04 from Erika alone cannot supply fourth scenario trophy; historic Sabrina defeat plus badge06 is recognized', 'passed':True})
    trophies(r,255);r.call('FlagClear',0x345)
    r.call('ScriptContext_SetupScript',r.symbols['IndigoPlateau_EventScript_CheckEightTrophies']);r.run(8)
    assert r.call('VarGet',0x800D)==0
    results.append({'test':'Old native Sabrina sixth badge cannot replace the canonical sixth trophy awarded by Alyzon','passed':True})
    # Every missing single trophy must block actual northward movement.
    for missing in range(8):
        trophies(r, 255 ^ (1 << missing))
        warp(r)
        assert position(r) == (4, 3), position(r)
        r.keys = {4}
        r.run(20)
        r.keys = set()
        r.run(40)
        if missing == 0:
            r.frame.save(OUT / 'temple-refus.png')
        advance(r)
        assert position(r) == (4, 3), (missing, position(r))
        assert r.read(r.u32(r.symbols['gSaveBlock1Ptr']) + 4, 2) == bytes([13, 0])
    results.append({'test': 'Eight actual entrance crossings refused, one distinct missing trophy each; safe step back', 'passed': True})
    trophies(r, 255)
    assert r.call('TrySavingData', 0, max_frames=1200) == 1
    trophies(r, 0)
    assert r.call('LoadGameSave', 0, max_frames=1200) == 1
    assert all(r.call('FlagGet', 0x820 + i) for i in range(8)) and r.call('FlagGet',0x32F)
    results.append({'test': 'Eight trophy flags retained by native Flash save/load', 'passed': True})
    warp(r)
    r.keys = {4}
    r.run(20)
    r.keys = set()
    r.run(60)
    r.keys = {4}
    r.run(180)
    advance(r, 2400)
    r.frame.save(OUT / 'diagnostic-entree.png')
    assert r.read(r.u32(r.symbols['gSaveBlock1Ptr']) + 4, 2) == bytes([1, 75]), (position(r), r.read(r.u32(r.symbols['gSaveBlock1Ptr']) + 4, 2))
    r.frame.save(OUT / 'temple-entree.png')
    results.append({'test': 'All eight trophies permit actual warp into first room', 'passed': True})
finally:
    r.close()
report = {'rom_sha256': hashlib.sha256((ROOT / 'pokefirered.gba').read_bytes()).hexdigest(), 'scope': 'Native scripts and button movement at the entrance, fixture warp; existing first room still contains old League content. Not a full adventure or new Temple validation.', 'results': results}
(OUT / 'TEST_ACCES_TEMPLE_MGBA.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""Native map removal and engineered legacy-save migration, not a full playthrough."""
import hashlib
import json
import os
import struct
import subprocess
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from scenario_qa_helpers import warp, pos, idle, face_a

OUT = ROOT / 'QA_RECETTE_FINALE/CARMIN_RETRAIT_USAPYON'


def actors(r):
    return [r.read(r.symbols['gObjectEvents'] + 36*i + 5, 1)[0]
            for i in range(16) if r.read(r.symbols['gObjectEvents'] + 36*i, 1)[0] & 1]


def continue_save(r):
    assert r.call('TrySavingData', 0, max_frames=1200) == 1
    assert r.call('LoadGameSave', 0, max_frames=1200) == 1
    r.call('SetMainCallback2', r.symbols['CB2_ContinueSavedGame'] | 1)
    r.keys = set()
    r.run(900)
    assert idle(r)


def main():
    OUT.mkdir(exist_ok=True)
    cases = []
    for gender, name in [(0, 'nathan'), (1, 'katie')]:
        r = new_game(gender)
        try:
            r.call('CreateMon', r.symbols['gPlayerParty'], 1, 24, 15, 1, 100, 0, 0)
            r.write(r.symbols['gPlayerPartyCount'], b'\x01')
            r.call('FlagSet', 0x821)
            r.call('FlagSet', 0x264)
            warp(r, 9, 6, 5, 3)
            assert actors(r).count(152) == 1 and 153 not in actors(r)
            r.frame.save(OUT / (name + '-ariane-seule.png'))
            # Model a prior-release save: its sixth cached actor really existed
            # in bda317714. Use the current script address; no old ROM addresses.
            template = bytearray.fromhex('069900000600020003080000000000000000000000000000')
            struct.pack_into('<I', template, 16, r.symbols['Route25_EventScript_UsapionCameo'])
            p = r.u32(r.symbols['gSaveBlock1Ptr']) + 0x8e0 + 24*5
            r.write(p, bytes(template))
            r.call('FlagSet', 0x32C)
            r.call('FlagClear', 0x32D)
            continue_save(r)
            assert pos(r) == (5, 17)
            assert r.call('FlagGet', 0x32D) and r.call('FlagGet', 0x32C)
            assert r.call('FlagGet', 0x821) and r.call('FlagGet', 0x264)
            assert 153 not in actors(r)
            assert r.read(r.u32(r.symbols['gSaveBlock1Ptr']) + 0x8e0 + 24*5, 1) == b'\x00'
            # Later Continue keeps position: the migration is one-shot.
            warp(r, 9, 6, 5, 3)
            continue_save(r)
            assert pos(r) == (5, 3) and actors(r).count(152) == 1 and 153 not in actors(r)
            face_a(r, 'U')
            callbacks = {int(f[0], 16) | 1 for line in subprocess.check_output(
                ['arm-none-eabi-nm', '--defined-only', str(r.elf_path)], text=True).splitlines()
                if len(f := line.split()) == 3 and f[2] == 'HandleInputChooseAction'}
            for frame in range(12000):
                r.keys = {8} if frame % 16 < 4 else set()
                r.run()
                if (r.u32(r.symbols['gMain'] + 4) == r.symbols['BattleMainCB2'] | 1
                        and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks):
                    break
            else:
                raise AssertionError('Ariane native action menu not reached')
            r.keys = set()
            r.run(30)
            assert r.u32(r.symbols['gTrainerBattleOpponent_A']) & 65535 == 416
            party = [r.call('GetMonData', r.symbols['gEnemyParty'] + 100*i, 11, 0) for i in range(4)]
            assert party == [96, 17, 51, 100], party
            assert r.call('GetBattleBGM') == 377
            r.frame.save(OUT / (name + '-combat-ariane.png'))
            cases.append(dict(gender=name, passed=True, map_ariane_count=1,
                              usapyon_map_absent=True, flash_save_continue_migration=True,
                              subsequent_continue_preserves_position=True,
                              native_ariane_party=party, battle_music=377))
        finally:
            r.close()
    rom = Path(os.environ['YOKAI_QA_ROM'])
    report = dict(passed=True, scope=__doc__, rom_size=rom.stat().st_size,
                  rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(), cases=cases)
    (OUT / 'TEST_MGBA.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

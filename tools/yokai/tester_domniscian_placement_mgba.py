#!/usr/bin/env python3
"""Targeted native mGBA fixtures: approved portrait layout, send-out and victory.

Map, flags and player party are fixtures. Battles run with controller input;
enemy HP, battle outcome and portrait OAM are never patched by this test.
"""
import hashlib
import json
import os
import struct
import subprocess
from pathlib import Path

from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C, MAPS, strong_party, warp


def main():
    mode = 'prive' if '_audio' in os.environ.get('YOKAI_QA_ROM', '') else 'public'
    dest = ROOT / 'docs/dossier-20261023/domniscian-placement' / mode
    dest.mkdir(parents=True, exist_ok=True)
    rows = []
    r = new_game()
    rom = Path(os.environ.get('YOKAI_QA_ROM', ROOT / 'pokefirered.gba'))
    result = {'passed': False, 'scope': __doc__, 'rom_sha256': hashlib.sha256(rom.read_bytes()).hexdigest(), 'checks': rows}
    try:
        actions = {int(line.split()[0], 16) | 1 for line in subprocess.check_output(['arm-none-eabi-nm', '--defined-only', str(r.elf_path)], text=True).splitlines() if len(line.split()) == 3 and line.split()[2] == 'HandleInputChooseAction'}
        base = r.snapshot()
        for name, rematch, regression in [('champion', False, False), ('revanche', True, False), ('berenice-regression', False, True)]:
            r.restore(base)
            r.call('VarSet', 0x4068, 1)
            r.call('FlagSet', 0x3E)
            if rematch:
                r.call('FlagSet', 0x82C)
                r.call('FlagSet', 0x825)
            mapname = 'FuchsiaCity_Gym' if regression else 'SaffronCity_Gym'
            label = 'Koga' if regression else 'Sabrina'
            warp(r, *MAPS[mapname], *( (4, 9) if regression else (14, 13)))
            strong_party(r)
            r.call('ScriptContext_SetupScript', r.symbols[mapname + '_EventScript_' + label])
            frames, portraits = [], []
            started = False
            action_seen = False
            seen_departed = False
            pic = C['TRAINER_PIC_YOKAI_BERENICE' if regression else 'TRAINER_PIC_YOKAI_DOMNISCIAN']
            last_portrait = False
            for f in range(26000):
                r.keys = {8} if f % 16 < 4 else set()
                r.run()
                battle = r.u32(r.symbols['gMain'] + 4) == r.symbols['BattleMainCB2'] | 1
                if battle:
                    started = True
                    sid = r.read(r.symbols['gBattlerSpriteIds'] + 1, 1)[0]
                    found = False
                    if sid < 64:
                        sp = r.symbols['gSprites'] + sid * 68
                        found = (r.read(sp + 62, 1)[0] & 5) == 1 and struct.unpack('<H', r.read(sp + 6, 2))[0] == pic
                        stationary = found and r.u32(sp + 28) == r.symbols['SpriteCallbackDummy'] | 1 and r.read(sp + 36, 2) == b'\0\0'
                        if stationary and not last_portrait:
                            x, y = struct.unpack('<hh', r.read(sp + 32, 4))
                            attr0, attr1 = struct.unpack('<HH', r.read(sp, 4))
                            matrix = (attr1 >> 9) & 31
                            affine = struct.unpack('<hhhh', r.read(r.symbols['gOamMatrices'] + matrix * 8, 8))
                            assert (x, y) == ((176, 40) if regression else (180, 28)), (name, x, y)
                            assert affine == ((256, 0, 0, 256) if regression else (192, 0, 0, 192)), (name, affine)
                            assert (attr0 >> 8) & 3 == (1 if regression else 3)
                            last_portrait = True
                            capture = name + ('-retour-portrait' if action_seen else '-portrait')
                            # Render the checked OAM at least once before saving the framebuffer.
                            r.run()
                            r.frame.save(dest / (capture + '.png'))
                            r.frame.resize((720, 480), Image.Resampling.NEAREST).save(dest / (capture + '-x3.png'))
                            portraits.append({'file': capture + '.png', 'center': [x, y], 'matrix': list(affine), 'after_sendout': action_seen})
                    if not found:
                        last_portrait = False
                    # Native action menu: the trainer has departed and the enemy is visible.
                    controller = r.u32(r.symbols['gBattlerControllerFuncs'])
                    if controller in actions:
                        action_seen = True
                        assert not found, 'Trainer portrait remained on screen after send-out'
                        seen_departed = True
                        if regression:
                            break
                if started and f % 8 == 0 and not action_seen:
                    frames.append(r.frame.copy().resize((480, 320), Image.Resampling.NEAREST))
                if started and not battle and f > 100 and r.u32(r.symbols['gMain'] + 4) == r.symbols['CB2_Overworld'] | 1 and r.read(r.symbols['sGlobalScriptContextStatus'], 1) == b'\2':
                    assert r.read(r.symbols['gBattleOutcome'], 1) == b'\1'
                    break
            else:
                raise AssertionError((name, 'battle timed out'))
            assert portraits and seen_departed
            if not regression:
                assert any(p['after_sendout'] for p in portraits), 'Victory portrait did not return'
            if frames:
                frames[0].save(dest / (name + '-intro.gif'), save_all=True, append_images=frames[1:], duration=135, loop=0)
            rows.append({'case': name, 'passed': True, 'portraits': portraits, 'sendout_cleared_portrait': seen_departed, 'controller_victory': not regression})
            print(name, 'passed', flush=True)
        result['passed'] = True
    finally:
        r.close()
        (dest / 'TEST_MGBA.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()

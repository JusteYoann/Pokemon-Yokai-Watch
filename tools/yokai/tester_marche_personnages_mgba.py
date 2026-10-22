#!/usr/bin/env python3
"""Real map actors, native VRAM animation cycles and unchanged trainer intros.

Walking is driven in place by the engine for reproducible rendering; this does
not claim new story movement scenes or a complete campaign playthrough.
"""
import hashlib
import json
import os
import re
from pathlib import Path

from PIL import Image

from mgba_new_game import new_game
from mgba_rpc import ROOT
from scenario_qa_helpers import warp

OUT = ROOT/os.environ.get('YOKAI_WALK_REPORT_DIR', 'QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/MARCHE')
OUT.mkdir(parents=True, exist_ok=True)
GROUPS = json.loads((ROOT/'data/maps/map_groups.json').read_text())
MAPS = {name: (i, j) for i, group in enumerate(GROUPS['group_order']) for j, name in enumerate(GROUPS[group])}
CONSTANTS = dict(re.findall(r'^#define\s+(\w+)\s+(\w+)\s*$', (ROOT/'include/constants/opponents.h').read_text(), re.M))
GFX = {k: int(v) for k, v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*$', (ROOT/'include/constants/event_objects.h').read_text(), re.M)}
ACTORS = [
    ('ariane', 0, 'VermilionCity_Gym', (3, 6), 'OBJ_EVENT_GFX_ARIANE', 'Ariane', 'Ariane', 'TRAINER_LEADER_LT_SURGE'),
    ('wyatt', 0, 'PewterCity_Gym', (4, 7), 'OBJ_EVENT_GFX_YOKAI_WYATT', 'YokaiWyatt', 'YokaiWyatt', 'TRAINER_LEADER_BROCK'),
    ('nathaniel', 0, 'FuchsiaCity', (25, 10), 'OBJ_EVENT_GFX_YOKAI_NATHANIEL', 'YokaiNathaniel', 'YokaiNathaniel', 'TRAINER_YOKAI_NATHANIEL'),
    ('michael', 1, 'FuchsiaCity', (25, 10), 'OBJ_EVENT_GFX_YOKAI_MICHAEL', 'YokaiMichael', 'YokaiMichael', 'TRAINER_YOKAI_MICHAEL'),
    ('don_morleone', 0, 'FiveIsland_RocketWarehouse', (22, 24), 'OBJ_EVENT_GFX_YOKAI_DONMORLEONE', 'YokaiDonMorleone', 'YokaiDonMorleone', 'TRAINER_YOKAI_DONMORLEONE'),
    ('mafiamille_1', 0, 'FiveIsland_RocketWarehouse', (22, 24), 'OBJ_EVENT_GFX_YOKAI_MAFIAMILLE1', 'YokaiMafiamille1', 'YokaiMafiamille1', 'TRAINER_YOKAI_MAFIAMILLE1'),
    ('mafiamille_2', 0, 'FiveIsland_RocketWarehouse', (22, 24), 'OBJ_EVENT_GFX_YOKAI_MAFIAMILLE2', 'YokaiMafiamille2', 'YokaiMafiamille2', 'TRAINER_YOKAI_MAFIAMILLE2'),
    ('mafiamille_3', 0, 'FiveIsland_RocketWarehouse', (22, 24), 'OBJ_EVENT_GFX_YOKAI_MAFIAMILLE3', 'YokaiMafiamille3', 'YokaiMafiamille3', 'TRAINER_YOKAI_MAFIAMILLE3'),
    ('employe_rouge', 0, 'SilphCo_11F', (9, 17), 'OBJ_EVENT_GFX_YOKAI_EMPLOYEROUGE', 'YokaiEmployeRouge', 'YokaiEmployeRouge', 'TRAINER_YOKAI_EMPLOYEROUGE'),
    ('employe_bleu', 0, 'SilphCo_11F', (9, 17), 'OBJ_EVENT_GFX_YOKAI_EMPLOYEBLEU', 'YokaiEmployeBleu', 'YokaiEmployeBleu', 'TRAINER_YOKAI_EMPLOYEBLEU'),
]


def number(name):
    while not str(name).isdigit():
        name = CONSTANTS[name]
    return int(name)


def main():
    reports = []
    selected = os.environ.get('YOKAI_WALK_ACTORS', 'ariane,nathaniel,michael,don_morleone,mafiamille_1,mafiamille_2,mafiamille_3,employe_rouge,employe_bleu').split(',')
    for actor, gender, map_name, position, gfx, picture, table, trainer in ACTORS:
        if actor not in selected:
            continue
        r = new_game(gender)
        try:
            r.call('CreateMon', r.symbols['gPlayerParty'], 1, 50, 31, 1, 100, 0, 0)
            r.write(r.symbols['gPlayerPartyCount'], b'\x01')
            if map_name in ('FiveIsland_RocketWarehouse', 'SilphCo_11F'):
                r.call('FlagSet', 0x82C)  # Actual existing postgame visibility condition.
            warp(r, *MAPS[map_name], *position)
            r.call('LockPlayerFieldControls')
            objects = [r.symbols['gObjectEvents']+36*i for i in range(16)]
            found = [o for o in objects if r.read(o, 1)[0]&1 and r.read(o+5, 1)[0] == GFX[gfx]]
            assert len(found) == 1, (actor, 'actual map actor absent or duplicated', found)
            obj = found[0]
            sprite = r.symbols['gSprites']+68*r.read(obj+4, 1)[0]
            data = (ROOT/f'graphics/yokai_characters/{actor}/overworld.4bpp').read_bytes()
            assert len(data) == 2304
            assert r.read(r.symbols['gObjectEventPic_'+picture], len(data)) == data
            png = Image.open(ROOT/f'graphics/yokai_characters/{actor}/overworld.png')
            assert png.mode == 'P' and png.info.get('transparency') == 0
            assert max(png.tobytes()) < 16
            bank = int.from_bytes(r.read(sprite+4, 2), 'little')>>12
            loaded_palette = r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank, 32)
            palette = png.getpalette()
            for index in set(png.tobytes())-{0}:
                red, green, blue = palette[3*index:3*index+3]
                expected_color = (red>>3) | ((green>>3)<<5) | ((blue>>3)<<10)
                assert int.from_bytes(loaded_palette[2*index:2*index+2], 'little') == expected_color, (actor, 'palette', index)
            frames = [data[i*256:(i+1)*256] for i in range(9)]
            image_table = r.symbols['sPicTable_'+table]
            assert r.u32(sprite+12) == image_table
            for i in range(9):
                assert r.u32(image_table+i*8) == r.symbols['gObjectEventPic_'+picture]+256*i
                assert int.from_bytes(r.read(image_table+i*8+4, 2), 'little') == 256
            directions = []
            for direction, label, expected in [(1, 'sud', {0, 3, 4}), (2, 'nord', {1, 5, 6}), (3, 'ouest', {2, 7, 8}), (4, 'est', {2, 7, 8})]:
                r.call('ObjectEventClearHeldMovementIfFinished', obj)
                r.call('ObjectEventTurn', obj, direction)
                r.run(20)
                r.frame.save(OUT/f'{actor}-{label}-fixe.png')
                observed = set()
                movie = []
                # Each held action performs one step, then stops. Repeat it so
                # both alternating feet are actually requested by the engine.
                for repeat in range(4):
                    r.call('ObjectEventClearHeldMovementIfFinished', obj)
                    r.call('ObjectEventSetHeldMovement', obj, 0x24+direction)
                    for t in range(40):
                        r.run()
                        attr2 = int.from_bytes(r.read(sprite+4, 2), 'little')
                        tile = attr2&1023
                        rendered = r.read(0x06010000+tile*32, 256)
                        observed.update(i for i, frame in enumerate(frames) if rendered == frame)
                        if t % 4 == 0:
                            movie.append(r.frame.copy())
                assert expected <= observed, (actor, label, expected, observed)
                movie[0].save(OUT/f'{actor}-{label}-marche.gif', save_all=True, append_images=movie[1:], duration=67, loop=0)
                contact = Image.new('RGB', (960, 320))
                for i in range(8):
                    contact.paste(movie[i*2], ((i%4)*240, (i//4)*160))
                contact.save(OUT/f'{actor}-{label}-marche.png')
                directions.append(dict(direction=label, native_vram_frames=sorted(observed), expected_frames=sorted(expected), passed=True))
                r.call('ObjectEventClearHeldMovementIfFinished', obj)
            # Exercise unchanged portrait and party through the native battle entry.
            r.call('UnlockPlayerFieldControls')
            trainer_id = number(trainer)
            r.w32(r.symbols['gTrainerBattleOpponent_A'], trainer_id)
            r.call('StartTrainerBattle')
            battle = []
            for t in range(520):
                r.keys = {8} if t % 16 < 4 else set()
                r.run()
                if t % 16 == 0:
                    battle.append(r.frame.copy())
            r.keys = set()
            assert r.u32(r.symbols['gMain']+4) == r.symbols['BattleMainCB2']|1
            battle[0].save(OUT/f'{actor}-entree-combat.gif', save_all=True, append_images=battle[1:], duration=267, loop=0)
            contact = Image.new('RGB', (960, 320))
            for i, index in enumerate([2, 4, 6, 8, 10, 12, 16, 24]):
                contact.paste(battle[index], ((i%4)*240, (i//4)*160))
            contact.save(OUT/f'{actor}-entree-combat.png')
            reports.append(dict(actor=actor, gender=gender, actual_map=map_name, linked_frames=9,
                                directions=directions, native_trainer_intro=True, trainer_id=trainer_id,
                                used_palette_indices_verified=True, transparent_index=0,
                                complete_battle=False, passed=True))
            print('PASS', actor, flush=True)
        except BaseException:
            r.frame.save(OUT/f'{actor}-diagnostic.png')
            raise
        finally:
            r.close()
    assert reports, 'No selected actors tested'
    rom = Path(os.environ['YOKAI_QA_ROM'])
    result = dict(passed=True, scope=__doc__, rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(), rom_bytes=rom.stat().st_size, tests=reports)
    (OUT/'TEST_MGBA.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()

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

OUT = ROOT/'QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/MARCHE'
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
]


def number(name):
    while not str(name).isdigit():
        name = CONSTANTS[name]
    return int(name)


def main():
    reports = []
    selected = os.environ.get('YOKAI_WALK_ACTORS', 'ariane,wyatt,nathaniel,michael').split(',')
    for actor, gender, map_name, position, gfx, picture, table, trainer in ACTORS:
        if actor not in selected:
            continue
        r = new_game(gender)
        try:
            r.call('CreateMon', r.symbols['gPlayerParty'], 1, 50, 31, 1, 100, 0, 0)
            r.write(r.symbols['gPlayerPartyCount'], b'\x01')
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

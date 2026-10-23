#!/usr/bin/env python3
"""Enma's existing dialogue and Matt's original Champion battle in mGBA.

Explicit map/flags/strong-party fixtures, no changes to opposing teams or ROM.
Not a full adventure playthrough or subjective listening.
"""
import hashlib, json, os, ctypes
from collections import deque
import numpy as np
from mgba_new_game import new_game
from mgba_rpc import ROOT, BATCH
from pilote_combat_mgba import battle_keys
import tester_cameos_boss_mgba as boss
from tester_musiques_integrees_mgba import MAPS, channel

P = ROOT/os.environ.get('YOKAI_AUDIO31_EVENTS_DIR','QA_RECETTE_FINALE/AUDIO_31_OST/evenements')
P.mkdir(parents=True, exist_ok=True)
r = new_game()
base = r.snapshot()
rows = []
passed = False
error = 'Interrupted'
try:
    r.call('FlagSet', boss.C['FLAG_SYS_GAME_CLEAR'])
    boss.warp(r, {'map': MAPS['MtEmber_Summit'][1]}, {'x': 11, 'y': 6})
    field = r.u32(r.symbols['gMPlayInfo_BGM'])
    boss.interact(r)
    for f in range(1800):
        r.run()
        if channel(r, 5): break
    else: raise AssertionError('Existing Enma dialogue did not play slot 5')
    assert r.u32(r.symbols['gMPlayInfo_BGM']) == r.symbols['mus_yokai_05']
    r.run(120); r.frame.save(P/'enma-dialogue.png')
    # B advances dialogue and declines the original yes/no offer.
    for f in range(10000):
        r.keys = {0} if f % 16 < 2 else set(); r.run()
        if f > 120 and r.read(r.symbols['sGlobalScriptContextStatus'], 1) == b'\x02' and r.u32(r.symbols['gMPlayInfo_BGM']) == field: break
    else: raise AssertionError('Enma decline did not restore exploration music')
    r.keys = set(); r.run(120); r.frame.save(P/'enma-retour.png')
    rows.append(dict(event='Original Enma dialogue at Mont Braise', slot=5,
                     actual_NPC_interaction=True, decline_restores_field_music=True))
    print('EVENT PASS Enma dialogue/decline', flush=True)

    r.restore(base)
    for flag in (0x828, 0x829, boss.C['FLAG_HIDE_OAK_IN_CHAMP_ROOM']): r.call('FlagSet', flag)
    r.call('VarSet', 0x4031, 0)
    r.call('CreateMon', r.symbols['gPlayerParty'], 1, 100, 31, 1, 100, 0, 0)
    r.write(r.symbols['gPlayerPartyCount'], b'\x01')
    scratch = r.PARAMS + 128
    for field in ['MON_DATA_HP', 'MON_DATA_MAX_HP', 'MON_DATA_ATK', 'MON_DATA_SPATK', 'MON_DATA_DEF', 'MON_DATA_SPDEF']:
        r.w32(scratch, 999); r.call('SetMonData', r.symbols['gPlayerParty'], boss.C[field], scratch)
    for slot, move in enumerate(['MOVE_AERIAL_ACE', 'MOVE_SHOCK_WAVE', 'MOVE_SWIFT', 'MOVE_MAGICAL_LEAF']):
        r.call('SetMonMoveSlot', r.symbols['gPlayerParty'], boss.C[move], slot)
    boss.warp(r, {'map': MAPS['PokemonLeague_ChampionsRoom'][1]}, {'x': 6, 'y': 17})
    started = False
    seen = False
    for f in range(65000):
        r.keys = battle_keys(r, f); r.run()
        if r.u32(r.symbols['gMain']+4) == r.symbols['BattleMainCB2'] | 1:
            started = True
            if channel(r, 25) and not seen:
                seen = True; music_frame = f
            if seen and f == music_frame + 180:
                r.frame.save(P/'matt-combat.png')
                hold_frames = int(os.environ.get('YOKAI_AUDIO31_MATT_HOLD_FRAMES','0'))
                if hold_frames:
                    ring = deque(maxlen=200)
                    def capture(data, frames):
                        ring.append(ctypes.string_at(data, frames*4)); return frames
                    callback = BATCH(capture); r.lib.retro_set_audio_sample_batch(callback)
                    r.keys = set(); r.run(hold_frames)
                    r.lib.retro_set_audio_sample_batch(r.callbacks[3])
                    signal = np.frombuffer(b''.join(ring),'<i2').astype(float)
                    active = channel(r,25) is not None
                    rows.append(dict(event='Prolonged actual Matt battle, no controller action',
                        held_frames=hold_frames, held_seconds_approx=hold_frames/59.7275,
                        native_sample_still_active=active, final_audio_AC_RMS_pcm16=float(signal.std()),
                        requested_continuous_music_goal_met=active,
                        known_limitation=None if active else 'Unresolved Final Battle loop; original one-shot ends and falls silent'))
                    r.frame.save(P/'matt-combat-prolonge.png')
        if started and r.u32(r.symbols['gMPlayInfo_BGM']) == r.symbols['mus_yokai_26'] and channel(r, 26): break
    else: raise AssertionError(('Champion did not reach victory music', started, seen))
    assert seen and r.read(r.symbols['gBattleOutcome'], 1) == b'\x01'
    assert r.call('FlagGet', boss.C['FLAG_DEFEATED_CHAMP'])
    r.keys = set(); r.run(120); r.frame.save(P/'matt-conclusion.png')
    rows.append(dict(event='Original Champion scene and battle', battle_slot=25,
                     victory_slot=26, controller_victory=True, opponent_team_unchanged=True))
    print('EVENT PASS Matt Champion/victory', flush=True)
    passed = True
    error = None
except BaseException as exc:
    error = str(exc); r.frame.save(P/'diagnostic.png'); raise
finally:
    r.close()
    (P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed, error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(), results=rows,
        scope='Controller-started new game, explicit progression/warp/strong-party fixtures. Original Enma interaction and actual Matt battle won via controller. Not full adventure or listening.'), indent=2)+'\n')

#!/usr/bin/env python3
"""Native boot/title/menu proof. Inputs only until menu; fixtures labelled.

Private audio captures stay outside Git. Full new-game/continue checks are
separate so captures do not depend on a modified save state.
"""
import ctypes
import hashlib
import json
import os
import wave
from pathlib import Path
from mgba_rpc import ROOT, Emulator, BATCH

mode = 'prive' if '_audio' in os.environ.get('YOKAI_QA_ROM', '') else 'public'
out = ROOT / 'docs/ecran-titre-credits-20261024' / mode
out.mkdir(parents=True, exist_ok=True)
r = Emulator(initial_frames=1)
chunks = []
callback = BATCH(lambda data, frames: (chunks.append(ctypes.string_at(data, frames * 4)) or frames))
r.lib.retro_set_audio_sample_batch(callback)
frames = []
def bgm_inactive():
    status = r.u32(r.symbols['gMPlayInfo_BGM'] + 4)
    return status == 0 or bool(status & 0x80000000)

seen_signature = False
signature_frames = 0
title_frames = 0
try:
    for frame in range(1300):
        r.run()
        is_title = r.read(r.symbols['sPresentationTitle'], 1)[0]
        tick = r.u32(r.symbols['sPresentationTick'])
        if r.u32(r.symbols['gMain'] + 4) == r.symbols['CB2_RunYokaiPresentation'] | 1:
            if is_title:
                title_frames += 1
                if tick == 310:
                    r.frame.save(out / 'titre.png')
                    r.frame.resize((720, 480)).save(out / 'titre-x3.png')
            else:
                seen_signature = True
                signature_frames += 1
                assert bgm_inactive()
                if tick == 60:
                    r.frame.save(out / 'signature.png')
        if frame % 6 == 0:
            frames.append(r.frame.copy())
    assert seen_signature and 118 <= signature_frames <= 140, signature_frames
    assert title_frames > 1000
    frames[0].save(out / 'titre-20s.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
    raw = b''.join(chunks)
    if mode == 'prive':
        private = Path('/workspace/private-audio/title-credits-preuves')
        private.mkdir(exist_ok=True)
        with wave.open(str(private / 'titre-nates-house-mgba.wav'), 'wb') as wav:
            wav.setparams((2, 2, 32768, 0, 'NONE', 'not compressed'))
            wav.writeframes(raw)
    r.keys = {3}  # native START, immediate stop rather than fade-out
    r.run()
    assert bgm_inactive(), 'START did not immediately stop BGM'
    r.keys = set()
    r.run(240)
    assert r.u32(r.symbols['gMain'] + 4) == r.symbols['CB2_MainMenu'] | 1
    assert bgm_inactive()
    r.frame.save(out / 'menu-sans-sauvegarde.png')
    chunks.clear()
    r.run(360)
    assert not any(b''.join(chunks)), 'BGM/audio remained in the idle menu'
    report = dict(passed=True, rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(), signature_frames=signature_frames, title_frames=title_frames, start_immediate_stop=True, menu_idle_silent=True, scope=__doc__)
    (out / 'TEST_TITRE.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2))
finally:
    r.close()

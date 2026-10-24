#!/usr/bin/env python3
"""Full255s native credits, both genders, native texture/palette/timing checks.

DoCredits entry is a fixture after an actual new game, not a League playthrough.
Separate finale tests cover the Hall of Fame and real Continue transition.
"""
import ctypes
import hashlib
import json
import os
import wave
from pathlib import Path
from PIL import Image, ImageDraw
from mgba_rpc import ROOT, BATCH
from mgba_new_game import new_game

mode = 'prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
doc = ROOT / 'docs/ecran-titre-credits-20261024'
slides = json.loads((ROOT / 'data/yokai/credits_storyboard.json').read_text())['slides']
all_results = []
class Geometry(ctypes.Structure):
    _fields_ = [('base_width',ctypes.c_uint),('base_height',ctypes.c_uint),('max_width',ctypes.c_uint),('max_height',ctypes.c_uint),('aspect_ratio',ctypes.c_float)]
class Timing(ctypes.Structure):
    _fields_ = [('fps',ctypes.c_double),('sample_rate',ctypes.c_double)]
class AV(ctypes.Structure):
    _fields_ = [('geometry',Geometry),('timing',Timing)]
for gender, label in enumerate(['garcon','fille']):
    r = new_game(gender)
    out = doc / mode / 'credits' / label
    out.mkdir(parents=True, exist_ok=True)
    chunks = []
    callback = BATCH(lambda data,frames: (chunks.append(ctypes.string_at(data,frames*4)) or frames))
    r.lib.retro_set_audio_sample_batch(callback)
    excerpt = []
    final = []
    transitions = []
    captured = set()
    try:
        # Preflight actual encoded strings with the native font, before timing.
        for index, slide in enumerate(slides):
            width = r.call('GetStringWidth', 2 if index == 31 else 0, r.symbols[f'sCreditText{index}'], 0)
            assert width <= slide['text_width'], ('text overflow', index, width, slide['text_width'])
        r.call('DoCredits')
        for _ in range(30):
            if r.u32(r.symbols['gMain']+4) == r.symbols['CB2_RollYokaiCredits'] | 1:
                break
            r.run()
        else:
            raise AssertionError('DoCredits did not enter new credits')
        chunks.clear()
        previous = -1
        while True:
            index = r.read(r.symbols['sYokaiCreditsSlide'],1)[0]
            tick = int.from_bytes(r.read(r.symbols['sYokaiCreditsTick'],2),'little')
            total = r.u32(r.symbols['sYokaiCreditsTotalFrames'])
            if index >= 32:
                break
            if total > 5 and (tick <= 6 or slides[index]['frames'] - tick <= 3):
                assert max(hi for lo,hi in r.frame.convert('RGB').getextrema()) <= 64, ('bright transition flash', index, tick, total)
            if index != previous:
                stem = f'{label}-{index:02}'
                binary = (ROOT / f'graphics/yokai_credits/{stem}.8bpp').read_bytes()
                assert r.read(0x06000000,len(binary)) == binary, ('tiles',index)
                assert r.read(0x0600E000,2048) == (ROOT / f'graphics/yokai_credits/{stem}.bin').read_bytes(), ('map',index)
                assert r.read(r.symbols['gPlttBufferUnfaded'],480) == (ROOT / f'graphics/yokai_credits/{stem}.gbapal').read_bytes()[:480], ('palette',index)
                transitions.append(dict(index=index,frame=total))
                previous = index
            if (index < 31 and tick == 140) or (index == 31 and tick == 700):
                r.frame.save(out / f'{index+1:02}.png')
                captured.add(index)
            if total % 6 == 0:
                if total < 868:
                    excerpt.append(r.frame.copy())
                if index == 31:
                    final.append(r.frame.copy())
            r.run()
        assert captured == set(range(32))
        assert total == 15239, total
        for i in range(31):
            assert abs(transitions[i+1]['frame'] - transitions[i]['frame'] - slides[i]['frames']) <= 3
        assert abs(total - transitions[31]['frame'] - 1792) <= 3
        if mode == 'prive':
            assert r.u32(r.symbols['gMPlayInfo_BGM']) == r.symbols['mus_yokai_credits']
            if gender == 0:
                av = AV()
                r.lib.retro_get_system_av_info(ctypes.byref(av))
                private = Path('/workspace/private-audio/title-credits-preuves')
                private.mkdir(exist_ok=True)
                with wave.open(str(private/'credits-complets-mgba.wav'),'wb') as wav:
                    wav.setparams((2,2,round(av.timing.sample_rate),0,'NONE','not compressed'))
                    wav.writeframes(b''.join(chunks))
        # Text and images fully black; no sound after the actual ending.
        r.run(8)
        chunks.clear()
        r.run(50)
        assert not any(b''.join(chunks)), 'audio persists after ending'
        assert not any(r.frame.convert('RGB').tobytes()), 'ending not black'
        excerpt[0].save(out/'extrait.gif',save_all=True,append_images=excerpt[1:],duration=100,loop=0)
        final[0].save(out/'final-30s.gif',save_all=True,append_images=final[1:],duration=100,loop=0)
        board = Image.new('RGB',(960,768),'black')
        draw = ImageDraw.Draw(board)
        for i in range(32):
            x=(i%4)*240
            y=(i//4)*96
            photo=Image.open(out/f'{i+1:02}.png').resize((120,80),Image.Resampling.NEAREST)
            board.paste(photo,(x+50,y+14))
            draw.text((x+8,y+16),str(i+1),fill='white')
        board.save(out/'planche-32.png')
        all_results.append(dict(gender=gender,passed=True,frames=total,final_frames=1792,transitions=transitions,all_32_native_assets_verified=True,transition_flash_check=True,ending_black_and_silent=True))
        print('PASS full credits',mode,label,total,flush=True)
    finally:
        r.close()
(doc/mode/'TEST_CREDITS.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=all_results),indent=2,ensure_ascii=False)+'\n')

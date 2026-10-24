#!/usr/bin/env python3
"""Native static photo set: plain grass field background and14 native OW sprites.

Developer-only staging uses OAM sprites rather than moving field objects.
No sprite artwork is drawn or composited into the screenshot. Every palette is
loaded from its native graphics tag, assigned its own OBJ bank and verified.
"""
import hashlib
import json
import os
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS, C, warp

gender = int(os.environ.get('YOKAI_QA_GENDER', '0'))
out = ROOT / os.environ.get('YOKAI_CREDITS_PHOTO_DIR', 'docs/ecran-titre-credits-20261024/souvenirs') / ['garcon', 'fille'][gender]
out.mkdir(parents=True, exist_ok=True)
actors = [
    ("Enma l'Ancien", 178, 44, 48), ('Orqanos', 179, 82, 48),
    ('Zazel', 177, 120, 48), ('Maître Nyada', 180, 158, 48), ('Domniscian', 161, 196, 48),
    ('Michael' if gender else 'Nathaniel', 159 if gender else 158, 44, 80),
    ('Hovernyan', 176, 82, 80), ('Don Morléone', 164, 120, 80),
    ('Ariane', 152, 158, 80), ('Usapion', 153, 196, 80),
    ('Matt', 72, 62, 112), ('Protagoniste', 7 if gender else 0, 100, 112),
    ('Nathan' if gender else 'Katie', 156 if gender else 157, 138, 112),
    ('Jibanyan', 172, 176, 112),
]
r = new_game(gender)
try:
    warp(r, *MAPS['Route1'], 10, 17)
    r.call('InitMap')
    for y in range(7, 32):
        for x in range(7, 30):
            r.call('MapGridSetMetatileIdAt', x, y, 0x3001)
    r.call('DrawWholeMapView')
    r.run(4)
    r.call('SetMainCallback1', 0)
    r.call('SetMainCallback2', r.symbols['SpriteCallbackDummy'] | 1)
    r.call('ResetTasks')
    r.call('ResetSpriteData')
    r.call('FreeAllSpritePalettes')
    rows = []
    for bank, (name, graphics, x, y) in enumerate(actors):
        info = r.call('GetObjectEventGraphicsInfo', graphics)
        tag = int.from_bytes(r.read(info + 2, 2), 'little')
        palette_index = r.call('FindObjectEventPaletteIndexByTag', tag)
        assert palette_index < 255, (name, tag)
        palette = r.u32(r.symbols['sObjectEventSpritePalettes'] + 8 * palette_index)
        sprite = r.call('CreateObjectGraphicsSprite', graphics, r.symbols['SpriteCallbackDummy'] | 1, x, y, 0)
        assert sprite < 64, name
        r.call('StartSpriteAnim', r.symbols['gSprites'] + 68 * sprite, 0)
        attr = r.symbols['gSprites'] + 68 * sprite + 4
        r.write(attr, ((int.from_bytes(r.read(attr, 2), 'little') & 0x3FF) | bank << 12).to_bytes(2, 'little'))
        rows.append(dict(name=name, graphics_id=graphics, sprite_id=sprite, x=x, y=y, bank=bank, palette=palette))
    for row in rows:
        r.call('LoadPalette', row['palette'], 256 + 16 * row['bank'], 32)
    r.call('AnimateSprites')
    r.call('BuildOamBuffer')
    r.run(4)
    for row in rows:
        assert r.read(r.symbols['gPlttBufferFaded'] + 512 + 32 * row['bank'], 32) == r.read(row['palette'], 32), row['name']
    r.frame.save(out / '32.png')
    r.frame.resize((720, 480)).save(out / 'groupe-x3.png')
    (out / 'GROUPE.json').write_text(json.dumps(dict(passed=True, scope=__doc__, rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(), members=rows, excluded=['Whisper', 'Komasan', 'Don Spiraton', 'Léo', 'Professeur Chen']), ensure_ascii=False, indent=2) + '\n')
    print('PASS native14-member group', gender)
finally:
    r.close()

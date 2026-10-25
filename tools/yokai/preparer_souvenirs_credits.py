#!/usr/bin/env python3
"""Pack real mGBA stills as small native BG photographs. No synthetic memories."""
import argparse
import csv
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'graphics/yokai_credits'
DOC = ROOT / 'docs/ecran-titre-credits-20261024'
ORDER = [1,2,3,15,4,5,17,6,7,8,9,10,11,12,13,14,18,19,20,21,22,23,24,25,26,27,28,29,16,30,31,32]
PAGES = [
    'Une aventure de\nJuste Yoann', 'Univers Yo-kai\nLEVEL-5', 'Jeu original\nGAME FREAK',
    'Adaptation du récit\nJuste Yoann', 'Pokémon\nNintendo\nCreatures\nGAME FREAK',
    'Création de Kanto\nGAME FREAK', 'Adaptation Yo-kai\nJuste Yoann',
    'Personnages\nLEVEL-5', 'Musique originale\nYo-kai Watch',
    'Scénario adapté\nJuste Yoann', 'Jeu original\nPokémon Rouge Feu',
    'Univers Yo-kai\nLEVEL-5', 'Réalisation\nJuste Yoann',
    'Graphismes du jeu\nGAME FREAK\nLEVEL-5', 'Remerciements\nÀ la communauté',
    'Adaptation de Kanto\nJuste Yoann', 'Personnages\nLEVEL-5',
    'Musique originale\nYo-kai Watch', 'Jeu original\nGAME FREAK',
    'Création du projet\nJuste Yoann', 'Émulation de test\nmGBA',
    'Univers Yo-kai\nLEVEL-5', 'Développement\nJuste Yoann',
    'Personnages\nLEVEL-5', 'Remerciements\nAux joueurs',
    'Jeu original\nGAME FREAK', 'Adaptation Yo-kai\nJuste Yoann',
    'Univers Yo-kai\nLEVEL-5', 'Réalisation\nJuste Yoann',
    'Musique des crédits\nYo-kai Watch', 'Remerciements\nÀ la communauté',
    "MERCI D'AVOIR JOUÉ !",
]
LAYOUTS = [(120,80,8,24,136,42,96),(120,80,112,16,8,48,96),(96,64,72,8,8,96,224),(80,56,16,88,112,24,120)]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--generate', action='store_true')
p.add_argument('--pack')
a = p.parse_args()
OUT.mkdir(exist_ok=True, parents=True)

if a.generate:
    storyboard = list(csv.DictReader((DOC / 'sources/STORYBOARD_CREDITS_32.csv').open()))
    slides = []
    declarations = []
    tables = []
    shared_maps = {}
    for gender in ['garcon', 'fille']:
        records = []
        for index, scene in enumerate(ORDER):
            replacements_path=ROOT/'data/yokai/credits_replacements.json'
            replacements=json.loads(replacements_path.read_text()) if replacements_path.exists() else {}
            replacement=replacements.get(str(index))
            source = ROOT/replacement['captures'][gender] if replacement else DOC / f'souvenirs/{gender}/{scene:02}.png'
            original = Image.open(source).convert('RGB')
            w,h,x,y,tx,ty,tw = (192,112,24,8,0,136,240) if scene == 32 else LAYOUTS[index % 4]
            if scene == 32:
                original = original.crop((24,24,216,136))
            elif scene in [28,29] and not replacement:
                original = original.crop((0,40,240,160))
            photo = ImageOps.fit(original,(w,h),method=Image.Resampling.NEAREST).quantize(colors=223,dither=Image.Dither.NONE)
            indexed = Image.new('P',photo.size)
            indexed.putpalette([0,0,0] + photo.getpalette()[:669] + [0] * 96)
            indexed.putdata([i + 1 for i in photo.getdata()])
            stem = f'{gender}-{index:02}'
            indexed.save(OUT / f'{stem}.png')
            suffix = stem.replace('-','_')
            for kind,typ,extension in [('Tiles','u32','8bpp.lz'),('Map','u32','bin.lz'),('Pal','u16','gbapal')]:
                if kind == 'Map':
                    key = (w,h,x,y)
                    if key in shared_maps:
                        continue
                    shared_maps[key] = suffix
                declarations.append(f'static const {typ} sCredit{kind}_{suffix}[] = INCBIN_{"U16" if typ == "u16" else "U32"}("graphics/yokai_credits/{stem}.{extension}");')
            records.append(f'    {{sCreditTiles_{suffix}, sCreditMap_{shared_maps[(w,h,x,y)]}, sCreditPal_{suffix}}},')
            if gender == 'garcon':
                frames = 1792 if scene == 32 else 434 if index < 24 else 433
                slides.append(dict(index=index, original_scene=scene, title=replacement['title'] if replacement else storyboard[scene-1]['scene'], width=w,height=h,x=x,y=y,text_x=tx,text_y=ty,text_width=tw,frames=frames,text=PAGES[index]))
        tables.append('{\n' + '\n'.join(records) + '\n}')
    for s in slides:
        declarations.append(f'static const u8 sCreditText{s["index"]}[] = _({json.dumps(s["text"],ensure_ascii=False)});')
    declarations.append('static const struct CreditAssets sCreditAssets[2][32] = {\n' + ',\n'.join(tables) + '\n};')
    declarations.append('static const struct CreditSlide sCreditSlides[32] = {')
    for s in slides:
        declarations.append(f'    {{sCreditText{s["index"]}, {s["frames"]}, {s["text_x"]}, {s["text_y"]}, {s["text_width"]}}},')
    declarations.append('};\n')
    (ROOT / 'src/data/yokai_credits.h').write_text('\n'.join(declarations))
    (ROOT / 'data/yokai/credits_storyboard.json').write_text(json.dumps(dict(order_approved_by_user=True,final_exclusions=['Whisper','Komasan','Don Spiraton','Léo','Professeur Chen','Usapion'],slides=slides),indent=2,ensure_ascii=False) + '\n')
    assert sum(s['frames'] for s in slides) == 15239
    print('Generated64 native indexed photographs, total15239 frames')

if a.pack:
    stem = a.pack
    im = Image.open(OUT / f'{stem}.png')
    assert im.mode == 'P' and max(im.getdata()) <= 223
    slide_index = int(stem.split('-')[-1])
    slides = json.loads((ROOT / 'data/yokai/credits_storyboard.json').read_text())['slides']
    slide = slides[slide_index]
    tiles = bytearray(64)
    tilemap = [0] * 1024
    for y in range(im.height // 8):
        for x in range(im.width // 8):
            tilemap[(y + slide['y']//8) * 32 + x + slide['x']//8] = len(tiles) // 64
            tiles.extend(im.crop((x*8,y*8,x*8+8,y*8+8)).tobytes())
    assert len(tiles) < 32768
    (OUT / f'{stem}.8bpp').write_bytes(tiles)
    (OUT / f'{stem}.bin').write_bytes(struct.pack('<1024H',*tilemap))
    pal = (im.getpalette() + [0] * 768)[:768]
    (OUT / f'{stem}.gbapal').write_bytes(b''.join(struct.pack('<H',(r>>3)|((g>>3)<<5)|((b>>3)<<10)) for r,g,b in zip(pal[::3],pal[1::3],pal[2::3])))

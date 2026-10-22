#!/usr/bin/env python3
"""Extract native cells from a zoom16 pixel-art sheet; preserve existing artwork.

No illustration resizing, painted pixels or generated faces: only native leg
cells in rows26..31 are taken from the separately drawn walking source.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_palette(actor):
    # Original preview PNGs sometimes retained a softer outline color than the
    # actual overworld palette. Export the real bank, without changing that bank.
    group = 'don_morleone' if actor.startswith('mafiamille_') else 'domniscian' if actor.startswith('employe_') else actor
    path = ROOT/'graphics/yokai_characters'/group/'overworld.pal'
    colors = [tuple((int(v)>>3)<<3 for v in line.split()) for line in path.read_text().splitlines()[3:19]]
    assert len(colors) == 16 and all(len(c) == 3 for c in colors)
    return [v for color in colors for v in color]+[0]*720, path


def save_native_loops(folder, sheet):
    for label, order in [('sud', [3, 0, 4, 0]), ('nord', [5, 1, 6, 1]), ('ouest', [7, 2, 8, 2])]:
        frames = [sheet.crop((16*i, 0, 16*(i+1), 32)) for i in order]
        frames[0].save(folder/'source'/f'marche-{label}-native.gif', save_all=True,
                       append_images=frames[1:], duration=133, loop=0,
                       transparency=0, disposal=2, optimize=False)


def convert(actor):
    folder = ROOT/'graphics/yokai_characters'/actor
    source = folder/'source/walk-native-grid.png'
    original = folder/'source/idle-native-before-walk.png'
    base = Image.open(original)
    drawing = Image.open(source).convert('RGB')
    assert base.mode == 'P' and base.size == (48, 32)
    assert drawing.size == (1536, 1024), 'Reject wrong logical grid rather than rescale'
    palette = np.array(base.getpalette()[:48], dtype=np.int32).reshape(16, 3)
    exported_palette, palette_path = active_palette(actor)
    raw = np.asarray(drawing).astype(np.int32)
    sheet = Image.new('P', (144, 32))
    sheet.putpalette(exported_palette)
    sheet.paste(base, (0, 0))
    frames = []
    purity = []
    for slot in range(6):
        frame = base.crop((slot//2*16, 0, (slot//2+1)*16, 32))
        values = []
        for y in range(26, 32):
            for x in range(16):
                # One authored logical pixel occupies exactly16x16 source pixels.
                pixels = raw[y*16:(y+1)*16, (slot*16+x)*16:(slot*16+x+1)*16].reshape(-1, 3)
                distances = ((pixels[:, None, :]-palette[None, 1:, :])**2).sum(2)
                indices = distances.argmin(1)+1
                background = (pixels[:, 0]>180) & (pixels[:, 2]>180) & (pixels[:, 1]<90)
                indices[background] = 0
                counts = np.bincount(indices, minlength=16)
                index = int(counts.argmax())
                values.append(index)
                purity.append(float(counts[index])/256)
        patch = Image.new('P', (16, 6))
        patch.putpalette(base.getpalette())
        patch.putdata(values)
        frame.paste(patch, (0, 26))
        assert frame.crop((0, 0, 16, 26)).tobytes() == base.crop((slot//2*16, 0, (slot//2+1)*16, 26)).tobytes()
        assert frame.getbbox() is not None
        frames.append(frame)
        sheet.paste(frame, ((slot+3)*16, 0))
    differences = [sum(a != b for a, b in zip(frames[i].tobytes(), frames[i+1].tobytes())) for i in (0, 2, 4)]
    assert all(differences), f'{actor}: no real alternating steps {differences}'
    assert np.mean(purity) > .95, 'Source failed the logical pixel grid; request new artwork'
    assert sheet.crop((0, 0, 48, 32)).tobytes() == base.tobytes()
    assert max(sheet.tobytes()) < 16
    sheet.info['transparency'] = 0
    sheet.save(folder/'overworld.png', bits=4, transparency=0)
    save_native_loops(folder, sheet)
    rgba = sheet.convert('RGBA')
    preview = Image.new('RGB', rgba.size, (200, 200, 200))
    preview.paste(rgba, (0, 0), rgba)
    preview.resize((1152, 256), Image.Resampling.NEAREST).save(folder/'walk-preview-x8.png')
    report = dict(actor=actor, source_sha256=sha(source), idle_sha256=sha(original),
                  source_logical_grid=[96, 64], zoom=16, frame=[16, 32], frames=9,
                  order=['idle south', 'idle north', 'idle west', 'south A', 'south B', 'north A', 'north B', 'west A', 'west B'],
                  east='Native horizontal flip, as in previous fixed sprite',
                  original_idle_indices_preserved=True, original_head_and_torso_indices_preserved=True,
                  original_palette_preserved=True, transparent_index=0,
                  exported_png_palette_matches_active_bank=str(palette_path.relative_to(ROOT)),
                  active_palette_sha256=sha(palette_path),
                  changed_step_pixels_by_pair=differences, mean_source_cell_palette_purity=float(np.mean(purity)),
                  method=__doc__, status='Produced; emulator integration results recorded separately')
    (folder/'walk-production.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(actor, 'six new step frames', differences)


def shared_variant(actor, parent, lut=None):
    folder = ROOT/'graphics/yokai_characters'/actor
    parent_folder = folder.parent/parent
    original = folder/'source/idle-native-before-walk.png'
    if not original.exists():
        original.parent.mkdir(exist_ok=True)
        original.write_bytes((folder/'overworld.png').read_bytes())
    idle = Image.open(original)
    result = Image.open(parent_folder/'overworld.png')
    assert result.size == (144, 32)
    if lut:
        table = list(range(256))
        for old, new in lut.items():
            table[old] = new
        result = result.point(table)
    parent_image = Image.open(parent_folder/'overworld.png')
    assert all((a == 0) == (b == 0) for a, b in zip(result.tobytes(), parent_image.tobytes()))
    expected_palette, palette_path = active_palette(actor)
    assert result.getpalette()[:48] == expected_palette[:48]
    assert result.crop((0, 0, 48, 32)).tobytes() == idle.tobytes()
    if lut:
        result.info['transparency'] = 0
        result.save(folder/'overworld.png', bits=4, transparency=0)
    else:
        (folder/'overworld.png').write_bytes((parent_folder/'overworld.png').read_bytes())
    save_native_loops(folder, result)
    rgba = result.convert('RGBA')
    preview = Image.new('RGB', result.size, (200, 200, 200))
    preview.paste(rgba, (0, 0), rgba)
    preview.resize((1152, 256), Image.Resampling.NEAREST).save(folder/'walk-preview-x8.png')
    report = dict(actor=actor, shared_native_walk=parent, exact_geometry=True,
                  index_variant=lut or {}, frames=9, original_idle_indices_preserved=True,
                  original_palette_preserved=True, original_combat_portrait_preserved=True,
                  source_sha256=sha(parent_folder/'overworld.png'), idle_sha256=sha(original),
                  exported_png_palette_matches_active_bank=str(palette_path.relative_to(ROOT)),
                  status='Produced; emulator integration results recorded separately')
    (folder/'walk-production.json').write_text(json.dumps(report, indent=2)+'\n')
    print(actor, 'shared approved map design', parent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('actors', nargs='*')
    parser.add_argument('--variants', action='store_true')
    args = parser.parse_args()
    if not args.actors and not args.variants:
        parser.error('Select actors or --variants')
    for actor in args.actors:
        convert(actor)
    if args.variants:
        shared_variant('mafiamille_2', 'mafiamille_1')
        shared_variant('mafiamille_3', 'mafiamille_1')
        shared_variant('employe_bleu', 'employe_rouge', {4:10, 5:10, 6:2})

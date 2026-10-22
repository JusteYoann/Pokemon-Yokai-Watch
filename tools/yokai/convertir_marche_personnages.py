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


def convert(actor):
    folder = ROOT/'graphics/yokai_characters'/actor
    source = folder/'source/walk-native-grid.png'
    original = folder/'source/idle-native-before-walk.png'
    base = Image.open(original)
    drawing = Image.open(source).convert('RGB')
    assert base.mode == 'P' and base.size == (48, 32)
    assert drawing.size == (1536, 1024), 'Reject wrong logical grid rather than rescale'
    palette = np.array(base.getpalette()[:48], dtype=np.int32).reshape(16, 3)
    raw = np.asarray(drawing).astype(np.int32)
    sheet = Image.new('P', (144, 32))
    sheet.putpalette(base.getpalette())
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
                  changed_step_pixels_by_pair=differences, mean_source_cell_palette_purity=float(np.mean(purity)),
                  method=__doc__, status='Produced; emulator integration results recorded separately')
    (folder/'walk-production.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(actor, 'six new step frames', differences)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('actors', nargs='+')
    for actor in parser.parse_args().actors:
        convert(actor)

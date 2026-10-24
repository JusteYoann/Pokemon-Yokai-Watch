#!/usr/bin/env python3
"""Convert supplied artwork to native GBA palettes/tiles, without dithering.

--landscape creates the indexed source PNG. --pack rebuilds binary assets from
the versioned indexed PNGs; no generated full-resolution illustration required.
"""
import argparse
import json
import struct
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'graphics/yokai_title'
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--landscape', type=Path)
p.add_argument('--pack', choices=['fresque', 'logo'])
a = p.parse_args()
if a.landscape:
    image = Image.open(a.landscape).convert('RGB').resize((256, 128), Image.Resampling.LANCZOS)
    image.quantize(colors=16, dither=Image.Dither.NONE).save(OUT / 'fresque.png')
    image = Image.open(OUT / 'logo-original.png').convert('RGBA').resize((208, 120), Image.Resampling.LANCZOS)
    mask = image.getchannel('A').point(lambda n: 255 if n >= 128 else 0)
    colors = image.convert('RGB').quantize(colors=15, dither=Image.Dither.NONE)
    indexed = Image.new('P', image.size)
    indexed.putpalette([0, 0, 0] + colors.getpalette()[:45] + [0] * (768 - 48))
    indexed.putdata([n + 1 if opaque else 0 for n, opaque in zip(colors.getdata(), mask.getdata())])
    indexed.save(OUT / 'logo.png', transparency=0)

if a.pack:
    name = a.pack
    im = Image.open(OUT / f'{name}.png')
    assert im.mode == 'P'
    palette = (im.getpalette() + [0] * 48)[:48]
    assert max(im.getdata()) <= 15
    (OUT / f'{name}.gbapal').write_bytes(b''.join(struct.pack('<H', (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)) for r, g, b in zip(palette[::3], palette[1::3], palette[2::3])))
    tiles = [bytes(32)]
    lookup = {tiles[0]: 0}
    tilemap = [0] * (2048 if name == 'fresque' else 1024)
    for y in range(im.height // 8):
        for x in range(im.width // 8):
            pixels = list(im.crop((x * 8, y * 8, x * 8 + 8, y * 8 + 8)).getdata())
            tile = bytes(pixels[i] | (pixels[i + 1] << 4) for i in range(0, 64, 2))
            if tile not in lookup:
                lookup[tile] = len(tiles)
                tiles.append(tile)
            if name == 'fresque':
                index = (y + 2) * 32 + x % 32 + (x // 32) * 1024
                tilemap[index] = lookup[tile]
                # Native reflected second half: identical border pixels at both
                # joins, no crossfade/double buffer, no visible wrap seam.
                tilemap[(y + 2) * 32 + (31 - x) + 1024] = lookup[tile] | 0x400
            else:
                tilemap[(y + 1) * 32 + x + 2] = lookup[tile] | 0x1000
    assert len(tiles) <= (1024 if name == 'fresque' else 512), (name, len(tiles))
    (OUT / f'{name}.4bpp').write_bytes(b''.join(tiles))
    (OUT / f'{name}.bin').write_bytes(struct.pack('<' + 'H' * len(tilemap), *tilemap))
    print(json.dumps(dict(asset=name, unique_tiles=len(tiles), tile_bytes=len(tiles) * 32, map_bytes=len(tilemap) * 2)))

#!/usr/bin/env python3
"""Technical conversion of original generated art: nearest resize, indexed GBA palette.
No repainting; the full source is preserved. Banks13–15 reserved for engine UI.
"""
from pathlib import Path
from PIL import Image
import struct
ROOT=Path(__file__).resolve().parents[2];folder=ROOT/'graphics/yokai_presentation'
im=Image.open(folder/'source/nuit-kanto-original.png').convert('RGB').resize((240,160),Image.Resampling.NEAREST).quantize(colors=208,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
pal=im.getpalette();im.putpalette(pal[:624]+[0]*(768-624));im.save(folder/'nuit.png')
tiles=[y*30+x if x<30 and y<20 else 0 for y in range(32) for x in range(32)];(folder/'nuit.bin').write_bytes(struct.pack('<1024H',*tiles))
print('240x160; 600 8bpp tiles, 208 indexed colors; 32x32 tilemap')

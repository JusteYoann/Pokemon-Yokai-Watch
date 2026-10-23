#!/usr/bin/env python3
"""Render a literal native pixel matrix transcribed from the creator's grid.
No generative image, drawing rescale, interpolated outlines, or invented animation.
RGB values remain a visual transcription rather than a binary-original extraction.
"""
from pathlib import Path
import json,struct
from PIL import Image
R=Path(__file__).resolve().parents[4];D=R/'graphics/yokai_zombies/errant';g=json.loads((D/'front-grid.json').read_text());keys=list(g['palette_rgb555']);assert keys[0]=='.' and len(keys)<=16
pal=[c for k in keys for c in g['palette_rgb555'][k]];pal=(pal+[0]*768)[:768]
im=Image.new('P',(g['width'],g['height']),0);im.putpalette(pal);im.info['transparency']=0
for y,row in enumerate(g['rows']):
 assert len(row)==g['width']
 for x,k in enumerate(row):im.putpixel((x,y),keys.index(k))
im.save(D/'front-native.png',transparency=0)
frame=Image.new('P',(32,32),0);frame.putpalette(pal);frame.info['transparency']=0;frame.paste(im,(g['frame_x'],g['frame_y']));frame.save(D/'front.png',transparency=0)
frame.convert('RGBA').resize((256,256),Image.Resampling.NEAREST).save(D/'front-x8.png')
(D/'front.gbapal').write_bytes(struct.pack('<16H',*[((pal[i*3]>>3)|((pal[i*3+1]>>3)<<5)|((pal[i*3+2]>>3)<<10)) for i in range(16)]))
b=bytearray()
for ty in range(4):
 for tx in range(4):
  for y in range(8):
   for x in range(0,8,2):b.append(frame.getpixel((tx*8+x,ty*8+y))|(frame.getpixel((tx*8+x+1,ty*8+y))<<4))
(D/'front.4bpp').write_bytes(b)
assert len(b)==512 and frame.convert('RGBA').getbbox()==(9,11,23,31)
print('Native matrix 14x20, indexed32x32, foot y30, 512-byte 4bpp,32-byte palette')

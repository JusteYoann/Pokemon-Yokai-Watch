#!/usr/bin/env python3
"""Convert the existing indexed Hovernyan frames to Nathaniel's visible height; no redraw or palette change."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'graphics/yokai_characters/hovernyan'
source=Image.open(D/'overworld-reference.png');nathan=Image.open(ROOT/'graphics/yokai_characters/nathaniel/overworld.png')
mask=nathan.crop((0,0,16,32)).point(lambda x:255 if x else 0);bbox=mask.getbbox();height=bbox[3]-bbox[1]
out=Image.new('P',source.size,0);out.putpalette(source.getpalette());out.info['transparency']=0
for y in [0,32]:
 frame=source.crop((0,y,32,y+32));box=frame.point(lambda x:255 if x else 0).getbbox();width=round((box[2]-box[0])*height/(box[3]-box[1]))
 scaled=frame.crop(box).resize((width,height),Image.Resampling.NEAREST);out.paste(scaled,((32-width)//2,y+bbox[3]-height))
out.save(D/'overworld.png',bits=4,transparency=0)
out.convert('RGBA').resize((256,512),Image.Resampling.NEAREST).save(D/'apercu-x8.png')
assert out.getpalette()==source.getpalette()
print('Native visible height',height,'width',width,'foot baseline',bbox[3]-1)

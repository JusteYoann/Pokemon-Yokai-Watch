#!/usr/bin/env python3
"""Opaque checkerboard views of actual native PNGs, with intended hardware flips."""
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
active='graphics/yokai_characters/nathan/normal.4bpp' in (R/'src/data/object_events/object_event_graphics.h').read_text()
for person in ['nathan','katie','matt']:
 d=R/'graphics/yokai_characters'/person
 roles=[('front',64,64),('back',64,64),('normal',16,32),('surf_run',16,32),('bike',32,32),('vs_seeker_bike',32,32),('item',32,32),('fish',32,32),('credits',64,64)] if person!='matt' else [('credits',64,64)]
 out=Image.new('RGB',(1536,len(roles)*144))
 for y in range(out.height):
  for x in range(out.width):out.putpixel((x,y),(224,224,224) if (x//16+y//16)%2 else (176,176,176))
 draw=ImageDraw.Draw(out)
 for row,(file,w,h) in enumerate(roles):
  p=d/(file+'.png');draw.text((4,row*144+2),file+' / '+('ACTIVE' if active else 'NOT ACTIVE YET')+' / GBA orientation preview',fill=(0,0,0))
  if not p.exists():continue
  im=Image.open(p);count=im.width//w if im.width>w else im.height//h
  for i in range(count):
   f=im.crop((i*w,0,(i+1)*w,h)) if im.width>w else im.crop((0,i*h,w,(i+1)*h))
   if person=='katie' and i in {'surf_run':{11},'bike':{2,7},'fish':{0,1,2,3}}.get(file,set()):f=f.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   scale=2 if w==64 else 4;a=f.convert('RGBA').resize((w*scale,h*scale),Image.Resampling.NEAREST);out.paste(a,(i*w*scale,row*144+16),a)
 out.save(d/'complete-preview.png')

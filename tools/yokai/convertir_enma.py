#!/usr/bin/env python3
"""GBA format conversion of original generated Lord Enma and Kyubi artwork."""
import hashlib,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/enma'
im=Image.open(D/'source/generated-sheet.png').convert('RGBA')
rects=[(210,15,740,680),(830,140,1400,680),(250,700,470,1005),(650,700,880,1005),(1040,700,1260,1005)]
crops=[]
for box in rects:
 c=im.crop(box);a=c.getchannel('A').point(lambda x:255 if x>=128 else 0);c.putalpha(a);c=c.crop(a.getbbox());crops.append(c)
palette=[(0,0,0),(24,8,24),(64,8,24),(120,16,32),(208,24,40),(248,72,64),(248,128,96),(184,120,40),
         (232,176,56),(248,224,104),(248,240,184),(248,248,224),(64,32,80),(136,72,168),(184,112,216),(40,168,192)]
palette=[tuple((v>>3)*255//31 for v in color) for color in palette];flat=[v for color in palette for v in color]
frames=[]
for index,c in enumerate(crops):
 size=(64,64) if index==0 else ((32,32) if index==1 else (16,32))
 scale=min(60/c.width,60/c.height) if index==0 else (min(30/c.width,30/c.height) if index==1 else min(16/max(x.width for x in crops[2:]),28/max(x.height for x in crops[2:])))
 resized=c.resize((max(1,round(c.width*scale)),max(1,round(c.height*scale))),Image.Resampling.NEAREST)
 f=Image.new('RGBA',size);f.alpha_composite(resized,((size[0]-resized.width)//2,size[1]-resized.height-1))
 pixels=[]
 for red,green,blue,alpha in f.getdata():
  pixels.append(0 if not alpha else min(range(1,16),key=lambda k:sum((v-p)**2 for v,p in zip((red,green,blue),palette[k]))))
 out=Image.new('P',size);out.putpalette(flat+[0]*(768-len(flat)));out.putdata(pixels);out.info['transparency']=0;frames.append(out)
frames[0].save(D/'battle.png',bits=4,transparency=0);frames[1].save(D/'kyubi_overworld.png',bits=4,transparency=0)
ow=Image.new('P',(48,32));ow.putpalette(frames[0].getpalette());ow.info['transparency']=0
for i,f in enumerate(frames[2:]):ow.paste(f,(i*16,0))
ow.save(D/'overworld.png',bits=4,transparency=0)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
p=Image.new('RGB',(512,300))
for y in range(p.height):
 for x in range(p.width):p.putpixel((x,y),(224,224,224) if (x//16+y//16)%2 else (176,176,176))
for i,f in enumerate(frames):
 scale=4 if i<2 else 3;g=f.convert('RGBA').resize((f.width*scale,f.height*scale),Image.Resampling.NEAREST)
 xy=(0,0) if i==0 else ((320,0) if i==1 else (290+(i-2)*70,170));p.paste(g,xy,g)
p.save(D/'preview-checkerboard.png')
(D/'conversion.json').write_text(json.dumps({'source_sha256':hashlib.sha256((D/'source/generated-sheet.png').read_bytes()).hexdigest(),'source_dimensions':im.size,'crop_rectangles':rects,'trainer':[64,64],'enma_overworld':[16,32,3],'kyubi_overworld':[32,32,1],'palette_colors':16,'transparent_index':0,'npc_animation_policy':'Stationary NPC, four facing directions via three frames and native horizontal flip; no walking scene required or claimed.'},ensure_ascii=False,indent=2)+'\n')

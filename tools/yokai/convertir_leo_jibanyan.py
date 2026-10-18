#!/usr/bin/env python3
"""Technical crop/NN/indexing of nine original generated map frames, no redraw."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'graphics/yokai_characters/leo_jibanyan';source=D/'source/generated-sheet.png';im=Image.open(source).convert('RGBA');frames=[];boxes=[]
for n in range(9):
 x=n%3;y=n//3;cell=im.crop((x*im.width//3,y*im.height//3,(x+1)*im.width//3,(y+1)*im.height//3));alpha=cell.getchannel('A').point(lambda v:255 if v>=128 else 0);cell.putalpha(alpha);box=alpha.getbbox();assert box;boxes.append(list(box));crop=cell.crop(box);scale=min(30/crop.width,29/crop.height);crop=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.NEAREST);frame=Image.new('RGBA',(32,32));frame.alpha_composite(crop,((32-crop.width)//2,32-crop.height));frames.append(frame)
order=[0,3,6,1,2,4,5,7,8];pixels=[p for frame in frames for p in frame.getdata() if p[3]];atlas=Image.new('RGB',(len(pixels),1));atlas.putdata([p[:3] for p in pixels]);pal=atlas.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette();palette=[(0,0,0)]+[tuple((v>>3)*255//31 for v in pal[i:i+3]) for i in range(0,45,3)];sheet=Image.new('P',(32,32*9));sheet.putpalette([v for rgb in palette for v in rgb]+[0]*720)
for n,source_n in enumerate(order):
 frame=frames[source_n];indices=[0 if not a else min(range(1,16),key=lambda k:sum((v-p)**2 for v,p in zip((r,g,b),palette[k]))) for r,g,b,a in frame.getdata()];tile=Image.new('P',(32,32));tile.putpalette(sheet.getpalette());tile.putdata(indices);sheet.paste(tile,(0,n*32))
sheet.info['transparency']=0;sheet.save(D/'overworld.png',bits=4,transparency=0);(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
preview=Image.new('RGB',(384,384));px=preview.load()
for y in range(384):
 for x in range(384):px[x,y]=(224,224,224) if (x//8+y//8)%2 else (176,176,176)
for src,n in enumerate(order):
 sp=sheet.crop((0,src*32,32,(src+1)*32)).convert('RGBA').resize((128,128),Image.Resampling.NEAREST);preview.paste(sp,((n%3)*128,(n//3)*128),sp)
preview.save(D/'preview-checkerboard.png');(D/'conversion.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_cells=boxes,native_dimensions=[32,32],native_frame_order=order,frames=9,palette_colors=16,transparent_index=0,role='Only transformed Bill/Leo event; original human form and separation scripts retained'),indent=2)+'\n')

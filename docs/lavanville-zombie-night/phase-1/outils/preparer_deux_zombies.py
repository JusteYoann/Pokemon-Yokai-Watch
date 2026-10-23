#!/usr/bin/env python3
"""Technical format conversion for emulator preview. No pose redesign.
Candidate logical grid is an extraction from a generated source, not certified pixel-identical to the submitted screenshot.
"""
import sys,json,shutil
from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parents[1]/'prototypes/apercu-deux-zombies-mgba';D.mkdir(exist_ok=True)
src=Path(sys.argv[1]);im=Image.open(src).convert('RGBA');
if src.resolve()!=(D/'source-transparente.png').resolve():shutil.copyfile(src,D/'source-transparente.png')
rows=[]
for i in range(2):
 p=im.crop((round(i*im.width/2),0,round((i+1)*im.width/2),im.height));a=p.getchannel('A').point(lambda x:255 if x>=240 else 0);p.putalpha(a);p=p.crop(a.getbbox())
 p.thumbnail((24,24),Image.Resampling.NEAREST);alpha=p.getchannel('A');rgb=p.convert('RGB');q=rgb.quantize(colors=12,dither=Image.Dither.NONE);base=q.getpalette()[:36];pixels=[rgb.getpixel((x,y)) for y in range(p.height) for x in range(p.width) if alpha.getpixel((x,y))];red=max(pixels,key=lambda c:c[0]-c[1]-c[2]);ivory=max(pixels,key=lambda c:min(c[0],c[1])+c[2]//2);pink=max([c for c in pixels if c[0]>150 and c[2]>80 and c[1]<180],key=lambda c:min(c[0],c[2]));pal=[v//8*8 for v in base+list(red)+list(ivory)+list(pink)];triples=[tuple(pal[j:j+3]) for j in range(0,45,3)];out=Image.new('P',(32,32),0);out.putpalette(([0,0,0]+pal+[0]*768)[:768]);out.info['transparency']=0;dx=(32-p.width)//2;dy=31-p.height
 for y in range(p.height):
  for x in range(p.width):
   if alpha.getpixel((x,y)):out.putpixel((x+dx,y+dy),min(range(15),key=lambda k:sum((a-b)**2 for a,b in zip(rgb.getpixel((x,y)),triples[k])))+1)
 out.save(D/f'zombie-{i+1}.png',transparency=0)
 out.convert('RGBA').resize((256,256),Image.Resampling.NEAREST).save(D/f'zombie-{i+1}-x8.png')
 rows.append(dict(index=i+1,canvas=[32,32],bbox=list(out.convert('RGBA').getbbox()),opaque_colors=len({v[:3] for v in out.convert('RGBA').getdata() if v[3]}),alpha_binary=True,foot_y=30))
(D/'CONVERSION.json').write_text(json.dumps(dict(method='Crop two transparent assets, NEAREST native-size candidate 24px high proportionally inside32x32, <=15 opaque RGB555 colors. Not a pixel-identity certification.',sprites=rows),indent=2)+'\n');print(rows)

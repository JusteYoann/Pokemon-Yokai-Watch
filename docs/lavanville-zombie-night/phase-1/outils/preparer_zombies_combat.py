#!/usr/bin/env python3
"""Prepare four generated battle concepts as indexed GBA candidates.
Source generation + native conversion, not a claim of hand-authored native pixel art.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,struct,sys,hashlib
import numpy as np
from scipy.ndimage import label,find_objects
R=Path(__file__).resolve().parents[4];G=R/'graphics/yokai_zombies';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/zombies-combat';Q.mkdir(exist_ok=True)
S=G/'sources';S.mkdir(exist_ok=True);src=Path(sys.argv[1]);target=S/'quatre-zombies-combat-source.png'
if src.resolve()!=target.resolve():shutil.copyfile(src,target)
sheet=Image.open(target).convert('RGBA');rows=[];images=[]
labels,count=label(np.array(sheet)[:,:,3]>=240,np.ones((3,3)));areas=np.bincount(labels.ravel());slices=find_objects(labels);ids=sorted((np.argsort(areas[1:])[-4:]+1).tolist(),key=lambda j:slices[j-1][1].start)
variants=[('errant',(52,54)),('sprinteur',(58,50)),('colosse',(58,56)),('spectral',(50,56))]
for i,(name,limit) in enumerate(variants):
 im=sheet.copy();a=Image.fromarray(((labels==ids[i])*255).astype('uint8'));im.putalpha(a);im=im.crop(a.getbbox());im.thumbnail(limit,Image.Resampling.NEAREST)
 a=im.getchannel('A');rgb=im.convert('RGB');pix=[rgb.getpixel((x,y)) for y in range(im.height) for x in range(im.width) if a.getpixel((x,y))]
 q=rgb.quantize(colors=11,dither=Image.Dither.NONE);pal=q.getpalette()[:33]
 red=max(pix,key=lambda c:c[0]-c[1]-c[2]);teal=max(pix,key=lambda c:c[1]+c[2]-2*c[0]);ivory=max(pix,key=lambda c:min(c[0],c[1])+c[2]//2);pink=max([c for c in pix if c[0]>140 and c[2]>70 and c[1]<c[0]*.85],key=lambda c:min(c[0],c[2]))
 pal=[v//8*8 for v in pal+list(red)+list(teal)+list(ivory)+list(pink)];colors=[tuple(pal[j:j+3]) for j in range(0,45,3)]
 out=Image.new('P',(64,64),0);out.putpalette(([0,0,0]+pal+[0]*768)[:768]);out.info['transparency']=0;dx=(64-im.width)//2;dy=60-im.height
 for y in range(im.height):
  for x in range(im.width):
   if a.getpixel((x,y)):out.putpixel((dx+x,dy+y),1+min(range(15),key=lambda j:sum((u-v)**2 for u,v in zip(rgb.getpixel((x,y)),colors[j]))))
 d=G/name;d.mkdir(exist_ok=True);out.save(d/'battle-front.png',transparency=0);out.convert('RGBA').resize((384,384),Image.Resampling.NEAREST).save(d/'battle-front-x6.png')
 full=out.getpalette();(d/'battle-front.gbapal').write_bytes(struct.pack('<16H',*[(full[j*3]>>3)|((full[j*3+1]>>3)<<5)|((full[j*3+2]>>3)<<10) for j in range(16)]))
 b=bytearray()
 for ty in range(8):
  for tx in range(8):
   for yy in range(8):
    for xx in range(0,8,2):b.append(out.getpixel((tx*8+xx,ty*8+yy))|out.getpixel((tx*8+xx+1,ty*8+yy))<<4)
 (d/'battle-front.4bpp').write_bytes(b);rgba=out.convert('RGBA');used={v[:3] for v in rgba.getdata() if v[3]};assert len(used)<=15 and len(b)==2048
 rows.append(dict(variant=name,file=f'graphics/yokai_zombies/{name}/battle-front.png',canvas=[64,64],bbox=list(rgba.getbbox()),opaque_colors=len(used),tile_bytes=len(b),palette_bytes=32,sha256=hashlib.sha256((d/'battle-front.png').read_bytes()).hexdigest(),status='Created native-format artwork candidate; no species/team/stat/patrol assignment'))
 images.append(rgba)
board=Image.new('RGBA',(256,64))
for i,im in enumerate(images):board.alpha_composite(im,(64*i,0))
board.save(Q/'quatre-zombies-natif.png');board.resize((1536,384),Image.Resampling.NEAREST).save(Q/'quatre-zombies-x6.png')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
labelled=Image.new('RGBA',(1024,292),(232,232,240,255));draw=ImageDraw.Draw(labelled)
for y in range(0,256,16):
 for x in range(0,1024,16):
  if (x//16+y//16)%2:draw.rectangle((x,y,x+15,y+15),fill=(208,208,220,255))
for i,im in enumerate(images):labelled.alpha_composite(im.resize((256,256),Image.Resampling.NEAREST),(256*i,0));draw.text((256*i+20,264),variants[i][0].upper(),font=font,fill='black')
labelled.save(Q/'planche-quatre-zombies.png')
compare=Image.new('RGBA',(384,128),(232,232,240,255))
for i,im in enumerate(images):compare.alpha_composite(im,(64*i,0))
for i,n in enumerate([1,41,48,115,143,70]):compare.alpha_composite(Image.open(R/f'graphics/yokai/{n:03}/front.png').convert('RGBA'),(64*i,64))
compare.resize((1536,512),Image.Resampling.NEAREST).save(Q/'comparaison-151-x4.png')
manifest=dict(kind='Four front battle sprite candidates',creation='Generated concepts guided by six existing151fronts, approved OW identity and user-provided Zombifdge artwork; binary-alpha NEAREST64x64 preparation and RGB555 palette reduction. Sources retained. Not described as hand-authored native artwork.',source_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),overworld_approved_asset_unchanged=True,records=rows)
(Q/'RESSOURCES.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows))

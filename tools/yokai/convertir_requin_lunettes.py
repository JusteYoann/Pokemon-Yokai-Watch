#!/usr/bin/env python3
"""Conversion technique de la planche imagegen : découpe, réduction, palette GBA.
Aucun redessin : les silhouettes viennent entièrement de la planche source.
"""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/requin_lunettes';S=D/'source/planche-generee.png'
im=Image.open(S).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0))
approved=Image.open(D/'source/profils-valides.png').convert('RGBA');approved.putalpha(approved.getchannel('A').point(lambda v:255 if v>=128 else 0))
reference=Image.open(R/'graphics/dossier-20261023/nyada/overworld.png').convert('RGBA').getchannel('A').getbbox();height=reference[3]-reference[1];baseline=reference[3]
palette=[(0,0,0),(14,14,20),(40,42,54),(64,66,76),(39,69,91),(64,106,133),(95,145,166),(236,235,200),(223,218,169),(250,250,247),(163,192,204),(81,142,171),(47,99,130),(101,58,31),(155,100,51),(208,87,112)]
flat=[c for rgb in palette for c in rgb]+[0]*720
sheet=Image.new('P',(288,32));sheet.putpalette(flat);sheet.info['transparency']=0
rows=[(0,390),(390,725),(725,1086)];records=[]
for direction in range(3):
 for pose,row in enumerate((1,0,2)):
  x0=direction*im.width//4;x1=(direction+1)*im.width//4;y0,y1=rows[row]
  cell=(im if direction==0 else approved).crop((x0,y0,x1,y1));box=cell.getchannel('A').getbbox();assert box
  body=cell.crop(box);width=max(1,round(body.width*height/body.height));assert width<=32
  body=body.resize((width,height),Image.Resampling.NEAREST)
  out=Image.new('P',(32,32));out.putpalette(flat)
  indices=[0 if a<128 else min(range(1,16),key=lambda i:sum((rgb[k]-palette[i][k])**2 for k in range(3))) for *rgb,a in body.get_flattened_data()]
  sprite=Image.new('P',body.size);sprite.putpalette(flat);sprite.putdata(indices);out.paste(sprite,((32-width)//2,baseline-height))
  sheet.paste(out,((direction*3+pose)*32,0));records.append(dict(direction=['face','dos','gauche','droite'][direction],pose=['pas-gauche','repos','pas-droit'][pose],source_box=[x0+box[0],y0+box[1],x0+box[2],y0+box[3]],native_bbox=[(32-width)//2,baseline-height,(32-width)//2+width,baseline]))
sheet.save(D/'overworld.png',transparency=0,bits=4)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
(D/'CONVERSION.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(S.read_bytes()).hexdigest(),approved_profiles_sha256=hashlib.sha256((D/'source/profils-valides.png').read_bytes()).hexdigest(),method=__doc__,nyada_bbox=reference,height=height,baseline=baseline,colors=palette,right_profile='exact hardware horizontal flip of left profile',frames=records),ensure_ascii=False,indent=2)+'\n')
P=R/'docs/requin-lunettes-overworld-20261025';P.mkdir(exist_ok=True)
preview=Image.new('RGBA',(96,128))
for n in range(12):
 frame=sheet.crop(((n if n<9 else n-3)*32,0,(n if n<9 else n-3)*32+32,32)).convert('RGBA')
 if n>=9:frame=frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 preview.paste(frame,((n%3)*32,(n//3)*32))
preview.save(P/'planche-native.png');preview.resize((576,768),Image.Resampling.NEAREST).save(P/'planche-x6.png')

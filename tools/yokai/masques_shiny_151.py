#!/usr/bin/env python3
"""Localized color masks for shared normal indices. Silhouette and coordinates fixed.
The 8 color-only textures are derived from normal pixels; no drawing or dithering.
"""
import colorsys,json
from collections import Counter
from pathlib import Path
from PIL import Image,ImageDraw
from nettoyer_shiny_151 import rgb555,luma
MASKED={18,51,66,67,120,133,145,150}

def tone(base,i,pal):
 level=luma(pal[i]);factor=.65 if level<.25 else .83 if level<.5 else 1 if level<.8 else 1.13
 h,l,s=colorsys.rgb_to_hls(*(v/255 for v in base));return rgb555([round(v*255) for v in colorsys.hls_to_rgb(h,min(.95,l*factor),s)])
def pointmask(poly):
 a=Image.new('1',(64,64));ImageDraw.Draw(a).polygon(poly,fill=1);return a

def create(n,originals,normal,shiny,root):
 if n not in MASKED:return None
 images={};overrides={};preserved={}
 muzzle=pointmask([(11,33),(18,31),(24,34),(29,31),(36,33),(41,32),(40,36),(34,40),(23,40),(15,38)])
 for side,im in originals.items():
  out=Image.new('RGBA',(64,64));pix=[];coords=[];protected=[]
  hair=pointmask([(20,22),(22,14),(28,11),(37,11),(43,18),(44,30),(39,33),(36,23),(29,22),(24,24)]) if side=='front' else pointmask([(19,13),(28,11),(38,11),(44,18),(44,31),(36,34),(25,32),(20,26)])
  if n==67:hair=pointmask([(22,12),(38,10),(46,17),(43,31),(38,34),(37,20),(30,19),(27,44),(24,42)]) if side=='front' else pointmask([(20,12),(38,10),(47,17),(45,30),(37,33),(25,31),(20,24)])
  for y in range(64):
   for x in range(64):
    i=im.getpixel((x,y));c=rgb555(shiny[i]);old=rgb555(normal[i]);new=None
    if not i:pix.append((0,0,0,0));continue
    edge=any(not(0<=xx<64 and 0<=yy<64) or not im.getpixel((xx,yy)) for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
    if n==18:
     # Color each metal half; preserve eyes, white muzzle and flame outlines.
     shell=(y<30 and i in {3,4,5,6,7,8,10,11,12}) or (y>=38 and i in {3,4,5,6,7,8,10,11,12})
     if shell:
      blue=(x<32) if side=='front' else (x>=32)
      new=tone((54,133,199) if blue else (202,58,76),i,normal)
     if i in {5,6,7} and side=='front' and 27<=y<37:new=tone((228,232,219),i,normal)
    elif n==51 and i in {6,8,9,10,11}:
     cream=side=='front' and (muzzle.getpixel((x,y)) or (25<=x<=36 and 46<=y<=54))
     new=tone((239,225,194) if cream else (46,46,53),i,normal)
    elif n in (66,67):
     if hair.getpixel((x,y)) and i in ({4,5,6,7,9,12} if n==66 else {2,3,4,7}) and not edge:
      new=rgb555((130,141,166) if luma(normal[i])<.15 else (169,181,204))
     if n==66 and y<19 and i in {1,2,3}:new=tone((206,119,133),i,normal)
     if n==67 and side=='front' and 28<=x<=35 and 23<=y<=35 and i in {6,8,10,11}:new=tone((241,231,210),i,normal)
    elif n==120 and i in {1,3,5,8,9,10,11,12,13}:
     if y<24 and 22<=x<=45:new=tone((184,70,45),i,normal)
     elif y>=24:new=tone((99,123,92),i,normal)
     else:new=tone((214,184,89),i,normal)
    elif n==133:
     # Every mechanical/clothing pixel outside the head keeps its native color.
     new=old;protected.append([x,y])
     if y<32 and i in {1,3,6,7,9,10,12}:
      new=rgb555((164,76,100));protected.pop()
    elif n==145:
     if y<20 and 18<=x<=55 and i in {1,2,3,4,5,8,13}:new=old
     if 34<=y<=48 and 16<=x<=52 and i in {2,3,4}:
      new=rgb555((224,225,213) if i==4 else (171,183,183))
      if side=='front' and 30<=x<=35 and y<44:new=rgb555((37,45,54))
    elif n==150 and side=='front' and 31<=x<=47 and 16<=y<=27 and i in {6,7,8,9,10,11,12,13,14}:
     new=tone((115,167,176),i,normal)
    if new is not None:c=new;coords.append([x,y])
    pix.append((*c,255))
  out.putdata(pix);images[side]=out;overrides[side]=coords;preserved[side]=protected
 # Quantize opaque colors only: transparency is never merged with an outline.
 samples=[c[:3] for a in images.values() for c in a.get_flattened_data() if c[3]];unique=list(dict.fromkeys(samples))
 if len(unique)>15:
  a=Image.new('RGB',(len(samples),1));a.putdata(samples);a=a.quantize(colors=15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
  p=a.getpalette();selected=list(dict.fromkeys(rgb555(p[i*3:i*3+3]) for count,i in a.getcolors()))
 else:selected=unique
 # Terminyanator: normal bike uses14 native colors +one ruby; preserve exactly.
 if n==133:assert len(unique)<=15,(n,len(unique));selected=unique
 palette=[[0,0,0]]+[list(c) for c in selected];palette+=[[0,0,0]]*(16-len(palette));indexed={}
 distance=lambda a,b:sum(w*(u-v)**2 for w,u,v in zip((.21,.72,.07),a,b))
 for side,a in images.items():
  indices=[]
  for c in a.get_flattened_data():
   indices.append(0 if not c[3] else 1+min(range(len(selected)),key=lambda i:distance(c[:3],selected[i])))
  dst=Image.new('P',(64,64));dst.putdata(indices);dst.putpalette(sum(palette,[])+[0]*(768-48));dst.info['transparency']=0
  assert [bool(v) for v in dst.get_flattened_data()]==[bool(v) for v in originals[side].get_flattened_data()]
  if n==133:
   aa=dst.convert('RGBA')
   for x,y in preserved[side]:assert aa.getpixel((x,y))[:3]==rgb555(normal[originals[side].getpixel((x,y))])
  path=root/f'graphics/yokai_shiny_revised/{n:03}';path.mkdir(parents=True,exist_ok=True);dst.save(path/f'{side}.png',transparency=0);indexed[side]=dst
 return indexed,palette,dict(local_color_masks=overrides,preserved_mechanical_pixels=preserved,opaque_colors=len(selected),quantized_without_dither=True)

def build_profiles_and_header(root):
 p=root/'data/yokai/sprite_presentation.json';data=json.loads(p.read_text());original=[v for v in data['profiles'] if not v['id'].startswith('shiny-revised/')];profiles=[];header=['// Generated color-only masks. Geometry copied verbatim from normal profiles.']
 for n in sorted(MASKED):
  for side in ['front','back']:
   for kind in ['display','battle']:
    source=f'graphics/yokai/{n:03}/{side}-{kind}.4bpp';base=next(v for v in original if v['target']==source)
    new=dict(base);new['id']=f'shiny-revised/{n:03}/{side}-{kind}';new['source']=f'graphics/yokai_shiny_revised/{n:03}/{side}.4bpp';new['target']=f'graphics/yokai_shiny_revised/{n:03}/{side}-{kind}.4bpp';new['reason']='Color-mask texture: same silhouette, placement, scale and sampling as normal.';profiles.append(new)
    header.append(f'static const u32 sShinyRevised{n:03}{side}{kind}[] = INCBIN_U32("{new["target"]}.lz");')
 header.append('static const u32 *const sShinyRevisedPictures[152][2][2] = {')
 for n in sorted(MASKED):header.append(f'    [{n}] = {{{{sShinyRevised{n:03}frontdisplay, sShinyRevised{n:03}backdisplay}}, {{sShinyRevised{n:03}frontbattle, sShinyRevised{n:03}backbattle}}}},')
 header.append('};');(root/'src/data/yokai_shiny_revised.h').write_text('\n'.join(header)+'\n');data['profiles']=original+profiles;p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

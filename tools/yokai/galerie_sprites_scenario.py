#!/usr/bin/env python3
"""Build a readable native-pixel review gallery, never modifies source art."""
import json
from PIL import Image,ImageDraw,ImageFont
from convertir_sprites_scenario import ROOT,BASE,PACK
OUT=ROOT/'QA_RECETTE_FINALE/SPRITES_SCENARIO_2026'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
d=json.loads((PACK/'manifest.json').read_text())
actors=[a for a in d['characters'] if (BASE/a['id']/'battle.png').exists()]
actors += [{'id':'enma','name':'Enma royal (carte adaptée)'},{'id':'domniscian','name':'Domniscian (carte adaptée)'}]
out=Image.new('RGB',(1024,((len(actors)+3)//4)*160),(220,228,216));draw=ImageDraw.Draw(out)
for i,a in enumerate(actors):
 x=i%4*256;y=i//4*160;draw.text((x+4,y+4),a['name'],font=font,fill=(20,24,28))
 p=Image.open(BASE/a['id']/'battle.png').convert('RGBA').resize((128,128),Image.Resampling.NEAREST);out.paste(p,(x,y+25),p)
 p=Image.open(BASE/a['id']/'overworld.png').convert('RGBA');w=32 if a['id']=='domniscian' else 16
 for j in range(3):
  f=p.crop((j*w,0,(j+1)*w,32)).resize((w*2,64),Image.Resampling.NEAREST)
  if w==32 and j>0:break
  out.paste(f,(x+160 if w==32 else x+136+j*38,y+62),f)
out.save(OUT/'GALERIE_PERSONNAGES.png')
red=Image.open(ROOT/'graphics/object_events/pics/people/red_normal.png').convert('RGBA')
out=Image.new('RGB',(768,160),(220,228,216));draw=ImageDraw.Draw(out)
for k,n in enumerate(['Red','enma','domniscian']):
 im=red if n=='Red' else Image.open(BASE/n/'overworld.png').convert('RGBA');w=32 if n=='domniscian' else 16
 x=[0,192,384][k];draw.text((x+4,4),n,font=font,fill='black')
 for i in range(3):
  p=im.crop((i*w,0,(i+1)*w,32)).resize((w*3,96),Image.Resampling.NEAREST);out.paste(p,(x+i*(w*3+8),35),p)
out.save(OUT/'COMPARAISON_RED_ANCIENS.png')
print('Generated native sprite review galleries')

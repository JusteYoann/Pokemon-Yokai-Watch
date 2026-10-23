#!/usr/bin/env python3
"""Layout actual unmodified mGBA frames side by side; no generated game scene."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from mgba_rpc import ROOT
D=ROOT/'docs/cramois-ile-passe/phase-a'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for mode in ['public','prive']:
 for filename,cases in [
  ('comparaison-exterieur',[('exterieur','Cramois’Île')]),
  ('comparaison-interieurs',[('centre','Centre'),('laboratoire-fossiles','Laboratoire des fossiles'),('manoir-rdc','Manoir'),('arene','Arène')]),
  ('comparaison-combats',[('nathaniel-portrait','Nathaniel'),('michael-portrait','Michael'),('sauvage-combat','Combat sauvage et interface')]),
 ]:
  canvas=Image.new('RGB',(1000,48+len(cases)*360),(27,24,22));draw=ImageDraw.Draw(canvas)
  draw.text((16,12),'AVANT — version validée',font=font,fill='white');draw.text((512,12),'APRÈS — prototype sépia',font=font,fill='white')
  for row,(stem,label) in enumerate(cases):
   y=48+row*360;draw.text((16,y),label,font=font,fill=(239,218,171))
   for col,version in enumerate(['avant','apres']):
    frame=Image.open(D/mode/version/(stem+'.png')).convert('RGB')
    assert frame.size==(240,160)
    canvas.paste(frame.resize((480,320),Image.Resampling.NEAREST),(16+col*496,y+28))
  canvas.save(D/mode/(filename+'.png'))
print('Native comparison sheets saved')

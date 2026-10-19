#!/usr/bin/env python3
"""Contact sheets only: user mockup / actual before mGBA / actual after mGBA."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[2];q=root/'QA_RECETTE_FINALE/CADRAGE_COMBATS_151';names={int(m['numero_yokai']):m['nom_yokai'] for m in json.loads((root/'data/yokai/noms_affiches.json').read_text())}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for page in range(19):
 nums=list(range(page*8+1,min(page*8+9,152)))
 if not all((q/f'apres/{n:03}.png').exists() for n in nums):continue
 out=q/'comparaisons';out.mkdir(exist_ok=True)
 sheet=Image.new('RGB',(744,len(nums)*184+22),'#dddddd');d=ImageDraw.Draw(sheet)
 for x,label in [(4,'RÉFÉRENCE / maquette'),(252,'AVANT / mGBA'),(500,'APRÈS / mGBA')]:d.text((x,2),label,fill='black',font=font)
 for i,n in enumerate(nums):
  y=22+i*184;d.text((4,y),f'{n:03} — {names[n]}',font=font,fill='black')
  for col,folder in enumerate(['references','avant','apres']):sheet.paste(Image.open(q/f'{folder}/{n:03}.png'),(col*248+4,y+20))
 sheet.save(out/f'comparatif-{page+1:02}.png')

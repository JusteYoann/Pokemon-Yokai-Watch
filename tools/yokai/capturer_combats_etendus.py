#!/usr/bin/env python3
"""Real mGBA enlarged battles and reference / prior engine / enlarged engine sheets."""
import argparse,csv,json
from PIL import Image,ImageDraw,ImageFont
import preparer_cadrage_definitif_151 as t
p=argparse.ArgumentParser();p.add_argument('--species');a=p.parse_args();t.Q=t.ROOT/'QA_RECETTE_FINALE/COMBATS_ETENDUS';(t.Q/'sources').mkdir(exist_ok=True)
if a.species:
 nums=set(map(int,a.species.split(',')));t.NAMES=[m for m in t.NAMES if int(m['numero_yokai']) in nums]
s=t.inventory('apres')
for mon in s['species']:
 for side in ['front','back']:
  mon[side]['generic_active_4bpp']=mon[side]['active_4bpp'];mon[side]['active_4bpp']=f"graphics/yokai/{mon['number']:03}/{side}-battle.4bpp";mon[side]['active_sha256']=t.sha(t.ROOT/mon[side]['active_4bpp'])
s['scope']='Battle-only centered originals. Generic menus retain their previous display assets. Real GBA affine transforms applied by the engine, no composited battle mockup.'
(t.Q/'sources/ETAT_APRES.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');t.capture(s,'apres')
old=t.ROOT/'QA_RECETTE_FINALE/CADRAGE_COMBATS_151';out=t.Q/'comparaisons';out.mkdir(exist_ok=True);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for page in range((len(s['species'])+7)//8):
 batch=s['species'][page*8:page*8+8];sheet=Image.new('RGB',(744,len(batch)*184+22),'#ddd');d=ImageDraw.Draw(sheet)
 for x,label in [(4,'RÉFÉRENCE / maquette'),(252,'AVANT / moteur64px'),(500,'APRÈS / moteur étendu')]:d.text((x,2),label,font=font,fill='black')
 for i,mon in enumerate(batch):
  n=mon['number'];y=22+i*184;d.text((4,y),f"{n:03} — {mon['name']}",font=font,fill='black')
  for c,path in enumerate([old/f'references/{n:03}.png',old/f'apres/{n:03}.png',t.Q/f'apres/{n:03}.png']):sheet.paste(Image.open(path),(c*248+4,y+20))
 sheet.save(out/f'comparatif-{page+1:02}.png')

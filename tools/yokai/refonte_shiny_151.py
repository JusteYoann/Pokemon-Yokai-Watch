#!/usr/bin/env python3
"""Recoloration indexée traçable, sans redessin. Dossier utilisateur du 24/10/2026.
Les groupes sont définis manuellement par espèce, jamais hérités par index.
"""
import csv,hashlib,io,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
DOSSIER=ROOT/'docs/shiny-151-20261024'
Q=DOSSIER/'revision-2'
DATA=ROOT/'data/yokai/shiny-151-20261024'
BASE='903281f4982a4b2e5cbe3d6ac8fc6c4cb47dff08'
def old(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT)
def colors(raw):return [list(map(int,l.split())) for l in raw.decode().splitlines()[3:]]
def palwrite(path,cs):path.write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in cs)+'\n')
def lum(c):return sum(a*b for a,b in zip(c,(.2126,.7152,.0722)))
def rgba(im,pal):
 a=im.copy();a.putpalette(sum(pal,[])+[0]*(768-48));a.info['transparency']=0;return a.convert('RGBA')
def fingerprint(b):return hashlib.sha256(b).hexdigest()
def pupil_split(n,normal):
 # Pupille uniquement : coordonnées dans le dessin 64x64 original. Pas le cerclage.
 im=Image.open(io.BytesIO(old(f'graphics/yokai/{n:03}/front.png'))); before=im.convert('RGBA');mask=[]
 boxes={137:[(28,16,30,18),(44,16,47,18)],138:[(21,20,24,22),(37,20,40,22)]}[n]
 normal[14]=normal[1].copy();normal[15]=normal[3].copy()
 for x0,y0,x1,y1 in boxes:
  for y in range(y0,y1):
   for x in range(x0,x1):
    v=im.getpixel((x,y))
    if v in (1,3):im.putpixel((x,y),14 if v==1 else 15);mask.append([x,y])
 flat=im.getpalette();flat[42:48]=normal[14]+normal[15];im.putpalette(flat);im.save(ROOT/f'graphics/yokai/{n:03}/front.png',transparency=0)
 assert rgba(im,normal).tobytes()==before.tobytes(),('Normal visibly changed',n)
 assert mask
 palwrite(ROOT/f'graphics/yokai/{n:03}/normal.pal',normal)
 return im,mask

def main():
 Q.mkdir(parents=True,exist_ok=True);out=Q/'apercus';out.mkdir(exist_ok=True)
 rows=list(csv.DictReader((DOSSIER/'dossier/PALETTES_151.csv').open(encoding='utf-8-sig')))
 definitions={}
 for line in (DATA/'zones.txt').read_text().splitlines():
  n,raw=line.split('|');groups=[]
  for group in raw.split(';'):
   label,rest=group.split(':');ids,h=rest.split('=');groups.append(dict(zone=label,indices=list(map(int,ids.split(','))),target=[int(h[i:i+2],16) for i in (0,2,4)]))
  definitions[int(n)]=groups
 assert set(definitions)==set(range(1,152))
 results=[];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
 eligible={int(m['number']) for f in json.loads((ROOT/'data/yokai/shiny_families.json').read_text())['families'] if f['shiny_allowed'] for m in f['members']}
 for row in rows:
  n=int(row['number']);normal=colors(old(f'graphics/yokai/{n:03}/normal.pal'));before=normal.copy();mask=[]
  front=Image.open(io.BytesIO(old(f'graphics/yokai/{n:03}/front.png')))
  if n in (137,138):front,mask=pupil_split(n,normal)
  shiny=[c.copy() for c in normal];groups=definitions[n]
  from collections import Counter
  weights=Counter(front.get_flattened_data());weights.update(Image.open(ROOT/f'graphics/yokai/{n:03}/back.png').get_flattened_data())
  from nettoyer_shiny_151 import reviewed
  groups,keep,shiny=reviewed(n,groups,normal,weights,DATA/'revue-151.txt')
  if n in (2,3,55,56):
   donor,indices={2:(3,[4,6,7,8,9,11]),3:(2,[4,6,8,11,12]),55:(56,[6,8,13]),56:(55,[6,7,10])}[n]
   dp=colors(old(f'graphics/yokai/{donor:03}/normal.pal'));ramp=sorted([dp[i] for i in indices],key=lum);ids=sorted(groups[0]['indices'],key=lambda i:lum(normal[i]))
   for j,i in enumerate(ids):shiny[i]=ramp[round(j*(len(ramp)-1)/max(1,len(ids)-1))].copy()
   groups[0]['normal_donor']=donor;groups[0]['donor_indices']=indices
  if n in (137,138):shiny[15]=[188,93,24]
  from masques_shiny_151 import create
  originals={'front':front,'back':Image.open(ROOT/f'graphics/yokai/{n:03}/back.png')}
  localized=create(n,originals,normal,shiny,ROOT)
  extra={}
  if localized:masked_images,shiny,extra=localized
  palwrite(ROOT/f'graphics/yokai/{n:03}/shiny.pal',shiny)
  # Render the actual 15-bit GBA colors, not unrepresentable 24-bit proposals.
  native=lambda cs:[[v>>3<<3 for v in c] for c in cs]
  strip=Image.new('RGB',(1024,292),'#ececec');d=ImageDraw.Draw(strip);d.text((8,3),f"{n:03} {row['name']} — {row['slug']}",fill='black',font=font)
  for j,(side,im) in enumerate([('front',front),('back',Image.open(ROOT/f'graphics/yokai/{n:03}/back.png'))]):
   for k,cs in enumerate([normal,shiny]):
    a=rgba(masked_images[side] if localized and k==1 else im,native(cs));a.save(out/(f'{n:03}-{side}-'+('normal.png' if k==0 else 'shiny.png')))
    a=a.resize((256,256),Image.Resampling.NEAREST);x=(j*2+k)*256;strip.paste(a,(x,36),a);d.text((x+6,20),('Face' if j==0 else 'Dos')+' / '+('NORMAL' if k==0 else 'SHINY'),font=font,fill='black')
  strip.save(out/f'{n:03}-comparaison-x4.png')
  notes=['Palette de 16 entrées, index 0 transparent ; rampes HLS cohérentes, contraste local resserré pour retirer les nuances parasites.','Toutes les nuances utilisées sont classées : zone recolorée ou teinte conservée volontairement. Ombres de chaque zone harmonisées dans sa nouvelle gamme.']
  if n==8:notes.append('Le sprite normal ne porte pas de robe : crème et doré adaptés au corps existant, sans inventer de vêtement.')
  if n==18:notes.append('Masques bleu/rouge de la carrosserie, face et dos ; le visage reste clair.')
  if n==34:notes.append('Mapping confirmé SPECIES_NIDOKING / Métaureau., sprite bovin. Aucun remplacement par Métaurolog.')
  if n in (137,138):notes=['Pupilles seules : réindexation locale vers deux cases libres, couleurs normales strictement conservées. Dos strictement identique.']
  if localized:notes.append('Masques de couleur locaux : zones séparées sans déplacer aucun pixel opaque ni modifier la silhouette ; palette commune face/dos de15 couleurs opaques au maximum.')
  if n==133:notes.append('Tous les pixels mécaniques et vestimentaires hors de la tête conservent exactement leurs couleurs normales RGB555.')
  if n in (53,54):notes.append('Le sprite ne possède pas de bandes régulières : identité rouge/blanc adaptée aux zones existantes, sans dessiner de rayures nouvelles.')
  if n==145:notes.append('Chapeau sombre et blouse claire séparés par masques, indépendamment de la peau bleue.')
  if n==150:notes.append('Référence : autre présentation d’Enma (cheveux clairs, robe violette). Le dessin humain à épée existant est conservé ; seules ses zones sont recolorées.')
  result=dict(masked_texture=bool(localized),mask_details=extra,number=n,name=row['name'],species='SPECIES_'+row['slug'],mode=row['mode'],reference=row['reference'],instruction=row['instruction'],groups=groups,normal_palette=normal,shiny_palette=shiny,eye_pixels=mask,preserved_indices=sorted(keep),all_used_indices_reviewed=True,notes=notes,front=True,back=True,natural_shiny_enabled=n in eligible,normal_front_original_sha256=fingerprint(old(f'graphics/yokai/{n:03}/front.png')),normal_back_sha256=fingerprint((ROOT/f'graphics/yokai/{n:03}/back.png').read_bytes()))
  results.append(result)
 from masques_shiny_151 import build_profiles_and_header
 build_profiles_and_header(ROOT)
 (DATA/'palettes.json').write_text(json.dumps(dict(base_commit=BASE,validation='proposition_non_validee',species=results),ensure_ascii=False,indent=2)+'\n')
 # Twelve cells/page; each has both front/back at nearest x2.
 for page in range(13):
  batch=results[page*12:(page+1)*12];im=Image.new('RGB',(1040,170*((len(batch)+1)//2)),'#ececec');d=ImageDraw.Draw(im)
  for j,rec in enumerate(batch):
   x=8+j%2*520;y=4+j//2*170;n=rec['number'];d.text((x,y),f"{n:03} {rec['name']}",font=font,fill='black')
   for k,(side,kind) in enumerate([('front','normal'),('front','shiny'),('back','normal'),('back','shiny')]):
    d.text((x+k*128,y+18),('Face' if side=='front' else 'Dos')+' '+kind,font=font,fill='black')
    a=Image.open(out/f'{n:03}-{side}-{kind}.png').resize((128,128),Image.Resampling.NEAREST);im.paste(a,(x+k*128,y+36),a)
  im.save(Q/f'planche-{page+1:02}.png')
 # Shinies only: independent readability at native scale and x3, no normal nearby.
 for page in range(10):
  batch=results[page*16:(page+1)*16];im=Image.new('RGB',(1088,174*((len(batch)+3)//4)),'#d8dce2');d=ImageDraw.Draw(im)
  for j,rec in enumerate(batch):
   x=j%4*272;y=j//4*174;n=rec['number'];d.text((x+6,y+4),f"{n:03} {rec['name']}",font=font,fill='#181c25')
   for k,side in enumerate(['front','back']):
    a=Image.open(out/f'{n:03}-{side}-shiny.png').resize((128,128),Image.Resampling.NEAREST);im.paste(a,(x+k*132+4,y+26),a)
  im.save(Q/f'shinies-seuls-{page+1:02}.png')
 report=['# Audit et propositions des 151 palettes','',f'Base : `{BASE}`. Révision2 : toutes les nuances revues. Couleurs seules ; silhouettes et animations conservées. Aucun merge.','',"Les 67 exclusions historiques sont conservées : les 151 palettes sont préparées mais seules 84 espèces peuvent actuellement apparaître shiny. Leur activation globale devra être arbitrée après validation visuelle ; ni taux ni rencontres modifiés.",'', 'Les zones et les teintes sont des propositions manuelles issues des références, quantifiées en RGB555. Les index peuvent réunir plusieurs zones : la validation porte aussi sur ces approximations locales. Les #008, #018 et #150 présentent des limites détaillées ci-dessous.','']
 for rec in results:
  n=rec['number'];name=rec['name'];link=f'apercus/{n:03}-comparaison-x4.png';desc=' ; '.join(f"{g['zone']} : index {','.join(map(str,g['indices']))} → #{''.join(f'{v:02x}' for v in g['target'])}" for g in rec['groups'])
  report += [f'## {n:03} — {name} (`{rec["species"]}`)','',f'[{rec["mode"]} — comparaison face/dos]({link})',f'Source : `{rec["reference"]}`. {rec["instruction"]}','',desc+'.','',*rec['notes'],'']
 (Q/'AUDIT_151.md').write_text('\n'.join(report)+'\n')
 from nettoyer_shiny_151 import write_gallery
 write_gallery(Q,results)
 print('151 palettes et comparaisons face/dos ; 13 planches ; 151 rapports individuels dans AUDIT_151.md')
if __name__=='__main__':main()

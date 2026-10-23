#!/usr/bin/env python3
"""Recoloration indexée traçable, sans redessin. Dossier utilisateur du 24/10/2026.
Les groupes sont définis manuellement par espèce, jamais hérités par index.
"""
import csv,hashlib,io,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
Q=ROOT/'docs/shiny-151-20261024'
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
 Q.mkdir(exist_ok=True);out=Q/'apercus';out.mkdir(exist_ok=True)
 rows=list(csv.DictReader((Q/'dossier/PALETTES_151.csv').open(encoding='utf-8-sig')))
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
  for g in groups:
   ids=g['indices'];assert 0 not in ids and all(0<i<16 for i in ids)
   ordered=sorted(ids,key=lambda i:lum(normal[i]));half=sum(weights[i] for i in ids)/2;total=0;anchor=ordered[-1]
   for i in ordered:
    total+=weights[i]
    if total>=half:anchor=i;break
   maximum=lum(normal[anchor])
   for i in ids:
    if max(normal[i])<40 and n not in (137,138):continue  # Deep outline shared with eye/hair: preserve.
    factor=(lum(normal[i])/maximum)**0.8 if maximum else 1
    shiny[i]=[min(255,round(v*factor)) for v in g['target']]
  if n in (2,3,55,56):
   donor,indices={2:(3,[4,6,7,8,9,11]),3:(2,[4,6,8,11,12]),55:(56,[6,8,13]),56:(55,[6,7,10])}[n]
   dp=colors(old(f'graphics/yokai/{donor:03}/normal.pal'));ramp=sorted([dp[i] for i in indices],key=lum);ids=sorted(groups[0]['indices'],key=lambda i:lum(normal[i]))
   for j,i in enumerate(ids):shiny[i]=ramp[round(j*(len(ramp)-1)/max(1,len(ids)-1))].copy()
   groups[0]['normal_donor']=donor;groups[0]['donor_indices']=indices
  if n in (137,138):shiny[15]=[188,93,24]
  palwrite(ROOT/f'graphics/yokai/{n:03}/shiny.pal',shiny)
  # Render the actual 15-bit GBA colors, not unrepresentable 24-bit proposals.
  native=lambda cs:[[v>>3<<3 for v in c] for c in cs]
  strip=Image.new('RGB',(1024,292),'#ececec');d=ImageDraw.Draw(strip);d.text((8,3),f"{n:03} {row['name']} — {row['slug']}",fill='black',font=font)
  for j,(side,im) in enumerate([('front',front),('back',Image.open(ROOT/f'graphics/yokai/{n:03}/back.png'))]):
   for k,cs in enumerate([normal,shiny]):
    a=rgba(im,native(cs));a.save(out/(f'{n:03}-{side}-'+('normal.png' if k==0 else 'shiny.png')))
    a=a.resize((256,256),Image.Resampling.NEAREST);x=(j*2+k)*256;strip.paste(a,(x,36),a);d.text((x+6,20),('Face' if j==0 else 'Dos')+' / '+('NORMAL' if k==0 else 'SHINY'),font=font,fill='black')
  strip.save(out/f'{n:03}-comparaison-x4.png')
  notes=['Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.','Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.']
  if n==8:notes.append('Le sprite normal ne porte pas de robe : crème et doré adaptés au corps existant, sans inventer de vêtement.')
  if n==18:notes.append('La carrosserie bleue partage ses index : le bicolore rouge/bleu de la référence reste approximatif.')
  if n==34:notes.append('Mapping confirmé SPECIES_NIDOKING / Métaureau., sprite bovin. Aucun remplacement par Métaurolog.')
  if n in (137,138):notes=['Pupilles seules : réindexation locale vers deux cases libres, couleurs normales strictement conservées. Dos strictement identique.']
  if n in (51,66,67,121,133,151):notes.append('Index partagés entre zones : pelage/ventre (#051), cheveux/contours (#066/#067), visage/contours (#121), fourrure/pièces mécaniques (#133), yeux/ornements (#151). Recoloration globale approchée à arbitrer visuellement pour cette espèce.')
  if n in (53,54):notes.append('Le sprite ne possède pas de bandes régulières : identité rouge/blanc adaptée aux zones existantes, sans dessiner de rayures nouvelles.')
  if n==145:notes.append('Le noir du vêtement partage les index du chapeau et des contours : vêtement conservé sombre au lieu de la blouse blanche de la référence, à arbitrer.')
  if n==150:notes.append('Référence : autre présentation d’Enma (cheveux clairs, robe violette). Le dessin humain à épée existant est conservé ; seules ses zones sont recolorées.')
  result=dict(number=n,name=row['name'],species='SPECIES_'+row['slug'],mode=row['mode'],reference=row['reference'],instruction=row['instruction'],groups=groups,normal_palette=normal,shiny_palette=shiny,eye_pixels=mask,notes=notes,front=True,back=True,natural_shiny_enabled=n in eligible,normal_front_original_sha256=fingerprint(old(f'graphics/yokai/{n:03}/front.png')),normal_back_sha256=fingerprint((ROOT/f'graphics/yokai/{n:03}/back.png').read_bytes()))
  results.append(result)
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
 html='''<!doctype html><meta charset="utf-8"><title>151 shiny — propositions à valider</title><style>body{font:16px system-ui;background:#ddd;margin:24px}article{background:#eee;margin:16px 0;padding:12px}img{image-rendering:pixelated;max-width:100%}input{padding:10px;width:350px}details{max-width:1000px}</style><h1>151 shiny : face et dos</h1><p>Propositions à valider. Les images montrent les couleurs GBA, sans redessin. Les taux et les 67 exclusions historiques restent inchangés.</p><input id="q" placeholder="Numéro ou nom" oninput="document.querySelectorAll('article').forEach(a=>a.hidden=!a.textContent.toLowerCase().includes(this.value.toLowerCase()))">'''
 report=['# Audit et propositions des 151 palettes','',f'Base : `{BASE}`. Palette seule, silhouettes et animations conservées. Aucun merge.','',"Les 67 exclusions historiques sont conservées : les 151 palettes sont préparées mais seules 84 espèces peuvent actuellement apparaître shiny. Leur activation globale devra être arbitrée après validation visuelle ; ni taux ni rencontres modifiés.",'', 'Les zones et les teintes sont des propositions manuelles issues des références, quantifiées en RGB555. Les index peuvent réunir plusieurs zones : la validation porte aussi sur ces approximations locales. Les #008, #018 et #150 présentent des limites détaillées ci-dessous.','']
 for rec in results:
  n=rec['number'];name=rec['name'];link=f'apercus/{n:03}-comparaison-x4.png';desc=' ; '.join(f"{g['zone']} : index {','.join(map(str,g['indices']))} → #{''.join(f'{v:02x}' for v in g['target'])}" for g in rec['groups'])
  html+=f'<article><h2>{n:03} {name}</h2><img src="{link}"><details><summary>Source, zones et limites</summary><p>{rec["mode"]} — {rec["reference"]}</p><p>{desc}</p><p>'+ ' '.join(rec['notes'])+'</p></details></article>'
  report += [f'## {n:03} — {name} (`{rec["species"]}`)','',f'[{rec["mode"]} — comparaison face/dos]({link})',f'Source : `{rec["reference"]}`. {rec["instruction"]}','',desc+'.','',*rec['notes'],'']
 (Q/'index.html').write_text(html);(Q/'AUDIT_151.md').write_text('\n'.join(report)+'\n')
 print('151 palettes et comparaisons face/dos ; 13 planches ; 151 rapports individuels dans AUDIT_151.md')
if __name__=='__main__':main()

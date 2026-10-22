#!/usr/bin/env python3
"""Read-only artwork contact sheets and local HTML catalogue; no asset changes."""
import html,json,math,re,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from presentation_4bpp import decode
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'QA_RECETTE_FINALE/GALERIE_SPRITES_2026';OUT.mkdir(exist_ok=True)
BASE=ROOT/'graphics/yokai_characters'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(FONT,14);small=ImageFont.truetype(FONT,11)
manifest=json.loads((BASE/'scenario_2026/manifest.json').read_text())
names={a['id']:a['name'] for a in manifest['characters']}
names.update({'nathan':'Nathan','katie':'Katie','matt':'Matt','wyatt':'Wyatt','ariane':'Ariane','enma':'Enma royal','domniscian':'Domniscian','don_morleone':'Don Morleone','nathaniel':'Nathaniel','michael':'Michael','leo_jibanyan':'Léo / Jibanyan','enma_creature':'Enma (créature)','bingo_kai':'Bingo-kai','capsule_souhait':'Capsule de souhait','triptic_tac':'Triptic-tac','soranaki_phase1':'Soranaki — forme 1','soranaki_phase2':'Soranaki — forme 2'})
def rgba(path):
 im=Image.open(path)
 if im.mode=='P':im.info['transparency']=0
 return im.convert('RGBA')
def binary(path,w,h,pal):
 data=path.read_bytes()[:w*h//2];pixels=decode(data,w,h);b=pal.read_bytes();colors=[]
 for i in range(16):
  v=int.from_bytes(b[i*2:i*2+2],'little');colors.append(tuple(((v>>s)&31)*255//31 for s in [0,5,10])+(255 if i else 0,))
 im=Image.new('RGBA',(w,h));im.putdata([colors[v] for row in pixels for v in row]);return im
actors=[]
order=['nathan','katie','matt','wyatt','ariane','berenice','giraud','alyzon','don_morleone','mafiamille_1','mafiamille_2','mafiamille_3','employe_rouge','employe_bleu','nathaniel','michael','enma_humain','enma','domniscian']
order+= [p.name for p in sorted(BASE.iterdir()) if (p/'overworld.png').exists() and p.name not in order]
for key in order:
 folder=BASE/key;ow=folder/('normal.png' if key in ['nathan','katie'] else 'overworld.png')
 if not ow.exists():continue
 portraits=[p for p in [folder/'front.png',folder/'battle.png',*sorted(folder.glob('battle_*.png'))] if p.exists() and p.name!='battle_large.png']
 actors.append({'name':names.get(key,key.replace('_',' ').title()),'ow':ow,'portraits':portraits})
for p,name in [(BASE/'ariane/usapion_overworld.png','Usapion'),(BASE/'enma/kyubi_overworld.png','Kyubi'),*[(p,p.parent.name.title()) for p in sorted((BASE/'static_yokai').glob('*/overworld.png'))]]:
 actors.append({'name':name,'ow':p,'portraits':[]})
def map_image(a):
 p=a['ow'];im=rgba(p)
 if p.parent.name in ['domniscian','leo_jibanyan','enma_creature'] or 'static_yokai' in str(p) or p.stem in ['usapion_overworld','kyubi_overworld'] or p.parent.name in ['bingo_kai','triptic_tac']:w=32
 else:w=16
 h=min(32,im.height)
 # Only two historical assets use display transforms on the map.
 display=p.with_name(p.stem+'-display.4bpp')
 if display.exists():
  pal=p.parent/('normal.gbapal' if p.parent.name=='leo_jibanyan' else 'overworld.gbapal')
  return [binary(display,w,h,pal)]
 if im.width==w and im.height>h:return [im.crop((0,j*h,w,(j+1)*h)) for j in range(min(3,im.height//h))]
 return [im.crop((j*w,0,(j+1)*w,h)) for j in range(min(3,im.width//w))]
pages=[];records=[]
for start in range(0,len(actors),16):
 group=actors[start:start+16];canvas=Image.new('RGB',(1440,50+180*math.ceil(len(group)/4)),(228,234,225));d=ImageDraw.Draw(canvas)
 d.text((12,10),'PERSONNAGES — portraits et carte (pixels agrandis ×2)',font=f,fill='#15271c')
 for i,a in enumerate(group):
  x=i%4*360;y=50+i//4*180;d.text((x+8,y+2),a['name'],font=f,fill='#15271c')
  if a['portraits']:
   im=rgba(a['portraits'][0]).resize((128,128),Image.Resampling.NEAREST);canvas.paste(im,(x+4,y+28),im)
  for j,im in enumerate(map_image(a)):
   im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);canvas.paste(im,(x+138+j*(im.width+5),y+70),im)
  d.text((x+8,y+158),'Portrait + carte' if a['portraits'] else 'Carte / objet',font=small,fill='#42534a')
 name=f'personnages-{len(pages)+1:02}.png';canvas.save(OUT/name);pages.append(name)
for a in actors:
 records.append({'name':a['name'],'map':str(a['ow'].relative_to(ROOT)),'portraits':[str(p.relative_to(ROOT)) for p in a['portraits']]})
# Select exact build-time display textures from the linked C registry.
registry=(ROOT/'src/data/graphics/pokemon.h').read_text()
linked={}
for number,kind,path in re.findall(r'graphics/yokai/(\d{3})/(front|back)([^"\n]*)',registry):
 linked[(number,kind)]=ROOT/f'graphics/yokai/{number}/{kind}{path}'.removesuffix('.lz')
yokai=json.loads((ROOT/'data/yokai/noms_affiches.json').read_text());creature_pages=[]
for start in range(0,len(yokai),24):
 group=yokai[start:start+24];canvas=Image.new('RGB',(1120,48+178*math.ceil(len(group)/4)),(228,234,225));d=ImageDraw.Draw(canvas)
 d.text((12,10),'YO-KAI — normal : face / dos ; chromatique : face / dos',font=f,fill='#15271c')
 for i,a in enumerate(group):
  num=a['numero_yokai'].zfill(3);folder=ROOT/f'graphics/yokai/{num}';x=i%4*280;y=48+i//4*178
  d.text((x+7,y),f'{num}  {a["nom_affiche_gba"]}',font=f,fill='#15271c')
  for j,(kind,palette) in enumerate([('front','normal'),('back','normal'),('front','shiny'),('back','shiny')]):
   im=binary(linked[(num,kind)],64,64,folder/f'{palette}.gbapal');canvas.paste(im,(x+6+j*68,y+32),im)
  d.text((x+7,y+112),'Textures liées ; taille native 64×64',font=small,fill='#42534a')
 name=f'yokai-{len(creature_pages)+1:02}.png';canvas.save(OUT/name);creature_pages.append(name)
styles='body{background:#17231f;color:#e4eae1;font:16px system-ui;margin:24px auto;max-width:1160px;padding:16px}a{color:#94dcab}img{image-rendering:pixelated;max-width:100%}article{background:#e4eae1;color:#15271c;border-radius:8px;padding:16px;margin:16px 0}.sheet{width:100%}.asset{min-height:64px;max-width:100%;vertical-align:middle;margin:12px}h1,h2{line-height:1.3}'
def asset(p):
 target=OUT/'assets'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target);return 'assets/'+str(p.relative_to(ROOT))
parts=['<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Sprites — Poket Monster</title><style>'+styles+'</style><h1>Sprites actuels — Yo-kai Watch: Poket Monster</h1>',f'<p>{len(actors)} ensembles de personnages, créatures de carte et objets ; 151 Yo-kai de combat. Ressources existantes, sans redessin. Leur présence ici ne garantit pas que tous leurs événements sont déjà jouables.</p><p><a href="#personnages">Personnages</a> · <a href="#details">Feuilles et variantes</a> · <a href="#yokai">151 Yo-kai</a></p><h2 id="personnages">Personnages et objets</h2>']
for p in pages:parts.append(f'<a href="{p}"><img class="sheet" src="{p}"></a>')
parts.append('<h2 id="details">Feuilles complètes et variantes de portraits</h2><p>Les feuilles montrent les poses disponibles dans les PNG sources. Les planches ci-dessus appliquent aussi les dérivés de présentation de Léo et Usapion. Les portraits de Soranaki sont les aperçus 64×64 ; ses maîtres 128×128 sont accessibles ci-dessous. Les textures de combat ne reproduisent pas les transformations matérielles du moteur.</p>')
for a in actors:
 parts.append('<article><h3>'+html.escape(a['name'])+'</h3>')
 extras=[]
 if a['ow'].parent.name in ['nathan','katie','matt']:
  extras=[p for p in sorted(a['ow'].parent.glob('*.png')) if p not in [a['ow'],*a['portraits']] and 'preview' not in p.stem]
 for p in [a['ow'],*a['portraits'],*extras]:
  rel=asset(p);parts.append(f'<a href="{rel}"><img class="asset" src="{rel}" alt="{html.escape(p.name)}"></a>')
 large=a['ow'].parent/'battle_large.png'
 if large.exists():parts.append(f'<p><a href="{asset(large)}">Maître de boss 128×128</a></p>')
 parts.append('</article>')
parts.append('<h2 id="yokai">Les 151 Yo-kai — normal et chromatique, face et dos</h2><p>Textures de présentation sélectionnées par le registre actif de compilation, décodées avec leurs palettes GBA. Pas une capture d’un combat ni une validation artistique.</p>')
for p in creature_pages:parts.append(f'<a href="{p}"><img class="sheet" src="{p}"></a>')
parts.append('</html>');(OUT/'index.html').write_text('\n'.join(parts)+'\n')
(OUT/'INVENTAIRE.json').write_text(json.dumps({'characters_and_objects':records,'pokemon_species':151,'character_sheets':pages,'creature_sheets':creature_pages,'scope':'Current project artwork, not narrative integration or artistic approval'},ensure_ascii=False,indent=2)+'\n')
print(f'{len(actors)} character/object sets, {len(pages)} character sheets, 151 species, {len(creature_pages)} creature sheets')

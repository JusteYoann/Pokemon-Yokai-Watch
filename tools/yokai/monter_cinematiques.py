#!/usr/bin/env python3
"""Montage chronologique à vitesse 1, audio natif ; coupes documentées des combats."""
import concurrent.futures,hashlib,json,subprocess,sys,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];D=R/'docs/cinematiques-compilation-20261025';W=D/'montage-travail';W.mkdir(exist_ok=True)
items=[
('00-titre-introduction','Titre et présentation du monde'),
('01-chen-depart','Le professeur Chen vient chercher Nathan'),
('01b-choix-partenaire','Le choix du premier partenaire'),
('01c-matt-laboratoire','Premier défi de Matt'),
('01d-medallium','Le colis et le Médallium'),
('01e-tutoriel-capture','La démonstration de capture'),
('02b-matt-route22','Matt sur la Route 22'),
('02-argenta','Le discours de Don Morléone, avec Wyatt'),
('arene-01','Wyatt : premier Badge'),
('02d-chaussures','Le cadeau du professeur Chen'),
('02e-fossiles','Le conflit autour des fossiles au Mont Sélénite'),
('02c-matt-azuria','Retrouvailles avec Matt à Azuria'),
('arene-02','Le deuxième Badge'),
('23-leo-transformation','Léo et son problème de transformation'),
('23b-leo-separateur','Le séparateur de Léo'),
('03b-matt-oceane','Matt à bord de l’Océane'),
('03c-capitaine','Le capitaine de l’Océane'),
('03d-depart-oceane','Le départ de l’Océane'),
('03-ariane-rencontre','La rencontre avec Ariane'),
('04-enquete-entrepot','La Pierre Philosovni : enquête dans l’entrepôt'),
('arene-03','Ariane : le Badge Foudre'),
('05-zombie-night','Lavanville : la Zombie Night et Alizon Bie'),
('arene-04','Alizon Bie au sommet de la Tour'),
('24-repaire-morleone','Don Morléone dans le repaire'),
('07b-matt-yopple','Matt dans les bureaux de Yopple'),
('07-yopple-liberation','La libération de Yopple'),
('arene-05','Bérénice : le cinquième Badge'),
('arene-06','Domniscian : le sixième Badge'),
('06-cramois-rencontre','Cramois’Île et la rencontre avec Nathaniel'),
('28-depart-sevii','Le départ pour les Îles Sevii'),
('28b-motards-argument','Les motards sur l’Île 3'),
('28c-motards-depart','La fin des troubles sur l’Île 3'),
('27-perdue-sauvetage','Le sauvetage de la petite fille dans la forêt'),
('29-retour-sevii','Le retour des Îles Sevii'),
('arene-08','Le dernier Badge'),
('07c-matt-route22','Le dernier défi de Matt avant la Ligue'),
('conseil-01','Conseil 4 : premier adversaire'),
('conseil-02','Conseil 4 : deuxième adversaire'),
('conseil-03','Conseil 4 : Zazel'),
('conseil-04','Conseil 4 : Maître Nyada'),
('08-finale','Don Morléone, fusion, Don Spiration et fin de l’histoire'),
('10-enma-postgame','Le Seigneur Enma après la Ligue'),
('10b-chen-jibanyan','Le cadeau postgame du professeur Chen'),
('26-lorelei-grotte','L’intervention dans la Grotte de Glace'),
('34-celio-rubis','Le Rubis et le Passe Prisme'),
('30-saphir-vol','Le vol du Saphir'),
('31-entrepot-admin1','L’entrepôt de la Mafiamille : premier administrateur'),
('32-entrepot-admin2','L’entrepôt de la Mafiamille : second administrateur'),
('33-entrepot-scientifique','La récupération du Saphir'),
('35-celio-saphir','Le Saphir et la machine réseau'),
('11-nyada-premiere-quete','Maître Nyada : la première quête'),
('12-nyada-retour-amis','Le retour auprès de Maître Nyada'),
('13-alizon-quete-oni','Alizon Bie et le Short Oni'),
('terre-heure-complete','La Terr’heure : activation et porte de sortie'),
('14-alizon-rendez-vous','Les trois Oni vaincus : le rendez-vous'),
('gorgouille','Gorgouille : arrivée d’Alizon, capture et départ'),
('16-nyada-seconde-quete','Maître Nyada : la seconde quête'),
('17-demophage','L’endormissement, Démophage et la récompense'),
('18-nyada-sommet','Maître Nyada au sommet de la Tour'),
('19-scientifique-lavanville','Le scientifique : Lavanville'),
('20-scientifique-carmin','Le scientifique : Carmin sur Mer'),
('21-scientifique-yopple','Le scientifique : Yopple et Robonyan 28 shiny'),
('25-champion-don-exil','Don Morléone en exil'),
('21b-chen-invitation','Médallium rempli : l’invitation de Juste Yoann'),
('22-yoann','Juste Yoann, THANK FOR PLAY, crédits et Charme Chroma'),
]
def source(name):
 if name=='gorgouille':return R/'docs/gorgouille-alizon-20261025/gorgouille-arrivee-capture-depart-mgba.mp4'
 if name=='terre-heure-complete':return D/name/'declenchement-porte-sortie-mgba.mp4'
 return D/(name+'.mp4')
def duration(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True))
def ranges(name,p,data):
 total=duration(p);cuts=[]
 if name=='terre-heure-complete':
  ev=data['evenements_secondes'] if 'evenements_secondes' in data else data.get('evenements',{})
  # Keep the transformation and the complete exit scene; ordinary exploration is cut.
  end=ev.get('exploration');door=ev.get('interaction_porte')
  if end is None or door is None:raise ValueError(('Événements Terr’heure manquants',data.keys()))
  return [(0,min(total,end+2)),(max(end+2,door-3),total)]
 if name=='gorgouille':return [(0,total)]
 events=[e for e in data.get('events',[]) if 'callback' in e]
 # A battle may temporarily open the party menu. Keep the entire interval
 # grouped until the native return-to-field callback, rather than leaking menus.
 battle=None
 for e in events:
  cb=e['callback'];t=e['seconds']
  if cb=='CB2_InitBattle' and battle is None:battle=t
  if battle is not None and (cb.startswith('CB2_ReturnToField') or cb=='CB2_Overworld'):
   if t-battle>14:cuts.append((battle+10,t))
   battle=None
 result=[];at=0
 for a,b in cuts:
  if a>at:result.append((at,a))
  at=b
 if total>at:result.append((at,total))
 return result

def metadata(name,p):
 if name=='terre-heure-complete':return json.loads((p.parent/'ENREGISTREMENT_SORTIE.json').read_text())
 return json.loads(p.with_suffix('.json').read_text())
def make(item):
 index,(name,title)=item;p=source(name);out=W/f'{index:02}-{name}.mp4'
 if not p.exists():return None
 try:data=metadata(name,p)
 except FileNotFoundError:return None
 if out.exists() and out.stat().st_mtime>p.stat().st_mtime:return out
 keep=ranges(name,p,data)
 img=Image.new('RGB',(720,480),'#101828');draw=ImageDraw.Draw(img)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
 small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
 draw.text((360,135),f'YO-KAI WATCH GBA — {index+1:02}',font=small,anchor='mm',fill='#91c991')
 for n,line in enumerate(textwrap.wrap(title,38)):draw.text((360,208+n*38),line,font=font,anchor='mm',fill='white')
 draw.text((360,365),'Cinématiques à vitesse normale • Son du jeu',font=small,anchor='mm',fill='#c0c6d0')
 card=W/f'{index:02}.png';img.save(card)
 filters=['[1:v]trim=duration=2,setpts=PTS-STARTPTS,fps=30,format=yuv420p[v0]','anullsrc=r=48000:cl=stereo,atrim=duration=2[a0]'];tags=['[v0][a0]']
 for i,(a,b) in enumerate(keep,1):
  filters += [f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{i}]',f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aresample=48000[a{i}]'];tags.append(f'[v{i}][a{i}]')
 filters.append(''.join(tags)+f'concat=n={len(tags)}:v=1:a=1[v][a]')
 log=W/f'{index:02}.log'
 with log.open('w') as f:subprocess.run(['ffmpeg','-nostats','-v','warning','-y','-i',str(p),'-loop','1','-framerate','30','-i',str(card),'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-threads','2','-preset','veryfast','-crf','29','-c:a','aac','-b:a','80k','-ar','48000','-ac','2','-video_track_timescale','15360',str(out)],stdout=f,stderr=f,check=True)
 (W/f'{index:02}-{name}.json').write_text(json.dumps(dict(name=name,title=title,source=str(p.relative_to(R)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rom_sha256=data['rom_sha256'],retained_source_intervals=keep,seconds=duration(out)),ensure_ascii=False,indent=2)+'\n')
 print('MONTÉ',index+1,name,round(duration(out)),flush=True);return out
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(make,enumerate(items)))
if '--prepare' in sys.argv:
 print('PRÉPARÉS',sum(p is not None for p in results),'/',len(items));sys.exit()
assert all(results),[items[i][0] for i,p in enumerate(results) if p is None]
chapters=[];at=0
for index,(name,title) in enumerate(items):
 data=json.loads((W/f'{index:02}-{name}.json').read_text());chapters.append(dict(start_seconds=at,**data));at+=data['seconds']
(D/'CHAPITRES.json').write_text(json.dumps(dict(speed=1,native_audio=True,chapters=chapters),ensure_ascii=False,indent=2)+'\n')
ffmeta=[';FFMETADATA1','title=Yo-kai Watch GBA — Cinématiques de l’histoire et du postgame']
for ch in chapters:
 ffmeta+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(ch['start_seconds']*1000)}",f"END={round((ch['start_seconds']+ch['seconds'])*1000)}",'title='+ch['title'].replace('=','\\=')]
(W/'chapitres.ffmeta').write_text('\n'.join(ffmeta)+'\n')
(W/'concat.txt').write_text(''.join("file '"+p.name+"'\n" for p in results))
subprocess.run(['ffmpeg','-nostats','-v','warning','-y','-f','concat','-safe','0','-i',str(W/'concat.txt'),'-i',str(W/'chapitres.ffmeta'),'-map_metadata','1','-map_chapters','1','-c:v','copy','-c:a','aac','-b:a','80k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(D/'cinematiques-histoire-et-postgame.mp4')],check=True)
print('COMPILATION',at,len(items),flush=True)

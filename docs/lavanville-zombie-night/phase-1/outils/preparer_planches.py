#!/usr/bin/env python3
"""Format GENERATED PROTOTYPES for scale/palette evaluation; not production sprite authoring.
Technical extraction, binary alpha, nearest-neighbour scale, indexed GBA palette.
The prototypes need manual pixel review before any engine integration.
"""
from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib,shutil
D=Path(__file__).resolve().parents[1];P=D/'prototypes';S=P/'sources';S.mkdir(exist_ok=True);N=P/'natifs';N.mkdir(exist_ok=True)
sources={'zombies-initial':'exec-cff26bed-03ac-4f65-b3d0-bf1a6180111c.png','dresseurs':'exec-c7147e22-71c0-4115-8b98-32c4f15d49d5.png','alyzon':'exec-54ea39f4-a296-4dd0-9516-ffebf5dad1fc.png','zombies-nouvelle-base':'exec-1a98c4b6-a6ec-49ac-9451-037ea4a9318d.png','zombies-frlg-face':'exec-4fa0deba-1b4c-468a-80a2-468a7991779d.png'}
for k,f in sources.items():
 source=Path('/workspace/generated_images')/f
 if source.exists():shutil.copyfile(source,S/(k+'.png'))
 else:assert (S/(k+'.png')).exists(),k
records=[]
def region(src,box):
 im=Image.open(S/(src+'.png')).convert('RGBA').crop(box)
 a=im.getchannel('A').point(lambda v:255 if v>=240 else 0);im.putalpha(a);bbox=a.getbbox();assert bbox,(src,box)
 return im.crop(bbox)
def native(im,name,canvas=(32,32),limit=(24,28)):
 im.thumbnail(limit,Image.Resampling.NEAREST)
 # Palette entries use representable RGB555 values. No dithering or partial alpha.
 alpha=im.getchannel('A');rgb=im.convert('RGB').point(lambda x:(x>>3)<<3);q=rgb.quantize(colors=15,dither=Image.Dither.NONE)
 pal=[(v>>3)<<3 for v in q.getpalette()[:45]];out=Image.new('P',canvas,0);out.putpalette(([0,0,0]+pal+[0]*768)[:768]);out.info['transparency']=0
 dx=(canvas[0]-im.width)//2;dy=canvas[1]-im.height-(1 if canvas==(32,32) else 0)
 for y in range(im.height):
  for x in range(im.width):
   if alpha.getpixel((x,y)):out.putpixel((dx+x,dy+y),q.getpixel((x,y))+1)
 out.save(N/(name+'.png'),transparency=0)
 rgba=out.convert('RGBA');records.append(dict(file='natifs/'+name+'.png',canvas=list(canvas),silhouette=list(rgba.getbbox()),opaque_colors=len({p[:3] for p in rgba.getdata() if p[3]}),alpha_binary=True,method='Generated concept extracted and NEAREST fitted as PROTOTYPE ONLY; not manually pixel-finalized'))
 return rgba
z=[];dirs=['face','dos','droite','gauche'];variants=['errant','sprinteur','colosse','spectral']
for row in range(4):
 for col,v in enumerate(variants):
  im=region('zombies-nouvelle-base',(round(col*1086/4),[50,420,748,1052][row],round((col+1)*1086/4),[414,744,1048,1410][row]));z.append(native(im,f'{v}-{dirs[row]}',limit=((26 if col==2 else 20),28)))
tr=[];tn=['clochemar','zomgralos','zombigo-t','supermanager','king-deadward','encore-dead']
for row in range(2):
 for col,v in enumerate(tn):
  im=region('dresseurs',(col*362,row*362,(col+1)*362,(row+1)*362));tr.append(native(im,v+('-ow-face' if row==0 else '-portrait'),canvas=(32,32) if row==0 else (64,64),limit=(26,28) if row==0 else (62,62)))
al=[]
for i,(x1,x2) in enumerate([(320,635),(635,900),(900,1200)]):al.append(native(region('alyzon',(x1,0,x2,315)),['alyzon-face','alyzon-dos','alyzon-gauche'][i],limit=(20,28)))
for i,(x1,x2) in enumerate([(300,770),(790,1280)]):al.append(native(region('alyzon',(x1,320,x2,1010)),f'alyzon-portrait-{i+1}',canvas=(64,64),limit=(58,62)))
frlg=[]
for col,v in enumerate(variants):
 im=region('zombies-frlg-face',(round(col*2172/4),0,round((col+1)*2172/4),724))
 frlg.append(native(im,v+'-frlg-face',limit=(18,20) if col==2 else (14,19)))
zb=[]
for col,v in enumerate(variants):zb.append(native(region('zombies-initial',(col*384,470,(col+1)*384,1000)),v+'-combat',canvas=(64,64),limit=(62,62)))
def sheet(filename,items,cols,cell):
 rows=(len(items)+cols-1)//cols;im=Image.new('RGBA',(cols*cell[0],rows*cell[1]),(0,0,0,0))
 for i,p in enumerate(items):im.alpha_composite(p,((i%cols)*cell[0]+(cell[0]-p.width)//2,(i//cols)*cell[1]+cell[1]-p.height))
 im.save(P/(filename+'-natif.png'));im.resize((im.width*6,im.height*6),Image.Resampling.NEAREST).save(P/(filename+'-x6.png'));return im
red=Image.open(D/'prototypes/gabarit-frlg-natif.png').convert('RGBA');redbox=Image.new('RGBA',(32,32));redbox.alpha_composite(red,(8,0))
sheet('FRLG-comparaison-red', [redbox]+frlg,5,(32,32));sheet('zombies-frlg-face',frlg,4,(32,32));
sheet('zombies-overworld',z,4,(32,32));sheet('zombies-combat',zb,4,(64,64));sheet('dresseurs-overworld',tr[:6],6,(32,32));sheet('dresseurs-portraits',tr[6:],6,(64,64));sheet('alyzon-overworld',al[:3],3,(32,32));sheet('alyzon-portraits',al[3:],2,(64,64))
# Presentation composites, explicitly named MONTAGE. None are engine integrations.
base=Image.open(P/'mgba-nuit-brume-ram.png').convert('RGBA')
for i,sp in enumerate(frlg):base.alpha_composite(sp,[(103,12),(134,32),(166,12),(197,58)][i])
base.save(P/'MONTAGE-zombies-sur-carte-natif.png');base.resize((960,640),Image.Resampling.NEAREST).save(P/'MONTAGE-zombies-sur-carte-x4.png')
for label,group in [('dresseurs',tr[6:]),('zombies',zb),('alyzon',al[3:])]:
 panels=[]
 for sp in group:
  base=Image.open(P/'mgba-combat-fond-fixture.png').convert('RGBA');base.alpha_composite(sp,(144,16));panels.append(base)
 sheet('MONTAGE-'+label+'-combat',panels,2,(240,160))
(D/'controle-graphique.json').write_text(json.dumps(dict(status='PROTOTYPES TO REVIEW, NOT FINAL ASSETS',source_method='Image generation from supplied artwork and revised CraftPix visual base; extraction and palette fitting for native-size evaluation. Native samples are not advertised as pixel-authored production sprites.',records=records),ensure_ascii=False,indent=2)+'\n')
# Review page includes explicit labels and pixelated CSS, no misleading screenshots.
html='''<!doctype html><meta charset="utf-8"><title>Lavanville — phase 1</title><style>body{background:#181a28;color:#eee;font:18px system-ui;max-width:1200px;margin:2em auto}img{image-rendering:pixelated;max-width:100%}figure{background:#33354a;padding:20px}a{color:#9dd}</style><h1>Lavanville : propositions à valider</h1><p>Aucune intégration au jeu. Les sprites ci-dessous sont des prototypes issus des planches générées, préparés pour évaluer leur silhouette et leur palette à petite échelle. Retouches au pixel et animations restent à réaliser après choix.</p>'''
for title,f in [('Nouvelle piste FRLG : Red puis errant, sprinteur, colosse, spectral — pieds alignés, échelle corrigée','FRLG-comparaison-red-x6.png'),('FRLG : comparaison à résolution native','FRLG-comparaison-red-natif.png'),('Étude précédente, trop haute : face / dos / droite / gauche à reprendre','zombies-overworld-x6.png'),('Zombies : résolution native, transparence','zombies-overworld-natif.png'),('Montage des quatre variantes sur carte : PAS une capture d’intégration','MONTAGE-zombies-sur-carte-x4.png'),('Six Dresseurs : prototypes overworld','dresseurs-overworld-x6.png'),('Six Dresseurs : portraits 64 × 64 candidats','dresseurs-portraits-x6.png'),('Alyzon : trois vues candidates','alyzon-overworld-x6.png'),('Alyzon : deux poses de portrait candidates','alyzon-portraits-x6.png'),('Capture réelle mGBA : nuit et météo natives, palettes temporaires en RAM','mgba-nuit-brume-ram-x4.png'),('Capture réelle mGBA : brume animée, ROM inchangée','mgba-brume-ram.gif'),('Montages des portraits dans une interface de combat : PAS des captures d’intégration','MONTAGE-dresseurs-combat-x6.png')]:
 html+=f'<h2>{title}</h2><figure><img src="prototypes/{f}" alt="{title}"></figure>'
html+='<p>Lire <a href="RAPPORT.md">le rapport technique</a>, <a href="DIALOGUES.md">les dialogues proposés</a> et <a href="EQUIPES.md">les équipes proposées</a>. Originaux officiels fournis conservés hors dépôt, sans licence de redistribution présumée. La base CraftPix n’est pas extraite du pack commercial.</p>'
(D/'galerie.html').write_text(html)
print('Prepared',len(records),'candidate frames; binary alpha and <=15 colors checked.')

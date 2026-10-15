#!/usr/bin/env python3
"""Render a self-contained QA gallery from actual GBA resources. Requires Pillow.
Default: render from the published compact snapshot. --refresh: export current integrated game assets first.
Never writes game sources, palettes, sprite positions or ROM files.
"""
import argparse, pathlib, json, zipfile, hashlib, re, struct, zlib, subprocess, shutil, math
from PIL import Image, ImageDraw, ImageFont
HERE=pathlib.Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
P=argparse.ArgumentParser();P.add_argument('--refresh',action='store_true');A=P.parse_args()
def sha(data):return hashlib.sha256(data).hexdigest()
def unlz(data):
 if data[0]!=0x10:raise ValueError('Not GBA LZ77')
 size=int.from_bytes(data[1:4],'little');out=bytearray();pos=4
 while len(out)<size:
  flags=data[pos];pos+=1
  for bit in range(7,-1,-1):
   if len(out)>=size:break
   if flags&(1<<bit):
    a,b=data[pos:pos+2];pos+=2;length=(a>>4)+3;distance=((a&15)<<8|b)+1;assert distance<=len(out)
    for _ in range(length):
     out.append(out[-distance])
     if len(out)==size:break
   else:out.append(data[pos]);pos+=1
 return bytes(out)
def indices(raw,w,h):
 assert len(raw)==w*h//2 and w%8==h%8==0;out=bytearray(w*h)
 for y in range(h):
  for x in range(w):
   offset=((y//8)*(w//8)+x//8)*32+(y%8)*4+(x%8)//2;out[y*w+x]=(raw[offset]>>(4*(x%2)))&15
 return bytes(out)
def colors(raw):
 assert len(raw)==32;result=[]
 for v, in struct.iter_unpack('<H',raw):
  rgb=[(v>>s)&31 for s in (0,5,10)];result.append(tuple((c<<3)|(c>>2) for c in rgb))
 return result
def rgba(data,palette,w,h):
 out=Image.new('RGBA',(w,h));out.putdata([(*palette[i],255 if i else 0) for i in data]);return out
if A.refresh:
 m=json.loads((ROOT/'docs/yokai-graphics/manifest.json').read_text())['entries']+json.loads((ROOT/'docs/yokai-graphics/wave2/manifest.json').read_text())['entries'];m.sort(key=lambda e:e['index']);assert [e['index'] for e in m]==list(range(1,152))
 originals=[p for p in (ROOT/'graphics/yokai').rglob('*') if p.is_file()]+[ROOT/p for p in ['src/data/graphics/pokemon.h','src/pokemon_icon.c','src/data/pokemon_graphics/front_pic_coordinates.h','src/data/pokemon_graphics/back_pic_coordinates.h','src/data/pokemon_graphics/enemy_mon_elevation.h','pokefirered.gba']];before={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in originals}
 inc=(ROOT/'src/data/graphics/pokemon.h').read_text();icon=(ROOT/'src/pokemon_icon.c').read_text().split('const u8 gMonIconPaletteIndices',1)[1]
 nm=shutil.which('arm-none-eabi-nm') or str(ROOT.parent/'.setup/sysroot/usr/bin/arm-none-eabi-nm');symbols={}
 for line in subprocess.check_output([nm,'-S','--defined-only','pokefirered.elf'],cwd=ROOT).decode().splitlines():
  f=line.split()
  if len(f)==4:
   try:symbols[f[3]]=int(f[0],16)
   except ValueError:pass
 rom=(ROOT/'pokefirered.gba').read_bytes();records=[];payload={};verified=0
 for e in m:
  n=e['index'];rec={'index':n,'name':e['yokai'],'species_id':e['species_id'],'constant':e['species_constant'],'resources':{},'positions':{}}
  for kind,sym in e['symbols'].items():
   path=re.search(r'const \w+ '+re.escape(sym)+r'\[\] = INCBIN_\w+\(\s*"([^"]+)"',inc)[1];packed=(ROOT/path).read_bytes();offset=symbols[sym]-0x08000000;assert 0<=offset<len(rom) and rom[offset:offset+len(packed)]==packed
   raw=unlz(packed) if path.endswith('.lz') else packed;filename=f'{n:03}/'+{'front':'front.4bpp','back':'back.4bpp','icon':'icon.4bpp','footprint':'footprint.1bpp','normal':'normal.gbapal','shiny':'shiny.gbapal'}[kind];payload[filename]=raw;rec['resources'][kind]={'snapshot':filename,'engine_path':path,'symbol':sym,'rom_offset':offset,'sha256':sha(raw)};verified+=1
   if kind in ['front','back','icon']:
    w,h=(32,64) if kind=='icon' else (64,64);decoded=indices(raw,w,h)
    with Image.open(ROOT/e['active_sources'][kind]) as src:src.load();assert src.mode=='P' and src.size==(w,h) and bytes(src.get_flattened_data())==decoded,(n,kind)
   elif kind in ['normal','shiny']:
    lines=(ROOT/e['active_sources'][kind]).read_text().splitlines();rgb=[tuple(map(int,l.split())) for l in lines[3:19]];expected=b''.join(struct.pack('<H',(r>>3)|((g>>3)<<5)|((b>>3)<<10)) for r,g,b in rgb);assert raw==expected
  pi=int(re.search(r'\['+e['species_constant']+r'\]\s*=\s*(\d+)',icon)[1]);assert pi in range(3);payload[f'icons/palette-{pi}.gbapal']=(ROOT/f'graphics/pokemon/icon_palettes/icon_palette_{pi}.gbapal').read_bytes();rec['icon_palette_index']=pi
  for side in ['front','back']:
   t=(ROOT/f'src/data/pokemon_graphics/{side}_pic_coordinates.h').read_text();rec['positions'][side]=re.search(r'\['+e['species_constant']+r'\]\s*=\s*\{(.*?)\}',t,re.S)[1].strip()
  records.append(rec)
 assert verified==906 and all((ROOT/p).is_file() and sha((ROOT/p).read_bytes())==h for p,h in before.items())
 manifest={'species':records,'resource_count':verified,'rom_sha256':sha(rom),'rgb555_expansion':'bit replication (v << 3) | (v >> 2)','icon_frame':0,'preserved_game_files':len(before)}
 (HERE/'sources').mkdir(exist_ok=True)
 with zipfile.ZipFile(HERE/'sources/gba-graphics.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for filename,data in sorted(payload.items()):z.writestr(filename,data)
  z.writestr('manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
 (HERE/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(HERE/'sources/gba-graphics.zip') as z:
 assert z.testzip() is None;manifest=json.loads(z.read('manifest.json'));records=manifest['species'];assert [e['index'] for e in records]==list(range(1,152)) and len({e['name'] for e in records})==151
 images={}
 for e in records:
  n=e['index'];get=lambda key:z.read(e['resources'][key]['snapshot']);assert all(sha(get(k))==v['sha256'] for k,v in e['resources'].items())
  for category in ['normal','shiny']:
   palette=colors(get(category))
   for side in ['front','back']:images[(n,category,side)]=rgba(indices(get(side),64,64),palette,64,64)
  pal=colors(z.read(f'icons/palette-{e["icon_palette_index"]}.gbapal'));idx=indices(get('icon'),32,64);images[(n,'icons','frame0')]=rgba(idx[:1024],pal,32,32)
 assert records[149]['name']=='Enma' and records[149]['constant']=='SPECIES_MEWTWO'
def font(size):
 for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/Library/Fonts/Arial.ttf','C:/Windows/Fonts/arial.ttf']:
  if pathlib.Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default(size=size)
def checker(canvas,x,y,size,step):
 d=ImageDraw.Draw(canvas)
 for yy in range(0,size,step):
  for xx in range(0,size,step):d.rectangle((x+xx,y+yy,x+xx+step-1,y+yy+step-1),fill=(224,224,224) if (xx//step+yy//step)%2==0 else (176,176,176))
def place(canvas,sprite,x,y,scale):
 s=sprite.resize((sprite.width*scale,sprite.height*scale),Image.Resampling.NEAREST);checker(canvas,x,y,s.width,8*scale);canvas.paste(s,(x,y),s)
 # Ensure compositing kept each source opaque pixel exactly, and used no interpolation.
 crop=canvas.crop((x,y,x+s.width,y+s.height));mask=s.getchannel('A');a=list(s.get_flattened_data() if hasattr(s,'get_flattened_data') else s.getdata());b=list(crop.get_flattened_data() if hasattr(crop,'get_flattened_data') else crop.getdata());assert all(p[:3]==q for p,q in zip(a,b) if p[3]==255)
outputs=[];readme=['# Galerie Pokémon × Yo-kai Watch — 151 espèces','', 'Galerie de contrôle des ressources réellement intégrées : aucune image de référence WebP ni nouveau dessin. Les sprites de combat gardent le canevas complet 64 × 64 et une échelle uniforme **×3**, sans recadrage ; face et dos sont côte à côte. Les icônes sont affichées **×4**, première frame sur deux. Les damiers sont des pixels opaques des PNG RGB 8 bits.','', 'Les couleurs proviennent des palettes **RGB555 de la ROM**, développées vers RGB 8 bits sans recoloration. Les shinies utilisent leurs palettes existantes : ils ne sont pas de nouveaux sprites.','', 'Les marges du canevas sont conservées. Ces planches ne simulent pas le terrain de combat ni les offsets appliqués par le moteur ; les coordonnées actuelles sont consignées dans [le manifeste](source-manifest.json).','']
for category,title in [('normal','1. Sprites de combat normaux'),('shiny','2. Sprites shiny'),('icons','3. Icônes')]:
 (HERE/category).mkdir(exist_ok=True);readme+=['## '+title,'']
 if category=='icons':readme+=['Image fixe : frame 0 de l’animation existante. Palette d’icône sélectionnée par la table du jeu ; pas de variante shiny d’icône inventée.','']
 for start in range(0,151,25):
  group=records[start:start+25];a,b=group[0]['index'],group[-1]['index'];is_icon=category=='icons';scale=4 if is_icon else 3;s=32*scale if is_icon else 64*scale;cw=s+24 if is_icon else 2*s+36;ch=s+56;cols=5;rows=math.ceil(len(group)/cols);header=48;canvas=Image.new('RGB',(cols*cw,header+rows*ch),(238,238,238));d=ImageDraw.Draw(canvas);d.text((12,12),f'{title[3:]} — {a:03}–{b:03} — x{scale}',font=font(22 if not is_icon else 18),fill=(20,20,20))
  for j,e in enumerate(group):
   x=(j%cols)*cw;y=header+(j//cols)*ch;text=f'{e["index"]:03} — {e["name"]}';f=font(18 if not is_icon else 12)
   while d.textbbox((0,0),text,font=f)[2]>cw-12:f=font(f.size-1)
   box=d.textbbox((0,0),text,font=f);d.text((x+(cw-box[2])/2,y+3),text,font=f,fill=(20,20,20))
   if is_icon:place(canvas,images[(e['index'],'icons','frame0')],x+12,y+30,scale)
   else:
    for side,off,label in [('front',12,'Face'),('back',24+s,'Dos')]:
     d.text((x+off,y+24),label,font=font(12),fill=(40,40,40));place(canvas,images[(e['index'],category,side)],x+off,y+42,scale)
  rel=f'{category}/{a:03}-{b:03}.png';path=HERE/rel;canvas.save(path,format='PNG',compress_level=9)
  data=path.read_bytes();w,h,depth,typ,_,_,inter=struct.unpack('>IIBBBBB',data[16:29]);assert depth==8 and typ==2 and inter==0
  with Image.open(path) as check:check.load();assert check.mode=='RGB' and check.tobytes()==canvas.tobytes() and len(check.getcolors(w*h) or [])>20
  outputs.append({'path':rel,'indices':[e['index'] for e in group],'width':w,'height':h,'scale':scale,'sha256':sha(data)});readme += [f'### {a:03}–{b:03}',f'[Ouvrir en pleine résolution]({rel})','',f'![{title[3:]} {a:03}–{b:03}]({rel})','']
readme+=['## Données et vérifications','', 'Les **906 ressources** sont : 302 sprites de combat (151 faces + 151 dos), 151 icônes à deux frames, 151 empreintes et 302 palettes de combat (151 normales + 151 shiny). Les trois palettes d’icônes partagées sont supplémentaires. Les empreintes sont présentes dans l’instantané mais ne constituent pas une quatrième galerie demandée.','', 'Les 906 ressources ont été retrouvées byte pour byte dans la ROM compilée au moment de l’export ; indices des PNG sources et palettes RGB555 vérifiés. Enma est bien **150 / SPECIES_MEWTWO**. Les 151 numéros apparaissent exactement une fois dans chaque section, soit **755 vues** affichées (302 normales, 302 shiny, 151 icônes).','', 'Les PNG sont opaques, non entrelacés et sans profil de couleur. Les sprites/palettes du jeu et la ROM sont inchangés. Cette galerie permet une revue hors jeu ; elle ne remplace pas un test en émulateur.','', '## Régénérer la galerie','', 'La branche galerie est autonome : l’[instantané compact](sources/gba-graphics.zip) conserve les données indexées nécessaires. Aucun fichier ROM n’est distribué.','', 'Avec Python et Pillow, depuis la racine du dépôt :','', '```sh','python3 docs/yokai-gallery/scripts/gallery.py','```','', 'Pour rafraîchir cet instantané depuis le checkout de développement complet et sa ROM compilée (modifications du jeu non incluses dans cette branche) :','', '```sh','python3 docs/yokai-gallery/scripts/gallery.py --refresh','```','', '[Manifeste des sources](source-manifest.json) · [Rapport de validation](validation.json)','']
text='\n'.join(readme).rstrip();(HERE/'README.md').write_text(text+'\n')
links=re.findall(r'\]\(([^)]+)\)',text);assert all((HERE/l).is_file() for l in links if l!='validation.json')
for category in ['normal','shiny','icons']:assert [n for o in outputs if o['path'].startswith(category+'/') for n in o['indices']]==list(range(1,152))
report={'species':151,'normal_views':302,'shiny_views':302,'icon_views':151,'displayed_views':755,'sheets':len(outputs),'resource_count':906,'missing_resources':[],'rom_assets_verified_at_export':manifest['resource_count'],'normal_scale':3,'shiny_scale':3,'icon_scale':4,'canvas_cropping':False,'individual_resizing':False,'png_format':'opaque RGB8 non-interlaced','readme_links_checked':len(links),'generated':outputs};(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert all((HERE/l).is_file() for l in links)
print(json.dumps({k:v for k,v in report.items() if k!='generated'},ensure_ascii=False,indent=2))

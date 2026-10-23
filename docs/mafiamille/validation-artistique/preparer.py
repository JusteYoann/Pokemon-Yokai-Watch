#!/usr/bin/env python3
"""Preview only: explicit native pixel masks; never writes active game assets."""
from pathlib import Path
import hashlib,json,struct,subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
BASE='ddcb53b10e8cca51283b291078a1d91d20e3643c'
N=Image.Resampling.NEAREST
FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
# One character is one native pixel. O outline, L light grey, S grey shadow,
# B dark band. The four sizes are individually drawn, never downscaled.
MASKS={
 'rouleaux':[
 '........OOOOOOOOOO........','......OOLLLLLLLLLLOO......',
 '.....OLLLLLLLLLLLLLSO.....','.....OLLLLLLLLLLLLLSO.....',
 '.....OLLLLLLLLLLLLLSO.....','.....OLLLLLLLLLLLLSSO.....',
 '.....OLLLLLLLLLLLLSSO.....','.....OLLLLLLLLLLLSSSO.....',
 '.....OBBBBBBBBBBBBBBO.....','.....OBBBBBBBBBBBBBBO.....',
 '...OOSSSSSSSSSSSSSSSSOO...','.OOLLLLLLLLLLLLLLLLLLLLSOO.',
 'OLLLLLLLLLLLLLLLLLLLLLLSSO','OOSSSSSSSSSSSSSSSSSSSSSSOO',
 '..OOOOOOOOOOOOOOOOOOOOOO..'],
 'gains':[
 '....OOOOOO....','...OLLLLLSO...','...OLLLLLSO...',
 '...OLLLLSSO...','...OBBBBBBO...','..OSSSSSSSSO..',
 'OOLLLLLLLLLSOO','OSSSSSSSSSSSSO','.OOOOOOOOOOOO.'],
 'repaire':[
 '...OOOOOO...','..OLLLLSSO..','..OLLLLSSO..','..OLLLSSSO..',
 '..OBBBBBBO..','.OSSSSSSSSO.','OLLLLLLLLLSO','OSSSSSSSSSSO','.OOOOOOOOOO.'],
 'entrepot':[
 '.....OOOOOO.....','....OLLLLLSO....','...OLLLLLLLSO...',
 '...OLLLLLLLSO...','...OLLLLLLSSO...','...OBBBBBBBBO...',
 '..OSSSSSSSSSSO..','.OLLLLLLLLLLLSO.','OLLLLLLLLLLLLSSO',
 'OSSSSSSSSSSSSSSO','.OOOOOOOOOOOOOO.']}
# Fix lengths deliberately padded to max mask width (transparent pixels).
MASKS={k:[s.ljust(max(map(len,v)),'.') for s in v] for k,v in MASKS.items()}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(rel):return Image.open(ROOT/rel).copy()
def mask(key,palette,indices):
 rows=MASKS[key];im=Image.new('P',(len(rows[0]),len(rows)),0);im.putpalette(palette)
 for y,row in enumerate(rows):
  for x,c in enumerate(row):
   if c!='.':im.putpixel((x,y),indices[c])
 return im

def stamp(dst,m,xy):
 for y in range(m.height):
  for x in range(m.width):
   if m.getpixel((x,y)):dst.putpixel((xy[0]+x,xy[1]+y),m.getpixel((x,y)))

def compare(name,before,after,scale):
 b=before.convert('RGB').resize((before.width*scale,before.height*scale),N)
 a=after.convert('RGB').resize(b.size,N)
 sheet=Image.new('RGB',(max(600,b.width*2+36),b.height+65),'#e9e9e9');d=ImageDraw.Draw(sheet)
 d.text((12,8),'AVANT — ressource actuelle',font=FONT,fill='black');d.text((b.width+24,8),'APRÈS — simulation NON intégrée',font=FONT,fill='black')
 sheet.paste(b,(12,42));sheet.paste(a,(b.width+24,42));sheet.save(OUT/(name+'-comparaison.png'))

def render(tiles,raw,banks=False):
 entries=struct.unpack('<'+'H'*(len(raw)//2),raw);im=Image.new('P',(256,len(entries)//32*8));im.putpalette(tiles.getpalette());cols=tiles.width//8
 for i,v in enumerate(entries):
  t=v&1023;x=t%cols*8;y=t//cols*8;a=tiles.crop((x,y,x+8,y+8))
  if v&1024:a=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v&2048:a=a.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  if banks:
   bank=max(0,(v>>12)-7);a=a.point([j%16+bank*16 for j in range(256)])
  im.paste(a,((i%32)*8,(i//32)*8))
 return im

checks=[]
reel=load('graphics/slot_machine/firered/reel_icons.png');after=reel.copy();after.paste(0,(0,32,32,64))
m=mask('rouleaux',reel.getpalette(),dict(O=33,L=42,S=46,B=33));stamp(after,m,((32-m.width)//2,40))
assert reel.getpalette()==after.getpalette()
assert reel.crop((0,0,32,32)).tobytes()==after.crop((0,0,32,32)).tobytes()
assert reel.crop((0,64,32,224)).tobytes()==after.crop((0,64,32,224)).tobytes()
after.save(OUT/'rouleaux-proposition.png');compare('rouleaux',reel,after,3)
# Isolated 32x32 icon, true transparency; same palette as actual bank 2.
logo=Image.new('RGBA',(32,32));p=reel.getpalette()
for y,row in enumerate(MASKS['rouleaux']):
 for x,c in enumerate(row):
  if c!='.':
   idx=dict(O=33,L=42,S=46,B=33)[c];logo.putpixel(((32-m.width)//2+x,8+y),tuple(p[3*idx:3*idx+3])+(255,))
logo.save(OUT/'embleme-natif-32x32.png');logo.resize((512,512),N).save(OUT/'embleme-x16.png')
board=Image.new('RGB',(660,575),'#e5e5e5');draw=ImageDraw.Draw(board)
draw.text((18,10),'Chapeau Don Morléone — 32 × 32 natif / agrandi ×16',font=FONT,fill='black')
board.paste(logo,(24,60),logo);board.paste(logo.resize((512,512),N),(120,50),logo.resize((512,512),N))
board.save(OUT/'embleme-presentation.png')
checks.append(dict(resource='reel_icons.png',size=list(reel.size),edit_box=[0,32,32,64],palette_unchanged=True,other_six_icons_identical=True,mask_size=list(m.size)))
chart=load('graphics/slot_machine/firered/combos_window.png');after=chart.copy();after.paste(15,(48,0,64,16));m=mask('gains',chart.getpalette(),dict(O=17,L=18,S=25,B=17));stamp(after,m,(49,3))
after.save(OUT/'gains-proposition.png');compare('gains-feuille',chart,after,5)
raw=(ROOT/'graphics/slot_machine/firered/combos_window.bin').read_bytes();cb=render(chart,raw,True);ca=render(after,raw,True);cb.save(OUT/'gains-avant-natif.png');ca.save(OUT/'gains-apres-natif.png');compare('gains-en-situation',cb,ca,2)
for y in range(chart.height):
 for x in range(chart.width):
  if not(48<=x<64 and y<16):assert chart.getpixel((x,y))==after.getpixel((x,y))
checks.append(dict(resource='combos_window.png',size=list(chart.size),edit_box=[48,0,64,16],palette_unchanged=chart.getpalette()==after.getpalette(),other_pixels_identical=True,mask_size=list(m.size),rendered_three_times_by_unchanged_tilemap=True))
for key,folder,box,pos in [('repaire','rocket_hideout',(3,66,14,83),(2,69)),('entrepot','rocket_warehouse',(20,61,36,82),(20,65))]:
 rel='graphics/map_preview/'+folder;tiles=load(rel+'/tiles.png');raw=(ROOT/rel/'tilemap.bin').read_bytes();before=render(tiles,raw);after=before.copy()
 # Erase only the letter inside its original flat plaque, preserve its border.
 background=10 if key=='repaire' else 2
 # Existing letter and plaque shades, sampled rather than guessed.
 background=before.getpixel((box[0],box[1]))
 after.paste(background,box);m=mask(key,tiles.getpalette(),dict(O=1,L=8,S=13,B=1));stamp(after,m,pos)
 # Pack the simulated result with flip-aware deduplication into the SAME sheet
 # dimensions. Tilemaps are preview copies only; no live file is touched.
 candidate=Image.new('P',tiles.size);candidate.putpalette(tiles.getpalette())
 catalog={};new_entries=[];unique=0
 for y in range(0,after.height,8):
  for x in range(0,after.width,8):
   tile=after.crop((x,y,x+8,y+8));data=tile.tobytes()
   if data not in catalog:
    assert unique < (tiles.width//8)*(tiles.height//8), 'Native tile sheet capacity exceeded'
    candidate.paste(tile,(unique%(tiles.width//8)*8,unique//(tiles.width//8)*8))
    for flags,variant in [(0,tile),(1024,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),(2048,tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),(3072,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM))]:
     catalog.setdefault(variant.tobytes(),unique|flags)
    unique+=1
   new_entries.append(catalog[data])
 new_raw=struct.pack('<'+'H'*len(new_entries),*new_entries)
 assert render(candidate,new_raw).tobytes()==after.tobytes()
 assert candidate.size==tiles.size and candidate.getpalette()==tiles.getpalette()
 candidate.save(OUT/(key+'-tiles-proposition.png'));(OUT/(key+'-tilemap-proposition.bin')).write_bytes(new_raw)
 before.save(OUT/(key+'-avant-natif.png'));after.save(OUT/(key+'-apres-natif.png'));compare(key,before,after,2)
 changed=sum(a!=b for a,b in zip(before.tobytes(),after.tobytes()))
 checks.append(dict(resource=rel+'/tiles.png',size=list(tiles.size),render_size=list(before.size),mask_size=list(m.size),changed_pixels=changed,preview_tilemap_repacked=True,palette_unchanged=True,shared_tile_no_collateral_changes=True,used_tiles=unique,available_tiles=(tiles.width//8)*(tiles.height//8),erase_box=list(box),erase_background_index=background,mask_position=list(pos)))
# Source poses, no redrawing. East uses native horizontal reflection.
walk=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/marche'
for actor,title in [('don_morleone','Don Morléone'),('mafiamille_1','Sbire Mafiamille')]:
 sheet=load('graphics/yokai_characters/'+actor+'/overworld.png').convert('RGBA');sheet.putalpha(Image.open(ROOT/'graphics/yokai_characters'/actor/'overworld.png').convert('RGBA').getchannel('A'))
 board=Image.new('RGB',(700,650),'#d5ddd1');d=ImageDraw.Draw(board);d.text((18,10),title+' — poses sources inchangées, ×4',font=FONT,fill='black')
 for j,(direction,ids) in enumerate([('sud',[0,3,4]),('nord',[1,5,6]),('est',[2,7,8]),('ouest',[2,7,8])]):
  d.text((18,55+j*145),direction,font=FONT,fill='black')
  for k,i in enumerate(ids):
   frame=sheet.crop((i*16,0,i*16+16,32))
   if direction=='est':frame=frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   board.paste(frame.resize((64,128),N),(170+k*165,45+j*145),frame.resize((64,128),N))
 board.save(OUT/(actor+'-poses-x4.png'))
 # Direct copies of existing native emulator GIFs, no recompression.
 for direction in ['sud','nord','est','ouest']:
  name=actor+'-'+direction+'-marche.gif';(OUT/name).write_bytes((walk/name).read_bytes())
# Synchronized presentation of the eight existing mGBA captures.
movies=[Image.open(walk/(a+'-'+direction+'-marche.gif')) for a in ['don_morleone','mafiamille_1'] for direction in ['sud','nord','est','ouest']]
frames=[];durations=[]
for i in range(max(m.n_frames for m in movies)):
 board=Image.new('RGB',(960,390),'#e9e9e9');d=ImageDraw.Draw(board)
 for j,movie in enumerate(movies):
  movie.seek(i%movie.n_frames);x=j%4*240;y=j//4*195
  if j==0:durations.append(movie.info['duration'])
  else:assert movie.info['duration']==durations[-1], 'Different capture timelines'
  d.text((x+6,y+5),('Don' if j<4 else 'Sbire')+' — '+['sud','nord','est','ouest'][j%4],font=FONT,fill='black');board.paste(movie.convert('RGB'),(x,y+30))
 frames.append(board)
frames[0].save(OUT/'marche-mgba-8-vues.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
frames[0].save(OUT/'marche-mgba-8-vues.png')
# Entire tracked tree protected, except the preview-only directory.
subprocess.run(['git','diff','--exit-code',BASE,'--','.',':!docs/mafiamille/validation-artistique'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
tracked=subprocess.check_output(['git','ls-tree','-rz','--name-only',BASE],cwd=ROOT).split(b'\0')[:-1]
report=dict(base=BASE,scope='previews_only_no_ROM_integration',active_tracked_files_identical_to_base=len(tracked),native_masks=MASKS,checks=checks,walking_gifs_byte_identical=True,emblem_author='Native pixel masks drawn specifically for this project from existing Don artwork; no external artwork imported.',emulator_tests_rerun=False)
(OUT/'CONTROLES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: previews generated, all',len(tracked),'existing tracked files unchanged')

# Compact overview; full native comparisons remain separately available.
board=Image.new('RGB',(1050,750),'#e5e5e5');d=ImageDraw.Draw(board)
for label,name,x,y,scale in [('Rouleaux — simulation','rouleaux-proposition.png',12,35,2),('Gains — simulation','gains-apres-natif.png',255,35,2),('Repaire — simulation','repaire-apres-natif.png',12,410,2),('Entrepôt — simulation','entrepot-apres-natif.png',535,410,2)]:
 im=Image.open(OUT/name).convert('RGB')
 if name.startswith('rouleaux'):im=im.crop((0,32,32,64));scale=7
 d.text((x,y-26),label,font=FONT,fill='black');board.paste(im.resize((im.width*scale,im.height*scale),N),(x,y))
board.save(OUT/'quatre-usages-simules.png')

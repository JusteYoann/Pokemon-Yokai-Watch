#!/usr/bin/env python3
"""Install approved native hat art; warehouse wall restored without any emblem.

Only the four PNGs and the two entrance tilemaps are written. Casino code,
probabilities, payouts, palettes and all character animation sources untouched.
"""
from pathlib import Path
import io,json,hashlib,struct,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
REF='cee38fa5f22f95b65d63d995848c5ee94578b12c'
PRE='docs/mafiamille/validation-artistique/'
OUT=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/finalisation';OUT.mkdir(parents=True,exist_ok=True)

def blob(rel):return subprocess.check_output(['git','show',REF+':'+rel],cwd=ROOT)
def render(tiles,raw):
 entries=struct.unpack('<'+'H'*(len(raw)//2),raw);im=Image.new('P',(256,len(entries)//32*8));im.putpalette(tiles.getpalette());cols=tiles.width//8
 for i,v in enumerate(entries):
  t=v&1023;x=t%cols*8;y=t//cols*8;a=tiles.crop((x,y,x+8,y+8))
  if v&1024:a=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v&2048:a=a.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  im.paste(a,((i%32)*8,(i//32)*8))
 return im

def pack(im,size,template):
 attributes=struct.unpack('<640H',template)
 tiles=Image.new('P',size);tiles.putpalette(im.getpalette());catalog={};entries=[];count=0;cols=size[0]//8
 for y in range(0,im.height,8):
  for x in range(0,im.width,8):
   tile=im.crop((x,y,x+8,y+8));data=tile.tobytes()
   if data not in catalog:
    assert count<cols*(size[1]//8)
    tiles.paste(tile,(count%cols*8,count//cols*8))
    for flags,a in [(0,tile),(1024,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),(2048,tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),(3072,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM))]:catalog.setdefault(a.tobytes(),count|flags)
    count+=1
   entries.append(catalog[data] | (attributes[len(entries)] & 0xF000))
 raw=struct.pack('<'+'H'*len(entries),*entries)
 assert render(tiles,raw).tobytes()==im.tobytes()
 return tiles,raw,count

changes=[]
for target,source in [('graphics/slot_machine/firered/reel_icons.png','rouleaux-proposition.png'),('graphics/slot_machine/firered/combos_window.png','gains-proposition.png'),('graphics/map_preview/rocket_hideout/tiles.png','repaire-tiles-proposition.png'),('graphics/map_preview/rocket_hideout/tilemap.bin','repaire-tilemap-proposition.bin')]:
 data=blob(PRE+source);old=blob(target)
 if target.endswith('.png'):
  a=Image.open(io.BytesIO(old));b=Image.open(io.BytesIO(data));assert a.size==b.size and a.getpalette()==b.getpalette()
 if target.endswith('tilemap.bin'):
  proposed=struct.unpack('<640H',data);original=struct.unpack('<640H',old)
  data=struct.pack('<640H',*(v | (oldv & 0xF000) for v,oldv in zip(proposed,original)))
 (ROOT/target).write_bytes(data);changes.append(dict(path=target,approved_preview_exact=target.endswith('.png'),palette_bank_attributes_preserved=True,sha256=hashlib.sha256(data).hexdigest()))
# Original warehouse logo crosses a vertical light/shadow boundary at x=29.
# Restore BOTH underlying wall colours, including all letter highlights and
# the lighter rectangular backing; no blank plaque or new drawing remains.
folder='graphics/map_preview/rocket_warehouse/'
tiles=Image.open(io.BytesIO(blob(folder+'tiles.png')));raw=blob(folder+'tilemap.bin');before=render(tiles,raw);after=before.copy()
for y in range(58,83):
 for x in range(17,38):after.putpixel((x,y),10 if x<29 else 2)
# Every exterior pixel remains identical, including scratches and structure.
for y in range(before.height):
 for x in range(before.width):
  if not(17<=x<38 and 58<=y<83):assert before.getpixel((x,y))==after.getpixel((x,y))
newtiles,newraw,count=pack(after,tiles.size,raw)
newtiles.save(ROOT/(folder+'tiles.png'));(ROOT/(folder+'tilemap.bin')).write_bytes(newraw)
for rel in ['tiles.png','tilemap.bin']:changes.append(dict(path=folder+rel,sha256=hashlib.sha256((ROOT/(folder+rel)).read_bytes()).hexdigest()))
after.save(OUT/'entrepot-mur-restaure-natif.png')
assert newtiles.getpalette()==tiles.getpalette()
# Source Casino symbols unchanged outside original R cells.
for rel,box in [('reel_icons.png',(0,32,32,64)),('combos_window.png',(48,0,64,16))]:
 target='graphics/slot_machine/firered/'+rel;a=Image.open(io.BytesIO(blob(target)));b=Image.open(ROOT/target)
 for y in range(a.height):
  for x in range(a.width):
   if not(box[0]<=x<box[2] and box[1]<=y<box[3]):assert a.getpixel((x,y))==b.getpixel((x,y))
assert len(changes)==6
(OUT/'INTEGRATION.json').write_text(json.dumps(dict(reference=REF,modified_resources=changes,warehouse=dict(no_emblem=True,restored_box=[17,58,38,83],original_wall_boundary_x=29,original_palette_indices=[10,2],outside_pixels_identical=True,used_tiles=count),palettes_and_dimensions_preserved=True,other_casino_symbols_preserved=True),indent=2)+'\n')
print('PASS: six native resources installed; no gameplay or animation changes')

from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,struct,hashlib
R=Path(__file__).resolve().parents[4];D=R/'graphics/alyzon_bie/calque-pnj';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-calque-pnj';D.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
source=R/'graphics/object_events/pics/people/beauty.png';src=Image.open(source)
# Native Beauty palette roles retained, recolored locally for Alyzon.
# Index9 is unused in the source and becomes the cyan iris.
pal=[(0,0,0),(248,208,176),(240,184,144),(216,144,112),(120,64,64),(248,224,104),(216,184,64),(144,112,40),(128,64,152),(24,152,168),(40,64,88),(248,248,240),(184,184,192),(48,40,48),(248,248,240),(8,8,8)]
flat=sum((list(c) for c in pal),[])+[0]*(768-48)
def retouches_alyzon(f,direction,phase,off,base):
 # Small native recolorings: hair flows diagonally instead of the base's crown curl.
 patterns={
  'face':{12:{6:5,7:5,8:6},13:{6:5,7:5,8:5,10:6},14:{4:5,5:5,6:5,9:6,10:6},15:{4:5,5:5,6:5,9:6},16:{7:5,8:6,9:7},17:{8:7,9:6},21:{2:5,13:5}},
  'dos':{17:{6:5,7:6},18:{6:5,7:6},19:{6:5,7:6},20:{5:5,6:5},21:{2:5,6:6,7:7,13:5},22:{3:5,6:7,7:7,12:5}},
  'gauche':{14:{8:5,9:5,10:6},15:{7:5,8:5,10:6},17:{8:5,9:5,10:6},21:{13:5},22:{12:5}}
 }
 for yy,changes in patterns[direction].items():
  y=yy+off
  for x,c in changes.items():
   if y<32 and f.getpixel((x,y)) in [5,6,7]:f.putpixel((x,y),c)
 # Coat sleeves follow the exact existing arm shapes, with hands kept visible.
 if direction=='face':
  y=24+off
  for x,c in [(3,12),(4,11),(11,11),(12,12)]:
   if y<32 and base.getpixel((x,y)) in [1,2,3,4]:f.putpixel((x,y),c)
  # Purple neckline extends by a single row; small gray buckle at the waist.
  y=24+off
  for x in [7,8]:
   if y<32 and base.getpixel((x,y)) in [1,2,3,8,10,11,12,14]:f.putpixel((x,y),8)
  y=27+off
  if y<32 and base.getpixel((7,y)) in [8,10,11,12,14]:f.putpixel((7,y),12)
 elif direction=='gauche':
  for yy in [24,25]:
   y=yy+off
   for x,c in [(7,11),(8,12)]:
    if y<32 and base.getpixel((x,y)) in [1,2,3,4]:f.putpixel((x,y),c)
 return f
frames={};records=[];order={'face':[0,3,4],'dos':[1,5,6],'gauche':[2,7,8]}
for direction,indices in order.items():
 frames[direction]=[]
 for phase,idx in enumerate(indices):
  base=src.crop((16*idx,0,16*(idx+1),32));f=base.copy();f.putpalette(flat);f.info['transparency']=0;b=base.convert('RGBA').getbbox();origin=b[1];off=origin-11;edits=[]
  def paint(x,y,c):
   old=f.getpixel((x,y))
   if old!=c:edits.append([x,y,old,c]);f.putpixel((x,y),c)
  # Source body/feet/animation are traced exactly. Only the crown's top row
  # is trimmed when the original silhouette is20px tall, matching Nathan19px.
  if b[3]-b[1]>19:
   for x in range(16):
    if f.getpixel((x,origin)):paint(x,origin,0)
  if direction=='face':
   # Diagonal existing-hair extension masks the viewer-left eye, no added outline.
   for yy,patch in {18:{6:6,7:5},19:{5:6,6:5,7:6},20:{4:6,5:5,6:6},21:{4:6,5:6,6:7}}.items():
    for x,c in patch.items():
     y=yy+off
     if base.getpixel((x,y)):paint(x,y,c)
   paint(9,21+off,9)
   # Purple neckline, navy skirt between the original white skirt panels.
   if phase==0:
    for x in [7,8]:paint(x,25,8);paint(x,27,10);paint(x,28,10)
   else:
    # Walking torso moves with the existing source silhouette; repaint center
    # clothing pixels only, leaving hand and leg shapes and shading intact.
    for y in range(25,30):
     for x in [7,8]:
      c=base.getpixel((x,y))
      if c in [8,10,11,12,14]:paint(x,y,8 if y==25 else 10)
  elif direction=='gauche':
   # The covered-eye profile extends native blonde clusters over skin/eye pixels.
   for yy,patch in {18:{3:6,4:5},19:{3:6,4:5,5:6},20:{3:6,4:6,5:7},21:{4:6,5:7}}.items():
    for x,c in patch.items():
     y=yy+off
     if base.getpixel((x,y)):paint(x,y,c)
   for yy in [18,19,20]:paint(2,yy+off,0)
   for y in [24+off,25+off]:
    if y<32 and base.getpixel((4,y)):paint(4,y,8)
  f=retouches_alyzon(f,direction,phase,off,base)
  # Native source silhouettes below the crown remain pixel-for-pixel identical.
  for y in range(23+off,32):
   for x in range(16):assert bool(f.getpixel((x,y)))==bool(base.getpixel((x,y)))
  frames[direction].append(f);pose=['repos','pas-1','pas-2'][phase];f.save(D/f'{direction}-{pose}.png',transparency=0)
  bb=f.convert('RGBA').getbbox();records.append(dict(direction=direction,pose=pose,source_frame=idx,source_bbox=b,bbox=bb,height=bb[3]-bb[1],paint_edits=edits,body_alpha_unchanged=True,source_feet_unchanged=True))
# Opposite side begins with the same source profile mirrored, retains visible
# skin and pupil, and gets a cyan iris rather than the covered-eye paintover.
frames['droite']=[]
for phase,idx in enumerate(order['gauche']):
 base=src.crop((idx*16,0,(idx+1)*16,32));f=base.copy();f.putpalette(flat);f.info['transparency']=0;b=base.convert('RGBA').getbbox();off=b[1]-11
 if b[3]-b[1]>19:
  for x in range(16):f.putpixel((x,b[1]),0)
 # Native side eye is a single dark pixel at x5,y20. Keep its pupil and add iris below.
 if base.getpixel((5,21+off)):f.putpixel((5,21+off),9)
 for yy in [18,19,20]:f.putpixel((2,yy+off),0)
 for y in [24+off,25+off]:
  if y<32 and base.getpixel((4,y)):f.putpixel((4,y),8)
 f=retouches_alyzon(f,'gauche',phase,off,base)
 f=ImageOps.mirror(f);frames['droite'].append(f);pose=['repos','pas-1','pas-2'][phase];f.save(D/f'droite-{pose}.png',transparency=0)
 records.append(dict(direction='droite',pose=pose,source_frame=idx,source_bbox=b,bbox=f.convert('RGBA').getbbox(),body_alpha_unchanged=True,source_feet_unchanged=True,mirrored_source=True))
# Reusable native exports.
allp=Image.new('P',(48,128));allp.putpalette(flat);allp.info['transparency']=0
for j,d in enumerate(['face','dos','gauche','droite']):
 for i,f in enumerate(frames[d]):allp.paste(f,(16*i,32*j))
allp.save(D/'douze-poses.png',transparency=0)
engine=[frames[d][i] for d,i in [('face',0),('dos',0),('gauche',0),('face',1),('face',2),('dos',1),('dos',2),('gauche',1),('gauche',2)]]
sheet=Image.new('P',(144,32));sheet.putpalette(flat);sheet.info['transparency']=0;raw=bytearray()
for i,f in enumerate(engine):
 sheet.paste(f,(i*16,0))
 for ty in range(4):
  for tx in range(2):
   for y in range(8):
    for x in range(0,8,2):raw.append(f.getpixel((tx*8+x,ty*8+y))|f.getpixel((tx*8+x+1,ty*8+y))<<4)
sheet.save(D/'overworld.png',transparency=0);(D/'overworld.4bpp').write_bytes(raw);(D/'overworld.gbapal').write_bytes(b''.join(struct.pack('<H',(r//8)|((g//8)<<5)|((b//8)<<10)) for r,g,b in pal))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
board=Image.new('RGB',(720,900),(232,232,240));dr=ImageDraw.Draw(board)
for i,t in enumerate(['REPOS','PAS 1','PAS 2']):dr.text((175+i*175,8),t,font=font,fill='black')
for j,d in enumerate(['face','dos','gauche','droite']):
 dr.text((8,150+j*210),d.upper(),font=font,fill='black')
 for i,f in enumerate(frames[d]):
  a=f.convert('RGBA').resize((160,320),Image.Resampling.NEAREST).crop((0,100,160,320));board.paste(a,(135+i*175,35+j*210),a)
board.save(Q/'douze-poses-x10.png')
comp=Image.new('RGB',(760,330),(232,232,240));dr=ImageDraw.Draw(comp)
for i,(label,im) in enumerate([('BASE FRLG',src.crop((0,0,16,32)))]+[(d.upper(),frames[d][0]) for d in ['face','dos','gauche','droite']]):
 a=im.convert('RGBA').resize((128,256),Image.Resampling.NEAREST);comp.paste(a,(i*150+10,5),a);dr.text((i*150+20,280),label,font=font,fill='black')
comp.save(Q/'base-et-calque-x8.png')
movie=[]
for phase in [0,1,0,2]:
 im=Image.new('RGBA',(64,32),(232,232,240,255))
 for i,d in enumerate(['face','dos','gauche','droite']):im.alpha_composite(frames[d][phase].convert('RGBA'),(16*i,0))
 movie.append(im.convert('RGB').resize((768,384),Image.Resampling.NEAREST))
movie[0].save(Q/'marche-quatre-directions.gif',save_all=True,append_images=movie[1:],duration=134,loop=0)
(D/'CONSTRUCTION.json').write_text(json.dumps(dict(source=str(source.relative_to(R)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),base='Original FRLG Beauty NPC',method='Direct indexed pixel paintover of native source frames; no redrawn body or reconstructed animation',native_canvas=[16,32],palette_rgb555=pal,records=records),ensure_ascii=False,indent=2))
print('Native Beauty paintover:12poses; original body silhouettes and feet kept.')

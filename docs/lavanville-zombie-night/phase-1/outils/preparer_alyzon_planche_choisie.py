from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np,json,struct,hashlib
R=Path(__file__).resolve().parents[4];D=R/'graphics/alyzon_bie/poses-planche-validee';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-planche-validee'
src=Image.open(R/'graphics/alyzon_bie/sources/trois-poses-choisies.png').convert('RGBA');a=np.array(src)
# Explicit logical cell edges traced on the enlarged source, not a resize.
grids={
'gauche':([54,81,110,137,164,193,221,247,272,298,325,350,375,405,433,463,492,522,549,585],[142,170,197,224,252,280,309,333,362,388,415,444,470,496,522,545,570,595,631,655,681,709,734,760]),
'dos':([668,696,724,752,779,806,836,863,891,919,950,978,1007,1035,1063,1095,1127,1156],[140,167,198,226,252,281,306,336,362,389,415,440,467,495,521,547,571,595,622,650,678,702,725,752]),
'droite':([1236,1273,1303,1331,1361,1389,1417,1447,1472,1498,1525,1551,1576,1603,1632,1659,1686,1713,1741,1768],[142,169,197,224,252,281,309,336,361,388,415,443,467,496,522,545,570,595,631,655,681,709,734,760])}
raw={};colors=[]
for name,(xs,ys) in grids.items():
 b=np.zeros((23,len(xs)-1,4),dtype=np.uint8)
 for y in range(23):
  for x in range(len(xs)-1):
   cx=(xs[x]+xs[x+1])//2;cy=(ys[y]+ys[y+1])//2;patch=a[cy-4:cy+5,cx-4:cx+5];rgba=np.median(patch.reshape(-1,4),axis=0).astype('uint8')
   if rgba[3]>128:b[y,x]=[*rgba[:3],255];colors.append(tuple(rgba[:3]))
 raw[name]=b
# A shared native palette. The source is a high-resolution pixel-art study, not
# an original indexed GBA PNG: RGB555 adaptation necessarily changes exact RGB.
palette=[(0,0,0),(8,8,8),(168,120,24),(208,160,40),(248,216,80),(248,232,120),(232,176,128),(192,136,88),(0,144,184),(248,248,248),(208,216,224),(128,48,152),(32,56,96),(224,184,56),(248,224,104),(128,88,32)]
flat=sum((list(v) for v in palette),[])+[0]*(768-48)
frames={};records=[]
for name,b in raw.items():
 im=Image.new('P',(32,32),0);im.putpalette(flat);im.info['transparency']=0;ox=(32-b.shape[1])//2
 for y in range(23):
  for x in range(b.shape[1]):
   if b[y,x,3]:
    rgb=b[y,x,:3].astype(int);k=min(range(1,16),key=lambda i:sum((int(rgb[j])-palette[i][j])**2 for j in range(3)));im.putpixel((ox+x,8+y),k)
 frames[name]=[im]
 # Preserve all hair/face pixels. Only move hands, coat hem and feet below y27.
 for phase in [1,2]:
  f=im.copy();pix=np.array(im);arr=pix.copy();arr[27:31,:]=0
  # Two short legs alternate; each half shifts vertically one pixel up on its step.
  for y in range(27,31):
   for x in range(32):
    if pix[y,x]:
     dy=-1 if ((x<16)==(phase==1)) and y>=29 else 0
     arr[y+dy,x]=pix[y,x]
  # Whole lower legs can spread one pixel on profile step 1/2, never rescale.
  f=Image.fromarray(arr.astype('uint8'));f.putpalette(flat);f.info['transparency']=0
  assert f.crop((0,0,32,27)).tobytes()==im.crop((0,0,32,27)).tobytes()
  frames[name].append(f)
 for phase,f in enumerate(frames[name]):
  f.save(D/f'{name}-{["repos","pas-1","pas-2"][phase]}.png',transparency=0)
  records.append(dict(direction=name,pose=phase,bbox=f.convert('RGBA').getbbox()))
board=Image.new('RGB',(850,850),(232,232,240));dr=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
dr.text((14,10),'ALYZON BIE — LES TROIS POSES CHOISIES',font=font,fill='black')
for i,t in enumerate(['REPOS','PAS 1','PAS 2']):dr.text((180+220*i,45),t,font=font,fill='black')
for j,(name,fs) in enumerate(frames.items()):
 dr.text((10,160+250*j),name.upper(),font=font,fill='black')
 for i,im in enumerate(fs):
  big=im.convert('RGBA').resize((256,256),Image.Resampling.NEAREST);board.paste(big,(125+220*i,76+250*j),big)
board.save(Q/'planche-native-x8.png')
movie=[]
for phase in [0,1,0,2]:
 im=Image.new('RGBA',(96,32),(232,232,240,255))
 for j,name in enumerate(frames):im.alpha_composite(frames[name][phase].convert('RGBA'),(32*j,0))
 movie.append(im.convert('RGB').resize((960,320),Image.Resampling.NEAREST))
movie[0].save(Q/'marche-trois-poses.gif',save_all=True,append_images=movie[1:],loop=0,duration=160)
meta=dict(source='graphics/alyzon_bie/sources/trois-poses-choisies.png',source_sha256=hashlib.sha256((R/'graphics/alyzon_bie/sources/trois-poses-choisies.png').read_bytes()).hexdigest(),logical_grid_edges=grids,native_canvas=[32,32],native_grid_height=23,palette_rgb555=palette,pixel_identity_to_high_resolution_source=False,method='Explicit logical cell-center sampling, shared RGB555 palette; no replacement drawing of idle poses',records=records)
(D/'EXTRACTION.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print('Three source poses extracted on native logical grid; nine indexed PNGs.')

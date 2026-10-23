from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,struct,hashlib
R=Path(__file__).resolve().parents[4];D=R/'graphics/alyzon_bie';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-marche'
# Literal logical pixels; no reduction of a large illustration.
pal={'.':(0,0,0),'K':(8,8,8),'o':(168,120,24),'h':(208,160,40),'Y':(248,216,80),'L':(248,232,120),'s':(192,136,88),'S':(232,176,128),'E':(0,144,184),'W':(248,248,248),'w':(208,216,224),'P':(128,48,152),'p':(96,32,120),'B':(32,56,96),'b':(24,40,72),'d':(144,96,56)}
face=[
'.....oooo.....',
'....hLLLLh....',
'...hhYYYYYh...',
'.hhhLLYYYYYh..',
'.hLLhLLYYYYYh.',
'.hLLYhhYYYhYh.',
'..hLYSSShYLYh.',
'..hLYKSSKhLYh.',
'..hLYESSEhLYh.',
'.hLLYSSSShLLYh',
'.hLYKSSSSKLYYh',
'hLYKWWPPWWWKYh',
'..KSSWPPWSSK..',
'..KSWWBBWWsK..',
'..KKWWBBWWKK..',
'..KWWKKKKWWK..',
'..WWKK..KKWW..']
left=[
'.....oooo.....',
'....hLLLLh....',
'...hYYYYYYh...',
'..hLLYYYYYYh..',
'..hLYYYYYYYh..',
'..hLYYYYYYYh..',
'..hLShYYYYYh..',
'..hSKhYYYYYh..',
'.KSSEhYYYYYh..',
'..KSSShYYYYh..',
'...KSSKLYYh...',
'...KWPWWKYh...',
'...KWSWWWK....',
'...KwSSWWK....',
'...KWWWWWK....',
'...KWWKKWK....',
'...WKK.KKW....']
right=[r[::-1] for r in left]
# Distinct asymmetric hair contours rather than changing the approved front.
back=[
'.....oooo.....',
'....hLLLLh....',
'...hhYYYYYh...',
'..hLLYYYYYYh..',
'..hLLYYYYYYh..',
'..hLYYYYYYYh..',
'..hLYYYYYYYh..',
'..hLYYYYYYYh..',
'..hLYYhYYYYh..',
'.hLLYhhYYYLYh.',
'.hLYYhhYYYLYh.',
'hLYKhWhYhWWKYh',
'..KSSWWWWSSK..',
'..KsWWwwWWsK..',
'..KKWWwwWWKK..',
'..KWWWKKWWWK..',
'..WWKK..KKWW..']
for rows in [face,left,right,back]:assert all(len(r)==14 for r in rows)
keys=list(pal);palette=sum((list(v) for v in pal.values()),[])+[0]*(768-48)
frames={}
for name,rows in [('face',face),('dos',back),('gauche',left),('droite',right)]:
 frames[name]=[]
 for phase in range(3):
  mat=[list(r) for r in rows]
  if phase:
   # Preserve head and torso. Animate only lower coat, feet and short hands.
   if name in ['face','dos']:
    if phase==1:
     mat[15]=list('..KWWKKKKWWK..');mat[16]=list('..WKKK..KWWW..');mat.append(list('...KK.........'))
    else:
     mat[15]=list('..KWWKKKKWWK..');mat[16]=list('..WWWK..KKKW..');mat.append(list('.........KK...'))
   else:
    tail=['...KWWKKWK....','..WKK...KWW...','...KK.........'] if phase==1 else ['...KWWKKWK....','...WWWK.KK....','........KK....']
    if name=='droite':tail=[r[::-1] for r in tail]
    mat[15:]=[list(r) for r in tail]
  im=Image.new('P',(32,32));im.putpalette(palette);im.info['transparency']=0
  # Ground baseline y30 for each pose, no scale variation.
  oy=31-len(mat)
  for y,row in enumerate(mat):
   for x,c in enumerate(row):im.putpixel((9+x,oy+y),keys.index(c))
  # Keep head at same y for animation; walking feet get 1px extension and rest moves via body step.
  if phase:
   im=Image.new('P',(32,32));im.putpalette(palette);im.info['transparency']=0
   for y,row in enumerate(mat):
    for x,c in enumerate(row):im.putpixel((9+x,14+y),keys.index(c))
  im.save(D/'mouvement'/f'{name}-{["repos","pas-1","pas-2"][phase]}.png',transparency=0);frames[name].append(im)
# Front rest is kept separately for review against creator screenshot.
frames['face'][0].save(D/'front.png',transparency=0)
order=[('face',0),('dos',0),('gauche',0),('face',1),('face',2),('dos',1),('dos',2),('gauche',1),('gauche',2)]
sheet=Image.new('P',(288,32));sheet.putpalette(palette);sheet.info['transparency']=0;raw=bytearray()
for i,(n,p) in enumerate(order):
 f=frames[n][p];sheet.paste(f,(32*i,0))
 for ty in range(4):
  for tx in range(4):
   for y in range(8):
    for x in range(0,8,2):raw.append(f.getpixel((tx*8+x,ty*8+y))|(f.getpixel((tx*8+x+1,ty*8+y))<<4))
sheet.save(D/'overworld.png',transparency=0);(D/'overworld.4bpp').write_bytes(raw);(D/'overworld.gbapal').write_bytes(b''.join(struct.pack('<H',(r//8)|((g//8)<<5)|((b//8)<<10)) for r,g,b in pal.values()))
board=Image.new('RGB',(680,820),(232,232,240));dr=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for i,label in enumerate(['REPOS','PAS 1','PAS 2']):dr.text((140+i*176,10),label,font=font,fill='black')
for j,name in enumerate(frames):
 dr.text((8,106+j*192),name.upper(),font=font,fill='black')
 for i,im in enumerate(frames[name]):board.paste(im.convert('RGBA').resize((192,192),Image.Resampling.NEAREST),(100+i*184,36+j*192),im.convert('RGBA').resize((192,192),Image.Resampling.NEAREST))
board.save(Q/'planche-directions-x6.png')
anim=[]
for phase in [0,1,0,2]:
 im=Image.new('RGBA',(128,32),(232,232,240,255))
 for j,name in enumerate(frames):im.alpha_composite(frames[name][phase].convert('RGBA'),(32*j,0))
 anim.append(im.convert('RGB').resize((1024,256),Image.Resampling.NEAREST))
anim[0].save(Q/'marche-quatre-directions.gif',save_all=True,append_images=anim[1:],loop=0,duration=160)
(D/'grille.json').write_text(json.dumps(dict(palette=pal,face=face,gauche=left,dos=back,source='Transcription visuelle de la capture choisie, couleurs estimées sur grille GBA. Original binaire indisponible.'),ensure_ascii=False,indent=2))
print('12 poses, 9 frames FRLG,',len(raw),'bytes')

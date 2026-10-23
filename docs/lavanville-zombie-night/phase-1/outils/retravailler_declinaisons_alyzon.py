from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[4];D=R/'graphics/alyzon_bie/declinaisons-v2';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-marche-v2'
D.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
old=R/'graphics/alyzon_bie/front.png';before=hashlib.sha256(old.read_bytes()).hexdigest()
pal=json.loads((R/'graphics/alyzon_bie/grille.json').read_text())['palette'];keys=list(pal);p=sum((v for v in pal.values()),[]);p+= [0]*(768-len(p))
# Same 14x17 envelope as creator's front in the screenshot. Broader hair,
# side locks flaring at shoulders; short torso, open white coat, compact feet.
left=[
'.....oooo.....',
'....hLLLLh....',
'...hhYYYYYh...',
'.hhhLLYYYYYh..',
'.hLLhLYYYYYYh.',
'.hLLYhYYYYYYh.',
'..hLYShYYYYYh.',
'..hLSKhYYYYYh.',
'....SEhYYYYYh.',
'....SShYYhYLYh',
'...KSSKYYhLLYh',
'...KWPWKhKLYYh',
'...KWSSWWKKYh.',
'...KwSsWWwK...',
'...KWBKWWWK...',
'...KWBKKWWK...',
'...WKK.KKWW...']
back=[
'.....oooo.....',
'....hLLLLh....',
'...hhYYYYYh...',
'..hLLYYYYYYh..',
'.hLLhLYYYYYYh.',
'.hLLYhYYYYYYh.',
'..hLYYYYYYLYh.',
'..hLYYhYYYLYh.',
'..hLYYhYYhLYh.',
'.hLLYhhYYhLLYh',
'.hLYYhhYYhLYYh',
'hLYKWhWYhWWKYh',
'..KSSWWWWSSK..',
'..KsWWwwWWsK..',
'..KKWWwwWWKK..',
'..KWWWKKWWWK..',
'..WWKK..KKWW..']
right=[r[::-1] for r in left]
# The asymmetric fringe is longer toward the opposite profile.
right[6]='.hYYYYYYhSYLh.'
right[7]='.hYYYYYYhKSLh.'
right[8]='.hYYYYYYhES...'
rows_by={'gauche':left,'dos':back,'droite':right};frames={};records=[]
for name,rows in rows_by.items():
 assert all(len(r)==14 for r in rows),(name,[(i,len(r)) for i,r in enumerate(rows)])
 frames[name]=[]
 for phase in range(3):
  mat=[list(r) for r in rows]
  if phase:
   if name=='dos':
    mat[12]=list('..KSSWWWWSSK..' if phase==1 else '..KSWWWWWWsK..')
    mat[13]=list('..KSWwwWWWsK..' if phase==1 else '..KsWWWwwWSK..')
    mat[15]=list('..KWWKKKKWWK..')
    mat[16]=list('..WKKK..KWWW..' if phase==1 else '..WWWK..KKKW..')
   else:
    temp=[list(r) for r in left]
    temp[12]=list('...KWSSWWKKYh.' if phase==1 else '...KSSWWWKKYh.')
    temp[13]=list('...KwSsWWwK...' if phase==1 else '...KSSWWWwK...')
    temp[15]=list('...KWBKKWWK...')
    temp[16]=list('..WWKK..KWW...' if phase==1 else '...WKKKWWK....')
    for y in [12,13,15,16]:mat[y]=temp[y] if name=='gauche' else temp[y][::-1]
  im=Image.new('P',(32,32));im.putpalette(p);im.info['transparency']=0
  for y,row in enumerate(mat):
   for x,c in enumerate(row):im.putpixel((9+x,14+y),keys.index(c))
  pose=['repos','pas-1','pas-2'][phase];im.save(D/f'{name}-{pose}.png',transparency=0);frames[name].append(im)
  records.append(dict(direction=name,pose=pose,bbox=im.convert('RGBA').getbbox()))
 for im in frames[name][1:]:assert im.crop((0,0,32,26)).tobytes()==frames[name][0].crop((0,0,32,26)).tobytes()
board=Image.new('RGB',(790,720),(228,230,238));dr=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
dr.text((18,12),'ALYZON BIE — DECLINAISONS RETRAVAILLEES',fill='black',font=font)
for i,t in enumerate(['REPOS','PAS 1','PAS 2']):dr.text((155+i*210,48),t,fill='black',font=font)
for j,name in enumerate(frames):
 dr.text((12,152+j*210),name.upper(),fill='black',font=font)
 for i,im in enumerate(frames[name]):
  a=im.convert('RGBA').resize((256,256),Image.Resampling.NEAREST)
  # Tight sprite display, no change to source data.
  a=a.crop((48,96,224,256));board.paste(a,(126+210*i,82+210*j),a)
board.save(Q/'planche-directions-x8.png')
anim=[]
for phase in [0,1,0,2]:
 im=Image.new('RGBA',(96,32),(228,230,238,255))
 for j,name in enumerate(frames):im.alpha_composite(frames[name][phase].convert('RGBA'),(32*j,0))
 anim.append(im.convert('RGB').resize((960,320),Image.Resampling.NEAREST))
anim[0].save(Q/'marche-profils-dos.gif',save_all=True,append_images=anim[1:],duration=160,loop=0)
assert before==hashlib.sha256(old.read_bytes()).hexdigest()
(D/'grilles.json').write_text(json.dumps(dict(palette=pal,rows=rows_by,records=records,old_front_untouched=True,source='Déclinaisons adaptées visuellement à la capture choisie ; face non incluse dans cette nouvelle planche.'),ensure_ascii=False,indent=2))
print('9 poses, contours opaques, hauteur fixe, ancienne transcription de face inchangée.')

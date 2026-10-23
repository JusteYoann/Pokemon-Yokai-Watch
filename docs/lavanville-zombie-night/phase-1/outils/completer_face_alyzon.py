from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,struct
R=Path(__file__).resolve().parents[4];D=R/'graphics/alyzon_bie/taille-nathan';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-face-complete';Q.mkdir(exist_ok=True)
palette=json.loads((D/'EXTRACTION.json').read_text())['palette_rgb555'];keys='.KohYLsSEWwPBatd';assert len(keys)==16
# Palette indices: source colors from the selected GBA adaptation.
# Literal transcription of screenshot 114647; a visual reconstruction, not
# a claim to have recovered the unavailable original PNG bytes.
rows=[
'.....oooo.....',
'....hYYYYh....',
'..hhLLLhYYh...',
'.hLLLLLLLLYh..',
'.hLoLLLLLohYh.',
'.hLLLLLLohLYh.',
'..hLLLLohLYh..',
'..hLLLohShYh..',
'..hLLLhSKhYh..',
'.hLLLhhSEhLYh.',
'.hLYKKSSSKLYYh',
'hLYKWWPPWWWKYh',
'..KSSWPPWSSK..',
'..KSWWBBWWsK..',
'..KKWWBBWWKK..',
'..KWWKKKKWWK..',
'..WWKK..KKWW..']
assert all(len(r)==14 for r in rows)
# Explicit mapping ensures skin/eye/coat/garments share the existing palette.
mapping={'.':0,'K':1,'o':2,'h':3,'Y':4,'L':5,'S':6,'s':7,'E':8,'W':9,'w':10,'P':11,'B':12,'a':13,'t':14,'d':15}
flat=sum((list(v) for v in palette),[])+[0]*(768-48)
logical=Image.new('P',(14,17));logical.putpalette(flat);logical.info['transparency']=0
for y,row in enumerate(rows):
 for x,c in enumerate(row):logical.putpixel((x,y),mapping[c])
# Requested calibration from 17 to Nathan's measured 19 logical pixels.
part=logical.resize((16,19),Image.Resampling.NEAREST)
idle=Image.new('P',(32,32));idle.putpalette(flat);idle.info['transparency']=0;idle.paste(part,(8,12));frames=[idle]
for phase in (1,2):
 f=idle.copy()
 # Alternate only the foot/hem pixels; the upper 28 rows remain identical.
 for y in range(29,31):
  for x in range(8,24):f.putpixel((x,y),0)
 for y in range(29,31):
  for x in range(8,24):
   c=idle.getpixel((x,y))
   if c:
    dy=-1 if (x<16)==(phase==1) else 0
    f.putpixel((x,y+dy),c)
 assert f.crop((0,0,32,28)).tobytes()==idle.crop((0,0,32,28)).tobytes()
 frames.append(f)
for pose,f in zip(['repos','pas-1','pas-2'],frames):f.save(D/f'face-{pose}.png',transparency=0)
board=Image.new('RGB',(820,1080),(232,232,240));draw=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for i,title in enumerate(['REPOS','PAS 1','PAS 2']):draw.text((180+i*215,15),title,font=font,fill='black')
for j,direction in enumerate(['face','dos','gauche','droite']):
 draw.text((8,160+j*250),direction.upper(),font=font,fill='black')
 for i,pose in enumerate(['repos','pas-1','pas-2']):
  im=Image.open(D/f'{direction}-{pose}.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);board.paste(im,(120+215*i,40+250*j),im)
board.save(Q/'douze-poses-x8.png')
anim=[]
for phase in [0,1,0,2]:
 im=Image.new('RGBA',(128,32),(232,232,240,255))
 for i,d in enumerate(['face','dos','gauche','droite']):im.alpha_composite(Image.open(D/f'{d}-{["repos","pas-1","pas-2"][phase]}.png').convert('RGBA'),(32*i,0))
 anim.append(im.convert('RGB').resize((1024,256),Image.Resampling.NEAREST))
anim[0].save(Q/'marche-quatre-directions.gif',save_all=True,append_images=anim[1:],duration=160,loop=0)
# Native FRLG sheet, with right exported independently for asymmetric direction handling.
order=[('face',0),('dos',0),('gauche',0),('face',1),('face',2),('dos',1),('dos',2),('gauche',1),('gauche',2)]
sheet=Image.new('P',(288,32));sheet.putpalette(flat);sheet.info['transparency']=0;raw=bytearray()
for i,(direction,phase) in enumerate(order):
 im=Image.open(D/f'{direction}-{["repos","pas-1","pas-2"][phase]}.png');sheet.paste(im,(32*i,0))
 for ty in range(4):
  for tx in range(4):
   for y in range(8):
    for x in range(0,8,2):raw.append(im.getpixel((tx*8+x,ty*8+y))|im.getpixel((tx*8+x+1,ty*8+y))<<4)
sheet.save(D/'overworld.png',transparency=0);(D/'overworld.4bpp').write_bytes(raw);(D/'overworld.gbapal').write_bytes(b''.join(struct.pack('<H',(r//8)|((g//8)<<5)|((b//8)<<10)) for r,g,b in palette))
manifest=dict(reference='Screenshot 2026-10-23 114647.png',method='Visual literal-grid transcription, shared existing GBA palette; source binary unavailable',logical_rows=rows,height_idle=19,head_and_eye_fixed=True,native_frame=[32,32],approved_original_pixel_identity=False,poses=12,front_pngs=[f'graphics/alyzon_bie/taille-nathan/face-{p}.png' for p in ['repos','pas-1','pas-2']])
(Q/'FACE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
meta=json.loads((D/'EXTRACTION.json').read_text());meta['front_status']='Visual transcription from creator screenshot, 19px idle and two steps; compare against creator original before integration';meta['front_manifest']='docs/lavanville-zombie-night/phase-1/prototypes/alyzon-face-complete/FACE.json';(D/'EXTRACTION.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print('Face + two steps, all 12 poses, front idle bbox',idle.convert('RGBA').getbbox())

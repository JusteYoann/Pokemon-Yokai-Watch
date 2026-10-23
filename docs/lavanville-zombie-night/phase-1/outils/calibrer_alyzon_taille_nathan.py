from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[4];S=R/'graphics/alyzon_bie/poses-planche-validee';D=R/'graphics/alyzon_bie/taille-nathan';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-taille-nathan';D.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
n=Image.open(R/'graphics/yokai_characters/nathan/normal.png').crop((0,0,16,32));box=n.convert('RGBA').getbbox();height=box[3]-box[1];assert height==19
original=json.loads((S/'EXTRACTION.json').read_text());records=[];frames={}
for direction in ['gauche','dos','droite']:
 frames[direction]=[]
 # One fixed transformation per direction retains consistent framing throughout the walk.
 ref=Image.open(S/f'{direction}-repos.png');bbox=ref.convert('RGBA').getbbox();w=round((bbox[2]-bbox[0])*height/(bbox[3]-bbox[1]));ox=(32-w)//2;oy=31-height
 for pose in ['repos','pas-1','pas-2']:
  im=Image.open(S/f'{direction}-{pose}.png');part=im.crop(bbox).resize((w,height),Image.Resampling.NEAREST)
  f=Image.new('P',(32,32),0);f.putpalette(im.getpalette());f.info['transparency']=0;f.paste(part,(ox,oy))
  out=D/f'{direction}-{pose}.png';f.save(out,transparency=0);frames[direction].append(f)
  fb=f.convert('RGBA').getbbox();assert fb[3]-fb[1]<=height
  if pose=='repos':assert fb[3]-fb[1]==height
  records.append(dict(direction=direction,pose=pose,source_bbox=bbox,bbox=fb,height=fb[3]-fb[1],sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
original.update(target_height=height,nathan_bbox=box,records=records,front_status='Creator screenshot 120009 selected; native source PNG required to preserve its exact pixels; no front redrawn')
(D/'EXTRACTION.json').write_text(json.dumps(original,ensure_ascii=False,indent=2))
board=Image.new('RGB',(760,330),(232,232,240));draw=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
draw.text((15,10),'MEME HAUTEUR : 19 PIXELS — PIEDS ALIGNES',font=font,fill='black')
for i,(name,im) in enumerate([('NATHAN',n),('GAUCHE',frames['gauche'][0]),('DOS',frames['dos'][0]),('DROITE',frames['droite'][0])]):
 a=im.convert('RGBA');c=a.crop(a.getbbox());c=c.resize((c.width*8,c.height*8),Image.Resampling.NEAREST);board.paste(c,(i*185+90-c.width//2,230-c.height),c);draw.text((i*185+40,248),name,font=font,fill='black')
draw.line((15,231,740,231),fill=(140,140,140),width=1);board.save(Q/'comparaison-nathan-x8.png')
print('Nathan bbox',box,'height',height,'; all idle poses',height,'pixels tall')

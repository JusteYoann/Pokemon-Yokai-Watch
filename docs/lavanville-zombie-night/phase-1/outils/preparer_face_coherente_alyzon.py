from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,struct
R=Path(__file__).resolve().parents[4];D=R/'graphics/alyzon_bie/face-coherente';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-face-coherente'
ref=R/'graphics/alyzon_bie/taille-nathan';palette=json.loads((ref/'EXTRACTION.json').read_text())['palette_rgb555'];flat=sum((list(c) for c in palette),[])+[0]*(768-48)
a=np.array(Image.open(D/'etude-face.png').convert('RGBA'))
# Reconstruct the guide's logical clusters, then calibrate this new proposal
# to the same 19px height as the three approved directions.
xs=[round(132+(1042-132)*i/19) for i in range(20)];ys=[round(134+(1186-134)*i/23) for i in range(24)]
im=Image.new('P',(19,23));im.putpalette(flat);im.info['transparency']=0
for y in range(23):
 for x in range(19):
  cx=(xs[x]+xs[x+1])//2;cy=(ys[y]+ys[y+1])//2
  rgba=np.median(a[cy-4:cy+5,cx-4:cx+5].reshape(-1,4),axis=0)
  if rgba[3]>128:
   rgb=rgba[:3];idx=min(range(1,16),key=lambda k:sum((int(rgb[j])-palette[k][j])**2 for j in range(3)))
   im.putpixel((x,y),idx)
im.save(D/'face-grille.png',transparency=0)
part=im.resize((17,19),Image.Resampling.NEAREST);out=Image.new('P',(32,32));out.putpalette(flat);out.info['transparency']=0;out.paste(part,(7,12))
assert 8 in out.get_flattened_data(),'Cyan eye must survive calibration'
assert out.convert('RGBA').getbbox()[3]-out.convert('RGBA').getbbox()[1]==19
out.save(D/'face-repos.png',transparency=0)
# Transparent, enlarged view and a neutral board for the new face only.
out.convert('RGBA').resize((512,512),Image.Resampling.NEAREST).save(Q/'face-transparente-x16.png')
face=out.convert('RGBA').crop(out.convert('RGBA').getbbox()).resize((272,304),Image.Resampling.NEAREST)
solo=Image.new('RGBA',(352,384),(232,232,240,255));solo.alpha_composite(face,(40,40));solo.save(Q/'face-x16.png')
board=Image.new('RGB',(850,340),(232,232,240));dr=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
dr.text((14,12),'NOUVELLE FACE — MEME PALETTE, MEME HAUTEUR',font=font,fill='black')
for i,(name,p) in enumerate([('FACE',D/'face-repos.png'),('GAUCHE',ref/'gauche-repos.png'),('DOS',ref/'dos-repos.png'),('DROITE',ref/'droite-repos.png')]):
 f=Image.open(p).convert('RGBA');b=f.getbbox();c=f.crop(b).resize(((b[2]-b[0])*8,19*8),Image.Resampling.NEAREST)
 board.paste(c,(i*210+105-c.width//2,240-c.height),c);dr.text((i*210+65,260),name,font=font,fill='black')
board.save(Q/'comparaison-quatre-poses-x8.png')
raw=bytearray()
for ty in range(4):
 for tx in range(4):
  for y in range(8):
   for x in range(0,8,2):raw.append(out.getpixel((tx*8+x,ty*8+y))|out.getpixel((tx*8+x+1,ty*8+y))<<4)
(D/'face-repos.4bpp').write_bytes(raw);(D/'face-repos.gbapal').write_bytes(b''.join(struct.pack('<H',(r//8)|((g//8)<<5)|((b//8)<<10)) for r,g,b in palette))
(Q/'CONTROLE.json').write_text(json.dumps(dict(new_design=True,height=19,frame=[32,32],bbox=out.convert('RGBA').getbbox(),palette_rgb555=palette,cyan_pixels=sum(v==8 for v in out.get_flattened_data()),colors=len(set(out.get_flattened_data()))-1,old_poses_unchanged=True,method='Generated front study guided by chosen three sprites; logical-grid reconstruction and nearest-neighbor calibration to19px',source_grid_edges=[xs,ys]),ensure_ascii=False,indent=2))
print('New front, 19px tall, shared palette; old directional files unchanged.')

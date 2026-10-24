#!/usr/bin/env python3
"""Native GBA conversion of the imagegen four-view sheet; no shape repainting."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/patrouille_oni';P=R/'docs/patrouille-oni-20261024';P.mkdir(exist_ok=True)
source=D/'source/planche-generee.png';im=Image.open(source).convert('RGBA')
colors=[(0,0,0),(24,8,32),(64,32,88),(88,56,120),(120,88,160),(160,128,200),(200,176,224),(0,72,56),(8,152,112),(56,216,168),(184,104,8),(248,176,16),(232,184,48),(248,224,80),(248,248,144),(248,248,216)]
flat=[v for c in colors for v in c]+[0]*720;sheet=Image.new('P',(128,32));sheet.putpalette(flat);boxes=[]
for n,(x0,x1) in enumerate([(35,510),(575,1050),(1125,1560),(1700,2130)]):
 p=im.crop((x0,90,x1,620));p.putalpha(p.getchannel('A').point(lambda a:255 if a>=128 else 0));b=p.getbbox();assert b;boxes.append([x0+b[0],90+b[1],x0+b[2],90+b[3]])
 p=p.crop(b);p=p.resize((round(p.width*22/p.height),22),Image.Resampling.NEAREST)
 q=Image.new('P',p.size);q.putpalette(flat);q.putdata([0 if a<128 else min(range(1,16),key=lambda j:sum((v-colors[j][k])**2 for k,v in enumerate((r,g,b)))) for r,g,b,a in p.get_flattened_data()]);sheet.paste(q,(n*32+(32-p.width)//2,9))
sheet.save(D/'overworld.png',transparency=0);sheet.save(P/'quatre-vues.png',transparency=0);sheet.convert('RGBA').resize((768,192),Image.Resampling.NEAREST).save(P/'quatre-vues-x6.png')
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
(D/'CONVERSION.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frame_size=[32,32],visible_height=22,order=['face','dos','gauche','droite'],source_boxes=boxes,method='alpha threshold, nearest-neighbor reduction, common 15-color GBA palette; no repainted shapes'),indent=2)+'\n')

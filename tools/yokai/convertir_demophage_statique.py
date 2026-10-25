#!/usr/bin/env python3
"""Conversion technique du dessin généré vers une cellule GBA statique, 15 couleurs."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/demophage_statique';P=R/'docs/demophage-statique-20261025';P.mkdir(exist_ok=True)
src=D/'source/face-generee.png';im=Image.open(src).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));bounds=im.getbbox();im=im.crop(bounds).resize((27,26),Image.Resampling.NEAREST)
colors=[(0,0,0),(24,16,24),(64,40,40),(128,80,8),(184,120,0),(232,168,0),(248,200,32),(248,232,104),(152,144,136),(216,208,192),(248,248,232),(0,72,80),(0,128,144),(72,192,192),(120,24,56),(216,56,88)]
pal=[v for c in colors for v in c]+[0]*720
small=Image.new('P',im.size);small.putpalette(pal);small.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((v-colors[i][k])**2 for k,v in enumerate((r,g,b)))) for r,g,b,a in im.get_flattened_data()])
frame=Image.new('P',(32,32));frame.putpalette(pal);frame.paste(small,((32-im.width)//2,31-im.height));frame.info['transparency']=0
visible=frame.convert('RGBA').getbbox();assert visible[2]-visible[0]==27 and visible[3]-visible[1]==26 and visible[3]==31
frame.save(D/'overworld.png',transparency=0);frame.save(P/'demophage-face.png',transparency=0);frame.convert('RGBA').resize((256,256),Image.Resampling.NEAREST).save(P/'demophage-face-x8.png')
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
(D/'CONVERSION.json').write_text(json.dumps({'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_bounds':bounds,'frame_size':[32,32],'visible_bounds':visible,'visible_width':27,'visible_height':26,'reference_oni_width':18,'reference_oni_height':22,'poses':1,'direction':'face','colors':15,'transparent_index':0,'new_story_event':False},ensure_ascii=False,indent=2)+'\n')
print('Démophage: face statique, 27×26 pixels visibles, cellule 32×32 transparente.')

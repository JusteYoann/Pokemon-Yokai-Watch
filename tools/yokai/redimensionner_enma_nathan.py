#!/usr/bin/env python3
"""Reprend le caméo royal approuvé, aux proportions de largeur de Nathan.
Conversion d'indices uniquement, plus proche voisin ; portrait de combat inchangé.
"""
import json,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/enma'
source=D/'source/cameo-original-3abcd3586.png';im=Image.open(source)
nathan=Image.open(R/'graphics/yokai_characters/nathan/normal.png').convert('RGBA').crop((0,0,16,32)).getchannel('A').getbbox()
target_width=nathan[2]-nathan[0];baseline=nathan[3]
front=im.convert('RGBA').crop((0,0,16,32)).getchannel('A').getbbox();scale=target_width/(front[2]-front[0])
out=Image.new('P',im.size);out.putpalette(im.getpalette());rows=[]
for i in range(3):
 frame=im.crop((i*16,0,(i+1)*16,32));box=frame.convert('RGBA').getchannel('A').getbbox();sprite=frame.crop(box)
 w=max(1,round(sprite.width*scale));h=max(1,round(sprite.height*scale));assert w<=16 and h<=31
 sprite=sprite.resize((w,h),Image.Resampling.NEAREST);out.paste(sprite,(i*16+(16-w)//2,baseline-h))
 rows.append({'pose':i,'source_visible_bbox':box,'native_size':[w,h]})
for p in (D/'overworld.png',R/'graphics/yokai_characters/overworld_red_v3/approved_overrides/enma.png'):out.save(p,bits=4,transparency=0)
pal=(im.getpalette()+[0]*48)[:48];(D/'overworld.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,pal[i:i+3])) for i in range(0,48,3))+'\n')
m=R/'graphics/yokai_characters/overworld_red_v3/manifest.json';data=json.loads(m.read_text());data.setdefault('override_source_commits',{})['enma']=None;data.setdefault('override_origins',{})['enma']=str(source.relative_to(R));data['latest_selection']='Seigneur Enma royal des caméos adapté à la largeur de Nathan ; Domniscian et autres sélections conservés.';m.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
report={'source':str(source.relative_to(R)),'source_commit':'3abcd3586','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'nathan_front_visible_width':target_width,'nathan_front_visible_height':nathan[3]-nathan[1],'scale':scale,'baseline':baseline,'frames':rows,'battle_portrait_unchanged':True}
(D/'TAILLE_NATHAN_20261025.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report)

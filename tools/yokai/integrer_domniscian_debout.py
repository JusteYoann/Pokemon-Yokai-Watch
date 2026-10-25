#!/usr/bin/env python3
"""Convertit la planche debout fournie vers les trois poses natives de Domniscian.
Aucun dessin ajouté. Palette partagée conservée pour préserver les employés.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];root=R/'graphics/yokai_characters';source=root/'overworld_red_v3/source/domniscian.png';im=Image.open(source).convert('RGBA');alpha=np.asarray(im)[:,:,3]>=128
cols=np.where(alpha.sum(0)>3)[0];runs=[];start=last=int(cols[0])
for x in cols[1:]:
 x=int(x)
 if x-last>7:runs.append((start,last+1));start=x
 last=x
runs.append((start,last+1));assert len(runs)==3,runs
reference=Image.open(R/'graphics/dossier-20261023/nyada/overworld.png');bbox=reference.point(lambda v:255 if v else 0).getbbox();target_height=bbox[3]-bbox[1];baseline=bbox[3]
colors=[tuple(map(int,line.split())) for line in (root/'domniscian/overworld.pal').read_text().splitlines()[3:19]];flat=[v for c in colors for v in c]+[0]*720;sheet=Image.new('P',(96,32));sheet.putpalette(flat);sheet.info['transparency']=0;rows=[]
for i,(x1,x2) in enumerate(runs):
 ys=np.where(alpha[:,x1:x2].sum(1)>3)[0];box=(x1,int(ys[0]),x2,int(ys[-1])+1);height=target_height;width=min(24,round((box[2]-box[0])*height/(box[3]-box[1])));pose=im.crop(box).resize((width,height),Image.Resampling.NEAREST)
 data=[0 if a<128 else min(range(1,16),key=lambda n:sum((v-c)**2 for v,c in zip((r,g,b),colors[n]))) for r,g,b,a in pose.get_flattened_data()];native=Image.new('P',pose.size);native.putpalette(flat);native.putdata(data);sheet.paste(native,(i*32+(32-width)//2,baseline-height));rows.append({'pose':i,'source_box':box,'native_visible_size':[width,height]})
for p in [root/'domniscian/overworld.png',root/'overworld_red_v3/approved_overrides/domniscian.png']:sheet.save(p,bits=4,transparency=0)
meta={'source':str(source.relative_to(R)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frames':rows,'frame_size':[32,32],'reference_visible_height':target_height,'baseline':baseline,'standing_without_desk':True,'palette_unchanged':True,'battle_portrait_unchanged':True}
(R/'docs/nyada-espace-domniscian-20261025/DOMNISCIAN_SOURCE.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
p=root/'overworld_red_v3/manifest.json';m=json.loads(p.read_text());m['latest_selection']='Domniscian debout à la hauteur visible de Maître Nyada (19 pixels); autres sélections conservées.';m['override_source_commits']={'domniscian':None};m['override_origins']={'domniscian':str(source.relative_to(R))};p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(meta)

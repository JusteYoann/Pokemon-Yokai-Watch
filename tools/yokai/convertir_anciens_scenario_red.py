#!/usr/bin/env python3
"""Apply explicit head/body landmarks while converting new art to Red's grid.

Retains the old native art, battle pictures, all palette banks and IDs. The
supplied artwork is resampled in two bands to 10px head +9px body, not painted.
Domniscian's desk extends sideways in its existing 32px object canvas.
"""
import hashlib,json,re,shutil
import numpy as np
from PIL import Image,ImageDraw
from convertir_sprites_scenario import ROOT,BASE,PACK,tight,indexed,runs
source=PACK/'source/royal-desk-red.png';im=Image.open(source).convert('RGBA');h=im.height//2
legacy=PACK/'legacy';legacy.mkdir(exist_ok=True)
reports=[]
for row,name,width,fraction in [(0,'enma',16,0.63),(1,'domniscian',32,0.55)]:
 directory=BASE/name;old=directory/'overworld.png'
 if not (legacy/(name+'-overworld.png')).exists():shutil.copy2(old,legacy/(name+'-overworld.png'))
 palette=[tuple(map(int,line.split())) for line in (directory/'overworld.pal').read_text().splitlines()[3:19]]
 strip=im.crop((0,row*h,im.width,(row+1)*h));cols=runs((np.asarray(strip)[:,:,3]>=128).sum(0)>2,0);assert len(cols)==9,(name,cols)
 sheet=Image.new('P',(width*9,32));sheet.putpalette([v for c in palette for v in c]+[0]*720);sheet.info['transparency']=0
 for i,(x0,x1) in enumerate(cols):
  p,bb=tight(strip.crop((x0,0,x1,h)),True);cut=round(p.height*fraction)
  head=p.crop((0,0,p.width,cut));body=p.crop((0,cut,p.width,p.height))
  # Explicit Red landmark targets, including hair/crown in the ten-pixel head.
  head_height=9 if i in [7,8] else 10
  head=head.resize((14,head_height),Image.Resampling.NEAREST)
  body=body.resize((14 if width==16 else 24,9),Image.Resampling.NEAREST)
  bottom=31 if i in [0,1,2,7,8] else 32;frame=Image.new('RGBA',(width,32))
  left=(1 if i in [0,1,4,5,6] else 0) if width==16 else (width-14)//2
  frame.alpha_composite(head,(left,bottom-9-head_height))
  frame.alpha_composite(body,(left if width==16 else (width-body.width)//2,bottom-9))
  sheet.paste(indexed(frame,palette),(i*width,0))
 sheet.save(old,bits=4,transparency=0)
 overrides=BASE/'overworld_red_v3/approved_overrides';shutil.copy2(old,overrides/(name+'_scenario2026.png'))
 report={'actor':name,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'head_landmark_fraction':fraction,'target_head_height':{'idle_and_vertical_gait':10,'horizontal_gait':9},'target_body_height':9,'visible_height_target':19,'native_frame_width':width,'frames':9,'palette_unchanged':True,'battle_unchanged':True,'old_resource_retained':str((legacy/(name+'-overworld.png')).relative_to(ROOT))}
 reports.append(report)
 # Replace three-pose native table with the nine actual source frames.
 p=ROOT/'src/data/object_events/object_event_pic_tables.h';s=p.read_text();camel='YokaiEnma' if name=='enma' else 'YokaiDomniscian'
 body='\n'+''.join(f'    overworld_frame(gObjectEventPic_{camel}, {width//8}, 4, {i}),\n' for i in range(9))
 s,n=re.subn(r'(static const struct SpriteFrameImage sPicTable_'+camel+r'\[\] = \{).*?(\};)',lambda m:m[1]+body+m[2],s,count=1,flags=re.S);assert n==1;p.write_text(s)
 p=ROOT/'src/data/object_events/object_event_graphics_info.h';s=p.read_text();s,n=re.subn(r'(const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_'+camel+r' = \{.*?\.anims = )sAnimTable_\w+',lambda m:m[1]+'sAnimTable_Standard',s,count=1,flags=re.S);assert n==1;p.write_text(s)
p=BASE/'overworld_red_v3/manifest.json';d=json.loads(p.read_text())
for name in ['enma','domniscian']:d['approved_overrides'][name]='approved_overrides/'+name+'_scenario2026.png'
d['latest_selection']='2026-10-22: user requested Red proportions for all map characters; new Enma/Domniscian nine-frame conversions, old resources retained in scenario_2026/legacy.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=PACK/'manifest.json';d=json.loads(p.read_text());d['adapted_existing']=[{'id':'enma','graphics_id':154,'trainer_pic_id':149,'map_palette_symbol':'gObjectEventPal_YokaiEnma','frame_width':16},{'id':'domniscian','graphics_id':161,'trainer_pic_id':153,'map_palette_symbol':'gObjectEventPal_YokaiDomniscianGroup','frame_width':32}];p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(ROOT/'QA_RECETTE_FINALE/SPRITES_SCENARIO_2026/ANCIENS_RED.json').write_text(json.dumps(reports,indent=2)+'\n')
print('Adapted Enma and Domniscian; battle art/palette banks preserved')

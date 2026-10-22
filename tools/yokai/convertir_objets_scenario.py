#!/usr/bin/env python3
"""Technical crops for Bingo-kai/capsules/Triptic-tac and 128px boss masters."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
from convertir_sprites_scenario import ROOT, BASE, PACK, tight, indexed
source=PACK/'source/bosses-objets.png';im=Image.open(source).convert('RGBA')
colors=[tuple(map(int,l.split())) for l in (BASE/'berenice/overworld.pal').read_text().splitlines()[3:19]]
rects=[(15,845,124,1024),(148,845,257,1024),(273,845,383,1024),(406,845,514,1024),(550,900,642,1024),(680,900,802,1024),(840,880,1008,1024),(1025,880,1191,1024),(1207,902,1285,1024),(1300,898,1480,1024)]
parts=[tight(im.crop(b),True)[0] for b in rects]
reports=[]
for name,indices,size in [('bingo_kai',[0,1,2,3],32),('capsule_souhait',[4,5],16),('triptic_tac',[6,7,8,9],32)]:
 directory=BASE/name;directory.mkdir(exist_ok=True)
 selected=[parts[i] for i in indices]
 # One common scale preserves machine/creature dimensions through animation.
 scale=min((size-2)/max(p.width for p in selected),(size-2)/max(p.height for p in selected))
 sheet=Image.new('P',(size*len(indices),size));sheet.putpalette([v for c in colors for v in c]+[0]*720);sheet.info['transparency']=0
 for i,p in enumerate(selected):
  p=p.resize((max(1,round(p.width*scale)),max(1,round(p.height*scale))),Image.Resampling.NEAREST)
  frame=Image.new('RGBA',(size,size));frame.alpha_composite(p,((size-p.width)//2,size-p.height-1))
  sheet.paste(indexed(frame,colors),(i*size,0))
 sheet.save(directory/'overworld.png',bits=4,transparency=0)
 (directory/'overworld.pal').write_bytes((BASE/'berenice/overworld.pal').read_bytes())
 preview=Image.new('RGB',(size*len(indices)*4, size*4+20),(224,224,224));d=ImageDraw.Draw(preview);d.text((2,2),name,fill='black')
 pp=sheet.convert('RGBA').resize((sheet.width*4,sheet.height*4),Image.Resampling.NEAREST);preview.paste(pp,(0,20),pp);preview.save(directory/'preview.png')
 report={'actor':name,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frame_size':[size,size],'frames':len(indices),'rectangles':[rects[i] for i in indices],'status':'converted_not_yet_engine_tested','note':'Objects and nonhuman clock creature retain reference silhouettes; they are not stretched into human heads/bodies.'}
 (directory/'conversion.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report)
# Keep high-resolution indexed art for the future exceptional boss renderer.
for name,box in [('soranaki_phase1',(1200,307,1536,601)),('soranaki_phase2',(1200,601,1536,901))]:
 p,_=tight(im.crop(box));scale=min(124/p.width,124/p.height);p=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.NEAREST)
 frame=Image.new('RGBA',(128,128));frame.alpha_composite(p,((128-p.width)//2,127-p.height))
 palette=[tuple(map(int,l.split())) for l in (BASE/name/'normal.pal').read_text().splitlines()[3:19]]
 indexed(frame,palette).save(BASE/name/'battle_large.png',bits=4,transparency=0)
 reports.append({'actor':name,'large_master':[128,128],'status':'pixel_master_not_boss_gameplay','palette':'normal.pal'})
(ROOT/'QA_RECETTE_FINALE/SPRITES_SCENARIO_2026/OBJETS_CONVERSION.json').write_text(json.dumps(reports,indent=2)+'\n')
print('Converted three animated objects and two 128px boss masters')

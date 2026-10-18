#!/usr/bin/env python3
"""GBA indexed conversion only: generated shiny-only approved special designs.

Original normal sprites/palettes are never edited. Native aspect ratios preserved
with nearest sampling; shared RGB555 palette for each front/back; zero transparent.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_shiny'
coach=[(0,0,0),(16,16,24),(48,48,56),(96,104,112),(248,248,240),(176,128,24),(232,192,40),(248,224,96),(128,56,16),(208,88,24),(248,128,32),(216,40,24),(16,128,160),(80,200,224),(88,48,160),(160,160,160)]
usa=[(0,0,0),(16,16,24),(32,32,40),(64,80,88),(112,136,144),(160,104,24),(248,216,40),(248,240,104),(0,80,96),(0,144,160),(64,200,208),(240,32,48),(240,240,224),(88,56,112),(168,192,192),(16,48,56)]
jojo=[(0,0,0),(24,16,24),(64,48,64),(144,128,144),(248,240,232),(200,192,192),(176,128,32),(232,192,56),(248,232,96),(96,136,32),(152,184,40),(208,56,56),(160,80,32),(48,48,104),(104,104,200),(232,160,160)]
settings={99:dict(source='specials-beach-emperor-tuxedo.png',row=0,rows=3,width=56,height=54,bottoms=[59,57],palette=coach),100:dict(source='specials-beach-emperor-tuxedo.png',row=1,rows=3,width=40,height=56,bottoms=[60,59],palette=usa),101:dict(source='emperor-cape.png',row=0,rows=1,width=56,height=56,bottoms=[60,60],palette=usa),126:dict(source='specials-beach-emperor-tuxedo.png',row=2,rows=3,width=56,height=50,bottoms=[51,53],palette=jojo)}
report=[]
for n,c in settings.items():
 outdir=D/f'{n:03}';outdir.mkdir(exist_ok=True);path=D/'source'/c['source'];src=Image.open(path).convert('RGBA');colors=[tuple((v>>3)*255//31 for v in rgb) for rgb in c['palette']];frames=[];records=[]
 for col,(name,bottom) in enumerate(zip(['front','back'],c['bottoms'])):
  rect=(col*src.width//2,c['row']*src.height//c['rows'],(col+1)*src.width//2,(c['row']+1)*src.height//c['rows']);im=src.crop(rect);alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0);im.putalpha(alpha);box=alpha.getbbox();assert box;im=im.crop(box)
  scale=min(c['width']/im.width,c['height']/im.height);size=(max(1,round(im.width*scale)),max(1,round(im.height*scale)));im=im.resize(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(64,64));canvas.alpha_composite(im,((64-size[0])//2,bottom-size[1]));out=Image.new('P',(64,64));out.putpalette([v for rgb in colors for v in rgb]+[0]*720)
  out.putdata([0 if a<128 else min(range(1,16),key=lambda i:sum((v-p)**2 for v,p in zip((r,g,b),colors[i]))) for r,g,b,a in canvas.get_flattened_data()]);out.info['transparency']=0;out.save(outdir/f'{name}.png',bits=4,transparency=0);frames.append(out);records.append(dict(view=name,crop=rect,alpha_bbox=box,native_size=size,baseline=bottom))
 (R/f'graphics/yokai/{n:03}/shiny.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,rgb)) for rgb in colors)+'\n')
 view=Image.new('RGB',(512,280));draw=ImageDraw.Draw(view)
 for y in range(0,280,16):
  for x in range(0,512,16):draw.rectangle((x,y,x+15,y+15),fill=(224,224,224) if (x//16+y//16)%2 else (176,176,176))
 draw.text((4,3),f'{n:03} SHINY ONLY - 64x64 x4 - 16 colors',fill='black')
 for i,f in enumerate(frames):im=f.convert('RGBA').resize((256,256),Image.Resampling.NEAREST);view.paste(im,(256*i,24),im)
 view.save(outdir/'preview.png');report.append(dict(number=n,source=str(path.relative_to(R)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),palette_colors=16,transparent_index=0,normal_art_preserved=True,frames=records))
(D/'SPECIALS_CONVERSION.json').write_text(json.dumps(report,indent=2)+'\n')
# Adopt the same per-species presentation as normal, without affecting normal.
p=R/'data/yokai/sprite_presentation.json';profiles=json.loads(p.read_text());old={p['id']:p for p in profiles['profiles']}
for n in settings:
 for a in ['front','back']:
  key=f'{n:03}/{a}'
  if key not in old:continue
  q=dict(old[key]);q['id']=f'{n:03}/shiny-{a}';q['source']=f'graphics/yokai_shiny/{n:03}/{a}.4bpp';q['target']=f'graphics/yokai_shiny/{n:03}/{a}-display.4bpp';q['reason']='Shiny-only derived presentation, same uniform nearest scale and anchor as normal; native verification required.'
  profiles['profiles']=[p for p in profiles['profiles'] if p['id']!=q['id']];profiles['profiles'].append(q)
p.write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n')

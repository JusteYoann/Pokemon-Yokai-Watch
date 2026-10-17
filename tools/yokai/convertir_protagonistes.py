#!/usr/bin/env python3
"""Technical native-format conversion of original generated protagonist artwork.

No drawing/recoloring of original FireRed sprites: audited source rectangles,
nearest-neighbor sizing, binary alpha and a shared 15-color RGB555 palette.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];G=R/'graphics/yokai_characters'
RAW=[(0,0,0),(24,24,32),(80,48,32),(136,80,56),(208,144,104),(248,200,152),(248,224,184),(248,248,240),
     (168,16,40),(232,56,64),(136,144,128),(40,56,80),(112,160,200),(232,120,160),(40,152,152),(144,216,208)]
PALETTE=[tuple((v>>3)*255//31 for v in c) for c in RAW]
FLAT=[v for c in PALETTE for v in c]+[0]*(768-48)
def indexed(im):
 out=Image.new('P',im.size);out.putpalette(FLAT);out.putdata([0 if p[3]<128 else min(range(1,16),key=lambda n:sum((a-b)**2 for a,b in zip(p[:3],PALETTE[n]))) for p in im.get_flattened_data()]);out.info['transparency']=0;return out
def sheet(frames,vertical=False):
 w,h=frames[0].size;out=Image.new('P',(w,h*len(frames)) if vertical else (w*len(frames),h));out.putpalette(FLAT)
 for i,f in enumerate(frames):out.paste(f,(0,i*h) if vertical else (i*w,0))
 out.info['transparency']=0;return out
def fit(c,size,scale=None,bottom=None):
 if scale is None:scale=min((size[0]-2)/c.width,(size[1]-2)/c.height)
 v=c.resize((max(1,round(c.width*scale)),max(1,round(c.height*scale))),Image.Resampling.NEAREST)
 out=Image.new('RGBA',size);out.alpha_composite(v,((size[0]-v.width)//2,(bottom if bottom is not None else size[1]-1)-v.height));return indexed(out)
def save(im,path):im.save(path,bits=4,transparency=0)
def load_pack(directory,pack):
 src=Image.open(directory/pack['source']).convert('RGBA');parts=[]
 for rect in pack['rectangles']:
  c=src.crop(rect);alpha=c.getchannel('A').point(lambda x:255 if x>=128 else 0);c.putalpha(alpha);bbox=alpha.getbbox();assert bbox,rect;parts.append(c.crop(bbox))
 return parts
def actor_body_height(im):
 # Locate the brown hair cluster; ignore thin brown rods above it. This only
 # normalizes source scale, never draws or morphs a character.
 counts=[]
 for y in range(im.height):
  counts.append(sum(a>=128 and r>g*1.2 and g>b*1.1 and r<185 and g<135 and b<110 for r,g,b,a in [im.getpixel((x,y)) for x in range(im.width)]))
 threshold=max(3,max(counts)*0.15);top=next((i for i,n in enumerate(counts) if n>=threshold),0)
 return im.height-top
for name in ['nathan','katie']:
 d=G/name;spec=json.loads((d/'production.json').read_text());core=spec['core'];p=d/core['source'];source=Image.open(p).convert('RGBA');crops=[]
 for rect in core['rectangles']:
  im=source.crop(rect);a=im.getchannel('A').point(lambda x:255 if x>=128 else 0);im.putalpha(a);bbox=a.getbbox();assert bbox,rect;crops.append(im.crop(bbox))
 front=fit(crops[core['trainer_front']],(64,64));save(front,d/'front.png')
 poses=[crops[i] for i in core['trainer_back']];scale=min(60/max(c.width for c in poses),62/max(c.height for c in poses));back=[fit(c,(64,64),scale) for c in poses];save(sheet(back,True),d/'back.png')
 poses=[crops[i] for i in core['normal']];scale=min(16/max(c.width for c in poses),20/max(c.height for c in poses));walk=[fit(c,(16,32),scale,bottom=31) for c in poses];save(sheet(walk),d/'normal.png')
 icon=fit(crops[core['region_icon']],(16,16));save(icon,d/'region_icon.png')
 # The introduction uses 8bpp indices in BG palette bank4, not ordinary 4bpp.
 intro4=fit(crops[core['trainer_front']],(64,96),bottom=94)
 intro=Image.new('P',(64,96));ip=[0]*768;ip[:3]=[115,197,164]
 for i,c in enumerate(PALETTE):ip[(64+i)*3:(65+i)*3]=[115,197,164] if i==0 else c
 intro.putpalette(ip);intro.putdata([0 if n==0 else n+64 for n in intro4.get_flattened_data()]);intro.save(d/'intro.png',bits=8)
 (d/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in PALETTE)+'\n')
 for file,amount,tint in [('reflection.pal',0.32,(248,248,248)),('bridge_reflection.pal',0.28,(208,216,224))]:
  colors=[(0,0,0)]+[tuple((round((v*(1-amount)+t*amount)/8)*8>>3)*255//31 for v,t in zip(c,tint)) for c in RAW[1:]]
  (d/file).write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
 (d/'intro.pal').write_text('JASC-PAL\n0100\n32\n'+'\n'.join(' '.join(map(str,c)) for c in [(115,197,164)]+PALETTE[1:]+[(0,0,0)]*16)+'\n')
 preview=Image.new('RGB',(640,430))
 for y in range(preview.height):
  for x in range(preview.width):preview.putpixel((x,y),(224,224,224) if (x//16+y//16)%2 else (176,176,176))
 def paste(im,xy,scale):
  a=im.convert('RGBA').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST);preview.paste(a,xy,a)
 paste(front,(0,20),3)
 for i,im in enumerate(back):paste(im,(i*126,220),2)
 for i,im in enumerate(walk):paste(im,(200+i*48,40),3)
 ImageDraw.Draw(preview).text((4,4),name+' — SOURCE ART ONLY / NOT ACTIVE',fill=(0,0,0));preview.save(d/'core-preview.png')
 if 'motion' in spec:
  pack=spec['motion'];parts=load_pack(d,pack)
  def group(indices,height,bottom=31,width=16):
   v=[parts[i] for i in indices];sc=min(width/max(c.width for c in v),height/max(c.height for c in v));return [fit(c,(width,32),sc,bottom) for c in v]
  run=group(pack['run'],22);surf=group(pack['surf'],18,30);turns=group(pack['head_turns'],20)
  save(sheet(surf+run+turns),d/'surf_run.png')
 if 'actions' in spec:
  pack=spec['actions'];parts=load_pack(d,pack)
  # Enlarging this action's frame to32x32 preserves normal character size
  # while allowing a raised watch; integration must update its metadata too.
  v=[parts[i] for i in pack['item']];v=[c.resize((round(c.width*200/actor_body_height(c)),round(c.height*200/actor_body_height(c))),Image.Resampling.NEAREST) for c in v];sc=min(31/max(c.width for c in v),31/max(c.height for c in v),20/200)
  actions=[fit(c,(32,32),sc) for c in v];save(sheet(actions),d/'item.png')
  if 'north_fishing' in spec:
   north=load_pack(d,spec['north_fishing']);fishing=[parts[i] for i in pack['fish']]
   fishing[4:8]=north
   # Body-scale normalization is recorded per source before the final32x32 fit.
   heights=[actor_body_height(c) for c in fishing]
   normalized=[c.resize((round(c.width*200/h),round(c.height*200/h)),Image.Resampling.NEAREST) for c,h in zip(fishing,heights)]
   sc=min(30/max(c.width for c in normalized),30/max(c.height for c in normalized),20/200)
   save(sheet([fit(c,(32,32),sc) for c in normalized]),d/'fish.png')
 if 'supplement' in spec:
  pack=spec['supplement'];fixed=load_pack(d,pack);credits=[fixed[i] for i in pack['credits']]
  sc=min(58/max(c.width for c in credits),54/max(c.height for c in credits));save(sheet([fit(c,(64,64),sc) for c in credits],True),d/'credits.png')
 if 'equipment' in spec:
  pack=spec['equipment'];src=Image.open(d/pack['source']).convert('RGBA');parts=[]
  for rect in pack['rectangles']:
   c=src.crop(rect);alpha=c.getchannel('A').point(lambda x:255 if x>=128 else 0);c.putalpha(alpha);bbox=alpha.getbbox();assert bbox,rect;parts.append(c.crop(bbox))
  scale=min(30/max(c.width for c in parts),30/max(c.height for c in parts))
  equipment=[fit(c,(32,32),scale) for c in parts]
  save(sheet([equipment[i] for i in pack['bike']]),d/'bike.png')
  save(sheet([equipment[i] for i in pack['vs_seeker_bike']]),d/'vs_seeker_bike.png')
  v=Image.new('RGB',(512,512),(224,224,224))
  for y in range(v.height):
   for x in range(v.width):v.putpixel((x,y),(224,224,224) if (x//16+y//16)%2 else (176,176,176))
  for i,f in enumerate(equipment):
   a=f.convert('RGBA').resize((128,128),Image.Resampling.NEAREST);v.paste(a,((i%4)*128,(i//4)*128),a)
  v.save(d/'equipment-preview.png')
 (d/'conversion.json').write_text(json.dumps({'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_dimensions':source.size,'native_front':[64,64],'native_back':[64,64,5],'native_walk':[16,32,9],'native_walk_height':20,'palette_colors':16,'transparent_index':0,'intro':'8bpp, opaque indices65..79, bank4 palette','integrated':('graphics/yokai_characters/'+name+'/normal.4bpp') in (R/'src/data/object_events/object_event_graphics.h').read_text(),'completed_source_packs':[k for k in ['core','equipment','motion','actions','supplement','north_fishing'] if k in spec],'remaining_source_packs':[k for k in ['equipment','motion','actions','supplement','north_fishing'] if k not in spec],'remaining':'Native field and battle fixtures passed; full intro, Surf, card, Hall of Fame and credits still require dedicated checks (see QA reports)'},ensure_ascii=False,indent=2)+'\n')

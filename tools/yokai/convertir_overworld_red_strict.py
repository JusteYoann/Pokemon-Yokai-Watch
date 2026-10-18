#!/usr/bin/env python3
"""Native frame/palette conversion of individually redrawn Red-template actors.

Artwork comes exclusively from imagegen. This tool crops, samples to the native
Red frame bounds and assigns existing palette indices; it does not paint shapes.
Mafia clones share exactly one indexed map resource. Employees share geometry
and differ only by a declared suit-index variant in their existing shared bank.
"""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters';S=D/'overworld_red_v3/source';Q=R/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/RED_STRICT_V3';Q.mkdir(parents=True,exist_ok=True)
def runs(bits,gap=6):
 out=[];start=last=None
 for i,v in enumerate(bits):
  if not v:continue
  if start is None:start=i
  if last is not None and i-last>gap+1:out.append((start,last+1));start=i
  last=i
 if start is not None:out.append((start,last+1))
 return out
def figures(path,count):
 im=Image.open(path).convert('RGBA');a=np.asarray(im)[:,:,3]>=128;boxes=[]
 for y,b in runs(a.sum(1)>3):
  if b-y<=30:continue
  for x,r in runs(a[y:b].sum(0)>3):
   if r-x<=20:continue
   p=im.crop((x,y,r,b));p.putalpha(p.getchannel('A').point(lambda v:255 if v>=128 else 0));bb=p.getbbox()
   if bb:boxes.append((x+bb[0],y+bb[1],x+bb[2],y+bb[3]))
 assert len(boxes)==count,(path,len(boxes),count)
 return im,boxes
red=Image.open(R/'graphics/object_events/pics/people/red_normal.png').convert('RGBA');report=[];views=[]
def palette(actor):return [tuple(map(int,l.split())) for l in (D/actor/'normal.pal').read_text().splitlines()[3:19]]
def convert(actor,source,width=16,count=3,source_count=None,selection=None):
 im,boxes=figures(source,source_count or count)
 if selection is not None:boxes=[boxes[i] for i in selection]
 colors=palette(actor);flat=[v for c in colors for v in c]+[0]*720;sheet=Image.new('P',(width*count,32));sheet.putpalette(flat);sheet.info['transparency']=0;poses=[]
 for i,b in enumerate(boxes):
  target=red.crop((16*i,0,16*(i+1),32)).getbbox();assert target
  p=im.crop(b).resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.NEAREST)
  def color_index(r,g,b,a):
   if a<128:return 0
   candidates=range(1,16)
   # Shared boss bank has skin-pink entries but no neutral gray. Keep the
   # employee's neutral ghost head/collar in its cream/white/outline subset,
   # rather than letting nearest RGB turn gray shading into pink skin.
   if actor=='employe_rouge':candidates=[1,9,15] if max(r,g,b)-min(r,g,b)<45 else [k for k in range(1,16) if k not in [7,8]]
   return min(candidates,key=lambda k:sum((v-c)**2 for v,c in zip((r,g,b),colors[k])))
  quant=[color_index(*pixel) for pixel in p.get_flattened_data()]
  small=Image.new('P',p.size);small.putpalette(flat);small.putdata(quant);frame=Image.new('P',(width,32));frame.putpalette(flat);frame.info['transparency']=0;frame.paste(small,(target[0]+(width-16)//2,target[1]));assert frame.getbbox()
  sheet.paste(frame,(width*i,0));mask=np.asarray(frame.crop(((width-16)//2,0,(width+16)//2,32)))>0;ref=np.asarray(red.crop((16*i,0,16*(i+1),32)))[:,:,3]>0
  poses.append(dict(frame=i,source_bbox=b,red_target_bbox=target,visible_bbox=frame.getbbox(),alpha_iou_with_red=float((mask&ref).sum()/(mask|ref).sum()),row_width_mean_difference_from_red=float(np.abs(mask.sum(1).astype(int)-ref.sum(1)).mean())))
  views.append((actor,i,frame.copy()))
 sheet.save(D/actor/'overworld.png',bits=4,transparency=0)
 report.append(dict(actor=actor,source=str(source.relative_to(R)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),frame_width=width,frame_height=32,frames=count,palette_sha256=hashlib.sha256((D/actor/'normal.pal').read_bytes()).hexdigest(),poses=poses))
 return sheet

for actor in ['nathaniel','wyatt','don_morleone','ariane','michael','enma','domniscian']:
 source=S/(actor+'.png')
 if source.exists():convert(actor,source,32 if actor=='domniscian' else 16)
source=S/'mafiamille.png'
if source.exists():
 convert('mafiamille_1',source)
 for actor in ['mafiamille_2','mafiamille_3']:
  assert palette(actor)==palette('mafiamille_1');(D/actor/'overworld.png').write_bytes((D/'mafiamille_1/overworld.png').read_bytes())
  report.append(dict(actor=actor,exact_indexed_clone_of='mafiamille_1',battle_portrait_unchanged=True))
  im=Image.open(D/actor/'overworld.png')
  for i in range(3):views.append((actor,i,im.crop((i*16,0,(i+1)*16,32))))
source=S/'employe.png'
if source.exists():
 sheet=convert('employe_rouge',source);assert palette('employe_bleu')==palette('employe_rouge')
 lut=list(range(256));lut[4]=10;lut[5]=10;lut[6]=2
 blue=sheet.point(lut);blue.putpalette(sheet.getpalette());blue.info['transparency']=0;blue.save(D/'employe_bleu/overworld.png',bits=4,transparency=0)
 assert np.array_equal(np.asarray(sheet)>0,np.asarray(blue)>0)
 report.append(dict(actor='employe_bleu',exact_geometry_of='employe_rouge',shared_head_and_body=True,suit_index_variant={4:10,5:10,6:2},battle_portrait_unchanged=True))
 for i in range(3):views.append(('employe_bleu',i,blue.crop((i*16,0,(i+1)*16,32))))
# Matt already has coherent Red-like poses; bring all nine native bounds and
# foot anchors onto Red, preserving its individually drawn gait and identity.
if (S/'matt.png').exists():convert('matt',S/'matt.png',16,9)
# Ariane's existing compact drawing is retained; only its native bounds and
# anchoring are normalized from20px to Red19px. Katie already uses19px and is
# deliberately preserved across all59 player frames, like approved Nathan.
convert('ariane',D/'overworld_frlg_v2/source/group-a.png',source_count=12,selection=[0,1,2])
sheet=Image.new('RGB',(768,((len(views)+7)//8)*148),(224,224,224));draw=ImageDraw.Draw(sheet)
for k,(actor,i,im) in enumerate(views):
 x=k%8*96;y=k//8*148;draw.text((x+2,y+2),actor[:14],fill='black');draw.text((x+2,y+14),str(i),fill='black');p=im.convert('RGBA').resize((im.width*3,96),Image.Resampling.NEAREST);sheet.paste(p,(x+(96-p.width)//2,y+36),p)
sheet.save(Q/'NATIFS_X3.png');(Q/'CONVERSION.json').write_text(json.dumps(dict(artwork='Individually generated edits of original Red pose guide',no_palette_changes=True,assets=report),indent=2)+'\n');print('Converted actors:',len(report))

#!/usr/bin/env python3
"""Mechanical crop/nearest-neighbor RGB555 indexing of supplied/generated sources.
No repainting: preserve sources and record every native output/height for review.
"""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'graphics/dossier-20261023/source';D=R/'docs/dossier-20261023/demande';results=[]
def crop(im):
 im=im.convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));b=im.getchannel('A').getbbox();assert b;return im.crop(b)
def fit(im,size,visible_h=None):
 im=crop(im);scale=min((size[0]-2)/im.width,(visible_h or size[1]-4)/im.height)
 im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.NEAREST)
 frame=Image.new('RGBA',size);frame.alpha_composite(im,((size[0]-im.width)//2,size[1]-1-im.height));return frame

def indexed(frames,palette=None):
 if palette is None:
  colors=[p[:3] for im in frames for p in im.getdata() if p[3]]
  atlas=Image.new('RGB',(len(colors),1));atlas.putdata(colors);raw=atlas.quantize(colors=14,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).getpalette()
  palette=[(0,0,0),(0,0,0)]+[tuple((v>>3)*255//31 for v in raw[i:i+3]) for i in range(0,42,3)]
 out=[]
 for im in frames:
  frame=Image.new('P',im.size);frame.putpalette([v for c in palette for v in c]+[0]*720)
  frame.putdata([0 if not p[3] else min(range(1,16),key=lambda k:sum((a-b)**2 for a,b in zip(p[:3],palette[k]))) for p in im.getdata()]);frame.info['transparency']=0;out.append(frame)
 return out,palette

def save(frames,dest,paths):
 dest.mkdir(parents=True,exist_ok=True);frames,pal=indexed(frames)
 for f,n in zip(frames,paths):f.save(dest/n,bits=4,transparency=0)
 (dest/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in pal)+'\n')
 return frames

# First native pose from provided two-pose sheets; no invented walking cycle.
specs=[('zazel','Zazel',D/'library_originals/Nintendo Switch - Yo-kai Watch 4++ - Yo-kai (Onnen Tribe) - Zazel.png',19),('orqanos','Orqanos',D/'library_originals/Nintendo Switch - Yo-kai Watch 4++ - Yo-kai (Oni Tribe) - Orcanos(1).png',22),('nyada','Nyada',D/'library_originals/Nintendo Switch - Yo-kai Watch 4++ - Yo-kai (Mononoke Tribe) - Master Nyada.png',19),('kyubi','Kyubi',D/'references/kyubi_overworld_yw4.png',19),('octorgone','Octorgone',D/'references/octorgone_overworld_yw4.png',19)]
for name,symbol,path,height in specs:
 im=Image.open(path);im=im.crop((0,0,im.width,im.height//2));dest=R/'graphics/dossier-20261023'/name
 f=save([fit(im,(32,32),height)],dest,['overworld.png'])[0]
 results.append({'name':name,'source':str(path.relative_to(R)),'role':'static overworld','height':f.convert('RGBA').getchannel('A').getbbox()[3]-f.convert('RGBA').getchannel('A').getbbox()[1],'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
# Latest user-provided Ancient Enma sheet has priority over earlier artwork adaptation.
f=save([fit(Image.open(S/'enma-ancien-overworld.png'),(32,32),22)],R/'graphics/dossier-20261023/enma_ancien',['overworld.png'])[0]
results.append({'name':'enma_ancien','role':'static overworld','height':22,'source':'Latest user sprite sheet, transparent extraction through image tool; full generated source retained for review.'})
# Trainer portraits: requested new references of Zazel/Nyada supersede archived attempts.
im=Image.open(S/'portraits-zazel-nyada-corriges.png');w,h=im.size
for name,box in [('zazel',(0,0,w//2,h)),('nyada',(w//2,0,w,h))]:save([fit(im.crop(box),(64,64),60)],R/'graphics/dossier-20261023'/name,['battle.png'])
# Need one palette for both battle portrait and overworld for each? Native tags are separate,
# so keep overworld.pal before assigning normal.pal from the portrait below.
# Recreate OW palette deterministically from original source; battle keeps its own normal.pal.
for name,_,path,height in specs:
 dest=R/'graphics/dossier-20261023'/name
 frames,pal=indexed([fit(Image.open(path).crop((0,0,144,110)),(32,32),height)])
 frames[0].save(dest/'overworld.png',bits=4,transparency=0)
 (dest/'overworld.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in pal)+'\n')
im=Image.open(S/'combat-enma-orqanos-nyada.png');w,h=im.size
save([fit(im.crop((0,h//2,w//2,h)),(64,64),60)],R/'graphics/dossier-20261023/orqanos',['battle.png'])
# Reuse recovered Ancient Enma portrait; retain its native, already indexed palette.
dest=R/'graphics/dossier-20261023/enma_ancien';(dest/'overworld.pal').write_text((dest/'normal.pal').read_text())
save([fit(Image.open(S/'enma-ancien-portrait-reference-finale.png'),(64,64),60)],dest,['battle.png'])
# Full sword-design front/back, a common palette, no anisotropic display stretch.
dest=R/'graphics/yokai/150';frames=save([fit(im.crop((0,0,w//2,h//2)),(64,64),58),fit(im.crop((w//2,0,w,h//2)),(64,64),58)],dest,['front.png','back.png'])
(dest/'shiny.pal').write_text((dest/'normal.pal').read_text())
# Seigneur Enma already has a dedicated royal overworld. Match Nathan's19 px while keeping all poses.
# Domniscian's user-confirmed three views already exist; preserve their native palette.
for name,frame_width in [('enma',16),('domniscian',32)]:
 p=R/'graphics/yokai_characters'/name/'overworld.png';orig=p.with_name('overworld-before-dossier.png')
 approved=R/'graphics/yokai_characters/overworld_red_v3/approved_overrides'/(name+'.png')
 if approved.exists():
  p.write_bytes(approved.read_bytes());results.append({'name':name,'method':'Approved native override preserved without a second resize','source':str(approved.relative_to(R))});continue
 if not orig.exists():orig.write_bytes(p.read_bytes())
 im=Image.open(orig);pal=im.getpalette();out=Image.new('P',im.size);out.putpalette(pal)
 boxes=[]
 for x in range(0,im.width,frame_width):
  c=im.crop((x,0,x+frame_width,32));rgba=c.convert('RGBA');rgba.putalpha(c.point(lambda v:255 if v else 0).convert('L'));b=rgba.getchannel('A').getbbox();sprite=c.crop(b);scale=19/sprite.height;sprite=sprite.resize((max(1,round(sprite.width*scale)),19),Image.Resampling.NEAREST)
  out.paste(sprite,(x+(frame_width-sprite.width)//2,31-19));boxes.append(sprite.size)
 out.save(p,bits=4,transparency=0);results.append({'name':name,'height':19,'poses':boxes,'method':'nearest indexed sampling; original saved; unchanged native palette'})
(R/'docs/dossier-20261023/graphismes.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
# Preview is a technical native upscaling for review, not an in-game screenshot.
frames=[(n,Image.open(R/'graphics/dossier-20261023'/n/'overworld.png').convert('RGBA')) for n in ['zazel','enma_ancien','orqanos','nyada','kyubi','octorgone']]
from PIL import ImageDraw
preview=Image.new('RGB',(32*8*len(frames),32*8+24),(40,48,56));draw=ImageDraw.Draw(preview)
for i,(n,f) in enumerate(frames):preview.paste(f.resize((256,256),Image.Resampling.NEAREST),(i*256,24),f.resize((256,256),Image.Resampling.NEAREST));draw.text((i*256+4,4),n,fill='white')
preview.save(R/'docs/dossier-20261023/planche-overworld-x8.png')

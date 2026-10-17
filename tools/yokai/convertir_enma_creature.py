#!/usr/bin/env python3
"""Technical crop, nearest-neighbor sampling and GBA indexing of original artwork."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'graphics/yokai_characters/enma_creature';source=D/'source/generated-sprite.png'
im=Image.open(source).convert('RGBA');alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0);im.putalpha(alpha);box=alpha.getbbox();assert box
crop=im.crop(box);scale=min(30/crop.width,31/crop.height);crop=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.NEAREST)
frame=Image.new('RGBA',(32,32));frame.alpha_composite(crop,((32-crop.width)//2,32-crop.height))
# Quantization is solely technical; the source drawing and original species assets stay intact.
colors=[rgb[:3] for rgb in frame.getdata() if rgb[3]];atlas=Image.new('RGB',(len(colors),1));atlas.putdata(colors)
quantized=atlas.quantize(colors=15,method=Image.Quantize.MEDIANCUT);raw=quantized.getpalette();palette=[(0,0,0)]+[tuple((v>>3)*255//31 for v in raw[i:i+3]) for i in range(0,45,3)]
indexed=Image.new('P',(32,32));indexed.putpalette([v for rgb in palette for v in rgb]+[0]*720)
indexed.putdata([0 if not a else min(range(1,16),key=lambda k:sum((v-p)**2 for v,p in zip((r,g,b),palette[k]))) for r,g,b,a in frame.getdata()]);indexed.info['transparency']=0;indexed.save(D/'overworld.png',bits=4,transparency=0)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
preview=Image.new('RGB',(256,256));pix=preview.load()
for y in range(256):
 for x in range(256):pix[x,y]=(224,224,224) if (x//16+y//16)%2 else (176,176,176)
sprite=indexed.convert('RGBA').resize((256,256),Image.Resampling.NEAREST);preview.paste(sprite,(0,0),sprite);preview.save(D/'preview-checkerboard.png')
(D/'conversion.json').write_text(json.dumps({'species':150,'species_constant':'SPECIES_MEWTWO','role':'Capturable artificial celestial feline Enma, not human Lord Enma NPC','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_dimensions':list(im.size),'crop':box,'native_dimensions':[32,32],'transparent_index':0,'palette_colors':16,'animation':'Single stationary front frame, native inanimate object; no movement scene','reference':'graphics/yokai/150/front.png; approved battle art untouched'},ensure_ascii=False,indent=2)+'\n')

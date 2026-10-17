#!/usr/bin/env python3
"""Technical asset conversion of generated original artwork; no character redrawing.

The model did not obey the requested canvas/grid. Explicit audited rectangles isolate
actual sprites; nearest-neighbor sampling, binary alpha and 15-color GBA quantization
produce engine assets. The original generated sheet remains preserved verbatim.
"""
from pathlib import Path
import hashlib,json
from PIL import Image
R=Path(__file__).resolve().parents[2];D=R/'graphics/yokai_characters/matt';D.mkdir(exist_ok=True)
source=D/'source/generated-sheet.png';im=Image.open(source).convert('RGBA')
# Actual content rows/columns inspected on the returned 1254px source, NOT assumed 1024px.
rects=[(45,20,280,400),(325,20,645,400),(690,20,915,400),
       (75,430,240,670),(393,430,550,670),(705,430,865,670),(1015,430,1180,670),
       (75,715,235,960),(393,715,550,960),(706,715,862,960),(1020,715,1183,960),(70,1005,235,1230)]
crops=[]
for box in rects:
 c=im.crop(box);alpha=c.getchannel('A').point(lambda p:255 if p>=128 else 0)
 c.putalpha(alpha);c=c.crop(alpha.getbbox());crops.append(c)
# Uniform scale within each role, maintaining native silhouettes and walking head size.
frames=[]
for index,c in enumerate(crops):
 w,h=(64,64) if index<3 else (16,32)
 scale=min(60/max(x.height for x in crops[:3]),60/max(x.width for x in crops[:3])) if index<3 else min(28/max(x.height for x in crops[3:]),16/max(x.width for x in crops[3:]))
 resized=c.resize((max(1,round(c.width*scale)),max(1,round(c.height*scale))),Image.Resampling.NEAREST)
 frame=Image.new('RGBA',(w,h),(0,0,0,0));frame.alpha_composite(resized,((w-resized.width)//2,h-resized.height-1));frames.append(frame)
# Shared 15-color palette; opaque colors rounded to RGB555 before quantization.
colors=[]
for frame in frames:
 for red,green,blue,alpha in frame.getdata():
  if alpha:colors.append(((red>>3)*255//31,(green>>3)*255//31,(blue>>3)*255//31))
# Fifteen representative source hues: protect orange headphones and olive jacket
# from being discarded by a frequency-only quantizer in favor of near-black AA shades.
palette=[(0,0,0),(24,24,32),(64,40,24),(104,64,24),(152,96,32),(192,144,64),
         (248,192,144),(248,224,192),(208,144,104),(56,72,32),(104,112,48),
         (152,160,80),(240,240,224),(32,48,72),(64,96,144),(224,104,24)]
palette=[tuple((v>>3)*255//31 for v in rgb) for rgb in palette]
flat=[v for rgb in palette for v in rgb]
for index,frame in enumerate(frames):
 pixels=[]
 for red,green,blue,alpha in frame.getdata():
  if not alpha:pixels.append(0);continue
  pixels.append(min(range(1,16),key=lambda k:sum((v-p)**2 for v,p in zip((red,green,blue),palette[k]))))
 indexed=Image.new('P',frame.size);indexed.putpalette(flat+[0]*(768-len(flat)));indexed.putdata(pixels);indexed.info['transparency']=0
 frames[index]=indexed
for index,name in enumerate(['battle_early','battle_late','battle_champion']):frames[index].save(D/(name+'.png'),bits=4,transparency=0)
ow=Image.new('P',(144,32));ow.putpalette(frames[3].getpalette());ow.info['transparency']=0
for i,f in enumerate(frames[3:]):ow.paste(f,(i*16,0))
ow.save(D/'overworld.png',bits=4,transparency=0)
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,rgb)) for rgb in palette)+'\n')
# Preview only: opaque checkerboard; assets retain indexed transparency.
preview=Image.new('RGB',(3*256,420))
for y in range(preview.height):
 for x in range(preview.width):preview.putpixel((x,y),(224,224,224) if (x//16+y//16)%2 else (176,176,176))
for i,f in enumerate(frames[:3]):
 rgb=f.convert('RGBA').resize((256,256),Image.Resampling.NEAREST);preview.paste(rgb,(i*256,0),rgb)
for i,f in enumerate(frames[3:]):
 rgb=f.convert('RGBA').resize((64,128),Image.Resampling.NEAREST);preview.paste(rgb,(i*80+24,280),rgb)
preview.save(D/'preview-checkerboard.png')
metadata={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_dimensions':list(im.size),'audited_crop_rectangles':rects,
 'native_frames':{'battle':[64,64,3],'overworld':[16,32,9]},'opaque_palette_colors':15,'transparent_index':0,
 'technical_conversion':['binary alpha threshold 128','uniform nearest-neighbor sampling per role','shared RGB555 palette, retaining distinct orange and olive source hues'],
 'orientation_note':'Generated walk frame 7 faces right; engine animation flips that frame in west direction and leaves it unflipped in east direction.',
 'artwork_review':'Recognizable Matt, original drawing. Pixel-scale and walking fidelity require in-game review before acceptance.'}
(D/'conversion.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
print(metadata)

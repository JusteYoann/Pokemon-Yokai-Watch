#!/usr/bin/env python3
"""Technical crop, area resampling preserving source ink coverage, and shared GBA palette conversion.

The drawing is generated separately; this converter does not invent artwork.
"""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'graphics/yokai_characters/dr_jobard'
source=OUT/'source/proposition.png'
im=Image.open(source).convert('RGB');w,h=im.size
nathan=Image.open(ROOT/'graphics/yokai_characters/nathan/normal.png')
sheet=Image.new('RGB',(64,32),(255,0,255));boxes=[]
for i in range(4):
    # Remove only the generated sheet's white panel dividers.
    frame=im.crop((i*w//4+16,0,(i+1)*w//4-16,h)).convert('RGBA')
    mask=Image.new('L',frame.size);mask.putdata([0 if min(r,b)>50 and max(r,b)<2*min(r,b) and g<0.6*min(r,b) else 255 for r,g,b,a in frame.getdata()])
    frame.putalpha(mask);box=mask.getbbox();assert box;frame=frame.crop(box)
    j=min(i,2)
    reference=nathan.crop((16*j,0,16*(j+1),32))
    if i==3:reference=reference.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    reference_mask=Image.new('L',reference.size);reference_mask.putdata([255 if k else 0 for k in reference.getdata()])
    target=reference_mask.getbbox();assert target
    size=(target[2]-target[0],target[3]-target[1])
    # Point sampling dropped source contours thinner than one destination pixel.
    # Preserve their measured coverage instead of inventing an outline afterward.
    ink=Image.new('L',frame.size)
    ink.putdata([255 if a and max(r,g,b)<70 else 0 for r,g,b,a in frame.getdata()])
    ink=ink.resize(size,Image.Resampling.BOX)
    point=frame.resize(size,Image.Resampling.NEAREST)
    area=frame.resize(size,Image.Resampling.BOX)
    # Keep the original point-sampled interior (eye, iris, heart). Only source
    # ink on the silhouette boundary receives conservative coverage sampling.
    pixels=[]
    for yy in range(size[1]):
        for xx in range(size[0]):
            r,g,b,a=area.getpixel((xx,yy))
            border=any(nx<0 or ny<0 or nx>=size[0] or ny>=size[1]
                       or area.getpixel((nx,ny))[3]<1
                       for nx,ny in [(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)])
            pr,pg,pb,pa=point.getpixel((xx,yy))
            if a<1:pixels.append((0,0,0,0))
            elif border and ink.getpixel((xx,yy))>=64:pixels.append((0,0,0,255))
            else:pixels.append((pr,pg,pb,255) if pa else (r,g,b,255))
    frame=Image.new('RGBA',size);frame.putdata(pixels)
    x=i*16+target[0];y=target[1]
    sheet.paste(frame,(x,y),frame);boxes.append([x-i*16,y,x-i*16+frame.width,y+frame.height])
q=sheet.quantize(colors=16,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
pal=q.getpalette();used=sorted(set(q.getdata()));bg=min(used,key=lambda k:sum((pal[3*k+j]-[255,0,255][j])**2 for j in range(3)))
order=[bg]+[x for x in used if x!=bg];mapping={k:i for i,k in enumerate(order)}
colors=[(0,0,0)]+[tuple((pal[3*k+j]>>3)<<3 for j in range(3)) for k in order[1:]]
colors+= [(0,0,0)]*(16-len(colors))
result=Image.new('P',sheet.size);result.putpalette([c for rgb in colors for c in rgb]+[0]*720);result.putdata([mapping[k] for k in q.getdata()]);result.info['transparency']=0
result.save(OUT/'overworld.png',bits=4,transparency=0)
(OUT/'overworld.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,rgb)) for rgb in colors)+'\n')
preview=Image.new('RGB',result.size,(192,192,192));rgba=result.convert('RGBA');preview.paste(rgba,(0,0),rgba);preview.resize((512,256),Image.Resampling.NEAREST).save(OUT/'preview-x8.png')
(OUT/'production.json').write_text(json.dumps(dict(status='Simplified adaptation of the creator-provided Dr Jobard artwork; cables, apparatus and claws removed; exact Nathan visible dimensions',reference='Dr Jobard artwork supplied in conversation on 2026-10-22',size_reference='graphics/yokai_characters/nathan/normal.png',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),logical_frame=[16,32],frames=['front','back','left','right; distinct drawing preserves split skin colors'],opaque_bounds=boxes,palette_colors=16,transparent_index=0,method=__doc__),indent=2)+'\n')
print('Converted',boxes)

#!/usr/bin/env python3
"""Crop generated original art and convert to indexed native GBA resources.

No drawing: retains source PNG, records every crop and uses nearest-neighbour
sampling, shared 15-colour RGB555 palette and transparent index zero.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'graphics/yokai_characters'
PACK = BASE / 'scenario_2026'
RED = Image.open(ROOT / 'graphics/object_events/pics/people/red_normal.png').convert('RGBA')

def runs(bits, gap=8):
    out = []; start = last = None
    for i, b in enumerate(bits):
        if not b: continue
        if start is None: start = i
        if last is not None and i-last > gap+1:
            out.append((start, last+1)); start = i
        last = i
    if start is not None: out.append((start, last+1))
    return out

def tight(im, primary=False):
    im = im.copy()
    im.putalpha(im.getchannel('A').point(lambda a: 255 if a >= 128 else 0))
    if primary:
        a=np.asarray(im)[:,:,3]>=128
        bands=runs(a.sum(1)>0,8)
        if len(bands)>1:
            top,bottom=max(bands,key=lambda band:int(a[band[0]:band[1]].sum()))
            # Exclude fragments from neighboring rows, retain all pixels of this figure.
            box=im.crop((0,top,im.width,bottom)).getchannel('A').getbbox()
            return im.crop((box[0],top+box[1],box[2],top+box[3])), (box[0],top+box[1],box[2],top+box[3])
    box = im.getchannel('A').getbbox()
    if not box: raise ValueError('Empty character crop')
    return im.crop(box), box

def indexed(im, palette):
    arr = np.asarray(im); out = np.zeros(arr.shape[:2], dtype=np.uint8)
    opaque = arr[:,:,3] >= 128
    rgb = arr[:,:,:3][opaque].astype(np.int32)
    pal = np.asarray(palette[1:], dtype=np.int32)
    out[opaque] = 1 + np.argmin(((rgb[:,None,:]-pal[None,:,:])**2).sum(2), axis=1)
    p = Image.fromarray(out, 'P'); p.putpalette([v for c in palette for v in c] + [0]*720)
    p.info['transparency'] = 0
    return p

def character(actor, source, row, portrait_box=None, row_span=None, selection=None, flips=None, alternate=None, map_limit=1200):
    im = Image.open(source).convert('RGBA'); h = im.height//4
    y0,y1 = row_span or (row*h,(row+1)*h)
    strip = im.crop((0,y0,im.width,y1))
    h=y1-y0
    cols = runs((np.asarray(strip)[:,:map_limit,3] >= 128).sum(0) > 2, 0)
    assert len(cols) == 9, (source, row, cols)
    parts=[]; boxes=[]
    for x0,x1 in cols[:9]:
        part, bb = tight(strip.crop((x0,0,x1,h)),True)
        parts.append(part); boxes.append([x0+bb[0],y0+bb[1],x0+bb[2],y0+bb[3]])
    if portrait_box is None:
        x0,x1=cols[-1]; portrait_box=[x0,y0,x1,y1]
    if alternate:
        alt_im=Image.open(ROOT/alternate['source']).convert('RGBA')
        alt_strip=alt_im.crop((0,y0,alt_im.width,y1))
        alt_cols=runs((np.asarray(alt_strip)[:,:map_limit,3]>=128).sum(0)>2,0)
        assert len(alt_cols)==9
        for dst,src in alternate['frames'].items():
            ax0,ax1=alt_cols[src]
            parts[int(dst)],_=tight(alt_strip.crop((ax0,0,ax1,h)),True)
    if selection: parts=[parts[i] for i in selection]
    for i in flips or []: parts[i]=parts[i].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    battle, bb=tight(im.crop(tuple(portrait_box)))
    # Each map pose uses the corresponding original Red frame's exact bounds.
    native=[]
    for i,part in enumerate(parts):
        rb = RED.crop((i*16,0,(i+1)*16,32)).getchannel('A').getbbox()
        assert rb
        part=part.resize((rb[2]-rb[0],rb[3]-rb[1]),Image.Resampling.NEAREST)
        frame=Image.new('RGBA',(16,32)); frame.alpha_composite(part,(rb[0],rb[1]));native.append(frame)
    scale=min(60/battle.width,60/battle.height)
    battle=battle.resize((round(battle.width*scale),round(battle.height*scale)),Image.Resampling.NEAREST)
    frame=Image.new('RGBA',(64,64));frame.alpha_composite(battle,((64-battle.width)//2,63-battle.height))
    # Quantize jointly, then round to actual GBA channel precision.
    pixels=[]
    for p in native+[frame]:
        pixels.extend(tuple(c[:3]) for c in p.get_flattened_data() if c[3]>=128)
    swatch=Image.new('RGB',(len(pixels),1));swatch.putdata(pixels)
    q=swatch.quantize(colors=15,method=Image.Quantize.MEDIANCUT)
    raw=q.getpalette()[:45]
    colors=[tuple((v>>3)*255//31 for v in raw[i:i+3]) for i in range(0,45,3)]
    palette=[(0,0,0)]+colors
    directory=BASE/actor;directory.mkdir(exist_ok=True)
    (directory/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
    map_colors = [(0,0,0),(16,24,32),(56,56,72),(120,72,56),(184,120,88),(248,200,152),(248,248,232),(176,184,192),(80,48,104),(168,128,184),(248,224,112),(216,160,48),(200,48,64),(72,128,72),(48,184,200),(56,88,136)]
    map_colors = [tuple((v>>3)*255//31 for v in c) for c in map_colors]
    (directory/'overworld.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in map_colors)+'\n')
    ow=Image.new('P',(144,32));ow.putpalette([v for c in map_colors for v in c]+[0]*720);ow.info['transparency']=0
    for i,p in enumerate(native):ow.paste(indexed(p,map_colors),(i*16,0))
    ow.save(directory/'overworld.png',bits=4,transparency=0)
    indexed(frame,palette).save(directory/'battle.png',bits=4,transparency=0)
    preview=Image.new('RGB',(704,160),(224,224,224));d=ImageDraw.Draw(preview);d.text((4,2),actor,fill='black')
    for i in range(9):
        p=ow.crop((i*16,0,(i+1)*16,32)).convert('RGBA').resize((48,96),Image.Resampling.NEAREST)
        preview.paste(p,(i*52,28),p)
    p=indexed(frame,palette).convert('RGBA').resize((128,128),Image.Resampling.NEAREST)
    preview.paste(p,(552,24),p);preview.save(directory/'preview.png')
    report={'actor':actor,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'map_crop_boxes':boxes,'battle_crop_box':portrait_box,'native_frames':9,'frame_size':[16,32],'battle_size':[64,64],'palette':'RGB555, 15 opaque colors + transparent index 0','red_bounds':[RED.crop((16*i,0,16*(i+1),32)).getchannel('A').getbbox() for i in range(9)],'status':'converted_not_yet_engine_tested'}
    (directory/'conversion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

def main():
    config=json.loads((PACK/'sources.json').read_text());report=[]
    for batch in config:
        source=ROOT/batch['source']
        for row,actor in enumerate(batch['actors']):
            report.append(character(actor,source,row,batch.get('portrait_boxes',[None]*4)[row],batch.get('row_spans',[None]*4)[row],batch.get('selections',{}).get(actor),batch.get('flips',{}).get(actor),batch.get('alternates',{}).get(actor),batch.get('map_limit',1200)))
    (ROOT/'QA_RECETTE_FINALE/SPRITES_SCENARIO_2026/CONVERSION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Converted',len(report),'characters')
if __name__=='__main__': main()

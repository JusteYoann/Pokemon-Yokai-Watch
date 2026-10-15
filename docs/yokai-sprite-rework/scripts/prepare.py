#!/usr/bin/env python3
"""Technical conversion of artist-redrawn atlases. Never writes outside this dossier.
Requires ImageMagick and Pillow. No drawing, stretching or individual size fitting.
Transparent atlas margins are removed only during NEW artwork extraction;
one sampling factor is shared by every new drawing in a batch.
Original 64x64 canvases are never trimmed or resized.
Palettes are the existing normal/shiny pair, with their indices unchanged.
"""
import pathlib, json, zipfile, subprocess, tempfile, math, struct, zlib, hashlib, io
from PIL import Image

D = pathlib.Path(__file__).resolve().parents[1]
BATCHES = json.loads((D / 'batches.json').read_text())
KEEP_FRONT = {17,22,25,27,28,41,47,48,61,62,90,93,98,100,111,124}
KEEP_BACK = {70,133,139,147}

def sha(b): return hashlib.sha256(b).hexdigest()
def mag(*a):
    subprocess.run(['magick','-limit','thread','1',*map(str,a)],check=True,capture_output=True)
def chunk(tag, data):
    return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
def indexed(path, indices, palette):
    rows=b''.join(b'\0'+bytes((indices[y*64+x]<<4)|indices[y*64+x+1] for x in range(0,64,2)) for y in range(64))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,64,4,3,0,0,0))+chunk(b'PLTE',bytes(c for rgb in palette for c in rgb))+chunk(b'tRNS',bytes([0]+[255]*15))+chunk(b'IDAT',zlib.compress(rows))+chunk(b'IEND',b''))
def palette(data): return [tuple(map(int,s.split())) for s in data.decode().splitlines()[3:19]]
def seams(ink, size):
    # Find gutters near the requested equal grid, without trimming a character.
    edges=[0]
    for j in range(1,4):
        target=round(j*size/4);radius=round(size/4*.23)
        edges.append(min(range(target-radius,target+radius+1),key=lambda p:(sum(ink[max(0,p-1):p+2]),abs(p-target))))
    return edges+[size]

report={'source':'AI image-editing proposals, reviewed separately; not approved game assets','species':[],'atlases':[]}
with zipfile.ZipFile(D/'sources/originals.zip') as originals, tempfile.TemporaryDirectory(prefix='yokai-rework-convert-') as tmp:
    T=pathlib.Path(tmp)
    for batch, ns in enumerate(BATCHES,1):
        atlas=D/'sources'/f'proposal-{batch}.png'
        with Image.open(atlas) as image:
            im=image.convert('RGBA');w,h=im.size;pix=list(im.get_flattened_data())
        ink_y=[sum(pix[y*w+x][3]>=192 for x in range(w)) for y in range(h)]
        ink_x=[sum(pix[y*w+x][3]>=192 for y in range(h)) for x in range(w)]
        xs=seams(ink_x,w);ys=seams(ink_y,h)
        boxes={}
        for offset,n in enumerate(ns):
            for side,col in [('front',2*(offset%2)),('back',2*(offset%2)+1)]:
                row=offset//2;x0,x1=xs[col:col+2];y0,y1=ys[row:row+2]
                coords=[(x,y) for y in range(y0,y1) for x in range(x0,x1) if pix[y*w+x][3]>=192]
                assert coords,(n,side,'missing artwork')
                boxes[n,side]=(min(x for x,y in coords),min(y for x,y in coords),max(x for x,y in coords)+1,max(y for x,y in coords)+1)
        factor=58/max(max(x1-x0,y1-y0) for x0,y0,x1,y1 in boxes.values())
        report['atlases'].append({'batch':batch,'sha256':sha(atlas.read_bytes()),'dimensions':[w,h],'x_gutters':xs,'y_gutters':ys,'uniform_sampling_factor':factor,'individual_fitting':False,'transparent_atlas_margins_removed':True,'original_canvases_cropped':False})
        for offset,n in enumerate(ns):
            folder=D/'proposals'/f'{n:03}';folder.mkdir(parents=True,exist_ok=True)
            normal=originals.read(f'{n:03}/normal.pal');pal=palette(normal)
            for kind in ['normal','shiny']:(folder/f'{kind}.pal').write_bytes(originals.read(f'{n:03}/{kind}.pal'))
            rec={'index':n,'batch':batch,'views':{}}
            for side,col in [('front',2*(offset%2)),('back',2*(offset%2)+1)]:
                row=offset//2;dest=folder/f'{side}.png';before=originals.read(f'{n:03}/{side}.png')
                keep=n in (KEEP_FRONT if side=='front' else KEEP_BACK)
                if keep:
                    dest.write_bytes(before)
                else:
                    x0,y0,x1,y1=boxes[n,side]
                    mag(atlas,'-crop',f'{x1-x0}x{y1-y0}+{x0}+{y0}','+repage','-filter','point','-resize',f'{100*factor:.8f}%','-gravity','center','-background','none','-extent','64x64',T/'sample.png')
                    with Image.open(T/'sample.png') as sampled:
                        rgba=list(sampled.convert('RGBA').get_flattened_data())
                    cache={}
                    def match(rgb):
                        if rgb not in cache:cache[rgb]=min(range(1,16),key=lambda k:sum((rgb[c]-pal[k][c])**2 for c in range(3)))
                        return cache[rgb]
                    indices=[0 if p[3]<192 else match(p[:3]) for p in rgba]
                    indexed(dest,indices,pal)
                with Image.open(io.BytesIO(before)) as old,Image.open(dest) as new:
                    old.load();new.load();assert old.mode==new.mode=='P' and new.size==(64,64)
                    a=bytes(old.get_flattened_data());b=bytes(new.get_flattened_data());assert max(b)<16
                    assert new.info.get('transparency')==0
                    changed=sum(i!=j for i,j in zip(a,b));assert (changed==0)==keep,(n,side,changed)
                    if not keep:assert all(not b[y*64+x] for y in range(64) for x in range(64) if min(x,y,63-x,63-y)<2),(n,side,'edge clipping')
                    rec['views'][side]={'preserved':keep,'changed_index_pixels':changed,'sha256':sha(dest.read_bytes()),'opaque_pixels':sum(bool(i) for i in b),'bounds':new.convert('RGBA').getbbox()}
            report['species'].append(rec)
(D/'conversion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Converted',len(report['species']),'species; preserved requested views byte for byte. Game untouched.')

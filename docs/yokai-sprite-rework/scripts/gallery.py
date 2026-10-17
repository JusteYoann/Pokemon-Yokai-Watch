#!/usr/bin/env python3
"""Render comparisons only. Full 64x64 canvases at x3, fixed checkerboard, no fitting."""
import pathlib,json,zipfile,io,math,hashlib,re,struct
from PIL import Image,ImageDraw,ImageFont
D=pathlib.Path(__file__).resolve().parents[1]
B=json.loads((D/'batches.json').read_text())
M={e['index']:e for e in json.loads((D/'source-map.json').read_text())}
N={int(p[0]):p[1:] for l in (D/'observations.tsv').read_text().splitlines() if (p:=l.split('\t'))}
REV={int(p[0]):p[1:] for l in (D/'review.tsv').read_text().splitlines() if (p:=l.split('\t'))}
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(n):return ImageFont.truetype(F,n)
def palette(data):
    rows=[tuple(map(int,s.split())) for s in data.decode().splitlines()[3:19]]
    return [tuple(((v>>3)<<3)|((v>>3)>>2) for v in rgb) for rgb in rows]
def rgba(data,pal):
    with Image.open(io.BytesIO(data)) as im:
        assert im.mode=='P' and im.size==(64,64)
        idx=list(im.get_flattened_data())
    out=Image.new('RGBA',(64,64));out.putdata([(*pal[k],255 if k else 0) for k in idx]);return out
def place(canvas,im,x,y):
    draw=ImageDraw.Draw(canvas)
    for yy in range(0,192,24):
        for xx in range(0,192,24):draw.rectangle((x+xx,y+yy,x+xx+23,y+yy+23),fill=(224,224,224) if (xx//24+yy//24)%2==0 else (176,176,176))
    scaled=im.resize((192,192),Image.Resampling.NEAREST);canvas.paste(scaled,(x,y),scaled)
    # Verify every opaque pixel survived composition exactly.
    a=list(scaled.get_flattened_data());b=list(canvas.crop((x,y,x+192,y+192)).get_flattened_data())
    assert all(p[:3]==q for p,q in zip(a,b) if p[3])
outputs=[]
with zipfile.ZipFile(D/'sources/originals.zip') as original:
    for category in ['normal','shiny']:
        (D/'comparisons'/category).mkdir(parents=True,exist_ok=True)
        for batch,ns in enumerate(B,1):
            group=[102,103,104,105,87,88,99,119] if batch==5 else ns
            cw,ch=408,510;cols=4;header=54
            canvas=Image.new('RGB',(cols*cw,header+math.ceil(len(group)/cols)*ch),(240,240,240));draw=ImageDraw.Draw(canvas)
            draw.text((12,12),f'Propositions {category} — lot {batch} — avant / après — x3 — non intégrées',font=font(21),fill=(20,20,20))
            for j,n in enumerate(group):
                x=(j%cols)*cw;y=header+(j//cols)*ch;label=f'{n:03} {M[n]["name"]} — {N[n][0]}';f=font(16)
                while draw.textbbox((0,0),label,font=f)[2]>cw-12:f=font(f.size-1)
                draw.text((x+8,y+2),label,font=f,fill=(20,20,20))
                badge='ESSAI INCOMPLET — voir réserves' if REV[n][1]!='—' else 'PROPOSITION À VALIDER'
                draw.text((x+8,y+23),badge,font=font(11),fill=(125,55,20) if REV[n][1]!='—' else (35,75,65))
                pal=palette(original.read(f'{n:03}/{category}.pal'))
                for side,dy,name in [('front',44,'Face'),('back',268,'Dos')]:
                    for after,dx,title in [(False,6,'Avant'),(True,210,'Après')]:
                        data=(D/'proposals'/f'{n:03}'/f'{side}.png').read_bytes() if after else original.read(f'{n:03}/{side}.png')
                        draw.text((x+dx,y+dy),f'{name} — {title}',font=font(13),fill=(35,35,35))
                        place(canvas,rgba(data,pal),x+dx,y+dy+21)
            path=D/'comparisons'/category/f'lot-{batch:02}.png';canvas.save(path,compress_level=9)
            with Image.open(path) as check:
                check.load();assert check.mode=='RGB' and check.tobytes()==canvas.tobytes()
                assert len(check.getcolors(check.width*check.height) or [])>20
            raw=path.read_bytes();assert raw[24:26]==bytes([8,2]) and raw[28]==0
            outputs.append({'file':str(path.relative_to(D)),'species':group,'size':canvas.size,'sha256':hashlib.sha256(raw).hexdigest()})
for c in ['normal','shiny']:
    assert sorted(n for o in outputs if '/'+c+'/' in o['file'] for n in o['species'])==sorted(n for g in B for n in g)
(D/'preview-validation.json').write_text(json.dumps({'sheets':len(outputs),'compared_species':sum(map(len,B)),'views_before_and_after_per_palette':sum(map(len,B))*4,'scale':3,'opaque_rgb8':True,'source_indices_unchanged_in_preview':True,'same_full_64x64_canvas':True,'outputs':outputs},ensure_ascii=False,indent=2)+'\n')
print('PASS:',len(outputs),'RGB8 comparison sheets, 51 species normal and shiny, no clipping or individual fitting in previews.')

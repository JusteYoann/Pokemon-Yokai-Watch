#!/usr/bin/env python3
"""Lossless indexing of the user's corrected native PNGs. No crop or resize.
Original RGBA files are archived unchanged. RGB555 conversion happens in gbagfx.
"""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'graphics/juste_yoann';S=D/'source/corrections-utilisateur-20261024'
frames={name:Image.open(S/(name+'.png')).convert('RGBA') for name in ['battle','overworld']}
for name,im in frames.items():
 assert im.size==((64,64) if name=='battle' else (32,32))
 assert set(im.getchannel('A').get_flattened_data())<={0,255}
colors=sorted({p[:3] for im in frames.values() for p in im.get_flattened_data() if p[3]})
assert len(colors)<=15, 'Do not quantize the user corrections without review'
palette=[(0,0,0)]+colors+[(0,0,0)]*(15-len(colors));indices={c:i+1 for i,c in enumerate(colors)};results=[]
for name,im in frames.items():
 out=Image.new('P',im.size);out.putpalette([v for c in palette for v in c]+[0]*720)
 out.putdata([indices[p[:3]] if p[3] else 0 for p in im.get_flattened_data()]);out.save(D/(name+'.png'),bits=4,transparency=0)
 decoded=Image.open(D/(name+'.png')).convert('RGBA')
 assert decoded.getchannel('A').tobytes()==im.getchannel('A').tobytes()
 assert all(a==b for a,b in zip(im.get_flattened_data(),decoded.get_flattened_data()) if a[3])
 results.append(dict(name=name,frame=list(im.size),opaque_bbox=im.getbbox(),source=str((S/(name+'.png')).relative_to(R)),source_sha256=hashlib.sha256((S/(name+'.png')).read_bytes()).hexdigest(),opaque_pixels_exact=True,alpha_exact=True,resampled=False))
(D/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')
(D/'conversion.json').write_text(json.dumps(dict(source='User-corrected native PNGs from Nouveau dossier (3).rar; supersede approved reproduction.',frames=results,opaque_colors=len(colors),palette_entries=16,transparent_index=0,conversion='Lossless PNG indexing. Only the native RGB555 hardware palette representation limits RGB precision.'),ensure_ascii=False,indent=2)+'\n')
print('User-corrected sprites indexed losslessly:',len(colors),'opaque colors; original dimensions, positions and alpha retained')

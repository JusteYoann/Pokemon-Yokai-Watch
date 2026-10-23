#!/usr/bin/env python3
"""Original indexed artwork centered once; native GBA affine geometry per mockup.
No reference pixels are imported and no axis is flipped.
"""
import json,math,re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/CADRAGE_COMBATS_151';O=R/'QA_RECETTE_FINALE/COMBATS_ETENDUS';O.mkdir(exist_ok=True)
def extent(size,inv):
 l=-(size//2);return math.ceil(l*256/inv),math.ceil((l+size)*256/inv)
def fit(size,target):
 ideal=256*size/target
 inv=min(range(16,2049),key=lambda v:(abs(extent(size,v)[1]-extent(size,v)[0]-target),extent(size,v)[1]-extent(size,v)[0]>target,abs(v-ideal)))
 l,r=extent(size,inv);return inv,l,r-l
config=json.loads((R/'data/yokai/battle_geometry_overrides.json').read_text());overrides=config['back_crops'];uniform_scale_species=set(config.get('uniform_scale_species',[]))
baseline=json.loads((Q/'sources/ETAT_AVANT.json').read_text())['species'];refs=json.loads((Q/'sources/MESURES_REFERENCES_BRUTES.json').read_text())['results']
p=R/'data/yokai/sprite_presentation.json';data=json.loads(p.read_text());preserved=json.loads((Q/'sources/apres-sprite_presentation.json').read_text());profiles={v['id']:v for v in preserved['profiles']};pictures=[];pointers=[];table=['// Generated from latest indexed artwork and user mockup geometry.','static const struct YokaiBattleGeometry sYokaiBattleGeometry[152][2] = {'];report=[]
for mon,ref in zip(baseline,refs):
 n=mon['number'];fields=[]
 for side in ['front','back']:
  sw,sh=mon[side]['source_visible_size'];b=ref[side];tw,th=b[2]-b[0],b[3]-b[1]
  crop_bottom=None
  if side=='back' and f'{n:03}' in overrides:
   crop_bottom=mon[side]['source_visible_bbox'][1]+overrides[f'{n:03}']['keep_source_rows_from_opaque_top']
   im=Image.open(R/mon[side]['original_png']);pts=[(x,y) for y in range(crop_bottom) for x in range(64) if im.getpixel((x,y))];sw=max(x for x,y in pts)-min(x for x,y in pts)+1;sh=max(y for x,y in pts)-min(y for x,y in pts)+1
  targeth=(max(1,th-1) if crop_bottom is not None else th) if side=='front' or crop_bottom is not None else max(th,round(sh*tw/sw))
  ix,left,w=fit(sw,tw);iy,top,h=fit(sh,targeth);cx=b[0]-left;cy=b[1]-top-(1 if side=='back' else 0)
  dx=cx-(176 if side=='front' else 72);dy=cy-(40 if side=='front' else 80)
  if n in uniform_scale_species:
   # Preserve vertical size and anchor; remove horizontal stretching only.
   ix=iy;left,right=extent(sw,ix);w=right-left
  assert -64<=left and left+w<=64 and -64<=top and top+h<=64,(n,side,'outside double-size OAM')
  assert math.ceil(w/8)*math.ceil(h/8)*32<=4096,(n,side,'animation background capacity')
  fields.append('{ %d, %d, %d, %d, %d, %d, %d, %d }'%(ix,iy,dx,dy,left,top,w,h))
  profile=dict(profiles[f'{n:03}/{side}']);profile['id']=f'{n:03}/battle-{side}';profile['target']=f'graphics/yokai/{n:03}/{side}-battle.4bpp';profiles[profile['id']]=profile;profile.update(scale_q8=256,center_x=32,top=32-sh//2,reason='Original indexed art centered without resizing. Battle-only hardware affine geometry in yokai_battle_geometry.h; normal and color-only shiny share pixels.')
  profile.pop('bottom',None)
  if crop_bottom is not None:profile['crop_source_bottom']=crop_bottom
  pictures.append(f'const u32 gYokaiBattle{n:03}{side}[] = INCBIN_U32("graphics/yokai/{n:03}/{side}-battle.4bpp.lz");')
  report.append(dict(number=n,name=mon['name'],side=side,reference_bbox=b,source_size=[sw,sh],inverse_x_q8=ix,inverse_y_q8=iy,offset_x=dx,offset_y=dy,left=left,top=top,width=w,height=h,desired_width=tw,desired_full_height=targeth,source_unchanged=True,crop_source_bottom=crop_bottom,nearest_hardware_sampling=True))
 table.append(f'    [{n}] = {{ '+', '.join(fields)+' },')
 pointers.append(f'    [{n}] = {{ gYokaiBattle{n:03}front, gYokaiBattle{n:03}back }},')
 for side in ['front','back']:
  pth=R/f'src/data/pokemon_graphics/{side}_pic_coordinates.h';s=pth.read_text();s=re.sub(r'(\['+mon['species']+r'\]\s*=\s*\{[^}]*?\.y_offset\s*=\s*)\d+',lambda m:m[1]+'0',s);pth.write_text(s)
pictures+=['static const u32 *const sYokaiBattlePictures[152][2] = {']+pointers+['};'];(R/'src/data/yokai_battle_pictures.h').write_text('\n'.join(pictures)+'\n');table.append('};');(R/'src/data/yokai_battle_geometry.h').write_text('\n'.join(table)+'\n');data['scope']='Original indexed artwork; generic displays unchanged. Separate centered/cropped battle textures use per-species GBA affine OAM presentation and matching animation background transforms.';data['profiles']=list(profiles.values());p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(O/'GEOMETRIE_302.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('GEOMETRY',len(report),'max background bytes',max(math.ceil(v['width']/8)*math.ceil(v['height']/8)*32 for v in report))

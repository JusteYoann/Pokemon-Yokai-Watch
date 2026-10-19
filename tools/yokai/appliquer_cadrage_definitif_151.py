#!/usr/bin/env python3
"""Per-reference indexed presentation; never imports reference artwork into game.
Aspect ratio and palette indices retained; back lower-body crop is intentional.
"""
import csv,json,math,re
from pathlib import Path
from PIL import Image
from presentation_4bpp import transform,decode
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/CADRAGE_COMBATS_151'
def bounds(path):
 im=Image.open(path);m=Image.new('L',im.size);m.putdata([255 if v else 0 for v in im.get_flattened_data()]);return m.getbbox()
def main():
 baseline=json.loads((Q/'sources/ETAT_AVANT.json').read_text());measures=[]
 for mon in baseline['species']:
  n=mon['number'];im=Image.open(Q/f'references/{n:03}.png').convert('RGB');row={'number':n}
  for side,roi in [('front',(118,2,240,74)),('back',(0,48,124,113))]:
   pts=[]
   for y in range(roi[1],roi[3]):
    for x in range(roi[0],roi[2]):
     c=im.getpixel((x,y))
     if max(c)<115 or (max(c)-min(c)>40 and min(c)<120):pts.append((x,y))
   row[side]=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts)+1,max(y for x,y in pts)+1]
  measures.append(row)
 path=R/'data/yokai/sprite_presentation.json';data=json.loads(path.read_text());profiles={p['id']:p for p in data['profiles']};decisions=[];header=R/'src/data/graphics/pokemon.h';s=header.read_text()
 coords={side:(R/f'src/data/pokemon_graphics/{side}_pic_coordinates.h').read_text() for side in ['front','back']}
 for mon,measure in zip(baseline['species'],measures):
  n=mon['number']
  for side in ['front','back']:
   box=mon[side]['source_visible_bbox'];sw,sh=box[2]-box[0],box[3]-box[1];ref=measure[side];tw,th=ref[2]-ref[0],ref[3]-ref[1]
   # Back lower body hidden by the dialogue window: width controls zoom, top controls framing.
   ratio=math.sqrt(tw/sw*th/sh) if side=='front' else tw/sw
   cap=min(64/sw,64/sh) if side=='front' else 64/sw
   scale=min(ratio,cap);q=round(scale*256)
   while (sw*q+128)//256>64 or (side=='front' and (sh*q+128)//256>64):q-=1
   dw=max(1,(sw*q+128)//256);dh=max(1,(sh*q+128)//256)
   # Keep the complete horizontal silhouette inside the native 64px tile.
   origin=144 if side=='front' else 40;cx=round((ref[0]+ref[2])/2-origin);cx=max(dw//2,min(64-(dw-dw//2),cx))
   if side=='front':
    top=max(0,min(64-dh,ref[3]-8-dh));yoff=max(0,ref[3]-8-(top+dh))
   else:top=max(0,min(60,ref[1]-53));yoff=4
   key=f'{n:03}/{side}';p=dict(id=key,source=f'graphics/yokai/{n:03}/{side}.4bpp',target=f'graphics/yokai/{n:03}/{side}-display.4bpp',frame_width=64,frame_height=64,scale_q8=q,center_x=cx,top=top,reason=f'BATTLE_SPRITE {n:03}: reference bounds {ref}; latest artwork aspect retained, nearest indexed sampling, no axis flip; '+('complete front silhouette' if side=='front' else 'reference head height, lower body may be cropped'))
   profiles[key]=p
   s=re.sub(r'graphics/yokai/'+f'{n:03}/{side}'+r'(?:-display)?\.4bpp\.lz',p['target']+'.lz',s)
   pat=r'(\['+mon['species']+r'\]\s*=\s*\{[^}]*?\.y_offset\s*=\s*)\d+'
   coords[side],count=re.subn(pat,lambda m:m[1]+str(yoff),coords[side]);assert count==1
   raw=transform((R/p['source']).read_bytes(),p);pixels=decode(raw,64,64);assert any(v for line in pixels for v in line)
   limits=[]
   if ratio>cap+0.01:limits.append('reference exceeds native64px/aspect constraint')
   actual=[origin+cx-dw//2,(8+yoff if side=='front' else 53)+top,origin+cx-dw//2+dw,(8+yoff if side=='front' else 53)+min(64,top+dh)]
   if side=='back':actual[3]=min(113,actual[3])
   if side=='back' and top+dh>64:limits.append('intentional lower body canvas crop')
   decisions.append(dict(number=n,name=mon['name'],side=side,source_bbox=box,reference_bbox=ref,scale_q8=q,center_x=cx,top=top,y_offset=yoff,predicted_bbox=actual,limitations=limits,source_artwork_unchanged=True,axis_flip=False))
   # Independent shiny silhouettes receive equivalent placement, with their own width safety.
   shiny=profiles.get(f'{n:03}/shiny-{side}')
   if (R/f'graphics/yokai_shiny/{n:03}/{side}.png').exists():
    if shiny is None:
     shiny=dict(p,id=f'{n:03}/shiny-{side}',source=f'graphics/yokai_shiny/{n:03}/{side}.4bpp',target=f'graphics/yokai_shiny/{n:03}/{side}-display.4bpp');profiles[shiny['id']]=shiny
    b=bounds(R/f'graphics/yokai_shiny/{n:03}/{side}.png');w,h=b[2]-b[0],b[3]-b[1];sq=q
    while (w*sq+128)//256>64 or (side=='front' and (h*sq+128)//256>64):sq-=1
    width=(w*sq+128)//256;height=(h*sq+128)//256
    shiny.update(scale_q8=sq,center_x=max(width//2,min(64-(width-width//2),cx)),top=(max(0,min(64-height,ref[3]-8-yoff-height)) if side=='front' else top),reason='Same reference placement as normal; existing independent shiny artwork untouched; native width bounded')
    shiny.pop('bottom',None)
 decompress=R/'src/decompress.c';text=decompress.read_text()
 for n in [19,99,100,101,126]:
  for side in ['front','back']:text=re.sub(r'graphics/yokai_shiny/'+f'{n:03}/{side}'+r'(?:-display)?\.4bpp\.lz',f'graphics/yokai_shiny/{n:03}/{side}-display.4bpp.lz',text)
 decompress.write_text(text)
 data['profiles']=list(profiles.values());path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');header.write_text(s)
 for side,s in coords.items():(R/f'src/data/pokemon_graphics/{side}_pic_coordinates.h').write_text(s)
 (Q/'sources/MESURES_REFERENCES_BRUTES.json').write_text(json.dumps(dict(method='Colored/dark outline ROI bounds, excludes white mockup eraser halos and health HUD. Reviewed as visual guides; not artwork import.',results=measures),indent=2)+'\n')
 (Q/'AJUSTEMENTS_302.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')
 with (Q/'AJUSTEMENTS_302.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['numero','nom','cote','reference_xyxy','source_xyxy','scale_q8','centre_x','haut','decalage_y','bbox_cible_realisable','limites'])
  for d in decisions:w.writerow([d[k] for k in ['number','name','side','reference_bbox','source_bbox','scale_q8','center_x','top','y_offset','predicted_bbox','limitations']])
 print('INDIVIDUAL PRESENTATION PROFILES',len(decisions),'bounded fronts',sum(bool(d['limitations']) for d in decisions if d['side']=='front'))
if __name__=='__main__':main()

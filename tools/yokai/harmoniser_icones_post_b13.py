#!/usr/bin/env python3
"""Per-species menu bounds from reviewed natural-size groups, not a battle-wide zoom."""
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
SMALL={9,11,22,24,29,31,36,41,45,46,49,51,52,53,55,61,62,63,66,76,82,85,87,90,91,93,94,98,106,108,110,113,115,117,118,119,121,122,123,124,125,126,127,128,129,131,134,136,139,141,143,146,151}
LARGE={14,15,16,19,23,25,27,28,33,35,37,40,48,57,60,65,70,71,74,75,77,78,79,80,81,83,86,88,89,92,95,96,97,99,101,104,105,107,109,111,112,114,116,120,130,132,133,135,138,140,142,144,145,147,148,150}
def main():
 p=ROOT/'data/yokai/sprite_presentation.json';d=json.loads(p.read_text());d['profiles']=[r for r in d['profiles'] if not r['id'].endswith('/icon')];proof=[]
 for n in range(1,152):
  im=Image.open(ROOT/f'graphics/yokai/{n:03d}/icon.png');points=[(x,y%32) for y in range(64) for x in range(32) if im.getpixel((x,y))];left=min(x for x,y in points);right=max(x for x,y in points)+1;top=min(y for x,y in points);bottom=max(y for x,y in points)+1;w=right-left;h=bottom-top;cap=20 if n in SMALL else 24 if n in LARGE or n==1 else 22
  if n==9:cap=18
  if n==82:cap=18
  q=min(256,cap*256//h,28*256//w);dw=max(1,(w*q+128)//256);dh=max(1,(h*q+128)//256)
  shift=round((w/2-sum(x-left+.5 for x,y in points)/len(points))*q/256);center=max(dw//2,min(32-(dw-dw//2),16+shift))
  reason=f'Icône {n:03d}: gabarit '+('petit' if n in SMALL else 'grand' if n in LARGE or n==1 else 'moyen')+f', boîte initiale {w}×{h}, plafond {cap}px, centre de masse et deux images préservés'
  if q<256 or top!=(32-dh)//2:
   d['profiles'].append(dict(id=f'{n:03d}/icon',source=f'graphics/yokai/{n:03d}/icon.4bpp',target=f'graphics/yokai/{n:03d}/icon-display.4bpp',frame_width=32,frame_height=32,scale_q8=q,top=(32-dh)//2,center_x=center,reason=reason))
  proof.append(dict(number=n,source_bbox=[left,top,right,bottom],target_pixels=[dw,dh],scale_q8=q,natural_height_cap=cap,reason=reason))
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/'src/data/graphics/pokemon.h';s=p.read_text()
 for r in d['profiles']:
  if r['id'].endswith('/icon'):s=s.replace('"'+r['source']+'"','"'+r['target']+'"')
 p.write_text(s)
 out=ROOT/'QA_RECETTE_FINALE/POST_B13/sprites/ICÔNES_HARMONISATION.json';out.write_text(json.dumps({'scope':'All151 source icons inspected for native menu cell bounds; individual natural-size caps18–24px, no upscaling, original PNG/palette unchanged; actual menu/PC QA still required','species':proof},ensure_ascii=False,indent=2)+'\n');print('Profiles total',len(d['profiles']))
if __name__=='__main__':main()

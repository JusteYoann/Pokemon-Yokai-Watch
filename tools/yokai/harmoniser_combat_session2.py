#!/usr/bin/env python3
"""Individual presentation choices after native151 review and supplied FRLG examples.

No source artwork or palette is painted. Nearest-neighbour indexed derivatives
and native coordinates preserve the original art and the gameplay tables.
"""
import json,re
from pathlib import Path
from PIL import Image
from presentation_4bpp import transform,decode
from harmoniser_icones_post_b13 import SMALL
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES'
# Visible-size decisions, reviewed with the actual drawings, not dex height data.
# Baku is exempt: its naturally horizontal body is bounded by the 64px width.
CAPS={n:42 for n in SMALL if n not in [49,141,146]}
CAPS.update({5:46,9:42,13:46,24:42,26:46,29:42,36:42,41:42,45:42,
             51:44,55:44,61:44,63:42,66:44,68:46,76:44,82:40,85:44,
             87:44,90:42,91:40,94:44,98:42,100:46,106:40,108:44,
             110:46,112:44,113:46,115:44,118:40,119:44,121:44,122:42,
             123:44,124:42,125:44,126:44,127:42,128:48,129:40,
             131:44,134:44,136:44,137:44,139:44,143:44,146:46,151:44})
# Morphology exceptions: winged/swimming/floating silhouettes retain their air
# rather than forcing a foot-placement rule onto clouds, fish and ghosts.
AIR={8,11,12,14,15,26,27,41,42,45,46,56,57,58,71,72,73,74,75,
     112,115,116,126,129,135,143,144,150}
# Back canvas placement in native pixels. Waist/basin framing for upright forms;
# quadrupeds, fish, serpents and special bodies keep their anatomical silhouette.
BACK={
 1:(256,20),2:(256,19),3:(256,21),4:(256,19),
 5:(307,14),6:(282,20),7:(282,19),9:(256,20),10:(256,18),
 17:(282,19),18:(256,20),19:(256,21),20:(256,18),21:(256,19),
 24:(256,22),25:(256,18),26:(256,20),27:(256,18),29:(256,22),30:(256,18),
 38:(256,20),39:(256,18),40:(256,20),43:(256,19),44:(256,19),
 47:(333,16),48:(256,19),51:(256,21),
 61:(256,20),62:(256,19),63:(256,22),64:(256,19),65:(256,18),
 68:(256,21),69:(256,19),70:(282,17),74:(256,22),75:(256,22),
 78:(256,19),79:(256,19),80:(256,19),81:(256,19),
 87:(282,23),88:(256,21),89:(256,18),90:(256,22),
 93:(256,19),94:(256,20),95:(256,18),96:(256,20),97:(333,15),
 98:(256,21),99:(282,20),100:(384,13),101:(307,13),
 106:(256,21),107:(256,18),110:(294,15),111:(256,19),
 113:(256,19),114:(256,20),119:(282,20),120:(282,17),121:(256,18),
 125:(256,19),127:(256,21),128:(256,20),131:(256,22),132:(256,19),
 133:(256,18),136:(256,21),137:(358,13),138:(410,12),
 140:(256,18),141:(256,19),146:(294,15),147:(256,18),148:(282,19),
 149:(256,20),151:(256,20),
}
# Preserve whole silhouettes for bowls, mirrors, bacon, barrels, slugs and
# monoliths: these do not have a humanoid waist to crop indiscriminately.
for n in [24,25,43,44,93,94,95,98,125,141,147]:BACK.pop(n,None)


def main():
 path=ROOT/'data/yokai/sprite_presentation.json';d=json.loads(path.read_text())
 previous=d['profiles']
 baseline=json.loads((P/'sources/PROFILS_AVANT.json').read_text())['profiles']
 by={r['id']:r for r in previous if not r['id'].endswith(('/front','/back'))}
 by.update({r['id']:r for r in baseline if r['id'].endswith(('/front','/back'))});decisions=[]
 for n in range(1,152):
  ident=f'{n:03d}/front';src=ROOT/f'graphics/yokai/{n:03d}/front.png'
  im=Image.open(src);mask=Image.new('L',im.size);mask.putdata([255 if x else 0 for x in im.get_flattened_data()]);box=mask.getbbox();w=box[2]-box[0];h=box[3]-box[1]
  if n in CAPS:
   q=min(256,round(CAPS[n]*256/max(w,h)))
   by[ident]=dict(id=ident,source=f'graphics/yokai/{n:03d}/front.4bpp',target=f'graphics/yokai/{n:03d}/front-display.4bpp',frame_width=64,frame_height=64,scale_q8=q,bottom=58,
       reason=f'Session2 : gabarit apparent individualisé {CAPS[n]}px maximum ; petit sujet/pré-évolution, proportions et indices de couleur conservés.')
  if n==49:
   by[ident]['center_x']=30
   by[ident]['reason']='Session2 : Baku garde le léger agrandissement déjà validé ; centre du corps déplacé de2px sans couper la trompe, largeur60px limite64. Anatomie quadrupède horizontale préservée.'
  p=by.get(ident)
  if p:
   pixels=decode(transform((ROOT/p['source']).read_bytes(),p),64,64)
   bottom=max(y for y in range(64) for x in range(64) if pixels[y][x])+1
  else:bottom=box[3]
  yoff=4 if n in AIR else 64-bottom
  assert 0<=yoff<=32,(n,yoff)
  decisions.append(dict(number=n,front_maximum_pixels=CAPS.get(n),front_y_offset=yoff,
                        front_grounding='Air/eau/vol conservé' if n in AIR else 'Base sur la plateforme native y72',
                        back_profile=list(BACK[n]) if n in BACK else 'Présentation antérieure conservée',
                        source_artwork_unchanged=True))
  if n in BACK:
   q,top=BACK[n];ident=f'{n:03d}/back'
   by[ident]=dict(id=ident,source=f'graphics/yokai/{n:03d}/back.4bpp',target=f'graphics/yokai/{n:03d}/back-display.4bpp',frame_width=64,frame_height=64,scale_q8=q,top=top,
       reason='Session2 : cadrage haut du corps/ceinture adapté à la silhouette ; source intacte, bas masqué au premier plan comme les références Rouge Feu. Contrôle natif avant/après.')
 d['profiles']=list(by.values());path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 header=ROOT/'src/data/graphics/pokemon.h';s=header.read_text()
 for p in previous:
  if p['id'].endswith(('/front','/back')):s=s.replace('"'+p['target']+'"','"'+p['source']+'"')
 for p in d['profiles']:s=s.replace('"'+p['source']+'"','"'+p['target']+'"')
 header.write_text(s)
 coords=ROOT/'src/data/pokemon_graphics/front_pic_coordinates.h';s=coords.read_text()
 names={int(r['species_id']):r['species_constant'] for r in json.loads((ROOT/'data/yokai/noms_affiches.json').read_text())}
 for row in decisions:
  species=names[row['number']]
  pattern=r'(\['+species+r'\]\s*=\s*\{[^}]*?\.y_offset\s*=\s*)\d+'
  s,count=re.subn(pattern,lambda m:m[1]+str(row['front_y_offset']),s);assert count==1,species
 coords.write_text(s)
 (P/'DECISIONS_COMBAT.json').write_text(json.dumps(dict(scope='Per-species decisions after151 native captures and FRLG references. No artistic approval claimed before after-capture review.',species=decisions),ensure_ascii=False,indent=2)+'\n')
 print('Presentation profiles',len(d['profiles']),'front size decisions',len(CAPS),'back framing decisions',len(BACK))


if __name__=='__main__':main()

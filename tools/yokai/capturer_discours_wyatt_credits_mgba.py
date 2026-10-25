#!/usr/bin/env python3
"""Capture native du discours actuel avec Wyatt, via l'entrée Route 2.
Parties de test isolées ; aucun acteur ajouté ni recomposé dans l'image.
"""
import json,hashlib,subprocess,struct
from pathlib import Path
from PIL import Image,ImageOps
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/'docs/credits-souvenirs-20261025';D.mkdir(exist_ok=True)
rows=[];replacements=ROOT/'data/yokai/credits_replacements.json';repl=json.loads(replacements.read_text())
slide=json.loads((ROOT/'data/yokai/credits_storyboard.json').read_text())['slides'][3]
for gender,label in enumerate(('garcon','fille')):
 q=QA('TEMP.json');r=q.r
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));q.mon()
  q.f(0x892,False)
  q.warp('Route2',8,1);r.keys={4};r.run(90);r.keys=set()
  q.wait(lambda:r.read(r.symbols['gStringVar4'],8)==r.read(r.symbols['Argenta_DonSpeech'],8),30000)
  r.keys=set();r.run(600)
  actors=q.actors();local=q.local('LOCALID_ARGENTA_WYATT');assert local in actors
  a=actors[local];assert r.read(a+5,1)[0]==160
  sp=r.symbols['gSprites']+68*r.read(a+4,1)[0];x,y,dx,dy=struct.unpack('<hhhh',r.read(sp+32,8));x+=dx;y+=dy
  if r.read(sp+62,1)[0]&2:
   x+=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetX'],2))[0]
   y+=struct.unpack('<h',r.read(r.symbols['gSpriteCoordOffsetY'],2))[0]
  assert 0<=x<240 and 0<=y<160 and not(r.read(sp+62,1)[0]&4),(x,y)
  bank=r.read(sp+5,1)[0]>>4
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_YokaiWyatt'],32)
  path=D/f'{label}-03-discours-wyatt-native.png';r.frame.save(path)
  photo=ImageOps.fit(r.frame.convert('RGB'),(slide['width'],slide['height']),method=Image.Resampling.NEAREST).quantize(colors=223,dither=Image.Dither.NONE)
  im=Image.new('P',photo.size);im.putpalette([0,0,0]+photo.getpalette()[:669]+[0]*96);im.putdata([v+1 for v in photo.get_flattened_data()]);im.save(ROOT/f'graphics/yokai_credits/{label}-03.png')
  subprocess.run(['python3',str(ROOT/'tools/yokai/preparer_souvenirs_credits.py'),'--pack',label+'-03'],check=True)
  rows.append(dict(gender=label,source_rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),capture=str(path.relative_to(ROOT)),wyatt_visible=True,wyatt_palette_verified=True,wyatt_native_screen_xy=[x,y],current_arrival_scene_via_route2=True))
  print('PASS discours',label,flush=True)
 finally:r.close()
repl['3']={'title':'Discours de Don Morléone avec Wyatt','captures':{g:next(a['capture'] for a in rows if a['gender']==g) for g in ('garcon','fille')}}
replacements.write_text(json.dumps(repl,ensure_ascii=False,indent=2)+'\n')
(D/'DISCOURS_PROVENANCE.json').write_text(json.dumps(dict(scope=__doc__,captures=rows),ensure_ascii=False,indent=2)+'\n')

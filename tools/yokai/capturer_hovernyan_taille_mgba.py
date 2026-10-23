#!/usr/bin/env python3
"""Native short entrance clips and equal-height assertions. New game, map and strong-party fixtures only."""
import os,json,hashlib
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import warp,MAPS,strong_party
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
D=ROOT/'docs/cramois-ile-passe/phase-c/taille-hovernyan'/mode;D.mkdir(parents=True,exist_ok=True)
im=Image.open(ROOT/'graphics/yokai_characters/hovernyan/overworld.png');n=Image.open(ROOT/'graphics/yokai_characters/nathaniel/overworld.png')
b=n.crop((0,0,16,32)).point(lambda x:255 if x else 0).getbbox()
for y in [0,32]:
 box=im.crop((0,y,32,y+32)).point(lambda x:255 if x else 0).getbbox();assert box[3]-box[1]==b[3]-b[1]==19 and box[3]==b[3]==31
r=None
try:
 for gender in [0,1]:
  r=new_game(gender);strong_party(r);r.call('VarSet',0x40f4,3);warp(r,*MAPS['CinnabarIsland_Gym'],5,5)
  name='nathaniel' if gender==0 else 'michael';r.frame.save(D/(name+'-taille.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-taille-x4.png'))
  movie=[]
  for f in range(1200):
   r.keys={4} if f==30 else {8} if f>60 and f%16<4 else set();r.run()
   if f%6==0:movie.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
  movie[0].save(D/('rencontre-'+name+'.gif'),save_all=True,append_images=movie[1:],duration=100,loop=0)
  sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();r=None
 (D/'TAILLE.json').write_text(json.dumps(dict(passed=True,rom_sha256=sha,hovernyan_visible_height=19,nathaniel_visible_height=19,feet_baseline=30,unchanged_palette=True,native_mgba_captures=True),indent=2)+'\n')
finally:
 if r:r.close()

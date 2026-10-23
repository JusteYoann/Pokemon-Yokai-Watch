#!/usr/bin/env python3
"""Short real mGBA introductions; map/player/script fixtures, no edited battle output."""
import os,subprocess,json,hashlib
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,warp,strong_party
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/dossier-20261023/tests'/mode;D.mkdir(parents=True,exist_ok=True)
cases=[('zazel','PokemonLeague_LoreleisRoom','Lorelei',5,7),('enma-ancien','PokemonLeague_BrunosRoom','Bruno',5,7),('orqanos','PokemonLeague_AgathasRoom','Agatha',5,7),('maitre-nyada','PokemonLeague_LancesRoom','Lance',5,7),('domniscian','SaffronCity_Gym','Sabrina',14,13),('berenice','FuchsiaCity_Gym','Koga',4,9)];rows=[]
for name,mapname,label,x,y in cases:
 r=new_game();frames=[]
 try:
  actions={int(l.split()[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(l.split())==3 and l.split()[2]=='HandleInputChooseAction'}
  r.call('VarSet',0x4068,1);r.call('FlagSet',0x3E);warp(r,*MAPS[mapname],x,y);strong_party(r);r.call('ScriptContext_SetupScript',r.symbols[mapname+'_EventScript_'+label]);started=False
  for f in range(5000):
   r.keys={8} if f%16<4 else set();r.run();battle=r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
   if battle and f%8==0:
    im=r.frame.copy()
    if im.getbbox():started=True;frames.append(im)
   if started and battle and r.u32(r.symbols['gBattlerControllerFuncs']) in actions:
    r.keys=set();r.run(24);frames.append(r.frame.copy());break
  else:raise AssertionError(name+' did not reach action menu')
  fs=[im.resize((480,320),Image.Resampling.NEAREST) for im in frames];fs[0].save(D/(name+'-extrait-intro.gif'),save_all=True,append_images=fs[1:],duration=135,loop=0)
  rows.append({'character':name,'native_frames':f,'sampled_frames':len(fs),'file':name+'-extrait-intro.gif'})
 finally:
  sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close()
(D/'EXTRAITS.json').write_text(json.dumps({'passed':True,'scope':__doc__,'rom_sha256':sha,'captures':rows},indent=2)+'\n')

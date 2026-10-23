#!/usr/bin/env python3
"""Actual native intro selection for both sexes, with complete first-page captures."""
import os,json,hashlib
from pathlib import Path
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,warp,strong_party
rom=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba'));mode='prive' if '_audio' in rom.name else 'public';P=ROOT/'docs/champions-yokai-watch/validation'/mode;P.mkdir(parents=True,exist_ok=True)
rows=[];passed=False;r=None
try:
 for gender in [0,1]:
  r=new_game(gender);base=r.snapshot()
  for key,city,leader,x,y,intro in [('katie' if gender==0 else 'nathan','CeruleanCity','Misty',7,6,'MistyIntro' if gender==0 else 'NathanIntro'),('nathaniel' if gender==0 else 'michael','CinnabarIsland','Blaine',3,5,'BlaineIntro' if gender==0 else 'MichaelIntro')]:
   r.restore(base);warp(r,*MAPS[city+'_Gym'],x,y);strong_party(r);r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[city+'_Gym_EventScript_'+leader]);r.run(180)
   expected=r.symbols[city+'_Gym_Text_'+intro];assert r.u32(r.symbols['sTrainerAIntroSpeech'])==expected,(gender,key,'wrong native dialogue selected')
   r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(key+'-introduction-complete-x3.png'))
   rows.append(dict(champion=key,gender=gender,passed=True,intro_symbol=city+'_Gym_Text_'+intro))
  r.close();r=None
 passed=True
finally:
 if r:r.close()
 (P/'VARIANTES_DIALOGUES_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),scope=__doc__,results=rows),ensure_ascii=False,indent=2)+'\n')
print('Native dialogue variants PASS',len(rows))

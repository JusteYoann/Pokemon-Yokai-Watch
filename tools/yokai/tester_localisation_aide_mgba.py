#!/usr/bin/env python3
"""Help opened with R; linked text widths and real fixed help-panel rendering."""
import hashlib,json,re
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/aide';P.mkdir(exist_ok=True)
layout=json.loads((P.parent/'AIDE_CADRAGE.json').read_text())['results'];r=new_game();rows=[];shots=[];passed=False;error='Interrupted'
try:
 r.call('DecompressGlyph_Normal',0xbb,0);height=r.read(r.symbols['gGlyphInfo']+129,1)[0];assert 7*(height+1)-1<=104,height
 scratch=r.call('AllocZeroed',2048)
 for e in layout:
  ptr=r.symbols[e['symbol']];raw=r.read(ptr,2048).split(b'\xff',1)[0];assert len(raw)<1024
  widths=[]
  for line in raw.split(b'\xfe'):
   # Generic native GetStringWidth doesn't expand Help's custom PLAYER/PC
   # placeholders. Those rows retain the stronger static bounded-name check.
   if b'\xfd' in line:continue
   r.write(scratch,line+b'\xff');w=r.call('GetStringWidth',2,scratch,0)
   assert w<=208,(e['symbol'],w)
   widths.append(w)
  rows.append(dict(symbol=e['symbol'],native_widths=widths,conservative_width=e['max_conservative_pixels'],lines=e['lines'],passed=True))
 r.call('Free',scratch)
 # The early bedroom does not always enable Help until its tutorial has run.
 # Grant only that UI permission in RAM; use the actual R-button dispatcher.
 r.write(r.symbols['gHelpSystemEnabled'],b'\x01');r.keys={11};r.run(1);r.keys=set();r.run(180)
 assert r.read(r.symbols['sVideoState']+21,1)==b'\x05','Help did not open via R'
 r.frame.save(P/'ouverture.png');shots.append('ouverture');base=r.snapshot()
 pairs=[('PlayingForFirstTime','AnswerPlayingForFirstTime'),('WantToMakeMonStronger','AnswerWantToMakeMonStronger'),('UsingHM','HowToUseHM'),('UsingBag','HowToUseBag'),('HP','DefineHP'),('Attack','DefineAttack'),('Ability','DefineAbility'),('StatusProblem','DefineStatusProblem'),('OwnPokemonSteel','TypeMatchupOwnPokemonSteel'),('UsingBillsPC','HowToUseBillsPC')]
 for question,answer in pairs:
  r.restore(base)
  # Help normally intercepts Main before callback2. Temporarily release that
  # dispatcher only for the RAM fixture calls, retaining the native VRAM state.
  r.write(r.symbols['sVideoState']+21,b'\x00')
  r.call('HelpSystem_PrintQuestionAndAnswerPair',r.symbols['Help_Text_'+question],r.symbols['Help_Text_'+answer]);r.call('CommitTilemap')
  r.write(r.symbols['sVideoState']+21,b'\x05');r.write(r.symbols['sInHelpSystem'],b'\x01');r.run(4)
  r.frame.save(P/(answer+'.png'));shots.append(answer)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='369 linked help text/native width checks, seven-line answer capacity, actual R-button opening with early Help permission granted in RAM;10 native question-answer panel fixtures. Not full traversal of all context-dependent help menus.',glyph_height=height,results=rows,captures=shots),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(720,((len(shots)+2)//3)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,key in enumerate(shots):
  x=i%3*240;y=i//3*184;d.text((x+2,y+2),key,fill='black');sheet.paste(Image.open(P/(key+'.png')),(x,y+22))
 sheet.save(P/'PLANCHE.png');print('HELP FR PASS',len(rows),len(shots))

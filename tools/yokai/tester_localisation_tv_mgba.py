#!/usr/bin/env python3
"""Native TV ABC menu/input and introductory text; not full tutorial battles."""
import hashlib,json,re
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/tv_abc';P.mkdir(exist_ok=True)
r=new_game();rows=[];shots=[];passed=False;error='Interrupted'
def pulse(key,frames=120):
 r.keys={key};r.run(1);r.keys=set();r.run(frames)
try:
 item=int(re.search(r'^#define\s+ITEM_TM_CASE\s+(\d+)',(ROOT/'include/constants/items.h').read_text(),re.M)[1])
 assert r.call('AddBagItem',item,1)
 r.call('InitTeachyTvController',0,r.symbols['CB2_Overworld']|1);r.run(600)
 r.frame.save(P/'menu.png');shots.append('menu');base=r.snapshot()
 for key in ['TeachBattle','StatusProblems','TypeMatchups','CatchPkmn','AboutTMs','RegisterItem','Cancel']:
  symbol='gTeachyTvString_'+key;width=r.call('GetStringWidth',2,r.symbols[symbol],0)
  assert width<=160,(key,width);rows.append(dict(test='Native linked menu label width',symbol=symbol,width=width,passed=True))
 for i,label in enumerate(['combats','statuts','types','captures','ct','objets']):
  r.restore(base)
  for _ in range(i):pulse(5,15)
  pulse(8,600);r.frame.save(P/(label+'-bonjour.png'));shots.append(label+'-bonjour')
  # Advance the common greeting's two pauses, then allow the episode's first
  # page to finish typing. No claim that the subsequent demo is completed.
  for _ in range(3):pulse(8,240)
  r.frame.save(P/(label+'-episode.png'));shots.append(label+'-episode')
  assert r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1
  rows.append(dict(test='Original TV menu selects episode and displays native introductory text',episode=label,passed=True))
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='7 linked menu widths and6 original TV menu selections/introductory rendering, with TM Case granted as a fixture to unlock all6 lessons. Does not test full scripted demo outcomes, capture or reward.',results=rows),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(720,((len(shots)+2)//3)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,key in enumerate(shots):
  x=i%3*240;y=i//3*184;d.text((x+2,y+2),key,fill='black');sheet.paste(Image.open(P/(key+'.png')),(x,y+22))
 sheet.save(P/'PLANCHE.png');print('TV FR PASS',len(rows))

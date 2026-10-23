#!/usr/bin/env python3
"""Native screenshots for the replayable pending-reward state and paired intro.
State2 is a reward-recovery fixture; the full chapter suite separately earns victory.
"""
import os,json,hashlib
from PIL import Image
from mgba_new_game import new_game
from mafiamille_qa import warp,strong_party,C,MAPS
from mgba_rpc import ROOT
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';P=ROOT/'docs/pierre-philosovni/validation'/mode;P.mkdir(parents=True,exist_ok=True)
r=new_game();strong_party(r);initial=r.snapshot();rows=[]
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
try:
 r.call('VarSet',0x40f4,2);warp(r,*MAPS['VermilionCity_PhilosovniWarehouse'],6,8);r.call('ScriptContext_SetupScript',r.symbols['Philosovni_Reward'])
 for f in range(5000):
  r.keys={8} if f%16<4 else set();r.run();p=r.u32(r.symbols['sGlobalScriptContext']+8)
  if r.symbols['EventScript_ObtainedItem']+5<=p<r.symbols['EventScript_ObtainedItem']+8:
   r.keys=set();r.run(600);assert r.call('BagGetQuantityByItemId',C['ITEM_HM01'])==1;shot('remise-cs-coupe');frames=[]
   for _ in range(15):r.keys=set();r.run(4);frames.append(r.frame.resize((480,320),Image.Resampling.NEAREST))
   frames[0].save(P/'remise-cs-coupe.gif',save_all=True,append_images=frames[1:],duration=67,loop=0);break
 else:raise AssertionError('Native HM obtained message not observed')
 rows.append(dict(test='Native pending-reward replay gives exactly one HM01 and shows obtained message',passed=True,fixture_state=2))
 r.restore(initial);r.call('VarSet',0x40f4,1);warp(r,*MAPS['VermilionCity_PhilosovniWarehouse'],6,8);r.call('ScriptContext_SetupScript',r.symbols['Philosovni_Overhear'])
 for f in range(12000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.read(r.symbols['gDisplayedStringBattle'],16)==r.read(r.symbols['sPhilosovniIntro'],16):
   r.keys=set();last=r.frame.copy()
   for _ in range(700):
    previous=r.frame.copy();r.run()
    if r.read(r.symbols['gDisplayedStringBattle'],16)!=r.read(r.symbols['sPhilosovniIntro'],16):
     last=previous;break
   last.save(P/'deux-sbires-introduction.png');last.resize((720,480),Image.Resampling.NEAREST).save(P/'deux-sbires-introduction-x3.png');break
 else:raise AssertionError('Paired native battle intro not observed')
 rows.append(dict(test='Two-grunt native trainer introduction photographed',passed=True))
 (P/'CAPTURES_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=rows),ensure_ascii=False,indent=2)+'\n')
finally:r.close()

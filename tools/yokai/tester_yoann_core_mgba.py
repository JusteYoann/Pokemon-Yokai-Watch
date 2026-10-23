#!/usr/bin/env python3
"""Native fixtures for quest core only; original Yoann artwork is still required.
No claim of NPC appearance, battle integration, or a full quest playthrough.
"""
import os,json,hashlib,struct,re
from pathlib import Path
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
D=ROOT/'docs/juste-yoann/core'/mode;D.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False;frames=[]
def report(test,**kw):
 rows.append(dict(test=test,passed=True,**kw));print(test,kw,flush=True)
def finish(limit=6000,record=False):
 for f in range(limit):
  r.keys={8} if f%24<4 else set();r.run()
  if record and f%6==0:frames.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2':
   r.keys=set();r.run(24);return
 raise AssertionError('Script failed to finish')
try:
 base=r.snapshot();assert not r.call('YoannMedalliumComplete')
 keys=[i for i,item in enumerate(json.loads((ROOT/'src/data/items.json').read_text())['items']) if item['pocket']=='POCKET_KEY_ITEMS' and i!=52]
 for item in keys:
  if not r.call('CheckBagHasSpace',52,1):break
  r.call('AddBagItem',item,1)
 assert not r.call('CheckBagHasSpace',52,1)
 r.call('YoannGiveCharm');assert not r.call('FlagGet',0x333);assert r.read(r.symbols['gSpecialVar_Result'],2)==b'\0\0'
 assert r.call('RemoveBagItem',keys[0],1);r.call('YoannGiveCharm');assert r.call('CheckBagHasItem',52,1) and r.call('FlagGet',0x333)
 report('Full key-item pocket defers reward safely; freeing a slot allows one successful retry')
 r.restore(base)
 for n in range(1,152):r.call('GetSetPokedexFlag',n,2)
 assert not r.call('YoannMedalliumComplete');report('151 seen does not satisfy completion')
 for n in range(1,151):r.call('GetSetPokedexFlag',n,3)
 assert not r.call('YoannMedalliumComplete');report('150 owned does not satisfy completion, including missing151')
 r.call('GetSetPokedexFlag',151,3);assert r.call('YoannMedalliumComplete')
 r.call('YoannCheckCompletion');assert r.read(r.symbols['gSpecialVar_Result'],2)==b'\1\0'
 r.call('FlagSet',0x331);r.call('YoannCheckCompletion');assert r.read(r.symbols['gSpecialVar_Result'],2)==b'\0\0'
 r.call('YoannSyncVisibility');assert not r.call('FlagGet',0x334)
 r.call('FlagClear',0x331);r.call('YoannSyncVisibility');assert r.call('FlagGet',0x334)
 report('151 owned accepted; invitation state and visibility flag are persistent and independent')
 r.restore(base);assert r.call('ItemId_GetImportance',52)==2;assert r.call('ItemId_GetPocket',52)==C['POCKET_KEY_ITEMS']
 r.call('YoannGiveCharm');assert r.call('FlagGet',0x333);assert r.call('CheckBagHasItem',52,1);assert not r.call('CheckBagHasItem',52,2)
 r.call('YoannGiveCharm');assert r.read(r.symbols['gSpecialVar_Result'],2)==b'\0\0';assert not r.call('CheckBagHasItem',52,2)
 report('Charm is a key item, importance2, given exactly once')
 assert r.call('TrySavingData',0,max_frames=1200)==1;assert r.call('LoadGameSave',0,max_frames=1200)==1;r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);finish()
 assert r.call('CheckBagHasItem',52,1) and r.call('FlagGet',0x333);report('Native Flash save and Continue preserve charm and given flag')
 # Check every compiled text line with the real font.
 labels=[n for n in r.symbols if n.startswith('Yoann_Text_')]+['gItemDescription_ITEM_SHINY_CHARM']
 count=0
 for name in labels:
  raw=r.read(r.symbols[name],2048).split(b'\xff',1)[0]
  for line in re.split(b'[\xfe\xfa\xfb]',raw):
   assert len(line)<128,(name,len(line));r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0)
   assert width<=216,(name,width)
   count+=1
 report('All compiled dialogue and item-description lines measured with native font',lines=count)
 r.restore(base);warp(r,*MAPS['PalletTown_PlayersHouse_2F'],6,7)
 original=r.read(r.symbols['gPlttBufferUnfaded'],1024)
 r.call('ScriptContext_SetupScript',r.symbols['Yoann_EventScript_FirstVictory']);thank_seen=False
 for f in range(8000):
  r.keys={8} if f%24<4 else set();r.run()
  if f%6==0:frames.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
  for i in range(16):
   p=r.symbols['gTasks']+40*i
   if r.u32(p)==r.symbols['Task_YoannThank']|1 and r.read(p+4,1)==b'\1' and struct.unpack('<h',r.read(p+8,2))[0]==1 and struct.unpack('<h',r.read(p+12,2))[0]>60:
    if not thank_seen:r.frame.save(D/'thank-for-play.png');thank_seen=True
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2':break
 else:raise AssertionError('Scene did not return control')
 r.keys=set();r.run(60);assert thank_seen;assert r.call('FlagGet',0x332) and r.call('FlagGet',0x333);assert r.call('CheckBagHasItem',52,1)
 r.frame.save(D/'chambre-apres-scene.png')
 assert r.read(r.symbols['gPlttBufferFaded'],1024)==r.read(r.symbols['gPlttBufferUnfaded'],1024),'White tint persisted'
 assert r.read(r.symbols['gPlttBufferUnfaded'],14*32)==original[:14*32],'Map palettes changed'
 assert not any(r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_YoannThank']|1 and r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' for i in range(16))
 report('Full dialogue/white-scene core, exact THANK FOR PLAY, reward and palette restoration',npc_art_integrated=False)
 passed=True
finally:
 if frames:frames[0].save(D/'scene-core-sans-pnj.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=sha,checks=rows),ensure_ascii=False,indent=2)+'\n')

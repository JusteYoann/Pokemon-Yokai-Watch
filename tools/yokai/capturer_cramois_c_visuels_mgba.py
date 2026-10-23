#!/usr/bin/env python3
"""Additional native phase C captures: both companion orientations, collision, interaction, quiz prompts. Explicit map/orientation fixtures, no graphic simulation."""
import os,json,hashlib,struct,traceback
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,warp,strong_party,C
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/cramois-ile-passe/phase-c'/mode;D.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False;failure=None

def run(n,key=None):r.keys=set() if key is None else {key};r.run(n)
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-x4.png'))
def free():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]
def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def task(name):return any(r.u32(r.symbols['gTasks']+40*i)==r.symbols[name]|1 and r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' for i in range(16))
def actor(local):
 for i in range(16):
  o=r.read(r.symbols['gObjectEvents']+36*i,36)
  if o[0]&1 and o[8]==local:return r.symbols['gObjectEvents']+36*i,o
 raise AssertionError(local)
def playerpos():
 o=r.read(r.symbols['gObjectEvents']+36*r.read(r.symbols['gPlayerAvatar']+5,1)[0],36);return struct.unpack_from('<hh',o,16)
try:
 strong_party(r);r.call('VarSet',0x40f4,3);warp(r,*MAPS['CinnabarIsland_Gym'],5,5);shot('compagnon-face')
 ptr,o=actor(10);r.call('ObjectEventForceSetHeldMovement',ptr,5);run(30);shot('compagnon-dos-cape');r.call('ObjectEventClearHeldMovementIfFinished',ptr)
 sprite=r.symbols['gSprites']+68*o[4];assert r.read(sprite+42,1)[0]==1;report('Native back-facing companion uses supplied cape-covered frame')
 r.call('ObjectEventForceSetHeldMovement',ptr,4);run(30);r.call('ObjectEventClearHeldMovementIfFinished',ptr)
 warp(r,*MAPS['CinnabarIsland_Gym'],6,5);p=playerpos();run(40,4);assert playerpos()==p;report('Companion occupies its tile and blocks overlap normally')
 run(1,8);run(240);shot('interaction-hovernyan')
 for f in range(1200):
  run(1,8 if f%16<4 else None)
  if f>30 and free():break
 else:raise AssertionError('companion interaction stuck')
 assert not r.call('FlagGet',0x32e) and not r.call('FlagGet',0x32d);report('Companion native A interaction returns control and grants no gift')
 # Rebuild through a full screen menu, then verify the own OBJ bank again.
 r.call('CB2_BagMenuFromStartMenu');run(180);run(1,0);run(180)
 if not free():run(1,0);run(90)
 assert free();_,o=actor(10);assert r.read(r.symbols['gPlttBufferUnfaded']+768,32)==r.read(r.symbols['gObjectEventPal_CramoisHovernyan'],32);report('Fullscreen Bag exit restores companion tile and palette')
 # Native sign prompts photographed before choosing any response.
 gym=json.loads((ROOT/'data/maps/CinnabarIsland_Gym/map.json').read_text())
 for i in range(1,7):
  e=next(x for x in gym['bg_events'] if x['script'].endswith(f'Quiz{i}Left'));warp(r,*MAPS['CinnabarIsland_Gym'],e['x'],e['y']+1);run(1,4);run(18);run(1,8)
  for f in range(3000):
   if task('Task_YesNoMenu_HandleInput'):break
   run(1,8 if f%16<4 else None)
  else:raise AssertionError(('quiz menu',i))
  run(30);shot(f'question-{i}');report(f'Native approved question {i} displayed with Yes/No menu')
  # End without touching opponents: restore via a new isolated game for next capture.
  if i!=6:r.close();r=new_game();strong_party(r);r.call('VarSet',0x40f4,3)
 passed=True
except BaseException:failure=traceback.format_exc();print(failure,flush=True);shot('ECHEC-VISUELS')
finally:
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(D/'VISUELS_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=sha,checks=rows,failure=failure,fixtures=__doc__),ensure_ascii=False,indent=2)+'\n')
assert passed,failure

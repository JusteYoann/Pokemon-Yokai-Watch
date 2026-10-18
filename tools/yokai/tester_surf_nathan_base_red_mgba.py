#!/usr/bin/env python3
"""Actual Surf entry, four native facings on water, controller exit to land.

Real new game, prepared party and shore warp. Not HM/badge progression proof.
"""
import hashlib,json
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/NATHAN_GABARIT_RED/surf';P.mkdir(parents=True,exist_ok=True)
def contact(frames,name):
 out=Image.new('RGB',(960,320),(224,224,224))
 for i in range(8):out.paste(frames[round(i*(len(frames)-1)/7)],((i%4)*240,(i//4)*160))
 out.save(P/(name+'.png'))
r=new_game();passed=False;error='Interrupted'
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],57,0)
 r.call('SetWarpDestination',3,39,255,12,10);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 obj=r.symbols['gObjectEvents']+r.read(r.symbols['gPlayerAvatar']+5,1)[0]*36;r.call('ObjectEventTurn',obj,1)
 assert r.call('IsPlayerFacingSurfableFishableWater'),'Not at the actual Route21 North shore'
 r.w32(r.symbols['gFieldEffectArguments'],0);r.call('FldEff_UseSurf');movie=[]
 for f in range(1500):
  r.run()
  if f%4==0:movie.append(r.frame.copy())
  if f>60 and f%16==0 and r.call('FindTaskIdByFunc',r.symbols['Task_FldEffUseSurf']|1)==255:break
 else:raise AssertionError('Surf field effect did not complete')
 assert r.read(r.symbols['gPlayerAvatar'],1)[0]&8;contact(movie,'entree-surf');r.frame.save(P/'sur-eau.png')
 r.call('LockPlayerFieldControls');movie=[]
 for direction in [1,2,3,4]:
  r.call('ObjectEventTurn',obj,direction)
  for f in range(48):
   r.run()
   if f%4==0:movie.append(r.frame.copy())
 contact(movie,'quatre-directions');r.call('UnlockPlayerFieldControls');r.keys={4}
 for f in range(100):
  r.run()
  if not r.read(r.symbols['gPlayerAvatar'],1)[0]&8:break
 r.keys=set();r.run(90);assert not r.read(r.symbols['gPlayerAvatar'],1)[0]&8,'Did not return to shore';r.frame.save(P/'sortie-surf.png');passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),hm_progression_checked=False),indent=2)+'\n')
print('PASS real Surf field effect, actual water/four facings, UP input to leave water')

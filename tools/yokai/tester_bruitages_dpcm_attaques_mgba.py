#!/usr/bin/env python3
"""Stress native move SFX under the actual compiled DPCM music, no ROM patch."""
import hashlib,json,os,struct
from pathlib import Path
import tester_animations_attaques_mgba as t
r=None;rows=[];failures=[];fatal=None
moves=[57,59,63,87,89,91,126,138,153,195,200,211,232,248,304,307,309,318,323,334,338,350,354]
def voice(r):
 for i in range(5):
  p=r.symbols['gSoundInfo']+80+64*i
  if r.u32(p+36)==r.symbols['yokai_wave_17'] and r.read(p,1)[0]&0x83:return p
 return None
try:
 r,_,_=t.setup((15,147),False);r.call('PlayBGM',363);r.run(60);assert voice(r);base=r.snapshot()
 for move in moves:
  for side in [0,1]:
   r.restore(base);r.write(r.symbols['gBattlerAttacker'],bytes([side]));r.write(r.symbols['gBattlerTarget'],bytes([1-side]));r.write(r.symbols['gActiveBattler'],bytes([side]));r.write(r.symbols['gAnimMoveTurn'],b'\x00');r.write(r.symbols['gAnimFriendship'],b'\xdc');r.write(r.symbols['gAnimMovePower'],r.read(r.symbols['gBattleMoves']+12*move+1,1)+b'\0');r.w32(r.symbols['gAnimMoveDmg'],10);r.w32(r.symbols['gAnimDisableStructPtr'],r.symbols['gDisableStructs']+0x1C*side);r.call('SetBattlerSpriteAffineMode',0);r.call('DoMoveAnim',move);absent=[]
   for f in range(2400):
    if not r.read(r.symbols['gAnimScriptActive'],1)[0]:break
    r.call(r.u32(r.symbols['gAnimScriptCallback']));r.run()
    if voice(r) is None:absent.append(f)
   else:raise AssertionError(('Animation not finished',move,side))
   r.run(120);present=voice(r) is not None;row=dict(move=move,side=side,frames=f,missing_voice_frames=len(absent),sampled_music_present_after_animation=present)
   rows.append(row)
   if not present:failures.append(row)
   print('MOVE',move,'SIDE',side,'BGM_AFTER',present,'ABSENT',len(absent),flush=True)
except BaseException as e:fatal=type(e).__name__+': '+str(e);raise
finally:
 if r:r.close()
 report=dict(passed=not failures and fatal is None and len(rows)==len(moves)*2,fatal=fatal,rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),scope='Actual compiled private BGM during selected loud/multi-SFX native attack animations; fixture calls/snapshots, not hardware CPU profiling or all soundtrack/move combinations',results=rows,failures=failures)
 (t.ROOT/'QA_RECETTE_FINALE/INTEGRATION_MUSIQUES/BRUITAGES_ATTAQUES_DPCM.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],failures=len(failures),cases=len(rows))),flush=True)

#!/usr/bin/env python3
"""Render native move scripts in real mGBA battle scenes, both attack sides.

Prepared mons/battle and direct DoMoveAnim/callback calls are explicit fixtures.
No ROM patch, no rewrite of animations, no claim of whole-battle effects/hardware.
Snapshots isolate each animation; no savedata is read/written between restores.
"""
import argparse,hashlib,json,struct,subprocess
from pathlib import Path
from PIL import Image
from mgba_rpc import Emulator,ROOT
import tester_cameos_boss_mgba as b
P=ROOT/'QA_RECETTE_FINALE/ANIMATIONS_ATTAQUES';P.mkdir(exist_ok=True);(P/'preuves').mkdir(exist_ok=True)
PAIRS=[(1,33),(15,147),(150,19),(114,84),(86,100),(98,127)]
SPECIAL={106,107,151,211,232,293,334}
TWO_TURN={13,19,76,91,130,143,291,340}
rows=[];errors=[]
def setup(pair,shiny):
 r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(b.glyphs[c] for c in 'Test')+b'\xff')
 for symbol,species in [('gPlayerParty',pair[0]),('gEnemyParty',pair[1])]:
  r.call('CreateMon',r.symbols[symbol],species,50,31,1,0 if shiny else 100,1,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.write(r.symbols['gEnemyPartyCount'],b'\x01');r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],33,0)
 actual=[bool(r.call('IsMonShiny',r.symbols[s])) for s in ['gPlayerParty','gEnemyParty']]
 callbacks={int(line.split()[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(line.split())==3 and line.split()[2]=='HandleInputChooseAction'}
 r.call('StartScriptedWildBattle')
 for f in range(7000):
  r.keys={0} if f%16<2 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Battle scene did not reach action menu')
 r.keys=set();r.run(60)
 # Freeze the idle input controllers: otherwise HandleInputChooseAction
 # re-creates bouncing every frame, unlike a real move after selection.
 for side in range(4):r.w32(r.symbols['gBattlerControllerFuncs']+4*side,r.symbols['BattleControllerDummy']|1)
 # As the actual move controller does, end selection-menu bouncing before
 # animation. Otherwise it rewrites y2 while Dig waits for exact zero.
 for side in [0,1]:
  r.call('EndBounceEffect',side,0);r.call('EndBounceEffect',side,1)
 r.run(4);return r,r.snapshot(),actual

def tiles(r,side):
 sid=r.read(r.symbols['gBattlerSpriteIds']+side,1)[0];sp=r.symbols['gSprites']+68*sid
 tile=struct.unpack('<H',r.read(sp+4,2))[0]&1023
 return hashlib.sha256(r.read(0x06010000+tile*32,0x800)).hexdigest()
def palettes(r):
 out=[]
 for side in [0,1]:
  sid=r.read(r.symbols['gBattlerSpriteIds']+side,1)[0];slot=struct.unpack('<H',r.read(r.symbols['gSprites']+68*sid+4,2))[0]>>12
  out.append(hashlib.sha256(r.read(r.symbols['gPlttBufferFaded']+512+32*slot,32)).hexdigest())
 return out
def contact(frames,name):
 if not frames:return
 out=Image.new('RGB',(240*4,160*2),(224,224,224))
 for i in range(8):out.paste(frames[round(i*(len(frames)-1)/7)],((i%4)*240,(i//4)*160))
 out.save(P/'preuves'/name)
def run(moves):
 for index,pair in enumerate(PAIRS):
  subset=[m for m in moves if (m-1)%len(PAIRS)==index]
  if not subset:continue
  for shiny in [False,True]:
   r,base,actual=setup(pair,shiny)
   try:
    for move in subset:
     # All 354 scripts on each side in normal and requested shiny fixtures.
     for side in [0,1]:
      for turn in ([0,1] if move in TWO_TURN else [0]):
       r.restore(base);before=[tiles(r,0),tiles(r,1)];pal_before=palettes(r);r.write(r.symbols['gBattlerAttacker'],bytes([side]));r.write(r.symbols['gBattlerTarget'],bytes([1-side]));r.write(r.symbols['gActiveBattler'],bytes([side]))
       r.write(r.symbols['gAnimMoveTurn'],bytes([turn]));r.write(r.symbols['gAnimFriendship'],b'\xdc');r.write(r.symbols['gAnimMovePower'],r.read(r.symbols['gBattleMoves']+12*move+1,1)+b'\x00');r.w32(r.symbols['gAnimMoveDmg'],10);r.w32(r.symbols['gAnimDisableStructPtr'],r.symbols['gDisableStructs']+0x1C*side)
       r.call('SetBattlerSpriteAffineMode',0);r.call('DoMoveAnim',move);frames=[];seen=False
       for f in range(2400):
        if not r.read(r.symbols['gAnimScriptActive'],1)[0]:break
        seen=True;r.call(r.u32(r.symbols['gAnimScriptCallback']));r.run()
        if move in SPECIAL and f%8==0:frames.append(r.frame.copy())
       else:
        errors.append(dict(move=move,side=side,turn=turn,shiny_requested=shiny,reason='Native animation exceeded2400 callback/render steps'));r.frame.save(P/'preuves'/f'erreur-{move}-{side}-{int(shiny)}.png');continue
       assert seen
       r.call('SetBattlerSpriteAffineMode',1);r.run(2)
       after=[tiles(r,0),tiles(r,1)];unchanged=before==after;pal_after=palettes(r)
       if frames:contact(frames,f'attaque-{move:03d}-cote-{side}-shiny-{int(shiny)}.png')
       rows.append(dict(move=move,side=side,turn=turn,pair=list(pair),shiny_requested=shiny,actual_shiny=actual,native_callback_render_steps=f,native_script_finished=True,battler_tile_bytes_unchanged=unchanged,battler_palettes_restored=(pal_before==pal_after),visual_task_count=r.read(r.symbols['gAnimVisualTaskCount'],1)[0],sound_task_count=r.read(r.symbols['gAnimSoundTaskCount'],1)[0],human_visual_review=False))
       if len(rows)%40==0:print('CASES',len(rows),'last move',move,flush=True)
   finally:r.close()
  print('PAIR COMPLETE',pair,flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--moves',default='all');args=parser.parse_args();moves=list(range(1,355)) if args.moves=='all' else [int(x) for x in args.moves.split(',')];fatal=None
 try:run(moves)
 except Exception as e:fatal=str(e);raise
 finally:
  # Completion is runtime-only: palette/masking/geometry still need image review.
  passed=not errors and fatal is None
  report=dict(passed=passed,fatal=fatal,errors=errors,rom_sha256=hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),scope='Actual GBA native animation scripts/callbacks and rendering in mGBA; seeded battle/DoMoveAnim/snapshots, not actual move effects/AI, full adventure or physical hardware',moves_requested=moves,distinct_moves_completed=sorted({r['move'] for r in rows}),cases=len(rows),visual_validation_complete=False,results=rows)
  (P/'TEST_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=passed,fatal=fatal,errors=len(errors),cases=len(rows))),flush=True)

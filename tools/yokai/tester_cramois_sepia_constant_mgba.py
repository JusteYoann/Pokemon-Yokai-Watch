#!/usr/bin/env python3
"""Native mGBA: Cinnabar terrain/trainers/Yo-kai remain sepia in both OBJ and animation BG; UI remains native. Explicit new-game/map/party/move fixtures; no enemy HP/outcome changes."""
import os,json,hashlib,struct,traceback,subprocess
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/cramois-ile-passe/phase-c/sepia-combat-constant'/mode;D.mkdir(parents=True,exist_ok=True)
lut=struct.unpack('<32768H',(ROOT/'data/yokai/cramois-sepia-rgb555.bin').read_bytes());r=None;checks=[];movies={};passed=False;failure=None

def report(name,**kw):checks.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def run(n,key=None):r.keys=set() if key is None else {key};r.run(n)
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-x4.png'))
def free():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]
def verify(mask,label):
 for attempt in range(16):
  run(1);src=struct.unpack('<512H',r.read(r.symbols['gPlttBufferFaded'],1024));actual=struct.unpack('<512H',r.read(0x05000000,1024));expected=tuple(lut[c&32767] if mask>>(i//16)&1 else c for i,c in enumerate(src))
  if actual==expected:break
 else:raise AssertionError((label,[i for i in range(512) if actual[i]!=expected[i]][:20]))
 report(label,palette_mask=hex(mask),untinted_colors_match_native=True)
def choose_action():
 for f in range(6000):
  run(1,8 if f%16<4 else None)
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:run(16);return
 raise AssertionError('action menu not reached')
try:
 r=new_game();callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
 r.call('VarSet',0x40f4,3);warp(r,*MAPS['CinnabarIsland_Gym'],5,5);verify(0x0fff1fff,'Island overworld sepia unchanged');shot('overworld-sepia-conserve')
 # Native leader introduction proves trainer palettes are still sepia.
 r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('FlagSet',0x32c)
 r.call('ScriptContext_SetupScript',r.symbols['CinnabarIsland_Gym_EventScript_Blaine'])
 for f in range(2500):
  run(1,8 if f%16<4 else None)
  if r.u32(r.symbols['gMain']+4)!=r.symbols['BattleMainCB2']|1:continue
  sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
  if sid<64:
   sp=r.symbols['gSprites']+68*sid
   if r.read(sp+62,1)[0]&1 and int.from_bytes(r.read(sp+6,2),'little')==C['TRAINER_PIC_YOKAI_NATHANIEL']:
    run(60);mask=0xf031c | (1<<(16+(int.from_bytes(r.read(sp+4,2),'little')>>12)));verify(mask,'Native Nathaniel introduction retains trainer sepia');shot('portrait-sepia-conserve');break
 else:raise AssertionError('trainer portrait missing')
 # Fresh native wild fixtures on the same island, each at a real action menu.
 r.close();r=new_game();r.call('VarSet',0x40f4,3);warp(r,*MAPS['CinnabarIsland_Gym'],5,5)
 for party,n,level in [('gPlayerParty',1,100),('gEnemyParty',149,45)]:r.call('CreateMon',r.symbols[party],n,level,31,1,100,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.symbols['gEnemyPartyCount'],b'\1');r.call('StartScriptedWildBattle');choose_action();verify(0xf031c,'Wild battle: terrain and both Yo-kai remain sepia');shot('yokai-sepia-constant')
 # Enter and cancel the actual battle Bag via controller; keep its UI native.
 run(1,7);run(16);run(1,8);run(240);verify(0,'Battle Bag keeps original fullscreen interface colors');shot('sac-combat-couleurs-normales')
 run(1,0)
 for f in range(2000):
  run(1)
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:run(20);break
 else:raise AssertionError('battle Bag did not return')
 verify(0xf031c,'Battle Bag cancellation restores constant battle sepia')
 state=r.snapshot()
 # Exercise both native monbg destinations with the actual active Yo-kai palettes.
 for b,to_bg,label in [(1,False,'BG1'),(0,True,'BG2')]:
  r.restore(state);r.call('MoveBattlerSpriteToBG',b,int(to_bg));
  run(20);verify(0xf031c,'Native '+label+' copy retains identical Yo-kai sepia');shot('copie-'+label.lower())
 # Actual controller attacks, including palette blends and temporary replacement backgrounds.
 for move in ['MOVE_TACKLE','MOVE_AERIAL_ACE','MOVE_SHADOW_BALL']:
  r.close();r=new_game();r.call('VarSet',0x40f4,3);warp(r,*MAPS['CinnabarIsland_Gym'],5,5)
  for party,n,level in [('gPlayerParty',1,100),('gEnemyParty',149,45)]:r.call('CreateMon',r.symbols[party],n,level,31,1,100,0,0)
  r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.symbols['gEnemyPartyCount'],b'\1');r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C[move],0)
  r.call('StartScriptedWildBattle');choose_action()
  frames=[];seen_move=False;hidden_frames=0;matched=0;watched=[8,9,16,17];previous={bank:tuple(lut[c&32767] for c in struct.unpack('<16H',r.read(r.symbols['gPlttBufferFaded']+32*bank,32))) for bank in watched}
  for f in range(5000):
   # Fixture has one valid first move: pure controller input, no RPC frame.
   r.keys={8} if f%16<4 else set();r.run()
   if f%6==0:frames.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
    seen_move|=int.from_bytes(r.read(r.symbols['gCurrentMove'],2),'little')==C[move]
    for bank in watched:
     current=tuple(lut[c&32767] for c in struct.unpack('<16H',r.read(r.symbols['gPlttBufferFaded']+32*bank,32)));hw=struct.unpack('<16H',r.read(0x05000000+32*bank,32))
     assert hw in [current,previous[bank]],(move,f,bank,'battle sepia mismatch')
     previous[bank]=current
    matched+=1
    for b in [0,1]:
     sid=r.read(r.symbols['gBattlerSpriteIds']+b,1)[0]
     if sid<64 and r.read(r.symbols['gSprites']+68*sid+62,1)[0]&4:hidden_frames+=1
   if f>120 and free():break
  assert seen_move and matched>60 and free(),(move,seen_move,matched,free());verify(0x0fff1fff,move+' victory returns to unchanged island sepia')
  movies[move.lower()]=frames;report(move+' native attack keeps Yo-kai sepia through animation and return',checked_battle_frames=matched,hidden_sprite_samples=hidden_frames)
 # Same two creatures outside Cinnabar keep normal terrain and colors.
 warp(r,*MAPS['PalletTown'],8,8)
 r.call('CreateMon',r.symbols['gEnemyParty'],149,45,31,1,100,0,0);r.call('StartScriptedWildBattle');choose_action();verify(0,'Outside island: terrain and Yo-kai remain native');shot('hors-ile-couleurs-normales')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True)
 if r:shot('ECHEC')
finally:
 for name,frames in movies.items():
  if frames:frames[0].save(D/(name+'.gif'),save_all=True,append_images=frames[1:],duration=100,loop=0)
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest() if r else None
 if r:r.close()
 (D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=sha,checks=checks,failure=failure,scope=__doc__),ensure_ascii=False,indent=2)+'\n')
assert passed,failure

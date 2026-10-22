#!/usr/bin/env python3
"""Real action-controller turns for Transform/Substitute and a double battle fixture."""
import hashlib,json,os,subprocess,struct
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
Q=ROOT/'QA_RECETTE_FINALE/COMBATS_ETENDUS/cas-particuliers';Q.mkdir(exist_ok=True);rows=[]
def begin(move=33,double=False):
 r=new_game()
 for symbol,nums in [('gPlayerParty',[29,19] if double else [29]),('gEnemyParty',[19,150] if double else [19])]:
  for i,n in enumerate(nums):
   r.call('CreateMon',r.symbols[symbol]+100*i,n,50,31,1,100,0 if symbol=='gPlayerParty' else 1,0);r.call('SetMonMoveSlot',r.symbols[symbol]+100*i,move if symbol=='gPlayerParty' else 150,0)
   if symbol=='gEnemyParty':
    for slot in range(4):r.call('SetMonMoveSlot',r.symbols[symbol]+100*i,150,slot)
 for name in ['gPlayerPartyCount','gEnemyPartyCount']:r.write(r.symbols[name],bytes([2 if double else 1]))
 r.call('StartScriptedWildBattle')
 if double:r.w32(r.symbols['gBattleTypeFlags'],r.u32(r.symbols['gBattleTypeFlags'])|1)
 r.choose={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
 for frame in range(9000):
  r.keys={0} if frame%16<2 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in r.choose:break
 else:raise AssertionError('Battle did not reach action menu')
 r.keys=set();r.run(12);return r
for move in [144,164]:
 r=begin(move)
 try:
  r.frame.save(Q/f'move-{move}-avant.png');oldhp=int.from_bytes(r.read(r.symbols['gBattleMons']+0x28,2),'little');oldpp=r.read(r.symbols['gBattleMons']+0x24,1)[0]
  # Controller buttons choose Combat, then the first move; no animation callback calls.
  for f in range(180):r.keys={8} if f%32<2 else set();r.run()
  r.keys=set();used=False
  for f in range(9000):
   r.keys={8} if f%32<2 else set();r.run();pp=r.read(r.symbols['gBattleMons']+0x24,1)[0]
   used|=pp<oldpp
   if used and r.u32(r.symbols['gBattlerControllerFuncs']) in r.choose:break
  else:
   r.frame.save(Q/f'move-{move}-diagnostic.png')
   raise AssertionError(('Move did not return to action menu',move))
  r.frame.save(Q/f'move-{move}-apres.png');species=int.from_bytes(r.read(r.symbols['gBattleMons'],2),'little');hp=int.from_bytes(r.read(r.symbols['gBattleMons']+0x28,2),'little')
  if move==144:
   assert species==19;path=ROOT/'graphics/yokai/019/back-battle.4bpp';ptr=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4);assert r.read(ptr,2048)==path.read_bytes()
  else:
   assert hp<oldhp and species==29;assert r.call('GetYokaiBattleGeometry',0)==0
  rows.append(dict(test='Native action turn',move=move,passed=True,species_after=species,hp_before=oldhp,hp_after=hp,pp_consumed=True,action_menu_returned=True))
 finally:r.close()
r=begin(double=True)
try:
 assert r.read(r.symbols['gBattlersCount'],1)[0]==4;r.frame.save(Q/'double.png');bounds=[]
 for b in range(4):
  left=r.call('GetBattlerSpriteCoordAttr',b,2);right=r.call('GetBattlerSpriteCoordAttr',b,3);bounds.append([left,right])
  assert left<240 and right<=240,(b,left,right)
 rows.append(dict(test='Native double wild battle fixture,4 actors and action menu',passed=True,bounds=bounds))
finally:r.close()
(Q/'TEST_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),scope=__doc__,results=rows),indent=2)+'\n');print('SPECIAL CASES PASS',len(rows),flush=True)

#!/usr/bin/env python3
"""Native Casino play/help/exit and map entrance captures. No ROM patching.

Controller new game, explicit coins/seed/warps are fixtures. Not a full adventure.
"""
import os,json,hashlib,struct
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp
P=ROOT/os.environ.get('YOKAI_EMBLEM_REPORT_DIR','QA_RECETTE_FINALE/MAFIAMILLE_KANTO/finalisation/apres-public')
P.mkdir(parents=True,exist_ok=True)
r=new_game();results=[];passed=False

def pulse(key,after=30):
 r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(after)
def task():
 state=r.u32(r.symbols['sSlotMachineState']);tid=r.read(state+16,1)[0]
 addr=r.symbols['gTasks']+40*tid
 return state,r.u32(addr),int.from_bytes(r.read(addr+8,2),'little')
def waiting():
 s,f,d=task();return f==r.symbols['MainTask_SlotsGameLoop']|1 and d==0
try:
 base=r.snapshot()
 warp(r,*MAPS['CeladonCity_GameCorner'],8,10)
 r.call('SetCoins',200);r.call('PlaySlotMachine',0,r.symbols['CB2_ReturnToFieldContinueScriptPlayMapMusic']|1);r.run(300)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_RunSlotMachine']|1
 assert waiting();r.frame.save(P/'casino-rouleaux.png')
 pulse(7,120);assert task()[1]==r.symbols['MainTask_ShowHelp']|1
 r.frame.save(P/'casino-gains.png');pulse(6,120);assert waiting()
 r.call('SeedRng',12345);rounds=[]
 for turn in range(3):
  coins=r.call('GetCoins');pulse(11,100) # R: native max bet and start
  assert r.call('GetCoins')==coins-3
  assert any(r.read(task()[0]+20,12)), 'Reels never spinning'
  r.frame.save(P/f'casino-tour-{turn+1}-rotation.png')
  for j in range(3):pulse(8,100)
  for f in range(6000):
   if waiting():break
   r.keys={8,3} if f%16<4 else set();r.run()
  else:raise AssertionError(('Slots round never settled',task()))
  r.keys=set();r.run(20);state=task()[0]
  positions=struct.unpack('<3h',r.read(state+32,6));reward=int.from_bytes(r.read(state+10,2),'little');new=r.call('GetCoins')
  r.frame.save(P/f'casino-tour-{turn+1}-arret.png')
  rounds.append(dict(coins_before=coins,bet=3,coins_after=new,reel_positions=positions,reward_class=reward))
 # Isolated payout fixture: align the existing symbol ID on the centre line.
 # This is a native calculation/VRAM check, not a naturally won jackpot.
 state=task()[0];r.write(state+32,struct.pack('<3h',1,2,18));r.write(state+14,struct.pack('<H',1));r.run(8)
 rank=r.call('CalcPayout');payout=r.call('GetPayout');assert rank==5 and payout==100
 r.frame.save(P/'casino-trois-chapeaux-fixture.png')
 r.write(state+14,b'\x00\x00')
 results.append(dict(test='triple_emblem_native_payout_fixture',forced_RAM_reel_positions=[1,2,18],bet=1,rank=rank,payout=payout,naturally_won=False,passed=True))
 pulse(0,100);pulse(8,600)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
 r.frame.save(P/'casino-sortie.png');results.append(dict(test='casino',native_help_and_exit=True,controller_rounds=rounds,passed=True))
 r.restore(base)
 for name,pos,flag in [('RocketHideout_B1F',(5,15),'FLAG_WORLD_MAP_ROCKET_HIDEOUT_B1F'),('FiveIsland_RocketWarehouse',(12,13),'FLAG_WORLD_MAP_FIVE_ISLAND_ROCKET_WAREHOUSE')]:
  r.restore(base)
  if flag in C:r.call('FlagClear',C[flag])
  r.call('SetWarpDestination',*MAPS[name],255,*pos);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
  frames=[]
  for i in range(70):
   r.run(5);frames.append(r.frame.copy())
  frames[20].save(P/(name+'.png'));frames[0].save(P/(name+'.gif'),save_all=True,append_images=frames[1:],duration=84,loop=0)
  assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
  results.append(dict(test=name,native_preview_and_return=True,passed=True))
 # Independent instance: libretro state restores are not used in Flash tests.
 r.close();r=new_game()
 # Save/load native Flash, verify coins plus location survive a load.
 warp(r,*MAPS['CeladonCity_GameCorner'],8,10);r.call('SetCoins',347)
 assert r.call('TrySavingData',0,max_frames=1200)==1
 location=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,8)
 r.call('SetCoins',1)
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 loaded_coins=r.call('GetCoins');loaded_location=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,8)
 assert loaded_coins==347 and loaded_location==location
 r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600);r.frame.save(P/'sauvegarde-rechargee.png')
 results.append(dict(test='native_flash_save_load',coins=347,location_preserved=True,passed=True))
 passed=True
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=results),indent=2)+'\n')
print('PASS',P)

#!/usr/bin/env python3
"""Native combat fixtures: prepared parties/enemies; real attacks, capture UI,
encounter consumption after escape, PC rescue and final loss. No injected battle
outcome or injected faint/HP loss. Saves belong to the isolated emulator only.
"""
import ctypes as C, json, os, struct, hashlib, subprocess
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/nuzlocke-20261024'/os.environ.get('NUZ_MODE','public');P.mkdir(parents=True,exist_ok=True)
r=new_game(gender=int(os.environ.get('NUZ_GENDER',0)),nuzlocke=True);rows=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
party=r.symbols['gPlayerParty'];enemy=r.symbols['gEnemyParty']
rev={v|1:k for k,v in r.symbols.items()}
actions={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}

def pulse(k,n=30):r.keys=set();r.run(4);r.keys={k};r.run(4);r.keys=set();r.run(n)
def warp(name,x,y):
 g,n=maps[name];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(300)
def wait(condition,limit=18000,keys=True):
 for f in range(limit):
  if condition():r.keys=set();r.run(2);return
  r.keys={8} if keys and f%20<3 else set();r.run()
 raise AssertionError(('Timeout',rev.get(r.u32(r.symbols['gMain']+4)),[rev.get(r.u32(r.symbols['gTasks']+40*i)) for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\1']))
def action():wait(lambda:r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in actions)
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1

def prepare(playerlevel,enemylevel,pc=False):
 r.call('ZeroPlayerPartyMons');r.call('CreateMon',party,1,playerlevel,31,1,12345,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('NuzlockeRecordOwned',party);r.call('SetMonMoveSlot',party,150,0)
 r.call('ZeroEnemyPartyMons');r.call('CreateMon',enemy,22,enemylevel,31,1,12345,0,0)
 r.call('SetMonMoveSlot',enemy,33,0)
 for move in range(1,4):r.call('SetMonMoveSlot',enemy,0,move)
 if pc:
  r.call('CreateMon',r.symbols['gPlayerParty']+100,7,20,31,1,12345,0,0)
  ptr=r.call('GetBoxedMonPtr',13,29);r.write(ptr,r.read(party+100,80));r.call('ZeroMonData',party+100)
 r.call('StartWildBattle');action()
try:
 r.call('FlagSet',0x829);r.call('SetLastHealLocationWarp',3)
 warp('Route2',10,4);base=r.snapshot();prepare(100,3);first_encounter=r.snapshot()
 # Flee from first real encounter, then test a second encounter's Ball restriction.
 pulse(7);pulse(5);pulse(8,90);wait(field)
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\4'
 r.call('ZeroEnemyPartyMons');r.call('CreateMon',enemy,23,3,31,1,12345,0,0);r.call('StartWildBattle');action()
 assert not r.call('NuzlockeCanCapture',enemy);r.call('ClearBag');r.call('AddBagItem',4,10)
 # Open Bag and select the Poké Ball pocket through controller input.
 pulse(7);pulse(8,180)
 # Bag battle picker initially opens Items. Move to Balls (next pocket).
 pulse(7,180);pulse(7,180);r.frame.save(P/'sac-balls.png');pulse(8,60);pulse(8,260)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_BagMenuRun']|1
 assert r.call('CheckBagHasItem',4,10)
 r.frame.save(P/'capture-refusee.png')
 assert r.call('CheckBagHasItem',4,10), 'Blocked Ball was consumed'
 rows.append('Real first encounter escaped; next encounter refuses capture without consuming a Ball')
 print('PASS',rows[-1],flush=True)
 # Replay the eligible first encounter and actually catch it with a Ball.
 r.restore(first_encounter);assert r.call('GetMonData',enemy,11)==22;r.call('ClearBag');r.call('AddBagItem',1,2)
 pulse(7);pulse(8,180);pulse(7,180);pulse(7,180);pulse(8,60);pulse(8,90)
 for f in range(18000):
  if field():break
  ptr=r.u32(r.symbols['gBattlescriptCurrInstr'])
  nick=ptr!=0 and r.read(ptr,1)==b'\xf3'
  r.keys={0 if nick else 8} if f%20<3 else set();r.run()
 else:raise AssertionError('Native catch never returned to the field')
 r.keys=set();r.run(180)
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\7'
 assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\2'
 assert r.call('GetMonData',party+100,11)==22, [r.call('GetMonData',party+100*i,11) for i in range(6)]
 assert r.call('CheckBagHasItem',1,1) and not r.call('CheckBagHasItem',1,2)
 r.frame.save(P/'capture-reussie.png');rows.append('Eligible first encounter caught through the real Ball UI, added to party and registered')
 print('PASS',rows[-1],flush=True)
 # Return to the pre-battle fixture branch, without injecting a battle result.
 r.restore(base)
 warp('Route1',10,10);prepare(3,100,pc=True)
 pulse(8);pulse(8,90)
 wait(lambda:field() and tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==maps['PewterCity_PokemonCenter_1F'])
 assert r.call('GetMonData',party,11)==7 and r.call('GetMonData',party,57)>0
 wait(lambda:field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0')
 r.keys=set();r.run(60)
 r.frame.save(P/'survivant-pc.png');rows.append('Actual lethal enemy attack: PC survivor is moved to party and player reaches the healing Center')
 print('PASS',rows[-1],flush=True)
 # This time there is no backup anywhere. Enemy Tackle must cause the final death.
 warp('Route3',10,8);lastbase=r.snapshot();prepare(3,100)
 pulse(8);pulse(8,90)
 wait(lambda:r.u32(r.symbols['gMain']+4)==r.symbols['CB2_WaitGameOver']|1)
 r.frame.save(P/'defaite-reelle.png')
 assert not r.read(r.symbols['gPlayerPartyCount'],1)[0]
 r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
 assert C.string_at(r.lib.retro_get_memory_data(0),131072)==b'\xff'*131072
 rows.append('Actual lethal enemy attack with no reserve: Game Over and erased battery')
 print('PASS',rows[-1],flush=True)
 # Also exercise an ordinary trainer callback, which must not heal a lost run.
 r.restore(lastbase);r.call('ZeroPlayerPartyMons');r.call('CreateMon',party,1,3,31,1,12345,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('NuzlockeRecordOwned',party);r.call('SetMonMoveSlot',party,150,0)
 warp('PewterCity_Gym',6,6);r.call('ScriptContext_SetupScript',r.symbols['PewterCity_Gym_EventScript_Brock']);action()
 pulse(8);pulse(8,90)
 wait(lambda:r.u32(r.symbols['gMain']+4)==r.symbols['CB2_WaitGameOver']|1)
 r.frame.save(P/'defaite-dresseur.png');assert not r.read(r.symbols['gPlayerPartyCount'],1)[0]
 rows.append('Actual trainer battle loss reaches Game Over instead of the native healing callback')
 print('PASS',rows[-1],flush=True)
 (P/'COMBATS.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),cases=rows),ensure_ascii=False,indent=2)+'\n')
finally:r.frame.save(P/'dernier-combat.png');r.close()

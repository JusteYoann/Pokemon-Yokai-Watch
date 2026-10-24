#!/usr/bin/env python3
"""mGBA surrender fixtures: native battles and controller confirmation/cancel.
Prepared map/party/last healing point, explicit test branch snapshots.
No injected victory/loss or enemy HP writes; UI triggers the defeat itself.
"""
import os,json,struct,subprocess,hashlib
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/abandon-dresseurs-20261024'/os.environ.get('ABANDON_MODE','prive');P.mkdir(parents=True,exist_ok=True)
r=new_game(int(os.environ.get('ABANDON_GENDER',0)));rows=[]
actions={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
groups=json.load(open(ROOT/'data/maps/map_groups.json'));maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
def pulse(k,n=60):r.keys=set();r.run(4);r.keys={k};r.run(4);r.keys=set();r.run(n)
def loc():return maps_inv.get(tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)),'?')
maps_inv={v:k for k,v in maps.items()}
def warp(name,x,y):
 g,n=maps[name];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(300)
def waitaction(battler=0):
 for f in range(18000):
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']+4*battler) in actions:r.keys=set();r.run(30);return
  r.keys={8} if f%24<3 else set();r.run()
 raise AssertionError('No battle menu')
def prompt(battler=0):
 cur=r.read(r.symbols['gActionSelectionCursor']+battler,1)[0]
 if not cur&1:pulse(7,20)
 if not cur&2:pulse(5,20)
 pulse(8,500)
 assert r.u32(r.symbols['gBattlerControllerFuncs']+4*battler)==r.symbols['HandleConfirmTrainerForfeit']|1
 r.frame.save(P/'confirmation.png')
def end():
 for f in range(18000):
  r.keys={8} if f%20<3 else set();r.run()
  if loc()=='PewterCity_PokemonCenter_1F' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]:r.keys=set();r.run(60);return
 raise AssertionError(('No Center',loc(),hex(r.u32(r.symbols['gMain']+4))))
try:
 for i,sp in enumerate((1,5)):r.call('CreateMon',r.symbols['gPlayerParty']+100*i,sp,30,31,1,12345+i,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\2');r.call('SetLastHealLocationWarp',3)
 warp('PewterCity_Gym',6,6);r.call('ScriptContext_SetupScript',r.symbols['PewterCity_Gym_EventScript_Brock']);waitaction();base=r.snapshot();money=r.call('GetMoney',r.u32(r.symbols['gSaveBlock1Ptr'])+0x290);fee=r.call('ComputeWhiteOutMoneyLoss');party=r.read(r.symbols['gPlayerParty'],200)
 prompt();pulse(8);waitaction();assert r.read(r.symbols['gPlayerParty'],200)==party;assert r.read(r.symbols['gBattleOutcome'],1)==b'\0';rows.append('Default No: no turn/HP/PP spent')
 r.restore(base);prompt();pulse(0);waitaction();assert r.read(r.symbols['gPlayerParty'],200)==party;rows.append('B cancels without a turn')
 r.restore(base);prompt();pulse(4,20);pulse(8,90);end();assert r.read(r.symbols['gBattleOutcome'],1)==b'\2';assert r.call('GetMoney',r.u32(r.symbols['gSaveBlock1Ptr'])+0x290)==money-fee
 for flag in (0x820,0x254,0x4b0,0x500+414):assert not r.call('FlagGet',flag)
 r.frame.save(P/'defaite-centre.png');rows.append('Yes: real loss and native healing center')
 # The local scripted partner must be cleaned without granting the quest win.
 warp('VermilionCity_PhilosovniWarehouse',6,8);r.call('VarSet',0x40f4,1);r.call('PhilosovniStartDuo');waitaction();prompt();pulse(4,20);pulse(8,90);end()
 assert r.call('VarGet',0x40f4)==1;assert r.call('GetMonData',r.symbols['gPlayerParty']+600,11,0)==0
 assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\2';r.frame.save(P/'duo-abandon-centre.png');rows.append('Ariane duo: loss, temporary partner cleared, quest remains pending')
 # Ordinary double: the second human-controlled battler may also forfeit.
 warp('PewterCity_Gym',6,6);r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',745));r.call('StartTrainerBattle');waitaction()
 assert not r.u32(r.symbols['gBattleTypeFlags'])&(1<<23)
 assert r.read(r.symbols['gBattlersCount'],1)==b'\4'
 pulse(8);pulse(8);pulse(8,180);waitaction(2);prompt(2);pulse(4,20);pulse(8,90);end()
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\2';rows.append('Ordinary double: second player battler can forfeit; whole battle lost')
 # Early-rival encounters normally resume their tutorial script even on defeat.
 warp('PalletTown_ProfessorOaksLab',6,4);r.call('ScriptContext_SetupScript',r.symbols['PalletTown_ProfessorOaksLab_EventScript_RivalBattleSquirtle']);waitaction()
 early=r.snapshot();before_party=r.read(r.symbols['gPlayerParty'],200);old_controller=r.u32(r.symbols['gBattlerControllerFuncs'])
 prompt();pulse(8);waitaction();assert r.u32(r.symbols['gBattlerControllerFuncs'])==old_controller;assert r.read(r.symbols['gPlayerParty'],200)==before_party;rows.append('Early rival: No preserves its tutorial controller and party')
 r.restore(early);prompt();pulse(0);waitaction();assert r.u32(r.symbols['gBattlerControllerFuncs'])==old_controller;rows.append('Early rival: B preserves its tutorial controller')
 r.restore(early);prompt();pulse(4,20);pulse(8,90);end()
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\2';rows.append('Early rival tutorial: surrender reaches healing center instead of resuming the cutscene')
 # Wild Flee retains its native escape flow, with no surrender dialogue.
 warp('Route2',10,4);r.call('ZeroEnemyPartyMons');r.call('CreateMon',r.symbols['gEnemyParty'],22,3,31,1,54321,0,0);r.call('StartWildBattle');waitaction()
 pulse(7,20);pulse(5,20);pulse(8,120)
 assert r.u32(r.symbols['gBattlerControllerFuncs'])!=r.symbols['HandleConfirmTrainerForfeit']|1
 for f in range(6000):
  r.keys={8} if f%20<3 else set();r.run()
  if loc()=='Route2' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Wild escape did not finish')
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\4';rows.append('Wild battle still escapes normally, without surrender confirmation')
 print(json.dumps(rows),flush=True);(P/'TEST.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,cases=rows),indent=2)+'\n')
finally:r.frame.save(P/'dernier.png');r.close()

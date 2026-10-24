#!/usr/bin/env python3
"""Native healthbox repaint fixtures: French labels, both sides, all five states."""
import json,hashlib,struct,subprocess
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/traduction-complete-20261024/etats-combat';P.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[]
try:
 for team,species in [('gPlayerParty',1),('gEnemyParty',16)]:
  r.call('CreateMon',r.symbols[team],species,20,31,1,100,0,0)
  r.write(r.symbols[team+'Count'],b'\1')
 r.call('StartWildBattle')
 commands={int(x.split()[0],16)|1 for x in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(x.split())==3 and x.split()[2]=='HandleInputChooseAction'}
 for f in range(6000):
  r.keys={8} if f%16<3 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in commands:break
 else:raise AssertionError('Battle did not reach action menu')
 r.keys=set();r.run(60);r.write(r.symbols['gMain'],(r.symbols['BattleControllerDummy']|1).to_bytes(4,'little'));base=r.snapshot()
 for label,status in [('SOM',1),('GEL',0x20),('BRU',0x10),('PSN',8),('PAR',0x40)]:
  r.restore(base)
  for battler,team in [(0,'gPlayerParty'),(1,'gEnemyParty')]:
   r.write(r.PARAMS+128,struct.pack('<I',status));r.call('SetMonData',r.symbols[team],55,r.PARAMS+128)
   sprite=r.read(r.symbols['gHealthboxSpriteIds']+battler,1)[0];r.call('UpdateStatusIconInHealthbox',sprite)
  r.run(4);r.frame.save(P/(label+'.png'));rows.append(dict(label=label,player_and_enemy_repainted=True))
finally:r.close()
(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256((ROOT/'pokefirered_audio.gba').read_bytes()).hexdigest(),results=rows),indent=2)+'\n')
print('PASS',len(rows))

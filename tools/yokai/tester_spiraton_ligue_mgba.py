#!/usr/bin/env python3
"""Native Don roster battle and actual postgame Champion triggers; not the final boss."""
import hashlib,json,struct,os
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp,strong_party
from pilote_combat_mgba import battle_keys
C['FLAG_SYS_CAN_LINK_WITH_RS']=0x844
Q=ROOT/os.environ.get('YOKAI_SPIRATON_LEAGUE_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON');Q.mkdir(parents=True,exist_ok=True);rows=[]
# MON_DATA_LEVEL is loaded from constants, not assumed offsets into Pokemon.
def roster(r):
 return [(r.call('GetMonData',r.symbols['gEnemyParty']+100*i,C['MON_DATA_SPECIES'],0),r.call('GetMonData',r.symbols['gEnemyParty']+100*i,C['MON_DATA_LEVEL'],0)) for i in range(6)]
passed=False
try:
 r=new_game();strong_party(r)
 r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',743));r.call('StartTrainerBattle')
 for f in range(1200):
  r.keys={0} if f%16<4 else set();r.run()
  if f>500 and r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
 assert roster(r)==[(147,56),(70,57),(140,56),(136,58),(115,57),(86,60)]
 assert r.call('GetBattleBGM')==349
 r.frame.save(Q/'don-premier-combat.png')
 rows.append(dict(test='Native independent Don League roster and Ghoulfather selection',passed=True))
 r.close()
 for starter,trainer in [(0,C['TRAINER_CHAMPION_REMATCH_CHARMANDER']),(1,C['TRAINER_CHAMPION_REMATCH_BULBASAUR']),(2,C['TRAINER_CHAMPION_REMATCH_SQUIRTLE'])]:
  r=new_game();strong_party(r);r.call('FlagSet',C['FLAG_SYS_GAME_CLEAR']);r.call('FlagClear',C['FLAG_SYS_CAN_LINK_WITH_RS']);r.call('VarSet',C['VAR_STARTER_MON'],starter)
  warp(r,*MAPS['PokemonLeague_ChampionsRoom'],6,18)
  for f in range(5000):
   r.keys=battle_keys(r,f);r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
  else:raise AssertionError('Postgame room never started battle')
  assert int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')==trainer
  actual=roster(r);assert [lv for sp,lv in actual]==[68,69,70,70,71,73]
  assert r.call('GetBattleBGM')==C['MUS_YOKAI_DECISIVE_BATTLE']
  r.keys=set();r.run(600);r.frame.save(Q/f'matt-revanche-{starter}.png')
  rows.append(dict(test='Real postgame Champion trigger, no RS-link flag',starter=starter,trainer=trainer,roster=actual,passed=True));r.close()
 # Native map loading confirms the cameo was removed while staff remain.
 r=new_game();r.call('FlagSet',C['FLAG_SYS_GAME_CLEAR']);warp(r,*MAPS['FiveIsland_RocketWarehouse'],27,24)
 mapdata=json.loads((ROOT/'data/maps/FiveIsland_RocketWarehouse/map.json').read_text())
 actors=mapdata['object_events'];assert not any(x.get('script')=='YokaiCameo_DonMorleone' for x in actors)
 assert sum(x.get('script','').startswith('YokaiCameo_Mafiamille') for x in actors)==3
 r.frame.save(Q/'sevii-sans-don.png');rows.append(dict(test='Warehouse loads, Don retired, three Mafia cameos retained',passed=True));passed=True
finally:
 try:r.close()
 except Exception:pass
 (Q/'LIGUE_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),indent=2)+'\n')
print('PASS: Don roster and postgame variants; final Spiraton encounter not tested')

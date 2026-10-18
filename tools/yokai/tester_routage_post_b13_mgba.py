#!/usr/bin/env python3
"""Native selector checks for approved battle roles, preserving mandatory specials."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
r=Emulator();checks=[];C={}
for f in ['songs','opponents']:
 C.update({k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)\s*(?:$|//)',(ROOT/f'include/constants/{f}.h').read_text(),re.M)})
try:
 r.w32(r.symbols['gBattleTypeFlags'],8)
 for name,trainer in C.items():
  if trainer<300:continue
  if name.startswith('TRAINER_ELITE_FOUR_'):expected=C['MUS_YOKAI_DECISIVE_BATTLE']
  elif name.startswith('TRAINER_CHAMPION_'):expected=C['MUS_YOKAI_FINAL_BATTLE']
  elif name.startswith('TRAINER_RIVAL_'):expected=C['MUS_YOKAI_VS_YOKAI']
  elif name.startswith('TRAINER_LEADER_'):expected=C['MUS_YOKAI_BOSS_YOKAI']
  else:continue
  r.write(r.symbols['gTrainerBattleOpponent_A'],trainer.to_bytes(2,'little'));actual=r.call('GetBattleBGM');assert actual==expected,(name,actual,expected);checks.append(dict(trainer=name,trainer_id=trainer,music_id=actual,passed=True))
 for trainer,slot in [(3,6),(14,2),(17,3),(15,28),(16,28),(18,28),(19,28),(20,28)]:
  r.write(r.symbols['gTrainerBattleOpponent_A'],trainer.to_bytes(2,'little'));actual=r.call('GetBattleBGM');assert actual==346+slot;(checks.append(dict(trainer_id=trainer,music_id=actual,passed=True)))
 r.w32(r.symbols['gBattleTypeFlags'],0);assert r.call('GetBattleBGM')==C['MUS_YOKAI_VS_YOKAI'];checks.append(dict(test='Wild selector',music_id=C['MUS_YOKAI_VS_YOKAI'],passed=True))
 report={'passed':True,'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':'Actual compiled GetBattleBGM with explicit opponent fixtures; not every battle played. Champion stays dedicated25 (pending sample); E4/rematches15, Hinozall2, Ghoulfather3 and Enma6 preserved','results':checks};(ROOT/'QA_RECETTE_FINALE/POST_B13/audio/ROUTAGE_COMBATS_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(checks))
finally:r.close()

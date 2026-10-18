#!/usr/bin/env python3
"""Native music selection for approved bosses, E4/rematches, rival and gyms.

Read/write fixture trainer ID and flags, call actual GetBattleBGM. No team edits.
Actual optional/E4 battle playback is tested separately.
"""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
r=Emulator();results=[]
constants={}
for f in ['songs','opponents']:
 constants.update({k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)\s*(?:$|//)',(ROOT/f'include/constants/{f}.h').read_text(),re.M)})
try:
 r.w32(r.symbols['gBattleTypeFlags'],8)
 for name,trainer in constants.items():
  if trainer<300:continue # Hoenn-only unused role constants are not Kanto battles
  if name.startswith('TRAINER_ELITE_FOUR_'):expected=constants['MUS_YOKAI_DECISIVE_BATTLE']
  elif name.startswith('TRAINER_CHAMPION_'):expected=constants['MUS_YOKAI_FINAL_BATTLE']
  elif name.startswith('TRAINER_RIVAL_'):expected=constants['MUS_VS_TRAINER']
  elif name.startswith('TRAINER_LEADER_'):expected=constants['MUS_VS_GYM_LEADER']
  else:continue
  r.write(r.symbols['gTrainerBattleOpponent_A'],trainer.to_bytes(2,'little'));actual=r.call('GetBattleBGM');assert actual==expected,(name,actual,expected)
  results.append({'trainer':name,'trainer_id':trainer,'music_id':actual,'passed':True})
 for trainer,number in [(3,6),(14,2),(17,3),(15,None),(16,None),(18,None),(19,None),(20,None)]:
  r.write(r.symbols['gTrainerBattleOpponent_A'],trainer.to_bytes(2,'little'));actual=r.call('GetBattleBGM');assert actual==(346+number if number else constants['MUS_VS_TRAINER'])
  results.append({'trainer_id':trainer,'selected_yokai_track':number,'music_id':actual,'passed':True})
 report={'passed':True,'rom_sha256':hashlib.sha256((r.elf_path.with_suffix('.gba')).read_bytes()).hexdigest(),'scope':'Native selection only, not every battle played. Actual original Lorelei and cameo battles tested separately. Selected V1 boss/Champion routes; a route alone does not prove private sample integration.','results':results}
 (ROOT/'QA_RECETTE_FINALE/INTEGRATION_MUSIQUES/ROUTAGE_COMBATS_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'routes_checked':len(results)}))
finally:r.close()

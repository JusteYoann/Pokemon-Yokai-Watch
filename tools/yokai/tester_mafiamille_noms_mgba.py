#!/usr/bin/env python3
"""Native battle text expansion for ordinary and postgame Mafia; no economics class edits."""
import hashlib,json,re
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C
r=new_game();rows=[]
try:
 glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
 prefix=bytes(glyph[c] for c in 'SBIRE MAFIAMILLE');dest=r.call('AllocZeroed',1024)
 for key in ['TRAINER_TEAM_ROCKET_GRUNT','TRAINER_TEAM_ROCKET_GRUNT_42','TRAINER_TEAM_ROCKET_ADMIN','TRAINER_GUITARIST','TRAINER_KINDLER','TRAINER_RS_CAMPER']:
  trainer=C[key];r.w32(r.symbols['gBattleTypeFlags'],8);r.write(r.symbols['gTrainerBattleOpponent_A'],trainer.to_bytes(2,'little'))
  r.call('BattleStringExpandPlaceholders',r.symbols['sText_Trainer1WantsToBattle'],dest)
  assert r.read(dest,len(prefix))==prefix,key
  if key in ['TRAINER_GUITARIST','TRAINER_KINDLER','TRAINER_RS_CAMPER']:assert r.read(r.symbols['gTrainers']+40*trainer+1,1)[0]==C['TRAINER_CLASS_COOLTRAINER']
  rows.append(dict(trainer=key,native_prefix='SBIRE MAFIAMILLE',passed=True))
finally:r.close()
(ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/NOMS_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=rows),indent=2)+'\n');print('NAMES PASS6')

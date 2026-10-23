#!/usr/bin/env python3
"""Native party-generation fixture, used to compare unchanged teams and variants."""
import os,json,hashlib
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C
r=new_game();rows={}
try:
 for gender in [0,1]:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
  r.w32(r.symbols['gBattleTypeFlags'],8)
  for trainer in ['TRAINER_LEADER_BROCK','TRAINER_LEADER_SABRINA','TRAINER_LEADER_KOGA','TRAINER_LEADER_GIOVANNI','TRAINER_LEADER_MISTY','TRAINER_LEADER_BLAINE']:
   count=r.call('CreateNPCTrainerParty',r.symbols['gEnemyParty'],C[trainer]);team=[]
   for i in range(count):
    mon=r.symbols['gEnemyParty']+100*i
    fields=['SPECIES','LEVEL','PERSONALITY','HP','MAX_HP','ATK','DEF','SPEED','SPATK','SPDEF','HELD_ITEM','MOVE1','MOVE2','MOVE3','MOVE4','PP1','PP2','PP3','PP4','ABILITY_NUM']
    team.append({f:r.call('GetMonData',mon,C['MON_DATA_'+f],0) for f in fields})
   rows[f'{gender}:{trainer}']=team
finally:r.close()
rom=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba'))
out=Path(os.environ['YOKAI_PARTY_REPORT']);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(dict(rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),fixture=__doc__,teams=rows),indent=2)+'\n')
print('Captured native generated teams',out)

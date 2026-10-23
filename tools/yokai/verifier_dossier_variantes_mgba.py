#!/usr/bin/env python3
"""Compare native generated Gym parties and both sex variants to the retained base capture."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'docs/dossier-20261023';base=json.loads((D/'equipes-generees-base.json').read_text())['teams'];rows=[]
for mode in ['public','prive']:
 new=json.loads((D/f'tests/{mode}/equipes-generees.json').read_text())['teams']
 for gender in [0,1]:
  for key in ['BROCK','MISTY','LT_SURGE','ERIKA','BLAINE','GIOVANNI']:
   name=f'{gender}:TRAINER_LEADER_{key}';assert new[name]==base[name],(mode,name);rows.append({'mode':mode,'gender':gender,'trainer':key,'native_party_identical':True})
  assert new[f'{gender}:TRAINER_LEADER_KOGA']==base[f'{gender}:TRAINER_LEADER_SABRINA'];rows.append({'mode':mode,'gender':gender,'trainer':'BERENICE_MOVED_TO_KOGA','native_party_identical':True})
(D/'VARIANTES_PRESERVEES.json').write_text(json.dumps({'passed':True,'checks':rows},indent=2)+'\n');print('PASS native parties and both gender variants',len(rows))

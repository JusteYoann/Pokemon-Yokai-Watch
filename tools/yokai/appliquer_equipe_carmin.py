#!/usr/bin/env python3
"""Apply only Ariane's third-trophy profile, preserving historical arrays."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def apply_profile():
 profile=json.loads((ROOT/'data/yokai/scenario_carmin.json').read_text())['active_trainer'];symbol=profile['source_party'];key='TRAINER_LEADER_LT_SURGE'
 body='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n'
 for m in profile['party']:body+='    {.iv = '+str(m['iv'])+', .lvl = '+str(m['level'])+', .species = '+m['species']+', .heldItem = '+m['held_item']+', .moves = {'+', '.join(m['moves'])+'}},\n'
 body+='};'
 p=ROOT/'src/data/trainer_parties.h';s=p.read_text();pat=r'static const struct TrainerMonItemCustomMoves '+symbol+r'\[\] = \{.*?\};';s=re.sub(pat,lambda _:body,s,flags=re.S) if symbol+'[]' in s else s+'\n'+body+'\n';p.write_text(s)
 p=ROOT/'src/data/trainers.h';s=p.read_text();pat=r'(    \['+key+r'\] = \{)(.*?)(\n    \},)'
 def replace(m):
  t=m[2];t=re.sub(r'\.trainerPic = \w+','.trainerPic = TRAINER_PIC_ARIANE',t);t=re.sub(r'\.trainerName = _\("[^"]*"\)','.trainerName = _("Ariane")',t);t=re.sub(r'\.encounterMusic_gender = [^,]+','.encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_FEMALE | F_TRAINER_FEMALE',t);t=re.sub(r'\.items = \{[^}]*\}','.items = {}',t);t=re.sub(r'\.party = [^\n]+','.party = ITEM_CUSTOM_MOVES('+symbol+'),',t);return m[1]+t+m[3]
 s,n=re.subn(pat,replace,s,flags=re.S);assert n==1;p.write_text(s)
 p=ROOT/'src/data/yokai_trainer_abilities.h';s=p.read_text();s,n=re.subn(r'\['+key+r'\] = \{[^}]*\}',lambda _:'['+key+'] = {'+', '.join(str(m['ability_num']) for m in profile['party'])+'}',s);assert n==1;p.write_text(s)
 p=ROOT/'data/yokai/equipes_appliquees.json';d=json.loads(p.read_text());d[key]=profile;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':apply_profile()

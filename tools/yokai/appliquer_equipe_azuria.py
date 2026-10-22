#!/usr/bin/env python3
"""Apply second-trophy profiles after deliberate historical team regeneration.

Preserves historical boss/cameo party arrays and their locked specification.
"""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]

def apply_profile():
    profile=json.loads((R/'data/yokai/scenario_azuria.json').read_text())['active_trainer'];symbol=profile['source_party']
    body='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n'
    for m in profile['party']:body+='    {.iv = '+str(m['iv'])+', .lvl = '+str(m['level'])+', .species = '+m['species']+', .heldItem = '+m['held_item']+', .moves = {'+', '.join(m['moves'])+'}},\n'
    body+='};'
    p=R/'src/data/trainer_parties.h';s=p.read_text();pat=r'static const struct TrainerMonItemCustomMoves '+symbol+r'\[\] = \{.*?\};';s=re.sub(pat,lambda _:body,s,flags=re.S) if symbol+'[]' in s else s+'\n'+body+'\n';p.write_text(s)
    for key,name,pic,gender in [('TRAINER_LEADER_MISTY','Katie','LEAF','FEMALE | F_TRAINER_FEMALE'),('TRAINER_BUG_MANIAC','Nathan','RED','MALE')]:
     p=R/'src/data/trainers.h';s=p.read_text();a=s.index('    ['+key+'] = {');b=s.index('\n    },',a)+7
     block='    ['+key+'] = {\n        .trainerClass = TRAINER_CLASS_LEADER,\n        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_'+gender+',\n        .trainerPic = TRAINER_PIC_'+pic+',\n        .trainerName = _("'+name+'"),\n        .items = {'+', '.join(profile['items'])+'}, .doubleBattle = FALSE,\n        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES('+symbol+'),\n    },';p.write_text(s[:a]+block+s[b:])
     p=R/'src/data/yokai_trainer_abilities.h';s=p.read_text();pat=r'\['+key+r'\] = \{[^}]+\}';new='['+key+'] = {'+', '.join(str(m['ability_num']) for m in profile['party'])+'}'
     if re.search(pat,s):s=re.sub(pat,new,s)
     else:s=s.replace('sYokaiTrainerAbilitySlots[NUM_TRAINERS][PARTY_SIZE] = {','sYokaiTrainerAbilitySlots[NUM_TRAINERS][PARTY_SIZE] = {\n    '+new+',')
     p.write_text(s)
    p=R/'data/yokai/equipes_appliquees.json';d=json.loads(p.read_text());d['TRAINER_LEADER_MISTY']=profile;d['TRAINER_BUG_MANIAC']=profile;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print('Applied active Azuria leaders; historical sources retained')

if __name__=='__main__':
    apply_profile()

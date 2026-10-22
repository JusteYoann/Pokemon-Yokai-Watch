#!/usr/bin/env python3
"""Apply the explicitly versioned third-champion migration to active trainer data.

Historical locked boss JSON and party arrays remain available for comparison.
Reapply this after any deliberate use of the historical full-party generator.
"""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
profile=json.loads((R/'data/yokai/scenario_carmin.json').read_text())['active_trainer'];symbol=profile['source_party']
body='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n'
for m in profile['party']:
 body+='    {.iv = '+str(m['iv'])+', .lvl = '+str(m['level'])+', .species = '+m['species']+', .heldItem = '+m['held_item']+', .moves = {'+', '.join(m['moves'])+'}},\n'
body+='};'
p=R/'src/data/trainer_parties.h';s=p.read_text();pat=r'static const struct TrainerMonItemCustomMoves '+symbol+r'\[\] = \{.*?\};'
s=re.sub(pat,lambda _:body,s,flags=re.S) if symbol+'[]' in s else s+'\n'+body+'\n';p.write_text(s)
p=R/'src/data/trainers.h';s=p.read_text();a=s.index('    [TRAINER_LEADER_LT_SURGE] = {');b=s.index('\n    },',a)+7;block=s[a:b]
block=re.sub(r'\.trainerPic = \w+', '.trainerPic = TRAINER_PIC_SCENARIO_BERENICE',block)
block=re.sub(r'\.encounterMusic_gender = [^,]+', '.encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_FEMALE | F_TRAINER_FEMALE',block)
block=re.sub(r'\.trainerName = _\("[^"]*"\)', '.trainerName = _("Bérénice")',block)
block=re.sub(r'\.items = \{[^}]*\}', '.items = {'+', '.join(profile['items'])+'}',block)
block=re.sub(r'\.party = \w+\(\w+\)', '.party = ITEM_CUSTOM_MOVES('+symbol+')',block);p.write_text(s[:a]+block+s[b:])
p=R/'src/data/yokai_trainer_abilities.h';s=p.read_text();s=re.sub(r'\[TRAINER_LEADER_LT_SURGE\] = \{[^}]+\}', '[TRAINER_LEADER_LT_SURGE] = {'+', '.join(str(m['ability_num']) for m in profile['party'])+'}',s);p.write_text(s)
p=R/'data/yokai/equipes_appliquees.json';d=json.loads(p.read_text());d['TRAINER_LEADER_LT_SURGE']=profile;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Applied active Berenice team; historical boss source retained')

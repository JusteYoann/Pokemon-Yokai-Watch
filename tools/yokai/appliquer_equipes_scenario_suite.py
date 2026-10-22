#!/usr/bin/env python3
"""Apply explicitly versioned late-story teams, retaining all historical arrays/IDs."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
profiles=sorted((R/'data/yokai').glob('scenario_suite_equipes*.json'))
for path in profiles:
 for trainer,p in json.loads(path.read_text()).items():
  symbol=p['source_party'];body='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n'
  for m in p['party']:body+='    {.iv = '+str(m['iv'])+', .lvl = '+str(m['level'])+', .species = '+m['species']+', .heldItem = '+m['held_item']+', .moves = {'+', '.join(m['moves'])+'}},\n'
  body+='};';file=R/'src/data/trainer_parties.h';s=file.read_text();pat=r'static const struct TrainerMonItemCustomMoves '+symbol+r'\[\] = \{.*?\};';s=re.sub(pat,lambda _:body,s,flags=re.S) if symbol+'[]' in s else s+'\n'+body+'\n';file.write_text(s)
  file=R/'src/data/trainers.h';s=file.read_text();block=f'''    [{trainer}] = {{
        .trainerClass = {p['trainer_class']},
        .encounterMusic_gender = {p['gender_music']},
        .trainerPic = {p['portrait']},
        .trainerName = _("{p['name']}"),
        .items = {{{', '.join(p['items'])}}},
        .doubleBattle = {'TRUE' if p.get('double') else 'FALSE'},
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = ITEM_CUSTOM_MOVES({symbol}),
    }},'''
  if f'[{trainer}] = {{' in s:
   a=s.index(f'    [{trainer}] = {{');b=s.index('\n    },',a)+7;s=s[:a]+block+s[b:]
  else:s=s.rstrip()[:-2]+block+'\n};\n'
  file.write_text(s)
  file=R/'src/data/yokai_trainer_abilities.h';s=file.read_text();entry=f'    [{trainer}] = {{'+', '.join(str(m['ability_num']) for m in p['party'])+'},'
  pat=r'    \['+trainer+r'\] = \{[^}]+\},'
  s=re.sub(pat,lambda _:entry,s) if f'[{trainer}]' in s else s.rstrip()[:-2]+entry+'\n};\n';file.write_text(s)
  file=R/'data/yokai/equipes_appliquees.json';d=json.loads(file.read_text());d[trainer]=p;file.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Applied late-story profiles; original teams and previous trainer IDs retained')

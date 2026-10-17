#!/usr/bin/env python3
"""Link curated Yo-kai move tables and French labels into active engine sources."""
import csv
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

R=Path(__file__).resolve().parents[2]
D=R/'data/yokai'
BASE='037335f4c725d7c9aecdac87066f2002b4bd7e14'


def original(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=R,text=True)


def rows(name):return list(csv.DictReader((D/name).open(encoding='utf-8-sig'),delimiter=';'))


tables=defaultdict(list);delayed={}
for row in rows('attaques_validees.csv'):
    n=int(row['numero_yokai'])
    if row['apprentissage']=='EVOLUTION_PLUS_2':delayed[n]=row['move_id']
    else:tables[n].append((int(row['niveau']),row['move_id'],row['species_constant']))
assert len(tables)==151 and set(delayed)=={4,14,19,44}
text=original('src/data/pokemon/level_up_learnsets.h')+'\n// Reconstructed Yo-kai move tables. Level 0 means evolution only.\n'
pointers=original('src/data/pokemon/level_up_learnset_pointers.h')
delay_text=['// Level +2 moves tracked using the reserved BoxPokemon separator word.',
            'static const u16 sYokaiDelayedEvolutionMoves[NUM_SPECIES] = {']
for n,entries in sorted(tables.items()):
    assert 8<=len(entries)<=19,(n,len(entries))
    text+=f'static const u16 sYokai{n:03}LevelUpLearnset[] = {{\n'
    for level,move,constant in entries:text+=f'    LEVEL_UP_MOVE({level}, {move}),\n'
    if n in delayed:
        text+=f'    LEVEL_UP_MOVE(101, {delayed[n]}), // Reminder uses saved evolution level.\n'
        delay_text.append(f'    [{entries[0][2]}] = {delayed[n]},')
    text+='    LEVEL_UP_END\n};\n'
    constant=entries[0][2]
    pointers,count=re.subn(r'(\['+constant+r'\]\s*=\s*)\w+(,)',lambda m:m[1]+f'sYokai{n:03}LevelUpLearnset'+m[2],pointers)
    assert count==1,constant
(R/'src/data/pokemon/level_up_learnsets.h').write_text(text)
(R/'src/data/pokemon/level_up_learnset_pointers.h').write_text(pointers)
(R/'src/data/pokemon/yokai_delayed_moves.h').write_text('\n'.join(delay_text+['};\n']))
labels=[]
for dataset,path in [('move_names_fr.csv','src/data/text/move_names.h'),('ability_names_fr.csv','src/data/text/abilities.h')]:
    text=original(path)
    for row in rows(dataset):
        constant=row['constant'];name=row['nom_fr'];short=name if len(name)<=12 else name[:11].rstrip()+'.'
        text,count=re.subn(r'(\['+constant+r'\]\s*=\s*_)\("[^"]*"\)',lambda m:m[1]+'("'+short.replace('"','')+'")',text)
        assert count==1,constant
        labels.append({**row,'display':short})
    (R/path).write_text(text)
(D/'libelles_attaques_talents.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2)+'\n')
print('151 learnsets + evolution moves linked; French move/ability names restored.')

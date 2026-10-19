#!/usr/bin/env python3
"""Translate only complete, explicitly reviewed visible literals. No identifiers."""
import re,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];table=R/'data/localisation/fr/libelles_communs.tsv'
pairs=dict(line.split('\t',1) for line in table.read_text().splitlines() if line and not line.startswith('#'));rows=[]
# No JSON, generated items.h, identifiers, technical strings or generic C literals.
for path in list((R/'src').rglob('*.c'))+list((R/'src').rglob('*.h'))+list((R/'data').rglob('*.inc')):
 if path.name in ['items.h','trainers.h','species_names.h'] or 'easy_chat' in path.parts:continue
 text=path.read_text();before=text
 def sub(m):
  old=m[2]
  if old not in pairs:return m[0]
  new=pairs[old]
  if new==old:return m[0]
  rows.append(dict(file=str(path.relative_to(R)),english=old,french=new));return m[1]+new+m[3]
 pattern=r'(_\(")((?:\\.|[^"\\])*)("\))' if path.suffix in ['.c','.h'] else r'(\.string ")((?:\\.|[^"\\])*)(")'
 text=re.sub(pattern,sub,text)
 if text!=before:path.write_text(text)
p=R/'QA_RECETTE_FINALE/LOCALISATION_FR/LIBELLES_COMMUNS.json';p.write_text(json.dumps({'changed_literals':len(rows),'results':rows},ensure_ascii=False,indent=2)+'\n');print(len(rows),'visible literals translated')

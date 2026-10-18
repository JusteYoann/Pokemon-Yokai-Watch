#!/usr/bin/env python3
"""Explicit display-literal migration; identifiers, engine tokens and scripts stay intact.

Default is a dry run. --apply changes only .string operands and _()/__() literals
in approved game-text source roots. This is vocabulary work, not full translation.
"""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DISPLAY=re.compile(r'(?P<prefix>\.string\s+|_{1,2}\()"(?P<text>(?:[^"\\]|\\.)*)"')
RULES=[(r'\bPOK[eé]MON\s+CENTER\b','Centre Yo-kai'),(r'\bCENTRE\s+POK[eé]MON\b','Centre Yo-kai'),(r'\bPOK[eé]MON\s+LEAGUE\b','Ligue Yo-kai'),(r'\bLIGUE\s+POK[eé]MON\b','Ligue Yo-kai'),(r'\bPOK[eé]MON\s+TRAINER\b','Dresseur de Yo-kai'),(r'\bDRESSEUR\s+POK[eé]MON\b','Dresseur de Yo-kai'),(r'\bPOK[eé]DEX\b','Médallium'),(r'\bPOK[eé]\s?BALLS\b','Yo-kai Balls'),(r'\bPOK[eé]\s?BALL\b','Yo-kai Ball'),(r'\bPOK[eé]MONS?\b','Yo-kai')]
COMPILED=[(re.compile(pattern,re.I),replacement) for pattern,replacement in RULES]
def adapt(text):
 # Never rewrite control/placeholder names, even if they contain a target noun.
 parts=re.split(r'(\{[^}]*\}|\\.)',text)
 for i,p in enumerate(parts):
  if p.startswith(('{',chr(92))):continue
  for pattern,replacement in COMPILED:p=pattern.sub(lambda m:replacement,p)
  parts[i]=p
 return ''.join(parts)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');a=parser.parse_args();rows=[]
 paths=sorted(set([*ROOT.glob('data/maps/**/*.inc'),*ROOT.glob('data/text/**/*.inc'),*ROOT.glob('data/scripts/**/*.inc'),*ROOT.glob('src/**/*.c'),*ROOT.glob('src/data/**/*.h')]))
 for p in paths:
  if str(p.relative_to(ROOT)) in ['src/data/items.h','src/data/region_map/region_map_entry_strings.h']:continue # Generated from source JSON.
  old=p.read_text();edits=[]
  def replace(m):
   before=m['text'];after=adapt(before)
   if after==before:return m[0]
   # Every backslash escape and ordered control token must remain unchanged.
   assert re.findall(r'\\.|\{[^}]*\}',before)==re.findall(r'\\.|\{[^}]*\}',after),(p,before)
   edits.append(dict(before=before,after=after));return m['prefix']+'"'+after+'"'
  new=DISPLAY.sub(replace,old)
  if edits:
   rows.append(dict(file=str(p.relative_to(ROOT)),literals=len(edits),edits=edits))
   if a.apply:p.write_text(new)
 for relative,fields in [('src/data/items.json',{'english','description_english'}),('src/data/region_map/region_map_sections.json',{'display_name'})]:
  p=ROOT/relative;obj=json.loads(p.read_text());edits=[]
  def visit(value):
   if isinstance(value,dict):
    for key,item in list(value.items()):
     if key in fields and isinstance(item,str):
      after=adapt(item)
      if after!=item:edits.append(dict(before=item,after=after));value[key]=after
     else:visit(item)
   elif isinstance(value,list):
    for item in value:visit(item)
  visit(obj)
  if edits:
   rows.append(dict(file=relative,literals=len(edits),edits=edits))
   if a.apply:p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 report=dict(applied=a.apply,scope='Display literals only; full French translation and all-window validation still pending; no identifier/placeholder/escape/script command changes',files=len(rows),literals=sum(r['literals'] for r in rows),changes=rows)
 if a.apply:(ROOT/'QA_RECETTE_FINALE/VERSION_1_DEVELOPPEMENT/HARMONISATION_VOCABULAIRE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='changes'},ensure_ascii=False))
if __name__=='__main__':main()

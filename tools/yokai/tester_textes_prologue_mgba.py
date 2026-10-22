#!/usr/bin/env python3
"""Native normal-font widths for all lab messages, intro speech and eight-trophy warning.

Conservative dynamic placeholders: seven W player name, Matt, fourteen W string vars.
No claim of visual review of every page or full-game French coverage.
"""
import hashlib,json,os,re
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game
OUT=ROOT/'QA_RECETTE_FINALE/RAPPROCHEMENT_2026_10_22/prologue';OUT.mkdir(parents=True,exist_ok=True)
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
rows=[];r=new_game()
try:
 for path in ['data/text/new_game_intro.inc','data/maps/PalletTown_ProfessorOaksLab/text.inc','data/maps/IndigoPlateau_PokemonCenter_1F/text.inc']:
  source=(ROOT/path).read_text()
  for label,body in re.findall(r'^(\w+)::\n((?:    \.string .*\n)+)',source,re.M):
   if 'new_game_intro' in path and not label.startswith('gOakSpeech_'):continue
   if 'IndigoPlateau' in path and label!='IndigoPlateau_Text_EightTrophiesRequired':continue
   for part in re.findall(r'\.string "(.*)"',body):
    part=part.replace('{PLAYER}','W'*7).replace('{RIVAL}','Matt')
    part=re.sub(r'\{STR_VAR_\d\}',lambda m:'W'*14,part)
    assert not re.search(r'\{[^}]+\}',part),(label,part)
    for line in re.split(r'\\[nlp]',part.rstrip('$')):
     if not line:continue
     raw=bytes(glyph[c] for c in line)+b'\xff';assert len(raw)<128
     r.write(r.PARAMS+128,raw);width=r.call('GetStringWidth',2,r.PARAMS+128,0)
     rows.append(dict(file=path,label=label,text=line,pixels=width,passed=width<=208))
finally:r.close()
report=dict(passed=all(x['passed'] for x in rows),rom_sha256=hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba')).read_bytes()).hexdigest(),scope=__doc__,lines=len(rows),max_pixels=208,results=rows)
(OUT/'LARGEURS_LABO_INTRO_ACCES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for row in rows:
 if not row['passed']:print(row,flush=True)
assert report['passed']
print('NATIVE TEXT WIDTHS PASS',len(rows),flush=True)

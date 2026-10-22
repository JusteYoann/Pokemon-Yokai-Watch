#!/usr/bin/env python3
"""Native normal-font width checks for the Wyatt lot; conservative seven-W player name."""
import hashlib,json,os,re
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
Q=ROOT/'QA_RECETTE_FINALE/SCENARIO_2026_10_22/wyatt'
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
samples=[]
for path in ['data/maps/PewterCity_Gym/text.inc','data/maps/PewterCity/text.inc','data/maps/MtMoon_1F/text.inc','data/text/fame_checker.inc']:
 for m in re.finditer(r'(\w+)::[^\n]*\n((?:[ \t]*\.string [^\n]*\n)+)',(ROOT/path).read_text()):
  if path.endswith('PewterCity_Gym/text.inc') or 'Brock' in m[1]:
   for part in re.findall(r'\.string "(.*)"',m[2]):
    part=part.replace('{PLAYER}','WWWWWWW').replace('{RIVAL}','Matt')
    part=re.sub(r'\{[^}]+\}','',part).replace('$','')
    for line in re.split(r'\\[npl]',part):
     if line:samples.append((path,m[1],line))
r=new_game();rows=[]
try:
 for path,symbol,line in samples:
  raw=bytes(glyph[c] for c in line)+b'\xff'
  assert len(raw)<128
  r.write(r.PARAMS+128,raw);width=r.call('GetStringWidth',2,r.PARAMS+128,0)
  rows.append(dict(file=path,symbol=symbol,text=line,pixels=width,passed=width<=208))
finally:r.close()
report=dict(passed=all(x['passed'] for x in rows),rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),scope=__doc__,max_pixels=208,results=rows)
(Q/'TEXTES_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for row in rows:
 if not row['passed']:print(row,flush=True)
assert report['passed']
print('TEXT WIDTH PASS',len(rows),flush=True)

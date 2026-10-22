#!/usr/bin/env python3
"""Validate actual native font widths, including worst-case player name."""
import hashlib,json,os
from pathlib import Path
import re
from mgba_rpc import ROOT,Emulator
out=ROOT/'QA_RECETTE_FINALE/AZURIA_REPRISE_2026_10_22';out.mkdir(exist_ok=True)
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyphs["'"]=glyphs['’']
r=Emulator();rows=[]
try:
 for path in ['data/maps/CeruleanCity_Gym/text.inc','data/maps/CeruleanCity/text.inc','data/text/fame_checker.inc']:
  text=(ROOT/path).read_text()
  if path.endswith('CeruleanCity/text.inc'):text=text[text.index('CeruleanCity_Text_GymSign::'):].split('\n\n',1)[0]
  if path.endswith('fame_checker.inc'):
   text='\n'.join(body for label,body in re.findall(r'^(\w+)::[^\n]*\n((?:\t.string .*\n)+)',text,re.M) if 'Misty' in label)
  for piece in re.findall(r'\.string "(.*)"',text):
   piece=piece.replace('{PLAYER}','WWWWWWW').replace('{RIVAL}','Matt').replace('{STR_VAR_1}','Nathan')
   piece=re.sub(r'\{[^}]+\}','',piece)
   for line in re.split(r'\\[nlp]',piece):
    line=line.rstrip('$')
    if not line:continue
    r.write(r.PARAMS+128,bytes(glyphs[c] for c in line)+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0)
    assert width<=208,(path,line,width)
    rows.append({'text':line,'pixels':width})
finally:r.close()
(out/'LARGEURS_DIALOGUES.json').write_text(json.dumps({'passed':True,'maximum_pixels':208,'lines':len(rows),'rom_sha256':hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba')).read_bytes()).hexdigest(),'results':rows},ensure_ascii=False,indent=2)+'\n');print('PASS',len(rows),'native text widths')

#!/usr/bin/env python3
"""Measure the chapter's actual dialogue using the ROM's normal font."""
import hashlib,json,re
from mgba_rpc import ROOT,Emulator
out=ROOT/'QA_RECETTE_FINALE/ARGENTA_SCENARIO_2026'
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyphs["'"]=glyphs['’']
r=Emulator();rows=[]
try:
 for path in ['data/maps/PewterCity/text.inc','data/maps/PewterCity_Gym/text.inc']:
  text=(ROOT/path).read_text()
  if path.endswith('PewterCity/text.inc'):text=text[text.index('PewterCity_Text_SpeechWitness::'):]
  for piece in re.findall(r'\.string "(.*)"',text):
   piece=piece.replace('{PLAYER}','WWWWWWW').replace('{RIVAL}','Matt')
   piece=re.sub(r'\{[^}]+\}','',piece)
   for line in re.split(r'\\[nlp]',piece):
    line=line.rstrip('$')
    if not line:continue
    r.write(r.PARAMS+128,bytes(glyphs[c] for c in line)+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0)
    assert width<=208,(path,line,width)
    rows.append({'text':line,'pixels':width,'file':path})
finally:r.close()
(out/'LARGEURS_DIALOGUES.json').write_text(json.dumps({'passed':True,'lines':len(rows),'maximum_pixels':208,'player_name_case':'7 W characters','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'results':rows},ensure_ascii=False,indent=2)+'\n');print('PASS',len(rows),'native dialogue widths')

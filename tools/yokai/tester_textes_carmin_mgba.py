#!/usr/bin/env python3
"""Native text widths for Ariane's chapter, Fame Checker and two corrected Azuria references."""
import hashlib,json,os,re
from pathlib import Path
from mgba_rpc import ROOT,Emulator
OUT=ROOT/'QA_RECETTE_FINALE/CARMIN_2026_10_22'
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
rows=[];r=Emulator()
try:
 for path,select in [('data/maps/VermilionCity_Gym/text.inc',None),('data/maps/VermilionCity/text.inc','GymSign'),('data/text/fame_checker.inc','LtSurge'),('data/maps/Route20/text.inc','MistyTrainsHere'),('data/maps/CeladonCity_Condominiums_3F/text.inc','IWroteTheStory')]:
  for label,body in re.findall(r'^(\w+)::[^\n]*\n((?:[ \t]+\.string .*\n)+)',(ROOT/path).read_text(),re.M):
   if select and select not in label:continue
   for text in re.findall(r'\.string "(.*)"',body):
    text=text.replace('{PLAYER}','WWWWWWW').replace('{RIVAL}','Matt');text=re.sub(r'\{[^}]+\}','',text)
    for line in re.split(r'\\[nlp]',text.rstrip('$')):
     if not line:continue
     r.write(r.PARAMS+128,bytes(glyph[c] for c in line)+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0)
     rows.append(dict(label=label,line=line,pixels=width,passed=width<=208))
finally:r.close()
report=dict(passed=all(x['passed'] for x in rows),lines=len(rows),max_pixels=208,rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),results=rows)
(OUT/'TEXTES_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert report['passed'],[x for x in rows if not x['passed']]
print('TEXT PASS',len(rows),flush=True)

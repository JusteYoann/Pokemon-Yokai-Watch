#!/usr/bin/env python3
"""Measure added cameo dialogue with the native GBA font, not character counts."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
paths=['data/maps/Route25/scripts.inc','data/maps/MtEmber_Summit/scripts.inc','data/maps/CeruleanCave_B1F/scripts.inc','data/maps/CeladonCity/scripts.inc']
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
glyphs["'"]=glyphs['’']
r=Emulator();results=[]
try:
 r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 for path in paths:
  for number,line in enumerate((ROOT/path).read_text().splitlines(),1):
   if path.endswith('CeladonCity/scripts.inc') and number < (ROOT/path).read_text().splitlines().index('CeladonCity_Text_YokaiFriendOffer::')+1:continue
   m=re.search(r'\.string "(.*)"',line)
   if not m:continue
   assert '{' not in m[1],('Dynamic text requires a separate variable-width analysis',path,number)
   for text in re.split(r'\\[nlp]',m[1]):
    text=text.rstrip('$')
    if not text:continue
    r.write(r.PARAMS+128,bytes(glyphs[c] for c in text)+b'\xff')
    width=r.call('GetStringWidth',2,r.PARAMS+128,0)
    results.append({'file':path,'line':number,'text':text,'pixels':width})
    assert width<=208,(path,number,text,width,'exceeds 26-tile dialogue width')
finally:r.close()
report={'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'engine':'native GetStringWidth in mGBA','font':'FONT_NORMAL (2)','max_pixels':208,'scope':'Added Ariane/Enma/opposite protagonist static dialogue lines only; not all game text or battle dynamic placeholders','lines_checked':len(results),'results':results}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/LARGEURS_DIALOGUES_CAMEOS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'lines_checked':len(results),'passed':True}))

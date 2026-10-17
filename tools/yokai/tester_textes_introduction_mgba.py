#!/usr/bin/env python3
"""Native width and ROM encoding checks for Chen's new introductory story."""
import hashlib,json,re
from mgba_rpc import ROOT,Emulator
source=(ROOT/'data/text/new_game_intro.inc').read_text()
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
r=Emulator();results=[]
try:
 r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 for label,body in re.findall(r'^(gOakSpeech_Text_\w+)::\n((?:    \.string .*\n)+)',source,re.M):
  pieces=re.findall(r'\.string "(.*)"',body)
  assert not any(x in ''.join(pieces) for x in ['POKéMON','POKéDEX']),label
  # Exercise the actual seven-character player-name limit with wide glyphs.
  for piece in pieces:
   for line in re.split(r'\\[nlp]',piece):
    line=line.rstrip('$').replace('{PLAYER}','WWWWWWW').replace('{RIVAL}','Matt')
    if not line:continue
    encoded=bytes(glyphs[c] for c in line)+b'\xff';r.write(r.PARAMS+128,encoded)
    width=r.call('GetStringWidth',2,r.PARAMS+128,0)
    assert width<=208,(label,line,width)
    results.append({'label':label,'expanded_line':line,'pixels':width})
 report={'passed':True,'engine':'mGBA native GetStringWidth FONT_NORMAL','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'max_pixels':208,'dynamic_name_case':'seven wide W characters; Matt fixed','scope':'Chen introductory speech, not full-game translation or cinematic','lines':results}
 (ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/LARGEURS_INTRODUCTION_CHEN.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'passed':True,'lines':len(results)}))
finally:r.close()

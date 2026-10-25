#!/usr/bin/env python3
"""Dialogues compilés : nouvelle partie des deux genres, noms dynamiques et police native."""
import re,json,hashlib,struct
from pathlib import Path
from postgame_qa_common import QA
import postgame_qa_common as common
from mgba_new_game import new_game as fresh_game
from mgba_rpc import ROOT
D=ROOT/'docs/dialogues-coherence-20261025';records=json.loads((D/'MODIFICATIONS.json').read_text());checks=[]
for gender in (0,1):
 common.new_game=lambda:fresh_game(gender)
 q=QA('TEMP.json');r=q.r
 assert r.read(r.u32(r.symbols['gSaveBlock2Ptr'])+8,1)[0]==gender
 try:
  # QA starts a fresh game using controller input, including the entire revised Oak intro.
  assert q.callback()=='CB2_Overworld'
  r.write(r.u32(r.symbols['gSaveBlock2Ptr']),b'\xd1'*7+b'\xff')
  maxima={2:0,4:0};count=0
  for row in records:
   label=row['label'];r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols[label]);raw=r.read(r.symbols['gStringVar4'],2048).split(b'\xff',1)[0]
   assert len(raw)<1000,(label,'expanded text exceeds native message buffer',len(raw))
   for line in re.split(b'[\xfe\xfa\xfb]',raw):
    if not line:continue
    for font in (2,4):
     r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',font,r.PARAMS+128,0);maxima[font]=max(maxima[font],width)
     assert width<=208,(gender,label,font,width,line.hex())
    count+=1
  # Native placeholder is resolved after the player's gender is chosen.
  r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols['gOakSpeech_Text_LetsGo']);text=r.read(r.symbols['gStringVar4'],1024).split(b'\xff',1)[0]
  expected='MICHAEL' if gender else 'NATHANIEL'
  encoded=bytes(0xbb+ord(c)-ord('A') for c in expected)
  assert encoded not in text,'Prototype creator must be revealed at Cramois, not in the intro'
  r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols['CinnabarIsland_Gym_Text_Meeting']);assert encoded in r.read(r.symbols['gStringVar4'],2048)
  checks.append(dict(gender=gender,new_game_completed=True,dialogues=len(records),expanded_lines=count,native_max_width=maxima,first_inventor=expected,prototype_revealed_at_Cramois=True));print('PASS',checks[-1],flush=True)
 finally:r.close()
(D/'TESTS_TEXTES.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,checks=checks),ensure_ascii=False,indent=2)+'\n')

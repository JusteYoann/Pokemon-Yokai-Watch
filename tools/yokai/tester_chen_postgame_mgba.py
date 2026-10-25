#!/usr/bin/env python3
"""Compatibilité des anciens états de laboratoire : garçon/fille, visibilité et histoire."""
import json,hashlib,re
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/'docs/postgame-corrections-terminyanator-20261025';checks=[]
for gender in (0,1):
 q=QA('TEMP.json');r=q.r
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));q.mon();base=r.snapshot()
  for stage in (7,8,9):
   r.restore(base);q.f(0x82c);q.f(0x2b);q.f(0x2d,False);r.call('VarSet',0x4055,stage);q.warp('PalletTown_ProfessorOaksLab',6,4)
   oak=q.local('LOCALID_OAKS_LAB_PROF_OAK');matt=q.local('LOCALID_OAKS_LAB_RIVAL');a=q.actors()
   assert oak in a and matt not in a
   assert not r.read(a[oak]+1,1)[0]&0x20
   assert r.call('VarGet',0x4055)==9 and r.call('IsNationalPokedexEnabled')
   checks.append(dict(gender=gender,old_stage=stage,Chen_visible=True,Matt_absent=True,normalized_stage=9))
  r.restore(base);q.f(0x2b,False);q.f(0x2d,False);r.call('VarSet',0x4055,2);q.warp('PalletTown_ProfessorOaksLab',6,4)
  assert q.local('LOCALID_OAKS_LAB_RIVAL') in q.actors();checks.append(dict(gender=gender,story_rival_preserved=True))
  maximum=0
  for file in ('data/maps/FourIsland_IcefallCave_Back/text.inc','data/scripts/juste_yoann.inc','data/scripts/postgame_quests.inc'):
   for label in re.findall(r'^(\w+)::',(ROOT/file).read_text(),re.M):
    if not ('Text_' in label or '_Text' in label) or label not in r.symbols:continue
    raw=r.read(r.symbols[label],4096).split(b'\xff',1)[0]
    for line in re.split(b'[\xfa\xfb\xfe]',raw):
     if not line or len(line)>110:continue
     line=line.replace(b'\xfd\x01',b'\xd1'*7);r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0);maximum=max(maximum,width)
     assert width<=208,(label,width)
  checks.append(dict(gender=gender,native_text_maximum=maximum));print('PASS',gender,flush=True)
 finally:r.close()
(D/'TESTS_CHEN.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks),ensure_ascii=False,indent=2)+'\n')

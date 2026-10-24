#!/usr/bin/env python3
"""Normal-mode regression fixtures; no Nuzlocke rules may affect existing play."""
import os,json,hashlib
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/nuzlocke-20261024'/os.environ.get('NUZ_MODE','public');P.mkdir(parents=True,exist_ok=True)
rows=[]
for nuzlocke in (False,True):
 r=new_game(nuzlocke=nuzlocke)
 try:
  assert r.call('NuzlockeEnabled')==int(nuzlocke)
  r.call('ClearBag')
  r.call('ScriptContext_SetupScript',r.symbols['PalletTown_ProfessorOaksLab_EventScript_InitialNuzlockeBalls'])
  r.run(30)
  assert r.call('CheckBagHasItem',4,10 if nuzlocke else 5)
  assert not r.call('CheckBagHasItem',4,11 if nuzlocke else 6)
  rows.append('Native initial Ball gift: '+('10 in Nuzlocke' if nuzlocke else '5 in Normal'))
  if nuzlocke:continue
  ptr=r.symbols['gPlayerParty'];r.call('CreateMon',ptr,1,30,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
  r.call('NuzlockeMarkDead',ptr);assert not r.call('NuzlockeIsDead',ptr)
  scratch=r.symbols['gStringVar4'];r.w32(scratch,0);r.call('SetMonData',ptr,57,scratch)
  r.call('HealPlayerParty');assert r.call('GetMonData',ptr,57)>0
  assert r.call('NuzlockeResolveParty')==0
  assert r.call('NuzlockeCanCapture',ptr)
  assert r.call('ItemId_GetPrice',4)==200 and r.call('ItemId_GetPrice',3)==600 and r.call('ItemId_GetPrice',2)==1200
  rows.append('Normal: no permanent death, regular healing, unrestricted captures, original Ball prices')
 finally:r.close()
(P/'NORMAL.json').write_text(json.dumps(dict(passed=True,scope=__doc__,cases=rows),ensure_ascii=False,indent=2)+'\n')
print('PASS',rows,flush=True)

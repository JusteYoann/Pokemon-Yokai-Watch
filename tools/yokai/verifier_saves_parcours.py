#!/usr/bin/env python3
"""Cold mGBA Continue for untouched batteries exported by the actual playthrough."""
import ctypes as C,json,hashlib,struct
from pathlib import Path
from mgba_rpc import Emulator
OUT=Path('/workspace/artifacts/parcours-joueur-20261024')
class ReadOnly(Emulator):
 def assemble_stub(self):pass
 def call(self,*a,**k):raise RuntimeError('No injected calls')
 def write(self,*a,**k):raise RuntimeError('No RAM patches')
groups=json.loads((Path(__file__).resolve().parents[2]/'data/maps/map_groups.json').read_text());maps={(i,j):n for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
rows=[]
for p in sorted(OUT.glob('*/Pokemon_Yokai_Watch_Beta_0.1_FR.sav')):
 expected=json.loads((p.parent/'ETAT.json').read_text());data=p.read_bytes();sha=hashlib.sha256(data).hexdigest();r=ReadOnly()
 try:
  r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
  C.memmove(r.lib.retro_get_memory_data(0),data,len(data)) # Load the original battery file unchanged.
  r.lib.retro_reset();r.run(600);r.keys={3};r.run(2);r.keys=set();r.run(180)
  for i in range(9000):
   r.keys={8} if i%16<3 else set();r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3) and r.read(r.symbols['sLockFieldControls'],1)==b'\0':break
  else:raise AssertionError('Continue did not reach player control')
  r.keys=set();r.run(90);sb=r.u32(r.symbols['gSaveBlock1Ptr']);xy=struct.unpack('<hh',r.read(sb,4));party=r.read(r.symbols['gPlayerPartyCount'],1)[0]
  actual_map=maps[tuple(r.read(sb+4,2))];assert actual_map==expected['location']['map'],(p,actual_map,expected['location'])
  for j,mon in enumerate(expected['party']):
   ptr=r.symbols['gPlayerParty']+100*j
   assert r.read(ptr+84,1)[0]==mon['level'],(p,'Level differs',j)
   assert list(struct.unpack('<HH',r.read(ptr+86,4)))==mon['hp'],(p,'HP differs',j)
  assert party==len(expected['party']),(p,party,expected['party'])
  assert xy==tuple(expected['location']['xy']),(p,xy,expected['location'])
  assert p.read_bytes()==data
  r.frame.save(p.parent/'continuer-verifie.png');result=dict(passed=True,file=p.parent.name,sha256=sha,bytes=len(data),position=xy,party_count=party,source_unchanged=True)
  (p.parent/'CONTINUER.json').write_text(json.dumps(result,indent=2)+'\n');rows.append(result);print('PASS',p.parent.name,flush=True)
 finally:r.close()
(OUT/'VERIFICATION_SAVES.json').write_text(json.dumps(dict(scope=__doc__,results=rows),indent=2)+'\n')

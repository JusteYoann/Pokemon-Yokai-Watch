#!/usr/bin/env python3
"""ARM-native phase rules in mGBA, NOT a rendered eight-phase battle test."""
import hashlib,json,struct,time
from pathlib import Path
from mgba_rpc import ROOT,Emulator
Q=ROOT/'QA_RECETTE_FINALE/DON_SPIRATON';Q.mkdir(exist_ok=True)
r=Emulator();rows=[];passed=False
state=r.PARAMS+64;target=r.PARAMS+128
native_frames=[0];original_run=r.run
def counted_run(frames=1):
 native_frames[0]+=frames;original_run(frames)
r.run=counted_run
try:
 for species,types in [(1,(10,10)),(7,(11,11)),(150,(14,14))]:
  r.write(target,struct.pack('<HBBB x4H',species,60,*types,0,0,0,0))
  assert r.call('SpiratonCoreStart',state,52,target)==1
  forms=[];durations=[];selection_frames=[]
  for phase in range(8):
   form=r.call('SpiratonCoreInspect',state,0);forms.append(form)
   assert r.call('SpiratonCoreInspect',state,1)==56+phase and r.call('SpiratonCoreInspect',state,2)==phase
   hp=r.call('SpiratonCoreInspect',state,3);assert hp>0
   assert r.call('SpiratonCoreDamage',state,1000000)==hp
   assert r.call('SpiratonCoreInspect',state,3)==0
   assert r.call('SpiratonCoreDamage',state,1000000)==0
   start=time.monotonic();before=native_frames[0];result=r.call('SpiratonCoreEndTurn',state,target);selection_frames.append(native_frames[0]-before);durations.append(time.monotonic()-start)
   assert result==(1 if phase<7 else 0)
  assert len(set(forms))==8
  rows.append(dict(active_species=species,forms=forms,max_rpc_wall_seconds=max(durations),native_frames_per_end_turn_call=selection_frames,passed=True))
 passed=True
finally:
 r.close();(Q/'CORE_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows,human_playtest=False),indent=2)+'\n')
print('PASS native ARM core: three full eight-phase sequences; this does not validate battle engine integration')

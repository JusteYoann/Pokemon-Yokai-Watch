#!/usr/bin/env python3
"""Rencontres statiques natives: prérequis préparés, K.O. et capture par touches."""
import struct,subprocess
from postgame_qa_common import QA
q=QA('TESTS_STATIQUES.json');r=q.r
try:
 q.mon();r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],85,0);q.f(0x82c)
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);r.write(sb+0xee0+0x500//8,b'\xff'*96)
 nm=subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True)
 actions={int(a[0],16)|1 for line in nm.splitlines() if len(a:=line.split())==3 and a[2]=='HandleInputChooseAction'}
 cases=[('Kyubi','SeafoamIslands_B4F',9,3,3,'PG_Kyubi',16,'FLAG_PG_KYUBI_CAUGHT'),('Octorgone','PowerPlant',5,12,6,'PG_Octorgone',15,'FLAG_PG_OCTORGONE_CAUGHT'),('Enma','CeruleanCave_B1F',7,13,3,'CeruleanCave_B1F_EventScript_Mewtwo',150,0x305),('Gorgouille','MtEmber_Summit',9,7,1,'Onis_EventScript_Gorgouille',65,0x33b)]
 for name,map_,x,y,local,script,sp,flag in cases:
  print('START',name,flush=True)
  if name in ('Kyubi','Octorgone'):
   q.f('FLAG_PG_NYADA_I_ACTIVE',False);q.warp(map_,x,y);assert local not in q.actors();q.f('FLAG_PG_NYADA_I_ACTIVE')
  if name=='Gorgouille':
   for f in (0x335,0x336,0x337,0x33a):q.f(f,False)
   q.warp(map_,x,y);assert local not in q.actors()
   for f in (0x335,0x336,0x337,0x33a):q.f(f)
  q.warp(map_,x,y);assert local in q.actors();q.shot(name.lower()+'-statique')
  r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',local));q.script(script);q.wait(lambda:q.callback()=='BattleMainCB2',30000)
  assert r.call('GetMonData',r.symbols['gEnemyParty'],11,0)==sp
  q.drain(60000);assert not q.fg(flag) and local not in q.actors()
  q.warp('PalletTown_PlayersHouse_2F',5,5);q.warp(map_,x,y);assert local in q.actors()
  q.passed(name+': K.O. réel, absence temporaire puis réapparition au retour dans la zone')
  r.call('HealPlayerParty');r.call('ClearBag');r.call('AddBagItem',1,1)
  r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',local));q.script(script);q.wait(lambda:q.callback()=='BattleMainCB2',30000)
  for f in range(12000):
   if r.u32(r.symbols['gBattlerControllerFuncs']) in actions:break
   r.keys={0} if f%16<2 else set();r.run()
  else:raise AssertionError(('Menu capture',name))
  r.keys=set();r.run(16)
  r.write(r.symbols['gBagMenuState']+6,b'\x02\x00');q.pulse(7);assert r.read(r.symbols['gActionSelectionCursor'],1)==b'\x01'
  q.pulse(8,240);q.pulse(8,90);q.pulse(8,90)
  for f in range(18000):
   if q.idle():break
   r.keys={0} if f%16<2 else set();r.run()
  else:raise AssertionError(('Retour capture',name,q.callback()))
  assert r.read(r.symbols['gBattleOutcome'],1)==b'\x07' and q.fg(flag),(name,q.fg(flag))
  assert r.call('GetSetPokedexFlag',sp,1)==1
  q.warp('PalletTown_PlayersHouse_2F',5,5);q.warp(map_,x,y);assert local not in q.actors()
  q.passed(name+': capture réelle à la Master Ball, Médallium enregistré et disparition définitive au retour')
finally:q.finish()

#!/usr/bin/env python3
from postgame_qa_common import QA
q=QA('TESTS_SCIENTIFIQUE.json');r=q.r
try:
 q.mon();r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],53,0);q.f(0x82c)
 base=r.snapshot()
 for stage,map_,x,y,script,sp,level in [(1,'LavenderTown',9,13,'PG_ScientistLav',17,60),(2,'VermilionCity',17,27,'PG_ScientistPort',18,65),(3,'SaffronCity',19,23,'PG_ScientistYopple',19,70)]:
  q.warp(map_,x,y);local=q.local('LOCALID_PG_SCIENTIST_'+('LAV' if stage==1 else 'PORT' if stage==2 else 'YOPPLE'));assert local in q.actors(),(stage,q.actors())
  npc=q.actors()[local];import struct;nx,ny=struct.unpack('<hh',r.read(npc+16,4));assert not r.call('MapGridGetCollisionAt',nx,ny),(map_,nx,ny)
  q.script(script);q.wait(lambda:q.callback()=='BattleMainCB2',30000)
  enemy=r.symbols['gEnemyParty'];assert r.call('GetMonData',enemy,11,0)==sp and r.call('GetMonData',enemy,56,0)==level
  assert r.call('GetBattleBGM')==364
  assert bool(r.call('IsMonShiny',enemy))==(stage==3)
  r.run(100);q.shot('scientifique-'+str(stage)+'-combat')
  q.drain(60000)
  flag='FLAG_PG_SCIENTIST_1' if stage==1 else 'FLAG_PG_SCIENTIST_2' if stage==2 else 'FLAG_PG_ROBO_GIVEN';assert q.fg(flag)
  q.saved(flag)
  q.passed(f'Scientifique étape {stage}: vraie victoire, espèce {sp}, niveau {level}, OST Futur, progression séquentielle')
 assert q.fg('FLAG_PG_SCIENTIST_WON') and q.fg('FLAG_PG_ROBO_GIVEN');q.warp('SaffronCity',19,23);assert q.local('LOCALID_PG_SCIENTIST_YOPPLE') not in q.actors()
 q.passed('Robonyan 28 shiny offert après la troisième victoire; scientifique définitivement absent au retour')
 r.restore(base)
 for map_,x,y,local in [('VermilionCity',17,27,'PORT'),('SaffronCity',19,23,'YOPPLE')]:
  q.warp(map_,x,y);assert q.local('LOCALID_PG_SCIENTIST_'+local) not in q.actors()
 q.passed('Sans la première victoire, les rencontres de Carmin-sur-Mer et Safrania sont cachées')
finally:q.finish()

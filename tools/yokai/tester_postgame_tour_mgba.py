#!/usr/bin/env python3
from postgame_qa_common import QA
import re,struct
q=QA('TESTS_TOUR.json');r=q.r
try:
 q.mon(level=100)
 for i,sp in enumerate((149,65,123,25,87),1):q.mon(i,sp,100)
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],53,0);q.f(0x82c)
 q.warp('TrainerTower_Lobby',9,8);q.drain(18000);g,n=q.maps['SevenIsland_TrainerTower'];assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==(g,n)
 q.passed('Sans Ticket de la Tour: réception refusée, retour devant la porte et commandes rendues')
 q.f('FLAG_PG_DEMOPHAGE_GIVEN');r.call('PostgameGiveTicket');assert q.result()==1
 q.warp('TrainerTower_Lobby',9,8);q.drain(18000)
 assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==q.maps['TrainerTower_Lobby']
 q.passed('Avec le ticket: accès à la réception native, quatre modes conservés')
 base=r.snapshot()
 for mode in range(4):
  r.restore(base);r.write(r.symbols['gSpecialVar_0x8004'],struct.pack('<H',6));r.write(r.symbols['gSpecialVar_0x8005'],struct.pack('<H',mode));r.call('CallTrainerTowerFunc')
  levels=[]
  for floor in range(8):
   q.warp(f'TrainerTower_{floor+1}F',13,18)
   r.call('SetUpTrainerTowerDataStruct');r.call('VarSet',0x4001,0);r.call('BuildEnemyParty');r.call('FreeTrainerTowerDataStruct')
   species=[]
   for i in range(2):
    p=r.symbols['gEnemyParty']+100*i;sp=r.call('GetMonData',p,11,0)
    if sp:assert 1<=sp<=151;species.append(sp);assert r.call('GetMonData',p,56,0)==94+min(floor,6)
   assert species;levels.append(94+min(floor,6));r.call('TrainerTowerAddFloorCleared')
  q.warp('TrainerTower_Roof',7,8);assert q.fg('FLAG_PG_TOWER_CLEAR') and q.local('LOCALID_PG_NYADA_ROOF') in q.actors()
  q.passed(f'Mode {mode}: huit étages, équipes uniquement 151 Yo-kai, niveaux {levels}, Maître Nyada débloqué après ce seul mode')
 q.shot('maitre-nyada-sommet-tour')
 q.script('PG_NyadaRoof');q.wait(lambda:q.callback()=='BattleMainCB2',30000)
 expected=[27,30,14,18,40,148]
 for i,sp in enumerate(expected):assert r.call('GetMonData',r.symbols['gEnemyParty']+100*i,11,0)==sp
 assert r.call('GetBattleBGM')==375
 r.run(100);q.shot('maitre-nyada-combat-final')
 q.passed('Vrai combat final Maître Nyada: composition validée de la Ligue, Démophage puis Maître Nyada en derniers, OST boss')
 q.drain(90000);assert q.fg('FLAG_PG_NYADA_FINAL_WON') and q.fg('FLAG_PG_NYADA_GIVEN')
 assert q.give(2)==2
 q.passed('Victoire réelle au sommet: Maître Nyada offert une seule fois; cadeau non duplicable')
 # mGBA masks battery writeback after retro_unserialize. Test persistence
 # separately in a fresh core with no restored state, using the native gift script.
 checks=q.checks;r.close();q=QA('TESTS_TOUR.json');r=q.r;q.checks=checks;q.mon();q.f(0x82c)
 for flag in ('FLAG_PG_TOWER_CLEAR','FLAG_PG_NYADA_FINAL_WON'):q.f(flag)
 q.warp('TrainerTower_Roof',7,8);q.script('PG_NyadaRoof');q.drain(24000)
 assert q.fg('FLAG_PG_NYADA_GIVEN');q.saved('FLAG_PG_TOWER_CLEAR','FLAG_PG_NYADA_GIVEN');assert q.give(2)==2
 q.passed('Cadeau natif du sommet puis sauvegarde/Continuer: progression et unicité conservées (fixture séparée sans état rapide mGBA)')
finally:q.finish()

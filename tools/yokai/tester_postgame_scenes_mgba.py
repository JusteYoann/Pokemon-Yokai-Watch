#!/usr/bin/env python3
from postgame_qa_common import QA
q=QA('TESTS_SCENES.json');r=q.r
try:
 q.mon();
 for i,sp in enumerate((149,65,123,25,87),1):q.mon(i,sp,100)
 q.f(0x82c)
 q.warp('PalletTown_PlayersHouse_1F',6,6);assert q.fg('FLAG_PG_ENMA_INTRO_PENDING')
 q.warp('PalletTown',6,7);assert q.local('LOCALID_PG_ENMA_INTRO') in q.actors();q.shot('introduction-seigneur-enma')
 q.drain(24000);assert q.fg('FLAG_PG_ENMA_INTRO') and not q.fg('FLAG_PG_ENMA_INTRO_PENDING')
 q.passed('Première sortie de la maison après la Ligue: vraie cinématique Enma terminée et commandes rendues')
 q.warp('PalletTown_PlayersHouse_1F',6,6);q.warp('PalletTown',6,7);assert q.local('LOCALID_PG_ENMA_INTRO') not in q.actors()
 q.passed('L’introduction ne se rejoue pas après une nouvelle sortie de la maison')
 q.warp('SevenIsland_House_Room1',2,5);assert q.local('LOCALID_PG_NYADA_HOME') in q.actors()
 q.script('PG_NyadaHome');r.run(100);q.shot('maitre-nyada-quete-i');q.drain(24000);assert q.fg('FLAG_PG_NYADA_I_ACTIVE')
 q.script('PG_NyadaHome');q.drain();assert not q.fg('FLAG_PG_NYADA_I_COMPLETE')
 q.passed('Maître Nyada, chat dans la maison de l’Île 7: activation de la quête I puis refus sans les deux captures')
 r.call('ScriptGiveMon',15,60,0,0,0,0);r.call('ScriptGiveMon',16,60,0,0,0,0)
 q.script('PG_NyadaHome');q.drain(24000);assert q.fg('FLAG_PG_NYADA_I_COMPLETE') and r.call('CheckBagHasItem',197,1)
 q.saved('FLAG_PG_NYADA_I_COMPLETE')
 q.passed('Retour avec Kyubi et Octorgone: Œuf Chance reçu et quête I terminée')
 q.script('PG_NyadaHome');q.drain();assert not q.fg(0x32f)
 q.f(0x33b);q.script('PG_NyadaHome');q.drain();assert not q.fg(0x32f)
 q.passed('Nyada II refuse les trois victoires seules et exige aussi une nouvelle visite après les deux quêtes')
 q.warp('SevenIsland',8,8);q.warp('SevenIsland_House_Room1',2,5);q.script('PG_NyadaHome');q.drain(24000);assert q.fg(0x32f)
 q.passed('Nouvelle visite avec Gorgouille capturé: invitation à rejoindre Maître Nyada dans la Grotte Azurée')
 q.warp('CeruleanCave_1F',9,6);assert q.local('LOCALID_PG_NYADA_CAVE') in q.actors() and q.local('LOCALID_PG_DEMOPHAGE') in q.actors(),(q.actors(),q.fg(0x32f),q.fg('FLAG_PG_HIDE_NYADA_CAVE'),q.fg('FLAG_PG_HIDE_DEMOPHAGE'),q.fg('FLAG_PG_NYADA_II_COMPLETE'),q.callback());q.shot('maitre-nyada-demophage-grotte')
 r.call('VarSet',0x40fb,0x100);assert not r.call('TerreHeureTryStep');r.call('VarSet',0x40fb,0)
 q.passed('Les deux sprites sont présents dans la Grotte Azurée et bloquent la Terr’heure pendant la quête')
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],53,0)
 q.script('PG_CaveScene');q.wait(lambda:q.callback()=='BattleMainCB2',30000)
 expected=[80,78,99,86,40]
 for i,sp in enumerate(expected):
  p=r.symbols['gEnemyParty']+100*i;assert r.call('GetMonData',p,11,0)==sp and r.call('GetMonData',p,56,0)==61+i
 assert r.call('GetBattleBGM')==375
 r.run(90);q.shot('demophage-combat-portrait')
 q.passed('Scène de l’endormissement puis vrai combat Démophage: cinq espèces exactes, niveaux 61 à 65 et OST boss')
 q.drain(60000)
 assert q.fg('FLAG_PG_DEMOPHAGE_WON') and q.fg('FLAG_PG_DEMOPHAGE_GIVEN') and q.fg('FLAG_PG_NYADA_II_COMPLETE') and not q.fg(0x32f)
 assert r.call('CheckBagHasItem',54,1)
 q.saved('FLAG_PG_NYADA_II_COMPLETE','FLAG_PG_DEMOPHAGE_GIVEN','FLAG_PG_TICKET_GIVEN')
 q.passed('Véritable victoire contre Démophage, cadeau direct, ticket reçu, quête II conclue et blocage Terr’heure levé')
finally:q.finish()

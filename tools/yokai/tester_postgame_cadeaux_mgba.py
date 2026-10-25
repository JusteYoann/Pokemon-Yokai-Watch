#!/usr/bin/env python3
from postgame_qa_common import QA
import struct
q=QA('TESTS_CADEAUX.json');r=q.r
try:
 q.mon();r.call('PostgameSync')
 assert all(q.give(g)==2 for g in range(4));r.call('PostgameGiveTicket');assert q.result()==0
 q.passed('Avant la Ligue: les quatre nouveaux cadeaux et le ticket sont refusés')
 assert q.fg('FLAG_PG_HIDE_NYADA_HOME') and q.fg('FLAG_PG_HIDE_SCIENTIST_LAV')
 q.passed('Avant la Ligue: Maître Nyada et le scientifique restent invisibles')
 q.f(0x82c);base=r.snapshot()
 for i in range(6):q.mon(i,150,60)
 q.warp('PalletTown_ProfessorOaksLab',6,10)
 pc_empty=r.snapshot()
 assert q.give(0)==1 and q.fg('FLAG_PG_CHEN_JIBANYAN');assert q.give(0)==2
 q.passed('Jibanyan supplémentaire envoyé au PC avec équipe complète, puis refus d’un doublon')
 for gift,prereq,flag,species in [(1,'FLAG_PG_DEMOPHAGE_WON','FLAG_PG_DEMOPHAGE_GIVEN',40),(2,'FLAG_PG_NYADA_FINAL_WON','FLAG_PG_NYADA_GIVEN',148),(3,'FLAG_PG_SCIENTIST_WON','FLAG_PG_ROBO_GIVEN',19)]:
  assert q.give(gift)==2;q.f(prereq);assert q.give(gift)==1 and q.fg(flag);assert q.give(gift)==2
  q.passed(f'Cadeau {species}: prérequis vérifié, réception au PC, drapeau unique après succès')
 # The first four PC slots are the four successfully received gifts.
 for slot,sp in enumerate((1,40,148,19)):
  ptr=r.call('GetBoxedMonPtr',0,slot);assert r.call('GetBoxMonData',ptr,11,0)==sp
  assert not r.call('GetBoxMonData',ptr,4,0)
  if sp==19:
   pid=r.call('GetBoxMonData',ptr,0,0);ot=r.call('GetBoxMonData',ptr,1,0);assert ((pid>>16)^(pid&65535)^(ot>>16)^(ot&65535))<8
 q.passed('Robonyan 28 reçu réellement shiny dans ses données; quatre cadeaux valides au PC')
 r.call('PostgameGiveTicket');assert q.result()==1 and r.call('CheckBagHasItem',54,1)
 q.passed('Ticket de la Tour reçu comme objet clé, après Démophage')
 # Friends may be stored entirely in the PC.
 r.call('ScriptGiveMon',15,60,0,0,0,0);r.call('ScriptGiveMon',16,60,0,0,0,0);r.call('PostgameHaveFriends');assert q.result()==1
 q.passed('Kyubi et Octorgone reconnus grâce à leurs captures, même tous deux au PC')
 # Store a legitimate native save, then Continue through the real title menu.
 expected={k:q.fg(k) for k in ['FLAG_PG_CHEN_JIBANYAN','FLAG_PG_DEMOPHAGE_GIVEN','FLAG_PG_NYADA_GIVEN','FLAG_PG_ROBO_GIVEN','FLAG_PG_TICKET_GIVEN']}
 r.call('SaveMapView');r.call('SaveQuestLogData');assert r.call('TrySavingData',0,max_frames=3000)==1
 r.lib.retro_reset();r.run(600);q.pulse(3,180);q.wait(lambda:q.callback()=='CB2_Overworld' and q.unlocked(),18000)
 assert all(q.fg(k)==v for k,v in expected.items()) and r.call('CheckBagHasItem',54,1)
 q.passed('Sauvegarde native puis Continuer: cadeaux uniques et ticket conservés')
 r.restore(pc_empty)
 ptr=r.call('GetBoxedMonPtr',0,0);r.call('CreateBoxMon',ptr,1,10,31,1,12345,0,0);box=r.read(ptr,80);r.write(ptr,box*420)
 assert q.give(0)==2 and not q.fg('FLAG_PG_CHEN_JIBANYAN')
 r.call('ZeroBoxMonData',ptr);assert q.give(0)==1 and q.fg('FLAG_PG_CHEN_JIBANYAN')
 q.passed('Équipe et 420 cases PC pleines: cadeau conservé, puis reçu après libération d’une place')
finally:q.finish()

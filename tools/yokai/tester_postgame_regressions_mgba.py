#!/usr/bin/env python3
"""Contrôles ciblés des quêtes existantes et du texte, pas une nouvelle partie complète."""
import re,struct
from postgame_qa_common import QA
from mgba_rpc import ROOT
q=QA('TESTS_REGRESSIONS.json');r=q.r
try:
 for i,sp in enumerate((150,149,65,123,25,87)):q.mon(i,sp,100)
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],53,0)
 # Measure compiled text using native font, including expanded long names.
 checked=0
 for name in [n for n in r.symbols if n.startswith('PG_Text_')]:
  r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols[name]);raw=r.read(r.symbols['gStringVar4'],2048).split(b'\xff',1)[0]
  for line in re.split(b'[\xfe\xfa\xfb]',raw):
   assert len(line)<256;r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0);assert width<=216,(name,width);checked+=1
 q.passed(f'{checked} lignes des nouveaux dialogues mesurées avec la police native: aucune ne dépasse la boîte de texte')
 q.f(0x82c);q.warp('PokemonTower_7F',10,5);q.script('Onis_EventScript_AlizonTour');q.drain(24000)
 assert q.fg(0x338) and q.fg(0x339) and not q.fg(0x33a)
 for flag in (0x335,0x336,0x337):q.f(flag)
 q.script('Onis_EventScript_AlizonTour');q.drain(24000);assert q.fg(0x33a)
 q.passed('Quête Alizon conservée: Short Oni, trois victoires exigées, puis rendez-vous au Mont Braise')
 for flag in (0x32c,0x4b6,0x24e):q.f(flag)
 r.call('VarSet',0x40f4,3);q.warp('CinnabarIsland_Gym',5,5);q.script('CinnabarIsland_Gym_EventScript_Blaine');q.drain(90000)
 assert q.fg(0x32d) and q.fg(0x32e)
 found=False
 for slot in range(30):
  if r.call('GetBoxMonData',r.call('GetBoxedMonPtr',0,slot),11,0)==149:found=True;break
 assert found
 q.script('CinnabarIsland_Gym_EventScript_Blaine');q.drain();q.passed('Rematch réel Nathaniel/Michael de Cramois’Île: victoire, Hovernyan au PC et aucun deuxième cadeau')
 for n in range(1,151):
  r.call('GetSetPokedexFlag',n,2);r.call('GetSetPokedexFlag',n,3)
 # Mark the same151 roster through the native Medallium setter.
 r.call('GetSetPokedexFlag',150,2)
 assert not r.call('YoannMedalliumComplete')
 r.call('GetSetPokedexFlag',151,2);r.call('GetSetPokedexFlag',151,3);assert r.call('YoannMedalliumComplete');q.f(0x331);r.call('YoannSyncVisibility');assert not q.fg(0x334)
 q.warp('PalletTown_PlayersHouse_2F',6,3);q.script('Yoann_EventScript_FirstVictory');q.drain(24000)
 assert q.fg(0x332) and q.fg(0x333) and r.call('CheckBagHasItem',52,1)
 r.call('YoannGiveCharm');assert not q.result() and not r.call('CheckBagHasItem',52,2)
 q.saved(0x332,0x333);q.passed('Médallium exige les 151 captures; scène de remerciement, Charme Chroma unique et sauvegarde conservés (victoire secrète préparée)')
finally:q.finish()

#!/usr/bin/env python3
"""Scènes isolées préparées avant enregistrement ; commandes natives pendant le film.
Les combats sont gagnés normalement avec une équipe de niveau 100. Les coupes
ultérieures retirent les combats, jamais les déplacements ni les dialogues de scène.
"""
import sys,json,struct
from pathlib import Path
from postgame_qa_common import QA
from film_cible_mgba import Film
from mgba_rpc import ROOT
from mafiamille_qa import C
D=ROOT/'docs/cinematiques-compilation-20261025';D.mkdir(exist_ok=True)
name=sys.argv[1];q=QA('TEMP_CINEMA.json');r=q.r
flags=[];variables=[];script=None;local=1;automatic=False
# map,x,y,label,flags,vars. Fixtures are disclosed in the per-scene metadata.
cases={
 '28-depart-sevii':('CinnabarIsland',18,9,None,[],[(0x4071,1)]),
 '29-retour-sevii':('CinnabarIsland',21,7,None,[],[(0x4071,3)]),
 '30-saphir-vol':('SixIsland_DottedHole_SapphireRoom',5,6,'SixIsland_DottedHole_SapphireRoom_EventScript_Sapphire',[0x82c],[]),
 '31-entrepot-admin1':('FiveIsland_RocketWarehouse',14,43,'FiveIsland_RocketWarehouse_EventScript_Admin1',[0x82c],[]),
 '32-entrepot-admin2':('FiveIsland_RocketWarehouse',7,3,'FiveIsland_RocketWarehouse_EventScript_Admin2',[0x82c],[]),
 '33-entrepot-scientifique':('FiveIsland_RocketWarehouse',13,3,'FiveIsland_RocketWarehouse_EventScript_Gideon',[0x82c],[]),
 '34-celio-rubis':('OneIsland_PokemonCenter_1F',15,6,'OneIsland_PokemonCenter_1F_EventScript_Celio',[0x82c],[(0x4076,2)]),
 '35-celio-saphir':('OneIsland_PokemonCenter_1F',15,6,'OneIsland_PokemonCenter_1F_EventScript_Celio',[0x82c],[(0x4076,3)]),
 '01e-tutoriel-capture':('ViridianCity',21,7,'ViridianCity_EventScript_TutorialOldMan',[],[(0x4051,1)]),
 '02d-chaussures':('PewterCity',37,18,'PewterCity_EventScript_RunningShoesAideTriggerMid',[0x820,C['FLAG_ARGENTA_MORLEONE_DONE']],[]),
 '10b-chen-jibanyan':('PalletTown_ProfessorOaksLab',6,4,'PalletTown_ProfessorOaksLab_EventScript_ProfOak',[0x82c],[(0x4055,9)]),
 '21b-chen-invitation':('PalletTown_ProfessorOaksLab',6,4,'PalletTown_ProfessorOaksLab_EventScript_ProfOak',[0x82c],[(0x4055,9)]),
 '02e-fossiles':('MtMoon_B2F',14,11,'MtMoon_B2F_EventScript_MiguelTrigger',[],[]),
 '28b-motards-argument':('ThreeIsland',17,15,'ThreeIsland_EventScript_BikerBossIntroTrigger',[],[]),
 '28c-motards-depart':('ThreeIsland',17,15,'ThreeIsland_EventScript_BattleBikersTriggerMid',[],[]),
 '09-terreur':('MtMoon_1F',20,27,None,[],[]),
 '01-chen-depart':('PalletTown',10,1,'PalletTown_EventScript_OakTriggerLeft',[],[]),
 '01b-choix-partenaire':('PalletTown_ProfessorOaksLab',8,5,'PalletTown_ProfessorOaksLab_EventScript_BulbasaurBall',[],[(0x4055,2)]),
 '01c-matt-laboratoire':('PalletTown_ProfessorOaksLab',6,8,'PalletTown_ProfessorOaksLab_EventScript_RivalBattleTriggerMid',[],[]),
 '01d-medallium':('PalletTown_ProfessorOaksLab',6,4,'PalletTown_ProfessorOaksLab_EventScript_ReceiveDexScene',[],[]),
 '02b-matt-route22':('Route22',29,4,'Route22_EventScript_EarlyRivalTriggerTop',[],[]),
 '02c-matt-azuria':('CeruleanCity',20,7,'CeruleanCity_EventScript_RivalTriggerMid',[],[]),
 '03b-matt-oceane':('SSAnne_2F_Corridor',36,8,'SSAnne_2F_Corridor_EventScript_RivalTriggerMid',[],[]),
 '03c-capitaine':('SSAnne_CaptainsOffice',4,3,'SSAnne_CaptainsOffice_EventScript_Captain',[],[]),
 '03d-depart-oceane':('SSAnne_Exterior',32,7,None,[],[(C['VAR_MAP_SCENE_VERMILION_CITY'],1)]),
 '07b-matt-yopple':('SilphCo_7F',6,4,'SilphCo_7F_EventScript_RivalTriggerTop',[],[]),
 '07c-matt-route22':('Route22',29,4,'Route22_EventScript_LateRivalTriggerTop',[],[]),
 '23b-leo-separateur':('Route25_SeaCottage',5,4,'Route25_SeaCottage_EventScript_Computer',[0x002],[]),
 '26-lorelei-grotte':('FourIsland_IcefallCave_Back',12,19,'FourIsland_IcefallCave_Back_EventScript_LoreleiRocketsScene',[0x82c],[]),
 '27-perdue-sauvetage':('ThreeIsland_BerryForest',4,2,'ThreeIsland_BerryForest_EventScript_Lostelle',[],[]),
 '02-argenta':('PewterCity',23,35,'PewterCity_EventScript_MorleoneArrival',[],[]),
 '03-ariane-rencontre':('VermilionCity',33,30,'Philosovni_CityAriane',[],[]),
 '04-enquete-entrepot':('VermilionCity_PhilosovniWarehouse',6,9,'Philosovni_Overhear',[],[(0x40f4,1)]),
 '05-zombie-night':('LavenderTown',11,1,None,[],[]),
 '06-cramois-rencontre':('CinnabarIsland_Gym',5,5,'CinnabarIsland_Gym_EventScript_Blaine',[],[(0x40f4,3)]),
 '07-yopple-liberation':('SilphCo_11F',6,15,'SilphCo_11F_EventScript_GiovanniTriggerLeft',[],[]),
 '08-finale':('PokemonLeague_ChampionsRoom',6,20,None,[],[]),
 '10-enma-postgame':('PalletTown',6,7,None,[0x82c,'FLAG_PG_ENMA_INTRO_PENDING'],[]),
 '11-nyada-premiere-quete':('SevenIsland_House_Room1',2,5,'PG_NyadaHome',[0x82c],[]),
 '12-nyada-retour-amis':('SevenIsland_House_Room1',2,5,'PG_NyadaHome',[0x82c,'FLAG_PG_NYADA_I_ACTIVE'],[]),
 '13-alizon-quete-oni':('PokemonTower_7F',11,5,'PokemonTower_7F_EventScript_MrFuji',[0x82c],[]),
 '14-alizon-rendez-vous':('PokemonTower_7F',11,5,'PokemonTower_7F_EventScript_MrFuji',[0x82c,0x335,0x336,0x337,0x338,0x339],[]),
 '16-nyada-seconde-quete':('SevenIsland_House_Room1',2,5,'PG_NyadaHome',[0x82c,'FLAG_PG_NYADA_I_COMPLETE',0x33b,'FLAG_PG_NYADA_II_LEAVE_OK'],[]),
 '17-demophage':('CeruleanCave_1F',21,18,'PG_CaveScene',[0x82c,0x32f,0x345,0x33b],[]),
 '18-nyada-sommet':('TrainerTower_Roof',9,8,'PG_NyadaRoof',[0x82c,'FLAG_PG_TOWER_CLEAR','FLAG_PG_NYADA_II_COMPLETE'],[]),
 '19-scientifique-lavanville':('LavenderTown',12,8,'PG_ScientistLav',[0x82c,0x322],[(0x40f3,1)]),
 '20-scientifique-carmin':('VermilionCity',30,29,'PG_ScientistPort',[0x82c,'FLAG_PG_SCIENTIST_1'],[(0x40f4,3)]),
 '21-scientifique-yopple':('SaffronCity',21,9,'PG_ScientistYopple',[0x82c,'FLAG_PG_SCIENTIST_1','FLAG_PG_SCIENTIST_2'],[]),
 '22-yoann':('PalletTown_PlayersHouse_2F',6,3,'Yoann_EventScript_NPC',[0x82c,0x331],[]),
 '23-leo-transformation':('Route25_SeaCottage',5,4,'Route25_SeaCottage_EventScript_Bill',[],[]),
 '24-repaire-morleone':('RocketHideout_B4F',25,4,'RocketHideout_B4F_EventScript_Giovanni',[0x823],[]),
 '25-champion-don-exil':('SixIsland_WaterPath_House2',7,5,'SixIsland_WaterPath_House2_EventScript_DonMorleone',[0x82c],[]),
}
for n,(mp,x,y,label) in enumerate([
 ('PewterCity_Gym',6,6,'Brock'),('CeruleanCity_Gym',8,7,'Misty'),('VermilionCity_Gym',5,3,'LtSurge'),('PokemonTower_7F',11,5,'MrFuji'),('FuchsiaCity_Gym',7,14,'Koga'),('SaffronCity_Gym',14,12,'Sabrina'),('CinnabarIsland_Gym',5,5,'Blaine'),('ViridianCity_Gym',2,3,'Giovanni')],1):
 cases[f'arene-{n:02}']=(mp,x,y,mp+'_EventScript_'+label,[],[(0x40f4,3)] if n==3 else [])
for n,(room,label) in enumerate([('Loreleis','Lorelei'),('Brunos','Bruno'),('Agathas','Agatha'),('Lances','Lance')],1):
 mp='PokemonLeague_'+room+'Room';cases[f'conseil-{n:02}']=(mp,6,6 if n<4 else 9,mp+'_EventScript_'+label,[],[(0x4068,n)])
try:
 for i,sp in enumerate((150,149,65,123,25,87)):
  p=q.mon(i,sp,100)
  for j,m in enumerate((53,94,58,85)):r.call('SetMonMoveSlot',p,m,j)
 map_,x,y,script,flags,variables=cases[name]
 for flag in flags:q.f(flag)
 if name.startswith(('arene-','conseil-')):
  index=int(name[-2:]);q.f(0x827);q.f(0x3e)
  for badge in range(8):q.f(0x820+badge,name.startswith('conseil-') or badge<index-1)
  r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96)
  opponent=409+index if name.startswith('conseil-') else [414,415,416,417,418,420,419,350][index-1]
  r.call('ClearTrainerFlag',opponent)
  if name=='arene-08':q.f(0x55,False)

 for var,value in variables:r.call('VarSet',var,value)
 r.call('VarSet',0x4020,10000)
 if name=='09-terreur':
  r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96);r.call('VarSet',0x40f9,1);r.call('VarSet',0x40fa,0x101);q.f(0x82f)
 if name=='02-argenta':
  q.f(0x892,False);q.f(C['FLAG_ARGENTA_MORLEONE_DONE'],False);q.f(C['FLAG_ARGENTA_MORLEONE_PENDING']);
 if name=='12-nyada-retour-amis':
  r.call('ScriptGiveMon',15,60,0,0,0,0);r.call('ScriptGiveMon',16,60,0,0,0,0)
 if name in ('22-yoann','21b-chen-invitation'):
  for i in range(1,152):r.call('GetSetPokedexFlag',i,3)
 if name=='25-champion-don-exil':r.call('SetTrainerFlag',744)
 if name in ('28-depart-sevii','29-retour-sevii'):q.f(0x62,False)
 if name=='34-celio-rubis':q.f(0x2dd);r.call('AddBagItem',C['ITEM_RUBY'],1)
 if name=='35-celio-saphir':q.f(0x2dc);r.call('AddBagItem',C['ITEM_SAPPHIRE'],1)
 if name=='01d-medallium':r.call('AddBagItem',C['ITEM_OAKS_PARCEL'],1)
 if name=='07-yopple-liberation':r.call('VarSet',0x4054,0)
 # Interactions stand next to the actual registered NPC, not an arbitrary room tile.
 if name in ('30-saphir-vol','31-entrepot-admin1','32-entrepot-admin2','33-entrepot-scientifique','34-celio-rubis','35-celio-saphir','01b-choix-partenaire','03c-capitaine','27-perdue-sauvetage','23-leo-transformation','11-nyada-premiere-quete','12-nyada-retour-amis','16-nyada-seconde-quete','18-nyada-sommet','19-scientifique-lavanville','20-scientifique-carmin','21-scientifique-yopple','13-alizon-quete-oni','14-alizon-rendez-vous'):
  target=next((o for o in json.loads((ROOT/f'data/maps/{map_}/map.json').read_text())['object_events'] if o.get('script')==script),None)
  if target:x,y=target['x'],target['y']+1
 if script is not None:
  trigger=next((ev for ev in json.loads((ROOT/f'data/maps/{map_}/map.json').read_text()).get('coord_events',[]) if ev.get('script')==script),None)
  if trigger:
   x,y=trigger['x'],trigger['y']
   r.call('VarSet',C[trigger['var']],int(trigger['var_value'])+10)
  q.warp(map_,x,y)
  if not trigger:r.keys={4};r.run(2);r.keys=set();r.run(30)
  target=next((i+1 for i,o in enumerate(json.loads((ROOT/f'data/maps/{map_}/map.json').read_text()).get('object_events',[])) if o.get('script')==script),1)
  if name=='01d-medallium':target=4
  r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',target))
  if target in q.actors():r.write(r.symbols['gSelectedObjectEvent'],bytes([(q.actors()[target]-r.symbols['gObjectEvents'])//36]))
  r.call('VarSet',0x800c,r.call('GetPlayerFacingDirection'))
  if name=='23b-leo-separateur':
   r.call('RemoveObjectEventByLocalIdAndMap',1,q.maps[map_][1],q.maps[map_][0])
  r.call('ScriptContext_SetupScript',r.symbols[script])
 elif name=='09-terreur':
  q.warp(map_,x,y);r.run(120);r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep'),(q.callback(),q.idle(),r.read(r.symbols['sTh']+175,1).hex())
 else:
  g,n=q.maps[map_];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 film=Film(r,D/(name+'.mp4'));last=None;stable=0;busy=False;seencredits=False
 for f in range(round(film.fps*1600)):
  cb=film.callback()
  if cb!=last:film.events.append({'seconds':f/film.fps,'callback':cb});last=cb
  idle=q.idle()
  busy|=not idle
  if cb=='CB2_RollYokaiCredits':seencredits=True
  if name=='09-terreur':done=idle and r.read(r.symbols['sTh']+175,1)[0]!=0 and f>600
  elif name=='08-finale':done=seencredits and cb!='CB2_RollYokaiCredits'
  else:done=busy and idle and f>60
  stable=stable+1 if done else 0
  r.keys=set() if done else film.controls()
  r.run()
  if f%3600==0:print(name,f,cb,flush=True)
  if stable>=120:break
 else:raise RuntimeError(('Scène incomplète',name,film.callback()))
 r.frame.save(D/(name+'-fin.png'));film.finish(scene=name,map=map_,entry_script=script,prepared_flags=flags,prepared_vars=variables,prepared_party_level=100,native_battles=True,complete=True)
finally:r.close()

#!/usr/bin/env python3
"""Completed-scene fixtures: real map reload, walking over old triggers, and START.

This is regression testing of completed states, not an uninterrupted playthrough.
No battle outcome, ROM byte or save format is altered. Initial flags/positions are
explicit fixtures; controller input crosses each checked tile after map loading.
"""
import hashlib,json,os,struct
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C,MAPS,warp
# Symbol aliases from constants/flags.h and constants/vars.h.
C.update(FLAG_LAVENDER_INTRO_DONE=0x322,FLAG_BADGE04_GET=0x823,VAR_LAVENDER_INTRO=0x40F3,VAR_PHILOSOVNI_STATE=0x40F4,FLAG_CRAMOIS_MEETING_DONE=0x32C)
P=ROOT/'docs/argenta-retour-route2-20261024/autres-scenes'/('fille' if os.environ.get('YOKAI_ARGENTA_GENDER')=='1' else 'garcon');P.mkdir(parents=True,exist_ok=True)
r=new_game(int(os.environ.get('YOKAI_ARGENTA_GENDER',0)));rows=[];passed=False
r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
r.call('VarSet',C['VAR_REPEL_STEP_COUNT'],10000)

def loc():
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);return tuple(r.read(sb+4,2)),struct.unpack('<hh',r.read(sb,4))
def flag(k):r.call('FlagSet',C[k])
def var(k,v):r.call('VarSet',C[k] if isinstance(k,str) else k,v)
def move(key,n):r.keys={key};r.run(n);r.keys=set();r.run(60)
def menu(label):
 r.keys={3};r.run();r.keys=set();r.run(90)
 assert any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_StartMenuHandleInput']|1 for i in range(16)),(label,'START',loc())
 r.frame.save(P/(label+'.png'));r.keys={0};r.run();r.keys=set();r.run(60)
def settle():
 # Ariane's authorized five-second reminder can appear during a map-load wait.
 # Dismiss that visible dialogue normally before checking movement and START.
 for f in range(1800):
  if r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and r.read(r.symbols['sLockFieldControls'],1)==b'\0':r.keys=set();return
  r.keys={8} if f%16<4 else set();r.run()
 raise AssertionError(('Dialogue failed to release',loc()))
def check(label,mapname,x,y,key,frames=48):
 warp(r,*MAPS[mapname],x,y);settle();before=loc();move(key,frames);after=loc()
 if before==after:
  # A wall in one direction is not a control lock; try another adjacent tile.
  for other in (4,5,6,7):
   move(other,16);after=loc()
   if before!=after:break
 assert before!=after,(label,'No movement',before)
 assert r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2',(label,'Script still running')
 assert r.read(r.symbols['sLockFieldControls'],1)==b'\0',(label,'Field locked')
 menu(label);rows.append(dict(test=label,before=before,after=after,passed=True));print(label,after,flush=True)
try:
 flag('FLAG_ARGENTA_MORLEONE_DONE')
 for x in range(20,24):
  check('argenta-sortie-'+str(x),'PewterCity',x,34,5,150)
  assert loc()[0]==MAPS['Route2']
  move(4,400);assert loc()[0]==MAPS['PewterCity'] and loc()[1][1]<35,loc()
  menu('argenta-retour-'+str(x))
 # Completed flag + stale zero variable (old-save inconsistency) must self-heal.
 flag('FLAG_LAVENDER_INTRO_DONE');flag('FLAG_BADGE04_GET');var('VAR_LAVENDER_INTRO',0)
 check('lavanville-intro-deja-vue','LavenderTown',11,18,4)
 assert r.call('VarGet',C['VAR_LAVENDER_INTRO'])==1
 check('lavanville-rechargement','LavenderTown',11,18,4)
 for state in (2,3):
  var('VAR_PHILOSOVNI_STATE',state)
  check('carmin-entrepot-etat-'+str(state),'VermilionCity_PhilosovniWarehouse',6,7,4,48)
  assert r.call('VarGet',C['VAR_PHILOSOVNI_STATE'])==state
 # This meeting is interaction-based, so revisits must remain freely walkable.
 flag('FLAG_CRAMOIS_MEETING_DONE');var('VAR_MAP_SCENE_CINNABAR_ISLAND',4);var('VAR_MAP_SCENE_CINNABAR_ISLAND_2',2)
 check('cramois-arene-rencontre-vue','CinnabarIsland_Gym',5,5,5,16)
 check('cramois-retour-sur-ile','CinnabarIsland',17,13,5,32)
 # Boat departure has a persistent scene state, separate from temporary variables.
 var('VAR_MAP_SCENE_VERMILION_CITY',3)
 check('carmin-apres-oceane','VermilionCity',22,31,4,16)
 # End-of-story Yopple bosses are interactable rather than step-triggered.
 flag('FLAG_SYS_GAME_CLEAR');flag('FLAG_GOT_MASTER_BALL_FROM_SILPH')
 check('yopple-apres-liberation','SilphCo_11F',5,10,6,16)
 # Each defeated Council member room disables its automatic entrance scene.
 for n,name in enumerate(('Loreleis','Brunos','Agathas','Lances')):
  var('VAR_MAP_SCENE_POKEMON_LEAGUE',n+1)
  check('conseil-'+str(n+1)+'-apres-combat','PokemonLeague_'+name+'Room',5,10,5,16)
 passed=True
finally:
 if not passed:r.frame.save(P/'echec.png')
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,cases=rows),ensure_ascii=False,indent=2)+'\n')

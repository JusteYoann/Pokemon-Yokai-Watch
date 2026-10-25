#!/usr/bin/env python3
"""Fixtures mGBA: tirage d’entrée, délai persistant, priorité réelle sur Iris, sauvegarde/Continuer."""
import hashlib,json,os,struct
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs'/os.environ.get('TH_TEST_DIR','terre-heure-progressive-20261025');P.mkdir(parents=True,exist_ok=True)
r=new_game();checks=[];th=r.symbols['sTh'];party=r.symbols['gPlayerParty']
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
def passed(s):checks.append(s);print('PASS',s,flush=True)
def var(n):return r.call('VarGet',n)
def setvar(n,v):r.call('VarSet',n,v)
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def unlocked():return field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0'
def warp(n,x,y):
 g,m=maps[n];r.call('SetWarpDestination',g,m,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
def held(slot,item):r.w32(r.symbols['gStringVar4'],item);r.call('SetMonData',party+slot*100,12,r.symbols['gStringVar4'])
def wait(cond,n=12000,keys=True):
 for f in range(n):
  if cond():r.keys=set();return
  if keys:r.keys={8} if f%100<2 else set()
  r.run()
 raise AssertionError(('Timeout',list(r.read(th+175,17)),hex(r.u32(r.symbols['gMain']+4))))
def pulse(key,n=30):r.keys={key};r.run(2);r.keys=set();r.run(n)
def actor(local):
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i
  if r.read(p,1)[0]&1 and r.read(p+8,1)[0]==local:return p
 return None
def approaching():
 return any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_RunTrainerSeeFuncList']|1 for i in range(16))
def prime(steps):setvar(0x40fa,0x101);setvar(0x40fb,steps)
try:
 for i in range(2):r.call('CreateMon',party+100*i,1+i,50,31,1,12345+i,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\2');r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96)
 setvar(0x40fa,0x101);warp('MtMoon_1F',24,28);base=r.snapshot()
 assert r.call('TerreHeureEncounterChance')==5
 held(0,53);assert r.call('TerreHeureEncounterChance')==15
 held(1,53);assert r.call('TerreHeureEncounterChance')==15
 r.call('FlagSet',0x82c);assert r.call('TerreHeureEncounterChance')==30
 held(0,0);held(1,0);assert r.call('TerreHeureEncounterChance')==10
 passed('Taux natifs exacts 5/15 % aventure et 10/30 % postgame; plusieurs Shorts ne se cumulent pas')
 outcomes={}
 for seed in range(1,200):
  r.restore(base);setvar(0x40fa,0);setvar(0x40fb,0);r.call('SeedRng',seed);r.call('TerreHeureInputStep',False)
  pending=var(0x40fb);assert var(0x40fa)==0x101
  if pending:assert 30<=pending<=150;outcomes['success']=r.snapshot()
  else:outcomes['failure']=r.snapshot()
  if len(outcomes)==2:break
 assert len(outcomes)==2
 passed('Tirage réussi et échec reproduits; un succès programme secrètement entre 30 et 150 pas')
 r.restore(outcomes['failure'])
 for i in range(160):r.call('TerreHeureInputStep',True);assert not r.call('TerreHeureTryStep')
 assert var(0x40fb)==0
 passed('Un échec reste consommé pendant toute la visite, même après 160 pas')
 r.restore(outcomes['success']);pending=var(0x40fb)
 for i in range(40):r.call('TerreHeureInputStep',False);assert not r.call('TerreHeureTryStep')
 assert var(0x40fb)==pending
 passed('Attendre immobile ne fait ni avancer le compteur ni relancer le tirage')
 for steps in (30,150):
  r.restore(base);prime(steps)
  for i in range(steps-1):r.call('TerreHeureInputStep',True);assert not r.call('TerreHeureTryStep')
  assert var(0x40fb)==1
  r.call('TerreHeureInputStep',True);assert var(0x40fb)==0x100;assert r.call('TerreHeureTryStep')
  assert r.read(th+175,1)==b'\1' and var(0x40fb)==0 and r.call('FlagGet',0x33e)
  passed(f'Déclenchement exactement au {steps}e pas natif; première rencontre enregistrée dès le début')
 r.restore(base);prime(73);warp('MtMoon_B1F',3,3);assert var(0x40fb)==73 and var(0x40fa)==0x101
 passed('Compteur de 73 pas conservé après changement d’étage du même massif')
 warp('Route4',18,6);assert var(0x40fb)==0 and var(0x40fa)==0
 warp('MtMoon_1F',24,28);assert var(0x40fa)==0x101
 passed('Sortie complète annule le compteur; nouvelle entrée réarme un unique tirage')
 r.restore(base);prime(0x100);warp('MtMoon_1F',5,6)
 assert var(0x40fb)==0x100 and not r.call('TerreHeureTryStep') and r.read(th+175,1)==b'\0'
 warp('MtMoon_1F',24,28);assert r.read(th+175,1)==b'\1'
 passed('Un seuil atteint sur un escalier attend la fin de la transition et se lance une seule fois sur terrain sûr')
 r.restore(base);prime(1);r.call('LockPlayerFieldControls');r.call('TerreHeureInputStep',True)
 assert var(0x40fb)==0x100 and not r.call('TerreHeureTryStep') and var(0x40fb)==0x100
 r.call('UnlockPlayerFieldControls');assert r.call('TerreHeureTryStep')
 passed('Seuil atteint sous verrouillage: attente persistante puis lancement unique lorsque le terrain est sûr')
 r.restore(base);setvar(0x40fa,0x102);warp('RockTunnel_1F',44,4);setvar(0x40fa,0);setvar(0x40fb,0);r.call('TerreHeureInputStep',False)
 assert 30<=var(0x40fb)<=150
 r.call('FlagSet',0x33e);assert r.call('TerreHeureEncounterChance')==5
 passed('Garantie après le début de l’aventure à la Grotte Sombre avant la première rencontre; pas de garantie systématique au Mont Sélénite')
 for name in ('DiglettsCave_NorthEntrance','DiglettsCave_B1F','DiglettsCave_SouthEntrance','MtEmber_SummitPath_3F'):
  r.restore(base);setvar(0x40fa,0);setvar(0x40fb,0x100);warp(name,3,4);assert r.read(th+175,1)==b'\0' and not r.call('TerreHeureTryStep')
 passed('Grotte Bakuku et petits étages de passage: aucun déclenchement')
 r.restore(base);setvar(0x40fa,0x105);r.call('FlagSet',0x32f);warp('CeruleanCave_1F',7,5);setvar(0x40fb,0x100)
 assert not r.call('TerreHeureTryStep') and r.read(th+175,1)==b'\0'
 passed('Grotte Azurée protégée tant que le marqueur réservé de quête Nyada est actif')
 # Actual controller step into Iris’s sight, with one step left for Terr’heure.
 r.restore(base);prime(2);warp('MtMoon_1F',19,28);prime(1);r.call('ClearTrainerFlag',121)
 iris=actor(1);assert iris
 r.keys={7}
 wait(lambda:r.read(th+175,1)==b'\1',240,False);r.keys=set()
 assert r.call('GetTrainerApproachDistance',iris)>0
 assert not approaching() and not r.call('GetTrainerFlagFromScriptPointer',r.symbols['MtMoon_1F_EventScript_Iris'])
 r.frame.save(P/'priorite-terreur-iris.png')
 passed('Vrai pas manette dans le regard d’Iris: Terr’heure prioritaire, aucune tâche d’approche ni dialogue de Dresseur créé')
 wait(lambda:unlocked() and r.read(th+176,1)==b'\2')
 r.call('ScriptContext_SetupScript',r.symbols['TerreHeure_EventScript_EscapeReturn'])
 wait(lambda:unlocked() and r.read(th+175,1)==b'\0');r.keys=set();r.run(180)
 assert unlocked() and not approaching() and actor(1) and not r.call('CheckForTrainersWantingBattle')
 assert not r.call('GetTrainerFlagFromScriptPointer',r.symbols['MtMoon_1F_EventScript_Iris'])
 passed('Retour normal pendant 180 frames: Iris restaurée et non vaincue, aucun dialogue ou combat fantôme')
 # Move away from her line, then enter it again normally.
 r.keys={6};r.run(16);r.keys=set();r.run(8);r.keys={7}
 wait(lambda:approaching() or r.read(r.symbols['sLockFieldControls'],1)==b'\1',240,False)
 r.keys=set();wait(lambda:r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1,6000)
 passed('Une rencontre normale ultérieure relance effectivement le combat d’Iris')
 # Save during a pending ordinary visit, and Continue through the real title menu.
 r.restore(base);prime(73);r.call('SaveMapView');r.call('SaveQuestLogData');assert r.call('TrySavingData',0,max_frames=3000)==1;r.run(180)
 r.lib.retro_reset();r.run(600);pulse(3,180)
 wait(lambda:unlocked() and tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==maps['MtMoon_1F'] and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3),18000)
 r.keys=set();r.run(60)
 assert var(0x40fa)==0x101 and var(0x40fb)==73
 passed('Sauvegarde native et Continuer: résultat de visite et compteur de 73 pas conservés sans nouveau tirage')
finally:
 (P/'TESTS_DECLENCHEMENT.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':checks},ensure_ascii=False,indent=2)+'\n');r.close()

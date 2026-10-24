#!/usr/bin/env python3
"""Combats réellement exécutés par mGBA, avec une équipe de test préparée.
Les dégâts, résultats, captures et retours terrain ne sont pas injectés.
"""
import os,hashlib,json,struct,subprocess
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/terre-heure-20261025'/os.environ.get('TH_MODE','public');P.mkdir(parents=True,exist_ok=True)
r=new_game();r.call('VarSet',0x40f9,1);checks=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
actions={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
party=r.symbols['gPlayerParty'];th=r.symbols['sTh']
def passed(s):checks.append(s);print('PASS',s,flush=True)
def warp(n,x,y):
 g,m=maps[n];r.call('SetWarpDestination',g,m,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def pulse(k,n=30):r.keys=set();r.run(4);r.keys={k};r.run(4);r.keys=set();r.run(n)
def wait(cond,n=24000):
 for f in range(n):
  if cond():r.keys=set();return
  r.keys={8} if f%20<2 else set();r.run()
 print('DEBUG',[(key,hex(r.u32(r.symbols[key]))) for key in ('gBattleMainFunc','gMain','gBattlerControllerFuncs','gBattleControllerExecFlags')],flush=True);r.frame.save(P/'echec-combat.png');raise AssertionError('Timeout: '+hex(r.u32(r.symbols['gMain']+4)))
def action():wait(lambda:r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in actions)
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
def fixture_party():
 r.call('ZeroPlayerPartyMons');r.call('CreateMon',party,150,100,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('SetMonMoveSlot',party,89,0)
 for i in range(1,4):r.call('SetMonMoveSlot',party,0,i)
 for fieldid in (57,58,59,60,61,62,63):
  r.w32(r.symbols['gStringVar4'],999);r.call('SetMonData',party,fieldid,r.symbols['gStringVar4'])
def actor(local):
 for i in range(16):
  p=r.symbols['gObjectEvents']+i*36;b=r.read(p,36)
  if b[0]&1 and b[8]==local:return i
 return None
try:
 fixture_party();base=r.snapshot()
 for tier in range(3):
  r.restore(base)
  for f in (0x335,0x336,0x337,0x33e):r.call('FlagClear',f)
  if tier>=1:r.call('FlagSet',0x335)
  if tier>=2:r.call('FlagSet',0x336)
  warp('MtMoon_1F',18,35)
  for i in range(16):r.call('TerreHeureTryStep')
  wait(lambda:field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0',6000)
  oni=actor(230);assert oni is not None
  r.call('ObjectEventClearHeldMovementIfActive',r.symbols['gObjectEvents']+36*oni)
  r.call('MoveObjectEventToMapCoords',r.symbols['gObjectEvents']+36*oni,25,41)
  r.run(5);action();shot('combat-oni-'+str(tier+1))
  if tier==0:
   clock_before=r.u32(th+156);r.run(120);assert r.u32(th+156)==clock_before;passed('Le chronomètre est suspendu pendant un vrai combat Oni')
  assert r.call('GetMonData',r.symbols['gEnemyParty'],11)==(59,85,60)[tier]
  assert r.call('GetMonData',r.symbols['gEnemyParty'],56)==(75,75,80)[tier]
  assert sum(bool(r.call('GetMonData',r.symbols['gEnemyParty']+100*j,11)) for j in range(6))==(1,2,4)[tier]
  wait(lambda:field() and r.call('FlagGet',0x335+tier),42000)
  wait(lambda:field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0',6000)
  assert not any(actor(x) is not None for x in (230,231,232));shot('oni-'+str(tier+1)+'-vaincu')
  passed(('Gargaros','Ogralos','Orqanos')[tier]+': vrai combat gagné, équipe et niveaux contrôlés, poursuivants retirés')
  if os.environ.get('TH_TIMER_ONLY'):raise SystemExit(0)
 # A real trainer surrender is a loss inside the Terr'heure, not a Center warp.
 r.restore(base);warp('MtMoon_1F',18,35)
 for i in range(16):r.call('TerreHeureTryStep')
 wait(lambda:field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0',6000)
 oni=actor(230);assert oni is not None
 r.call('ObjectEventClearHeldMovementIfActive',r.symbols['gObjectEvents']+36*oni)
 r.call('MoveObjectEventToMapCoords',r.symbols['gObjectEvents']+36*oni,25,41);action()
 pulse(7);pulse(5);pulse(8,300)
 assert r.u32(r.symbols['gBattlerControllerFuncs'])==r.symbols['HandleConfirmTrainerForfeit']|1
 pulse(4,20);pulse(8,90)
 wait(lambda:field() and r.read(th+175,1)==b'\0' and r.read(r.symbols['sLockFieldControls'],1)==b'\0',18000)
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\2' and not r.call('FlagGet',0x335)
 assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==maps['MtMoon_1F'];shot('oni-defaite-retour');passed('Abandon réel: défaite, retour dans la grotte, aucun palier Oni validé')
 # Static encounter: actual native KO then actual native capture after re-entry.
 r.restore(base);r.call('FlagSet',0x82c)
 for f in (0x335,0x336,0x337,0x33a):r.call('FlagSet',f)
 warp('MtEmber_Summit',9,7);pulse(4,20);pulse(8,30);action();shot('combat-gorgouille-80')
 assert r.call('GetMonData',r.symbols['gEnemyParty'],11)==65 and r.call('GetMonData',r.symbols['gEnemyParty'],56)==80
 wait(lambda:field() and actor(1) is None,24000);wait(lambda:field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0',6000)
 assert not r.call('FlagGet',0x33b);passed('Gorgouille niveau 80: vrai K.O. sans indicateur de capture')
 warp('MtEmber_Exterior',29,8);warp('MtEmber_Summit',9,7);assert actor(1) is not None;passed('Gorgouille réapparaît après un vrai K.O.')
 r.call('ClearBag');r.call('AddBagItem',1,2);pulse(4,20);pulse(8,30);action()
 pulse(7);pulse(8,180);pulse(7,180);pulse(7,180);pulse(8,60);pulse(8,90)
 for f in range(24000):
  if field() and r.call('FlagGet',0x33b):break
  ptr=r.u32(r.symbols['gBattlescriptCurrInstr']);nick=ptr and r.read(ptr,1)==b'\xf3'
  r.keys={0 if nick else 8} if f%20<2 else set();r.run()
 else:raise AssertionError('Capture réelle de Gorgouille non terminée')
 r.keys=set();wait(lambda:field() and r.read(r.symbols['sLockFieldControls'],1)==b'\0',6000);assert actor(1) is None and actor(7) is None
 assert r.call('GetMonData',party+100,11)==65;shot('gorgouille-capture');passed('Capture réelle: Gorgouille rejoint l’équipe et la quête se termine')
 warp('MtEmber_Exterior',29,8);warp('MtEmber_Summit',9,7);assert actor(1) is None and actor(7) is None;passed('Après capture et rechargement de zone: aucun doublon de rencontre')
 assert r.call('GetSetPokedexFlag',65,1);passed('Gorgouille capturé est enregistré dans le Médallium sans modifier sa numérotation')
 r.call('SaveMapView');r.call('SaveQuestLogData')
 assert r.call('TrySavingData',0,max_frames=3000)==1
 r.run(180)
 r.lib.retro_reset();r.run(600);pulse(3,180);shot('menu-continuer')
 for f in range(18000):
  if field() and tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==maps['MtEmber_Summit'] and r.read(r.symbols['sLockFieldControls'],1)==b'\0' and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3):break
  r.keys={8} if f%20<2 else set();r.run()
 else:raise AssertionError('Continuer après sauvegarde: terrain inaccessible')
 r.keys=set();r.run(60)
 shot('quete-apres-continuer')
 assert r.call('FlagGet',0x33b) and actor(1) is None and actor(7) is None;passed('Sauvegarde native puis Continuer: capture et fin de quête conservées, aucun blocage')

finally:
 (P/'TESTS_COMBATS_REELS.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':checks},ensure_ascii=False,indent=2)+'\n');r.close()

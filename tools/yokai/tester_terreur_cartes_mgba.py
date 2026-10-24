#!/usr/bin/env python3
"""Validation mGBA par carte, porte réelle, menus, minuterie, Flash et palettes.
Les déplacements entre cartes de la fixture utilisent les fonctions de warp
natives. Ils ne constituent pas un parcours naturel de toute l'aventure.
"""
import os,hashlib,json,struct
from collections import Counter
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/terre-heure-20261025'/os.environ.get('TH_MODE','public');P.mkdir(parents=True,exist_ok=True)
r=new_game();r.call('VarSet',0x40f9,1);checks=[];frames=[];white_seen=False
audit=json.loads((ROOT/'docs/terre-heure-20261025/AUDIT_GROTTES.json').read_text())['maps']
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
th=r.symbols['sTh'];sb=r.u32(r.symbols['gSaveBlock1Ptr'])
def passed(s):checks.append(s);print('PASS',s,flush=True)
def warp(n,x,y):
 g,m=maps[n];r.call('SetWarpDestination',g,m,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
def pulse(k,n=30):r.keys=set();r.run(4);r.keys={k};r.run(4);r.keys=set();r.run(n)
def wait(cond,n=6000,record=False):
 global white_seen
 for f in range(n):
  if cond():r.keys=set();return
  r.keys={8} if f%24<2 else set();r.run()
  if record and all(lo==hi and lo>=248 for lo,hi in r.frame.getextrema()):
   assert r.read(0x05000000,1024)==b'\xff\x7f'*512
   white_seen=True
  if record and f%6==0:frames.append(r.frame.copy().resize((720,480),Image.Resampling.NEAREST))
 raise AssertionError(('Timeout',hex(r.u32(r.symbols['gMain']+4)),list(r.read(th+175,17))))
def unlocked():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sLockFieldControls'],1)==b'\0'
def begin():
 for i in range(16):r.call('TerreHeureTryStep')
 assert r.call('TerreHeureActive');wait(lambda:unlocked() and r.read(th+176,1)==b'\2')
def actor(local):
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1 and b[8]==local:return i
 return None
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],150,100,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 r.write(sb+0xee0+0x500//8,b'\xff'*96);base=r.snapshot()
 for row in audit:
  if not row['candidates']:continue
  r.restore(base);counts=Counter(p[2] for p in row['candidates']);co=counts.most_common(1)[0][0];x,y,_=next(p for p in row['candidates'] if p[2]==co);warp(row['map'],x,y)
  for x,y,c in row['candidates']:
   assert not r.call('MapGridGetCollisionAt',x+7,y+7),(row['map'],x,y)
  passed(row['map']+': emplacements prévalidés compatibles avec les collisions natives')
  if row['pursuers']:
   r.call('VarSet',0x40f9,next(i+1 for i,prefix in enumerate(('MtMoon','RockTunnel','SeafoamIslands','VictoryRoad','CeruleanCave','MtEmber')) if row['map'].startswith(prefix)))
   begin();assert r.read(0x05000200,512)==r.read(r.symbols['gPlttBufferFaded']+512,512),'Une palette de sprite est teintée'
   assert not r.call('TryStandardWildEncounter',0);passed(row['map']+': événement, couleurs des sprites et blocage des rencontres sauvages')
 # Native door interaction and timer in menus.
 r.restore(base);warp('MtMoon_1F',18,35);begin();event=r.snapshot()
 assert r.read(th+175,2)==b'\1\2'
 door_map,point=r.read(th+179,2);row=audit[door_map];x,y,_=row['candidates'][point]
 other='MtMoon_B1F' if row['map']!='MtMoon_B1F' else 'MtMoon_1F';warp(other,3,3)
 warp(row['map'],x,y+1);assert actor(233) is not None;shot('porte-terreur-placee')
 pulse(4,10);pulse(8,10)
 wait(lambda:r.read(th+175,1)==b'\0' and unlocked(),6000,True)
 assert white_seen,'Le fondu n’a jamais atteint le blanc complet'
 assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==maps['MtMoon_1F'];assert r.call('CanUseEscapeRopeOnCurrMap');shot('porte-sortie-reussie');passed('Interaction A: porte coulissante, fondu, retour au point d’origine et commandes libérées')
 # Menu stays usable but cannot stop time or offer Save.
 r.restore(event);remaining=r.u32(th+156);pulse(3,120);shot('menu-sans-sauvegarde')
 order=r.read(r.symbols['sStartMenuOrder'],8);count=r.read(r.symbols['sNumStartMenuItems'],1)[0]
 assert 4 not in order[:count],(order,count) # STARTMENU_SAVE=4
 r.run(120);assert r.u32(th+156)<remaining-100;passed('Le menu continue de décompter et ne propose pas Sauvegarder')
 r.w32(th+156,2);r.run(20);assert r.u32(th+156)==0
 pulse(0,120);wait(lambda:r.read(th+175,1)==b'\0' and unlocked());shot('expiration-retour');passed('Temps épuisé dans le menu: échec imposé dès le retour au terrain, sans blocage')
 # Native Flash register restoration on a dark floor.
 r.restore(base);warp('RockTunnel_1F',17,4);before=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x30,1);assert before!=b'\0';r.call('VarSet',0x40f9,2);begin();assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x30,1)==b'\0';shot('grotte-sombre-eclairee')
 r.call('ScriptContext_SetupScript',r.symbols['TerreHeure_EventScript_Failure']);r.call('LockPlayerFieldControls');wait(lambda:r.read(th+175,1)==b'\0' and unlocked());assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x30,1)==before;shot('obscurite-restauree');passed('Flash absent: visibilité complète pendant l’événement, obscurité initiale restaurée à la sortie')
finally:
 (P/'TESTS_CARTES_PORTE.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':checks},ensure_ascii=False,indent=2)+'\n')
 if frames:frames[0].save(P/'porte-sortie-mgba-x3.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
 r.close()

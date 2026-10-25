#!/usr/bin/env python3
"""Régressions natives: Nathan immobile, matérialisation, garde de porte, collisions et alerte."""
import hashlib,json,re,struct
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-nathan-patrouilles-20261025';P.mkdir(parents=True,exist_ok=True)
r=new_game();th=r.symbols['sTh'];checks=[]
def passed(s):checks.append(s);print('PASS',s,flush=True)
def phase():return r.read(th+176,1)[0]
def actors():
 return {r.read(r.symbols['gObjectEvents']+36*i+8,1)[0]:r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1}
def sprite(obj):return r.symbols['gSprites']+68*r.read(obj+4,1)[0]
def tiledata(obj,size=256):return r.read(0x06010000+(int.from_bytes(r.read(sprite(obj)+4,2),'little')&1023)*32,size)
def pos(obj):return struct.unpack('<hh',r.read(obj+16,4))
def unlocked():return r.read(r.symbols['sLockFieldControls'],1)==b'\0'
def wait(cond,limit=9000):
 for f in range(limit):
  if cond():r.keys=set();return
  r.keys={8} if f%100<2 else set();r.run()
 raise AssertionError(('Timeout',phase()))
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96);r.call('VarSet',0x40fa,0x101)
 g=json.loads((ROOT/'data/maps/map_groups.json').read_text());group=g['group_order'].index('gMapGroup_Dungeons');num=g['gMapGroup_Dungeons'].index('MtMoon_1F')
 r.call('SetWarpDestination',group,num,255,20,27);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
 player=actors()[255];reference=tiledata(player);assert any(reference)
 flagtext=(ROOT/'include/constants/flags.h').read_text();map_objects=json.loads((ROOT/'data/maps/MtMoon_1F/map.json').read_text())['object_events']
 itemflags=[int(re.search(r'^#define\s+'+o['flag']+r'\s+(0x[0-9A-Fa-f]+)',flagtext,re.M)[1],16) for o in map_objects if o['graphics_id']=='OBJ_EVENT_GFX_ITEM_BALL']
 flags_before={f:r.call('FlagGet',f) for f in itemflags}
 r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep')
 wait(lambda:phase()==1);r.keys=set();r.run(80)
 npc=actors()[1];old=r.read(npc+4,1)
 # Reproduce the transient native spawn binding: a resident aliases sprite 0.
 r.write(npc+4,r.read(player+4,1));r.call('TerreHeureFadeResidents');r.write(npc+4,old)
 assert tiledata(player)==reference
 passed('Un objet transitoire pointant vers le sprite de Nathan ne peut plus effacer ses tuiles')
 samples=[]
 for f in range(1000):
  r.keys=set();r.run();assert tiledata(player)==reference,('Nathan effacé',phase(),f)
  if phase()==7:
   patrols=[p for local,p in actors().items() if local in (231,232,236,237,238,239,240,241)]
   samples.append(sum(sum(v!=0 for v in tiledata(p,512)) for p in patrols))
  if phase()==3:break
 else:raise AssertionError('Texte non atteint')
 assert len(set(samples))>=5 and samples[-1]>samples[0],samples
 passed('Patrouilles matérialisées progressivement avant le texte; Nathan conserve ses pixels pendant toute la transition')
 directions={r.read(p+24,1)[0]&15 for local,p in actors().items() if local in (231,232,236,237,238,239,240,241)}
 assert len(directions)>=3,directions
 passed('Orientations initiales variées: au moins trois directions différentes')
 for f in range(180):
  r.keys=set();r.run();assert tiledata(player)==reference
 assert not r.read(sprite(player)+62,1)[0]&4
 r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/'nathan-texte.png')
 passed('Nathan reste visible et intact pendant trois secondes de texte immobile, sans mouvement pour recharger son image')
 assert {f:r.call('FlagGet',f) for f in itemflags}==flags_before
 passed('La disparition temporaire des objets conserve leurs drapeaux: aucun objet original marqué comme ramassé')
 wait(lambda:phase()==2 and unlocked());r.keys=set();initial={local:pos(p) for local,p in actors().items() if local in (231,232,236,237,238,239,240,241)}
 moved=set();door=actors().get(233)
 for f in range(240):
  r.run();a=actors()
  for local,oldpos in initial.items():
   if local in a and pos(a[local])!=oldpos:moved.add(local)
   if local in a and door:
    x,y=pos(a[local]);dx,dy=pos(door);assert abs(x-dx)>2 or abs(y-dy)>2,(local,(x,y),(dx,dy))
 assert len(moved)>=3,moved
 passed(f'{len(moved)} patrouilles se déplacent réellement à vitesse de marche normale en quatre secondes')
 # Isolate native collision and detection on a straight free line in this fixture.
 wait(unlocked);r.call('LockPlayerFieldControls');a=actors();patrol=a[231]
 for local,p in a.items():
  if local in (230,231,232,236,237,238,239,240,241):r.call('ObjectEventClearHeldMovementIfActive',p)
 px,py=pos(player)
 r.call('MoveObjectEventToMapCoords',patrol,px,py-2);r.call('ObjectEventTurn',patrol,1)
 assert r.call('GetCollisionAtCoords',r.symbols['gObjectEvents']+(player-r.symbols['gObjectEvents']),px,py-2,2)!=0
 passed('Collision native du joueur avec la patrouille, comme avec un Dresseur')
 # Restore sight latch and a neutral AI tick, then let the real field loop react.
 r.write(th+162,b'\0\0');r.write(th+188,b'\1');r.call('UnlockPlayerFieldControls');r.keys=set()
 for f in range(60):
  r.run()
  if not unlocked():break
 else:raise AssertionError('Regard non détecté')
 start=r.u32(r.symbols['gMain']+0x24);origin=pos(player)
 for f in range(400):
  r.keys={6};r.run()
  if unlocked():break
  assert pos(player)==origin
 elapsed=r.u32(r.symbols['gMain']+0x24)-start;r.keys=set()
 assert 120<=elapsed<=150,elapsed
 passed(f'Regard détecté: cri de l’introduction via script natif, immobilisation de {elapsed} VBlanks malgré la manette')
 assert not r.call('SetUpFieldMove_Dig')
 passed('Tunnel et Corde Sortie refusés par leur validation native pendant la Terr’heure')
 # Validate the protected square on the actual door floor, with patrols active.
 graph=json.loads((P/'GRAPHE_DISTANCES.json').read_text())['maps'];audit=json.loads((ROOT/'docs/terre-heure-20261025/AUDIT_GROTTES.json').read_text())['maps']
 dm=r.read(th+179,1)[0];dx,dy=r.read(th+192,2);row=graph[dm]
 px,py=next((dx+ox,dy+oy) for ox,oy in ((0,3),(3,0),(0,-3),(-3,0)) if 0<=dx+ox<row['width'] and 0<=dy+oy<row['height'] and row['safe_labels'][(dy+oy)*row['width']+dx+ox])
 number=g['gMapGroup_Dungeons'].index(row['map']);r.call('SetWarpDestination',group,number,255,px,py);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1000):
  r.run()
  if r.read(th+178,1)[0]==dm and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and not r.read(r.symbols['gPaletteFade']+7,1)[0]&128 and 230 in actors():
   # Isolate patrol motion/white return from the boss encounter in this fixture.
   r.call('RemoveObjectEventByLocalIdAndMap',230,number,group);break
 assert 233 in actors();checked=0;white=0
 for f in range(240):
  r.keys=set();r.run()
  for local,p in actors().items():
   if local in (231,232,236,237,238,239,240,241):
    x,y=pos(p);assert abs(x-7-dx)>2 or abs(y-7-dy)>2;checked+=1
 assert checked>=240,checked
 passed(f'Périmètre carré de deux cases vérifié sur l’étage réel de la porte ({checked} contrôles), y compris pendant la marche')
 r.call('LockPlayerFieldControls');r.call('BeginNormalPaletteFade',0xffffffff,0,16,16,0x7fff);r.run(4)
 r.call('ScriptContext_SetupScript',r.symbols['TerreHeure_EventScript_EscapeReturn'])
 for f in range(3000):
  r.keys=set();r.run()
  if phase()==8:
   if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:assert r.read(0x05000000,416)==b'\xff\x7f'*208
   else:assert r.read(0x05000000,2)==b'\xff\x7f'
   white+=1
  if not r.read(th+175,1)[0] and unlocked() and phase()!=8:break
 else:raise AssertionError('Retour blanc non terminé')
 assert white>0,white
 passed(f'Retour par écran blanc maintenu sur {white} frames; aucune palette de l’ancien décor révélée')
 assert r.call('SetUpFieldMove_Dig')
 passed('Tunnel redevient utilisable après la sortie, sans modification de la sauvegarde')
 assert {f:r.call('FlagGet',f) for f in itemflags}==flags_before
 passed('Après retour: les objets originaux restent disponibles avec leurs drapeaux inchangés')

finally:
 (P/'TESTS_NATHAN_PATROUILLES.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'checks':checks},ensure_ascii=False,indent=2)+'\n');r.close()

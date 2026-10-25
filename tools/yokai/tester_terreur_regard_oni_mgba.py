#!/usr/bin/env python3
"""Fixtures natives ciblées: regard Oni, approche sous verrouillage et densité."""
import hashlib,json,struct
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-regard-oni-20261025';P.mkdir(parents=True,exist_ok=True)
r=new_game();th=r.symbols['sTh'];checks=[]
def passed(s):checks.append(s);print('PASS',s,flush=True)
def actors():return {r.read(r.symbols['gObjectEvents']+36*i+8,1)[0]:r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1}
def pos(o):return struct.unpack('<hh',r.read(o+16,4))
def unlocked():return r.read(r.symbols['sLockFieldControls'],1)==b'\0'
def wait(cond,limit=1800):
 for f in range(limit):
  if cond():r.keys=set();return
  r.keys={8} if f%60<2 else set();r.run()
 raise AssertionError(('Timeout',r.read(th+176,1)))
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96);r.call('VarSet',0x40fa,0x101)
 g=json.loads((ROOT/'data/maps/map_groups.json').read_text());group=g['group_order'].index('gMapGroup_Dungeons');num=g['gMapGroup_Dungeons'].index('MtMoon_1F')
 r.call('SetWarpDestination',group,num,255,20,27);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
 r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep');wait(lambda:r.read(th+176,1)==b'\3')
 r.keys=set();r.run(180);r.frame.resize((720,480)).save(P/'intro-nathan.png')
 wait(lambda:r.read(th+176,1)==b'\2' and unlocked());r.call('LockPlayerFieldControls')
 a=actors();player=a[255];oni=a[230]
 patrols=[o for local,o in a.items() if local in (231,232,236,237,238,239,240,241)]
 for o in patrols:
  x,y=pos(o);open_count=sum(not r.call('MapGridGetCollisionAt',x+dx,y+dy) for dx,dy in [(0,1),(0,-1),(-1,0),(1,0)])
  assert open_count>=3
 passed(f'{len(patrols)} patrouilles présentes; aucune ancrée dans un couloir à deux issues')
 for i,o in enumerate(patrols):
  assert all(abs(pos(o)[0]-pos(q)[0])+abs(pos(o)[1]-pos(q)[1])>=3 for q in patrols[i+1:])
 passed('Patrouilles espacées, même après leurs premiers mouvements')
 for local,o in a.items():
  if local in (231,232,236,237,238,239,240,241):r.call('RemoveObjectEventByLocalIdAndMap',local,num,group)
 r.call('ObjectEventClearHeldMovementIfActive',oni)
 # Find an unobstructed six-cell line for the exact native sight experiment.
 row=next((x,y) for y in range(7,40) for x in range(7,30) if all(not r.call('MapGridGetCollisionAt',x,y+i) for i in range(7)))
 x,y=row;r.call('MoveObjectEventToMapCoords',player,x,y+6);r.call('MoveObjectEventToMapCoords',oni,x,y);r.call('ObjectEventTurn',oni,1)
 r.write(th+160,b'\0\0');r.write(th+162,b'\0\0');r.write(th+186,b'\0');r.write(th+187,b'\0');r.write(th+188,b'\1')
 base=r.snapshot();r.call('UnlockPlayerFieldControls');r.keys=set()
 for f in range(30):
  r.run()
  if not unlocked():break
 else:raise AssertionError('Alerte Oni absente')
 assert r.read(th+162,2)==b'\0\1'
 passed('Regard Oni à six cases: même script de cri et immobilisation que les patrouilles')
 origin=pos(player);start=pos(oni);frames=0;moved=False
 for f in range(180):
  r.keys={6};r.run();frames+=1
  if unlocked():break
  assert pos(player)==origin
  moved|=pos(oni)!=start
 assert 120<=frames<=150,frames
 assert moved,(start,pos(oni))
 assert abs(pos(oni)[0]-start[0])+abs(pos(oni)[1]-start[1])<=2,(start,pos(oni))
 passed(f'Pendant {frames} VBlanks, Nathan reste immobile et l’Oni se rapproche réellement')
 r.keys=set();r.frame.resize((720,480)).save(P/'oni-approche.png')
 # Test immediate contact from all four sides with the native field routine.
 for dx,dy,label in [(0,-1,'derrière'),(-1,0,'gauche'),(1,0,'droite')]:
  r.restore(base);r.call('MoveObjectEventToMapCoords',oni,x,y+3);r.call('MoveObjectEventToMapCoords',player,x+dx,y+3+dy);r.call('ObjectEventTurn',oni,1)
  r.write(th+162,b'\0\0');r.write(th+187,b'\0');r.call('UnlockPlayerFieldControls');r.call('Pursuers')
  assert unlocked(),label
  passed(f'Contact {label}: aucun combat immédiat hors de la case face à l’Oni')
 r.restore(base);r.call('MoveObjectEventToMapCoords',oni,x,y+3);r.call('MoveObjectEventToMapCoords',player,x,y+4);r.call('ObjectEventTurn',oni,1)
 # An already registered sight avoids a new alert and tests battle contact itself.
 r.write(th+162,b'\0\1');r.call('UnlockPlayerFieldControls');r.call('Pursuers');assert not unlocked()
 wait(lambda:r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1,2400)
 passed('Case immédiatement devant l’Oni: vrai combat lancé par le moteur natif')
 raw=r.read(r.symbols['TerreHeure_Text_Intro'],180)
 five=bytes([0xa6,0,0xc7,0xc3,0xc8,0xcf,0xce,0xbf,0xcd])
 assert five in raw,raw
 passed('Texte compilé de l’introduction: 5 MINUTES')
 r.restore(base)
 # Narrow-area fixture selected from the actual map's foot-traversable mask.
 graph=json.loads((ROOT/'docs/terre-heure-nathan-patrouilles-20261025/GRAPHE_DISTANCES.json').read_text())['maps']
 row=next(m for m in graph if m['map']=='MtMoon_1F');w=row['width'];h=row['height'];labels=row['safe_labels']
 def ground(x,y):return 0<=x<w and 0<=y<h and bool(labels[y*w+x])
 def exits(x,y):return sum(ground(x+dx,y+dy) for dx,dy in [(0,1),(0,-1),(-1,0),(1,0)])
 candidates=[]
 for cy in range(h):
  for cx in range(w):
   if ground(cx,cy) and exits(cx,cy)==2:
    roomy=sum(ground(xx,yy) and exits(xx,yy)>=3 for yy in range(cy-5,cy+6) for xx in range(cx-7,cx+8))
    if 4<=roomy<=72:candidates.append((roomy,cx,cy))
 assert candidates
 _,cx,cy=min(candidates);r.call('MoveObjectEventToMapCoords',player,cx+7,cy+7);r.call('MaintainPatrols',1)
 guards=[o for local,o in actors().items() if local in (231,232,236,237,238,239,240,241)]
 assert len(guards)<=2,len(guards)
 passed(f'Passage étroit réel du Mont Sélénite ({cx},{cy}): seulement {len(guards)} patrouille(s)')
 # The movement loop must not take a guard into a two-exit corridor.
 for frame in range(180):
  r.write(th+162,b'\xff\x01');r.call('Pursuers');r.run()
  for local,o in actors().items():
   if local in (231,232,236,237,238,239,240,241):
    xx,yy=pos(o);assert sum(not r.call('MapGridGetCollisionAt',xx+dx,yy+dy) for dx,dy in [(0,1),(0,-1),(-1,0),(1,0)])>=3
 passed('Les patrouilles ne pénètrent pas dans les couloirs à deux issues pendant leurs déplacements')
 counts=[];paces=[]
 for tier,name in enumerate(('Gargaros','Ogralos','Orqanos')):
  r.restore(base);r.write(th+182,bytes([tier]));r.call('SeedRng',1);r.call('Populate')
  guards={local:o for local,o in actors().items() if local in (231,232,236,237,238,239,240,241)}
  assert len(guards)<=1+tier;counts.append(len(guards))
  r.call('RemoveObjectEventByLocalIdAndMap',230,num,group)
  r.write(th+160,struct.pack('<H',1000));r.write(th+162,b'\xff\x01')
  old={k:pos(v) for k,v in guards.items()};moves={k:0 for k in guards}
  for frame in range(240):
   r.call('Pursuers');r.run()
   for local,o in guards.items():
    now=pos(o)
    if now!=old[local]:moves[local]+=abs(now[0]-old[local][0])+abs(now[1]-old[local][1]);old[local]=now
  paces.append(moves)
  passed(f'{name}: {len(guards)} patrouille(s), plafond {1+tier}, déplacements natifs mesurés sur 240 cycles de contrôle: {moves}')
 assert counts==sorted(counts),counts
 passed('La densité augmente progressivement de Gargaros vers Orqanos')
 # Consecutive gaze entries cannot chain immobilisations immediately.
 r.restore(base);r.call('UnlockPlayerFieldControls');r.write(th+160,struct.pack('<H',30));r.write(th+162,b'\0\0');r.call('Pursuers')
 assert unlocked() and int.from_bytes(r.read(th+160,2),'little')==29
 passed('Délai de reprise: un nouveau regard ne réimmobilise pas Nathan pendant la période de protection')
 for tier,name in enumerate(('Gargaros','Ogralos','Orqanos')):
  r.restore(base);r.write(th+182,bytes([tier]));r.call('MoveObjectEventToMapCoords',oni,x,y+4);r.call('ObjectEventTurn',oni,1)
  r.write(th+160,b'\0\0');r.write(th+162,b'\0\0');r.call('UnlockPlayerFieldControls');r.call('Pursuers');assert not unlocked()
  for frame in range(180):
   r.keys={7};r.run()
   if unlocked():break
   assert abs(pos(oni)[0]-pos(player)[0])+abs(pos(oni)[1]-pos(player)[1])>=2
  else:raise AssertionError('Immobilisation non terminée')
  r.keys=set()
  passed(f'{name}: alerte à deux cases, commandes rendues sans contact imposé pendant le verrouillage')
 r.restore(base);r.call('Populate');a=actors();player=a[255];oni=a[230]
 def pixels(o):
  sp=r.symbols['gSprites']+68*r.read(o+4,1)[0];tile=int.from_bytes(r.read(sp+4,2),'little')&1023
  return r.read(0x06010000+tile*32,256)
 r.call('MoveObjectEventToMapCoords',oni,27,34);r.run(4)
 sp=r.symbols['gSprites']+68*r.read(oni+4,1)[0]
 reference=pixels(player);before=pixels(oni);assert any(before)
 r.write(r.symbols['gBattleOutcome'],b'\1');r.call('TerreHeureBattleResult');assert r.read(th+176,1)==b'\x0a'
 assert 230 in actors();samples=[];images=[]
 for f in range(70):
  r.keys=set();r.run();assert pixels(player)==reference
  if r.read(th+176,1)==b'\x0a':samples.append(sum(v!=0 for v in pixels(oni)))
  if f%5==0:images.append(r.frame.resize((720,480)))
 assert len(set(samples))>=5 and samples[0]>samples[-1],samples
 assert not any(local in actors() for local in (230,231,232,236,237,238,239,240,241))
 images[0].save(P/'fondu-victoire-mgba.gif',save_all=True,append_images=images[1:],duration=84,loop=0)
 passed('Victoire: Oni et patrouilles se dissolvent en 64 VBlanks avant retrait; Nathan conserve tous ses pixels')
finally:
 (P/'TESTS_REGARD_ONI.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':'Fixtures ciblées mGBA, pas un parcours complet.','checks':checks},ensure_ascii=False,indent=2)+'\n');r.close()

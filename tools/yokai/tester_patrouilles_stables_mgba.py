#!/usr/bin/env python3
"""Régressions natives de conservation et de repositionnement hors champ."""
import hashlib,json,struct
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-patrouilles-stables-20261025';P.mkdir(exist_ok=True)
r=new_game();th=r.symbols['sTh'];checks=[];locals_=(231,232,236,237,238,239,240,241)
def actors():return {r.read(r.symbols['gObjectEvents']+36*i+8,1)[0]:r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1}
def pos(o):return struct.unpack('<hh',r.read(o+16,4))
def passed(s):checks.append(s);print('PASS',s,flush=True)
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],150,85,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96)
 g=json.loads((ROOT/'data/maps/map_groups.json').read_text());group=g['group_order'].index('gMapGroup_Dungeons');num=g['gMapGroup_Dungeons'].index('MtMoon_1F')
 r.call('SetWarpDestination',group,num,255,20,27);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
 r.call('FlagSet',0x336);r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep')
 for f in range(2000):
  r.keys={8} if f%60<2 else set();r.run()
  if r.read(th+176,1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]:break
 else:raise AssertionError('Introduction non terminée')
 r.keys=set();r.call('LockPlayerFieldControls');base=r.snapshot();px,py=pos(actors()[255])
 # Every runtime patrol ID must survive native view culling, including extras.
 for local in locals_:
  r.restore(base);a=actors();o=a.get(local)
  if o is None:
   r.call('SpawnSpecialObjectEventParameterized',183,1,local,px+30,py,0)
   o=actors()[local]
  r.call('MoveObjectEventToMapCoords',o,px+30,py+30);r.write(o+12,struct.pack('<hh',px+30,py+30))
  r.call('RemoveObjectEventIfOutsideView',o);assert local in actors(),local
 passed('Les huit identifiants de patrouille survivent à la suppression native des objets hors champ')
 r.restore(base);pat=actors()[231];r.call('MoveObjectEventToMapCoords',pat,px+3,py);r.run(4)
 before=(pos(pat),r.read(pat+4,1),r.read(pat+12,4))
 for f in range(90):r.call('MaintainPatrols',0);r.run()
 assert (pos(pat),r.read(pat+4,1),r.read(pat+12,4))==before
 passed('Patrouille près du joueur conservée sur 90 vérifications, sans recréation ni téléportation')
 r.restore(base)
 for local in locals_:
  if local in actors():r.call('RemoveObjectEventByLocalIdAndMap',local,num,group)
 r.call('MaintainPatrols',0);guards={k:o for k,o in actors().items() if k in locals_};assert guards
 for local,o in guards.items():
  x,y=pos(o);assert abs(x-px)>9 or abs(y-py)>7,(local,(x,y),(px,py))
 passed(f'{len(guards)} nouvelles patrouilles placées entièrement au-delà du champ et de sa marge, jamais au bord visible')
 before={k:(pos(o),r.read(o+4,1),r.read(o+12,4)) for k,o in guards.items()}
 for f in range(90):r.call('MaintainPatrols',0);r.run()
 for k,o in guards.items():assert (pos(o),r.read(o+4,1),r.read(o+12,4))==before[k]
 passed('Les patrouilles nouvellement placées gardent leur ancrage hors champ et ne sont pas recyclées en boucle')
 assert r.read(th+182,1)==b'\2' and len(guards)<=3
 passed('Plafond de difficulté Orqanos conservé; aucune hausse de densité')
finally:
 (P/'TESTS.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':'Fixtures mGBA ciblées sur le retrait et le repositionnement, sans enregistrement vidéo.','checks':checks},ensure_ascii=False,indent=2)+'\n');r.close()

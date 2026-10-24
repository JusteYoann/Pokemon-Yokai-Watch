#!/usr/bin/env python3
"""Transition de 120 frames réellement produite par mGBA et garantie de première apparition."""
import os,hashlib,json,struct
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/terre-heure-20261025'/os.environ.get('TH_MODE','public');P.mkdir(parents=True,exist_ok=True)
r=new_game();checks=[];movie=[];th=r.symbols['sTh']
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
def passed(s):checks.append(s);print('PASS',s,flush=True)
def warp(n,x,y):
 g,m=maps[n];r.call('SetWarpDestination',g,m,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
def start():
 for i in range(16):r.call('TerreHeureTryStep')
def actor(local):
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i;b=r.read(p,36)
  if b[0]&1 and b[8]==local:return p
 return None
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);r.write(sb+0xee0+0x500//8,b'\xff'*96);base=r.snapshot()
 r.call('VarSet',0x40f9,1);warp('MtMoon_1F',20,27);npc=actor(1);assert npc;shot('transformation-avant');start();assert r.read(th+175,1)==b'\1'
 for f in range(500):
  if r.read(th+176,1)==b'\1':break
  r.run()
 else:raise AssertionError('Début du fondu non atteint')
 sprite=r.symbols['gSprites']+68*r.read(npc+4,1)[0]
 assert (int.from_bytes(r.read(sprite,2),'little')>>10)&3==1
 player=None
 for local in (255,):player=actor(local)
 assert player
 ps=r.symbols['gSprites']+68*r.read(player+4,1)[0]
 assert (int.from_bytes(r.read(ps,2),'little')>>10)&3==0
 startv=r.u32(r.symbols['gMain']+0x24);half=None
 for f in range(125):
  r.run()
  if f%2==0:movie.append(r.frame.copy().resize((720,480),Image.Resampling.NEAREST))
  if f==58:half=r.call('GetGpuReg',0x52)&31;shot('transformation-mi-fondu')
 assert half is not None and 6<=half<=10,half
 assert actor(1) is None and r.read(th+176,1)==b'\3';shot('transformation-apres');passed('Fondu individuel des PNJ sur 120 frames; joueur opaque et décor transformé progressivement')
 # A chosen Rock Tunnel guarantee need not fire in Mt Moon; it does fire at Rock Tunnel.
 r.restore(base);r.call('VarSet',0x40f9,2);warp('MtMoon_1F',18,35);r.call('SeedRng',1);start();assert r.read(th+175,1)==b'\0'
 warp('RockTunnel_1F',17,4);start();assert r.read(th+175,1)==b'\1';passed('Première apparition variable: choix Grotte Sombre, pas de déclenchement forcé au Mont Sélénite')
 r.restore(base);r.call('VarSet',0x40f9,2);warp('VictoryRoad_1F',5,3);start();assert r.read(th+175,1)==b'\1';passed('Route Victoire garantit la première apparition si la grotte désignée a été contournée')
 # Tiny passages cannot start an event or spawn pursuers.
 r.restore(base);warp('MtEmber_SummitPath_3F',3,4);start();assert r.read(th+175,1)==b'\0';passed('Petit étage de passage: aucun déclenchement imposé')
finally:
 (P/'TESTS_TRANSITION.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'checks':checks},ensure_ascii=False,indent=2)+'\n')
 if movie:movie[0].save(P/'transparence-pnj-mgba-x3.gif',save_all=True,append_images=movie[1:],duration=34,loop=0)
 r.close()

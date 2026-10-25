#!/usr/bin/env python3
"""Vérifie le bandeau natif et la position BG0 du chrono entre les étages."""
import hashlib,json,struct
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-chrono-fixe-20261025';P.mkdir(exist_ok=True)
r=new_game();th=r.symbols['sTh'];checks=[]
def passed(s):checks.append(s);print('PASS',s,flush=True)
def popup():return r.call('IsMapNamePopupTaskActive')
def wait(cond,limit=2400):
 for f in range(limit):
  if cond():r.keys=set();return
  r.keys={8} if f%60<2 else set();r.run()
 raise AssertionError(('Attente',r.read(th+176,1)))
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],150,85,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96)
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());group=groups['group_order'].index('gMapGroup_Dungeons');maps=groups['gMapGroup_Dungeons']
 def warp(name,x,y):
  r.call('SetWarpDestination',group,maps.index(name),255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 warp('RockTunnel_1F',44,4);r.run(240);r.call('FlagClear',0x4000);r.call('ShowMapNamePopup',0);assert popup()
 passed('Hors Terr’heure, le bandeau natif du nom de grotte apparaît normalement')
 r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep');wait(lambda:r.read(th+176,1)==b'\1');r.run(20)
 assert not popup() and r.call('GetGpuReg',0x12)==0
 passed('Le bandeau encore actif au début est fermé avant le chrono; décalage BG0 remis à zéro')
 wait(lambda:r.read(th+176,1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]);r.keys=set();r.call('LockPlayerFieldControls')
 samples=0
 for name,x,y in [('RockTunnel_B1F',38,28),('RockTunnel_1F',44,4),('RockTunnel_B1F',33,4),('RockTunnel_1F',3,4)]:
  warp(name,x,y)
  wait(lambda:field() and not r.read(r.symbols['gPaletteFade']+7,1)[0]&128 and r.read(th+189,1)!=b'\xff')
  r.call('LockPlayerFieldControls');r.keys=set();r.call('ShowMapNamePopup',0);assert not popup()
  for frame in range(180):
   r.run()
   if field():
    # Check hardware offset without RPC frames between adjacent samples.
    assert struct.unpack('<H',r.read(0x04000012,2))[0]==0,(name,frame)
    window=r.read(th+189,1)[0];assert window!=255
    assert r.read(r.symbols['gWindows']+window*12,3)==bytes([0,24,0]),(name,window)
    samples+=1
  assert not popup()
  r.frame.save(P/(name+f'-{x}-{y}.png'))
  passed(f'{name} ({x},{y}): aucun bandeau, chrono sans décalage sur 180 frames')
 assert r.read(th+175,1)==b'\1' and r.read(th+176,1)==b'\2'
 r.call('LockPlayerFieldControls');r.write(r.symbols['gSpecialVar_0x8004'],b'\1\0');r.call('TerreHeureEnd')
 wait(lambda:field() and r.read(th+175,1)==b'\0' and not r.read(r.symbols['gPaletteFade']+7,1)[0]&128)
 r.call('FlagClear',0x4000);r.call('ShowMapNamePopup',0);assert popup()
 passed('Après la Terr’heure, l’affichage normal des noms de lieux est rétabli')
 passed(f'{samples} contrôles du décalage matériel BG0 au cours de quatre changements d’étage')
finally:
 (P/'TESTS.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':'Fixtures mGBA avec transitions natives entre étages, sans vidéo.','checks':checks},ensure_ascii=False,indent=2)+'\n');r.close()

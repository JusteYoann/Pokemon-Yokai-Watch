#!/usr/bin/env python3
"""Défaites Oni préparées via le callback natif, batteries temporaires uniquement."""
import json,hashlib,struct
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/postgame-quetes-20261025';checks=[]
def test(nuz,pc):
 r=new_game(nuzlocke=nuz);rev={v|1:k for k,v in r.symbols.items()};th=r.symbols['sTh'];party=r.symbols['gPlayerParty']
 try:
  r.call('CreateMon',party,1,30,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('NuzlockeRecordOwned',party)
  r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96);r.call('SetLastHealLocationWarp',3);r.call('FlagSet',0x829)
  groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());g=groups['group_order'].index('gMapGroup_Dungeons');m=groups['gMapGroup_Dungeons'].index('MtMoon_1F')
  r.call('SetWarpDestination',g,m,255,20,27);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
  r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep')
  for frame in range(2400):
   r.keys={8} if frame%24<2 else set();r.run()
   if r.read(th+176,1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]:break
  r.keys=set();r.call('LockPlayerFieldControls')
  if pc:
   r.call('CreateBoxMon',r.call('GetBoxedMonPtr',0,0),4,35,31,1,6789,0,0)
  # Native callback observes a real losing outcome and a fainted party.
  r.write(party+86,b'\0\0');r.write(r.symbols['gBattleOutcome'],b'\2')
  r.call('CB2_EndTrainerBattle')
  assert r.read(th+175,1)==b'\0' and r.read(th+176,1)==b'\0'
  target='CB2_WaitGameOver' if nuz and not pc else 'CB2_Overworld'
  for frame in range(8000):
   callback=rev.get(r.u32(r.symbols['gMain']+4),'?')
   if callback==target and (target!='CB2_Overworld' or frame>180):break
   r.keys={8} if frame%60<2 and target!='CB2_WaitGameOver' else set();r.run()
  else:raise AssertionError((nuz,pc,callback))
  if target=='CB2_Overworld':
   loc=tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2));expected=next((i,groups[key].index('PewterCity_PokemonCenter_1F')) for i,key in enumerate(groups['group_order']) if 'PewterCity_PokemonCenter_1F' in groups[key]);assert loc==expected,(loc,expected)
   assert r.call('GetMonData',party,11,0)==(4 if nuz else 1)
   assert r.call('GetMonData',party,57,0)>0
   msg='Nuzlocke: équipe morte retirée, survivant du PC récupéré et retour au dernier Centre' if nuz else 'Normal: défaite Oni, fin de Terr’heure, retour au dernier Centre et soins classiques'
  else:msg='Nuzlocke: aucun survivant dans l’équipe ou au PC, game over natif et fin de Terr’heure'
  checks.append(msg);print('PASS',msg,flush=True);r.frame.save(P/('defaite-oni-'+('nuz-pc' if pc else 'nuz-game-over' if nuz else 'normal')+'.png'))
  return hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest()
 finally:r.close()
try:
 for nuz,pc in [(False,False),(True,True),(True,False)]:sha=test(nuz,pc)
finally:(P/'TESTS_DEFAITE_ONI.json').write_text(json.dumps({'rom_sha256':locals().get('sha'),'scope':__doc__,'checks':checks},ensure_ascii=False,indent=2)+'\n')

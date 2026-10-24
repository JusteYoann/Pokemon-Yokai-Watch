#!/usr/bin/env python3
"""Fixtures ciblées: IA réelle, tenue, fréquence, transactions et quête persistante."""
import os,hashlib,json,struct,subprocess
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-20261025'/os.environ.get('TH_MODE','public');P.mkdir(parents=True,exist_ok=True)
r=new_game();r.call('VarSet',0x40f9,1);checks=[];movie=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
th=r.symbols['sTh'];party=r.symbols['gPlayerParty'];sb=r.u32(r.symbols['gSaveBlock1Ptr'])
def passed(s):checks.append(s);print('PASS',s,flush=True)
def warp(n,x,y):
 g,m=maps[n];r.call('SetWarpDestination',g,m,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
def pulse(k,n=30):r.keys=set();r.run(4);r.keys={k};r.run(4);r.keys=set();r.run(n)
def unlocked():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sLockFieldControls'],1)==b'\0'
def wait(cond,n=6000):
 for f in range(n):
  if cond():r.keys=set();return
  r.keys={8} if f%24<2 else set();r.run()
 raise AssertionError(('Timeout',list(r.read(th+175,17))))
def begin():
 for i in range(16):r.call('TerreHeureTryStep')
 assert r.read(th+175,1)==b'\1';wait(lambda:unlocked() and r.read(th+176,1)==b'\2')
def obj(local):
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i;b=r.read(p,36)
  if b[0]&1 and b[8]==local:return p
 return None
def coords(p):return struct.unpack('<hh',r.read(p+16,4))
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
def script(n):r.call('ScriptContext_SetupScript',r.symbols[n]);r.call('LockPlayerFieldControls')
try:
 for i in range(2):r.call('CreateMon',party+100*i,150-i,100,31,1,12345+i,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\2');r.write(sb+0xee0+0x500//8,b'\xff'*96)
 base=r.snapshot();assert r.call('ItemId_GetImportance',53)==0
 r.call('GiveItemToMon',party,53);assert r.call('GetMonData',party,12)==53
 assert r.call('TryTakeMonItem',party)==2;assert not r.call('GetMonData',party,12);assert r.call('CheckBagHasItem',53,1);passed('Short Oni: équiper puis retirer via les fonctions natives de l’équipe et du SAC')
 # Same RNG seeds, no bonus stacking for two holders.
 r.restore(base);r.call('FlagSet',0x33e);warp('MtMoon_1F',18,35);chancebase=r.snapshot();samples=[]
 for holders in (0,1,2):
  outcomes=[]
  for seed in range(32):
   r.restore(chancebase)
   for slot in range(holders):r.call('GiveItemToMon',party+100*slot,53)
   r.call('SeedRng',seed)
   for i in range(16):r.call('TerreHeureTryStep')
   outcomes.append(r.read(th+175,1)==b'\1')
  samples.append(outcomes)
 assert sum(samples[1])>sum(samples[0]) and samples[1]==samples[2],list(map(sum,samples));passed('32 graines identiques: bonus sensible du Short Oni, deux porteurs sans cumul '+str(list(map(sum,samples))))
 r.restore(base);warp('MtMoon_1F',24,28);begin();event=r.snapshot()
 if os.environ.get('TH_MODE')=='prive':
  import ctypes as C,wave
  from mgba_rpc import BATCH
  class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
  class Timing(C.Structure):_fields_=[('fps',C.c_double),('rate',C.c_double)]
  class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
  av=AV();r.lib.retro_get_system_av_info(C.byref(av));audio=[]
  def batch(data,n):audio.append(C.string_at(data,n*4));return n
  recording=BATCH(batch);r.lib.retro_set_audio_sample_batch.argtypes=[BATCH];r.lib.retro_set_audio_sample_batch(recording)
  assert r.call('GetCurrentMapMusic')==350;r.run(480)
  with wave.open(str(P/'infinite-tunnel-mgba.wav'),'wb') as wav:
   wav.setnchannels(2);wav.setsampwidth(2);wav.setframerate(round(av.timing.rate));wav.writeframes(b''.join(audio))
  assert any(b''.join(audio));passed('Infinite Tunnel native: piste 350 active et sortie audio mGBA enregistrée')
  r.restore(event)
 oni=obj(230);patrol=obj(231);assert oni and patrol
 for p,x,y in [(oni,24,24),(patrol,24,26)]:
  assert not r.call('MapGridGetCollisionAt',x+7,y+7);r.call('ObjectEventClearHeldMovementIfActive',p);r.call('MoveObjectEventToMapCoords',p,x+7,y+7);r.call('ObjectEventSetHeldMovement',p,1)
 r.run(3);assert r.read(th+184,1)==b'\0'
 r.call('ObjectEventClearHeldMovementIfActive',patrol);r.call('ObjectEventSetHeldMovement',patrol,0);r.run(5)
 assert r.read(th+184,1)==b'\1';assert r.read(th+185,1)==b'\0';shot('alerte-patrouille');passed('Une patrouille de face donne l’alerte; l’Oni qui regarde ailleurs ne voit pas directement le joueur')
 before=coords(oni);positions=set();clock=r.read(th+188,1);skipped=0;measured=0
 for f in range(120):
  r.run()
  if unlocked():
   now=r.read(th+188,1);skipped+=now==clock;clock=now;measured+=1
  positions.add(coords(oni))
  if f%3==0:movie.append(r.frame.copy().resize((720,480),Image.Resampling.NEAREST))
 assert any(p!=before for p in positions);assert coords(patrol)==(31,33)
 for x,y in positions:assert not r.call('MapGridGetCollisionAt',x,y)
 assert skipped<=max(3,measured//20),(skipped,measured);passed('Poursuite réelle avec collisions, patrouille immobile; mises à jour terrain '+str(measured-skipped)+'/'+str(measured))
 # Full bag-menu round trip must keep the alert on the same floor.
 pulse(3,60);pulse(8,120);pulse(0,180);pulse(0,60)
 assert r.read(th+184,1)==b'\1';passed('L’alerte survit à l’ouverture et à la fermeture du SAC sur le même étage')
 warp('MtMoon_B1F',3,3);assert r.read(th+184,1)==b'\0';passed('Changement d’étage: alerte annulée')
 # Pickup stays in escrow and cannot be duplicated; normal ground-item sprite.
 r.restore(event);chest=obj(234);assert chest and r.read(chest+5,1)==b'\x5c'
 r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',234));r.call('TerreHeureReward');assert r.read(th+171,1)==b'\1' and not r.call('CheckBagHasItem',2,1)
 r.call('TerreHeureReward');assert r.read(th+171,1)==b'\1';passed('Poké Ball d’objet d’origine: récompense provisoire, double interaction sans duplication')
 picked=r.snapshot();script('TerreHeure_EventScript_Failure');wait(lambda:r.read(th+175,1)==b'\0' and unlocked());assert not r.call('CheckBagHasItem',2,1);passed('Échec: les récompenses provisoires sont perdues')
 r.restore(picked);script('TerreHeure_EventScript_EscapeReturn');wait(lambda:r.read(th+175,1)==b'\0' and unlocked());assert r.call('CheckBagHasItem',2,1);passed('Sortie réussie: récompense versée dans le SAC')
 r.restore(event);r.call('AddBagItem',2,999);r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',234));r.call('TerreHeureReward');assert obj(234) is not None and r.read(th+171,1)==b'\0';passed('Pile pleine: la Poké Ball reste au sol et ne perd pas son contenu')
 # Refusal, acceptance, award, victories already recorded, rendezvous.
 r.restore(base);r.call('FlagSet',0x82c);warp('PokemonTower_7F',11,5)
 script('Onis_EventScript_AlizonTour')
 def yesno():
  return any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_YesNoMenu_HandleInput']|1 for i in range(16))
 wait(yesno);r.run(10);pulse(0,90);wait(unlocked)
 assert not r.call('FlagGet',0x338) and not r.call('CheckBagHasItem',53,1);passed('Refuser la quête ne remet aucun Short et permet de revenir plus tard')
 for f in (0x335,0x336,0x337):r.call('FlagSet',f)
 script('Onis_EventScript_AlizonTour');wait(lambda:unlocked() and bool(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x33a//8,1)[0]&(1<<(0x33a%8))),9000)
 assert r.call('CheckBagHasItem',53,1);assert r.call('FlagGet',0x339);shot('alizon-rendezvous');passed('Quête postgame: Short remis, victoires antérieures reconnues, rendez-vous au Mont Braise')
finally:
 (P/'TESTS_PROGRESSION.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':checks},ensure_ascii=False,indent=2)+'\n')
 if movie:movie[0].save(P/'patrouille-poursuite-mgba-x3.gif',save_all=True,append_images=movie[1:],duration=50,loop=0)
 r.close()

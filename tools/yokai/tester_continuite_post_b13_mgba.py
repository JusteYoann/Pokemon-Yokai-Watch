#!/usr/bin/env python3
"""Native door/connection continuity with controller input, explicit warp fixtures."""
import hashlib,json,struct
from pathlib import Path
from mgba_rpc import Emulator,ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/POST_B13/audio';(P/'preuves').mkdir(parents=True,exist_ok=True)
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());MAPS={name:(i,j) for i,key in enumerate(groups['group_order']) for j,name in enumerate(groups[key])}

def location(r):return tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))
def warp(r,name,x,y):
 r.keys=set();g,n=MAPS[name];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 assert location(r)==(g,n)

def fixture():
 r=new_game()
 r.call('CreateMon',r.symbols['gPlayerParty'],1,20,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.call('FlagSet',0x828);r.call('FlagSet',0x829);r.call('VarSet',0x4050,3);r.call('VarSet',0x4055,9)
 return r

def transition(r,destination,key,label):
 expected=MAPS[destination];header=r.u32(r.symbols['gMPlayInfo_BGM']);last=r.u32(r.symbols['gMPlayInfo_BGM']+12);before=last;paused=0
 for f in range(1500):
  r.keys={key} if f<40 else set();r.run()
  assert r.u32(r.symbols['gMPlayInfo_BGM'])==header,(label,'song changed')
  clock=r.u32(r.symbols['gMPlayInfo_BGM']+12)
  assert clock>=last,(label,'sequence restarted',last,clock)
  assert r.u32(r.symbols['gSoundInfo'])==0x68736D53,(label,'mixer stopped')
  last=clock;paused+=bool(r.u32(r.symbols['gMPlayInfo_BGM']+4)&0x80000000)
  if f>100 and location(r)==expected and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError((label,'Door or connection not crossed',location(r),expected))
 r.keys=set();r.run(60);assert last>before,(label,'sequencer not advancing');assert not paused,(label,'BGM paused')
 r.frame.save(P/'preuves'/(label+'.png'))
 return {'test':label,'destination':destination,'controller_frames':f+1,'same_header':True,'sequence_clock_before':before,'sequence_clock_after':last,'clock_never_reset':True,'paused_frames':paused,'passed':True}

checks=[];r=fixture();passed=False
try:
 warp(r,'VermilionCity',15,7);checks.append(transition(r,'VermilionCity_PokemonCenter_1F',4,'carmin-centre-entree'))
 checks.append(transition(r,'VermilionCity',5,'carmin-centre-sortie'))
 # Find a real traversable eastern border tile shared with Route11.
 warp(r,'VermilionCity',47,19)
 checks.append(transition(r,'Route11',7,'carmin-route11-connexion'))
 warp(r,'PalletTown',16,14);checks.append(transition(r,'PalletTown_ProfessorOaksLab',4,'palette-labo-entree'))
 checks.append(transition(r,'PalletTown',5,'palette-labo-sortie'))
 warp(r,'PalletTown',12,0);checks.append(transition(r,'Route1',4,'palette-route1-connexion'))
 passed=True
finally:
 if not passed:r.frame.save(P/'preuves'/'continuite-diagnostic.png')
 report={'passed':passed,'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':'Real controller new game, then actual controller door/connection crossings after warp and progression fixtures, music header/monotonic sequencer clock/no pause; not whole-adventure travel, not a subjective listening pass','results':checks};r.close();(P/'CONTINUITE_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

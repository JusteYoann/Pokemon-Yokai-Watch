#!/usr/bin/env python3
"""Native mGBA maritime traversals. Only initial map/party/repel are fixtures.
Controller movement crosses real connections; screenshots/GIFs are emulator frames.
"""
import os,json,struct,hashlib,traceback
from collections import deque
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp,strong_party
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
D=ROOT/'docs/cramois-ile-passe/phase-b'/mode;D.mkdir(parents=True,exist_ok=True)
r=None;rows=[];movies={};passed=False;failure=None

def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def run(n,key=None,movie=None):
 r.keys=set() if key is None else {key}
 for i in range(n):
  r.run()
  if movie is not None and i%4==0:movie.append(r.frame.copy())
def pair():return tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))
def pos():
 i=r.read(r.symbols['gPlayerAvatar']+5,1)[0];o=r.read(r.symbols['gObjectEvents']+36*i,36)
 return tuple(x-7 for x in struct.unpack_from('<hh',o,16))
def amount():return int.from_bytes(r.read(r.symbols['sFog']+2,2),'little')
def fog_sprites():
 cb=r.symbols['FogSprite']|1
 return [i for i in range(64) if r.read(r.symbols['gSprites']+68*i+62,1)[0]&1 and r.u32(r.symbols['gSprites']+68*i+28)==cb]
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def free():return field() and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-x4.png'))
def stage(name,x,y):
 warp(r,*MAPS[name],x,y);r.call('VarSet',0x4020,250);run(8)
def travel(key,name,goal,movie,limit=10000):
 seen=[]
 for f in range(limit):
  if free():r.keys={key}
  elif r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:r.keys=battle_keys(r,f)
  else:r.keys={8} if f%16<4 else set()
  r.run()
  if f%4==0:movie.append(r.frame.copy())
  if f%8==0:seen.append(amount())
  if pair()==MAPS[name] and pos()==goal:
   run(24,movie=movie);return seen
 raise AssertionError(('travel blocked',pair(),pos(),name,goal,hex(r.u32(r.symbols['gMain']+4)),r.read(r.symbols['gPlayerAvatar'],12).hex(),r.read(r.symbols['sLockFieldControls'],1).hex(),r.read(r.symbols['sGlobalScriptContext'],16).hex(),r.call('GetCollisionFlagsAtCoords',r.symbols['gObjectEvents']+36*r.read(r.symbols['gPlayerAvatar']+5,1)[0],pos()[0]+6,pos()[1]+7,3)))
def clear(label):
 run(20);assert amount()==0 and not fog_sprites(),(label,amount(),fog_sprites());report(label)
def save_continue():
 assert free();r.call('SaveMapView');assert r.call('TrySavingData',0,max_frames=1500)==1;assert r.call('LoadGameSave',0,max_frames=1500)==1;r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(2500):
  r.run()
  if f>180 and free():break
 else:raise AssertionError('Continue blocked')
 run(20)
def native_effect(name,destination,limit=3000):
 r.keys=set();r.call(name)
 for f in range(limit):
  r.run()
  if f>180 and free() and pair()==MAPS[destination]:break
 else:raise AssertionError((name,'effect did not land',pair(),pos()))
 clear(name+' arrives without fog');shot(name.lower())
try:
 r=new_game();strong_party(r);r.call('VarSet',0x40f4,3)
 # Beat Melissa for real before filming her sea lane; her actor and game data remain native.
 stage('Route20',9,9)
 for i in range(16):
  o=r.read(r.symbols['gObjectEvents']+36*i,36)
  if o[0]&1 and o[8]==1:r.write(r.symbols['gSelectedObjectEvent'],bytes([i]));r.write(r.symbols['gSpecialVar_LastTalked'],b'\1\0');break
 r.call('ScriptContext_SetupScript',r.symbols['Route20_EventScript_Melissa'])
 for f in range(18000):
  r.keys=battle_keys(r,f) if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 else ({8} if f%16<4 else set());r.run()
  if f>60 and free():break
 else:raise AssertionError('Native Melissa battle did not finish')
 report('Actual Melissa victory before filming; no NPC removed or trainer flag forced')
 stage('Route20',20,9);assert r.read(r.symbols['gPlayerAvatar'],1)[0]&8;clear('Route20 open sea has no fog');shot('mer-avant-brume')
 movie=[];levels=travel(6,'Route20',(17,9),movie);shot('entree-brume')
 levels+=travel(6,'Route20',(10,9),movie);run(50,movie=movie);assert amount()==192 and len(fog_sprites())==15;shot('brume-dense')
 report('Route20 native Surf and gradual fog onset',levels=sorted(set(levels)),fog_sprites=len(fog_sprites()))
 levels+=travel(6,'Route20',(2,9),movie);shot('sortie-brume')
 levels+=travel(6,'CinnabarIsland',(23,9),movie);clear('Route20 arrival: zero fog on island');shot('arrivee-sepia');run(60,movie=movie);movies['arrivee-route20']=movie
 stage('CinnabarIsland',23,9);movie=[];run(40,movie=movie);levels=travel(7,'Route20',(20,9),movie);run(60,movie=movie);clear('Route20 departure: restored normal Kanto');shot('retour-kanto');movies['depart-route20']=movie;assert max(levels)>=176
 # Find a real water corridor around rocks and trainer sight lines; change no actors.
 width=24;tiles=struct.unpack('<1200H',(ROOT/'data/layouts/Route21_South/map.bin').read_bytes())
 raw=(ROOT/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(ROOT/'data/tilesets/secondary/cinnabar_island/metatile_attributes.bin').read_bytes()
 attrs=struct.unpack('<'+str(len(raw)//4)+'I',raw)
 def safe(x,y):
  if not (2<=x<=21 and 26<=y<=49) or (tiles[y*24+x]>>10)&3:return False
  if attrs[tiles[y*24+x]&1023]&511 not in [0x10,0x11,0x12,0x13,0x15,0x1a,0x1b,0x50,0x51,0x52,0x53]:return False
  return abs(x-10)+abs(y-29)>5 and abs(x-15)+abs(y-38)>4
 start=(18,26);goal=(16,49);q=deque([start]);prev={start:None}
 while q:
  at=q.popleft()
  if at==goal:break
  for dx,dy in [(0,1),(-1,0),(1,0),(0,-1)]:
   nxt=at[0]+dx,at[1]+dy
   if nxt not in prev and safe(*nxt):prev[nxt]=at;q.append(nxt)
 assert goal in prev
 path=[];at=goal
 while prev[at] is not None:path.append(at);at=prev[at]
 path.reverse()
 def follow(points,movie):
  for x,y in points:
   px,py=pos();key=7 if x>px else 6 if x<px else 5 if y>py else 4
   travel(key,'Route21_South',(x,y),movie)
 stage('Route21_South',*start);movie=[];follow(path,movie);shot('nord-sortie-brume')
 travel(5,'CinnabarIsland',(16,0),movie);clear('Route21 north arrival: zero fog on island');run(50,movie=movie);shot('nord-arrivee-sepia');movies['arrivee-route21']=movie
 stage('CinnabarIsland',16,0);movie=[];run(40,movie=movie)
 travel(4,'Route21_South',goal,movie);follow(list(reversed([start]+path[:-1])),movie)
 clear('Route21 departure: restored normal sea');run(40,movie=movie);movies['depart-route21']=movie
 # Reverse course before crossing either map connection, and repeat without resource growth.
 stage('Route20',20,9)
 for cycle in range(3):
  travel(6,'Route20',(10,9),[]);run(50);assert amount()==192 and len(fog_sprites())==15
  travel(7,'Route20',(20,9),[]);clear('Route20 U-turn/repeated pass '+str(cycle+1))
 report('Three U-turns preserve sprites and fully release temporary fog')
 stage('Route20',10,9);save_continue();assert amount()==192 and len(fog_sprites())==15;report('Native Save/Continue in dense maritime fog restores local effect')
 # A wild encounter begins in dense fog but the battle itself must be clear.
 r.call('CreateMon',r.symbols['gEnemyParty'],C['SPECIES_PIDGEY'],30,20,1,100,0,0);r.call('StartWildBattle')
 for f in range(3000):
  run(1)
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
 else:raise AssertionError('Sea encounter failed to start')
 assert not fog_sprites();run(120);shot('combat-mer-sans-brume')
 for f in range(15000):
  r.keys=battle_keys(r,f);r.run()
  if f>60 and free():break
 else:raise AssertionError('Sea encounter failed to finish')
 run(120);assert amount()==192 and len(fog_sprites())==15;report('Wild battle inside fog is clear; field return reconstructs dense fog')
 run(1,3);run(100);shot('menu-dans-brume');run(1,0);run(60)
 r.call('CB2_BagMenuFromStartMenu');run(180);assert not fog_sprites();shot('sac-sans-brume');run(1,0);run(180)
 if not free():run(1,0);run(60)
 assert amount()==192 and len(fog_sprites())==15;report('Bag clears fog sprites, field return reconstructs them without duplication')
 stage('CinnabarIsland',12,11);save_continue();clear('Native Save/Continue on Cinnabar remains clear and sepia')
 # Thirteen past-era maps: absence checked from real native objects and fog state.
 positions=[('CinnabarIsland',12,11),('CinnabarIsland_Gym',5,5),('CinnabarIsland_Mart',5,5),('CinnabarIsland_PokemonCenter_1F',7,4),('CinnabarIsland_PokemonCenter_2F',6,4),('CinnabarIsland_PokemonLab_Entrance',3,6),('CinnabarIsland_PokemonLab_Lounge',7,6),('CinnabarIsland_PokemonLab_ResearchRoom',7,6),('CinnabarIsland_PokemonLab_ExperimentRoom',11,5),('PokemonMansion_1F',8,28),('PokemonMansion_2F',9,4),('PokemonMansion_3F',8,4),('PokemonMansion_B1F',34,28)]
 for name,x,y in positions:stage(name,x,y);clear('No fog on '+name)
 # A genuine native building exit and entrance, not a direct interior-only warp.
 stage('CinnabarIsland_PokemonCenter_1F',7,7);run(40,5);run(180);assert pair()==MAPS['CinnabarIsland'];clear('Native Pokemon Center door exit stays clear')
 # Actual Fly, Teleport and escape effects, with destinations explicitly staged.
 stage('Route20',10,9)
 g,n=MAPS['CinnabarIsland'];r.call('SetWarpDestination',g,n,255,12,12)
 r.call('ReturnToFieldFromFlyMapSelect')
 for f in range(4000):
  r.run()
  if f>180 and free() and pair()==MAPS['CinnabarIsland']:break
 else:raise AssertionError(('Fly did not finish',pair(),pos()))
 clear('Native Fly lands directly on past island without maritime fog');shot('vol-arrivee')
 # Healpoint is a fixture; Teleport animation and landing are native.
 r.call('SetLastHealLocationWarp',9);stage('Route20',10,9);r.w32(r.symbols['gFieldEffectArguments'],0);native_effect('FldEff_UseTeleport','CinnabarIsland')
 # Enter mansion through its actual door to establish the game's escape warp.
 stage('CinnabarIsland',8,4)
 travel(4,'PokemonMansion_1F',(8,32),[],limit=1000)
 assert r.call('CanUseEscapeRopeOnCurrMap')
 native_effect('StartEscapeRopeFieldEffect','CinnabarIsland')
 stage('CinnabarIsland',8,4);travel(4,'PokemonMansion_1F',(8,32),[],limit=1000)
 assert r.call('SetUpFieldMove_Dig');r.w32(r.symbols['gFieldEffectArguments'],0)
 native_effect('FldEff_UseDig','CinnabarIsland')
 r.call('FlagSet',0x82c);stage('Route20',20,9);movie=[];travel(6,'CinnabarIsland',(23,9),movie);clear('Postgame-flag fixture: native sea crossing still enters clear sepia island')
 report('No Phase C dialogue, quiz, party, map or save format changed')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True)
 if r:shot('ECHEC')
finally:
 for name,frames in movies.items():
  if frames:
   frames[0].resize((720,480),Image.Resampling.NEAREST).save(D/(name+'.gif'),save_all=True,append_images=[f.resize((720,480),Image.Resampling.NEAREST) for f in frames[1:]],duration=67,loop=0)
 if r:rom_hash=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close()
 else:rom_hash=None
 (D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=rom_hash,checks=rows,failure=failure,scope=__doc__,fixtures='Native new game, strong party, starting coordinates and 250-step Repel; no changed collisions, NPCs, enemy HP or battle outcomes. Special move destinations staged explicitly.'),ensure_ascii=False,indent=2)+'\n')
assert passed,failure

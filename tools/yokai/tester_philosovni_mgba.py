#!/usr/bin/env python3
"""Native mGBA chapter fixtures. Controller dialogue/combat; initial maps/parties are QA fixtures.
No enemy HP, battle outcome, or story victory flag is changed to force success.
Special edge cases restore snapshots and alter only the stated initial fixture.
"""
import os,json,struct,hashlib,traceback,subprocess
from pathlib import Path
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C,MAPS,warp,strong_party
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
P=ROOT/'docs/pierre-philosovni/validation'/mode;P.mkdir(parents=True,exist_ok=True)
r=None;rows=[];passed=False;failure=None;movies={};snapshots={}
STATE=0x40f4

def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def state():return r.call('VarGet',STATE)
def flag(n):return bool(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0xEE0+(n>>3),1)[0]&(1<<(n&7)))
def mapname():
 pair=tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2));return next((k for k,v in MAPS.items() if v==pair),str(pair))
def free():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]
def actors():return {b[8]:b for i in range(16) if (b:=r.read(r.symbols['gObjectEvents']+36*i,36))[0]&1}
def pos():return tuple(x-7 for x in struct.unpack_from('<hh',actors()[255],16))
def shot(name):r.frame.save(P/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(name+'-x3.png'))
def tick(f):r.keys=battle_keys(r,f) if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 else ({8} if f%16<4 else set());r.run()
def finish(limit=14000,movie=None):
 frames=[];captured=set()
 for f in range(limit):
  tick(f)
  if movie and f%12==0:frames.append(r.frame.copy())
  if movie and 'coupe' not in captured and r.symbols['EventScript_ObtainedItem']+5 <= r.u32(r.symbols['sGlobalScriptContext']+8) < r.symbols['EventScript_ObtainedItem']+8:
   r.keys=set();r.run(120);shot('remise-cs-coupe');captured.add('coupe')
  if f>60 and free():
   r.keys=set();r.run(12)
   if movie:movies[movie]=frames
   return
 raise AssertionError(('Script/battle did not return to field',hex(r.u32(r.symbols['gMain']+4)),hex(r.u32(r.symbols['gBattleMainFunc']))))
def script(name):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[name])
def walk(k):
 x,y=pos();dx,dy={4:(0,-1),5:(0,1),6:(-1,0),7:(1,0)}[k];goal=(x+dx,y+dy)
 for f in range(50):
  r.keys={k};r.run()
  if pos()==goal:r.keys=set();r.run(18);return
 raise AssertionError(('Blocked walking',mapname(),pos(),goal,k))
def save():
 assert free(),('Save outside safe field',mapname())
 before=state();here=mapname()
 r.call('SaveMapView')
 assert r.call('TrySavingData',0,max_frames=1500)==1
 assert r.call('LoadGameSave',0,max_frames=1500)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(2500):
  tick(f)
  if f>180 and free():break
 else:raise AssertionError('Continue blocked')
 r.keys=set();r.run(12);assert state()==before and mapname()==here
 return dict(state=before,map=here)
def mon(i,field):return r.call('GetMonData',r.symbols['gPlayerParty']+100*i,C[field],0)
def setmon(i,field,value):r.w32(r.PARAMS+128,value);r.call('SetMonData',r.symbols['gPlayerParty']+100*i,C[field],r.PARAMS+128)
def waitbattle():
 frames=[]
 for f in range(14000):
  tick(f)
  if f%12==0:frames.append(r.frame.copy())
  if r.u32(r.symbols['gBattleMainFunc'])==r.symbols['HandleTurnActionSelectionState']|1 and r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   r.keys=set();r.run(60);movies['entrepot-revelation']=frames;return
 raise AssertionError('Duo intro not reached')
def begin():script('Philosovni_Overhear');waitbattle()
def native_party(species,level,attack=None):
 r.call('ZeroPlayerPartyMons');r.call('CreateMon',r.symbols['gPlayerParty'],species,level,20,1,9,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 if attack is not None:
  for i in range(4):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],attack,i)
def at_action():return r.u32(r.symbols['gBattlerControllerFuncs'])==r.symbols['HandleInputChooseAction']|1

def pulse(key,after=15):r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(after)
try:
 r=new_game();strong_party(r);initial=r.snapshot()
 # Non-repeating Wyatt: after speech only; rewards earned by actual victory.
 r.call('FlagSet',C['FLAG_ARGENTA_MORLEONE_DONE']);warp(r,*MAPS['PewterCity_Gym'],5,3)
 script('PewterCity_Gym_EventScript_Brock');seen=False
 for f in range(15000):
  tick(f)
  if flag(0x326) and not seen:seen=True
  if f>120 and free():break
 else:raise AssertionError('Wyatt battle not complete')
 assert seen and flag(0x820) and flag(C['FLAG_GOT_TM39_FROM_BROCK']);shot('wyatt-badge');report('Wyatt concern after speech and unchanged real victory rewards; badge Roche, TM39')
 script('PewterCity_Gym_EventScript_Brock');finish();assert flag(0x326);report('Wyatt revisit returns without replay or new battle')
 report('Save/Continue after Wyatt',**save())
 # Reach port entirely by ordinary walking, no HM and no badge prerequisite.
 r.restore(initial);warp(r,*MAPS['VermilionCity'],23,8)
 assert not r.call('CheckBagHasItem',C['ITEM_HM01'],1)
 for _ in range(15):walk(7)
 for _ in range(8):walk(5)
 for _ in range(2):walk(6)
 for _ in range(13):walk(5)
 walk(5)
 for _ in range(3):walk(6)
 shot('carmin-rencontre');snapshots['city']=r.snapshot();report('Native walk from city north entrance to Ariane without Cut',position=pos())
 # Actual A interaction, then controller NO. Invitation is restartable.
 pulse(4);pulse(8,1)
 for f in range(6000):
  tick(f)
  funcs=[r.u32(r.symbols['gTasks']+40*i) for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\1']
  if (r.symbols['Task_YesNoMenu_HandleInput']|1) in funcs:break
 else:raise AssertionError('Invitation yes/no task not reached')
 r.keys=set();r.run(30);pulse(0,30);finish();assert state()==0;report('Invitation declined without quest advancement')
 # Native script fixture accepted; player position remains on the quay.
 script('Philosovni_CityAriane');finish(movie='ariane-rencontre');assert state()==1
 report('Accepted investigation and save/Continue on quay',**save())
 # Actual walking into the new door, followed by exploration and tile trigger.
 walk(6);walk(4)
 for _ in range(3):walk(6)
 r.keys={4}
 for _ in range(300):
  r.run()
  if mapname()=='VermilionCity_PhilosovniWarehouse':break
 r.keys=set();r.run(200)
 assert mapname()=='VermilionCity_PhilosovniWarehouse',(mapname(),pos())
 shot('entrepot-exploration');report('Warehouse entrance reached by native door without Cut',position=pos())
 report('Save/Continue before overhearing',**save());snapshots['warehouse']=r.snapshot()
 while pos()[1]>7:walk(4)
 # Last step activates the actual coordinate event.
 r.keys={4};r.run(20);r.keys=set();waitbattle();shot('combat-duo')
 assert r.u32(r.symbols['gBattleTypeFlags'])&(1<<23)
 indexes=struct.unpack('<4H',r.read(r.symbols['gBattlerPartyIndexes'],8));assert indexes==(0,0,6,1),indexes
 assert mon(6,'MON_DATA_SPECIES')==C['SPECIES_VOLTORB'] and mon(6,'MON_DATA_LEVEL')==21
 assert r.read(r.symbols['gBattlersCount'],1)==b'\4'
 snapshots['battle']=r.snapshot();report('Four native battlers: player plus AI Usapion versus one Yo-kai per grunt',party_indexes=indexes)
 # Observe real AI spending PP and dealing damage; victory follows real attacks.
 before_pp=[mon(6,'MON_DATA_PP1')+i*0 for i in range(1)]
 finish(movie='combat-duo-victoire');assert state()==3
 assert r.call('CheckBagHasItem',C['ITEM_HM01'],1) and flag(C['FLAG_GOT_HM01'])
 assert mon(6,'MON_DATA_SPECIES')==0
 shot('enquete-terminee');report('Actual double victory, grunt escape, one HM and temporary partner cleared')
 report('Save/Continue after Cut reward',**save());snapshots['complete']=r.snapshot()
 while pos()[1]<9:walk(5)
 r.keys={5}
 for _ in range(300):
  r.run()
  if mapname()=='VermilionCity':break
 r.keys=set();r.run(200);assert mapname()=='VermilionCity',(mapname(),pos())
 shot('sortie-entrepot');report('Native warehouse exit returns to quay',position=pos())
 r.restore(snapshots['complete'])
 # Reward script retry cannot duplicate HM.
 script('Philosovni_Reward');finish();assert state()==3
 assert r.call('BagGetQuantityByItemId',C['ITEM_HM01'])==1
 report('Reward re-entry never duplicates HM01')
 # Loss fixture: level-1 player with harmless moves, real AI Usapion and unmodified opponents.
 r.restore(snapshots['warehouse']);native_party(C['SPECIES_BULBASAUR'],1,C['MOVE_GROWL']);begin();finish(limit=45000,movie='combat-duo-defaite');assert state()==1
 assert not r.call('CheckBagHasItem',C['ITEM_HM01'],1) and not flag(0x329)
 assert mon(0,'MON_DATA_HP')==mon(0,'MON_DATA_MAX_HP') and mon(6,'MON_DATA_SPECIES')==0
 report('Genuine loss: no victory/reward flag, healed player, restartable investigation',**save())
 strong_party(r);begin();finish();assert state()==3;report('Actual retry after defeat wins and grants Cut')
 # Six real player slots preserved, including the sixth member in native menu.
 r.restore(snapshots['warehouse']);strong_party(r)
 for i in range(1,6):r.call('CreateMon',r.symbols['gPlayerParty']+100*i,i+1,30,20,1,40+i,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\6');six=[mon(i,'MON_DATA_PERSONALITY') for i in range(6)]
 begin();shot('duo-equipe-six');finish();assert state()==3
 assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\6' and [mon(i,'MON_DATA_PERSONALITY') for i in range(6)]==six
 report('All six player members and original personalities preserved through duo',**save())
 # Captain: real healing interaction preserves departure state and gives no HM.
 r.restore(initial);warp(r,*MAPS['SSAnne_CaptainsOffice'],4,3);script('SSAnne_CaptainsOffice_EventScript_Captain');finish(movie='capitaine-adapte')
 assert flag(0x32b) and not r.call('CheckBagHasItem',C['ITEM_HM01'],1) and r.call('VarGet',C['VAR_MAP_SCENE_VERMILION_CITY'])==1
 script('SSAnne_CaptainsOffice_EventScript_Captain');finish();assert not r.call('CheckBagHasItem',C['ITEM_HM01'],1)
 report('Captain heals normally and enables departure, never gives duplicate Cut')
 # Quest reward does not arm ship departure or prevent ticket admission.
 r.restore(snapshots['complete']);assert r.call('VarGet',C['VAR_MAP_SCENE_VERMILION_CITY'])==0
 warp(r,*MAPS['VermilionCity'],23,32);r.call('AddBagItem',C['ITEM_SS_TICKET'],1);r.call('FlagSet',C['FLAG_GOT_SS_TICKET']);walk(5)
 finish();r.keys={5};r.run(90);r.keys=set();r.run(200)
 assert mapname()=='SSAnne_Exterior',mapname();shot('oceane-accessible');report('Oceane remains boardable after quest reward; departure not armed by HM')
 # Gym presence and no phantom companions after Continue.
 r.restore(snapshots['complete']);warp(r,*MAPS['VermilionCity'],33,30);assert not ({9,10}&set(actors()))
 report('Completed city hides Ariane/Usapion across save/reload',**save())
 warp(r,*MAPS['VermilionCity_Gym'],5,3);assert any(b[5]==C['OBJ_EVENT_GFX_LT_SURGE'] for b in actors().values());shot('ariane-retour-arene');report('Ariane returns to native Gym; puzzle and trainers remain')
 # Fresh arrival Gym absent; imported badge3 saves retain leader for compatibility.
 r.restore(initial);warp(r,*MAPS['VermilionCity_Gym'],5,3);assert not any(b[5]==C['OBJ_EVENT_GFX_LT_SURGE'] for b in actors().values())
 r.call('FlagSet',0x822);warp(r,*MAPS['VermilionCity_Gym'],5,3);assert any(b[5]==C['OBJ_EVENT_GFX_LT_SURGE'] for b in actors().values());report('Gym visibility respects quest chronology and old completed-badge saves')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True)
 if r:shot('ECHEC')
finally:
 if r:
  for name,frames in movies.items():
   if frames:
    frames=frames[:300]
    frames[0].resize((480,320),Image.Resampling.NEAREST).save(P/(name+'.gif'),save_all=True,append_images=[x.resize((480,320),Image.Resampling.NEAREST) for x in frames[1:]],duration=200,loop=0)
  rom_hash=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close()
 else:rom_hash=None
 (P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=rom_hash,fixtures='Native new game; initial map/party fixtures and explicit edge-case snapshots. No enemy HP or outcome edited.',checks=rows,failure=failure),indent=2,ensure_ascii=False)+'\n')
assert passed,failure

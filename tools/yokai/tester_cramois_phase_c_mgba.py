#!/usr/bin/env python3
"""Phase C native scripts/controller tests. Warps/strong party/progression and PC fixtures stated explicitly; no opponent HP or outcome edits."""
import os,json,hashlib,traceback,re,struct
from pathlib import Path
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import warp,MAPS,C,strong_party
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
D=ROOT/'docs/cramois-ile-passe/phase-c'/mode;D.mkdir(parents=True,exist_ok=True)
rows=[];movies={};r=None;passed=False;failure=None
MEET,WIN,GIFT=0x32c,0x32d,0x32e
GYM=json.loads((ROOT/'data/maps/CinnabarIsland_Gym/map.json').read_text())
quizflags=[C['FLAG_CINNABAR_GYM_QUIZ_'+str(i)] for i in range(1,7)]
trainerids=[C['TRAINER_'+s] for s in ['BURGLAR_QUINN','SUPER_NERD_AVERY','BURGLAR_RAMON','SUPER_NERD_DEREK','BURGLAR_DUSTY','SUPER_NERD_ZAC']]

def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def run(n,key=None,movie=None):
 r.keys=set() if key is None else {key}
 for i in range(n):
  r.run()
  if movie is not None and i%6==0:movie.append(r.frame.copy())
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def battle():return r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
def free():return field() and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]
def flag(x):return r.call('FlagGet',x)
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-x4.png'))
def stage(x=5,y=5):warp(r,*MAPS['CinnabarIsland_Gym'],x,y)
def start(name):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[name])
def obj(local):
 for i in range(16):
  o=r.read(r.symbols['gObjectEvents']+36*i,36)
  if o[0]&1 and o[8]==local:return i,o
 raise AssertionError(('missing object',local))
def select(local):
 i,_=obj(local);r.write(r.symbols['gSelectedObjectEvent'],bytes([i]));r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',local))
def finish(limit=30000,movie=None):
 seen=False
 for f in range(limit):
  seen|=battle();r.keys=battle_keys(r,f) if battle() else ({8} if f%16<4 else set());r.run()
  if movie is not None and f%12==0:movie.append(r.frame.copy())
  if f>60 and free():run(12);return seen
 raise AssertionError('Native event did not finish')
def task(name):
 address=r.symbols[name]|1
 return any(r.u32(r.symbols['gTasks']+40*i)==address and r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' for i in range(16))
def answer(yes,movie=None):
 for f in range(3500):
  if task('Task_YesNoMenu_HandleInput'):break
  run(1,8 if f%16<4 else None,movie)
 else:raise AssertionError('Yes/No not reached')
 run(40,movie=movie)
 if not yes:run(1,5,movie);run(12,movie=movie)
 run(1,8,movie);run(12,movie=movie)
def save_continue():
 assert free();r.keys=set();r.call('SaveMapView');assert r.call('TrySavingData',0,max_frames=1500)==1
 assert r.call('LoadGameSave',0,max_frames=1500)==1;r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(2500):
  r.run()
  if f>180 and free():run(20);return
 raise AssertionError('Save/Continue blocked')
def door(i):
 points=[(26,9),(17,9),(17,16),(11,22),(5,17),(5,9)]
 x,y=points[i];return r.call('MapGridGetMetatileIdAt',x+7,y+7),r.call('MapGridGetCollisionAt',x+7,y+7)
def companion(label):
 _,o=obj(10);_,champ=obj(8)
 assert o[5]==176 and abs(int.from_bytes(o[16:18],'little')-int.from_bytes(champ[16:18],'little'))==1 and o[18:20]==champ[18:20]
 bank=r.read(r.symbols['gPlttBufferUnfaded']+(256+8*16)*2,32);expected=r.read(r.symbols['gObjectEventPal_CramoisHovernyan'],32);assert bank==expected,(label,'companion palette mismatch')
 assert r.call('MapGridGetCollisionAt',13,11)==0
 report(label,local_id=10,palette_bank=8,adjacent=True)
def measure_text():
 labels=re.findall(r'^(CinnabarIsland_Gym_Text_\w+)::', (ROOT/'data/maps/CinnabarIsland_Gym/text.inc').read_text(),re.M)
 checked=[]
 for gender in [0,1]:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
  for label in labels:
   if label not in r.symbols:continue
   r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols[label]);raw=r.read(r.symbols['gStringVar4'],1024).split(b'\xff',1)[0]
   for line in re.split(b'[\xfa\xfb\xfe]',raw):
    # Native BGM commands occur only in the approved old intro; measure its literal prefix.
    if b'\xfc' in line:line=line.split(b'\xfc')[0]
    r.write(r.PARAMS+128,line+b'\xff');w=r.call('GetStringWidth',2,r.PARAMS+128,0)
    assert w<=208,(label,gender,w);checked.append(w)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,b'\0');report('All Gym dialogue lines fit native font',lines=len(checked),max_pixels=max(checked),limit=208)
try:
 r=new_game();strong_party(r);r.call('VarSet',0x40f4,3);stage();companion('Nathaniel and Hovernyan initial spawn');shot('nathaniel-hovernyan')
 measure_text()
 # Meet and challenge via native A interaction, without setting the meeting flag.
 run(1,4);run(20);run(1,8);run(280);shot('rencontre-choc');movie=[];run(90,movie=movie)
 seen=finish(movie=movie);assert seen and flag(MEET) and flag(0x4b6) and flag(0x826) and flag(C['FLAG_GOT_TM38_FROM_BLAINE'])
 assert not flag(WIN) and not flag(GIFT);movies['rencontre-nathaniel-et-defi']=movie;shot('victoire-badge');companion('Companion preserved after first native victory')
 levels=[r.call('GetMonData',r.symbols['gEnemyParty']+100*i,C['MON_DATA_LEVEL'],0) for i in range(6)]
 assert levels==[40,41,41,42,43,45];report('Actual first Champion victory gives Badge and CT, no postgame gift',levels=levels)
 save_continue();assert flag(MEET) and flag(0x826) and not flag(GIFT);companion('Companion and meeting state survive native Save/Continue')
 select(8);start('CinnabarIsland_Gym_EventScript_Blaine');assert not finish();assert not flag(GIFT);report('Pre-League revisit cannot rematch or obtain Hovernyan')
 r.call('FlagClear',0x4b6)
 # Quiz choices run original sign events; positions/flags staged, not responses/outcomes.
 for wrong in [False,True]:
  for i in range(6):
   r.call('FlagClear',quizflags[i]);r.call('ClearTrainerFlag',trainerids[i]);ev=next(e for e in GYM['bg_events'] if e['script'].endswith(f'Quiz{i+1}'+('Right' if wrong else 'Left')))
   stage(ev['x'],ev['y']+1);before=door(i);assert before[1]!=0,(i,before)
   run(1,4);run(18);run(1,8);movie=[]
   answer((i!=0)!=wrong,movie);shot(f'quiz-{i+1}-'+('erreur' if wrong else 'reponse'))
   seen=finish(movie=movie);assert bool(seen)==wrong and flag(quizflags[i]) and door(i)[1]==0,(i,wrong,seen,door(i))
   if wrong:assert r.call('HasTrainerBeenFought',trainerids[i])
   report(f'Quiz {i+1} '+('wrong/right-side native battle opens door' if wrong else 'correct/left-side opens without battle'))
   if i in [0,5]:movies[f'quiz-{i+1}-'+('erreur-combat' if wrong else 'bonne-reponse')]=movie
   if not wrong and i==5:save_continue();assert all(flag(x) for x in quizflags);report('Six opened quiz doors survive native Save/Continue')
 # Direct challenges remain valid after resetting only the corresponding fixtures.
 for i in range(6):
  r.call('FlagClear',quizflags[i]);r.call('ClearTrainerFlag',trainerids[i]);event=next(x for x in GYM['object_events'] if x['script'].endswith('_'+['Quinn','Avery','Ramon','Derek','Dusty','Zac'][i]));stage(event['x'],event['y']+1)
  select(GYM['object_events'].index(event)+1);start(event['script']);assert finish() and flag(quizflags[i]) and door(i)[1]==0
  report(f'Direct native trainer challenge {i+1} opens its door')
 r.call('FlagSet',0x4b6)
 # Postgame eligibility requires BOTH initial Champion victory and League flag.
 r.call('FlagSet',0x82c);stage();select(8);start('CinnabarIsland_Gym_EventScript_Blaine');answer(False);assert not finish() and not flag(WIN) and not flag(GIFT);report('Postgame rematch refusal gives nothing')
 # Lose a real rematch with a naturally weak one-HP party (no forced enemy HP/outcome).
 r.call('CreateMon',r.symbols['gPlayerParty'],C['SPECIES_CATERPIE'],1,0,1,100,0,0);r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_SPLASH'],0);r.w32(r.PARAMS+128,1);r.call('SetMonData',r.symbols['gPlayerParty'],C['MON_DATA_HP'],r.PARAMS+128)
 select(8);start('CinnabarIsland_Gym_EventScript_Blaine');answer(True);assert finish() and not flag(WIN) and not flag(GIFT);report('Actual lost rematch cannot unlock gift')
 strong_party(r);stage();select(8);start('CinnabarIsland_Gym_EventScript_Blaine');movie=[];answer(True,movie);assert finish(movie=movie) and flag(WIN) and flag(GIFT)
 assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\2' and r.call('GetMonData',r.symbols['gPlayerParty']+100,C['MON_DATA_SPECIES'],0)==149
 movies['revanche-et-don-hovernyan']=movie;shot('hovernyan-recu');report('Actual post-League second victory awards Hovernyan level45 once')
 save_continue();select(8);start('CinnabarIsland_Gym_EventScript_Blaine');assert not finish() and r.read(r.symbols['gPlayerPartyCount'],1)==b'\2';companion('Past companion remains after gift Save/Continue');report('Gift flag durable, repeated talk gives no duplicate')
 # Full party/PC retry branches: won flag is a stated fixture, no further battle required.
 for i in range(6):r.call('CreateMon',r.symbols['gPlayerParty']+100*i,1,50,31,1,100,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\6');storage=r.u32(r.symbols['gPokemonStoragePtr']);r.write(storage+4,r.read(r.symbols['gPlayerParty'],80)*420);r.call('FlagClear',GIFT)
 select(8);start('CinnabarIsland_Gym_EventScript_Blaine');assert not finish() and flag(WIN) and not flag(GIFT);shot('boites-pleines');save_continue();assert flag(WIN) and not flag(GIFT);report('Full party + 420 full boxes keeps pending reward across Save/Continue')
 storage=r.u32(r.symbols['gPokemonStoragePtr']);r.write(storage+4,b'\0'*80);select(8);start('CinnabarIsland_Gym_EventScript_Blaine');assert not finish() and flag(GIFT) and r.call('GetBoxMonDataAt',0,0,C['MON_DATA_SPECIES'])==149;shot('hovernyan-envoye-pc');report('Retry after one freed PC slot transfers Hovernyan without another battle')
 save_continue();select(8);start('CinnabarIsland_Gym_EventScript_Blaine');assert not finish() and flag(GIFT) and r.call('GetBoxMonDataAt',0,1,C['MON_DATA_SPECIES'])!=149;report('PC reward cannot duplicate after Save/Continue')
 # Female variant: full native first victory and postgame victory with PC transfer.
 r.close();r=new_game(1);strong_party(r);r.call('VarSet',0x40f4,3);r.call('FlagSet',0x82c);stage();companion('Michael and Hovernyan initial spawn');shot('michael-hovernyan')
 run(1,4);run(18);run(1,8);movie=[];assert finish(movie=movie) and flag(MEET) and flag(0x826) and not flag(GIFT) and not flag(WIN);movies['rencontre-michael-et-defi']=movie;report('Michael actual first victory preserves Badge/CT and cannot gift even with League flag already set')
 r.call('FlagSet',0x82c);select(8);start('CinnabarIsland_Gym_EventScript_Blaine');answer(True);assert finish() and flag(GIFT) and flag(WIN);report('Michael actual postgame victory awards Hovernyan')
 save_continue();companion('Michael companion remains after postgame gift and Save/Continue')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True)
 if r:shot('ECHEC')
finally:
 for name,frames in movies.items():
  if frames:
   # Long native fights sampled to control file size, no simulated frames.
   if len(frames)>900:frames=frames[::2]
   frames[0].resize((480,320),Image.Resampling.NEAREST).save(D/(name+'.gif'),save_all=True,append_images=[f.resize((480,320),Image.Resampling.NEAREST) for f in frames[1:]],duration=100 if len(frames)<900 else 200,loop=0)
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest() if r else None
 if r:r.close()
 (D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=sha,checks=rows,failure=failure,fixtures=__doc__),ensure_ascii=False,indent=2)+'\n')
assert passed,failure

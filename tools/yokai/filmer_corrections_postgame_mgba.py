#!/usr/bin/env python3
"""Extraits natifs avec son ; prérequis/équipe 100 préparés avant la capture, puis boutons seuls."""
import sys,json,struct
from postgame_qa_common import QA
from film_cible_mgba import Film
from mgba_rpc import ROOT
mode=sys.argv[1];q=QA('TEMP.json');r=q.r;D=ROOT/'docs/postgame-corrections-terminyanator-20261025';D.mkdir(exist_ok=True)
try:
 for i,sp in enumerate((150,149,65,123,25,87)):
  p=q.mon(i,sp,100)
  for j,m in enumerate((53,94,58,85)):r.call('SetMonMoveSlot',p,m,j)
 q.f(0x82c)
 for flag in range(0x820,0x828):q.f(flag)
 if mode.startswith('chen'):
  # Deliberately reproduce the stale flags from the old film fixtures.
  q.f(0x2b);q.f(0x2d,False);r.call('VarSet',0x4055,9)
  if mode=='chen-151':
   q.f('FLAG_PG_CHEN_JIBANYAN')
   for i in range(1,152):
    r.call('GetSetPokedexFlag',i,2);r.call('GetSetPokedexFlag',i,3)
   assert r.call('YoannMedalliumComplete')
  q.warp('PalletTown_ProfessorOaksLab',6,4)
  assert q.local('LOCALID_OAKS_LAB_PROF_OAK') in q.actors() and q.local('LOCALID_OAKS_LAB_RIVAL') not in q.actors()
  r.frame.save(D/(mode+'-avant.png'));q.pulse(4,20)
  r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',q.local('LOCALID_OAKS_LAB_PROF_OAK')))
  r.write(r.symbols['gSelectedObjectEvent'],bytes([(q.actors()[q.local('LOCALID_OAKS_LAB_PROF_OAK')]-r.symbols['gObjectEvents'])//36]))
  r.call('VarSet',0x800c,2);r.call('ScriptContext_SetupScript',r.symbols['PalletTown_ProfessorOaksLab_EventScript_ProfOak'])
 elif mode=='matt-champion':q.warp('PokemonLeague_ChampionsRoom',6,20)
 elif mode=='alizon-grotte':
  from mafiamille_qa import C
  q.f(C['FLAG_HIDE_ICEFALL_CAVE_LORELEI'],False);q.f(C['FLAG_HIDE_ICEFALL_CAVE_ROCKETS'],False)
  q.warp('FourIsland_IcefallCave_Back',12,19)
  r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',q.local('LOCALID_ICEFALL_LORELEI')))
  r.call('ScriptContext_SetupScript',r.symbols['FourIsland_IcefallCave_Back_EventScript_LoreleiRocketsScene'])
 elif mode.startswith('scientifique-'):
  index=int(mode[-1]);mp=['LavenderTown','VermilionCity','SaffronCity'][index-1];target=next(o for o in json.loads((ROOT/f'data/maps/{mp}/map.json').read_text())['object_events'] if o.get('script')==['PG_ScientistLav','PG_ScientistPort','PG_ScientistYopple'][index-1]);x,y=target['x'],target['y'];q.f(0x322);r.call('VarSet',0x40f3,1);r.call('VarSet',0x40f4,3)
  for flag in ['FLAG_PG_SCIENTIST_1','FLAG_PG_SCIENTIST_2'][:index-1]:q.f(flag)
  q.warp(mp,x,y+1);r.call('ScriptContext_SetupScript',r.symbols[['PG_ScientistWin1','PG_ScientistWin2','PG_ScientistWin3'][index-1]])
 else:raise ValueError(mode)
 film=Film(r,D/(mode+'.mp4'));busy=False;stable=0;seenbattle=False;diploma=False;diploma_start=None;trainers=set();last=None
 for f in range(round(film.fps*900)):
  cb=film.callback()
  if cb!=last:film.events.append(dict(seconds=f/film.fps,callback=cb));last=cb
  diploma|='Diploma' in cb
  if 'Diploma' in cb and diploma_start is None:diploma_start=f
  if cb=='BattleMainCB2':seenbattle=True;trainers.add(int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little'))
  idle=q.idle();busy|=not idle
  done=(seenbattle and cb=='CB2_RollYokaiCredits') if mode=='matt-champion' else busy and idle and f>60
  stable=stable+1 if done else 0
  if done:r.keys=set()
  elif cb=='CB2_Diploma':r.keys={8} if f-diploma_start>300 and f%16<2 else set()
  else:r.keys=film.controls()
  r.run()
  if stable>=180:break
 else:raise AssertionError((mode,'timeout',cb))
 def flagbit(flag):return bool(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+flag//8,1)[0] & (1<<(flag%8)))
 if mode=='chen-151':assert diploma and flagbit(0x331)
 if mode=='chen-jibanyan':assert flagbit(0x341)
 if mode=='matt-champion':assert seenbattle and r.read(r.symbols['gBattleOutcome'],1)==b'\1'
 r.frame.save(D/(mode+'-fin.png'));film.finish(scene=mode,prepared_party_level=100,prepared_battle_return=mode.startswith('scientifique-'),diploma_shown=diploma,trainers=sorted(trainers),complete=True)
finally:r.close()

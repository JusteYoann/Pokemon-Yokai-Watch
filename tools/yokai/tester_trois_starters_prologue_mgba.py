#!/usr/bin/env python3
"""Choose each real starter and finish Matt's first battle via controller input.

Two new games (Nathan/Katie), fixture warp to the lab reception, then three
independent savestate branches per gender. No injected Pokemon, stats or moves.
The route from bedroom to the lab and the parcel journey are not played here.
"""
import hashlib,json,os,struct
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game
OUT=ROOT/'QA_RECETTE_FINALE/RAPPROCHEMENT_2026_10_22/starters';OUT.mkdir(parents=True,exist_ok=True)
rows=[]
def pos(r):return struct.unpack('<hh',r.read(r.u32(r.symbols['gSaveBlock1Ptr']),4))
def pulse(r,key,frames=8):
 r.keys=set();r.run(4);r.keys={key};r.run(frames);r.keys=set();r.run(20)
def warp(r,x,y):
 r.keys=set();r.call('SetWarpDestination',4,3,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(200)
def walk(r,x,y):
 for _ in range(30):
  px,py=pos(r)
  if (px,py)==(x,y):return
  key=7 if px<x else 6 if px>x else 5 if py<y else 4
  r.keys={key}
  for f in range(60):
   r.run()
   if pos(r)!=(px,py):break
  else:raise AssertionError(('Movement blocked',pos(r),(x,y)))
  r.keys=set();r.run(20)
 raise AssertionError(('Path not reached',pos(r),(x,y)))
def advance_to_stage(r,stage,limit=16000,decline_nickname=False):
 reached=False
 for f in range(limit):
  key=0 if reached or decline_nickname and r.read(r.symbols['gPlayerPartyCount'],1)==b'\x01' else 8
  r.keys={key} if f%16<4 else set();r.run()
  if f%64==0:reached |= r.call('VarGet',0x4055)==stage
  if reached and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02':
   r.keys=set();r.run(30);return
 raise AssertionError(('Stage did not finish',stage,r.call('VarGet',0x4055),pos(r)))

for gender,person in [(0,'nathan'),(1,'katie')]:
 r=new_game(gender)
 try:
  r.call('VarSet',0x4055,1);r.call('FlagClear',0x2B);r.call('FlagClear',0x2D);warp(r,6,12)
  advance_to_stage(r,2);assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\x00'
  base=r.snapshot()
  for index,own,enemy,trainer in [(0,5,87,328),(1,29,5,327),(2,87,29,326)]:
   stem=f'{person}-{own:03d}';r.restore(base);warp(r,8+index,5);pulse(r,4)
   pulse(r,8,2);advance_to_stage(r,3,decline_nickname=True)
   assert r.call('VarGet',0x4031)==index
   assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\x01'
   assert r.call('GetMonData',r.symbols['gPlayerParty'],11,0)==own
   assert r.call('GetMonData',r.symbols['gPlayerParty'],56,0)==5
   r.frame.save(OUT/(stem+'-choix.png'))
   walk(r,8+index,6);walk(r,7,6);walk(r,7,8)
   started=False;enemy_checked=False;battle_frames=0
   for f in range(36000):
    r.keys={8} if f%16<4 else set();r.run()
    if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
     started=True;battle_frames+=1
     if not enemy_checked:
      assert r.call('GetMonData',r.symbols['gEnemyParty'],11,0)==enemy
      assert all(r.call('GetMonData',r.symbols['gEnemyParty']+100*i,11,0)==0 for i in range(1,6))
      assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&65535==trainer
      enemy_checked=True
     if battle_frames==800:r.frame.save(OUT/(stem+'-combat.png'))
    if f%64==0 and started and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.call('VarGet',0x4055)==4 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
   else:raise AssertionError(('First battle did not complete',stem,started,pos(r)))
   r.keys=set();r.run(60);assert enemy_checked
   hp=r.call('GetMonData',r.symbols['gPlayerParty'],57,0);maximum=r.call('GetMonData',r.symbols['gPlayerParty'],58,0)
   assert hp==maximum and hp>0
   outcome=r.read(r.symbols['gBattleOutcome'],1)[0];assert outcome in [1,2]
   r.frame.save(OUT/(stem+'-apres.png'))
   assert r.call('TrySavingData',0,max_frames=1200)==1
   r.call('VarSet',0x4031,99);r.call('VarSet',0x4055,0)
   assert r.call('LoadGameSave',0,max_frames=1200)==1
   r.call('LoadPlayerParty')
   assert r.call('VarGet',0x4031)==index and r.call('VarGet',0x4055)==4
   assert r.call('GetMonData',r.symbols['gPlayerParty'],11,0)==own
   rows.append(dict(person=person,starter=own,rival_starter=enemy,rival_trainer=trainer,initial_level=5,outcome=outcome,healed_after_battle=True,native_flash_reload=True,passed=True))
   print('PASS',stem,'outcome',outcome,flush=True)
 except BaseException:
  r.frame.save(OUT/'diagnostic.png');raise
 finally:r.close()
report=dict(passed=True,rom_sha256=hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba')).read_bytes()).hexdigest(),scope=__doc__,results=rows)
(OUT/'TEST_TROIS_STARTERS_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

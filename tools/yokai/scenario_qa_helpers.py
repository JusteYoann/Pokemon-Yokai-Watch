#!/usr/bin/env python3
"""Shared native chapter QA helpers, extracted from the scenario branch; no Argenta scripts imported."""
import re,struct
from mgba_rpc import ROOT
from pilote_combat_mgba import battle_keys,capture_failure
OUT=ROOT/'QA_RECETTE_FINALE/AZURIA_REPRISE_2026_10_22'
C={k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)\b','\n'.join((ROOT/f'include/constants/{n}.h').read_text() for n in ['pokemon','items','moves']),re.M)}
def pos(r):return struct.unpack('<hh',r.read(r.u32(r.symbols['gSaveBlock1Ptr']),4))
def location(r):return tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))
def idle(r):return r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1

def warp(r,g,n,x,y):
 r.keys=set();r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)

def walk(r,d,n=1):
 dx,dy,key={'U':(0,-1,4),'D':(0,1,5),'L':(-1,0,6),'R':(1,0,7)}[d]
 x,y=pos(r);target=(x+dx*n,y+dy*n)
 for _ in range(1200):
  r.keys={key};r.run()
  if pos(r)==target:break
 else:raise AssertionError(('Walking blocked',d,n,(x,y),pos(r),target))
 r.keys=set();r.run(20)

def face_a(r,d):
 key={'U':4,'D':5,'L':6,'R':7}[d];r.keys={key};r.run(4);r.keys=set();r.run(12);r.keys={8};r.run(2);r.keys=set();r.run(12)

def finish(r,limit=12000,watch=False,stem=''):
 seen=[]
 for f in range(limit):
  r.keys={8} if f%16<4 else set();r.run()
  if f>60 and idle(r):r.keys=set();r.run(20);return seen
 raise AssertionError(('Script did not end',pos(r),location(r)))

def fight(r,stem,loss=False,limit=24000,expected=None):
 assert expected is not None, 'Declare the expected native party in every test'
 started=False;first_enemy=[]
 for f in range(limit):
  # Decline the real SHIFT replacement menu; the active Yo-kai is alive.
  if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_UpdatePartyMenu']|1 and int.from_bytes(r.read(r.symbols['gBattleMons']+0x28,2),'little')>0:
   r.keys={0} if f%16<4 else set()
  else:r.keys=battle_keys(r,f)
  r.run()
  cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['BattleMainCB2']|1:
   if not started:
    first_enemy=[(r.call('GetMonData',r.symbols['gEnemyParty']+100*i,11,0),r.call('GetMonData',r.symbols['gEnemyParty']+100*i,56,0)) for i in range(len(expected))]
    assert first_enemy==expected,first_enemy
   started=True
   if f==1024:r.frame.save(OUT/(stem+'-combat.png'))
  if started and cb==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==bytes([2 if loss else 1]):
   finish(r);return f
 r.frame.save(OUT/(stem+'-diagnostic.png'))
 detail=capture_failure(r,'azuria-'+stem,output_dir=OUT/'diagnostics')
 raise AssertionError(('Battle did not finish',stem,started,r.read(r.symbols['gBattleOutcome'],1).hex(),detail))

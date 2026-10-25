#!/usr/bin/env python3
"""Entrées natives et commandes normales jusqu'aux deux combats de Don.
Prérequis de portes/sbires déjà vaincus et équipe niveau 100 préparés avant test.
Aucune modification des adversaires, résultats, palettes ou caméra.
"""
import hashlib,json,struct
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
from mafiamille_qa import C
import parcours_navigation as nav
D=ROOT/'docs/morleone-palettes-20261025';D.mkdir(exist_ok=True)
nav.ROOT=D;nav.CACHE=Path('/workspace/artifacts/morleone-parcours-natif.json')
rows=[]
for mp,warp_id,don_local,opponent in [('RocketHideout_B4F',1,1,348),('SilphCo_11F',1,3,349)]:
 q=QA('TEMP.json');r=q.r;original_run=r.run;checked=0
 try:
  for i,sp in enumerate((150,149,65,123,25,87)):
   p=q.mon(i,sp,100)
   for j,m in enumerate((53,94,58,85)):r.call('SetMonMoveSlot',p,m,j)
  r.call('VarSet',0x4020,10000)
  if mp=='RocketHideout_B4F':
   for trainer in (366,367):r.call('SetTrainerFlag',trainer)
  else:
   q.f(0x28d)
   for trainer in (C['TRAINER_TEAM_ROCKET_GRUNT_40'],C['TRAINER_TEAM_ROCKET_GRUNT_41']):r.call('SetTrainerFlag',trainer)
  g,n=q.maps[mp]
  if mp=='RocketHideout_B4F':
   q.warp('RocketHideout_Elevator',2,4);r.run(180)
   r.call('SetDynamicWarpWithCoords',0,g,n,255,20,23)
  else:
   q.warp('SilphCo_7F',5,7);r.run(180)
  for _ in range(300):
   r.keys={5};r.run()
   if tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==(g,n):break
  else:raise AssertionError(('Entrée native non franchie',mp))
  r.keys=set();r.run(420)
  expected=r.read(r.symbols['gObjectEventPal_YokaiDonMorleoneGroup'],32)
  def palette(local):
   obj=q.actors().get(local)
   if obj is None:return None
   bank=r.read(r.symbols['gSprites']+68*r.read(obj+4,1)[0]+5,1)[0]>>4
   return bank,r.read(r.symbols['gPlttBufferUnfaded']+512+bank*32,32)
  def sample(label):
   p=palette(don_local);assert p and p[1]==expected,(mp,label,p[0] if p else None)
   r.frame.save(D/(mp+'-'+label+'.png'));return p[0]
  entry_bank=sample('entree') if don_local in q.actors() else None
  class SceneStarted(Exception):pass
  def pulse(keys,hold=1,after=20):
   r.keys=set();r.run(4);r.keys=set(keys);r.run(hold);r.keys=set();r.run(after)
   if not q.unlocked():raise SceneStarted()
  targets=[[19,5]] if mp=='RocketHideout_B4F' else [[6,16]]
  paths=[]
  try:
   for target in targets:
    result=nav.navigate(r,target,pulse,180);paths.append(result);assert result['reason']=='arrived',result
  except SceneStarted:
   assert mp=='SilphCo_11F'
  entry_bank=sample('approche')
  if mp=='SilphCo_11F':
   # Both opposite allocation orders: an employee rebuilt after Don and Don
   # rebuilt after the employee. Native graphics setter also reloads palettes.
   for ids in ((don_local,8),(8,don_local),(don_local,9),(9,don_local)):
    for lid in ids:
     actor=q.actors()[lid];r.call('ObjectEventSetGraphicsId',actor,r.read(actor+5,1)[0]);r.run(2)
    sample('ordre-'+str(ids[0])+'-'+str(ids[1]))
   for lid in (1,8,9):
    bank,data=palette(lid);assert bank!=entry_bank and data==r.read(r.symbols['gObjectEventPal_YokaiDomniscianGroup'],32)
   # Native field reconstruction as on return from a fullscreen interface.
   r.call('SetMainCallback2',r.symbols['CB2_ReturnToFieldContinueScriptPlayMapMusic']|1);r.run(420);sample('reconstruction')
   if q.unlocked():
    r.keys={4};r.run(16);r.keys=set();r.run(30)
  if mp=='RocketHideout_B4F':
   assert struct.unpack('<hh',r.read(r.u32(r.symbols['gSaveBlock1Ptr']),4))==(19,5)
   assert r.call('MapGridGetCollisionAt',26,12)==0
   q.pulse(4,24);q.pulse(8,30)
  def monitor(frames=1):
   global checked
   for _ in range(frames):
    original_run()
    if q.callback()=='CB2_Overworld' and don_local in q.actors():
     p=palette(don_local)
     # Initial white/black palette initialization is outside the visible scene.
     if p[1]!=b'\0'*32:assert p[1]==expected,(mp,'palette pendant scène',p[0])
     checked+=1
  r.run=monitor
  q.wait(lambda:q.callback()=='BattleMainCB2',20000)
  assert int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')==opponent
  q.drain(90000)
  assert r.read(r.symbols['gBattleOutcome'],1)==b'\1'
  assert don_local not in q.actors()
  if mp=='SilphCo_11F':
   for lid in (1,8,9):
    bank,data=palette(lid);assert bank==10 and data==r.read(r.symbols['gObjectEventPal_YokaiDomniscianGroup'],32)
  r.frame.save(D/(mp+'-apres-combat.png'))
  row=dict(map=mp,entry_route="elevator exit" if mp=="RocketHideout_B4F" else "teleporter",entered_with_controller=True,entry_source='RocketHideout_Elevator' if mp=='RocketHideout_B4F' else 'SilphCo_7F',walking_paths=paths,don_palette_bank=entry_bank,palette_frames_checked=checked,native_interaction_or_coordinate_trigger=True,native_battle_won=True,don_removed_after_victory=True,other_group_colors_preserved_after_battle=True if mp=='SilphCo_11F' else None)
  rows.append(row);print('PASS',row,flush=True)
 finally:r.run=original_run;r.close()
(D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256((ROOT/'pokefirered_audio.gba').read_bytes()).hexdigest(),scope=__doc__,cases=rows),ensure_ascii=False,indent=2)+'\n')

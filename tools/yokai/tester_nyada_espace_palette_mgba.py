#!/usr/bin/env python3
"""Fixtures natives de la scène Nyada/Démophage : sol, accès, palettes et combat.
Les déplacements d'approche et le combat emploient les boutons du jeu.
"""
import hashlib,json,struct
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
import parcours_navigation as nav
D=ROOT/'docs/nyada-demophage-placement-20261025';D.mkdir(exist_ok=True)
nav.ROOT=D;nav.CACHE=Path('/workspace/artifacts/nyada-nouveau-placement-carte.json')
checks=[]
for gender,label in enumerate(('garcon','fille')):
 q=QA('TEMP.json');q.P=D;r=q.r
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));q.mon();r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],53,0)
  for flag in (0x82c,0x32f,0x345,0x33b):q.f(flag)
  r.call('VarSet',0x4020,500)
  # Native floor-4 approach from the landing connected to the 2F ladder.
  q.warp('CeruleanCave_1F',30,11);r.run(300)
  def pulse(keys,hold=1,after=20):
   r.keys=set();r.run(4);r.keys=set(keys);r.run(hold);r.keys=set();r.run(after)
  def palettes():
   banks={}
   for local,name,symbol in [(q.local('LOCALID_PG_NYADA_CAVE'),'Nyada','gObjectEventPal_DossierNyada'),(q.local('LOCALID_PG_DEMOPHAGE'),'Démophage','gObjectEventPal_DemophageStatique')]:
    a=q.actors()[local];sid=r.read(a+4,1)[0];bank=r.read(r.symbols['gSprites']+68*sid+5,1)[0]>>4
    assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols[symbol],32),(name,bank)
    banks[name]=bank
   assert banks['Nyada']!=banks['Démophage'];return banks
  result=nav.navigate(r,[21,18],pulse,100);assert result['reason']=='arrived',result
  banks=palettes()
  for x,y in [(21,17),(23,17),(21,18),(22,18),(23,18)]:
   assert r.call('MapGridGetCollisionAt',x+7,y+7)==0
   assert r.call('MapGridGetMetatileBehaviorAt',x+7,y+7)==8
   assert r.call('MapGridGetElevationAt',x+7,y+7)==4
  # Both feet and their interaction approaches stand on the same open floor.
  for cx in (21,23):
   for y in range(17,19):
    for x in range(cx-1,cx+2):assert r.call('MapGridGetCollisionAt',x+7,y+7)==0
  for local in (q.local('LOCALID_PG_NYADA_CAVE'),q.local('LOCALID_PG_DEMOPHAGE')):
   obj=q.actors()[local];gfx=r.read(obj+5,1)[0]
   r.call('ObjectEventSetGraphicsId',obj,gfx);palettes()
  # Return to the field through a native UI reconstruction, as after a menu.
  r.call('SetMainCallback2',r.symbols['CB2_ReturnToFieldContinueScriptPlayMapMusic']|1);r.run(400);palettes()
  result=nav.navigate(r,[23,18],pulse,60);assert result['reason']=='arrived',result
  result=nav.navigate(r,[21,18],pulse,60);assert result['reason']=='arrived',result
  pulse([4],1,16);pulse([8],1,30)
  q.wait(lambda:q.callback()=='BattleMainCB2',30000)
  # The existing five-opponent Démophage fight and quest rewards remain native.
  assert r.call('GetBattleBGM')==375
  q.wait(lambda:q.callback()=='CB2_Overworld' and q.fg('FLAG_PG_DEMOPHAGE_WON'),60000)
  banks_after=palettes();r.frame.save(D/f'{label}-apres-combat.png')
  q.drain(30000);assert q.fg('FLAG_PG_NYADA_II_COMPLETE') and q.fg('FLAG_PG_DEMOPHAGE_GIVEN')
  assert q.local('LOCALID_PG_NYADA_CAVE') not in q.actors() and q.local('LOCALID_PG_DEMOPHAGE') not in q.actors()
  checks.append(dict(gender=label,walked_from_ladder_landing=True,both_npcs_reachable=True,open_floor_elevation=4,foot_tiles_and_approaches_clear=True,palettes=banks,palettes_after_native_battle=banks_after,graphics_rebuild_preserves_both_palettes=True,native_victory_and_rewards=True))
  print('PASS',label,checks[-1],flush=True)
 finally:r.close()
(D/'TESTS_SCENE.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks),ensure_ascii=False,indent=2)+'\n')

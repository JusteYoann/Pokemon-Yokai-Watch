#!/usr/bin/env python3
"""Native Toxic residual exhausts a full boss layer; no enemy HP/outcome writes.
Boosted QA player with Toxic/Splash. Status is applied by the actual move.
"""
import os,json,struct,hashlib
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,strong_party
from pilote_combat_mgba import battle_keys
Q=ROOT/os.environ.get('YOKAI_RESIDUAL_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON/ETAPE_B/jalon4/residuel-public');Q.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;poison=False;pending=False;started=False;hpp=[]
try:
 strong_party(r)
 for i,m in enumerate([C['MOVE_TOXIC'],C['MOVE_SPLASH'],0,0]):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],m,i)
 r.call('SpiratonBattleArmPrototype');r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',744));r.call('StartTrainerBattle')
 for f in range(30000):
  keys=battle_keys(r,f)
  if poison and f%16==0 and r.u32(r.symbols['gBattlerControllerFuncs']) in r.qa_move_callbacks:
   # Controller chooses Splash after one successful Toxic, leaving the boss HP
   # reduction to native poison damage, not an attack or test write.
   cursor=r.read(r.symbols['gMoveSelectionCursor'],1)[0];r.qa_next_keys={7} if cursor!=1 else {8};keys=r.qa_next_keys
  r.keys=keys;r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   started=True;mon=r.read(r.symbols['gBattleMons']+88,88);level=mon[42];hp=int.from_bytes(mon[40:42],'little');status=int.from_bytes(mon[76:80],'little')
   if level==56 and r.read(r.symbols['sFirst'],1)==b'\0' and status&0x80:
    poison=True
    if not hpp or hp!=hpp[-1]:hpp.append(hp)
   if poison and hp==0 and level==56:pending=True
   if poison and level==57 and r.u32(r.symbols['gBattleMainFunc'])!=(r.symbols['TransformStep']|1):
    assert pending and status==0 and hp>0,(pending,status,hp)
    r.frame.save(Q/'nouvelle-forme-apres-toxic.png');passed=True;break
  elif started:raise AssertionError('Battle ended before residual transition')
 assert passed,(poison,pending,hpp)
finally:
 if not passed:r.frame.save(Q/'diagnostic.png')
 (Q/'RESIDUEL_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),toxic_applied_by_native_move=poison,zero_hp_pending_seen=pending,hp_observed=hpp),indent=2)+'\n');r.close()
print('PASS: native Toxic exhausts first full layer, end-turn morph clears status and refills next life')

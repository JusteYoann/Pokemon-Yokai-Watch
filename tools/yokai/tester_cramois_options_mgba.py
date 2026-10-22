#!/usr/bin/env python3
"""Actual old Nathaniel rematch/reward and past shop purchase; not balance."""
import hashlib,json
from mgba_new_game import new_game
from tester_cramois_scenario_mgba import *
rows=[]
r=new_game()
try:
 party(r);warp(r,*MAPS['CinnabarPast_Mart'],4,3);face_a(r,'L')
 for f in range(1800):r.keys={8} if f%16<4 else set();r.run()
 assert r.call('CheckBagHasItem',C['ITEM_POTION'],1)
 lv.s.decline(r);assert location(r)==MAPS['CinnabarPast_Mart']
 r.frame.save(OUT/'boutique-achat.png')
 rows.append({'test':'Actual past shop counter and native purchase menus: Potion purchased by controller A, B exits to field','passed':True})
finally:r.close()
r=new_game()
try:
 party(r);r.call('FlagSet',0x30B);warp(r,*MAPS['CinnabarIsland_Gym'],7,6)
 assert r.call('AddBagItem',C['ITEM_LEAF_STONE'],999)
 face_a(r,'U');finish(r);assert not flag(r,0x30C)
 r.call('RemoveBagItem',C['ITEM_LEAF_STONE'],1);face_a(r,'U');finish(r);assert flag(r,0x30C) and r.call('CheckBagHasItem',C['ITEM_LEAF_STONE'],999)
 before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
 save_continue(r);assert flag(r,0x30C)
 rows.append({'test':'Historic earned Leaf Stone before postgame: full-stack refusal, retry without fight, no duplicate and Flash persistence','passed':True})
finally:r.close()
r=new_game()
try:
 p=r.symbols['gPlayerParty'];r.call('CreateMon',p,149,100,31,1,100,0,0);r.call('SetMonMoveSlot',p,C['MOVE_AERIAL_ACE'],0)
 for field in [57,58,59,60,61,62,63]:r.write(r.PARAMS+100,(999).to_bytes(2,'little'));r.call('SetMonData',p,field,r.PARAMS+100)
 r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.call('SetLastHealLocationWarp',9);r.call('FlagSet',0x82C)
 warp(r,*MAPS['CinnabarIsland_Gym'],7,6);face_a(r,'U');lv.s.decline(r);assert not flag(r,0x30D)
 face_a(r,'U');frames=lv.s.t.az.a.fight(r,'nathaniel-age',expected=[(149,59),(148,60),(35,61),(67,62),(20,63),(40,64)])
 assert flag(r,0x30D) and flag(r,0x30B) and flag(r,0x30C) and not flag(r,0x346) and not flag(r,0x826)
 save_continue(r);assert pos(r)==(7,6) and flag(r,0x30D)
 rows.append({'test':'Actual optional elderly Nathaniel postgame six-member rematch, No/Yes, original unique reward, no temporal trophy or native seventh, Flash persistence','passed':True,'battle_frames':frames,'fixture':'Hovernyan100 and HP/stats999: explicit event-flow check, not balance'})
finally:r.close()
(OUT/'TEST_OPTIONS_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Explicit old reward/postgame/boosted rematch fixtures, real menus and native battle; not balance or full adventure','results':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Deterministic regression: old A-only driver stalls at zero PP, legal-move driver wins.

This fixture starts with a legitimately exhausted party move; it does not force
an enemy to use Grudge and does not change any enemy team or game ROM data.
"""
import hashlib,json
import tester_cameos_boss_mgba as boss
from mgba_rpc import ROOT
spec=json.loads((ROOT/'data/yokai/cameos_boss.json').read_text());actor=next(a for a in spec['actors'] if a['name']=='DonMorleone');group={'name':'morleone','map':114,'boss':actor};r=boss.fixture(group)
try:
 # Isolate the controller test; actual prerequisite victories are covered elsewhere.
 for f in actor['need']:r.call('FlagSet',boss.C[f])
 scratch=r.PARAMS+128;r.w32(scratch,0);r.call('SetMonData',r.symbols['gPlayerParty'],boss.C['MON_DATA_PP1'],scratch)
 assert r.call('GetMonData',r.symbols['gPlayerParty'],boss.C['MON_DATA_PP1'],0)==0
 boss.interact(r)
 for f in range(3500):r.keys={8} if f%16<4 else set();r.run()
 assert r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.read(r.symbols['gBattleOutcome'],1)==b'\x00'
 assert r.read(r.symbols['gBattleMons']+0x24,1)==b'\x00'
 r.keys=set();r.frame.save(boss.P/'pilote-pp-ancien-bloque.png')
 frames=boss.fight(r,boss.C[actor['won']],'pilote-pp-corrige')
 assert r.call('FlagGet',boss.C[actor['won']]) and r.call('CheckBagHasItem',boss.C['ITEM_NUGGET'],3)
 fallbacks=[x for result in boss.results for x in result.get('fallbacks',[])]
 assert any(x['pp'][0]==0 and x['unusable_mask']&1 and x['to_slot']!=0 for x in fallbacks),fallbacks
 r.frame.save(boss.P/'pilote-pp-corrige-victoire.png')
 report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Party fixture at level100/999stats with four attacking moves, first move initially PP0; boss prerequisite flags set only to isolate driver; actual optional Don Morleone battle and reward through native controller input. Enemy teams unchanged. Not a Grudge move-execution or balance test.','old_A_only_driver_stalls_on_legally_exhausted_first_move':True,'new_driver_uses_native_CheckMoveLimitations_and_dpad_only':True,'new_driver_completes_real_boss_battle_and_reward':True,'fallbacks':fallbacks,'controller_loop_iterations_to_win':frames,'passed':True}
 (ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_PILOTE_PP_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
finally:r.close()

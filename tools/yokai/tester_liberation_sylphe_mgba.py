#!/usr/bin/env python3
"""Actual original Giovanni coordinate event; music restores without a manual call.

Fixture warps/strong party and initial progression flags, no team or win injection.
"""
import hashlib,json
import tester_musiques_integrees_mgba as t
r=t.boss.fixture({'map':57,'boss':{'x':6,'y':15}})
try:
 r.call('FlagClear',t.boss.C['FLAG_HIDE_SILPH_ROCKETS']);r.call('FlagClear',0x82C)
 # Use the canonical progression variable for the isolated original event.
 import re
 vars={k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)',(t.ROOT/'include/constants/vars.h').read_text(),re.M)}
 r.call('VarSet',vars['VAR_MAP_SCENE_SILPH_CO_11F'],0);t.boss.warp(r,{'map':57},{'x':6,'y':15});t.wait_header(r,11)
 before=r.call('GetGameStat',9);r.keys={4};r.run(16);r.keys=set();r.run(16)
 # The real coordinate script approaches, talks, fights and removes the Rockets.
 frames=t.boss.fight(r,t.boss.C['FLAG_HIDE_SILPH_ROCKETS'],'audio-liberation-sylphe');r.run(300)
 assert r.call('GetGameStat',9)==before+1 and r.call('FlagGet',t.boss.C['FLAG_HIDE_SILPH_ROCKETS'])
 assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_silph']
 assert r.call('VarGet',vars['VAR_MAP_SCENE_SILPH_CO_11F'])==1
 r.frame.save(t.P/'preuves'/'sylphe-apres-giovanni-musique-normale.png')
 report={'passed':True,'private_rom_sha256':hashlib.sha256(t.rom.read_bytes()).hexdigest(),'scope':'Actual original coordinate-triggered Giovanni2 script and trainer battle; fixture warp/strong party, not full Silph puzzle progression','occupied_private_theme_before':11,'native_liberated_theme_after':'mus_silph','explicit_music_call_in_test_after_victory':False,'original_teams_and_reward_scripts_unchanged':True,'frames':frames}
 (t.P/'TEST_LIBERATION_SYLPHE_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
finally:r.close()

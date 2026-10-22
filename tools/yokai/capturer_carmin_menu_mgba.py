#!/usr/bin/env python3
"""Native settled action-menu capture after interacting with Ariane.

Fixture party Jibanyan24, second trophy and solved-switch flag; not a puzzle or
full-battle test. No battle outcome, graphic data, palette or cursor is written.
"""
import hashlib,json,os,subprocess
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
OUT=ROOT/'QA_RECETTE_FINALE/CARMIN_2026_10_22';r=new_game(1)
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,24,15,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.call('FlagSet',0x821);r.call('FlagSet',0x264)
 r.call('SetWarpDestination',9,6,255,5,3);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 r.keys={4};r.run(4);r.keys=set();r.run(12);r.keys={8};r.run(2);r.keys=set();r.run(12)
 callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
 for f in range(12000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Native action menu was not reached')
 r.keys=set();r.run(30);r.frame.save(OUT/'combat-menu-natif.png')
 assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&65535==416
 assert r.call('GetMonData',r.symbols['gEnemyParty'],11,0)==96
 assert r.call('GetBattleBGM')==377
 expected=r.call('YokaiGetSongHeader',377,r.u32(r.symbols['gSongTable']+8*377))
 assert r.u32(r.symbols['gMPlayInfo_BGM'])==expected
 mask=r.call('YokaiGetPrivateAudioMask');available=bool(mask&(1<<30))
 report=dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),trainer=416,actual_first_enemy=96,battle_bgm_id=377,private_ariane_slot_available=available,native_mixer_header_matches_configured_theme=True)
 (OUT/'TEST_MENU_COMBAT_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
finally:r.close()

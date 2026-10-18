#!/usr/bin/env python3
"""Actual wild battle controller win, permanent EXP share and exploration BGM return.

New-game intro is real. Warp, player level and enemy species are explicit fixtures.
No enemy HP/PP, outcomes or EXP are written during the fight. Audio stays private.
"""
import ctypes,hashlib,json,os,re,wave
from pathlib import Path
import numpy as np
from mgba_rpc import ROOT,BATCH
from mgba_new_game import new_game
from pilote_combat_mgba import battle_keys
from auditer_niveaux_audio_post_b13 import measure
P=ROOT/'QA_RECETTE_FINALE/POST_B13/audio/transition-sauvage';P.mkdir(parents=True,exist_ok=True)
private=Path(os.environ['YOKAI_TRANSITION_PRIVATE']).resolve();assert not private.is_relative_to(ROOT);private.mkdir(parents=True,exist_ok=True)
C={}
for file in ['pokemon','moves']:
 C.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\b',(ROOT/f'include/constants/{file}.h').read_text(),re.M)})
r=new_game();passed=False;error='Interrupted';blocks=[];seen=[];observations=[]
callback=BATCH(lambda p,n:(blocks.append(ctypes.string_at(p,n*4)) or n));r.lib.retro_set_audio_sample_batch(callback)
def capture(label):
 path=private/(label+'.wav')
 with wave.open(str(path),'wb') as f:f.setparams((2,2,65536,0,'NONE',''));f.writeframes(b''.join(blocks))
 blocks.clear();observations.append(dict(phase=label,**measure(path)));r.frame.save(P/(label+'.png'))
try:
 for i,(sid,level) in enumerate([(1,70),(5,10)]):r.call('CreateMon',r.symbols['gPlayerParty']+i*100,sid,level,31,1,100,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\x02');r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0)
 before=r.call('GetMonData',r.symbols['gPlayerParty']+100,C['MON_DATA_EXP'],0)
 g=json.loads((ROOT/'data/maps/map_groups.json').read_text());name='MtMoon_1F';group,num=next((i,j) for i,key in enumerate(g['group_order']) for j,n in enumerate(g[key]) if n==name)
 r.call('SetWarpDestination',group,num,255,14,8);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 blocks.clear();r.run(720);assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_24'];capture('01-exploration')
 r.call('CreateMon',r.symbols['gEnemyParty'],9,8,31,1,101,0,0);r.write(r.symbols['gEnemyPartyCount'],b'\x01');r.call('StartWildBattle')
 for frame in range(6000):
  r.keys={0} if frame%16<2 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.read(r.symbols['gBattleCommunication'],1):
   if r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_28']:break
 else:raise AssertionError('Battle28 never reached')
 r.keys=set();r.run(720);assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_28'];capture('02-combat')
 for frame in range(16000):
  r.keys=battle_keys(r,frame);r.run();header=r.u32(r.symbols['gMPlayInfo_BGM'])
  if not seen or seen[-1]['header']!=hex(header):seen.append(dict(frame=frame,header=hex(header)))
  if frame>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==b'\x01':break
 else:raise AssertionError('Controller victory did not return to field')
 r.keys=set();r.run(300);capture('03-victoire-retour')
 after=r.call('GetMonData',r.symbols['gPlayerParty']+100,C['MON_DATA_EXP'],0);assert after>before,('Permanent party EXP not received',before,after)
 assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_24'];assert r.u32(r.symbols['gSoundInfo'])==0x68736D53
 r.run(720);capture('04-exploration-reprise');assert all(o['raw_clipped_samples']==0 for o in observations)
 passed=True;error=None
except BaseException as e:error=str(e);raise
finally:
 report=dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Real intro then explicit map/party/enemy fixture; native StartWildBattle, actual controller win, quiet ally receives EXP without participating, exploration sample24 returns. Private audio captured at constant emulator settings; no subjective listening or full adventure claim',idle_ally_exp_before=locals().get('before'),idle_ally_exp_after=locals().get('after'),observed_music_headers=seen,measurements=observations);r.close();(P/'TEST_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))

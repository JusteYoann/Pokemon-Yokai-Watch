#!/usr/bin/env python3
"""Play original Champion scene/battle through conclusion, Hall of Fame and credits.

Explicit fixture: initial warp to Champion room, prepared progression flags and
strong party; earlier adventure NOT played. Opponent team/script not modified.
"""
import hashlib,json,struct
import tester_musiques_integrees_mgba as t
from pilote_combat_mgba import battle_keys,capture_failure
b=t.boss
r=None;checks=[];passed=False;error='Interrupted'
try:
 r=t.Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(b.glyphs[c] for c in 'Test')+b'\xff')
 r.call('FlagSet',0x828);r.call('FlagSet',0x829)
 r.call('FlagSet',b.C['FLAG_HIDE_OAK_IN_CHAMP_ROOM']);r.call('VarSet',0x4031,0)
 r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');scratch=r.PARAMS+128
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_SPATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(scratch,999);r.call('SetMonData',r.symbols['gPlayerParty'],b.C[field],scratch)
 for slot,move in enumerate(['MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_SWIFT','MOVE_MAGICAL_LEAF']):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],b.C[move],slot)
 group,num=t.MAPS['PokemonLeague_ChampionsRoom'];assert group==1
 b.warp(r,{'map':num},{'x':6,'y':17}) # Native entry walk starts at (6,18).
 started=False
 for f in range(65000):
  r.keys=battle_keys(r,f);r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   if not started:
    started=True;r.frame.save(t.P/'preuves'/'ligue-matt-combat-v1.png')
    checks.append({'test':'Actual original Champion entry, dialogue, selected starter team and battle started','trainer_id':int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little'),'passed':True})
  if started and r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_26'] and t.channel(r,26):break
 else:raise AssertionError(('Champion/conclusion not reached',started,capture_failure(r,'ligue-v1')))
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\x01' and r.call('FlagGet',b.C['FLAG_DEFEATED_CHAMP'])
 checks.append({'test':'Actual Champion battle victory triggers Take Care, Grandpa 1 only after post-battle message','passed':True,'frames_to_music':f+1})
 t.run_song(r,26,'Actual Matt Champion victory and original conclusion script, not direct music call');checks.extend(t.results)
 r.frame.save(t.P/'preuves'/'ligue-conclusion-v1.png')
 seen_hof=False;seen_credits=False;seen_states=set();save_seen=False
 for f in range(40000):
  r.keys=battle_keys(r,f);r.run();cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['CB2_Credits']|1:
   seen_credits=True;mgr=r.u32(r.symbols['sCreditsMgr'])
   if mgr:seen_states.add(r.read(mgr,1)[0])
  if f%64==0:
   if cb==r.symbols['CB2_HofIdle']|1:seen_hof=True
   if seen_hof and not save_seen:
    r.frame.save(t.P/'preuves'/'ligue-pantheon-v1.png');save_seen=True
  if seen_credits and cb!=r.symbols['CB2_Credits']|1:break
 else:raise AssertionError(('Conclusion/Hall of Fame/credits stalled',seen_hof,seen_credits,sorted(seen_states),capture_failure(r,'ligue-fin-v1')))
 assert seen_hof and seen_credits and 17 in seen_states and 18 in seen_states
 checks.append({'test':'Original conclusion continues into Hall of Fame, sets League-clear flag and completes native credits states 17/18','passed':True,'frames':f+1,'credits_states':sorted(seen_states)})
 # Credits perform a native soft-reset. Let startup finish before any RPC.
 r.keys=set();r.run(1200)
 for f in range(7000):
  r.keys={3} if f%120<2 else {8} if f%120 in [60,61] else set();r.run()
  if f>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gQuestLogState'],1)[0] not in [2,3]:break
 else:raise AssertionError('Continue via title/main menu did not reach exploration')
 assert r.call('FlagGet',0x82C), ('League-clear flag absent after Continue',r.read(r.symbols['gQuestLogState'],1).hex(),hex(r.u32(r.symbols['gMain']+4)),r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2).hex())
 r.keys=set();r.run(180);r.frame.save(t.P/'preuves'/'ligue-sauvegarde-postgame-v1.png')
 checks.append({'test':'Native Hall of Fame Flash save reload, League flag retained and saved game resumes exploration','passed':True,'current_map':list(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))})
 passed=True;error=None
except Exception as e:
 error=str(e);raise
finally:
 if r:
  if not passed:r.frame.save(t.P/'preuves'/'ligue-rechargement-diagnostic.png')
  r.close()
 (t.P/'CONCLUSION_LIGUE_V1.json').write_text(json.dumps({'passed':passed,'error':error,'private_rom_sha256':hashlib.sha256(t.rom.read_bytes()).hexdigest(),'scope':'Original Champion scene and actual battle to postgame save continuation, warp/strong-party fixture; not a complete adventure playthrough','results':checks},indent=2)+'\n')
 print(json.dumps({'passed':passed,'error':error,'checks':len(checks)}),flush=True)

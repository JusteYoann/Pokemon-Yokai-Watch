#!/usr/bin/env python3
"""Actual original scientist/Dojo and optional employee fights with new music."""
import hashlib,json,re
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from pilote_combat_mgba import battle_keys
P=ROOT/'QA_RECETTE_FINALE/AUDIO_30MIO/evenements';P.mkdir(parents=True,exist_ok=True)
C={}
for file in ['moves','flags','opponents']:
 C.update({k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',(ROOT/f'include/constants/{file}.h').read_text(),re.M)})
for name,target in re.findall(r'^#define\s+(TRAINER_\w+)\s+(TRAINER_\w+)\b',(ROOT/'include/constants/opponents.h').read_text(),re.M):
 if target in C:C[name]=C[target]
G=json.loads((ROOT/'data/maps/map_groups.json').read_text());M={name:(i,j) for i,key in enumerate(G['group_order']) for j,name in enumerate(G[key])}
r=new_game();rows=[];passed=False;error='Interrupted'
try:
 for i in range(1):
  r.call('CreateMon',r.symbols['gPlayerParty']+i*100,1,100,31,1,100+i,0,0)
  for slot,move in enumerate(['MOVE_FLAMETHROWER','MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_MAGICAL_LEAF']):r.call('SetMonMoveSlot',r.symbols['gPlayerParty']+i*100,C[move],slot)
 r.write(r.symbols['gPlayerPartyCount'],b'\x01');base=r.snapshot()
 cases=[('scientifique','PokemonMansion_1F',22,25,'TRAINER_SCIENTIST_TED',19),('dojo','SaffronCity_Dojo',6,6,'TRAINER_BLACK_BELT_KOICHI',10),('employe','SilphCo_11F',7,15,'TRAINER_YOKAI_EMPLOYEROUGE',20)]
 for slug,mapname,x,y,trainer,track in cases:
  # Avoid an automatic trainer-sight scene before the baseline map music
  # capture; restore its unfought state immediately before interaction.
  r.restore(base);r.call('SetTrainerFlag',C[trainer]);r.call('VarSet',0x4081,1)
  if slug=='employe':
   # Water starter fixture avoids feeding Flash Fire with the fire fixture's
   # first move; no opposing stats, moves, PP or outcome are changed.
   r.call('CreateMon',r.symbols['gPlayerParty'],87,100,31,1,100,0,0)
   for slot,move in enumerate(['MOVE_SURF','MOVE_ICE_BEAM','MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE']):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C[move],slot)
   for flag in [0x82C,C['FLAG_HIDE_SILPH_ROCKETS'],C['FLAG_SILPH_11F_DOOR']]:r.call('FlagSet',flag)
  g,n=M[mapname];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
  field=r.u32(r.symbols['gMPlayInfo_BGM']);r.frame.save(P/f'{slug}-exploration.png')
  if slug=='dojo':assert field==r.symbols['mus_yokai_09']
  r.call('ClearTrainerFlag',C[trainer])
  # Current trainer encounter hook itself, without changing the script mode:
  # the real interaction below additionally verifies battle theme selection.
  if slug=='scientifique':
   r.write(r.symbols['gTrainerBattleOpponent_A'],C[trainer].to_bytes(2,'little'));r.call('PlayTrainerEncounterMusic');r.run(60)
   assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_18'];r.frame.save(P/'scientifique-rencontre.png')
   r.call('Overworld_ChangeMusicToDefault');r.run(180)
  r.keys={4};r.run(8);r.keys=set();r.run(20)
  started=False;music_seen=False;music_at=None;captured=False
  for f in range(60000):
   if not started:r.keys={8} if f%16<4 else set()
   else:r.keys=battle_keys(r,f)
   r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
    if not started:
     started=True
    if r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{track:02d}'] and not music_seen:
     music_seen=True;music_at=f
    if music_seen and not captured and f>=music_at+180:r.frame.save(P/f'{slug}-combat.png');captured=True
   if started and f>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==b'\x01':break
   if started and r.read(r.symbols['gBattleOutcome'],1)==b'\x02':raise AssertionError((slug,'Prepared player lost the battle'))
  else:raise AssertionError((slug,'Native battle did not finish',started,music_seen))
  assert music_seen,(slug,'Wrong battle music')
  for f in range(1800):r.keys={0} if f%16<4 else set();r.run()
  r.keys=set();r.run(180);assert r.u32(r.symbols['gMPlayInfo_BGM'])==field,(slug,'Exploration music not restored')
  assert r.call('HasTrainerBeenFought',C[trainer]);r.frame.save(P/f'{slug}-retour.png');rows.append(dict(event=slug,map=mapname,trainer=trainer,battle_slot=track,actual_original_interaction=True,controller_victory=True,field_music_restored=True,encounter_hook_checked=slug=='scientifique',passed=True));print('EVENT PASS',slug,flush=True)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows,scope='Real new game, explicit warp/progression/item/party preparation; original map NPC interaction and native battles won through controller. Scientist encounter hook also called directly as a fixture. Not the four unimplemented recurring-scientist quests or Coach Antonic scene.'),indent=2)+'\n')

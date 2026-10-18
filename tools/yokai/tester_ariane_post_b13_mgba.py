#!/usr/bin/env python3
"""Real NPC interaction, optional battle, full-bag reward retry and rematch in mGBA."""
import csv,hashlib,json,re,os
from pathlib import Path
from mgba_rpc import Emulator,ROOT
from mgba_new_game import new_game
C={}
for name in ['pokemon','items','moves','opponents']:
 C.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*(?:$|//)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
P=Path(os.environ.get('YOKAI_ARIANE_REPORT',str(ROOT/'QA_RECETTE_FINALE/POST_B13/audio/ariane')));P.mkdir(parents=True,exist_ok=True);proof=P/'preuves';proof.mkdir(exist_ok=True)
results=[]
r=new_game()
def flag(n):return r.call('FlagGet',n)
def finish_dialogue(limit=10000):
 # Wait for the script's actual end rather than assuming a fixed text duration.
 for frame in range(limit):
  r.keys={0} if frame%16<4 else set();r.run()
  if frame>60 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:
   r.keys=set();r.run(16);return frame
 raise AssertionError('NPC dialogue did not reach an unlocked field state')
def interact():
 # Real directional input; retry A after movement/message input cooldown.
 r.keys=set();r.run(60)
 r.keys={4};r.run(8);r.keys=set();r.run(16)
 for attempt in range(8):
  r.keys={8};r.run(2);r.keys=set();r.run(8)
  if r.read(r.symbols['sGlobalScriptContextStatus'],1)!=b'\x02':
   r.run(8);assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_31'];return
 raise AssertionError('A interaction did not start an NPC script after eight presses')
def fight_until(victory_flag,limit=18000):
 started=False;music_seen=False
 for frame in range(limit):
  r.keys={8} if frame%16<4 else set();r.run()
  if frame%64==0:
   callback=r.u32(r.symbols['gMain']+4)
   if callback==r.symbols['BattleMainCB2']|1:
    started=True
    music_seen |= r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_28']
   if frame==1024:r.frame.save(proof/'ariane-combat.png')
   if started and flag(victory_flag) and r.read(r.symbols['gBattleOutcome'],1)==b'\x01' and callback==r.symbols['CB2_Overworld']|1:
    assert music_seen, "Battle music28 never observed during actual fight"
    r.keys=set();finish_dialogue();r.run(300);assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_27'];return frame
 raise AssertionError(('Battle/script failed to return with victory flag',hex(victory_flag),started))
try:
 # A real controller intro has initialized field and audio.
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Nathan')+b'\xff')

 # Fixture starts outside the original trainers' sight ranges.
 r.call('SetWarpDestination',3,44,255,57,8);r.call('WarpIntoMap')
 r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(180)
 r.frame.save(proof/'ariane-usapion-route25.png')
 r.call('CreateMon',r.symbols['gPlayerParty'],5,10,31,1,100,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 before_no=r.call('GetGameStat',9)
 interact();finish_dialogue();r.run(300);assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_27']
 assert r.call('GetGameStat',9)==before_no
 initial_fixture=r.snapshot()
 assert flag(0x300)==0 and flag(0x301)==0 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
 results.append({'test':'Actual A interaction then No: no fight and no victory/reward flags','passed':True})
 # Script/transition fixture only: intentionally overpower the party, not an equilibrium test.
 party=r.symbols['gPlayerParty'];scratch=r.PARAMS+128
 r.call('CreateMon',party,1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(scratch,999);r.call('SetMonData',party,C[field],scratch)
 r.call('SetMonMoveSlot',party,C['MOVE_AERIAL_ACE'],0)
 r.call('ClearBag');filled=[]
 for item in range(1,347):
  if item==C['ITEM_MOON_STONE'] or r.call('GetPocketByItemId',item)!=1:continue
  if r.call('AddBagItem',item,1):filled.append(item)
  if len(filled)==42:break
 assert len(filled)==42 and not r.call('CheckBagHasSpace',C['ITEM_MOON_STONE'],1)
 interact();frames=fight_until(0x300)
 assert flag(0x301)==0 and not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],1)
 results.append({'test':'Win actual adventure battle with full bag: victory retained, reward pending','frames':frames,'passed':True})
 assert r.call('RemoveBagItem',filled[0],1)
 assert r.call('CheckBagHasSpace',C['ITEM_MOON_STONE'],1)
 interact();finish_dialogue()
 assert flag(0x301)==1 and r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],1)
 assert not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],2)
 interact();finish_dialogue()
 assert not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],2)
 results.append({'test':'Retry reward without another battle; one Moon Stone, no duplicate on revisit','passed':True})
 r.call('FlagSet',0x82C)
 interact();frames=fight_until(0x302)
 assert flag(0x301)==1 and not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],2)
 assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&0xFFFF==2
 results.append({'test':'Post-League rematch selects five-member team; unique reward preserved','frames':frames,'passed':True})
 assert r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02', 'Script did not terminate after battle'
 assert r.u32(r.symbols['sGlobalScriptContext']+8)==0
 r.frame.save(proof/'ariane-apres-revanche.png')
 # Flash persists the independent battle/reward flags.
 assert r.call('TrySavingData',0,max_frames=1200)==1
 for f in [0x300,0x301,0x302]:r.call('FlagClear',f)
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 assert all(flag(f) for f in [0x300,0x301,0x302])
 results.append({'test':'Ariane battle/reward/rematch flags survive native Flash reload','passed':True})
 # Same completed cameo may be challenged repeatedly after League.
 r.call('HealPlayerParty')
 before=r.call('GetGameStat',9)
 interact();frames=fight_until(0x302)
 assert r.call('GetGameStat',9)==before+1
 assert not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],2)
 results.append({'test':'Second voluntary postgame rematch really starts and completes; no duplicate reward','frames':frames,'passed':True})
 # Emulator snapshot is fixture setup only, never evidence of persistence.
 r.restore(initial_fixture)
 r.call('FlagSet',0x82C)
 r.call('CreateMon',party,1,100,31,1,100,0,0)
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(scratch,999);r.call('SetMonData',party,C[field],scratch)
 r.call('SetMonMoveSlot',party,C['MOVE_AERIAL_ACE'],0)
 interact();frames=fight_until(0x302)
 assert flag(0x300) and flag(0x301) and flag(0x302)
 assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&0xFFFF==2
 results.append({'test':'First ever Ariane encounter after League directly uses postgame team and gives unique reward','frames':frames,'passed':True})
 r.restore(initial_fixture)
 r.call('CreateMon',party,5,1,0,1,100,0,0)
 r.call('SetMonMoveSlot',party,C['MOVE_TACKLE'],0)
 r.w32(scratch,1);r.call('SetMonData',party,C['MON_DATA_HP'],scratch)
 interact();started=False;returned=False;music_seen=False
 for frame in range(15000):
  r.keys={8} if frame%16<4 else set();r.run()
  if frame%64==0:
   callback=r.u32(r.symbols['gMain']+4)
   if callback==r.symbols['BattleMainCB2']|1:
    started=True
    music_seen |= r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_28']
   if started and callback==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==b'\x02':returned=True;break
 assert returned,'Defeat did not return from whiteout'
 assert music_seen,'Battle28 never observed during defeat case'
 r.keys=set();r.run(60)
 assert flag(0x300)==0 and flag(0x301)==0 and flag(0x302)==0
 assert not r.call('CheckBagHasItem',C['ITEM_MOON_STONE'],1)
 results.append({'test':'Real player defeat and whiteout: no victory or reward flags and no item granted','passed':True})
 r.frame.save(proof/'ariane-defaite-sans-recompense.png')

finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),
 'scope':'Actual NPC interaction on Route25, ordinary controller input through fights and dialogs; fixture warp to Route25, level100/999-stat party for transition tests, normal weak party for defeat case',
 'balance_validated':False,'results':results,'remaining':['Other cameos','Full story traversal','Balanced party difficulty assessment']}
(P/'TEST_ARIANE_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

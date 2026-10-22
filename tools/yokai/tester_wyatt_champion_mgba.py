#!/usr/bin/env python3
"""Argenta/Wyatt: real controller battles on a warp fixture, not a full adventure."""
import hashlib,json,os,re,subprocess
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
Q=ROOT/'QA_RECETTE_FINALE/SCENARIO_2026_10_22/wyatt';Q.mkdir(exist_ok=True)
C={}
for name in ['pokemon','items','moves','species','opponents']:
 C.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*(?:$|//)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
rows=[]
def finish(r):
 for f in range(10000):
  r.keys={0} if f%16<4 else set();r.run()
  if f>60 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:
   r.keys=set();r.run(16);return
 raise AssertionError('Field dialogue did not finish')
def interact(r):
 r.keys=set();r.run(60);r.keys={4};r.run(8);r.keys=set();r.run(16)
 for _ in range(8):
  r.keys={8};r.run(2);r.keys=set();r.run(8)
  if r.read(r.symbols['sGlobalScriptContextStatus'],1)!=b'\x02':return
 raise AssertionError('Leader not interactable')
def fixture(gender,weak=False):
 r=new_game(gender)
 r.call('CreateMon',r.symbols['gPlayerParty'],1,1 if weak else 100,31,1,100,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 for slot in range(4):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_SPLASH'] if weak else C['MOVE_AERIAL_ACE'],slot)
 for name in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  scratch=r.PARAMS+128;r.w32(scratch,1 if weak else 999);r.call('SetMonData',r.symbols['gPlayerParty'],C[name],scratch)
 r.call('SetWarpDestination',6,2,255,6,6);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
 visible=[r.read(r.symbols['gObjectEvents']+36*i+5,1)[0] for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1]
 assert 160 in visible and 80 not in visible,visible
 trainer=r.symbols['gTrainers']+40*C['TRAINER_LEADER_BROCK']
 assert r.read(trainer+3,1)==bytes([152])
 glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
 assert r.read(trainer+4,6)==bytes(glyph[c] for c in 'Wyatt')+b'\xff'
 return r

def fight(r,stem,loss=False):
 started=False;count=0
 for f in range(26000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   started=True;count+=1
   if count in [150,800]:r.frame.save(Q/f'{stem}-combat-{count}.png')
  if f%64==0 and started and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==bytes([2 if loss else 1]):
   if not loss and not r.call('FlagGet',0x820):continue
   r.keys=set();finish(r);return f
 r.frame.save(Q/(stem+'-diagnostic.png'));raise AssertionError(('Battle not completed',stem,started))

for gender in [0,1]:
 r=fixture(gender);stem='nathan' if gender==0 else 'katie'
 try:
  r.frame.save(Q/(stem+'-map.png'))
  # Saturate the existing TM39 stack rather than corrupting pocket slots.
  if gender==0:
   assert r.call('AddBagItem',327,999)
   assert not r.call('CheckBagHasSpace',327,1)
  interact(r);frames=fight(r,stem)
  assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&65535==414
  assert r.call('FlagGet',0x4B0) and r.call('FlagGet',0x820)
  if gender==0:
   assert not r.call('FlagGet',0x254)
   assert r.call('RemoveBagItem',327,999)
   before=r.call('GetGameStat',9);interact(r);finish(r)
   assert r.call('GetGameStat',9)==before
  assert r.call('FlagGet',0x254) and r.call('CheckBagHasItem',327,1)
  assert not r.call('CheckBagHasItem',327,2)
  before=r.call('GetGameStat',9);interact(r);finish(r)
  assert r.call('GetGameStat',9)==before and not r.call('CheckBagHasItem',327,2)
  r.frame.save(Q/(stem+'-apres.png'))
  assert r.call('TrySavingData',0,max_frames=1200)==1
  for flag in [0x4B0,0x820,0x254]:r.call('FlagClear',flag)
  assert r.call('LoadGameSave',0,max_frames=1200)==1
  assert all(r.call('FlagGet',flag) for flag in [0x4B0,0x820,0x254])
  assert r.call('CheckBagHasItem',327,1)
  rows.append(dict(test=stem,passed=True,frames=frames,correct_overworld=True,correct_trainer_identity=True,real_controller_victory=True,trophy_and_tm39=True,tm39_unique=True,full_tm_stack_retry=gender==0,native_flash_reload=True));print('PASS',stem,flush=True)
 finally:r.close()
r=fixture(0,weak=True)
try:
 interact(r);frames=fight(r,'defaite',loss=True)
 assert not any(r.call('FlagGet',f) for f in [0x4B0,0x820,0x254])
 assert not r.call('CheckBagHasItem',327,1)
 rows.append(dict(test='Defeat/whiteout grants no trophy or reward',passed=True,frames=frames));print('PASS defeat',flush=True)
finally:r.close()
# Independently check the native Champion party against the locked data.
r=new_game()
try:
 expected=json.loads((ROOT/'data/yokai/equipes_boss_validees.json').read_text())['TRAINER_LEADER_BROCK']['party']
 r.w32(r.symbols['gBattleTypeFlags'],8)
 assert r.call('CreateNPCTrainerParty',r.symbols['gEnemyParty'],414)==len(expected)
 for i,mon in enumerate(expected):
  ptr=r.symbols['gEnemyParty']+100*i
  def get(key):return r.call('GetMonData',ptr,C['MON_DATA_'+key],0)
  assert get('SPECIES')==C[mon['species']] and get('LEVEL')==mon['level']
  assert get('HELD_ITEM')==C[mon['held_item']] and get('ABILITY_NUM')==mon['ability_num']
  assert [get('MOVE'+str(i)) for i in range(1,5)]==[C[v] for v in mon['moves']]
 rows.append(dict(test='Native party matches locked species, levels, moves, abilities and items',passed=True,members=len(expected)))
finally:r.close()
report=dict(passed=True,rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),scope=__doc__,fixtures='Fresh real new-game for each gender, warp to Gym, level100/999stats party for victory or level1/1HP for defeat; not a balance or access-through-story test.',results=rows)
(Q/'TEST_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)

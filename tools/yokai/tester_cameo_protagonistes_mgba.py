#!/usr/bin/env python3
"""Real opposite-protagonist NPC interaction, battles and one-time reward in mGBA."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
P=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves';results=[]
C={}
for name in ['pokemon','items','moves','species']:
 C.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*(?:$|//)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}

def fixture(gender,post,weak=False):
 r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Test')+b'\xff');r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
 if post:r.call('FlagSet',0x82C)
 r.call('CreateMon',r.symbols['gPlayerParty'],1,1 if weak else 100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 scratch=r.PARAMS+128
 for f in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(scratch,1 if weak else 999);r.call('SetMonData',r.symbols['gPlayerParty'],C[f],scratch)
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_TACKLE'] if weak else C['MOVE_AERIAL_ACE'],0)
 r.call('SetWarpDestination',3,6,255,25,14);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1800):
  r.run()
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 r.run(120);return r

def finish(r):
 for f in range(10000):
  r.keys={0} if f%16<4 else set();r.run()
  if f>60 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:
   r.keys=set();r.run(16);return
 raise AssertionError('Dialogue not finished')
def interact(r):
 r.keys=set();r.run(60);r.keys={4};r.run(8);r.keys=set();r.run(16)
 for _ in range(8):
  r.keys={8};r.run(2);r.keys=set();r.run(8)
  if r.read(r.symbols['sGlobalScriptContextStatus'],1)!=b'\x02':return
 raise AssertionError('NPC not interactable')
def fight(r,flag,stem,loss=False):
 started=False
 for f in range(25000):
  r.keys={8} if f%16<4 else set();r.run()
  if f%64==0:
   cb=r.u32(r.symbols['gMain']+4)
   if cb==r.symbols['BattleMainCB2']|1:started=True
   if f==1024:r.frame.save(P/(stem+'-combat.png'))
   if started and cb==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==bytes([2 if loss else 1]):
    if not loss and not r.call('FlagGet',flag):continue
    r.keys=set();finish(r);return f
 raise AssertionError(('Battle not completed',stem,started))
for gender,person in [(0,'katie'),(1,'nathan')]:
 for post in [False,True]:
  stem='cameo-'+person+('-post' if post else '-aventure');r=fixture(gender,post)
  try:
   visible=[]
   for i in range(16):
    o=r.symbols['gObjectEvents']+i*36
    if r.read(o,1)[0]&1 and r.read(o+5,1)[0] in [156,157]:visible.append(r.read(o+5,1)[0])
   assert visible==[157 if gender==0 else 156],(stem,visible)
   assert r.call('MapGridGetCollisionAt',25+7,13+7)==0,(stem,'blocked NPC tile')
   assert r.call('MapGridGetCollisionAt',25+7,14+7)==0,(stem,'blocked interaction tile')
   r.frame.save(P/(stem+'-carte.png'))
   before=r.call('GetGameStat',9);interact(r);finish(r)
   assert r.call('GetGameStat',9)==before and not r.call('FlagGet',0x306)
   results.append({'test':stem+' correct sole NPC and No declines without battle','passed':True})
   filled=[]
   if not post:
    r.call('ClearBag')
    for item in range(1,347):
     if item==C['ITEM_LEAF_STONE'] or r.call('GetPocketByItemId',item)!=1:continue
     if r.call('AddBagItem',item,1):filled.append(item)
     if len(filled)==42:break
    assert len(filled)==42 and not r.call('CheckBagHasSpace',C['ITEM_LEAF_STONE'],1)
   interact(r);frames=fight(r,0x308 if post else 0x306,stem)
   assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&65535==(5 if post else 4)+(2 if gender else 0)
   if not post:
    assert not r.call('FlagGet',0x307);assert r.call('RemoveBagItem',filled[0],1)
    interact(r);finish(r)
   assert r.call('FlagGet',0x307) and r.call('CheckBagHasItem',C['ITEM_LEAF_STONE'],1)
   assert not r.call('CheckBagHasItem',C['ITEM_LEAF_STONE'],2)
   results.append({'test':stem+' actual victory, correct adventure/post team, one Leaf Stone; full bag retry for adventure','frames':frames,'passed':True})
   if not post:
    before=r.call('GetGameStat',9);interact(r);finish(r);assert r.call('GetGameStat',9)==before
    r.call('FlagSet',0x82C)
   for rematch in range(2):
    r.call('HealPlayerParty');before=r.call('GetGameStat',9);interact(r);fight(r,0x308,stem+'-revanche-'+str(rematch))
    assert r.call('GetGameStat',9)==before+1 and not r.call('CheckBagHasItem',C['ITEM_LEAF_STONE'],2)
   assert r.call('TrySavingData',0,max_frames=1200)==1
   for f in [0x306,0x307,0x308]:r.call('FlagClear',f)
   assert r.call('LoadGameSave',0,max_frames=1200)==1
   assert all(r.call('FlagGet',f) for f in [0x306,0x307,0x308])
   results.append({'test':stem+' repeated actual postgame rematches, no duplicate reward, flags survive native Flash reload','passed':True})
  finally:r.close()
r=Emulator()
try:
 r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('NewGameInitData')
 teams=json.loads((ROOT/'data/yokai/cameo_protagonistes.json').read_text())['teams']
 assert [[m['number'] for m in t['members']] for t in teams]==[[1,8,5,87,49],[4,88,126,8,6,50],[1,8,5,87,49],[4,88,126,8,6,50]]
 for team in teams:
  r.w32(r.symbols['gBattleTypeFlags'],8)
  assert r.call('CreateNPCTrainerParty',r.symbols['gEnemyParty'],team['trainer_id'])==len(team['members'])
  for i,m in enumerate(team['members']):
   mon=r.symbols['gEnemyParty']+100*i
   assert r.call('GetMonData',mon,C['MON_DATA_SPECIES'],0)==m['number']
   assert r.call('GetMonData',mon,C['MON_DATA_LEVEL'],0)==m['level']
   assert r.call('GetMonData',mon,C['MON_DATA_HELD_ITEM'],0)==0
   assert [r.call('GetMonData',mon,C['MON_DATA_MOVE'+str(j)],0) for j in range(1,5)]==[C[x] for x in m['moves']]
   assert r.call('GetMonData',mon,C['MON_DATA_ABILITY_NUM'],0)==0
 results.append({'test':'Four native trainer parties: 22 members, exact approved species/order and adventure levels; post levels58..63, validated moves, primary abilities, no held items','passed':True})
finally:r.close()
r=fixture(0,False,True)
try:
 interact(r);fight(r,0x306,'cameo-katie-defaite',loss=True)
 assert all(not r.call('FlagGet',f) for f in [0x306,0x307,0x308]);assert not r.call('CheckBagHasItem',C['ITEM_LEAF_STONE'],1)
 results.append({'test':'Actual weak-party loss and whiteout grants no victory, reward or unlock','passed':True})
finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Real A interaction and controller-driven fights at Celadon (25,13), both genders; fixture warp, overpower party for victories, weak party for actual defeat, no savestates in Flash tests','balance_validated':False,'results':results,'remaining':['Actual trip to Celadon','Difficulty with ordinary team','Other cameo groups']}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_CAMEO_PROTAGONISTES_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

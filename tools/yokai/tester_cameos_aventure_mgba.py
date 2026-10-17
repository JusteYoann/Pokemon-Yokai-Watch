#!/usr/bin/env python3
"""Native Nathaniel/Michael and Wyatt optional encounters; approved teams and one-time gifts."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
P=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves';results=[]
C={}
for name in ['pokemon','items','moves','species']:
 C.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*(?:$|//)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}

def fixture(gender,post,area,weak=False):
 r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Test')+b'\xff');r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
 if post:r.call('FlagSet',0x82C)
 r.call('CreateMon',r.symbols['gPlayerParty'],1,1 if weak else 100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 scratch=r.PARAMS+128
 for f in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(scratch,1 if weak else 999);r.call('SetMonData',r.symbols['gPlayerParty'],C[f],scratch)
 r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_TACKLE'] if weak else C['MOVE_AERIAL_ACE'],0)
 r.call('SetWarpDestination',3,area['map'],255,area['x'],area['y']+1);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
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
areas=[{'person':'nathaniel','gender':0,'map':7,'x':27,'y':8,'gfx':158,'won':0x30B,'reward':0x30C,'postwon':0x30D,'item':C['ITEM_LEAF_STONE'],'trainer':8},
 {'person':'michael','gender':1,'map':7,'x':27,'y':8,'gfx':159,'won':0x30B,'reward':0x30C,'postwon':0x30D,'item':C['ITEM_LEAF_STONE'],'trainer':10},
 {'person':'wyatt','gender':0,'map':8,'x':9,'y':11,'gfx':160,'won':0x310,'reward':0x311,'postwon':0x312,'item':C['ITEM_WATER_STONE'],'trainer':12}]
for area in areas:
 for post in [False,True]:
  stem='cameo-'+area['person']+('-post' if post else '-aventure');print('START',stem,flush=True);r=fixture(area['gender'],post,area)
  try:
   visible=[];npc=None
   for i in range(16):
    o=r.symbols['gObjectEvents']+i*36
    if r.read(o,1)[0]&1 and r.read(o+5,1)[0] in [158,159,160]:visible.append(r.read(o+5,1)[0]);npc=o
   assert visible==[area['gfx']],(stem,visible)
   for dy in [0,1]:assert r.call('MapGridGetCollisionAt',area['x']+7,area['y']+7+dy)==0,(stem,'blocked tile',dy)
   r.frame.save(P/(stem+'-carte.png'));out=__import__('PIL.Image',fromlist=['Image']).new('RGB',(960,160))
   for i,direction in enumerate([1,2,3,4]):r.call('ObjectEventTurn',npc,direction);r.run(12);out.paste(r.frame,(240*i,0))
   out.save(P/(stem+'-directions.png'));before=r.call('GetGameStat',9);interact(r);finish(r)
   assert r.call('GetGameStat',9)==before and not r.call('FlagGet',area['won'])
   results.append({'test':stem+' sole correct NPC, four native facings, No declines','passed':True})
   filled=[]
   if not post:
    r.call('ClearBag')
    for item in range(1,347):
     if item==area['item'] or r.call('GetPocketByItemId',item)!=1:continue
     if r.call('AddBagItem',item,1):filled.append(item)
     if len(filled)==42:break
    assert len(filled)==42 and not r.call('CheckBagHasSpace',area['item'],1)
   interact(r);frames=fight(r,area['postwon'] if post else area['won'],stem)
   assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&65535==area['trainer']+int(post)
   if not post:
    assert not r.call('FlagGet',area['reward']);assert r.call('RemoveBagItem',filled[0],1);interact(r);finish(r)
   assert r.call('FlagGet',area['reward']) and r.call('CheckBagHasItem',area['item'],1)
   assert not r.call('CheckBagHasItem',area['item'],2)
   results.append({'test':stem+' actual victory, correct team, unique reward, full-bag retry on adventure','frames':frames,'passed':True})
   if not post:
    before=r.call('GetGameStat',9);interact(r);finish(r);assert r.call('GetGameStat',9)==before;r.call('FlagSet',0x82C)
   for rematch in range(2):
    r.call('HealPlayerParty');before=r.call('GetGameStat',9);interact(r);fight(r,area['postwon'],stem+'-revanche-'+str(rematch))
    assert r.call('GetGameStat',9)==before+1 and not r.call('CheckBagHasItem',area['item'],2)
   assert r.call('TrySavingData',0,max_frames=1200)==1
   for f in [area['won'],area['reward'],area['postwon']]:r.call('FlagClear',f)
   assert r.call('LoadGameSave',0,max_frames=1200)==1
   assert all(r.call('FlagGet',f) for f in [area['won'],area['reward'],area['postwon']])
   results.append({'test':stem+' repeated postgame rematches, no duplicate item, flags survive native Flash reload','passed':True});print('PASS',stem,flush=True)
  finally:r.close()
for area in [areas[0],areas[2]]:
 r=fixture(area['gender'],False,area,True)
 try:
  interact(r);fight(r,area['won'],'cameo-'+area['person']+'-defaite',loss=True)
  assert all(not r.call('FlagGet',f) for f in [area['won'],area['reward'],area['postwon']]);assert not r.call('CheckBagHasItem',area['item'],1)
  results.append({'test':area['person']+' actual defeat/whiteout gives no victory, unlock or reward','passed':True})
 finally:r.close()
# Wyatt must also remain available when Katie is the playable character.
r=fixture(1,False,areas[2])
try:
 interact(r);frames=fight(r,areas[2]['won'],'cameo-wyatt-joueuse');assert r.call('FlagGet',0x311)
 results.append({'test':'Katie player also interacts with and defeats Wyatt, receives Water Stone','frames':frames,'passed':True})
finally:r.close()
r=Emulator()
try:
 r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('NewGameInitData');teams=json.loads((ROOT/'data/yokai/cameos_aventure.json').read_text())['teams']
 assert [[m['number'] for m in t['members']] for t in teams]==[[149,52,20,34,66],[149,148,35,67,20,40],[149,52,20,34,66],[149,148,35,67,20,40],[21,117,121,146,93,96],[21,51,116,97,133,146]]
 for team in teams:
  r.w32(r.symbols['gBattleTypeFlags'],8);assert r.call('CreateNPCTrainerParty',r.symbols['gEnemyParty'],team['trainer_id'])==len(team['members'])
  for i,m in enumerate(team['members']):
   mon=r.symbols['gEnemyParty']+100*i
   assert r.call('GetMonData',mon,C['MON_DATA_SPECIES'],0)==m['number'];assert r.call('GetMonData',mon,C['MON_DATA_LEVEL'],0)==m['level'];assert r.call('GetMonData',mon,C['MON_DATA_HELD_ITEM'],0)==0
   assert [r.call('GetMonData',mon,C['MON_DATA_MOVE'+str(j)],0) for j in range(1,5)]==[C[x] for x in m['moves']];assert r.call('GetMonData',mon,C['MON_DATA_ABILITY_NUM'],0)==0
 results.append({'test':'All six native parties /34 members match approved species and order, selected levels, validated moves, primary abilities and no held items','passed':True})
finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Real controller interactions and completed battles on Fuchsia/Cinnabar maps; fixture warps, gender and postgame flags, overpower party for victories and weak party for defeats; independent instances, no savestates in Flash assertions','balance_validated':False,'results':results,'remaining':['Actual access during whole adventure','Balanced ordinary party difficulty','Domniscian and Don Morleone cameos','Private DPCM themes']}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_CAMEOS_AVENTURE_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

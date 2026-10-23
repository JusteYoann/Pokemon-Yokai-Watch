#!/usr/bin/env python3
"""Native postgame boss cameos, employees, gating, optional fights and unique rewards."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
from pilote_combat_mgba import battle_keys,capture_failure
P=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/postgame';results=[];P.mkdir(parents=True,exist_ok=True)
C={}
for name in ['pokemon','items','moves','species','flags']:
 C.update({k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*(?:$|//)',(ROOT/f'include/constants/{name}.h').read_text(),re.M)})
C.update({k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+)\s*(?:$|//)',(ROOT/'include/constants/flags.h').read_text(),re.M)})
C['FLAG_SYS_GAME_CLEAR']=0x82C # SYS_FLAGS0x800 +0x2C, pinned engine contract
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}

def fixture(group,post=True,weak=False):
 r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Test')+b'\xff')
 if post:
  for flag in [C['FLAG_SYS_GAME_CLEAR'],C['FLAG_HIDE_SILPH_ROCKETS'],C['FLAG_SILPH_11F_DOOR'],C['FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE'],C['FLAG_HIDE_FIVE_ISLAND_ROCKETS']]:r.call('FlagSet',flag)
 r.call('CreateMon',r.symbols['gPlayerParty'],1,1 if weak else 100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');scratch=r.PARAMS+128
 for f in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_SPATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(scratch,1 if weak else 999);r.call('SetMonData',r.symbols['gPlayerParty'],C[f],scratch)
 for slot,move in enumerate(['MOVE_TACKLE'] if weak else ['MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_SWIFT','MOVE_MAGICAL_LEAF']):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C[move],slot)
 warp(r,group,group['boss'])
 return r

def warp(r,group,actor):
 r.keys=set();r.call('SetWarpDestination',1,group['map'],255,actor['x'],actor['y']+1);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1800):
  r.run()
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Map not loaded')
 r.run(300) # Let the native map preview/fade finish before visual proof.

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
 for f in range(60000): # Long legal battles include defensive boosts, healing and PP fallback.
  r.keys=battle_keys(r,f);r.run()
  if f%64==0:
   cb=r.u32(r.symbols['gMain']+4)
   if cb==r.symbols['BattleMainCB2']|1:started=True
   if f==1024:r.frame.save(P/(stem+'-combat.png'))
   if started and cb==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==bytes([2 if loss else 1]):
    if not loss and not r.call('FlagGet',flag):continue
    r.keys=set();finish(r)
    if getattr(r,'qa_fallbacks',[]):
     results.append({'test':stem+' controller changed move after native limitations/PP exhaustion','fallbacks':list(r.qa_fallbacks),'passed':True});r.qa_fallbacks=[]
    return f
 state=capture_failure(r,stem)
 raise AssertionError(('Battle not completed',stem,started,state))
def main():
 spec=json.loads((ROOT/'data/yokai/cameos_boss.json').read_text());actors={a['name']:a for a in spec['actors']};gfx={a['person']:a['object_gfx'] for a in spec['graphics']}
 groups=[{'name':'domniscian','map':57,'boss':actors['Domniscian'],'staff':[actors['EmployeRouge'],actors['EmployeBleu']]}, {'name':'morleone','map':114,'boss':actors['DonMorleone'],'staff':[actors['Mafiamille1'],actors['Mafiamille2'],actors['Mafiamille3']]}]
 for group in groups:
  print('START',group['name'],flush=True);allactors=[group['boss']]+group['staff'];allgfx={gfx[a['name']] for a in allactors};r=fixture(group,False)
  try:
   visible=[r.read(r.symbols['gObjectEvents']+i*36+5,1)[0] for i in range(16) if r.read(r.symbols['gObjectEvents']+i*36,1)[0]&1 and r.read(r.symbols['gObjectEvents']+i*36+5,1)[0] in allgfx]
   assert not visible,(group['name'],'pre-League NPCs visible',visible);r.frame.save(P/('cameo-'+group['name']+'-avant-ligue.png'));results.append({'test':group['name']+' entire group hidden before League','passed':True})
  finally:r.close()
  r=fixture(group)
  try:
   visible=[r.read(r.symbols['gObjectEvents']+i*36+5,1)[0] for i in range(16) if r.read(r.symbols['gObjectEvents']+i*36,1)[0]&1 and r.read(r.symbols['gObjectEvents']+i*36+5,1)[0] in allgfx]
   assert set(visible)==allgfx,(group['name'],'missing/corrupt postgame actors',visible)
   r.frame.save(P/('cameo-'+group['name']+'-groupe-postgame.png'))
   for actor in allactors:
    for dy in [0,1]:assert r.call('MapGridGetCollisionAt',actor['x']+7,actor['y']+7+dy)==0,(actor['name'],'blocked tile',dy)
   before=r.call('GetGameStat',9);interact(r);finish(r);assert r.call('GetGameStat',9)==before
   assert not r.call('FlagGet',C[group['boss']['won']]);results.append({'test':group['name']+' boss refuses before staff victories','passed':True})
   # Map transitions reapply group visibility after clearing the progression flag in this fixture.
   r.call('FlagClear',0x82C);warp(r,group,group['staff'][0]);assert not any(r.read(r.symbols['gObjectEvents']+i*36,1)[0]&1 and r.read(r.symbols['gObjectEvents']+i*36+5,1)[0] in allgfx for i in range(16))
   r.call('FlagSet',0x82C)
   for i,actor in enumerate(group['staff']):
    warp(r,group,actor);before=r.call('GetGameStat',9);interact(r);finish(r)
    assert r.call('GetGameStat',9)==before and not r.call('FlagGet',C[actor['won']])
    interact(r);fight(r,C[actor['won']],'cameo-'+actor['name'].lower())
    assert r.call('FlagGet',C[actor['won']]);results.append({'test':actor['name']+' actual optional No then victory, correct prerequisite flag','passed':True})
    if i+1<len(group['staff']):
     warp(r,group,group['boss']);before=r.call('GetGameStat',9);interact(r);finish(r);assert r.call('GetGameStat',9)==before and not r.call('FlagGet',C[group['boss']['won']])
   boss=group['boss'];warp(r,group,boss);before=r.call('GetGameStat',9);interact(r);finish(r);assert r.call('GetGameStat',9)==before and not r.call('FlagGet',C[boss['won']])
   item,amount,rewardflag=boss['reward'];item=C[item];rewardflag=C[rewardflag];r.call('ClearBag');filled=[]
   for n in range(1,347):
    if n==item or r.call('GetPocketByItemId',n)!=1:continue
    if r.call('AddBagItem',n,1):filled.append(n)
    if len(filled)==42:break
   assert len(filled)==42 and not r.call('CheckBagHasSpace',item,amount)
   r.call('HealPlayerParty');interact(r);frames=fight(r,C[boss['won']],'cameo-'+group['name']+'-boss')
   assert not r.call('FlagGet',rewardflag) and not r.call('CheckBagHasItem',item,1)
   assert r.call('RemoveBagItem',filled[0],1);before=r.call('GetGameStat',9);interact(r);finish(r)
   assert r.call('GetGameStat',9)==before and r.call('FlagGet',rewardflag) and r.call('CheckBagHasItem',item,amount) and not r.call('CheckBagHasItem',item,amount+1)
   results.append({'test':group['name']+' actual boss victory; full-bag reward retained, later exact quantity without another battle','quantity':amount,'frames':frames,'passed':True})
   for repeat in range(2):
    r.call('HealPlayerParty');before=r.call('GetGameStat',9);interact(r);fight(r,C[boss['won']],'cameo-'+group['name']+'-revanche-'+str(repeat));assert r.call('GetGameStat',9)==before+1
    assert r.call('CheckBagHasItem',item,amount) and not r.call('CheckBagHasItem',item,amount+1);assert all(r.call('FlagGet',C[a['won']]) for a in group['staff'])
   flagset=[C[a['won']] for a in allactors]+[rewardflag];assert r.call('TrySavingData',0,max_frames=1200)==1
   for f in flagset:r.call('FlagClear',f)
   assert r.call('LoadGameSave',0,max_frames=1200)==1 and all(r.call('FlagGet',f) for f in flagset)
   results.append({'test':group['name']+' two real boss rematches without duplicate rewards or prerequisite reset; flags persist in native Flash','passed':True})
  finally:r.close()
  for target in [group['staff'][0],group['boss']]:
   r=fixture(group,True,True)
   try:
    if target==group['boss']:
     # For this independent loss-only fixture; real prerequisite wins were exercised above.
     for staff in group['staff']:r.call('FlagSet',C[staff['won']])
    warp(r,group,target);interact(r);fight(r,C[target['won']],'cameo-'+target['name'].lower()+'-defaite',loss=True)
    assert not r.call('FlagGet',C[target['won']]);assert not r.call('FlagGet',C[group['boss']['reward'][2]])
    results.append({'test':target['name']+' actual defeat/whiteout records no false victory or reward','passed':True})
   finally:r.close()
  print('PASS',group['name'],flush=True)
 r=Emulator()
 try:
  r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('NewGameInitData')
  expected=[[1,5,100,8,17,9],[1,28],[5,17],[147,70,140,136,115,86],[52],[38,92],[57,58,46]]
  assert [[m['number'] for m in t['members']] for t in spec['teams']]==expected
  for team in spec['teams']:
   r.w32(r.symbols['gBattleTypeFlags'],8);assert r.call('CreateNPCTrainerParty',r.symbols['gEnemyParty'],team['trainer_id'])==len(team['members'])
   raw=r.read(r.symbols['gTrainers']+40*team['trainer_id']+4,12);assert 255 in raw,(team['person'],'name lacks EOS')
   for i,m in enumerate(team['members']):
    mon=r.symbols['gEnemyParty']+100*i;assert r.call('GetMonData',mon,C['MON_DATA_SPECIES'],0)==m['number'];assert r.call('GetMonData',mon,C['MON_DATA_LEVEL'],0)==m['level'];assert r.call('GetMonData',mon,C['MON_DATA_HELD_ITEM'],0)==0
    assert [r.call('GetMonData',mon,C['MON_DATA_MOVE'+str(j)],0) for j in range(1,5)]==[C[x] for x in m['moves']];assert r.call('GetMonData',mon,C['MON_DATA_ABILITY_NUM'],0)==0
  results.append({'test':'Seven native trainer parties /22 members match approved species, order, levels, moves and abilities; trainer names have EOS within12bytes','passed':True})
 finally:r.close()
 report={'passed':True,'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Actual NPC interaction, prerequisite staff battles, boss battles, No choices, full bags and native Flash reload; fixture warps and post-story flags, overpower party with four attacking moves for wins, native legal-move controller for PP/Grudge, weak party for defeats, independent instances/no savestates. Not whole story or balance proof.','balance_validated':False,'results':results,'remaining':['Normal access through Silph/Rocket maze during a full adventure','Difficulty with ordinary party','Audio mixing/listening is outside this public-ROM test']}
 (ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/POSTGAME_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
 try:main()
 except Exception as error:
  failure={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'passed':False,'error':str(error),'partial_results':results}
  (ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/POSTGAME_MGBA.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2)+'\n')
  raise

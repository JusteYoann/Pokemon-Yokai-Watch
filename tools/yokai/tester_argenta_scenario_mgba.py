#!/usr/bin/env python3
"""Argenta chapter: real route connection, story, excavation, battle and Flash.

Party/progression fixtures are explicit. No fabricated battle outcomes/stat boosts.
"""
import hashlib,json,re,struct
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from pilote_combat_mgba import battle_keys,capture_failure
OUT=ROOT/'QA_RECETTE_FINALE/ARGENTA_SCENARIO_2026';OUT.mkdir(exist_ok=True)
C={k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)\b','\n'.join((ROOT/f'include/constants/{n}.h').read_text() for n in ['pokemon','items','moves']),re.M)}
G={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};G["'"]=G['’']
STAGE=0x40F3;R1=0x321;R2=0x322;BADGE=0x820;TM_FLAG=0x89
# Resolve the native TM flag rather than assume its historic number.
flags=(ROOT/'include/constants/flags.h').read_text();TM_FLAG=int(re.search(r'#define FLAG_GOT_TM39_FROM_BROCK\s+(0x[0-9A-Fa-f]+)',flags)[1],16)
results=[]
def pos(r):return struct.unpack('<hh',r.read(r.u32(r.symbols['gSaveBlock1Ptr']),4))
def location(r):return tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))
def idle(r):return r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1

def warp(r,g,n,x,y):
 r.keys=set();r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)

def walk(r,d,n=1):
 dx,dy,key={'U':(0,-1,4),'D':(0,1,5),'L':(-1,0,6),'R':(1,0,7)}[d]
 x,y=pos(r);target=(x+dx*n,y+dy*n)
 for _ in range(1200):
  r.keys={key};r.run()
  if pos(r)==target:break
 else:raise AssertionError(('Walking blocked',d,n,(x,y),pos(r),target))
 r.keys=set();r.run(20)

def face_a(r,d):
 key={'U':4,'D':5,'L':6,'R':7}[d];r.keys={key};r.run(4);r.keys=set();r.run(12);r.keys={8};r.run(2);r.keys=set();r.run(12)

def finish(r,limit=12000,watch=False,stem=''):
 seen=[]
 for f in range(limit):
  r.keys={8} if f%16<4 else set();r.run()
  if watch:
   text=r.read(r.symbols['gStringVar4'],1000)
   for label,phrase in [('morleone','MORLEONE: Écoutez-moi!'),('enma','Bourg Palette')]:
    encoded=bytes(G[c] for c in phrase)
    if label not in seen and encoded in text:
     seen.append(label);r.keys=set();r.run(400);r.frame.save(OUT/(stem+'-'+label+'.png'))
     pal='gObjectEventPal_YokaiDonMorleoneGroup' if label=='morleone' else 'gObjectEventPal_Scenario'
     assert r.read(r.symbols['gPlttBufferUnfaded']+512+10*32,32)==r.read(r.symbols[pal],32),label+' wrong native palette'
  if f>60 and idle(r):r.keys=set();r.run(20);return seen
 raise AssertionError(('Script did not end',pos(r),location(r)))

def party(r,starter=87,weak=False):
 members=[(starter,1)] if weak else [(starter,13),(8,11),(45,10)]
 for i,(species,level) in enumerate(members):
  mon=r.symbols['gPlayerParty']+i*100;r.call('CreateMon',mon,species,level,15,1,100+i,0,0)
  # Reorder existing learned attacks as the player can do in the summary UI.
  existing=[r.call('GetMonData',mon,13+j,0) for j in range(4)]
  preferred=['MOVE_WATER_GUN','MOVE_THUNDER_SHOCK','MOVE_EMBER','MOVE_SLUDGE','MOVE_LICK','MOVE_SCRATCH','MOVE_TACKLE','MOVE_ASTONISH']
  moves=sorted(existing,key=lambda m:next((j for j,n in enumerate(preferred) if C[n]==m),100 if m else 101))
  for j,m in enumerate(moves):r.call('SetMonMoveSlot',mon,m,j)
 r.write(r.symbols['gPlayerPartyCount'],bytes([len(members)]));r.call('SetLastHealLocationWarp',3)

def fight(r,stem,loss=False,limit=24000):
 started=False;first_enemy=[]
 for f in range(limit):
  # Decline the real SHIFT replacement menu; the active Yo-kai is alive.
  if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_UpdatePartyMenu']|1 and int.from_bytes(r.read(r.symbols['gBattleMons']+0x28,2),'little')>0:
   r.keys={0} if f%16<4 else set()
  else:r.keys=battle_keys(r,f)
  r.run()
  cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['BattleMainCB2']|1:
   if not started:
    first_enemy=[(r.call('GetMonData',r.symbols['gEnemyParty']+100*i,11,0),r.call('GetMonData',r.symbols['gEnemyParty']+100*i,56,0)) for i in range(2)]
    assert first_enemy==[(24,9),(25,11)],first_enemy
   started=True
   if f==1024:r.frame.save(OUT/(stem+'-combat.png'))
  if started and cb==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==bytes([2 if loss else 1]):
   finish(r);return f
 r.frame.save(OUT/(stem+'-diagnostic.png'))
 detail=capture_failure(r,'argenta-'+stem)
 raise AssertionError(('Battle did not finish',stem,started,r.read(r.symbols['gBattleOutcome'],1).hex(),detail))

def puzzle(r,stem):
 # Enter through the actual city -> gym door warp.
 warp(r,3,2,15,17);walk(r,'U');r.run(600);assert location(r)==(6,2),location(r)
 r.frame.save(OUT/(stem+'-fouilles.png'))
 walk(r,'U',3);walk(r,'L');walk(r,'U',4);walk(r,'R');walk(r,'U') # Approach around the central excavation.
 finish(r);assert pos(r)==(6,6),pos(r)
 walk(r,'L',3);walk(r,'D');face_a(r,'L');finish(r);assert r.call('FlagGet',R1)
 # One relic still does not allow the central passage.
 walk(r,'U');walk(r,'R',3);walk(r,'U');finish(r);assert pos(r)==(6,6)
 walk(r,'L',3);walk(r,'D',5);walk(r,'R',6);walk(r,'U',4);face_a(r,'R');finish(r);assert r.call('FlagGet',R2)
 assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('FlagClear',R1);r.call('FlagClear',R2)
 assert r.call('LoadGameSave',0,max_frames=1200)==1 and r.call('FlagGet',R1) and r.call('FlagGet',R2)
 # Reload normal map state after the save test, then walk the final approach.
 warp(r,6,2,9,7);walk(r,'U');walk(r,'L',3);walk(r,'U',2);assert pos(r)==(6,4)
 r.frame.save(OUT/(stem+'-wyatt.png'))
 results.append({'test':stem+' gym door warp, real walks to both relics, zero/one-relic refusals, persistent relic flags and final approach','passed':True})

for gender,name in [(0,'nathan'),(1,'katie')]:
 r=new_game(gender)
 try:
  party(r)
  warp(r,3,20,8,2) # Route2 northern exit, before the actual map connection.
  r.keys={4};r.run(220);r.keys=set()
  seen=finish(r,watch=True,stem=name)
  assert seen==['morleone','enma'],seen
  assert r.call('VarGet',STAGE)==2 and location(r)==(3,2),(location(r),r.call('VarGet',STAGE))
  r.frame.save(OUT/(name+'-argenta-apres.png'))
  assert r.call('TrySavingData',0,max_frames=1200)==1
  r.call('VarSet',STAGE,0);assert r.call('LoadGameSave',0,max_frames=1200)==1 and r.call('VarGet',STAGE)==2
  warp(r,3,2,22,36);walk(r,'U');assert idle(r),'Speech repeats after native Flash reload'
  results.append({'test':name+' actual Route2/city connection and coordinate-triggered speech; sequential correct palettes; incognito dialogue; Flash persistence/no replay','passed':True})
  puzzle(r,name)
  if gender==0:
   assert r.call('AddBagItem',327,999) and not r.call('CheckBagHasSpace',327,1)
  face_a(r,'U');frames=fight(r,name)
  assert r.call('FlagGet',BADGE)
  if gender==0:
   assert not r.call('FlagGet',TM_FLAG);r.call('RemoveBagItem',327,1);before=r.call('GetGameStat',9);face_a(r,'U');finish(r)
   assert r.call('GetGameStat',9)==before and r.call('CheckBagHasItem',327,999)
  else:assert r.call('CheckBagHasItem',327,1) and not r.call('CheckBagHasItem',327,2)
  assert r.call('FlagGet',TM_FLAG)
  before=r.call('GetGameStat',9);face_a(r,'U');finish(r);assert r.call('GetGameStat',9)==before
  assert r.call('TrySavingData',0,max_frames=1200)==1
  r.call('FlagClear',BADGE);r.call('FlagClear',TM_FLAG)
  assert r.call('LoadGameSave',0,max_frames=1200)==1 and r.call('FlagGet',BADGE) and r.call('FlagGet',TM_FLAG)
  # Exit with the trophy, then cross the real Route3 running-shoes trigger.
  warp(r,6,2,6,13);r.keys={5};r.run(80);r.keys=set();r.run(600);assert location(r)==(3,2),location(r)
  warp(r,3,2,45,22);walk(r,'R');finish(r);assert r.call('FlagGet',0x82F),'Running shoes not awarded'
  results.append({'test':name+' actual Wyatt victory with normal-stat fixture party; first trophy, unique TM/full-stack retry, no repeat battle, Flash save/load, gym exit and running-shoes event','battle_frames':frames,'passed':True})
 finally:r.close()
report={'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Real intro, fixture party/progression and warps to Route2 and gym entrance; chapter interactions and battles via buttons, no forced victory/stat boosts. Not a continuous Pallet-to-Pewter playthrough or exhaustive balancing.','results':results}
(OUT/'TEST_CHAPITRE_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

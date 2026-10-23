#!/usr/bin/env python3
"""Lance fixture -> real victory/door -> normal finale -> native HOF/credits/Continue.
Initial position and boosted QA party are fixtures. No story flags, enemy HP,
battle outcomes, script pointers or intermediate warps are injected thereafter.
This is the last League segment, not a start-to-finish adventure or balance test.
"""
import os,json,struct,hashlib,subprocess,gzip
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
from pilote_combat_mgba import battle_keys
Q=ROOT/os.environ.get('YOKAI_FINALE_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON/ETAPE_B/jalon3/public');Q.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;events=[];battles=[];phases=[];credits=set();hof=False;heal=False;white=False;first=False;conclusion=False;chen=False;departed=False;matt_checks=[]

def pos():
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1 and b[8]==255:return tuple(v-7 for v in struct.unpack_from('<hh',b,16))
 return None

def walk(key):
 x,y=pos();dx,dy={4:(0,-1),5:(0,1),6:(-1,0),7:(1,0)}[key];goal=(x+dx,y+dy)
 for _ in range(40):
  r.keys={key};r.run()
  if pos()==goal:r.keys=set();r.run(20);return
 raise AssertionError(('Blocked native walking',pos(),goal,key))

def fieldfree():
 return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and r.read(r.symbols['sLockFieldControls'],1)==b'\0'

def flags(n):
 b=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0xEE0+(n>>3),1)[0];return bool(b&(1<<(n&7)))

def mapname():
 pair=list(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))
 return next((k for k,v in MAPS.items() if list(v)==pair),str(pair))

def actors():
 return [b[8] for i in range(16) if (b:=r.read(r.symbols['gObjectEvents']+36*i,36))[0]&1]
def check_matt_companion(stage):
 objects={}
 for i in range(16):
  raw=r.read(r.symbols['gObjectEvents']+36*i,36)
  if raw[0]&1 and raw[9:11]==bytes([MAPS['PokemonLeague_ChampionsRoom'][1],MAPS['PokemonLeague_ChampionsRoom'][0]]):objects[raw[8]]=raw
 player,matt,don=objects[255],objects[1],objects[3]
 xy=lambda b:tuple(v-7 for v in struct.unpack_from('<hh',b,16))
 px,py=xy(player);mx,my=xy(matt)
 assert (mx,my)==(px-1,py),('Matt must be immediately left, same row',stage,xy(player),xy(matt))
 assert matt[24]&15==2 and player[24]&15==2,('Matt/player must face enemy',stage,matt[24]&15,player[24]&15)
 banks=[]
 for label,obj,bank,symbol in [('Matt',matt,6,'gObjectEventPal_Matt'),('Don',don,10,'gObjectEventPal_YokaiDonMorleoneGroup')]:
  actual=int.from_bytes(r.read(r.symbols['gSprites']+68*obj[4]+4,2),'little')>>12
  assert actual==bank,(stage,label,actual,bank)
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols[symbol],32),(stage,label,'Wrong palette after battle return')
  banks.append(actual)
 assert len({xy(b) for b in objects.values()})==len(objects),'Actors overlap'
 matt_checks.append(dict(stage=stage,player=xy(player),matt=xy(matt),both_face_north=True,matt_bank=banks[0],don_bank=banks[1],normal_palettes=True))
 r.frame.save(Q/f'matt-couleurs-position-etape-{stage}.png')

try:
 strong_party(r)
 # Native Set battle-style option avoids optional shift prompts in this pilot.
 opt=r.u32(r.symbols['gSaveBlock2Ptr'])+0x15
 r.write(opt,bytes([r.read(opt,1)[0]|2]))
 # Five real additional party members, including a fainted poisoned one with no PP.
 for i,species in enumerate([7,25,44,74,100],1):r.call('CreateMon',r.symbols['gPlayerParty']+100*i,species,55,24,1,100+i,0,0x1234)
 r.write(r.symbols['gPlayerPartyCount'],b'\6')
 assert not flags(C['FLAG_SYS_GAME_CLEAR']) and not flags(C['FLAG_DEFEATED_LANCE']) and not flags(0x500+743) and not flags(0x500+744)
 warp(r,*MAPS['PokemonLeague_LancesRoom'],6,9)
 r.keys={4};r.run(1);r.keys=set();r.run(20)
 lance=False
 for f in range(22000):
  ib=r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
  if ib:lance=True
  r.keys=battle_keys(r,f) if ib else (set() if lance and fieldfree() else {8} if f%16<4 else set());r.run()
  if lance and fieldfree() and flags(C['FLAG_DEFEATED_LANCE']):break
 else:raise AssertionError('Lance victory/field return missing')
 assert not flags(C['FLAG_SYS_GAME_CLEAR'])
 r.frame.save(Q/'01-lance-vaincu.png');events.append(dict(event='Actual fourth Elite Four victory',frame=f))
 # Native controller navigation through the door opened by Lance's victory.
 walk(6)
 for _ in range(3):walk(4)
 walk(7)
 for _ in range(360):
  r.keys={4};r.run()
  if mapname()=='PokemonLeague_ChampionsRoom':break
 else:raise AssertionError('Native Lance door did not reach Champion room')
 r.keys=set();r.run(360)
 assert mapname()=='PokemonLeague_ChampionsRoom',mapname()
 # Party-only healing fixture after walking; no poisoned-overworld step prompt.
 for field,value in [('MON_DATA_HP',0),('MON_DATA_STATUS',8),('MON_DATA_PP1',0),('MON_DATA_PP2',0),('MON_DATA_PP3',0),('MON_DATA_PP4',0)]:
  r.w32(r.PARAMS+128,value);r.call('SetMonData',r.symbols['gPlayerParty']+100,C[field],r.PARAMS+128)
 callbacks={int(v[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=l.split())==3 and v[2]=='HandleInputChooseAction'}
 laststage=-1;seencredits=False
 for f in range(85000):
  cb=r.u32(r.symbols['gMain']+4);ib=cb==r.symbols['BattleMainCB2']|1
  r.keys=battle_keys(r,f) if ib else ({8} if f%16<4 else set());r.run()
  name=mapname()
  if name=='PokemonLeague_ChampionsRoom':
   stageptr=r.u32(r.symbols['gSaveBlock1Ptr'])+0x1000+2 # VAR_TEMP_2 (4002)
   # Derive ABI offset once using GetVarPointer, never cache relocated address.
   if 'stageoffset' not in locals():stageoffset=r.call('GetVarPointer',0x4002)-r.u32(r.symbols['gSaveBlock1Ptr'])
   stage=int.from_bytes(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+stageoffset,2),'little')
   if stage!=laststage:
    events.append(dict(event='scene_stage',stage=stage,frame=f,actors=actors(),player=pos()))
    if stage in [6,7,8]:r.keys=set();r.run(120)
    r.frame.save(Q/f'etape-{stage}.png');laststage=stage
    if stage in [3,6]:check_matt_companion(stage)
   if stage==3 and not heal:
    for i in range(6):
     mon=r.symbols['gPlayerParty']+100*i;get=lambda k:r.call('GetMonData',mon,C[k],0)
     assert get('MON_DATA_HP')==get('MON_DATA_MAX_HP') and get('MON_DATA_HP')>0 and get('MON_DATA_STATUS')==0,i
     for j in range(4):
      move=r.call('GetMonData',mon,C['MON_DATA_MOVE1']+j,0);pp=r.call('GetMonData',mon,C['MON_DATA_PP1']+j,0)
      assert pp==r.call('CalculatePPWithBonus',move,get('MON_DATA_PP_BONUSES'),j),(i,j,pp)
    heal=True;r.frame.save(Q/'matt-soigne-six-yokai.png')
   if stage==5 and not white:
    assert not {3,4,5,6}&set(actors())
    white=sum(min(p)>245 for p in r.frame.convert('RGB').get_flattened_data())/(240*160)>.99
    if white:r.frame.save(Q/'flash-blanc.png')
   if stage==6:conclusion=True
   if stage==7:departed=not bool({3,4,5,6}&set(actors()))
   if stage==8:chen=2 in actors()
  if ib:
   trainer=int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')
   if trainer not in battles:battles.append(trainer)
   assert trainer in [743,744],trainer
   if trainer==743:assert not flags(C['FLAG_SYS_GAME_CLEAR']) and not flags(0x500+744)
   if trainer==744:
    if not first and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:
     r.keys=set();r.run(180);assert r.read(r.symbols['sFirst'],1)==b'\1' and r.call('SpiratonArtIsActive');first=True;r.frame.save(Q/'vrai-boss-premier-choix.png')
    level=r.read(r.symbols['gBattleMons']+88+42,1)[0]
    if level==56+len(phases):phases.append(level)
  if cb==r.symbols['CB2_HofIdle']|1:
   if any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_Hof_TryDisplayAnotherMon']|1 for i in range(16)) and not locals().get('hof_captured',False):
    r.keys=set();r.run(60);r.frame.save(Q/'pantheon-natif.png');hof_captured=True
   hof=True
  if cb==r.symbols['CB2_Credits']|1:
   seencredits=True;mgr=r.u32(r.symbols['sCreditsMgr'])
   if mgr:
    state=r.read(mgr,1)[0]
    if state not in credits and state in [0,17,18]:r.frame.save(Q/f'credits-{state}.png')
    credits.add(state)
  if seencredits and cb!=r.symbols['CB2_Credits']|1:break
 else:raise AssertionError(dict(timeout=True,events=events,battles=battles,phases=phases,map=mapname(),pos=pos(),cb=hex(cb),script=hex(r.u32(r.symbols['sGlobalScriptContext']+8))))
 assert hof and seencredits and {17,18}<=credits
 assert heal and white and first and conclusion and departed and chen and phases==list(range(56,64)) and battles==[743,744]
 r.keys=set();r.run(1200)
 for f in range(7000):
  r.keys={3} if f%120<2 else {8} if f%120 in [60,61] else set();r.run()
  if f>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gQuestLogState'],1)[0] not in [2,3]:break
 else:raise AssertionError('Real Continue after native save failed')
 assert flags(C['FLAG_SYS_GAME_CLEAR']) and flags(0x500+743) and flags(0x500+744)
 assert not r.call('SpiratonArtIsActive') and r.call('GetSpriteTileStartByTag',0x7D54)==65535
 r.keys=set();r.run(180);r.frame.save(Q/'postgame-apres-continue.png')
 artifact=ROOT.parent/'artifacts'/'spiraton-etape-b';artifact.mkdir(parents=True,exist_ok=True)
 (artifact/('postgame-prive.state.gz' if 'audio' in r.elf_path.name else 'postgame-public.state.gz')).write_bytes(gzip.compress(r.snapshot()))
 passed=True
finally:
 if not passed:r.frame.save(Q/'diagnostic.png')
 (Q/'FINALE_NORMALE_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),events=events,battles=battles,levels=phases,whole_six_party_heal=heal,white=white,first_choice_wait=first,conclusion=conclusion,mafia_departed=departed,chen_present=chen,hall_of_fame=hof,credits=sorted(credits),postgame_continue=passed,story_victory_flags_injected=False,qa_initial_party=True,matt_companion_palette_position_checks=matt_checks),indent=2)+'\n');r.close()
print('PASS: Lance, normal final-room entry, both battles, conclusion, native HOF/credits/save/Continue')

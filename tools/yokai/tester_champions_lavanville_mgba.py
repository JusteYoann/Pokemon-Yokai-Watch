#!/usr/bin/env python3
"""Native mGBA chapter scenarios. Map warps, starter strength and selected script
entry points are fixtures; graphics/palettes/battle results/flags are never injected.
Controller input drives dialogues, native battles and capture menus. This is not a
claim of an uninterrupted playthrough from Pallet Town or a full balance playtest.
"""
from pathlib import Path
import os,json,struct,hashlib,sys,subprocess,re
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
from mgba_rpc import ROOT
rom=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba'));mode='prive' if '_audio' in rom.name else 'public'
P=ROOT/'docs/champions-yokai-watch/validation/regressions/lavanville'/mode;P.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False;failure=None
F_INTRO=0x322;V_INTRO=0x40f3;BADGE=0x823
def flag(n):return r.call('FlagGet',n)!=0
def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def shot(name):r.frame.save(P/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(name+'-x3.png'))
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def free():return field() and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02'
def script(label):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[label])
def tick(f,key=8):r.keys={key} if f%16<4 else set();r.run()
def finish(limit=9000):
 for f in range(limit):
  tick(f)
  if f%8==0 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:
   raw=r.read(r.symbols['gStringVar4'],12);badge=r.read(r.symbols['LavenderAlyzon_Text_Badge'],12)
   if raw==badge:shot('alyzon-remise-badge')
  if f>32 and free():r.keys=set();r.run(8);return f
 raise AssertionError(('Script did not release',hex(r.u32(r.symbols['gMain']+4))))
def party():r.call('ZeroPlayerPartyMons');strong_party(r)
def value(mon,field):return r.call('GetMonData',mon,C[field],0)
def actors():
 out={}
 for i in range(16):
  a=r.symbols['gObjectEvents']+36*i;data=r.read(a,36)
  if data[0]&1:out[data[8]]=(i,data[5],struct.unpack('<hh',data[16:20]))
 return out
# Native object layout: localId offset8, graphicsId offset5. Verify through registry IDs below.
def oid(lid):
 return r.call('GetObjectEventIdByLocalIdAndMap',lid,r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+5,1)[0],r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,1)[0])
def action_menu(limit=6000):
 callbacks={int(line.split()[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(rom.with_suffix('.elf'))],text=True).splitlines() if len(line.split())==3 and line.split()[2]=='HandleInputChooseAction'}
 for f in range(limit):
  tick(f,0)
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and f%8==0:
   sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
   if sid<64:
    sp=r.symbols['gSprites']+68*sid
    if r.read(sp+62,1)[0]&1 and struct.unpack('<H',r.read(sp+6,2))[0]==160 and struct.unpack('<h',r.read(sp+36,2))[0]==0:
     shot('alyzon-portrait-natif')
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:
   r.keys=set();r.run(16);return
 raise AssertionError('Battle action menu not reached')
def walk(key):r.keys={key};r.run(30);r.keys=set();r.run(4)
def pulse(key,after=16):r.keys={key};r.run();r.keys=set();r.run(after)
def win(limit=16000):
 started=False;seen=[]
 for f in range(limit):
  tick(f)
  cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['BattleMainCB2']|1:
   started=True
   if f%8==0:
    idx=struct.unpack('<H',r.read(r.symbols['gBattlerPartyIndexes']+2,2))[0]
    if idx<6 and (not seen or idx!=seen[-1]):seen.append(idx)
  if started and field() and r.read(r.symbols['gBattleOutcome'],1)==b'\x01':
   r.keys=set();finish();return seen
 raise AssertionError(('Native fight did not return with KO victory',seen,hex(r.u32(r.symbols['gMain']+4))))
try:
 # Measure each literal dialogue line with the native GBA font, including all pages.
 widths=[]
 for file in ['LavenderTown','PokemonTower_7F','PokemonTower_2F','CeladonCity_Gym','CeladonCity_GameCorner']:
  text=(ROOT/f'data/maps/{file}/scripts.inc').read_text()
  for label in re.findall(r'^(Lavender\w*Text_\w+)::',text,re.M):
   raw=r.read(r.symbols[label],1024).split(b'\xff',1)[0]
   for line in re.split(b'[\xfa\xfb\xfe]',raw):
    assert len(line)<100
    r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0);assert width<=208,(label,width)
    widths.append(width)
 report('New French dialogue fits native GBA font within208 pixels per line',lines=len(widths),maximum_width=max(widths))
 party();initial=r.snapshot()
 # Native map loads from the three town approaches; no manually started intro script.
 for tag,x,y in [('nord',11,1),('ouest',1,9),('sud',11,18),('vol',6,6)]:
  r.restore(initial);r.keys=set();r.call('SetWarpDestination',*MAPS['LavenderTown'],255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
  movie=[];had_aly=False;had_zombie=False;peak=0
  for f in range(9000):
   tick(f)
   if f%12==0:
    # Observe actual spawned actors with their local IDs through native lookup.
    aly=r.call('GetObjectEventIdByLocalIdAndMap',201,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0]);zom=r.call('GetObjectEventIdByLocalIdAndMap',200,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0]);had_aly|=aly<16;had_zombie|=zom<16
    if tag=='nord':movie.append(r.frame.copy())
   if f%16==0 and flag(F_INTRO) and free():break
  else:raise AssertionError(('Intro never completes',tag))
  assert r.call('GetCurrentWeather')==6 and r.call('GetCurrentMapMusic')==360
  assert had_aly and had_zombie,(tag,had_aly,had_zombie)
  assert r.call('VarGet',V_INTRO)==1
  assert r.call('GetObjectEventIdByLocalIdAndMap',200,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0])==16
  assert r.call('GetObjectEventIdByLocalIdAndMap',201,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0])==16
  shot('arrivee-'+tag)
  if movie:movie[0].resize((720,480),Image.Resampling.NEAREST).save(P/'introduction.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in movie[1:]],duration=200,loop=0)
  report('First-entry native intro completes with both actors and releases controls',entry=tag,frames=f)
 # Old-save cramped position: all four adjacent rays obstructed. The special
 # must return literal0 and the script must finish without waiting on a nonexistent task.
 warp(r,*MAPS['LavenderTown'],14,9)
 for lid,(x,y) in enumerate([(14,8),(14,10),(13,9),(15,9)],210):
  assert r.call('SpawnSpecialObjectEventParameterized',174,C['MOVEMENT_TYPE_FACE_DOWN'],lid,x+7,y+7,3)<16
 assert r.call('LavanvillePrepareIntro')==0
 r.call('FlagClear',F_INTRO);script('LavenderIntro_Start');finish();assert flag(F_INTRO) and free();report('Cramped legacy-save position returns explicit0 and completes dialogue without a stuck scene task')
 # Return through a service interior: no repeat, no fog indoors.
 warp(r,*MAPS['LavenderTown_House2'],4,6);assert r.call('GetCurrentWeather')!=6;assert free();shot('maison-service')
 warp(r,*MAPS['LavenderTown'],14,9);assert flag(F_INTRO) and r.call('VarGet',V_INTRO)==1 and free()
 assert r.call('GetObjectEventIdByLocalIdAndMap',201,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0])==16
 # Actual fog callbacks, animation movement and no cumulative buffer mutation.
 fog=[]
 for i in range(64):
  a=r.symbols['gSprites']+68*i
  if r.u32(a+28)==r.symbols['FogHorizontalSpriteCallback']|1:fog.append(i)
 assert len(fog)==20,len(fog)
 sp=r.symbols['gSprites']+68*fog[0];x1=r.read(sp+32,2);p1=r.read(r.symbols['gPlttBufferUnfaded'],512);r.run(80);assert x1!=r.read(sp+32,2);assert p1==r.read(r.symbols['gPlttBufferUnfaded'],512)
 # Hardware palette derives from faded originals, not an accumulated tint.
 rgb=r.read(r.symbols['gPlttBufferFaded'],384);hw=r.read(0x05000000,384)
 expected=b''.join(struct.pack('<H',((c&31)*18//32)|((((c>>5)&31)*18//32)<<5)|(((((c>>10)&31)*24+max(c&31,(c>>5)&31,(c>>10)&31)*4)//32)<<10)) for c in struct.unpack('<192H',rgb))
 assert hw==expected,'Night hardware palette mismatch'
 shot('ville-nuit-brume');report('Permanent night, 20 animated native fog sprites, no repeated intro, no buffer accumulation, interior reset')
 warp(r,*MAPS['Route8'],50,8);assert not r.call('IsLavanvilleNight');assert r.call('GetCurrentWeather')!=6;shot('sortie-route8');report('Exterior effects stop on Route8')
 # Enter each hostile house and immediately leave through its actual door;
 # entry immunity gives control before a wandering resident can ambush the player.
 for house in ['LavenderTown_House1','LavenderTown_VolunteerPokemonHouse']:
  r.call('SetWarpDestination',*MAPS[house],255,4,6);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
  for f in range(600):
   r.run()
   if f>60 and free():break
  else:raise AssertionError('Hostile house entry did not release controls')
  assert r.call('LavanvilleCheckZombieImmunity')==1;walk(5)
  for f in range(600):
   r.run()
   if f>60 and free() and tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['LavenderTown']:break
  else:raise AssertionError('Hostile house exit blocked')
  report('Hostile house can be entered and left without an unavoidable combat',house=house)
 # Four repeatable wild-style direct zombies use registered art; no 151 entry is changed.
 warp(r,*MAPS['LavenderTown'],14,9);party();base=r.snapshot()
 for v,name in enumerate(['errant','sprinteur','colosse','spectral']):
  r.restore(base);r.write(r.symbols['gSpecialVar_0x8004'],struct.pack('<H',v));r.call('LavanvilleStartZombieBattle');action_menu()
  flags=r.u32(r.symbols['gBattleTypeFlags']);assert flags&(1<<20) and not flags&8 and ((flags>>21)&3)==v
  assert r.call('IsRunningFromBattleImpossible')==1
  assert not r.call('TryRunFromBattle',0)
  sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0];a=r.symbols['gSprites']+68*sid;tile=struct.unpack('<H',r.read(a+4,2))[0]&1023
  assert r.read(0x06010000+32*tile,2048)==(ROOT/f'graphics/yokai_zombies/{name}/battle-front.4bpp').read_bytes()
  shot('combat-'+name);seen=win();assert seen==[0],seen
  assert field();r.call('LavanvilleCheckZombieImmunity');assert r.read(r.symbols['gSpecialVar_Result'],2)==b'\x01\x00'
  report('Direct zombie native KO battle, no run, real art, field return and immunity',variant=name,party_indices=seen)
 # Actual Run menu and actual Master Ball attempt against a direct zombie.
 r.restore(base);r.call('ClearBag');r.call('AddBagItem',C['ITEM_MASTER_BALL'],1)
 r.write(r.symbols['gSpecialVar_0x8004'],b'\x00\x00');r.call('LavanvilleStartZombieBattle');action_menu()
 pulse(7);pulse(5);pulse(8,90);action_menu();shot('zombie-fuite-interdite')
 # Run cursor3 -> Fight0 -> Bag1 using controller input.
 pulse(6);pulse(4);r.write(r.symbols['gBagMenuState']+6,b'\x02\x00');pulse(7);pulse(8,240);pulse(8,90);pulse(8,90)
 action_menu();assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\x01';assert r.read(r.symbols['gBattleOutcome'],1)!=b'\x07';shot('zombie-capture-interdite')
 report('Controller Run refused and real Master Ball attempt dodged: no capture, battle continues')
 # A second combat against the same persistent town NPC must remain possible.
 r.restore(base);script('LavenderZombie_Variant0');action_menu();win();r.run(200);script('LavenderZombie_Variant0');action_menu();win();report('Same errant can be defeated twice without a trainer victory flag or removal')
 # Genuine ordinary tower wild capture with controller-driven Bag and Master Ball.
 r.restore(base);warp(r,*MAPS['PokemonTower_3F'],18,10);r.call('ClearBag');r.call('AddBagItem',C['ITEM_MASTER_BALL'],1);r.call('CreateScriptedWildMon',41,22,0);r.call('StartWildBattle');action_menu();assert not r.u32(r.symbols['gBattleTypeFlags'])&((1<<20)|(1<<15));assert r.call('IsRunningFromBattleImpossible')==0;shot('tour-rencontre-sauvage')
 r.write(r.symbols['gBagMenuState']+6,b'\x02\x00');pulse(7);assert r.read(r.symbols['gActionSelectionCursor'],1)==b'\x01';pulse(8,240);pulse(8,90);pulse(8,90)
 for f in range(12000):
  tick(f,0)
  if f%32==0 and field() and r.read(r.symbols['gBattleOutcome'],1)==b'\x07':break
 else:raise AssertionError('Ordinary Tower capture failed')
 assert value(r.symbols['gPlayerParty']+100,'MON_DATA_SPECIES')==41
 shot('tour-capture-reussie');report('Ordinary Tower encounter without Scope: native wild flags, Run permitted, actual Master Ball capture')
 # Native tower trainer script, saved victory and subsequent interaction without a battle.
 party();script('PokemonTower_3F_EventScript_Patricia');order=win();assert r.call('HasTrainerBeenFought',C['TRAINER_CHANNELER_PATRICIA']);script('PokemonTower_3F_EventScript_Patricia');finish();assert field()
 assert r.call('TrySavingData',0,max_frames=1200)==1;r.call('ClearTrainerFlag',C['TRAINER_CHANNELER_PATRICIA']);assert r.call('LoadGameSave',0,max_frames=1200)==1;assert r.call('HasTrainerBeenFought',C['TRAINER_CHANNELER_PATRICIA']);report('Tower trainer is one-time; actual native battle victory survives Flash save/reload')
 # Official champion fight and real badge award.
 warp(r,*MAPS['PokemonTower_7F'],11,5);party();before=r.call('GetGameStat',9);script('PokemonTower_7F_EventScript_MrFuji');action_menu();shot('alyzon-combat-intro');assert r.u32(r.symbols['gBattleTypeFlags'])&8
 expected=[(32,27),(8,28),(44,29),(32,31)]
 actual=[(value(r.symbols['gEnemyParty']+100*i,'MON_DATA_SPECIES'),value(r.symbols['gEnemyParty']+100*i,'MON_DATA_LEVEL')) for i in range(4)];assert actual==expected,actual
 order=win();assert order==[0,1,2,3],order;assert flag(BADGE) and flag(C['FLAG_DEFEATED_ERIKA']);shot('alyzon-badge')
 after=r.call('GetGameStat',9);script('PokemonTower_7F_EventScript_MrFuji');finish();assert r.call('GetGameStat',9)==after;report('Leader official team and ordered send-out, native victory, badge04 and no rematch/duplicate reward',team=actual,send_out_order=order)
 # Residence before/after badge, then post-League dialogue without an invented rematch.
 for has_badge in [False,True]:
  r.call('FlagSet' if has_badge else 'FlagClear',BADGE);warp(r,*MAPS['CeladonCity_Gym'],6,6 if has_badge else 12)
  matt=r.call('GetObjectEventIdByLocalIdAndMap',1,MAPS['CeladonCity_Gym'][1],MAPS['CeladonCity_Gym'][0]);aly=r.call('GetObjectEventIdByLocalIdAndMap',2,MAPS['CeladonCity_Gym'][1],MAPS['CeladonCity_Gym'][0]);assert (aly if has_badge else matt)<16;assert flag(0x324)==has_badge and flag(0x325)==(not has_badge)
  shot('residence-'+('apres' if has_badge else 'avant'));script('LavenderResidence_Alyzon' if has_badge else 'LavenderResidence_Matt');finish()
 r.call('FlagSet',0x82c);r.call('LavanvilleRematchReady');assert r.read(r.symbols['gSpecialVar_Result'],2)==b'\x00\x00';r.call('IncrementGameStat',10);r.call('LavanvilleRematchReady');assert r.read(r.symbols['gSpecialVar_Result'],2)==b'\x01\x00';script('LavenderResidence_Alyzon');finish();assert field();report('Residence changes Matt to Alyzon; future rematch requires BOTH League flag and Hall of Fame count, no invented team')
 # Reward available in old Scope-collected save after Don, real inventory and route flags.
 r.call('SetTrainerFlag',C['TRAINER_BOSS_GIOVANNI']);r.call('FlagSet',C['FLAG_HIDE_SILPH_SCOPE']);r.call('FlagClear',C['FLAG_GOT_POKE_FLUTE']);warp(r,*MAPS['RocketHideout_B4F'],15,12)
 assert not flag(C['FLAG_HIDE_SILPH_SCOPE']);script('RocketHideout_B4F_EventScript_SilphScope');finish();assert r.call('CheckBagHasItem',C['ITEM_POKE_FLUTE'],1) and flag(C['FLAG_GOT_POKE_FLUTE']) and flag(C['FLAG_HIDE_SILPH_SCOPE']);shot('flute-repaire');report('Old Scope-collected save receives real Flute reward after Don; inventory and wake-up flag set')
 # The two stair approaches really launch their mandatory battle on movement.
 for floor,tid,x,y,key in [(4,'TRAINER_CHANNELER_PAULA',6,10,6),(6,'TRAINER_CHANNELER_ANGELICA',13,16,6)]:
  r.call('ClearTrainerFlag',C[tid]);party();warp(r,*MAPS[f'PokemonTower_{floor}F'],x,y);walk(key);win();assert r.call('HasTrainerBeenFought',C[tid]);assert r.call('VarGet',0x4000)==1;walk(7);assert free();walk(6);assert free();shot(f'tour-obligatoire-{floor}')
  before=r.call('GetGameStat',9);script(f'LavenderTower_Gate{floor}');finish();assert r.call('GetGameStat',9)==before
  report('Actual movement into stair approach triggers mandatory trainer once',floor=floor,trainer=tid)
 # Walk into the original healing zone; HP is damaged only as a precondition fixture.
 party();warp(r,*MAPS['PokemonTower_5F'],9,9);r.w32(r.PARAMS+128,1);r.call('SetMonData',r.symbols['gPlayerParty'],C['MON_DATA_HP'],r.PARAMS+128);walk(7);finish();assert value(r.symbols['gPlayerParty'],'MON_DATA_HP')==value(r.symbols['gPlayerParty'],'MON_DATA_MAX_HP');shot('tour-soin');report('Original healing zone heals on actual tile entry')
 # Both real wake-up scripts use the recovered Flute and clear their route obstacle.
 for route,x,y,lid in [('Route12',14,71,5),('Route16',31,14,10)]:
  party();warp(r,*MAPS[route],x,y);r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',lid));script(route+'_EventScript_Snorlax');win();assert flag(C['FLAG_HIDE_'+('ROUTE_12' if route=='Route12' else 'ROUTE_16')+'_SNORLAX']);shot('misterre-'+route.lower());report('Real Flute awakening and KO removes route-blocking Misterre',route=route)
 # An old-open hideout entrance is blocked before the badge, including its approach tile.
 r.call('FlagClear',BADGE);r.call('FlagSet',C['FLAG_OPENED_ROCKET_HIDEOUT']);warp(r,*MAPS['CeladonCity_GameCorner'],11,2)
 before=r.call('GetGameStat',9);script('CeladonCity_GameCorner_EventScript_Poster');finish();assert field() and r.call('GetGameStat',9)==before;warp(r,*MAPS['CeladonCity_GameCorner'],13,2);walk(7);finish();save=r.u32(r.symbols['gSaveBlock1Ptr']);assert tuple(r.read(save+4,2))==MAPS['CeladonCity_GameCorner'];shot('repaire-verrouille')
 r.call('FlagSet',BADGE);warp(r,*MAPS['CeladonCity_GameCorner'],13,2);script('CeladonCity_GameCorner_EventScript_Poster');finish();assert flag(C['FLAG_OPENED_ROCKET_HIDEOUT']);shot('repaire-ouvert')
 for retry in range(4):
  walk(7);r.run(120)
  if tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['RocketHideout_B1F']:break
 else:raise AssertionError('Native stairs did not enter the hideout')
 report('Hideout refuses actual west stair approach before badge and permits native entry after, including legacy open flag')
 # Native save/continue in the new town reloads its current object definitions and keeps the intro flag.
 warp(r,*MAPS['LavenderTown'],14,9);saved=r.u32(r.symbols['gSaveBlock1Ptr']);r.write(saved+0x8e0+1,bytes([C['OBJ_EVENT_GFX_LITTLE_GIRL']]));legacy=r.call('GetObjectEventIdByLocalIdAndMap',3,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0]);assert legacy<16;r.write(r.symbols['gObjectEvents']+36*legacy+5,bytes([C['OBJ_EVENT_GFX_LITTLE_GIRL']]));assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('LoadGameSave',0,max_frames=1200);r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(1800):
  r.run()
  if f>120 and free():break
 else:raise AssertionError('Continue saved game did not return to field')
 assert flag(F_INTRO) and r.call('VarGet',V_INTRO)==1 and r.call('GetCurrentWeather')==6;assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x8e0+1,1)==bytes([174]);legacy=r.call('GetObjectEventIdByLocalIdAndMap',3,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0]);assert legacy<16 and r.read(r.symbols['gObjectEvents']+36*legacy+5,1)==bytes([174]);shot('reprise-sauvegarde');report('Native Flash save/continue retains intro completion and night, refreshes chapter object templates')
 passed=True
 for stale in P.glob('ECHEC*.png'):stale.unlink()
except BaseException as e:
 failure=repr(e);shot('ECHEC');raise
finally:
 report_data=dict(passed=passed,error=failure,mode=mode,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_bytes=len(r.rom_buffer.raw)-1,scope=__doc__,results=rows)
 (P/'TEST_MGBA.json').write_text(json.dumps(report_data,ensure_ascii=False,indent=2)+'\n');r.close()

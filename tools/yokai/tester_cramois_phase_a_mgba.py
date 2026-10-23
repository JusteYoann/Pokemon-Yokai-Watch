#!/usr/bin/env python3
"""Phase A visual fixtures. Native ROM, controller battles, explicit map/party setup.
Run --baseline with the archived pre-change ROM. Never edits enemy HP or outcome.
"""
import os,sys,json,struct,hashlib,traceback,subprocess
from pathlib import Path
from PIL import Image
from mgba_rpc import ROOT
baseline='--baseline' in sys.argv
private='_audio' in os.environ.get('YOKAI_QA_ROM','')
mode='prive' if private else 'public'
if baseline:
 os.environ['YOKAI_QA_ROM']='/tmp/cramois-baseline/pokefirered'+('_audio' if private else '')+'.gba'
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp,strong_party
from pilote_combat_mgba import battle_keys
D=ROOT/'docs/cramois-ile-passe/phase-a'/mode/('avant' if baseline else 'apres');D.mkdir(parents=True,exist_ok=True)
lut=struct.unpack('<32768H',(ROOT/'data/yokai/cramois-sepia-rgb555.bin').read_bytes())
r=None;rows=[];movies={};passed=False;failure=None

def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def run(n,key=None):r.keys=set() if key is None else {key};r.run(n)
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def free():return field() and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/(name+'-x4.png'))
def verify(mask,label):
 if baseline:mask=0
 night=tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['LavenderTown'] and field()
 # VBlank precedes a frame's palette animation. Sample a stable transfer frame.
 for attempt in range(16):
  run(1);source=struct.unpack('<512H',r.read(r.symbols['gPlttBufferFaded'],1024));actual=struct.unpack('<512H',r.read(0x05000000,1024))
  expected=tuple(lut[c&32767] if (mask>>(i//16))&1 else c for i,c in enumerate(source))
  if night:
   def old_night(c):
    red,green,blue=c&31,(c>>5)&31,(c>>10)&31
    return red*18//32 | (green*18//32)<<5 | ((blue*24+max(red,green,blue)*4)//32)<<10
   expected=tuple(old_night(c) if i<192 else c for i,c in enumerate(source))
  if actual==expected:break
 else:
  bad=[i for i in range(512) if actual[i]!=expected[i]]
  raise AssertionError((label,'hardware palette mismatch',bad[:40],[(i,hex(actual[i]),hex(expected[i])) for i in bad[:6]]))
 changed=sum(a!=b for a,b in zip(actual,source));assert changed>20 if mask or night else changed==0
 report(label,mask=hex(mask),hardware_colors_changed=changed,ui_banks_match_native_buffers=True,original_lavender_night=night)
 return actual

def finish(limit=30000):
 for f in range(limit):
  r.keys=battle_keys(r,f) if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 else ({8} if f%16<4 else set());r.run()
  if f>60 and free():run(12);return
 raise AssertionError('Native script/battle did not finish')
def script(name):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[name])
def save_continue():
 assert free();r.call('SaveMapView');assert r.call('TrySavingData',0,max_frames=1500)==1;assert r.call('LoadGameSave',0,max_frames=1500)==1;r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(2500):
  r.run()
  if f>180 and free():break
 else:raise AssertionError('Continue blocked')
 run(12)
def battle_capture(name,trainer=False,portrait=None,past=True):
 movie=[];captured=False;seen=False
 actions={int(parts[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(parts:=line.split())==3 and parts[2]=='HandleInputChooseAction'}
 for f in range(18000):
  r.keys={8} if f%16<4 else set();r.run()
  if f%6==0:movie.append(r.frame.copy())
  if r.u32(r.symbols['gMain']+4)!=r.symbols['BattleMainCB2']|1:continue
  if portrait is not None and not seen:
   sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
   if sid<64:
    sp=r.symbols['gSprites']+68*sid
    if r.read(sp+62,1)[0]&1 and struct.unpack('<H',r.read(sp+6,2))[0]==portrait and struct.unpack('<h',r.read(sp+36,2))[0]==0:
     run(180);portrait_mask=0x000f001c | (1 << (16+(int.from_bytes(r.read(sp+4,2),'little')>>12)));verify(portrait_mask,name+' portrait and UI palette');shot(name+'-portrait');seen=True
  if r.u32(r.symbols['gBattlerControllerFuncs']) in actions:
   run(10);verify(0x000f001c if past else 0,name+' battlefield, Yo-kai and healthbox palette');shot(name+'-combat');captured=True;break
 assert captured and (portrait is None or seen),(name,captured,seen)
 movies[name]=movie
 report(name+' native battle entry',trainer=trainer)

positions=[
 ('CinnabarIsland',12,11,'exterieur'),
 ('CinnabarIsland_PokemonCenter_1F',7,4,'centre'),
 ('CinnabarIsland_PokemonCenter_2F',6,4,'centre-etage'),
 ('CinnabarIsland_Mart',5,5,'boutique'),
 ('CinnabarIsland_PokemonLab_Entrance',3,6,'laboratoire-entree'),
 ('CinnabarIsland_PokemonLab_Lounge',7,6,'laboratoire-salon'),
 ('CinnabarIsland_PokemonLab_ResearchRoom',7,6,'laboratoire-recherche'),
 ('CinnabarIsland_PokemonLab_ExperimentRoom',11,5,'laboratoire-fossiles'),
 ('PokemonMansion_1F',8,28,'manoir-rdc'),
 ('PokemonMansion_2F',9,4,'manoir-etage-1'),
 ('PokemonMansion_3F',8,4,'manoir-etage-2'),
 ('PokemonMansion_B1F',34,28,'manoir-sous-sol'),
 ('CinnabarIsland_Gym',5,5,'arene'),
]
try:
 r=new_game();strong_party(r);r.call('VarSet',0x40f4,3)
 report('Native new game and baseline identity',baseline=baseline,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest())
 for name,x,y,label in positions:
  warp(r,*MAPS[name],x,y);verify(0x0fff1fff,label+' field palette');shot(label)
 # Start menu and dialogue preserve their palette while the world remains tinted.
 warp(r,*MAPS['CinnabarIsland'],12,11)
 run(1,3);run(100);verify(0x0fff1fff,'Start menu original interface banks');shot('menu-carte');run(1,0);run(50)
 r.call('CB2_BagMenuFromStartMenu');run(180);verify(0,'Fullscreen bag keeps original colors');shot('sac');run(1,0);run(180)
 if not free():run(1,0);run(60)
 verify(0x0fff1fff,'Bag exit restores tinted field')
 script('CinnabarIsland_EventScript_OldMan');run(320);verify(0x0fff1fff,'Dialogue original interface banks');shot('dialogue');finish()
 save_continue();verify(0x0fff1fff,'Native Save/Continue on island');shot('reprise-sauvegarde')
 # Walk through the native Centre entrance, then its actual exit.
 warp(r,*MAPS['CinnabarIsland_PokemonCenter_1F'],7,7);run(40,5);run(180)
 assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['CinnabarIsland']
 verify(0x0fff1fff,'Native Pokemon Center exit preserves sepia');shot('sortie-centre')
 # Show a real native wild battle, with a stated species/level fixture.
 warp(r,*MAPS['PokemonMansion_1F'],8,28)
 r.call('CreateMon',r.symbols['gEnemyParty'],C['SPECIES_PIDGEY'],30,20,1,100,0,0)
 r.call('StartWildBattle');battle_capture('sauvage');finish();verify(0x0fff1fff,'Wild victory returns to tinted mansion')
 # Native leader script; approved six-member team is never replaced.
 warp(r,*MAPS['CinnabarIsland_Gym'],5,5);script('CinnabarIsland_Gym_EventScript_Blaine')
 # Existing Champions suite reads trainer species ID from native .data/oam field.
 battle_capture('nathaniel',True,C.get('TRAINER_PIC_YOKAI_NATHANIEL',146))
 levels=[r.call('GetMonData',r.symbols['gEnemyParty']+100*i,C['MON_DATA_LEVEL'],0) for i in range(6)]
 assert levels==[40,41,41,42,43,45],levels
 run(2);finish();assert r.call('FlagGet',0x826);report('Native Nathaniel victory and Volcano Badge',levels=levels)
 verify(0x0fff1fff,'Champion victory returns to tinted Gym')
 # The island remains tinted in a postgame fixture, without pretending to beat the League here.
 r.call('FlagSet',C['FLAG_SYS_GAME_CLEAR']);warp(r,*MAPS['CinnabarIsland'],12,11);verify(0x0fff1fff,'Postgame-flag fixture keeps island palette')
 for name,x,y in [('PalletTown',8,8),('VermilionCity',33,30),('LavenderTown',8,8)]:
  warp(r,*MAPS[name],x,y);verify(0,name+' no residual sepia');shot('retour-'+name.lower())
 # Same two Yo-kai outside the island must use their original battle colors.
 warp(r,*MAPS['PalletTown'],8,8)
 r.call('CreateMon',r.symbols['gEnemyParty'],C['SPECIES_PIDGEY'],30,20,1,100,0,0)
 r.call('StartWildBattle');battle_capture('sauvage-hors-ile',past=False);finish();verify(0,'Outside-island wild victory leaves native colors')
 r.close();r=new_game(1);strong_party(r);r.call('VarSet',0x40f4,3);warp(r,*MAPS['CinnabarIsland_Gym'],5,5)
 verify(0x0fff1fff,'Michael overworld variant');shot('michael-carte');script('CinnabarIsland_Gym_EventScript_Blaine');battle_capture('michael',True,C.get('TRAINER_PIC_YOKAI_MICHAEL',147))
 report('Female player Michael portrait observed; full female victory deferred to Phase D')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True)
 if r:shot('ECHEC')
finally:
 for name,frames in movies.items():
  if frames:
   frames=frames[:350];frames[0].resize((480,320),Image.Resampling.NEAREST).save(D/(name+'-entree.gif'),save_all=True,append_images=[f.resize((480,320),Image.Resampling.NEAREST) for f in frames[1:]],duration=100,loop=0)
 if r:rom_hash=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close()
 else:rom_hash=None
 (D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,baseline=baseline,rom_sha256=rom_hash,checks=rows,failure=failure,scope=__doc__),ensure_ascii=False,indent=2)+'\n')
assert passed,failure

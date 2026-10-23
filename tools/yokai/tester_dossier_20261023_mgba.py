#!/usr/bin/env python3
"""Native mGBA controlled fixtures, NOT a full adventure or balance playthrough.
Maps/flags/player party/script entry are fixtures; no enemy HP, outcome, earned
badge/reward or enemy party order is patched. Controller earns each tested win.
"""
import json,os,re,struct,hashlib,subprocess,traceback,tempfile
from pathlib import Path
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
# Resolve native symbolic flag aliases used by the existing save layout.
for _ in range(5):
 for k,v in re.findall(r'^#define\s+(FLAG_\w+)\s+(FLAG_\w+)\s*$',(ROOT/'include/constants/flags.h').read_text(),re.M):
  if v in C:C[k]=C[v]
MODE='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/dossier-20261023/tests'/MODE;D.mkdir(parents=True,exist_ok=True)
rows=[];r=None;passed=False;failure=None
teams=json.loads((ROOT/'docs/dossier-20261023/ligue-equipes.json').read_text())
def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(D/(name+'-x3.png'))
def mon(i,enemy=False):return r.symbols['gEnemyParty' if enemy else 'gPlayerParty']+100*i
def val(i,key,enemy=False):return r.call('GetMonData',mon(i,enemy),C['MON_DATA_'+key],0)
def setval(i,key,value):r.w32(r.PARAMS+128,value);r.call('SetMonData',mon(i),C['MON_DATA_'+key],r.PARAMS+128)
def pulse(f):r.keys={8} if f%16<4 else set();r.run()
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def free():return field() and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2'
def script(name):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[name])
def text_finish(limit=4000):
 for f in range(limit):
  pulse(f)
  if f>60 and free():r.keys=set();r.run(8);return
 raise AssertionError(('text stuck',hex(r.u32(r.symbols['gMain']+4))))
def fight(name,expected=None,limit=26000,ordered=True):
 seen=[];frames=[];started=False;portrait=False
 for f in range(limit):
  pulse(f)
  battle=r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
  if battle:
   started=True
   if not portrait:
    sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
    if sid<64:
     s=r.symbols['gSprites']+68*sid
     if r.read(s+62,1)[0]&1 and r.read(s+6,2)!=b'\0\0' and int.from_bytes(r.read(s+36,2),'little',signed=True)==0 and r.frame.crop((120,0,240,100)).getbbox():shot(name+'-portrait');portrait=True
   if r.u32(r.symbols['gBattlerControllerFuncs']) in actions:
    idx=int.from_bytes(r.read(r.symbols['gBattlerPartyIndexes']+2,2),'little')
    if idx not in seen:seen.append(idx);shot(name+'-adversaire-'+str(idx))
  if started and f%18==0 and not os.environ.get('YOKAI_DOSSIER_NO_GIFS'):frames.append(r.frame.copy())
  if started and not battle and f>100 and free():break
 else:raise AssertionError((name,'battle did not finish',seen))
 r.keys=set();r.run(8)
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\1',(name,'not won')
 if expected is not None:assert (seen if ordered else sorted(seen))==list(range(expected)),(name,'wrong send-out order',seen)
 if frames:
  fs=[im.resize((480,320),Image.Resampling.NEAREST) for im in frames]
  fs[0].save(D/(name+'.gif'),save_all=True,append_images=fs[1:],duration=300,loop=0)
 report('Controller victory: '+name,opponent_indices=seen,frames=f,enemy_hp_or_outcome_patched=False)
try:
 r=new_game();actions={int(line.split()[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(line.split())==3 and line.split()[2]=='HandleInputChooseAction'};base=r.snapshot()
 # Native trainer generation, all eight League IDs and both sexes.
 for gender in [0,1]:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));r.w32(r.symbols['gBattleTypeFlags'],8)
  for key,team in teams.items():
   for suffix in ['', '_2']:
    trainer=C['TRAINER_ELITE_FOUR_'+key+suffix];count=r.call('CreateNPCTrainerParty',r.symbols['gEnemyParty'],trainer)
    actual=[(val(i,'SPECIES',True),val(i,'LEVEL',True)) for i in range(count)]
    assert actual==[(C['SPECIES_'+s],lv) for s,lv,moves in team]
    assert all(val(i,'ABILITY_NUM',True)==0 for i in range(count))
    r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',trainer));assert r.call('YokaiChampionOrderedPartySize')==6
    report('Native party '+key+suffix,gender=gender,party=actual,ordered=6)
 # Exact native XOR threshold over all65536 possibilities in a tiny test-only RAM loop.
 asm=f'''.syntax unified
.thumb
.global entry
.thumb_func
entry:
 push {{r4-r7,lr}}
 movs r5,r0
 movs r4,#0
 movs r6,#0
 ldr r7, ={r.symbols['SafariWildPersonality']|1}
loop:
 lsls r0,r4,#16
 ldr r2, =0xA5A5
 orrs r0,r2
 movs r1,r5
 bl invoke
 movs r1,r0
 lsrs r1,r1,#16
 eors r0,r1
 eors r0,r5
 lsrs r1,r5,#16
 eors r0,r1
 lsls r0,r0,#16
 lsrs r0,r0,#16
 cmp r0,#8
 bhs next
 adds r6,#1
next:
 adds r4,#1
 ldr r2, =65536
 cmp r4,r2
 blo loop
 movs r0,r6
 pop {{r4-r7,pc}}
invoke:
 bx r7
.pool
'''
 td=Path(tempfile.mkdtemp());(td/'x.s').write_text(asm);subprocess.run(['arm-none-eabi-as','-mcpu=arm7tdmi','-mthumb',str(td/'x.s'),'-o',str(td/'x.o')],check=True);subprocess.run(['arm-none-eabi-objcopy','-O','binary',str(td/'x.o'),str(td/'x.bin')],check=True)
 blob=(td/'x.bin').read_bytes();assert len(blob)<256;r.write(0x0203FD00,blob)
 for ot in [0,0x12345678,0xFFFFFFFF]:assert r.call(0x0203FD00,ot,max_frames=1200)==24
 report('Native exhaustive Safari XOR truth table',ot_values=3,outcomes_each=65536,shiny_each=24,exact_fraction='3/8192',regeneration=False)
 # Fixed-seed independent statistical distribution check, plus exact combinatorial proof above.
 import random
 rng=random.Random(20261023);n=2_000_000;hits=sum(1 for _ in range(n) if rng.getrandbits(16)<24);expect=n*24/65536
 assert abs(hits-expect)<6*(expect**.5)
 report('Safari statistical check of uniform XOR draws',draws=n,shiny=hits,expected=expect,seed=20261023)
 r.restore(base)
 for mapname,expected in [(x,True) for x in ['SafariZone_Center','SafariZone_East','SafariZone_North','SafariZone_West']]+[(x,False) for x in ['FuchsiaCity_SafariZone_Entrance','FuchsiaCity','VictoryRoad_3F','CinnabarIsland']]:
  warp(r,*MAPS[mapname],5,5);assert bool(r.call('IsSafariWildMap'))==expected
  # Exercise actual generation on each map and native checksum/personality getters.
  if expected:
   for species in [1,151]:
    r.call('GenerateWildMon',species,30,0);assert val(0,'SPECIES',True)==species;assert not val(0,'SANITY_IS_BAD_EGG',True)
  report('Safari map boundary: '+mapname,bonus=expected)
 # Quest gating and fixed encounter identity, independent of previous Enma trial.
 r.restore(base);r.call('FlagSet',0x82C);r.call('FlagClear',C['FLAG_YOKAI_ENMA_WON']);warp(r,*MAPS['CeruleanCave_B1F'],26,11);assert not r.call('FlagGet',C['FLAG_HIDE_MEWTWO']);shot('seigneur-enma-grotte-sans-quete')
 r.call('FlagSet',C['FLAG_YOKAI_ENMA_CAUGHT']);warp(r,*MAPS['CeruleanCave_B1F'],26,11);assert r.call('FlagGet',C['FLAG_HIDE_MEWTWO']);report('Enma appears without optional trial; caught Enma remains hidden')
 for clear in [False,True]:
  r.call('FlagSet' if clear else 'FlagClear',0x82C);r.call('FlagClear',0x32F);warp(r,*MAPS['MtEmber_Summit'],9,8);assert r.call('FlagGet',C['FLAG_HIDE_MOLTRES'])
  script('MtEmber_Summit_EventScript_Moltres');text_finish();assert field()
 report('Nyada locked before and after League while future quest flag is unset')
 # Real earned experience: leader + ordinary reserve + holder + egg + fainted holder.
 r.restore(base);warp(r,*MAPS['Route1'],10,10);experience=[]
 for holders in [[],[2],[0],[1,2]]:
  r.call('ZeroPlayerPartyMons')
  for i in range(5):r.call('CreateMon',mon(i),1,50,31,1,100+i,0,0)
  r.write(r.symbols['gPlayerPartyCount'],b'\5')
  for i in holders+[3,4]:setval(i,'HELD_ITEM',C['ITEM_EXP_SHARE'])
  setval(3,'IS_EGG',1);setval(4,'HP',0)
  for fieldname in ['ATK','SPATK','SPEED']:setval(0,fieldname,999)
  r.call('SetMonMoveSlot',mon(0),C['MOVE_AERIAL_ACE'],0)
  before=[val(i,'EXP') for i in range(5)]
  r.call('CreateMon',mon(0,True),1,5,31,1,555,0,0);r.write(r.symbols['gEnemyPartyCount'],b'\1');r.call('StartScriptedWildBattle');fight('experience-'+('-'.join(map(str,holders)) or 'sans-objet'),1)
  gains=[val(i,'EXP')-before[i] for i in range(5)];assert gains[0]>0
  for i in range(1,5):assert (gains[i]>0)==(i in holders and i<3),(holders,gains)
  experience.append({'holders':holders,'gains':gains})
 report('Native held-only Exp Share; reserves, egg and fainted exclusions',cases=experience)
 # New room assets and actual strict six-member sequence, including last two Nyada members.
 for key,room,label,name in [('LORELEI','Loreleis','Lorelei','zazel'),('BRUNO','Brunos','Bruno','enma-ancien'),('AGATHA','Agathas','Agatha','orqanos'),('LANCE','Lances','Lance','maitre-nyada')]:
  r.restore(base);r.call('VarSet',0x4068,1);warp(r,*MAPS['PokemonLeague_'+room+'Room'],5,7);strong_party(r);shot('salle-'+name)
  script('PokemonLeague_'+room+'Room_EventScript_'+label);fight('ligue-'+name,6)
 # Rescue reward before Gym; initial hard gate even for legacy/debug access.
 r.restore(base);warp(r,*MAPS['SaffronCity_Gym'],14,13);script('SaffronCity_Gym_EventScript_Sabrina');text_finish();assert not r.call('FlagGet',C['FLAG_DEFEATED_SABRINA']);shot('arene-yopple-occupee');report('Gym hard-gated until Yopple liberation')
 r.call('FlagSet',0x3E);warp(r,*MAPS['SilphCo_11F'],7,6);script('SilphCo_11F_EventScript_President');text_finish();assert r.call('CheckBagHasItem',C['ITEM_MASTER_BALL'],1);assert r.call('FlagGet',0x250);assert not r.call('FlagGet',C['FLAG_DEFEATED_SABRINA']);shot('master-ball-avant-arene');report('Master Ball earned after rescue, before Gym win')
 assert not r.call('CheckBagHasItem',C['ITEM_MASTER_BALL'],2);script('SilphCo_11F_EventScript_President');text_finish();assert not r.call('CheckBagHasItem',C['ITEM_MASTER_BALL'],2);report('Master Ball reward not duplicated')
 # Both Champion locations, native badges/TM; then actual postgame Gym rematch.
 warp(r,*MAPS['SaffronCity_Gym'],14,13);strong_party(r);shot('domniscian-arene');script('SaffronCity_Gym_EventScript_Sabrina');fight('domniscian-champion',5,ordered=False);assert r.call('FlagGet',0x825);assert r.call('CheckBagHasItem',C['ITEM_TM23'],1)
 r.call('FlagSet',0x82C);script('SaffronCity_Gym_EventScript_Sabrina');fight('domniscian-revanche-champion',5,ordered=False);assert r.call('CheckBagHasItem',C['ITEM_TM23'],1);assert not r.call('CheckBagHasItem',C['ITEM_TM23'],2)
 warp(r,*MAPS['SilphCo_11F'],10,14);assert r.call('FlagGet',C['FLAG_HIDE_YOKAI_DOMNISCIAN_GROUP']);shot('yopple-employes-postgame');report('Optional CEO cameo hidden after League; employees remain visible')
 for name in ['EmployeRouge','EmployeBleu']:
  strong_party(r);script('YokaiCameo_'+name);fight('yopple-'+name.lower(),2)
 warp(r,*MAPS['FuchsiaCity_Gym'],4,9);strong_party(r);shot('berenice-parmanie');script('FuchsiaCity_Gym_EventScript_Koga');fight('berenice-psy-parmanie',5,ordered=False);assert r.call('FlagGet',0x824);assert r.call('CheckBagHasItem',C['ITEM_TM29'],1)
 # New Enma front + back through real battle renderer, outside sepia region.
 r.restore(base);warp(r,*MAPS['Route1'],10,10)
 for enemy in [False,True]:r.call('CreateMon',mon(0,enemy),150,70,31,1,100,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.symbols['gEnemyPartyCount'],b'\1');r.call('StartScriptedWildBattle')
 for f in range(2500):
  pulse(f)
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in actions:r.keys=set();r.run(16);break
 else:raise AssertionError('Enma action menu absent')
 shot('seigneur-enma-combat-face-dos');report('New sword-design Enma front and back rendered with uniform axes')
 passed=True
except BaseException as e:
 failure=repr(e);traceback.print_exc()
 if r is not None:shot('ECHEC')
 raise
finally:
 if r is not None:
  rom=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba'));r.close()
  (D/'TEST_MGBA.json').write_text(json.dumps({'passed':passed,'rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'scope':__doc__,'results':rows,'failure':failure},ensure_ascii=False,indent=2)+'\n')

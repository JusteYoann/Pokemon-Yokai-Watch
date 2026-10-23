#!/usr/bin/env python3
"""Controlled native fixtures for badge math/obedience, Berenice poses, and
real Run/Master Ball refusals in Alyzon's trainer battle. Stat/flag fixtures are
isolated by a savestate; they do not count as earning badges or natural play.
"""
import os,re,json,hashlib,struct,subprocess
from pathlib import Path
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
rom=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba'));mode='prive' if '_audio' in rom.name else 'public';P=ROOT/'docs/champions-yokai-watch/validation'/mode;P.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False;failure=None
callbacks={int(line.split()[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(rom.with_suffix('.elf'))],text=True).splitlines() if len(line.split())==3 and line.split()[2]=='HandleInputChooseAction'}
def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def shot(name):r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(name+'-x3.png'))
def pulse(key,after=16):r.keys={key};r.run();r.keys=set();r.run(after)
def tick(f,key=8):r.keys={key} if f%16<4 else set();r.run()
def action(limit=8000):
 for f in range(limit):
  tick(f,0)
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:r.keys=set();r.run(8);return
 raise AssertionError('Action menu did not return')
def w16(a,v):r.write(a,struct.pack('<H',v))
def flag(n):return r.call('FlagGet',n)!=0
def base_damage(atk,defn,move):return r.call('CalculateBaseDamage',r.symbols['gBattleMons']+88*atk,r.symbols['gBattleMons']+88*defn,C[move],0,0,0,atk,defn)
try:
 warp(r,*MAPS['SaffronCity_Gym'],14,13)
 obj=r.call('GetObjectEventIdByLocalIdAndMap',7,MAPS['SaffronCity_Gym'][1],MAPS['SaffronCity_Gym'][0]);assert obj<16
 a=r.symbols['gObjectEvents']+36*obj;sid=r.read(a+4,1)[0];sprite=r.symbols['gSprites']+68*sid
 # Turn using native object animation, and inspect the visible tiles rather than
 # just the resource pointer. West/east share the same source with native flip.
 source=Image.open(ROOT/'graphics/yokai_characters/berenice/overworld.png');frames=[]
 for direction,frame,label in [(1,0,'face'),(2,1,'dos'),(3,2,'gauche'),(4,2,'droite')]:
  r.call('ObjectEventTurn',a,direction);r.run(4)
  attr=struct.unpack('<H',r.read(sprite+4,2))[0];tile=attr&1023
  raw=bytearray()
  for ty in range(4):
   for tx in range(2):
    for y in range(8):
     for x in range(0,8,2):raw.append(source.getpixel((16*frame+tx*8+x,ty*8+y))|source.getpixel((16*frame+tx*8+x+1,ty*8+y))<<4)
  assert r.read(0x06010000+32*tile,256)==bytes(raw),(label,'Berenice native frame')
  if direction in [3,4]:
   flip=bool(struct.unpack('<H',r.read(sprite+2,2))[0]&0x1000)
   assert flip==(direction==4),(label,'flip',flip)
  shot('berenice-'+label);frames.append(r.frame.copy())
 frames[0].resize((720,480),Image.Resampling.NEAREST).save(P/'berenice-quatre-orientations.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in frames[1:]],duration=600,loop=0)
 report('Berenice four native facings: approved PNG tiles, left/right native mirror, no redrawing')
 r.call('FlagSet',0x322);r.call('VarSet',0x40f3,1);warp(r,*MAPS['PokemonTower_7F'],11,5);r.call('ZeroPlayerPartyMons');strong_party(r);r.call('AddBagItem',C['ITEM_MASTER_BALL'],1)
 r.call('ScriptContext_SetupScript',r.symbols['PokemonTower_7F_EventScript_MrFuji']);action();original=r.snapshot()
 # Neutral battle structures; controlled flags affect only this mathematical fixture.
 for b in range(2):
  mon=r.symbols['gBattleMons']+88*b
  for off,value in [(0,1),(2,100),(4,100),(6,100 if b==0 else 105),(8,100),(10,100),(12,C['MOVE_TACKLE']),(40,100),(44,100),(46,0)]:w16(mon+off,value)
  r.write(mon+24,bytes([6]*8));r.write(mon+32,bytes([0,0,0,0]));r.write(mon+42,b'\x32');r.w32(mon+76,0);r.w32(mon+80,0)
 for i in range(8):r.call('FlagClear',0x820+i)
 physical=base_damage(0,1,'MOVE_TACKLE');r.call('FlagSet',0x820);boost=base_damage(0,1,'MOVE_TACKLE');assert boost>physical
 report('Badge Roche boosts native physical attack',without=physical,with_badge=boost)
 for i in range(8):r.call('FlagClear',0x820+i)
 physical=base_damage(1,0,'MOVE_TACKLE');r.call('FlagSet',0x824);boost=base_damage(1,0,'MOVE_TACKLE');assert boost<physical
 report('Badge Ame boosts native physical defense',without=physical,with_badge=boost)
 for i in range(8):r.call('FlagClear',0x820+i)
 a0=base_damage(0,1,'MOVE_EMBER');d0=base_damage(1,0,'MOVE_EMBER');r.call('FlagSet',0x826);a1=base_damage(0,1,'MOVE_EMBER');d1=base_damage(1,0,'MOVE_EMBER');assert a1>a0 and d1<d0
 report('Badge Volcan boosts native special attack and defense',attack=[a0,a1],defense=[d0,d1])
 for i in range(8):r.call('FlagClear',0x820+i)
 first=r.call('GetWhoStrikesFirst',0,1,1);r.call('FlagSet',0x822);second=r.call('GetWhoStrikesFirst',0,1,1);assert(first,second)==(1,0)
 report('Badge Foudre native speed bonus changes action order',without=first,with_badge=second)
 # A traded non-event Jibanyan, foreign OT; test deterministic caps and sampled
 # disobedience above them. Native source and flag IDs are preserved separately.
 mon=r.symbols['gBattleMons'];r.write(r.symbols['gBattlerAttacker'],b'\x00');r.w32(mon+84,0xFEEBCAFE);r.write(mon+60,b'\xbb\xbc\xbd\xbe\xbf\xff\xff\xff')
 for badge,cap,above in [(None,10,30),(0x821,30,50),(0x823,50,70),(0x825,70,90),(0x827,100,None)]:
  for i in range(8):r.call('FlagClear',0x820+i)
  if badge is not None:r.call('FlagSet',badge)
  r.write(mon+42,bytes([cap]));assert r.call('IsMonDisobedient')==0,(badge,cap)
  count=0
  if above:
   r.write(mon+42,bytes([above]))
   for seed in range(1,129):
    r.call('SeedRng',seed);count+=r.call('IsMonDisobedient')!=0
   assert count>0,(badge,above,'never disobedient')
  report('Native traded-mon obedience threshold',badge=badge,level=cap,above_level=above,above_disobedience_samples=count)
 r.restore(original)
 # Controller input earns all three preceding KOs. No enemy HP/index/outcome patch.
 for f in range(18000):
  tick(f)
  if r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks and struct.unpack('<H',r.read(r.symbols['gBattlerPartyIndexes']+2,2))[0]==3:r.keys=set();break
 else:raise AssertionError('Colossus not reached')
 before=r.read(r.symbols['gPlayerPartyCount'],1);assert before==b'\x01'
 pulse(7);pulse(5);pulse(8,90);shot('colosse-refus-fuite');action()
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\x00'
 # Cursor Run3 -> Fight0 -> Bag1. Select the only ball through the native bag UI.
 pulse(6);pulse(4);r.write(r.symbols['gBagMenuState']+6,b'\x02\x00');pulse(7);pulse(8,240);pulse(8,90);pulse(8,90);shot('colosse-refus-capture');action()
 assert r.read(r.symbols['gPlayerPartyCount'],1)==before and r.read(r.symbols['gBattleOutcome'],1)!=b'\x07'
 assert r.u32(r.symbols['gBattleTypeFlags'])&8 and not r.u32(r.symbols['gBattleTypeFlags'])&(1<<20)
 report('Actual Run and Master Ball attempts refused against trainer Colossus; native trainer-ball behavior retained',native_ball_consumed=not r.call('CheckBagHasItem',C['ITEM_MASTER_BALL'],1))
 # Runtime marker cannot leak onto Potofeu or other trainers/ordinary wild fights.
 assert r.call('YokaiChampionIsColossus',1)
 r.write(r.symbols['gBattlerPartyIndexes']+2,b'\x00\x00');assert not r.call('YokaiChampionIsColossus',1)
 w16(r.symbols['gTrainerBattleOpponent_A'],C['TRAINER_LEADER_KOGA']);r.write(r.symbols['gBattlerPartyIndexes']+2,b'\x03\x00');assert not r.call('YokaiChampionIsColossus',1)
 r.w32(r.symbols['gBattleTypeFlags'],0);assert not r.call('YokaiChampionIsColossus',1)
 report('Colossus marker scoped to Alyzon trainer battle and fourth enemy member')
 passed=True
except BaseException as e:
 failure=repr(e);print('FAIL',failure,flush=True);shot('ECHEC-effets');raise
finally:
 r.close();(P/'EFFETS_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),scope=__doc__,results=rows,failure=failure),ensure_ascii=False,indent=2)+'\n')

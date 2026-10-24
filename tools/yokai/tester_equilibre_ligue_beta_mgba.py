#!/usr/bin/env python3
"""Native League battles with legal offensive teams and controller-only decisions.
Fixtures: ordinary six-member team, IV20/EV80 per stat, full health per encounter.
No opponent/stat/HP/PP/outcome edits during battle. No bag items/revives used.
Damage estimates choose moves; the ROM alone resolves turns, AI and outcomes.
"""
import os,json,struct,hashlib,subprocess,traceback
from pathlib import Path
from mgba_new_game import new_game
from mafiamille_qa import C
from mgba_rpc import ROOT
OUT=ROOT/'docs/beta-retours-20261024/ligue';OUT.mkdir(parents=True,exist_ok=True)
LEVEL=int(os.environ.get('YOKAI_LEAGUE_LEVEL','60'));TRAINERS=list(map(int,os.environ.get('YOKAI_LEAGUE_TRAINERS','410,411,412,413').split(',')))
SEEDS=[int(v) for v in os.environ.get('YOKAI_LEAGUE_SEEDS','').split(',') if v] or [None]
TRIALS=[(tid,seed) for tid in TRAINERS for seed in SEEDS]
TEAM=[2,27,30,79,86,89]
TM_NUMBERS=[2,8,13,14,15,19,23,24,25,26,27,28,29,30,31,34,35,36,38,39,40,42,43,47]+[53,54]
# Source GBA item table order: HM01 follows TM50; HM03 Surf -> 53.
r=new_game();rows=[];failure=None
symbols={}
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines():
 v=line.split()
 if len(v)==3:symbols.setdefault(v[2],set()).add(int(v[0],16)|1)
rev={v|1:k for k,v in r.symbols.items()}
MOVES=[r.read(r.symbols['gBattleMoves']+12*i,12) for i in range(355)]
chart={}
raw=r.read(r.symbols['gTypeEffectiveness'],336)
for i in range(0,336,3):
 a,b,m=raw[i:i+3]
 if a<18 and b<18:chart[a,b]=m/10
species={n:r.read(r.symbols['gSpeciesInfo']+28*n,28) for n in TEAM}

def val(i,name):return r.call('GetMonData',r.symbols['gPlayerParty']+100*i,C[name],0)
def setval(i,name,v):r.w32(r.PARAMS+128,v);r.call('SetMonData',r.symbols['gPlayerParty']+100*i,C[name],r.PARAMS+128)
def multiplier(typ,types):
 result=1
 for t in set(types):result*=chart.get((typ,t),1)
 return result

def damage(move,att,deff):
 info=MOVES[move];power=info[1];typ=info[2]
 if not power or move in [12,13,19,32,49,63,68,69,76,82,90,91,101,117,120,138,149,153,143,130,162,243,248,264,315,353]:return 0
 if move==216:power=102
 physical=typ<=8;attack=att['atk'] if physical else att['spa'];defense=deff['def'] if physical else deff['spd']
 return ((2*att['level']/5+2)*power*attack/max(1,defense)/50+2)*(1.5 if typ in att['types'] else 1)*multiplier(typ,deff['types'])*(info[3] or 100)/100

def metadata(i):
 n=TEAM[i];s=species[n]
 return dict(species=n,level=LEVEL,atk=val(i,'MON_DATA_ATK'),spa=val(i,'MON_DATA_SPATK'),defense=val(i,'MON_DATA_DEF'),spd=val(i,'MON_DATA_SPDEF'),types=list(s[6:8]),moves=[val(i,'MON_DATA_MOVE1')])

def native_mon(side):
 b=r.read(r.symbols['gBattleMons']+88*side,88);u=lambda x:struct.unpack_from('<H',b,x)[0]
 stages=b[24:32];scale=lambda stage:(stage-4)/2 if stage>=6 else 2/(8-stage)
 return dict(species=u(0),level=b[42],hp=u(40),maxhp=u(44),atk=u(2)*scale(stages[1]),spa=u(8)*scale(stages[4]),**{'def':u(4)*scale(stages[2]),'spd':u(10)*scale(stages[5])},types=list(b[33:35]),moves=list(struct.unpack_from('<4H',b,12)),pp=list(b[36:40]))

try:
 r.call('ZeroPlayerPartyMons');roster=[]
 for i,n in enumerate(TEAM):
  r.call('CreateMon',r.symbols['gPlayerParty']+100*i,n,LEVEL,20,1,100+i*25,0,0)
  for attr in ['HP','ATK','DEF','SPEED','SPATK','SPDEF']:setval(i,'MON_DATA_'+attr+'_EV',80)
  setval(i,'MON_DATA_FRIENDSHIP',255);r.call('CalculateMonStats',r.symbols['gPlayerParty']+100*i)
  ptr=r.u32(r.symbols['gLevelUpLearnsets']+4*n);pool=set()
  for k in range(100):
   word=struct.unpack('<H',r.read(ptr+2*k,2))[0]
   if word==65535:break
   if word>>9<=LEVEL:pool.add(word&511)
  for tm in TM_NUMBERS:
   if r.call('CanMonLearnTMHM',r.symbols['gPlayerParty']+100*i,tm-1):pool.add(struct.unpack('<H',r.read(r.symbols['sTMHMMoves']+2*(tm-1),2))[0])
  att=dict(level=LEVEL,atk=val(i,'MON_DATA_ATK'),spa=val(i,'MON_DATA_SPATK'),types=list(species[n][6:8]))
  target={'def':100,'spd':100,'types':[0,0]};chosen=[];usedtypes=set()
  for move in sorted(pool,key=lambda m:damage(m,att,target),reverse=True):
   if damage(move,att,target)<=0:continue
   typ=MOVES[move][2]
   if typ in usedtypes:continue
   usedtypes.add(typ);chosen.append(move)
   if len(chosen)==4:break
  for move in sorted(pool,key=lambda m:damage(m,att,target),reverse=True):
   if len(chosen)>=4:break
   if move not in chosen and damage(move,att,target)>0:chosen.append(move)
  assert chosen
  while len(chosen)<4:chosen.append(chosen[0])
  for k,m in enumerate(chosen):r.call('SetMonMoveSlot',r.symbols['gPlayerParty']+100*i,m,k)
  roster.append(dict(species=n,level=LEVEL,iv=20,ev_per_stat=80,moves=chosen,legal_pool=sorted(pool),stats={k:val(i,'MON_DATA_'+k) for k in ['MAX_HP','ATK','DEF','SPEED','SPATK','SPDEF']}))
 r.write(r.symbols['gPlayerPartyCount'],b'\x06');base=r.snapshot();print('TEAM',roster,flush=True)
 for tid,seed in TRIALS:
  r.restore(base);r.keys=set();
  if seed is not None:r.w32(r.symbols['gRngValue'],seed)
  r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',tid));r.call('StartTrainerBattle');seen=False;turns=[];nextkeys={8};opponents=[];laststate=None
  for f in range(60000):
   if f%10000==0:
    print('PROGRESS',tid,f,hex(r.u32(r.symbols['gMain']+4)),flush=True);r.frame.save(OUT/f'progress-{LEVEL}-{tid}.png')
   if f%12==0:
    nextkeys={8};cb=r.u32(r.symbols['gMain']+4)
    tasks={rev.get(r.u32(r.symbols['gTasks']+40*i)) for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01'}
    controller=r.u32(r.symbols['gBattlerControllerFuncs'])
    if cb==r.symbols['BattleMainCB2']|1:
     seen=True;enemy=native_mon(1)
     if enemy['species'] not in opponents:opponents.append(enemy['species'])
     if controller in symbols.get('HandleInputChooseAction',set()):
      cursor=r.read(r.symbols['gActionSelectionCursor'],1)[0]
      nextkeys={6 if cursor&1 else 4} if cursor else {8}
     elif controller in symbols.get('HandleInputChooseMove',set()):
      att=native_mon(0);r.keys=set();mask=r.call('CheckMoveLimitations',0,0,255)&15
      choices=[i for i in range(4) if not mask&(1<<i)]
      if choices:
       target=max(choices,key=lambda k:damage(att['moves'][k],att,enemy));cur=r.read(r.symbols['gMoveSelectionCursor'],1)[0]
       nextkeys={7 if target&1 else 6} if (cur&1)!=(target&1) else {5 if target&2 else 4} if cur!=target else {8}
       state=(att['species'],att['hp'],tuple(att['pp']),enemy['species'],enemy['hp'])
       if cur==target and state!=laststate:turns.append(dict(attacker=att['species'],hp=att['hp'],enemy=enemy['species'],enemy_hp=enemy['hp'],move=att['moves'][target]));laststate=state
    if 'Task_HandleChooseMonInput' in tasks:
     r.keys=set();healthy=[i for i in range(6) if int.from_bytes(r.read(r.symbols['gPlayerParty']+100*i+86,2),'little')>0]
     current=r.read(r.symbols['gPartyMenu']+9,1)[0]
     # Default NEXT healthy slot, avoiding fainted mons and the currently active one.
     active=0  # Native party menu temporarily moves the active mon to slot 0.
     choices=[i for i in healthy if i!=active] or healthy
     target=choices[0] if choices else 6
     if current==target:nextkeys={8}
     else:nextkeys={5 if current<target else 4}
   r.keys=nextkeys if f%12<2 else set();r.run()
   if seen:
    outcome=r.read(r.symbols['gBattleOutcome'],1)[0]
    if outcome in [1,2] and r.u32(r.symbols['gMain']+4)!=r.symbols['BattleMainCB2']|1:break
  else:
   r.frame.save(OUT/f'blocage-{LEVEL}-{tid}.png');raise AssertionError(('Battle driver timeout',LEVEL,tid,hex(r.u32(r.symbols['gMain']+4)),tasks,controller))
  r.keys=set();r.frame.save(OUT/f'fin-{LEVEL}-{tid}.png')
  row=dict(trainer=tid,seed=seed,level=LEVEL,native_outcome=outcome,victory=outcome==1,frames=f,opponents_seen=opponents,decisions=turns)
  rows.append(row);print('BATTLE',row,flush=True)
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True)
finally:
 (OUT/(f'TEST_L{LEVEL}_'+ '-'.join(map(str,TRAINERS))+'_'+ '-'.join(map(str,SEEDS))+'.json')).write_text(json.dumps(dict(error=failure,completed=len(rows)==len(TRIALS),scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),team=locals().get('roster'),results=rows),indent=2)+'\n');r.close()
if failure:raise SystemExit(1)

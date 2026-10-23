#!/usr/bin/env python3
"""Exploratory native fights, normal level/stat creation and legal natural/TM moves.
A simple power/type pilot uses no items or voluntary switches. These trials are
not a human balance approval. Opponents, HP and outcomes are never edited.
"""
import json,os,struct,hashlib,subprocess
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C
Q=ROOT/'QA_RECETTE_FINALE/DON_SPIRATON/ETAPE_B/jalon4/equilibrage';Q.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];base=r.snapshot();complete=False
rom=r.rom_buffer.raw[:-1]
# BattleMove is12 bytes in the target ABI (checked by symbol size in the build).
moves=[rom[r.symbols['gBattleMoves']-0x8000000+12*i:r.symbols['gBattleMoves']-0x8000000+12*i+12] for i in range(355)]
callbacks={int(v[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=l.split())==3 and v[2]=='HandleInputChooseMove'}
types={};p=r.symbols['gTypeEffectiveness']-0x8000000
for i in range(200):
 a,b,v=rom[p+3*i:p+3*i+3]
 if a==255:break
 if a!=254:types[a,b]=v/10
team=[1,7,25,44,74,100]
def eff(t,a,b):return types.get((t,a),1)*(types.get((t,b),1) if a!=b else 1)
try:
 for level in [56,60,63]:
  r.restore(base);opt=r.u32(r.symbols['gSaveBlock2Ptr'])+21;r.write(opt,bytes([r.read(opt,1)[0]|2]));roster=[]
  for i,species in enumerate(team):
   mon=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',mon,species,level,24,1,100+i,0,0x1234)
   legal=[m for m in range(1,355) if moves[m][1]>1 and r.call('SpiratonCoreMoveLegal',species,level,m)]
   legal.sort(key=lambda m:moves[m][1]*moves[m][3]/100,reverse=True)
   chosen=[];seen=set()
   for m in legal:
    if moves[m][2] not in seen:chosen.append(m);seen.add(moves[m][2])
    if len(chosen)==4:break
   chosen+=( [m for m in legal if m not in chosen][:4-len(chosen)] )
   for slot in range(4):r.call('SetMonMoveSlot',mon,chosen[slot] if slot<len(chosen) else 0,slot)
   roster.append(dict(species=species,level=level,hp=r.call('GetMonData',mon,C['MON_DATA_MAX_HP'],0),moves=chosen,stats_unmodified=True))
  r.write(r.symbols['gPlayerPartyCount'],b'\6');prepared=r.snapshot()
  for trainer in [743,744]:
   # Separate healed starts isolate classic difficulty from eight-life difficulty.
   r.restore(prepared)
   if trainer==744:r.call('SpiratonBattleArmPrototype')
   r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',trainer));r.call('StartTrainerBattle')
   started=False;phases=[];turns=0;lastturn=-1;party_target=None;nextkeys={8};result='timeout'
   for f in range(65000):
    cb=r.u32(r.symbols['gMain']+4)
    if f%16==0:
     nextkeys={8}
     if cb==r.symbols['CB2_UpdatePartyMenu']|1:
      if party_target is None:
       active=r.read(r.symbols['gBattlerPartyIndexes'],1)[0]
       live=[i for i in range(6) if i!=active and r.call('GetMonData',r.symbols['gPlayerParty']+100*i,C['MON_DATA_HP'],0)>0]
       party_target=live[0] if live else 0
      current=r.read(r.symbols['gPartyMenu']+9,1)[0]
      if current!=party_target:nextkeys={7 if current==0 else 6 if party_target==0 else 5 if current<party_target else 4}
     else:
      party_target=None
      if cb==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:
       mask=r.call('CheckMoveLimitations',0,0,255)&15;mon=r.read(r.symbols['gBattleMons'],176);choices=[i for i in range(4) if not mask&(1<<i)]
       def score(i):
        move=int.from_bytes(mon[12+2*i:14+2*i],'little');d=moves[move];typ=d[2];power=d[1]
        atk=int.from_bytes(mon[2:4] if typ<9 else mon[8:10],'little');defense=int.from_bytes(mon[92:94] if typ<9 else mon[98:100],'little')
        return power*max(d[3],1)*eff(typ,mon[121],mon[122])*(1.5 if typ in mon[33:35] else 1)*atk/max(defense,1)
       if choices:
        target=max(choices,key=score);current=r.read(r.symbols['gMoveSelectionCursor'],1)[0]
        if target!=current:nextkeys={7 if target&1 else 6} if (target&1)!=(current&1) else {5 if target&2 else 4}
    r.keys=nextkeys if f%16<4 else set();r.run()
    if cb==r.symbols['BattleMainCB2']|1:
     started=True
     turn=r.read(r.symbols['gBattleResults']+0x13,1)[0] if False else 0
     if trainer==744:
      lv=r.read(r.symbols['gBattleMons']+130,1)[0]
      if 56<=lv<=63 and lv not in phases:phases.append(lv)
     outcome=r.read(r.symbols['gBattleOutcome'],1)[0]
     if outcome in [1,2,3]:result={1:'victory',2:'defeat',3:'draw'}[outcome];break
    elif started and cb==r.symbols['CB2_Overworld']|1:
     outcome=r.read(r.symbols['gBattleOutcome'],1)[0];result=str(outcome);break
   living=sum(r.call('GetMonData',r.symbols['gPlayerParty']+100*i,C['MON_DATA_HP'],0)>0 for i in range(6))
   r.frame.save(Q/f'niveau-{level}-combat-{trainer}.png')
   rows.append(dict(level=level,trainer=trainer,result=result,emulated_frames=f,emulated_seconds=round(f/59.7275,1),phases=phases,surviving_party=living,roster=roster,policy='best simple visible damage score; legal natural/TM, no items, no voluntary switches'))
   (Q/'MESURES.json').write_text(json.dumps(dict(complete=False,scope=__doc__,rom_sha256=hashlib.sha256(rom).hexdigest(),trials=rows),indent=2)+'\n')
 complete=True
finally:
 (Q/'MESURES.json').write_text(json.dumps(dict(complete=complete,scope=__doc__,rom_sha256=hashlib.sha256(rom).hexdigest(),trials=rows),indent=2)+'\n');r.close()
print('Exploratory normal-stat trials complete:',[(x['level'],x['trainer'],x['result']) for x in rows])

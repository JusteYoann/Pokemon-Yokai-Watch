#!/usr/bin/env python3
"""Native diagnostic guards and simultaneous self-KO. Fresh QA party/entry.
Run is attempted through controller input. Capture checks the native ball command
with a Master Ball fixture directly; this is not a complete bag UI interaction.
"""
import hashlib,json,struct,subprocess
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,strong_party
from pilote_combat_mgba import battle_keys
Q=ROOT/'QA_RECETTE_FINALE/DON_SPIRATON/limites';Q.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;rows=[]
def pulse(key,after=8):
 r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(after)
try:
 strong_party(r);r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_EXPLOSION'],0)
 r.call('SpiratonBattleArmPrototype');r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',744));r.call('StartTrainerBattle')
 callbacks={int(v[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=l.split())==3 and v[2]=='HandleInputChooseAction'}
 for f in range(3000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Initial menu absent')
 r.keys=set();r.run(30);base=r.snapshot()
 # Actual Run selection: down, right, A. First transform must still wait.
 pulse(5);pulse(7);pulse(8,0)
 expected=r.read(r.symbols['sText_NoRunningFromTrainers'],80).split(b'\xff')[0];seen=False
 for f in range(700):
  r.keys={8} if f%16<4 else set();r.run()
  if r.read(r.symbols['gDisplayedStringBattle'],len(expected))==expected:
   seen=True;r.frame.save(Q/'fuite-interdite.png');break
 assert seen and r.read(r.symbols['gBattleOutcome'],1)==b'\0'
 assert r.read(r.symbols['sFirst'],1)==b'\1','Rejected run must not start first turn'
 rows.append(dict(test='Controller Run rejected before first transform',passed=True));r.restore(base)
 # Native handler tests trainer block before capture odds, even for Master Ball.
 r.keys=set();r.write(r.symbols['gBattlerAttacker'],b'\0');r.write(r.symbols['gLastUsedItem'],struct.pack('<H',C['ITEM_MASTER_BALL']))
 # Explicit command fixture: release the menu controller handshake only here.
 r.w32(r.symbols['gBattleControllerExecFlags'],0)
 r.call('Cmd_handleballthrow')
 assert r.u32(r.symbols['gBattlescriptCurrInstr'])==r.symbols['BattleScript_TrainerBallBlock']
 assert r.read(r.symbols['gBattleOutcome'],1)==b'\0'
 rows.append(dict(test='Native Master Ball handler chooses trainer block, no capture calculation; injected command fixture, not bag UI',passed=True));r.restore(base)
 # Explosion truly executes: both battlers reach zero, pending layer is not a win.
 pending_seen=False;lost=False
 for f in range(9000):
  r.keys=battle_keys(r,f);r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   mon=r.read(r.symbols['gBattleMons'],176)
   hp0=int.from_bytes(mon[40:42],'little');hp1=int.from_bytes(mon[128:130],'little')
   if hp0==0 and hp1==0:pending_seen=True
   outcome=r.read(r.symbols['gBattleOutcome'],1)[0]
   assert outcome!=1,'Player self-KO at layer one must not win the boss'
   if outcome==2:
    lost=True;r.frame.save(Q/'ko-simultane-defaite.png');break
 assert pending_seen and lost,(pending_seen,lost)
 assert r.call('SpiratonBattleInspect',2)==0,'Loss must not advance a new phase'
 rows.append(dict(test='Real Explosion defeats player and exhausts layer one; loss, no false victory or new phase',passed=True))
 # Same real self-KO with a healthy backup: replacement precedes counter choice.
 r.restore(base)
 backup=r.symbols['gPlayerParty']+100
 r.call('CreateMon',backup,7,65,31,1,101,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x02')
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_SPATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(r.PARAMS+160,999);r.call('SetMonData',backup,C[field],r.PARAMS+160)
 for slot,move in enumerate(['MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_SWIFT','MOVE_MAGICAL_LEAF']):r.call('SetMonMoveSlot',backup,C[move],slot)
 picked=False;transformed=False;expected_species=None
 for f in range(13000):
  cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['CB2_UpdatePartyMenu']|1 and not picked:
   r.keys=set();r.run(120);pulse(7,12);pulse(8,12);pulse(8,12);picked=True
  r.keys=battle_keys(r,f);r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   mon=r.read(r.symbols['gBattleMons'],176)
   player_species=int.from_bytes(mon[:2],'little')
   if player_species==7 and expected_species is None:
    # Independent core state, public snapshot only; never mutate live boss state.
    target=r.PARAMS+128;state=r.PARAMS+64
    r.write(target,struct.pack('<HB2Bx4H',7,mon[42],mon[33],mon[34],0,0,0,0))
    assert r.call('SpiratonCoreStart',state,52,target)
    r.call('SpiratonCoreDamage',state,65535)
    expected_species=r.call('SpiratonCoreSelect',state,target)
   if mon[130]==57 and player_species==7:
    actual=int.from_bytes(mon[88:90],'little')
    assert expected_species is not None and actual==expected_species,(actual,expected_species)
    r.frame.save(Q/'remplacement-avant-contre.png');transformed=True;break
 assert picked and transformed,(picked,transformed)
 rows.append(dict(test='Player Explosion with healthy backup: controller replacement enters before end-turn selection; next form matches active replacement snapshot',passed=True,active_species=7,expected_counter=expected_species))
 passed=True
finally:
 (Q/'LIMITES_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),indent=2)+'\n');r.close()
print('PASS: Run rejected, native Master Ball blocked, simultaneous layer/player KO loses correctly')

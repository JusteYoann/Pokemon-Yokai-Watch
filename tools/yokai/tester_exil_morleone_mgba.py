#!/usr/bin/env python3
"""Existing house/door, conditional resident, actual Yes/No, two real rematches,
Flash reload and normal defeat in mGBA. Progression flags are explicit fixtures:
this does NOT claim the unfinished first League finale has been played.
Winning party is level100/999 stats; losing party level1/1 stats. No enemy edits.
"""
import json,hashlib,struct,os
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
from pilote_combat_mgba import battle_keys
Q=ROOT/os.environ.get('YOKAI_EXILE_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON/EXIL/public');Q.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;rows=[]
HOUSE='SixIsland_WaterPath_House2';OUT='SixIsland_WaterPath'

def at_map(name):return r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)==bytes(MAPS[name])
def actors():
 out={}
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1 and b[9:11]==bytes([MAPS[HOUSE][1],MAPS[HOUSE][0]]):out[b[8]]=b[5]
 return out

def pos():
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1 and b[8]==255:
   x,y=struct.unpack_from('<hh',b,16);return x-7,y-7
 raise AssertionError('Player object absent')

def pulse(key,after=10):
 r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(after)
def walk(key):
 x,y=pos();dx,dy={4:(0,-1),5:(0,1),6:(-1,0),7:(1,0)}[key];goal=(x+dx,y+dy)
 for f in range(40):
  r.keys={key};r.run()
  if pos()==goal:
   r.keys=set();r.run(20);return
 raise AssertionError(('Blocked native walk',pos(),goal,key))
def idle(maxframes=2000):
 stable=0
 def free():
  return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.read(r.symbols['sLockFieldControls'],1)==b'\0'
 for f in range(maxframes):
  # Never press A while field control is free: it would talk to Don again.
  r.keys=set() if free() else ({8} if f%16<4 else set());r.run()
  stable=stable+1 if free() else 0
  if stable>=60:r.keys=set();return
 raise AssertionError('Field script did not finish')
def enter(don):
 warp(r,*MAPS[OUT],11,20)
 for f in range(240):
  r.keys={4};r.run()
  if at_map(HOUSE):break
 else:raise AssertionError('Normal front door did not enter house')
 r.keys=set();r.run(360)
 a=actors();expected={255:C['OBJ_EVENT_GFX_RED_NORMAL'],2:C['OBJ_EVENT_GFX_YOKAI_DONMORLEONE']} if don else None
 npcs={k:v for k,v in a.items() if k!=255}
 assert npcs==({2:C['OBJ_EVENT_GFX_YOKAI_DONMORLEONE']} if don else {1:C['OBJ_EVENT_GFX_MAN']}),(don,a)
 if pos()==(4,7):walk(4)
 assert pos()==(4,6),pos()
def approach():
 for key in (7,7,7,4):walk(key)
 assert pos()==(7,5),pos();pulse(4)
def talk_to_choice():
 if pos()==(4,6):approach()
 else:
  assert pos()==(7,5),pos();pulse(4)
 pulse(8,0)
 task=r.symbols['Task_YesNoMenu_HandleInput']|1
 for f in range(2400):
  r.keys={8} if f%16<4 else set();r.run()
  if any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' and r.u32(r.symbols['gTasks']+40*i)==task for i in range(16)):
   r.keys=set();r.run(40);return
 raise AssertionError('Don Yes/No menu absent')
def leave_from_don():
 walk(5)
 for _ in range(3):walk(6)
 assert pos()==(4,6)
 for f in range(240):
  r.keys={5};r.run()
  if at_map(OUT):break
 else:raise AssertionError('Normal house exit failed')
 r.keys=set();r.run(360)
def story_flags():
 return dict(game_clear=r.call('FlagGet',0x82C),defeated_champ=r.call('FlagGet',C['FLAG_DEFEATED_CHAMP']),first_don=r.call('HasTrainerBeenFought',743) if 'HasTrainerBeenFought' in r.symbols else r.call('FlagGet',0x500+743),spiraton=r.call('FlagGet',0x500+744))
def permanent_flags():return r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0xEE0+4,0x120-4)
def battle(stem,loss=False):
 started=False;roster_checked=False;private_music=False;native_music=349
 for f in range(22000):
  r.keys=battle_keys(r,f);r.run();cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['BattleMainCB2']|1:
   started=True
   assert int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')==743
   if not roster_checked:
    roster=[(r.call('GetMonData',r.symbols['gEnemyParty']+100*i,C['MON_DATA_SPECIES'],0),r.call('GetMonData',r.symbols['gEnemyParty']+100*i,C['MON_DATA_LEVEL'],0)) for i in range(6)]
    assert roster==[(147,56),(70,57),(140,56),(136,58),(115,57),(86,60)],roster
    moves=[['ROCK_SLIDE','IRON_DEFENSE','REST','EARTHQUAKE'],['SHADOW_BALL','ROCK_SLIDE','EARTHQUAKE','THUNDER_WAVE'],['GIGA_DRAIN','CALM_MIND','HEAL_BELL','LIGHT_SCREEN'],['PSYCHIC','BODY_SLAM','FUTURE_SIGHT','RECOVER'],['NIGHT_SHADE','CONFUSE_RAY','WILL_O_WISP','PAIN_SPLIT'],['BRICK_BREAK','SURF','CROSS_CHOP','BODY_SLAM']]
    for i,expected in enumerate(moves):
     mon=r.symbols['gEnemyParty']+100*i
     assert [r.call('GetMonData',mon,C['MON_DATA_MOVE1']+j,0) for j in range(4)]==[C['MOVE_'+m] for m in expected]
     assert r.call('GetMonData',mon,C['MON_DATA_HELD_ITEM'],0)==0
    assert r.call('GetBattleBGM')==native_music
    assert not r.call('SpiratonBattleIsBoss',1)
    roster_checked=True
   if 'mus_yokai_03' in r.symbols and r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_03']:
    wave=r.symbols['yokai_wave_03']
    private_music|=any(r.u32(r.symbols['gSoundInfo']+80+64*i+36)==wave and r.read(r.symbols['gSoundInfo']+80+64*i,1)[0]&0x83 for i in range(5))
   if f==1024:r.frame.save(Q/f'{stem}-combat.png')
  if started and cb==r.symbols['CB2_Overworld']|1:
   outcome=r.read(r.symbols['gBattleOutcome'],1)[0]
   if outcome==(2 if loss else 1):
    idle(4000)
    if not loss:
     assert at_map(HOUSE);assert {k:v for k,v in actors().items() if k!=255}=={2:C['OBJ_EVENT_GFX_YOKAI_DONMORLEONE']}
    if 'mus_yokai_03' in r.symbols:assert private_music,'Private Ghoulfather channel not observed'
    r.frame.save(Q/f'{stem}-retour.png')
    return dict(test=stem,passed=True,outcome=outcome,roster=roster,ghoulfather_identifier=native_music,private_mixer_checked='mus_yokai_03' in r.symbols,private_channel_observed=private_music if 'mus_yokai_03' in r.symbols else None,frames=f)
 raise AssertionError(('Battle timeout',stem,started,hex(r.u32(r.symbols['gMain']+4)),r.read(r.symbols['gBattleOutcome'],1).hex()))
try:
 strong_party(r);base=r.snapshot()
 for stem,clear,don,spirit in [('avant-ligue',False,False,False),('premier-don-seulement',False,True,False),('ancienne-ligue-sans-boss',True,True,False),('boss-sans-pantheon',False,True,True),('apres-victoire-finale',True,True,True)]:
  r.restore(base)
  r.call('FlagSet' if clear else 'FlagClear',0x82C)
  for tid,on in [(743,don),(744,spirit)]:r.call('SetTrainerFlag' if on else 'ClearTrainerFlag',tid)
  enter(clear and spirit);r.frame.save(Q/f'{stem}.png')
  rows.append(dict(test='Conditional occupant plus real door entry',scenario=stem,fixture_game_clear=clear,fixture_first_don=don,fixture_spiraton=spirit,visible_npc=2 if clear and spirit else 1,passed=True))
  if stem=='avant-ligue':
   approach();pulse(8,180);r.frame.save(Q/'dialogue-habitant-original.png');idle()
   assert r.read(r.symbols['gBattleOutcome'],1)[0]!=1
 # Last case is the eligible Don house. Exercise choice and repeated battles.
 before=story_flags();permanent=permanent_flags();talk_to_choice();r.frame.save(Q/'dialogue-oui-non.png');pulse(5);pulse(8,180);r.frame.save(Q/'dialogue-refus.png');idle()
 assert story_flags()==before and permanent_flags()==permanent
 rows.append(dict(test='Controller No choice, original progression preserved, no battle',passed=True))
 # Already standing below Don; return to entrance for the common approach helper.
 leave_from_don();enter(True)
 for repeat in (1,2):
  r.call('HealPlayerParty');before=story_flags();permanent=permanent_flags();talk_to_choice();pulse(8)
  rows.append(battle(f'revanche-{repeat}'))
  assert story_flags()==before and permanent_flags()==permanent,'Rematch altered permanent story flags'
  # Second rematch starts immediately by talking again, without leaving/reloading.
 assert r.call('TrySavingData',0,max_frames=1200)==1
 r.call('FlagClear',0x82C);r.call('ClearTrainerFlag',744)
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 assert r.call('FlagGet',0x82C) and r.call('FlagGet',0x500+744)
 enter(True);r.frame.save(Q/'apres-sauvegarde-rechargement.png')
 rows.append(dict(test='Native Flash save/reload and normal door re-entry retain exiled Don',passed=True))
 # Real loss fixture, normal respawn at the island6 Pokemon Center.
 r.call('SetLastHealLocationWarp',20)
 r.call('CreateMon',r.symbols['gPlayerParty'],1,1,1,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_SPATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(r.PARAMS+128,1);r.call('SetMonData',r.symbols['gPlayerParty'],C[field],r.PARAMS+128)
 for i in range(4):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_TACKLE'] if i==0 else 0,i)
 before=story_flags();talk_to_choice();pulse(8);rows.append(battle('defaite',loss=True));assert story_flags()==before
 r.keys=set();r.run(360);idle(4000);r.keys=set();r.run(120)
 assert at_map('SixIsland_PokemonCenter_1F'),'Normal defeat did not reach island6 Pokemon Center'
 assert r.call('GetMonData',r.symbols['gPlayerParty'],C['MON_DATA_HP'],0)>0,'Whiteout did not heal the player'
 r.frame.save(Q/'defaite-centre-pokemon.png')
 enter(True);r.frame.save(Q/'don-present-apres-defaite.png')
 rows.append(dict(test='Normal loss/whiteout preserves unlock and Don remains on next visit',passed=True))
 # No navigation unlock is written by the house; flags outside TEMP6/7 are preserved in wins.
 passed=True
finally:
 if not passed:r.frame.save(Q/'diagnostic.png')
 (Q/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),house=HOUSE,progression_gate='GAME_CLEAR and native defeated-trainer744 flag; no new permanent flag',native_first_league_playthrough_tested=False,results=rows),ensure_ascii=False,indent=2)+'\n');r.close()
print('PASS: exile gate, real doors/dialogue, two exact rematches, Flash reload and loss')

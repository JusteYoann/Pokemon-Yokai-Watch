#!/usr/bin/env python3
"""Native mGBA quest fixtures: real A interaction, refusal, loss, six-mon win,
white scene, unique charm, Flash save/Continue and gender variant. Map, flags,
Medallium ownership and player parties are fixtures, not an adventure playthrough.
Enemy HP, trainer party, outcome, NPC graphics and OAM are never patched.
"""
import os,json,struct,hashlib,subprocess,traceback
from pathlib import Path
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp,strong_party
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/juste-yoann/integration'/mode;D.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False;failure=None
ROOM='PalletTown_PlayersHouse_2F';LAB='PalletTown_ProfessorOaksLab'
def flag(n):return bool(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+(n>>3),1)[0]&(1<<(n&7)))
def report(test,**kw):rows.append(dict(test=test,passed=True,**kw));print(test,kw,flush=True)
def shot(n):r.frame.save(D/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(D/(n+'-x3.png'))
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def free():return field() and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2'
def pulse(f):r.keys={8} if f%20<4 else set();r.run()
def finish(limit=7000):
 for f in range(limit):
  pulse(f)
  if f>60 and free():r.keys=set();r.run(30);return
 raise AssertionError('Dialogue did not release control')
def obj():return r.call('GetObjectEventIdByLocalIdAndMap',1,MAPS[ROOM][1],MAPS[ROOM][0])
def stationary():
 i=obj();assert i<16;s=r.symbols['gObjectEvents']+36*i
 assert r.read(s+5,1)==bytes([181]);assert struct.unpack('<hh',r.read(s+16,4))==(13,9);assert r.read(s+24,1)[0]&15==1
 return r.read(s+4,1)[0]
def interact():
 r.keys=set();r.run(30);r.keys={4};r.run(8);r.keys=set();r.run(16)
 for _ in range(8):
  r.keys={8};r.run(2);r.keys=set();r.run(8)
  if not free():return
 raise AssertionError('Actual A interaction did not start script')
def active_task(name):
 return next((i for i in range(16) if r.u32(r.symbols['gTasks']+40*i)==r.symbols[name]|1 and r.read(r.symbols['gTasks']+40*i+4,1)==b'\1'),None)
def choice(yes):
 for f in range(5000):
  pulse(f)
  if active_task('Task_YesNoMenu_HandleInput') is not None:break
 else:raise AssertionError('Yes/No menu not reached')
 r.keys=set();r.run(20)
 if not yes:r.keys={5};r.run(1);r.keys=set();r.run(8)
 r.keys={8};r.run(1);r.keys=set();r.run(12)
def movie(frames,name):
 assert frames;frames[0].save(D/(name+'.gif'),save_all=True,append_images=frames[1:],duration=200,loop=0)
def restore(state):
 r.restore(state)
 for name in ['qa_move_callbacks','qa_next_keys','qa_fallbacks']:
  if hasattr(r,name):delattr(r,name)
def save_continue():
 assert r.call('TrySavingData',0,max_frames=1200)==1;assert r.call('LoadGameSave',0,max_frames=1200)==1;r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);finish()
def battle_case(name,win):
 frames=[];intro=[];seen=[];started=False;portrait=False;party_checked=False;thank=False;reward=False
 for f in range(30000):
  r.keys=battle_keys(r,f);r.run();battle=r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
  if battle:
   started=True
   if not party_checked:
    team=[]
    for i in range(6):
     p=r.symbols['gEnemyParty']+100*i
     team.append((r.call('GetMonData',p,C['MON_DATA_SPECIES'],0),r.call('GetMonData',p,C['MON_DATA_LEVEL'],0)))
     assert r.call('GetMonData',p,C['MON_DATA_HELD_ITEM'],0)==0
     assert all(r.call('GetMonData',p,C['MON_DATA_MOVE1']+j,0) for j in range(4))
    assert team==[(40,70),(59,70),(89,70),(133,70),(40,70),(150,70)],team
    assert r.call('YokaiChampionOrderedPartySize')==6;party_checked=True
   sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
   if sid<64 and not portrait:
    sp=r.symbols['gSprites']+68*sid
    if r.read(sp+62,1)[0]&1 and int.from_bytes(r.read(sp+6,2),'little')==167 and r.read(sp+36,2)==b'\0\0':
     r.run(1);shot(name+'-portrait');portrait=True
   if r.u32(r.symbols['gBattlerControllerFuncs']) in actions:
    idx=int.from_bytes(r.read(r.symbols['gBattlerPartyIndexes']+2,2),'little')
    if idx not in seen:seen.append(idx)
   if f%12==0 and not seen:intro.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
  if started and field():
   if win and flag(0x332):
    if f%12==0:frames.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
    ti=active_task('Task_YoannThank')
    if ti is not None:
     data=r.symbols['gTasks']+40*ti+8
     if int.from_bytes(r.read(data,2),'little')==1 and int.from_bytes(r.read(data+4,2),'little')>60 and not thank:shot('thank-for-play');thank=True
    if flag(0x333) and not reward:shot('obtention-charme');reward=True
   if free():r.keys=set();r.run(30);break
 else:raise AssertionError((name,'never returned to field',seen,hex(r.u32(r.symbols['gMain']+4))))
 assert started and portrait and party_checked
 if win:
  assert seen==list(range(6)),seen;assert r.read(r.symbols['gBattleOutcome'],1)==b'\1';assert thank and reward
  assert flag(0x332) and flag(0x333) and r.call('CheckBagHasItem',52,1)
  assert r.read(r.symbols['gPlttBufferFaded'],1024)==r.read(r.symbols['gPlttBufferUnfaded'],1024)
  stationary();shot('chambre-apres-victoire');movie(frames,'discours-fondu-cadeau')
  giftframes=frames[-100:];movie(giftframes,'obtention-charme')
 else:
  assert r.read(r.symbols['gBattleOutcome'],1)==b'\2';assert not flag(0x332) and not flag(0x333)
  warp(r,*MAPS[ROOM],6,3);stationary();shot('retour-apres-defaite')
 if intro:movie(intro,name+'-introduction')
 report(name,party_verified=True,enemy_order=seen,actual_controller_result='victory' if win else 'loss',white_scene=thank,reward=reward)
try:
 actions={int(a[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(a:=line.split())==3 and a[2]=='HandleInputChooseAction'}
 base=r.snapshot();warp(r,*MAPS[ROOM],6,3);assert obj()==16;shot('absent-medallium-incomplet');report('Incomplete Medallium: NPC absent')
 for n in range(1,152):r.call('GetSetPokedexFlag',n,2)
 warp(r,*MAPS[ROOM],6,3);assert obj()==16;report('151 seen but not owned: NPC absent')
 for n in range(1,152):r.call('GetSetPokedexFlag',n,3)
 assert r.call('YoannMedalliumComplete');warp(r,*MAPS[ROOM],6,3);assert obj()==16;report('151 owned without Chen validation: NPC absent')
 # Actual talk with Chen, not direct setting of the invitation flag.
 r.call('FlagClear',C['FLAG_HIDE_OAK_IN_HIS_LAB']);r.call('VarSet',C['VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB'],9)
 warp(r,*MAPS[LAB],6,4);interact();finish();assert flag(0x331);report('Real Chen interaction sets the permanent invitation')
 warp(r,*MAPS[ROOM],6,3);stationary();r.run(240);stationary();shot('juste-yoann-chambre');report('NPC appears at top wall (6,2), remains stationary and faces south')
 save_continue();stationary();assert flag(0x331);report('Invitation and NPC appearance survive native Flash save/Continue')
 invited=r.snapshot();interact();choice(False);finish();assert not flag(0x332);stationary();shot('combat-refuse');report('Refusing battle returns control and leaves NPC present')
 # Lose with a level1 player fixture; native enemy damage and blackout run normally.
 restore(invited);r.call('CreateMon',r.symbols['gPlayerParty'],1,1,0,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0)
 interact();choice(True);battle_case('defaite-joueur',False)
 # A legal retry after the defeat, with a strong player fixture for test duration.
 strong_party(r);interact();choice(True);battle_case('victoire-joueur',True)
 assert not r.call('CheckBagHasItem',52,2)
 save_continue();assert flag(0x332) and flag(0x333) and r.call('CheckBagHasItem',52,1);stationary();report('First victory and unique charm survive Flash save/Continue')
 interact();finish();assert not active_task('Task_YoannThank');assert not r.call('CheckBagHasItem',52,2);stationary();report('Later dialogue does not replay emotional scene, rematch or duplicate gift')
 # Check a real menu after the white scene, then return to the same NPC.
 r.write(r.symbols['gBagMenuState']+6,b'\1\0');r.call('CB2_BagMenuFromStartMenu');r.run(600);shot('sac-apres-scene')
 assert r.call('GetItemIconGfxPtr',52,0)==r.symbols['gItemIcon_ShinyCharm']
 r.keys={0};r.run(1);r.keys=set();r.run(600);assert free();stationary();report('Native key-item bag remains usable after white scene, with charm icon; room control restored')
 # Girl variant: real room appearance and real NPC intro/decline.
 restore(invited);r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,b'\1');warp(r,*MAPS[ROOM],6,3);stationary();shot('juste-yoann-variante-fille');interact();choice(False);finish();stationary();report('Female player variant retains stationary NPC and refusal flow')
 passed=True
except BaseException:
 failure=traceback.format_exc();print(failure,flush=True);shot('ECHEC');raise
finally:
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=sha,results=rows,failure=failure),ensure_ascii=False,indent=2)+'\n')

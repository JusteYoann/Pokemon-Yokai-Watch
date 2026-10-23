#!/usr/bin/env python3
"""Native development-only Don -> Matt/heal -> white fusion -> eight-form boss.

Fresh fixture, controller drives both battles. Player boosted to level100/999
stats; no enemy HP/PP, outcome or script stage writes. Not a normal difficulty
playthrough. Does not approve true-form art or conclusion/Hall of Fame.
"""
import hashlib,json,os,struct,subprocess
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp,strong_party
from pilote_combat_mgba import battle_keys
Q=ROOT/os.environ.get('YOKAI_SPIRATON_SCENE_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON/scene');Q.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;rows=[];movie=[];stages=[];battles=[];white=False;heal=False;forms=[];first_choice=False;converged=False;palette_checked=False

def actors():
 out={}
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1 and b[9:11]==bytes([MAPS['PokemonLeague_ChampionsRoom'][1],MAPS['PokemonLeague_ChampionsRoom'][0]]):
   x,y=struct.unpack_from('<hh',b,16);out[b[8]]=(x-7,y-7)
 return out
try:
 strong_party(r)
 # Prevent the unchanged production Matt trigger in this isolated map fixture.
 for name in ['TRAINER_CHAMPION_FIRST_SQUIRTLE','TRAINER_CHAMPION_FIRST_BULBASAUR','TRAINER_CHAMPION_FIRST_CHARMANDER']:r.call('SetTrainerFlag',C[name])
 warp(r,*MAPS['PokemonLeague_ChampionsRoom'],6,10)
 assert not {3,4,5,6}&actors().keys(),'Diagnostic actors leaked into normal map'
 # A fainted, poisoned backup with no PP verifies whole-party healing.
 r.call('CreateMon',r.symbols['gPlayerParty']+100,7,50,20,1,101,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x02')
 for field,value in [('MON_DATA_HP',0),('MON_DATA_STATUS',8),('MON_DATA_PP1',0),('MON_DATA_PP2',0),('MON_DATA_PP3',0),('MON_DATA_PP4',0)]:
  r.w32(r.PARAMS+128,value);r.call('SetMonData',r.symbols['gPlayerParty']+100,C[field],r.PARAMS+128)
 stageptr=r.call('GetVarPointer',0x4002)
 stageoffset=stageptr-r.u32(r.symbols['gSaveBlock1Ptr'])
 r.call('ScriptContext_SetupScript',r.symbols['PokemonLeague_Spiraton_DevelopmentEntry'])
 active_battle=False;last_stage=0;seen_colors=set()
 action_callbacks={int(v[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=l.split())==3 and v[2]=='HandleInputChooseAction'}
 for f in range(70000):
  in_battle=r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
  r.keys=battle_keys(r,f) if in_battle else ({8} if f%16<4 else set());r.run()
  stage=int.from_bytes(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+stageoffset,2),'little')
  if stage!=last_stage:
   stages.append(dict(stage=stage,frame=f,actors=actors()));r.frame.save(Q/f'etape-{stage}.png');last_stage=stage
  if in_battle:
   trainer=int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')
   if trainer not in [x['trainer'] for x in battles]:
    battles.append(dict(trainer=trainer,bgm=r.call('GetBattleBGM'),frame=f));r.frame.save(Q/f'combat-{trainer}.png')
   if trainer==744:
    if not first_choice and r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:
     assert r.read(r.symbols['sFirst'],1)==b'\1'
     r.keys=set();r.run(180)
     assert r.read(r.symbols['sFirst'],1)==b'\1'
     first_choice=True;r.frame.save(Q/'boss-premier-choix-diagnostic-bouh.png')
    lvl=r.read(r.symbols['gBattleMons']+88+42,1)[0]
    if lvl==56+len(forms):forms.append(lvl)
  if stage==3 and not heal:
   for i in range(2):
    mon=r.symbols['gPlayerParty']+100*i
    get=lambda field:r.call('GetMonData',mon,C[field],0)
    hp,maxhp,status=get('MON_DATA_HP'),get('MON_DATA_MAX_HP'),get('MON_DATA_STATUS')
    assert hp==maxhp and hp>0 and status==0,(i,hp,maxhp,status)
    for j in range(4):
     move=get('MON_DATA_MOVE1') if j==0 else r.call('GetMonData',mon,C['MON_DATA_MOVE1']+j,0)
     pp=r.call('GetMonData',mon,C['MON_DATA_PP1']+j,0)
     assert pp==r.call('CalculatePPWithBonus',move,get('MON_DATA_PP_BONUSES'),j),(i,j,pp)
   heal=True;rows.append(dict(test='Native Matt heal restores HP, PP and status of all members including fainted backup',passed=True));r.frame.save(Q/'matt-soin-complet.png')
  if stage==3 and not palette_checked:
   ids={}
   for i in range(16):
    b=r.read(r.symbols['gObjectEvents']+36*i,36)
    if b[0]&1:ids[b[8]]=b[4]
   for lid,bank,symbol in [(1,6,'gObjectEventPal_Matt'),(3,10,'gObjectEventPal_YokaiDonMorleoneGroup')]:
    actual=int.from_bytes(r.read(r.symbols['gSprites']+ids[lid]*68+4,2),'little')>>12
    assert actual==bank,(lid,actual,bank)
    assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols[symbol],32)
   palette_checked=True
  if stage==4 and not converged:
   a=actors()
   if all(a.get(k)==v for k,v in {4:(5,8),5:(7,8),6:(6,7)}.items()):
    converged=True;r.frame.save(Q/'sbires-rassembles.png')
  if stage==5 and not white:
   a=actors();assert not {3,4,5,6}&a.keys(),a
   pixels=list(r.frame.convert('RGB').getdata());white=sum(min(p)>245 for p in pixels)/len(pixels)>.99
   if white:r.frame.save(Q/'flash-blanc-disparition.png')
  if f%16==0 and stage>=2:movie.append(r.frame.copy())
  if stage==6:
   r.keys=set();r.run(180);r.frame.save(Q/'retour-scene-apres-victoire.png')
   assert r.call('FlagGet',C['FLAG_SYS_GAME_CLEAR'])==0,'Development sequence must not alter Hall of Fame progression'
   assert heal and white and converged and palette_checked and forms==list(range(56,64)),(heal,white,forms)
   assert [(x['trainer'],x['bgm']) for x in battles]==[(743,349),(744,C['MUS_YOKAI_ZAZELMARE'])],battles
   if os.environ.get('YOKAI_SPIRATON_TEST_HOF'):
    from spiraton_hof_qa import check_hof
    rows.append(check_hof(r,Q))
   passed=True;break
 else:
  r.frame.save(Q/'diagnostic.png');raise AssertionError(dict(stages=stages,battles=battles,actors=actors(),forms=forms,cb=hex(r.u32(r.symbols['gMain']+4)),scriptptr=hex(r.u32(r.symbols['sGlobalScriptContext']+8))))
 if movie:movie[0].save(Q/'SCENE_DEVELOPPEMENT.gif',save_all=True,append_images=movie[1::3],duration=800,loop=0)
finally:
 (Q/'SCENE_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),stages=stages,battles=battles,whole_party_heal=heal,fullscreen_white_masks_removal=white,guards_reached_positions=converged,matt_don_palettes_independent=palette_checked,levels=forms,production_entry_enabled=False,first_transform_waits_for_player_choice=first_choice,approved_true_form_artwork=False,hall_of_fame_from_new_finale_tested=False,results=rows),indent=2)+'\n');r.close()
print('PASS: native development scene, two battles, full heal, convergence/white removal and eight phases')

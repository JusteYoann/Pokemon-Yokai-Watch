#!/usr/bin/env python3
"""Isolated eight-form battle prototype. Approved true-form artwork and native first Morphing.

Starts diagnostic trainer 744 explicitly, with a boosted QA player. No production
map arms this encounter. Controller selects moves; no enemy HP/PP writes.
"""
import hashlib,json,struct,os,subprocess
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C
from pilote_combat_mgba import battle_keys
Q=ROOT/os.environ.get('YOKAI_SPIRATON_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON');Q.mkdir(parents=True,exist_ok=True);r=new_game();passed=False;rows=[];captures=[];palette_checks={};normal_palette_checks={};white_effect_seen=set();source_palettes={};appearance_seen=False;first_menu_checked=False;first_morph_frames=[];sound_events=[];previous_se={}
try:
 # Level65 makes the intermediate-EXP assertion meaningful (level100 cannot gain).
 r.call('CreateMon',r.symbols['gPlayerParty'],1,65,31,1,100,0,0)
 r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_SPATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(r.PARAMS+128,999);r.call('SetMonData',r.symbols['gPlayerParty'],C[field],r.PARAMS+128)
 for slot,move in enumerate(['MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_SWIFT','MOVE_MAGICAL_LEAF']):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C[move],slot)
 if os.environ.get('YOKAI_SPIRATON_MULTIHIT'):
  r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_BULLET_SEED'],0)
 exp=r.call('GetMonData',r.symbols['gPlayerParty'],C['MON_DATA_EXP'],0)
 r.call('SpiratonBattleArmPrototype');r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',744));r.call('StartTrainerBattle')
 action_callbacks={int(v[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=l.split())==3 and v[2]=='HandleInputChooseAction'}
 appearance=r.read(r.symbols['sText_SpiratonAppears'],70).split(b'\xff')[0]
 layer_colors=[10|(25<<5)|(6<<10),31|(17<<5)|(2<<10),3|(26<<5)|(28<<10),5|(12<<5)|(31<<10),18|(8<<5)|(29<<10),29|(6<<5)|(22<<10),31|(7<<5)|(7<<10),31|(30<<5)|(23<<10)]
 last_phase=-1;started=False;pending_saw=False;injected=False;cure_seen=False
 status_name=os.environ.get('YOKAI_SPIRATON_STATUS','')
 statuses={'burn':(16,'sCureBurn'),'poison':(8,'sCurePoison'),'paralysis':(64,'sCureParalysis'),'sleep':(3,'sCureSleep'),'freeze':(32,'sCureFreeze')}
 for f in range(40000):
  r.keys=battle_keys(r,f);r.run()
  cb=r.u32(r.symbols['gMain']+4)
  for player in ['gMPlayInfo_SE1','gMPlayInfo_SE2','gMPlayInfo_SE3']:
   header,status,clock=r.u32(r.symbols[player]),r.u32(r.symbols[player]+4),r.u32(r.symbols[player]+12)
   old=previous_se.get(player,(0,0,0))
   if status&65535 and (header!=old[0] or not old[1]&65535 or clock<old[2]):
    for name in ['se_m_teleport','se_m_minimize']:
     if header==r.symbols[name]:sound_events.append(dict(frame=f,player=player,sound=name,clock=clock))
   previous_se[player]=(header,status,clock)
  if first_menu_checked and len(first_morph_frames)<330 and r.read(r.symbols['sFirst'],1)==b'\0':first_morph_frames.append(r.frame.copy())
  if cb==r.symbols['BattleMainCB2']|1:
   started=True
   assert r.u32(r.symbols['gBattleTypeFlags'])&8,'Boss must retain capture/run prohibition'
   if not first_menu_checked and r.u32(r.symbols['gBattlerControllerFuncs']) in action_callbacks:
    assert r.read(r.symbols['sFirst'],1)==b'\x01','First transform happened during entry'
    r.keys=set();r.run(180)
    assert r.read(r.symbols['sFirst'],1)==b'\x01','First transform happened before player choice'
    assert r.call('SpiratonArtIsActive'), 'Native true-form representation missing'
    sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
    assert (int.from_bytes(r.read(r.symbols['gSprites']+68*sid+4,2),'little')&1023)==r.call('GetSpriteTileStartByTag',0x7D54), 'Battler no longer uses true-form tiles'
    assert r.read(r.symbols['gPlttBufferUnfaded']+544,32)==r.read(r.symbols['sSpiratonPreviewPalette'],32), 'True-form palette overwritten'
    first_menu_checked=True;r.frame.save(Q/'premier-choix-avant-morphing.png')
   if r.read(r.symbols['gDisplayedStringBattle'],len(appearance))==appearance:appearance_seen=True
   # Native struct BattlePokemon has a documented 88-byte ABI.
   mon=r.read(r.symbols['gBattleMons']+88,88);species=int.from_bytes(mon[:2],'little');hp=int.from_bytes(mon[40:42],'little');level=mon[42]
   if f%8==0 and species and 56<=level<=63:
    phase=level-56
    # Compare both hardware palette buffers with the real decompressed species palette.
    if species not in source_palettes:
     pointer=r.call('GetMonSpritePalFromSpeciesAndPersonality',species,0x1234,0)
     r.call('LZDecompressWram',pointer,r.PARAMS+128)
     source_palettes[species]=r.read(r.PARAMS+128,32)
    source=source_palettes[species]
    faded=r.read(r.symbols['gPlttBufferFaded']+544,32)
    unfaded=r.read(r.symbols['gPlttBufferUnfaded']+544,32)
    white=struct.pack('<16H',*[(lambda c: sum((((c>>shift)&31)+((31-((c>>shift)&31))*6>>4))<<shift for shift in (0,5,10)))(c) for c in struct.unpack('<16H',source)])
    if r.u32(r.symbols['gBattleMainFunc'])==(r.symbols['TransformStep']|1) and faded==white:
     white_effect_seen.add(phase)
    if r.u32(r.symbols['gBattleMainFunc'])==(r.symbols['TransformStep']|1) and r.read(r.symbols['sStep'],1)==b'\3':
     assert faded==source and unfaded==source,('Normal species palette not restored',phase,species)
     normal_palette_checks[phase]=True
     assert not r.call('SpiratonArtIsActive')
     assert r.call('GetSpriteTileStartByTag',0x7D54)==65535
    if phase not in palette_checks and hp>0 and r.u32(r.symbols['gBattleMainFunc']) != (r.symbols['TransformStep']|1):
     tags=struct.unpack('<16H',r.read(r.symbols['sSpritePaletteTags'],32))
     if 0x7D53 in tags:
      bank=tags.index(0x7D53);color=int.from_bytes(r.read(r.symbols['gPlttBufferUnfaded']+512+bank*32+20,2),'little')
      if color==layer_colors[phase]:
       palette_checks[phase]=bank;r.frame.save(Q/f'phase-{phase+1:02d}.png')
    if status_name and not injected and phase==0 and hp>0 and r.call('SpiratonBattleInspect',0)==52:
     value,label=statuses[status_name];r.w32(r.symbols['gBattleMons']+88+76,value)
     r.w32(r.PARAMS+160,value);r.call('SetMonData',r.symbols['gEnemyParty'],C['MON_DATA_STATUS'],r.PARAMS+160);injected=True
    if status_name and phase>0:assert int.from_bytes(mon[76:80],'little')==0
    if phase>last_phase and hp>0:
     if phase>0:
      assert pending_saw,'A new form appeared without an exhausted phase';assert r.call('GetMonData',r.symbols['gPlayerParty'],C['MON_DATA_EXP'],0)==exp
     last_phase=phase;pending_saw=False;rows.append(dict(phase=phase+1,species=species,level=level,first_frame=f))
    if hp==0 and phase<7:pending_saw=True
   if status_name and injected and not cure_seen:
    value,label=statuses[status_name];expected=r.read(r.symbols[label],90).split(b'\xff')[0]
    if r.read(r.symbols['gDisplayedStringBattle'],len(expected))==expected:
     cure_seen=True;r.keys=set();r.run(100);r.frame.save(Q/'statut-retire.png')
   if f%32==0:captures.append(r.frame.copy())
   if f%256==0:
    r.frame.save(Q/'prototype-combat-en-cours.png')
   if len(rows)==8 and r.read(r.symbols['gBattleOutcome'],1)[0]==1:
    passed=True;r.frame.save(Q/'prototype-huitieme-vaincue.png');break
  elif started:
   if len(rows)==8 and r.read(r.symbols['gBattleOutcome'],1)[0]==1:passed=True;break
 if not passed:
  r.frame.save(Q/'prototype-diagnostic.png')
  raise AssertionError(dict(started=started,phases=rows,callback=hex(cb),battle_main=hex(r.u32(r.symbols['gBattleMainFunc'])),outcome=list(r.read(r.symbols['gBattleOutcome'],1))))
 assert len({x['species'] for x in rows})==8
 assert appearance_seen,'Custom appearance message never rendered'
 assert first_menu_checked,'Initial choice never observed'
 assert len(palette_checks)==8,dict(missing_phase_colors=palette_checks)
 assert len(normal_palette_checks)==8,dict(missing_normal_palettes=normal_palette_checks)
 assert len(white_effect_seen)==8,dict(missing_native_white_effect=sorted(white_effect_seen))
 if status_name:assert injected and cure_seen,'Expected native status-removal message'
 assert len(sound_events)==16, ('Expected exactly two native sound events per Morphing',sound_events)
 assert sum(x['sound']=='se_m_teleport' for x in sound_events)==8
 assert sum(x['sound']=='se_m_minimize' for x in sound_events)==8
 if first_morph_frames:first_morph_frames[0].save(Q/'PREMIER_MORPHING.gif',save_all=True,append_images=first_morph_frames[1:],duration=34,loop=0)
 if captures:captures[0].save(Q/'PROTOTYPE_COMBAT.gif',save_all=True,append_images=captures[1:],duration=533,loop=0)
finally:
 r.close();(Q/'COMBAT_PROTOTYPE_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),forms=rows,production_scene=False,approved_true_form_artwork=True,native_transform_sound_events=sound_events,human_listening_performed=False,qa_player_initial_level=65,intermediate_exp_checked_below_level_cap=True,approved_hp_colors=True,layer_palette_checks=palette_checks,normal_species_palette_restored_checks=normal_palette_checks,native_white_transition_seen_phases=sorted(white_effect_seen),appearance_message_seen=appearance_seen,first_transform_waits_for_player_choice=first_menu_checked,trainer_capture_run_protection_retained=True,status_fixture=status_name,status_removal_message_seen=cure_seen if status_name else None),indent=2)+'\n')
print('PASS isolated native eight-form battle; production/artistic validation remains pending')

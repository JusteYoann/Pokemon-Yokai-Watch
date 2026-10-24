#!/usr/bin/env python3
"""Real native save/Continue and menu B return. Options-return callback fixture.

FRLG does not expose Options in its save-selection menu. The existing Options
screen is opened by a native-call fixture, with return callback set to that menu.
No extra Options entry or release debug shortcut is introduced.
"""
import hashlib
import json
import os
from mgba_rpc import ROOT
from mgba_new_game import new_game

mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
out=ROOT/'docs/ecran-titre-credits-20261024'/mode/'retours-menu'
out.mkdir(parents=True,exist_ok=True)
results=[]
for gender in [0,1]:
    r=new_game(gender)
    def inactive():
        status=r.u32(r.symbols['gMPlayInfo_BGM']+4)
        return status==0 or bool(status&0x80000000)
    def pulse(key,after=180):
        r.keys=set();r.run(4);r.keys={key};r.run();r.keys=set();r.run(after)
    try:
        player=r.read(r.u32(r.symbols['gSaveBlock2Ptr']),9)
        pair=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)
        r.call('SaveMapView')
        assert r.call('TrySavingData',0,max_frames=1500)==1
        r.call('SetMainCallback1',0)
        r.call('SetMainCallback2',r.symbols['CB2_InitYokaiTitle']|1)
        r.run(360)
        assert not inactive()
        pulse(3)
        assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_MainMenu']|1
        assert inactive()
        r.frame.save(out/f'{gender}-menu-sauvegarde.png')
        pulse(0)  # B returns to title; then START returns to silent menu.
        assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_RunYokaiPresentation']|1
        assert not inactive()
        pulse(3)
        assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_MainMenu']|1
        assert inactive()
        r.w32(r.symbols['gMain']+8,r.symbols['CB2_InitMainMenu']|1)
        r.call('CB2_OptionsMenuFromStartMenu')
        r.run(300)
        assert inactive()
        r.frame.save(out/f'{gender}-options.png')
        pulse(0)
        assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_MainMenu']|1
        assert inactive()
        r.frame.save(out/f'{gender}-retour-options.png')
        pulse(8,30)
        for f in range(9000):
            r.keys={0} if f%32<2 else set();r.run()
            if f>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:
                break
        else:raise AssertionError('Continue did not load the actual field')
        r.keys=set();r.run(180)
        assert r.read(r.u32(r.symbols['gSaveBlock2Ptr']),9)==player
        assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)==pair
        assert not inactive()
        r.frame.save(out/f'{gender}-continue.png')
        results.append(dict(gender=gender,passed=True,native_save_continue=True,player_name_gender_map_preserved=True,menu_B_title_START_return=True,options_return_fixture=True,field_music_resumed=True))
    finally:r.close()
(out/'TEST_RETOURS.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=results),indent=2)+'\n')
print('PASS native save/Continue, B/title/START, Options-return fixture',mode)

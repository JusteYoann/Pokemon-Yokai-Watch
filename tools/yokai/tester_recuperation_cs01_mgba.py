#!/usr/bin/env python3
"""Recover a missing legacy HM01 through native harbour interactions.

Engineered legacy flags/inventory, not a supplied player save or full adventure.
No new HM before the captain's existing receipt flag; no new progression flags.
"""
import hashlib
import json
import os
import re
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT, Emulator
from scenario_qa_helpers import warp, face_a, finish, walk, pos, location, idle
from tester_oceane_progression_mgba import save_continue, fill_key_pocket

OUT=ROOT/'QA_RECETTE_FINALE/OCEANE_RECUPERATION_CS01'
HM,CASE,GOT,SCENE,SEVII=339,364,0x237,0x407e,0x4076


def setup(r, earned=True, sevii=0):
    r.call('CreateMon',r.symbols['gPlayerParty'],5,20,15,1,100,0,0)
    r.write(r.symbols['gPlayerPartyCount'],b'\x01')
    if earned:r.call('FlagSet',GOT)
    r.call('FlagSet',0x87)
    r.call('VarSet',SCENE,3)
    r.call('VarSet',SEVII,sevii)
    warp(r,3,5,24,32)


def speak(r):
    face_a(r,'D');finish(r)


def inventory(r):
    return bool(r.call('CheckBagHasItem',HM,1)),bool(r.call('CheckBagHasItem',HM,2))


def widths():
    glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
    glyph["'"]=glyph['’'];rows=[];r=Emulator()
    try:
        source=(ROOT/'data/maps/VermilionCity/text.inc').read_text()
        for label,body in re.findall(r'^(\w+)::[^\n]*\n((?:[ \t]+\.string .*\n)+)',source,re.M):
            if label not in ['VermilionCity_Text_RecoveredCut','VermilionCity_Text_CutRecoveryNoRoom']:continue
            for text in re.findall(r'\.string "(.*)"',body):
                for line in re.split(r'\\[nlp]',text.rstrip('$').replace('{PLAYER}','WWWWWWW')):
                    r.write(r.PARAMS+128,bytes(glyph[c] for c in line)+b'\xff')
                    w=r.call('GetStringWidth',2,r.PARAMS+128,0)
                    rows.append(dict(label=label,text=line,width=w,passed=w<=208))
    finally:r.close()
    assert all(x['passed'] for x in rows),rows
    return rows


def main():
    OUT.mkdir(exist_ok=True);rows=[];texts=widths()
    for gender in [0,1]:
        for sevii in [0,1,5]:
            r=new_game(gender)
            try:
                setup(r,sevii=sevii)
                before=[r.call('VarGet',v) for v in [SCENE,SEVII,0x4053]]
                # Persist the already-invalid old save before repairing it.
                save_continue(r)
                speak(r)
                assert inventory(r)==(True,False) and r.call('CheckBagHasItem',CASE,1)
                assert before==[r.call('VarGet',v) for v in [SCENE,SEVII,0x4053]]
                assert r.call('FlagGet',GOT) and not r.call('FlagGet',0x821)
                save_continue(r)
                assert inventory(r)==(True,False)
                r.frame.save(OUT/f'recupere-{gender}-sevii-{sevii}.png')
                if sevii:
                    face_a(r,'D')
                    callback=r.symbols['Task_MultichoiceMenu_HandleInput']|1
                    for frame in range(1200):
                        r.keys={8} if frame%16<4 else set();r.run()
                        if any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01'
                               and r.u32(r.symbols['gTasks']+40*i)==callback for i in range(16)):break
                    else:raise AssertionError(('Native ferry destinations not displayed',gender,sevii))
                    r.keys=set();r.run(30);r.frame.save(OUT/f'ferry-{gender}-sevii-{sevii}.png')
                    for frame in range(600):
                        r.keys={0} if frame%16<4 else set();r.run()
                        if frame>60 and idle(r):break
                    assert idle(r) and inventory(r)==(True,False)
                    assert before==[r.call('VarGet',v) for v in [SCENE,SEVII,0x4053]]
                else:
                    speak(r);assert inventory(r)==(True,False)
                rows.append(dict(gender=gender,sevii=sevii,test='Legacy missing HM, actual sailor interaction, receipt and Flash reload',passed=True))
            finally:r.close()

        r=new_game(gender)
        try:
            setup(r);added=fill_key_pocket(r);save_continue(r);speak(r)
            assert inventory(r)==(False,False) and r.call('VarGet',SCENE)==3
            r.frame.save(OUT/f'sac-plein-{gender}.png')
            assert r.call('RemoveBagItem',added[0],1)
            speak(r);assert inventory(r)==(True,False)
            speak(r);assert inventory(r)==(True,False)
            save_continue(r);assert inventory(r)==(True,False)
            rows.append(dict(gender=gender,test='Full key pocket rejection, free slot retry, repeated interaction and Flash Continue',passed=True))
        finally:r.close()

        r=new_game(gender)
        try:
            setup(r,earned=False);speak(r)
            assert inventory(r)==(False,False) and not r.call('FlagGet',GOT)
            assert r.call('VarGet',SCENE)==3
            rows.append(dict(gender=gender,test='No reward when original captain receipt flag is absent',passed=True))
        finally:r.close()

        for x in [22,23]:
            r=new_game(gender)
            try:
                setup(r);warp(r,3,5,x,32);walk(r,'D');finish(r)
                assert inventory(r)==(True,False) and pos(r)==(x,32)
                assert location(r)==(3,5) and r.call('VarGet',SCENE)==3
                r.frame.save(OUT/f'passage-{gender}-{x}.png')
                # Original no-ferry boarding rejection still moves the player
                # back up the pier, with no extra copy of the now-owned HM.
                walk(r,'D');finish(r)
                assert inventory(r)==(True,False) and pos(r)==(x,32)
                rows.append(dict(gender=gender,gate_x=x,test='Both boarding triggers repair old reward, native return up pier and no duplicate on repeat',passed=True))
            finally:r.close()

    rom=Path(os.environ['YOKAI_QA_ROM'])
    report=dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),rom_size=rom.stat().st_size,tests=rows,text_widths=texts)
    (OUT/'TEST_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS',len(rows),flush=True)


if __name__=='__main__':main()

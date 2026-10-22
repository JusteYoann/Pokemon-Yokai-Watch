#!/usr/bin/env python3
"""Targeted native SS Anne events with explicit map, party and inventory fixtures.

Not a complete journey. Rival victories use level-40 generated stats and a move
fixture to test branches, not difficulty. No battle outcomes are written.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT, Emulator
import scenario_qa_helpers as h
from scenario_qa_helpers import warp, face_a, finish, idle, pos, location, walk, C

OUT = ROOT/'QA_RECETTE_FINALE/OCEANE_2026_10_22'
HM, CASE, GOT, DEPARTURE = 339, 364, 0x237, 0x407e


def save_continue(r):
    # The actual Start menu prepares mapView before TrySavingData. Omitting
    # this step restores stale terrain even when flags/coordinates are correct.
    def tiles():
        x,y=pos(r);width=r.u32(r.symbols['VMap']);base=r.u32(r.symbols['VMap']+8)
        return b''.join(r.read(base+2*((y+7+dy)*width+x+7-2),10) for dy in range(-2,3))
    before=tiles()
    r.call('SaveMapView')
    assert r.call('TrySavingData', 0, max_frames=1200) == 1
    assert r.call('LoadGameSave', 0, max_frames=1200) == 1
    r.call('SetMainCallback2', r.symbols['CB2_ContinueSavedGame'] | 1)
    r.keys = set()
    r.run(900)
    assert idle(r)
    assert tiles()==before, 'Continue changed the local terrain'


def party(r, level=20):
    r.call('CreateMon', r.symbols['gPlayerParty'], 5, level, 15, 1, 100, 0, 0)
    r.write(r.symbols['gPlayerPartyCount'], b'\x01')
    r.call('SetLastHealLocationWarp', 5)


def fill_key_pocket(r):
    pocket = r.call('ItemId_GetPocket', 360)
    added = []
    for item in range(1, 375):
        if item != CASE and r.call('ItemId_GetPocket', item) == pocket:
            if r.call('AddBagItem', item, 1):
                added.append(item)
    assert not r.call('CheckBagHasItem', CASE, 1)
    assert r.call('BagPocketGetFirstEmptySlot', pocket-1) & 255 == 255
    return added


def captain(r):
    warp(r, 1, 11, 5, 5)
    face_a(r, 'U')
    finish(r)


def evidence(r):
    return dict(flag_got_hm01=bool(r.call('FlagGet', GOT)),
                actual_hm01=bool(r.call('CheckBagHasItem', HM, 1)),
                departure_scene=r.call('VarGet', DEPARTURE))


def reproduce_before():
    r = new_game()
    try:
        party(r)
        added = fill_key_pocket(r)
        captain(r)
        report = dict(rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),
                      fixture='Native AddBagItem fills key items pocket without TM Case; interact with captain through controller',
                      filled_item_ids=added, **evidence(r))
        assert report['flag_got_hm01'] and not report['actual_hm01'] and report['departure_scene']==1
        r.frame.save(OUT/'sac-plein-avant-correction.png')
        (OUT/'DEFAUT_AVANT.json').write_text(json.dumps(report, indent=2)+'\n')
    finally:
        r.close()


def captain_cases():
    rows=[]
    for gender, name in [(0,'nathan'),(1,'katie')]:
        for mode in ['normal','objets-rares-pleins','pile-cs-pleine']:
            r=new_game(gender)
            try:
                party(r)
                if mode=='objets-rares-pleins':
                    added=fill_key_pocket(r)
                elif mode=='pile-cs-pleine':
                    assert r.call('AddBagItem',HM,999)
                captain(r)
                if mode!='normal':
                    assert not r.call('FlagGet',GOT) and r.call('VarGet',DEPARTURE)==0
                    assert r.call('CheckBagHasItem',HM,1)==(mode=='pile-cs-pleine')
                    save_continue(r)
                    warp(r,1,4,32,7)
                    assert r.call('VarGet',DEPARTURE)==0 and not r.call('FlagGet',0x87)
                    r.frame.save(OUT/(name+'-'+mode+'-depart-bloque.png'))
                    if mode=='objets-rares-pleins':
                        assert r.call('RemoveBagItem',added[0],1)
                    else:
                        assert r.call('RemoveBagItem',HM,999)
                    captain(r)
                assert r.call('FlagGet',GOT) and r.call('CheckBagHasItem',HM,1)
                assert not r.call('CheckBagHasItem',HM,2)
                assert r.call('CheckBagHasItem',CASE,1)
                assert r.call('VarGet',DEPARTURE)==1
                save_continue(r)
                captain(r)
                assert not r.call('CheckBagHasItem',HM,2)
                r.frame.save(OUT/(name+'-'+mode+'-cs-obtenue.png'))
                warp(r,1,4,32,7)
                finish(r)
                r.run(240)
                assert location(r)==(3,5) and r.call('VarGet',DEPARTURE)==3, (location(r), pos(r), r.call('VarGet',DEPARTURE), idle(r))
                assert r.call('CheckBagHasItem',HM,1) and r.call('FlagGet',GOT)
                save_continue(r)
                r.run(240)
                assert location(r)==(3,5) and r.call('VarGet',DEPARTURE)==3, (location(r), pos(r), r.call('VarGet',DEPARTURE), idle(r))
                r.frame.save(OUT/(name+'-'+mode+'-retour-carmin.png'))
                rows.append(dict(gender=name,fixture=mode,passed=True,actual_departure_cutscene=True,
                                 unique_reward=True,flash_continue=True))
            finally:
                r.close()
    return rows


def rival_cases():
    rows=[]
    h.OUT=OUT
    for gender in [0,1]:
        for choice in range(3):
            r=new_game(gender)
            try:
                party(r,40)
                r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_FLAMETHROWER'],0)
                r.call('VarSet',0x4031,choice)
                warp(r,1,6,30+choice,7)
                walk(r,'U')
                expected=[(10,20),(1,19),(96,18),([87,5,29][choice],21)]
                frames=h.fight(r,f'matt-{gender}-{choice}',expected=expected)
                assert r.call('VarGet',0x405b)==1
                assert not r.call('FlagGet',GOT) and r.call('VarGet',DEPARTURE)==0
                save_continue(r)
                assert r.call('VarGet',0x405b)==1
                rows.append(dict(gender=gender,starter_choice=choice,passed=True,
                                 actual_rival_victory=True,party=expected,frames=frames))
            finally:
                r.close()
    return rows



def cut_cases():
    rows=[]
    for gender in [0,1]:
        r=new_game(gender)
        try:
            party(r)
            r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_CUT'],0)
            assert r.call('AddBagItem',HM,1)
            warp(r,3,5,19,25)
            face_a(r,'U');finish(r)
            assert not r.call('FlagGet',0x12)
            r.call('FlagSet',0x821)
            face_a(r,'U');finish(r)
            assert r.call('FlagGet',0x12)
            walk(r,'U')
            assert pos(r)==(19,24)
            r.frame.save(OUT/f'coupe-{gender}-arbre-retire.png')
            rows.append(dict(gender=gender,passed=True,cut_requires_second_trophy=True,
                             real_cut_field_animation=True,tree_tile_walkable=True))
        finally:
            r.close()
    return rows


def text_widths():
    glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
    glyph["'"]=glyph['’']
    rows=[]
    r=Emulator()
    try:
        paths=[ROOT/f'data/maps/{name}/text.inc' for name in ['SSAnne_CaptainsOffice','SSAnne_2F_Corridor']]
        paths.append(ROOT/'data/scripts/field_moves.inc')
        for path in paths:
            for label,body in re.findall(r'^(\w+)::[^\n]*\n((?:[ \t]+\.string .*\n)+)',path.read_text(),re.M):
                if path.name=='field_moves.inc' and label not in ['Text_CutTreeDown','Text_MonUsedMove','Text_TreeCanBeCutDown']:continue
                for text in re.findall(r'\.string "(.*)"',body):
                    text=text.replace('{PLAYER}','WWWWWWW').replace('{RIVAL}','Matt').replace('{STR_VAR_1}','W'*10).replace('{STR_VAR_2}','W'*12)
                    for line in re.split(r'\\[nlp]',text.rstrip('$')):
                        if not line:continue
                        r.write(r.PARAMS+128,bytes(glyph[c] for c in line)+b'\xff')
                        width=r.call('GetStringWidth',2,r.PARAMS+128,0)
                        rows.append(dict(label=label,line=line,pixels=width,passed=width<=208))
    finally:
        r.close()
    (OUT/'TEXTES_MGBA.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    assert all(row['passed'] for row in rows),[x for x in rows if not x['passed']]
    return len(rows)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--reproduce-before',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.reproduce_before:
        reproduce_before()
        return
    widths=text_widths()
    rows=captain_cases()+rival_cases()+cut_cases()
    rom=Path(os.environ['YOKAI_QA_ROM'])
    report=dict(passed=True,scope=__doc__,rom_size=rom.stat().st_size,
                rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),
                native_text_lines=widths,tests=rows)
    (OUT/'TEST_PROGRESSION_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS',len(rows),flush=True)


if __name__=='__main__':
    main()

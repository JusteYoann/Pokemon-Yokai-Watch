#!/usr/bin/env python3
"""Native reversible Mystery Doors prototype: new-game then explicit progression/map fixtures.

No complete campaign, combat, Yopple siege or betrayal is claimed by this test.
"""
import hashlib,json,os,re,struct
from pathlib import Path
from PIL import Image,ImageDraw
from mgba_new_game import new_game
from mgba_rpc import ROOT,Emulator
from scenario_qa_helpers import warp,walk,face_a,finish as finish_native,idle,pos,location
from tester_oceane_progression_mgba import save_continue
OUT=Path(os.environ.get('YOKAI_MYSTERY_QA_DIR',ROOT/'QA_RECETTE_FINALE/PORTES_MYSTERES_PROTOTYPE'))
NAMES=['YokaiMystery_Lab','YokaiMystery_Stability','YokaiMystery_Orientation','YokaiMystery_Return']
GROUPS=json.loads((ROOT/'data/maps/map_groups.json').read_text())
MAPS={name:next((i,j) for i,k in enumerate(GROUPS['group_order']) for j,n in enumerate(GROUPS[k]) if n==name) for name in NAMES}
FLAGS=[0x32F,0x330,0x331]

def finish(r):
    if idle(r):
        r.keys=set();r.run(20);return
    return finish_native(r)

def waitmenu(r,name):
    target=r.symbols[name]|1
    for frame in range(2000):
        if any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01' and r.u32(r.symbols['gTasks']+40*i)==target for i in range(16)):
            r.keys=set();r.run(20);return
        r.keys={8} if frame%16<4 else set();r.run()
    raise AssertionError(('Menu absent',name,location(r),pos(r)))

def tap(r,key):
    r.keys=set();r.run(3);r.keys={key};r.run();r.keys=set();r.run(16)

def choose(r,index):
    waitmenu(r,'Task_MultichoiceMenu_HandleInput')
    for _ in range(index):tap(r,5)
    assert r.call('Menu_GetCursorPos')==index
    tap(r,8);finish(r)

def computer(r,index=None):
    # From the arrival point (6,7), actual floor movement to the console.
    walk(r,'L',2);walk(r,'U');face_a(r,'U')
    if index is None:finish(r)
    else:choose(r,index)

def leave(r,x=6):
    # Console interaction ends at (4,6). Arrival point is (6,7).
    if pos(r)==(4,6):walk(r,'R',2);walk(r,'D')
    assert pos(r)==(6,7),pos(r)
    if x>6:walk(r,'R',x-6)
    walk(r,'D');finish(r)

def lab_doctor(r):
    assert pos(r)==(6,7)
    walk(r,'R');walk(r,'U');face_a(r,'U');finish(r)
    walk(r,'D');walk(r,'L')

def enter(r,yes=True):
    assert location(r)==(3,5) and pos(r)==(28,10)
    face_a(r,'U');waitmenu(r,'Task_YesNoMenu_HandleInput')
    tap(r,8 if yes else 0);finish(r)

def native_text_widths():
    glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
    rows=[];r=Emulator()
    try:
        source=(ROOT/'data/scripts/yokai_mystery.inc').read_text()
        for label,body in re.findall(r'^(\w+)::[^\n]*\n((?:[ \t]+\.string .*\n)+)',source,re.M):
            text=''.join(re.findall(r'\.string "(.*)"',body))
            for line in re.split(r'\\[nlp]',text.rstrip('$')):
                if not line:continue
                r.write(r.PARAMS+128,bytes(glyph[c] for c in line)+b'\xff');w=r.call('GetStringWidth',2,r.PARAMS+128,0)
                rows.append(dict(label=label,line=line,pixels=w,passed=w<=208))
    finally:r.close()
    (OUT/'TEXTES_MGBA.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    assert all(x['passed'] for x in rows),[x for x in rows if not x['passed']]
    return len(rows)


def graphics_validation():
    nathan=Image.open(ROOT/'graphics/yokai_characters/nathan/normal.png')
    jobard=Image.open(ROOT/'graphics/yokai_characters/dr_jobard/overworld.png')
    assert jobard.mode=='P' and jobard.size==(64,32)
    assert len(set(jobard.getdata()))<=16 and jobard.info.get('transparency')==0
    result=[];preview=Image.new('RGB',(640,560),(200,200,200));draw=ImageDraw.Draw(preview)
    for i in range(4):
        j=min(i,2);a=nathan.crop((j*16,0,(j+1)*16,32))
        if i==3:a=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        b=jobard.crop((i*16,0,(i+1)*16,32))
        def bounds(im):
            mask=Image.new('L',im.size);mask.putdata([255 if k else 0 for k in im.getdata()]);return mask.getbbox()
        assert bounds(a)==bounds(b),(i,bounds(a),bounds(b))
        result.append(dict(orientation=['front','back','left','right'][i],nathan_bounds=bounds(a),jobard_bounds=bounds(b),visible_width=12,visible_height=19))
        for row,im in enumerate([a,b]):
            rgba=im.convert('RGB').convert('RGBA');alpha=Image.new('L',im.size);alpha.putdata([255 if k else 0 for k in im.getdata()]);rgba.putalpha(alpha)
            sprite=rgba.resize((128,256),Image.Resampling.NEAREST);preview.paste(sprite,(100+i*132,20+row*270),sprite)
    draw.text((5,140),'Nathan',fill='black');draw.text((5,410),'Jobard',fill='black')
    preview.save(OUT/'comparaison-nathan-jobard-x8.png')
    assert (ROOT/'graphics/yokai_characters/dr_jobard/overworld.4bpp').stat().st_size==1024
    assert (ROOT/'graphics/yokai_characters/dr_jobard/overworld.gbapal').stat().st_size==32
    (OUT/'PROPORTIONS.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    OUT.mkdir(exist_ok=True);rows=[];proportions=graphics_validation();textlines=native_text_widths()
    for gender,name in [(0,'nathan'),(1,'katie')]:
        r=new_game(gender)
        try:
            r.call('CreateMon',r.symbols['gPlayerParty'],5,24,15,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
            warp(r,3,5,28,10);face_a(r,'U');finish(r)
            assert location(r)==(3,5) and not r.call('FlagGet',0x332)
            r.frame.save(OUT/f'{name}-jobard-ville.png')
            # Turn through all stationary orientations by actual interaction.
            for x,y,d,orientation in [(28,8,'D','dos'),(27,9,'R','gauche'),(29,9,'L','droite')]:
                warp(r,3,5,x,y);face_a(r,d);finish(r);r.frame.save(OUT/f'{name}-jobard-{orientation}.png')
            warp(r,3,5,28,10);r.call('FlagSet',0x822)
            enter(r,False);assert location(r)==(3,5)
            enter(r);assert location(r)==MAPS[NAMES[0]] and pos(r)==(6,7)
            r.frame.save(OUT/f'{name}-laboratoire.png')
            lab_doctor(r);assert not r.call('FlagGet',0x333)
            # B cancellation leaves the actor, map and observation flags intact.
            walk(r,'L',2);walk(r,'U');face_a(r,'U');waitmenu(r,'Task_MultichoiceMenu_HandleInput');tap(r,0);finish(r)
            assert location(r)==MAPS[NAMES[0]] and not any(r.call('FlagGet',f) for f in FLAGS)
            walk(r,'D');walk(r,'R',2)
            # Enter/leave an unobserved room, then revisit and complete in 3,1,2 order.
            computer(r,2);assert location(r)==MAPS[NAMES[3]]
            leave(r);assert location(r)==MAPS[NAMES[0]] and not r.call('FlagGet',FLAGS[2])
            for number in [2,0,1]:
                computer(r,number);assert location(r)==MAPS[NAMES[1+number]] and pos(r)==(6,7)
                for guard in ['CanUseEscapeRopeOnCurrMap','SetUpFieldMove_Dig','SetUpFieldMove_Teleport','SetUpFieldMove_Fly']:
                    assert guard in r.symbols and not r.call(guard),guard
                computer(r);assert r.call('FlagGet',FLAGS[number])
                save_continue(r);assert r.call('FlagGet',FLAGS[number]) and location(r)==MAPS[NAMES[1+number]]
                r.frame.save(OUT/f'{name}-salle-{number+1}.png')
                leave(r,6+number);assert location(r)==MAPS[NAMES[0]] and pos(r)==(6,7)
            lab_doctor(r);assert r.call('FlagGet',0x333)
            save_continue(r);assert all(r.call('FlagGet',f) for f in FLAGS+[0x332,0x333])
            # All three southern exit lanes, with re-entry and persistent completion.
            for x in [6,7,8]:
                leave(r,x);assert location(r)==(3,5) and pos(r)==(28,10)
                save_continue(r);assert r.call('FlagGet',0x333)
                enter(r);assert location(r)==MAPS[NAMES[0]]
            # Repeated completion gives no badge/item/experience benefit.
            bag=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x310,0x5F8-0x310)
            exp=r.call('GetMonData',r.symbols['gPlayerParty'],25,0)
            lab_doctor(r);lab_doctor(r)
            assert bag==r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x310,0x5F8-0x310)
            assert exp==r.call('GetMonData',r.symbols['gPlayerParty'],25,0)
            assert not any(r.call('FlagGet',f) for f in [0x820,0x821,0x823,0x824,0x825,0x826,0x827])
            rows.append(dict(gender=name,passed=True,city_guard=True,invitation_decline=True,menu_cancel=True,observation_order=[3,1,2],save_continue_in_each_room=True,all_three_return_lanes=True,all_three_lab_exit_lanes=True,repeat_no_item_badge_or_exp_reward=True,native_escape_rope_dig_teleport_fly_guards=True))
        except BaseException:
            r.frame.save(OUT/f'{name}-diagnostic.png');raise
        finally:r.close()
    # Old Carmin saves have only eight cached actor templates.
    r=new_game()
    try:
        warp(r,3,5,19,25);r.call('FlagSet',0x822)
        p=r.u32(r.symbols['gSaveBlock1Ptr'])+0x8e0+24*8;r.write(p,bytes(24));r.call('FlagClear',0x32E)
        r.call('SaveMapView');assert r.call('TrySavingData',0,max_frames=1200)==1
        assert r.call('LoadGameSave',0,max_frames=1200)==1
        r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);r.run(900)
        assert idle(r) and location(r)==(3,5) and pos(r)==(28,10)
        assert r.call('FlagGet',0x32E) and r.call('FlagGet',0x822)
        assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x8e0+24*8+1,1)==bytes([173])
        save_continue(r);assert pos(r)==(28,10)
        r.frame.save(OUT/'ancienne-sauvegarde-ville.png')
        rows.append(dict(test='Legacy Carmin cached actor refresh, safe return, trophy preserved and second Continue stable',passed=True))
    finally:r.close()
    rom=Path(os.environ['YOKAI_QA_ROM']);report=dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),rom_size=rom.stat().st_size,native_text_lines=textlines,proportions=proportions,maps=MAPS,tests=rows)
    (OUT/'TEST_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',len(rows),flush=True)

if __name__=='__main__':main()

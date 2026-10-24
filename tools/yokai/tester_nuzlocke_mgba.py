#!/usr/bin/env python3
"""Isolated mGBA Nuzlocke fixtures, not a complete adventure playthrough.
New-game mode selection and Continue use controller input. Parties, maps, status,
encounter policies and PC rosters are prepared via native calls. Flash writes and
final erasure affect only this emulator's temporary battery, never a user save.
"""
import ctypes as C
import hashlib
import json
import os
import struct
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game

P = ROOT / 'docs/nuzlocke-20261024' / os.environ.get('NUZ_MODE', 'public')
P.mkdir(parents=True, exist_ok=True)
r = new_game(gender=int(os.environ.get('NUZ_GENDER', 0)), nuzlocke=True, difficulty_capture=P/'choix-mode.png')
rows = []
groups = json.loads((ROOT/'data/maps/map_groups.json').read_text())
maps = {n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
party = r.symbols['gPlayerParty']; enemy = r.symbols['gEnemyParty']

def passed(msg):
    rows.append(msg); print('PASS', msg, flush=True)

def pulse(k, after=30):
    r.keys=set(); r.run(4); r.keys={k}; r.run(4); r.keys=set(); r.run(after)

def warp(name, x, y):
    g,n=maps[name]; r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap')
    r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(300)

def mon(ptr, species, level=30, shiny=False):
    ot=r.u32(r.u32(r.symbols['gSaveBlock2Ptr'])+10)
    r.call('CreateMon',ptr,species,level,31,1,ot if shiny else ot^0x1000,0,0)
    assert bool(r.call('IsMonShiny',ptr)) == shiny

def data(ptr,field,value):
    scratch=r.symbols['gStringVar4'];r.w32(scratch,value);r.call('SetMonData',ptr,field,scratch)

def encounter(species, shiny=False):
    mon(enemy,species,shiny=shiny); r.call('NuzlockeBeginBattle')
    return bool(r.call('NuzlockeCanCapture',enemy))

def battery():
    r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
    return C.string_at(r.lib.retro_get_memory_data(0),131072)

def save():
    assert r.call('TrySavingData',0,max_frames=3000)==1

def continue_game():
    r.lib.retro_reset();r.run(600);pulse(3,180)
    for f in range(15000):
        r.keys={8} if f%16<3 else set();r.run()
        if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3):break
    else:raise AssertionError('Continue did not reach overworld')
    r.keys=set();r.run(180)

try:
    assert r.call('NuzlockeEnabled')==1;passed('New game selects Nuzlocke through the native menu')
    mon(enemy,1);r.call('GiveMonToPlayer',enemy)
    r.call('FlagSet',0x829) # Pokedex and first supply unlocked; pre-Ball encounters must not consume zones.
    warp('Route2',10,4)
    assert encounter(22);assert r.call('NuzlockeCanCapture',enemy);passed('First encounter stays eligible for multiple Ball attempts')
    assert not encounter(23);passed('Leaving the first encounter without a catch consumes the zone')
    warp('Route1',10,10)
    assert not encounter(1);assert encounter(23);passed('Owned starter is skipped as a duplicate; the first new species is eligible')
    r.call('NuzlockeRecordCapture',enemy);r.call('GiveMonToPlayer',enemy)
    r.call('ZeroMonData',party+100);r.write(r.symbols['gPlayerPartyCount'],b'\1')
    warp('Route3',10,8)
    assert not encounter(23);assert encounter(24);passed('Previously obtained species blocked in another zone, including after release')
    assert encounter(23,True);passed('Shiny duplicate can be caught even in a consumed zone')
    warp('Route4',12,8)
    assert encounter(22,True);r.call('NuzlockeRecordCapture',enemy)
    assert encounter(25);passed('Shiny encounter does not consume the ordinary encounter')
    # Tutorial / pre-Ball encounters must not burn the player\'s Route 1 attempt.
    warp('Route5',10,8);r.call('FlagClear',0x829)
    assert encounter(26);r.call('FlagSet',0x829);assert encounter(27)
    passed('Encounter limits begin with the first Ball supply, not the parcel trip')
    assert r.call('ItemId_GetPrice',4)==160 and r.call('ItemId_GetPrice',3)==480 and r.call('ItemId_GetPrice',2)==960
    assert r.call('ItemId_GetPrice',13)==300;passed('Balls cost 20 percent less; Potion price unchanged')
    # Dead marker prevents every ordinary healing route, including PC rebuilding and item effects.
    first=party;second=party+100
    mon(first,1);mon(second,5);r.write(r.symbols['gPlayerPartyCount'],b'\2')
    r.call('NuzlockeRecordOwned',first);r.call('NuzlockeRecordOwned',second)
    r.call('NuzlockeMarkDead',first);assert r.call('NuzlockeIsDead',first)
    data(first,57,100);assert r.call('GetMonData',first,57)==0
    r.call('HealPlayerParty');assert r.call('GetMonData',first,57)==0
    assert r.call('PokemonUseItemEffects',first,24,0,0,0)==1
    assert r.call('PokemonUseItemEffects',first,25,0,0,0)==1
    assert r.call('PokemonItemUseNoEffect',first,24,0,0)==1
    ptr=r.call('GetBoxedMonPtr',0,0);r.write(ptr,r.read(first,80));r.call('BoxMonToMon',ptr,enemy)
    assert r.call('GetMonData',enemy,57)==0;r.call('ZeroBoxMonData',ptr)
    assert r.call('NuzlockeResolveParty')==0 and r.read(r.symbols['gPlayerPartyCount'],1)==b'\1'
    assert r.call('GetMonData',first,11)==5;passed('Permanent death: healing, Revive, Max Revive and PC reconstruction cannot revive; dead slot removed')
    # Actual poisoned HP reaches zero, then native poison handling marks and resolves it.
    mon(first,1);mon(second,5);r.write(r.symbols['gPlayerPartyCount'],b'\2')
    data(first,57,1);data(first,55,8);assert r.call('DoPoisonFieldEffect')==2
    r.call('FaintFromFieldPoison',0);assert r.call('NuzlockeIsDead',first)
    assert r.call('NuzlockeResolveParty')==0;passed('Field poison death is permanent too')
    # Last living PC survivor is moved into party, removed from its box.
    r.call('NuzlockeMarkDead',first);ptr=r.call('GetBoxedMonPtr',13,29);mon(enemy,7)
    r.write(ptr,r.read(enemy,80));assert r.call('NuzlockeResolveParty')==1
    assert r.call('GetMonData',first,11)==7 and r.call('GetMonData',first,57)>0
    assert not r.call('GetBoxMonData',ptr,11);passed('A survivor in the last PC slot rescues the run')
    # Linked battles are external to the challenge; ordinary local battles still count.
    old=r.u32(r.symbols['gBattleTypeFlags']);r.w32(r.symbols['gBattleTypeFlags'],2)
    assert not r.call('NuzlockeBattleApplies');r.w32(r.symbols['gBattleTypeFlags'],old)
    # Preserve rules / death history across battery save and cold Continue.
    warp('PalletTown_PlayersHouse_2F',4,4);save();save()
    initial=battery();assert initial!=b'\xff'*131072
    continue_game();assert r.call('NuzlockeEnabled')==1
    warp('Route2',10,4);assert not encounter(28)
    passed('Native battery Continue preserves mode and the lost first encounter')
    # Total loss, then real erase of both generations of the test battery.
    r.call('NuzlockeMarkDead',party);assert r.call('NuzlockeResolveParty')==2
    r.call('NuzlockeGameOver',max_frames=3000);r.run(60);r.frame.save(P/'game-over.png')
    assert battery()==b'\xff'*131072;passed('Total loss erases all flash sectors, including both alternating save slots')
    pulse(8,600)
    # No Continue item remains after soft reset.
    assert r.read(r.symbols['gSaveFileStatus'],2)==b'\0\0',r.read(r.symbols['gSaveFileStatus'],2)
    passed('After Game Over, reset has no valid Continue save')
    (P/'TEST.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),cases=rows),ensure_ascii=False,indent=2)+'\n')
finally:
    r.frame.save(P/'dernier.png');r.close()

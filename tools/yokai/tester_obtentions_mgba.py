#!/usr/bin/env python3
"""Native encounters and real gift scripts in mGBA, with explicit fixture scope."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
r=Emulator();results=[]
proof=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves';proof.mkdir(exist_ok=True)
try:
    r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault')
    glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
    r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Nathan')+b'\xff')
    r.call('CB2_NewGame');r.run(180)
    for index,expected in enumerate([5,29,87]):assert r.call('GetStarterSpeciesById',index)==expected
    results.append({'test':'Native starter selection order','species':[5,29,87],'passed':True})
    enemy=r.symbols['gEnemyParty']
    for cleared in [False,True]:
        r.call('FlagSet' if cleared else 'FlagClear',0x82C)
        for species in [48,84,145,5,29,87]:
            r.call('GenerateWildMon',species,30,0)
            actual=r.call('GetMonData',enemy,11,0)
            assert actual==(species if cleared else 91),(cleared,species,actual)
    results.append({'test':'Wild post-League guard, six restricted species before and after flag','passed':True})
    r.call('FlagClear',0x82C)
    for attempt in range(4):
        r.call('ScriptContext_SetupScript',r.symbols['CeladonCity_Condominiums_RoofRoom_EventScript_EeveeBall'])
        # B advances text and declines nickname; no arbitrary writes into script result.
        for frame in range(1200):r.keys={0} if frame%16<4 else set();r.run()
        expected=min(attempt+1,3)
        assert r.call('VarGet',0x40F2)==expected
        assert r.read(r.symbols['gPlayerPartyCount'],1)==bytes([expected])
    results.append({'test':'Three Jibanyan gifts, fourth attempt gives nothing; full native script and B input','passed':True})
    r.frame.save(proof/'jibanyan-trois-cadeaux.png')
    assert r.call('TrySavingData',0,max_frames=1200)==1
    r.call('VarSet',0x40F2,0)
    assert r.call('LoadGameSave',0,max_frames=1200)==1
    assert r.call('VarGet',0x40F2)==3
    results.append({'test':'Jibanyan gift counter survives native Flash save/load','passed':True})
    # Full party + all 420 PC slots full: failure must not spend a gift.
    party=r.symbols['gPlayerParty']
    for slot in range(6):r.call('CreateMon',party+100*slot,5,10,31,1,100,0,0)
    r.write(r.symbols['gPlayerPartyCount'],b'\x06')
    storage=r.u32(r.symbols['gPokemonStoragePtr'])
    boxed=r.read(party,80)
    r.write(storage+4,boxed*420)
    r.call('VarSet',0x40F2,0)
    r.call('FlagClear',0x57);r.call('FlagClear',0x263)
    r.call('ScriptContext_SetupScript',r.symbols['CeladonCity_Condominiums_RoofRoom_EventScript_EeveeBall'])
    for frame in range(1200):r.keys={0} if frame%16<4 else set();r.run()
    assert r.call('VarGet',0x40F2)==0 and r.call('FlagGet',0x57)==0
    assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\x06'
    results.append({'test':'Full party and 420 full PC slots: no Jibanyan gift consumed','passed':True})
    # Real Dojo map, trainers marked defeated, existing common gift scripts.
    r.write(storage+4,b'\0'*(420*80))
    for trainer in range(317,322):r.call('SetTrainerFlag',trainer)
    r.call('VarSet',0x4081,1)
    r.call('SetWarpDestination',14,2,255,6,8);r.call('WarpIntoMap')
    r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.keys=set();r.run(180)
    for index,(species,localid) in enumerate([(80,6),(78,7)]):
        r.call('VarSet',0x4001,species);r.call('VarSet',0x800F,localid)
        r.call('ScriptContext_SetupScript',r.symbols['SaffronCity_Dojo_EventScript_GiveHitmon'])
        for frame in range(1500):r.keys={0} if frame%16<4 else set();r.run()
        assert r.call('GetBoxMonDataAt',0,index,11)==species
        assert r.call('FlagGet',0x60+index)==1
    assert r.call('FlagGet',0x278)==1
    assert r.read(r.symbols['gPlayerPartyCount'],1)==b'\x06'
    results.append({'test':'Both Dojo gifts sent to PC on actual Dojo map; independent persistent flags','passed':True})
    r.frame.save(proof/'dojo-deux-cadeaux-pc.png')

finally:r.close()
report={'engine':'mGBA','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),
        'scope':'Native function and script fixtures on a new-game field. Gift entry scripts and common Dojo reward path tested; overworld object approach and Dojo Yes/No selection still pending.',
        'results':results,'all_151_obtainable_verified':False,'complete_story_verified':False}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_OBTENTIONS_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Capture Matt's actual battle portraits and native overworld orientations/steps."""
import hashlib,json,re
from PIL import Image
from mgba_rpc import Emulator,ROOT
proof=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves';proof.mkdir(exist_ok=True)
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
opponents={k:int(v) for k,v in re.findall(r'^#define\s+(TRAINER_\w+)\s+(\d+)',(ROOT/'include/constants/opponents.h').read_text(),re.M)}
def newgame():
    r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault')
    r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Nathan')+b'\xff')
    r.call('CB2_NewGame');r.run(180);return r
results=[]
for role,trainer in [('early','TRAINER_RIVAL_ROUTE22_EARLY_CHARMANDER'),('late','TRAINER_RIVAL_POKEMON_TOWER_CHARMANDER'),('champion','TRAINER_CHAMPION_FIRST_CHARMANDER')]:
    r=newgame()
    try:
        r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,0,0)
        r.write(r.symbols['gPlayerPartyCount'],b'\x01')
        r.w32(r.symbols['gTrainerBattleOpponent_A'],opponents[trainer])
        r.call('StartTrainerBattle');r.run(401)
        r.frame.save(proof/f'matt-combat-{role}.png')
        # Trainer metadata is checked independently of placeholder name expansion.
        raw=r.read(r.symbols['gTrainers']+40*opponents[trainer]+4,12)
        assert raw.startswith(bytes(glyphs[c] for c in 'Matt')+b'\xff')
        results.append({'test':'Real trainer battle portrait '+role,'name':'Matt','capture':f'matt-combat-{role}.png','battle_finished':False})
    finally:r.close()
r=newgame()
try:
    for trainer in range(317,322):r.call('SetTrainerFlag',trainer)
    r.call('VarSet',0x4081,1)
    r.call('SetWarpDestination',14,2,255,6,10);r.call('WarpIntoMap')
    r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(180)
    objects=[]
    for x,movement in [(3,8),(5,7),(7,9),(9,10)]:
        index=r.call('SpawnSpecialObjectEventParameterized',72,movement,100+x,x+7,7+7,3)
        assert index<16;objects.append(r.symbols['gObjectEvents']+index*36)
    r.run(30);r.frame.save(proof/'matt-overworld-quatre-directions.png')
    frames=[]
    for repeat in range(3):
        for obj,action in zip(objects,[0x25,0x26,0x27,0x28]):
            r.call('ObjectEventClearHeldMovementIfFinished',obj)
            r.call('ObjectEventSetHeldMovement',obj,action)
        for frame in range(48):
            r.run()
            if frame%4==0:frames.append(r.frame.copy())
    frames[0].save(proof/'matt-marche-quatre-directions.gif',save_all=True,append_images=frames[1:],duration=67,loop=0)
    frames[4].save(proof/'matt-marche-phase.png')
    results.append({'test':'Four native facing directions and three walk-in-place cycles each','fixture_map':'Dojo with defeated trainers','capture':'matt-marche-quatre-directions.gif'})
finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),
        'results':results,'native_assets':{'battle':[64,64,3],'overworld':[16,32,9]},
        'palette':'15 opaque RGB555 colors, transparent index 0, dedicated special NPC palette',
        'complete_story_appearances_verified':False,'Nathan_Katie_artwork_completed':'graphics/yokai_characters/nathan/normal.4bpp' in (ROOT/'src/data/object_events/object_event_graphics.h').read_text(),
        'remaining':'All scripted rival appearances and real navigation remain to be played; protagonist tests are reported separately.'}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_MATT_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

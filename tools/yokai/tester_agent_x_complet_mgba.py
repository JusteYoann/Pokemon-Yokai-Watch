#!/usr/bin/env python3
"""Compiled Agent X graphics: four facings, gait, displacement and native trainer loader.
No runtime graphics injection. Temporary field actors and battle-portrait fixture only.
"""
import hashlib,json,os
from PIL import Image,ImageDraw,ImageFont
from mgba_rpc import ROOT
from mgba_new_game import new_game
from scenario_qa_helpers import warp
OUT=ROOT/os.environ.get('YOKAI_AGENT_REPORT','QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/AGENT_X_COMPLET');OUT.mkdir(parents=True,exist_ok=True)
P=ROOT/'graphics/yokai_characters/agent_x';report=dict(passed=False,scope=__doc__,runtime_graphics_injection=False)
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={name:(i,j)for i,g in enumerate(groups['group_order'])for j,name in enumerate(groups[g])}
r=new_game();report['rom_sha256']=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();report['rom_bytes']=len(r.rom_buffer.raw)-1
try:
 warp(r,*maps['Route1'],6,12);r.call('LockPlayerFieldControls');actors=[]
 for n,(name,gfx,x,y) in enumerate([('Don Morleone',164,8,12),('Agent X',176,10,12),('Mafiamille 1',165,3,11),('Mafiamille 2',166,5,11),('Mafiamille 3',167,7,11),('Mafiamille 1',165,9,11),('Mafiamille 2',166,4,12),('Mafiamille 3',167,12,12)]):
  idx=r.call('SpawnSpecialObjectEventParameterized',gfx,0,220+n,x+7,y+7,3);assert idx<16
  obj=r.symbols['gObjectEvents']+36*idx;sp=r.symbols['gSprites']+68*r.read(obj+4,1)[0];r.call('ObjectEventTurn',obj,1)
  actors.append((name,gfx,obj,sp))
 r.run(60);a=next(v for v in actors if v[1]==176);obj,sp=a[2:]
 data=(P/'overworld.4bpp').read_bytes();assert r.read(r.symbols['gObjectEventPic_YokaiAgentX'],len(data))==data
 frames=[data[i*256:(i+1)*256]for i in range(9)];pal=(P/'overworld.gbapal').read_bytes()
 bank=int.from_bytes(r.read(sp+4,2),'little')>>12;assert 12<=bank<=15
 assert r.read(0x05000200+bank*32,32)==pal
 for name,gfx,o,s in actors:
  if gfx!=176:assert int.from_bytes(r.read(s+4,2),'little')>>12!=bank
 assert r.read(0x05000200+10*32,32)==(ROOT/'graphics/yokai_characters/don_morleone/overworld.gbapal').read_bytes()
 r.frame.save(OUT/'groupe-mgba-native.png');r.frame.resize((960,640),Image.Resampling.NEAREST).save(OUT/'groupe-mgba-x4.png')
 results=[]
 for direction,label,expected in [(1,'face',{0,3,4}),(2,'dos',{1,5,6}),(3,'gauche',{2,7,8}),(4,'droite',{2,7,8})]:
  r.call('ObjectEventClearHeldMovementIfFinished',obj);r.call('ObjectEventTurn',obj,direction);r.run(30)
  r.frame.save(OUT/f'{label}-mgba.png');seen=set();movie=[]
  for repeat in range(4):
   r.call('ObjectEventClearHeldMovementIfFinished',obj);r.call('ObjectEventSetHeldMovement',obj,0x24+direction)
   for f in range(40):
    r.run();attr=int.from_bytes(r.read(sp+4,2),'little');tile=attr&1023
    assert attr>>12==bank and r.read(0x05000200+bank*32,32)==pal
    assert bool(int.from_bytes(r.read(sp+2,2),'little')&0x1000)==(direction==4)
    native=r.read(0x06010000+tile*32,256);seen.update(i for i,b in enumerate(frames)if b==native)
    if f%4==0:movie.append(r.frame.copy().resize((720,480),Image.Resampling.NEAREST))
  assert expected<=seen,(label,seen)
  movie[0].save(OUT/f'marche-{label}-mgba.gif',save_all=True,append_images=movie[1:],duration=67,loop=0)
  results.append(dict(direction=label,frames_seen=sorted(seen),palette_verified=True,flip_correct=True))
 # Native one-tile displacement in both horizontal directions, with movement APIs.
 positions=[]
 for action in [0x12,0x13]:
  r.call('ObjectEventClearHeldMovementIfFinished',obj);before=r.read(obj+16,4)
  r.call('ObjectEventSetHeldMovement',obj,action);r.run(50);after=r.read(obj+16,4)
  assert before!=after;positions.append(dict(action=action,before=before.hex(),after=after.hex()))
 report.update(field_facings=results,simultaneous_morleone_palette_verified=True,agent_palette_bank=bank,displacements=positions,field_compiled_tiles_verified=True)
 # Native trainer-picture loader uses registered ID160 from the compiled ROM.
 # A battle fixture supplies the backdrop; no trainer team or story assignment is added.
 r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.w32(r.symbols['gTrainerBattleOpponent_A'],17);r.call('StartTrainerBattle');r.run(401)
 old=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0];oldsp=r.symbols['gSprites']+68*old
 r.write(oldsp+62,bytes([r.read(oldsp+62,1)[0]|4]));r.w32(oldsp+28,r.symbols['SpriteCallbackDummy']|1)
 new=r.call('CreateTrainerPicSprite',160,1,176,40,8,0xffff);assert new<64,new
 r.run(2);s=r.symbols['gSprites']+68*new;attr=int.from_bytes(r.read(s+4,2),'little');tile=attr&1023
 assert r.read(0x06010000+tile*32,2048)==(P/'battle.4bpp').read_bytes()
 assert r.read(0x05000200+(attr>>12)*32,32)==(P/'normal.gbapal').read_bytes()
 r.frame.save(OUT/'portrait-combat-mgba-native.png');r.frame.resize((960,640),Image.Resampling.NEAREST).save(OUT/'portrait-combat-mgba-x4.png')
 report.update(passed=True,battle_portrait_registered_id=160,battle_tiles_and_palette_verified=True,limitations=['Temporary spawned actors; no new story placement','Trainer portrait loaded natively on a battle fixture, not an Agent X scripted encounter or team','New poses and portrait await creator artistic review','No claim of complete adventure or all field-effect/reflection combinations tested'])
 print('PASS Agent X compiled field and trainer graphics')
finally:
 r.close();(OUT/'CONTROLE.json').write_text(json.dumps(report,indent=2)+'\n')

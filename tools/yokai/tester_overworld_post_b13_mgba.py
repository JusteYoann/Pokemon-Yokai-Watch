#!/usr/bin/env python3
"""Actual map objects, 5 static encounters/captures and original Leo teleporter.

Fixtures set progression/item access and warp; not proof of travel or full story.
"""
import hashlib,json,re,struct,subprocess,os
from pathlib import Path
from mgba_rpc import Emulator,ROOT
from mgba_new_game import new_game
import tester_cameos_boss_mgba as b
G=json.loads((ROOT/'data/maps/map_groups.json').read_text());MAPS={name:(i,j) for i,key in enumerate(G['group_order']) for j,name in enumerate(G[key])}
P=ROOT/'QA_RECETTE_FINALE/POST_B13/sprites/overworld';P.mkdir(parents=True,exist_ok=True);(P/'preuves').mkdir(exist_ok=True);checks=[]
def warp(r,name,x,y):
 g,n=MAPS[name];r.keys=set();r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1800):
  r.run()
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Map not loaded')
 r.run(180)
def fixture():
 r=new_game()
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(b.glyphs[c] for c in 'Test')+b'\xff')
 r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.call('FlagSet',0x828);r.call('FlagSet',0x829);r.call('FlagSet',0x82C)
 return r
def object_ptr(r,name,gfx):
 g,n=MAPS[name]
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i
  if r.read(p,1)[0]&1 and r.read(p+5,1)[0]==gfx:return p
 raise AssertionError(('Expected specific object absent',name,gfx))
def capture(r,species,stem):
 funcs={int(line.split()[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(line.split())==3 and line.split()[2]=='HandleInputChooseAction'}
 for f in range(9000):
  r.keys={8} if f%16<2 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
 else:raise AssertionError(('Original static event did not start combat',stem))
 for f in range(7000):
  r.keys={0} if f%16<2 else set();r.run()
  if r.u32(r.symbols['gBattlerControllerFuncs']) in funcs:break
 else:raise AssertionError(('Static did not reach action menu',stem))
 assert r.call('GetMonData',r.symbols['gEnemyParty'],b.C['MON_DATA_SPECIES'],0)==species
 r.keys=set();r.run(16);r.frame.save(P/'preuves'/f'{stem}-combat.png');r.write(r.symbols['gBagMenuState']+6,b'\x02\x00')
 r.keys={7};r.run(1);r.keys=set();r.run(16);assert r.read(r.symbols['gActionSelectionCursor'],1)==b'\x01'
 r.keys={8};r.run(1);r.keys=set();r.run(240)
 for _ in range(2):r.keys={8};r.run(1);r.keys=set();r.run(90)
 for f in range(15000):
  r.keys={0} if f%16<2 else set();r.run()
  if f%64==0 and r.read(r.symbols['gBattleOutcome'],1)==b'\x07' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError(('Capture did not return to map',stem))
 b.finish(r);assert r.call('GetMonData',r.symbols['gPlayerParty']+100,b.C['MON_DATA_SPECIES'],0)==species;assert r.call('GetSetPokedexFlag',species,1)==1
 checks.append(dict(test=stem+' original map interaction, correct wild species and actual Master Ball capture into party/Medallium',species=species,passed=True))
def statics():
 for name,old,gfx,species,slug in [('Route12','SNORLAX',169,33,'misterre-route12'),('Route16','SNORLAX',169,33,'misterre-route16')]:
  print('START',slug,flush=True);r=fixture()
  try:
   objects=json.loads((ROOT/f'data/maps/{name}/map.json').read_text())['object_events'];obj=next(o for o in objects if o['graphics_id']==f'OBJ_EVENT_GFX_YOKAI_'+('MISTERRE' if species==33 else 'OCTORGONE' if species==15 else 'MADEMOAISELLE'))
   if species==33:r.call('FlagSet',b.C['FLAG_GOT_POKE_FLUTE']);r.call('AddBagItem',b.C['ITEM_POKE_FLUTE'],1)
   r.call('ClearBag');r.call('AddBagItem',b.C['ITEM_MASTER_BALL'],1);warp(r,name,obj['x'],obj['y']+1);ptr=object_ptr(r,name,gfx);r.frame.save(P/'preuves'/f'{slug}-carte.png')
   pal=ROOT/'graphics/yokai_characters/static_yokai'/('misterre' if species==33 else 'octorgone' if species==15 else 'mademoaiselle')/'normal.gbapal'
   assert r.read(r.symbols['gPlttBufferUnfaded']+512+10*32,32)==pal.read_bytes()
   checks.append(dict(test=slug+' correct dedicated object and native RGB555 palette in map',object_gfx=gfx,passed=True))
   b.interact(r);capture(r,species,slug)
  finally:r.close()
  print('PASS',slug,flush=True)
def leo():
 for gender in [0,1]:
  r=fixture()
  try:
   r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));warp(r,'Route25_SeaCottage',10,7);object_ptr(r,'Route25_SeaCottage',172);r.frame.save(P/'preuves'/f'leo-{gender}-avant.png')
   b.interact(r);b.finish(r);assert r.call('FlagGet',2) # Original BILL_IN_TELEPORTER FLAG_TEMP_2.
   assert not r.call('FlagGet',b.C['FLAG_HELPED_BILL_IN_SEA_COTTAGE'])
   # Walk from the unchanged player tile (10,7) to below the original PC at (4,5).
   def player_xy():
    ptr=r.symbols['gObjectEvents']+36*r.read(r.symbols['gPlayerAvatar']+5,1)[0]
    x,y=struct.unpack('<hh',r.read(ptr+16,4));return x-7,y-7
   for dest in [(10,6),(4,6)]:
    for attempt in range(180):
     x,y=player_xy()
     if (x,y)==dest:break
     key=7 if x<dest[0] else 6 if x>dest[0] else 5 if y<dest[1] else 4
     r.keys={key};r.run(1)
    else:raise AssertionError(('Controller could not reach PC',player_xy(),dest))
    r.keys=set();r.run(20)
   assert player_xy()==(4,6),player_xy()
   b.interact(r);b.finish(r)
   assert r.call('FlagGet',b.C['FLAG_HELPED_BILL_IN_SEA_COTTAGE'])
   object_ptr(r,'Route25_SeaCottage',73);r.frame.save(P/'preuves'/f'leo-{gender}-humain.png')
   checks.append(dict(test='Leo/Jibanyan original walking/teleporter and restoration, actual room controls',gender=gender,passed=True))
  finally:r.close()
passed=False;error='Interrupted'
try:statics();leo();passed=True;error=None
except Exception as e:error=str(e);raise
finally:
 (P/'MISTERRE_LEO_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba')).read_bytes()).hexdigest(),scope='Native objects/interactions/captures, warp/progression/item fixtures; not whole adventure',results=checks),indent=2)+'\n');print(dict(passed=passed,error=error,checks=len(checks)),flush=True)

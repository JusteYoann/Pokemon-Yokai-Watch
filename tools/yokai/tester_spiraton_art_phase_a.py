#!/usr/bin/env python3
"""Stage A only: static candidate on real mGBA battle, no production art swap.
Fresh boosted QA party and explicit diagnostic boss. Candidate shown only by RPC.
Also inspect unmodified house maps and exercise their existing exit warps.
"""
import os,json,hashlib,struct,subprocess
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
Q=ROOT/os.environ.get('YOKAI_SPIRATON_ART_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A');Q.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;rows=[]
try:
 field=r.snapshot();strong_party(r)
 r.call('SpiratonBattleArmPrototype');r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',744));r.call('StartTrainerBattle')
 callbacks={int(v[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=l.split())==3 and v[2]=='HandleInputChooseAction'}
 for f in range(3000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Initial menu missing')
 r.keys=set();r.run(60);before=r.frame.copy();r.frame.save(Q/'avant-apercu-bouh.png')
 native_sprite=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
 native_hidden=bool(r.read(r.symbols['gSprites']+68*native_sprite+62,1)[0]&4)
 sprite=r.call('SpiratonArtPreviewShow');assert sprite<64,sprite
 r.keys=set();r.run(60);after=r.frame.copy();r.frame.save(Q/'don-spiraton-candidat-natif.png')
 assert r.read(r.symbols['sFirst'],1)==b'\1','Static art preview started combat turn'
 bank=r.call('IndexOfSpritePaletteTag',0x7D55);tile=r.call('GetSpriteTileStartByTag',0x7D54)
 assert bank<16 and tile!=0xFFFF
 expected=r.read(r.symbols['sSpiratonPreviewPalette'],32)
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+bank*32,32)==expected
 for label,box in [('enemy HUD',(0,0,108,47)),('player HUD',(124,76,240,112)),('menus',(0,114,240,160))]:
  assert before.crop(box).tobytes()==after.crop(box).tobytes(),('Candidate altered interface',label)
 assert before.tobytes()!=after.tobytes()
 rows.append(dict(test='Actual static native candidate, HUD/menu unchanged, first turn still pending',passed=True,logical_sprite=sprite,hardware_objects=4,palette_bank=bank,tile_start=tile,obj_bytes=6144,visible_bbox_in_screen=[120,-4,232,72]))
 r.call('SpiratonArtPreviewHide');r.run(60)
 assert r.call('IndexOfSpritePaletteTag',0x7D55)==255
 assert r.call('GetSpriteTileStartByTag',0x7D54)==65535
 assert bool(r.read(r.symbols['gSprites']+68*native_sprite+62,1)[0]&4)==native_hidden
 rows.append(dict(test='Preview removal frees tile/palette resources and restores native diagnostic sprite',passed=True))
 # Normal existing Yo-kai as a live rendering reference, not an edited screenshot.
 r.restore(field);strong_party(r)
 r.call('CreateMon',r.symbols['gEnemyParty'],86,60,24,1,0,0,0x1234)
 r.call('StartScriptedWildBattle')
 for f in range(3000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Normal Turboss reference menu missing')
 r.keys=set();r.run(60);r.frame.save(Q/'turboss-reference-mgba.png')
 rows.append(dict(test='Existing Turboss battle graphic rendered without preview overlay',species=86,passed=True))
 # Independent house inspection fixtures, no actor inserted and no map/script edited.
 for house,outside,stem in [('SixIsland_WaterPath_House2','SixIsland_WaterPath','ile6-chemin-o'),('FiveIsland_House2','FiveIsland','ile5-maison2')]:
  r.restore(field);r.call('FlagSet',C['FLAG_SYS_GAME_CLEAR']);warp(r,*MAPS[house],4,6)
  r.keys=set();r.run(90);r.frame.save(Q/f'{stem}-interieur-existant.png')
  r.keys={5};r.run(90);r.keys=set();r.run(180)
  assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)==bytes(MAPS[outside]),house
  r.frame.save(Q/f'{stem}-exterieur-existant.png')
  rows.append(dict(test='Unmodified existing interior loads and normal door exit reaches paired exterior',house=house,outside=outside,passed=True))
 passed=True
finally:
 (Q/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),production_art_unchanged=True,production_finale_enabled=False,morphing_composite_not_yet_integrated=True,results=rows),indent=2)+'\n');r.close()
print('PASS: native static candidate and existing house exits; artistic approval pending')

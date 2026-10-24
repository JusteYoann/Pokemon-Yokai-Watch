#!/usr/bin/env python3
import sys,os,json,hashlib,subprocess,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/yokai'))
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp,strong_party
OUT=ROOT/'docs/beta-retours-20261024/interfaces';OUT.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[]
def pulse(k,after=30):r.keys=set();r.run(6);r.keys={k};r.run(3);r.keys=set();r.run(after)
def shot(n):r.frame.save(OUT/(n+'.png'))
try:
 r.call('FlagSet',0x828);r.call('FlagSet',0x829);r.call('CreateMon',r.symbols['gPlayerParty'],150,60,20,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');base=r.snapshot()
 pulse(3,120);order=list(r.read(r.symbols['sStartMenuOrder'],r.read(r.symbols['sNumStartMenuItems'],1)[0]));target=order.index(1)
 for _ in range(target):pulse(5,20)
 pulse(8,300);shot('enma-menu-equipe')
 sid=r.read(r.u32(r.symbols['sPartyMenuBoxes'])+9,1)[0];sp=r.symbols['gSprites']+68*sid;attr=int.from_bytes(r.read(sp+4,2),'little');vram=0x06010000+(attr&1023)*32;source=r.u32(r.symbols['gMonIconTable']+4*150);expected=[r.read(source,512),r.read(source+512,512)];seen=set()
 palindex=r.read(r.symbols['gMonIconPaletteIndices']+150,1)[0];pal=r.u32(r.symbols['gMonIconPaletteTable']+8*palindex);assert r.read(r.symbols['gPlttBufferUnfaded']+512+(attr>>12)*32,32)==r.read(pal,32)
 for _ in range(60):
  r.run();blob=r.read(vram,512);assert blob in expected;seen.add(expected.index(blob))
 assert seen;rows.append(dict(test='Enma party icon native tiles and original shared palette',stored_frames_identical=expected[0]==expected[1],native_frames_observed=sorted(seen),passed=True))
 r.restore(base);strong_party(r);r.call('FlagSet',C['FLAG_ARGENTA_MORLEONE_DONE']);warp(r,*MAPS['PewterCity_Gym'],4,4)
 oid=r.call('GetObjectEventIdByLocalIdAndMap',1,*reversed(MAPS['PewterCity_Gym']));r.write(r.symbols['gSelectedObjectEvent'],bytes([oid]));r.write(r.symbols['gSpecialVar_LastTalked'],b'\x01\0');r.call('ScriptContext_SetupScript',r.symbols['PewterCity_Gym_EventScript_Brock'])
 old=r.read(r.symbols['PewterCity_Gym_Text_BrockIntro'],12);story=r.read(r.symbols['Philosovni_Text_WyattConcern'],12);seenstory=False;seenold=False;movie=[]
 for f in range(6000):
  r.keys={8} if f%20<2 else set();r.run()
  raw=r.read(r.symbols['gStringVar4'],12);seenstory|=raw==story;seenold|=raw==old
  if raw==story and f%20==0 and not movie:shot('wyatt-introduction')
  if f%12==0:movie.append(r.frame.copy())
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
 else:raise AssertionError('Wyatt battle did not start')
 assert seenstory and not seenold,(seenstory,seenold);rows.append(dict(test='Wyatt story intro directly starts native battle without generic second greeting',passed=True))
 movie[0].save(OUT/'wyatt-introduction.gif',save_all=True,append_images=movie[1:],duration=200,loop=0)
 r.restore(base);strong_party(r)
 for name,script in [('CeladonCity_PokemonCenter_1F','CeladonCity_PokemonCenter_1F_EventScript_CooltrainerF'),('PewterCity_PokemonCenter_1F','PewterCity_PokemonCenter_1F_EventScript_BenchMan')]:
  warp(r,*MAPS[name],4,6)
  if script not in r.symbols:continue
  r.call('ScriptContext_SetupScript',r.symbols[script]);r.run(150);shot(name+'-francais');rows.append(dict(test='Native Centre dialogue',script=script,passed=True))
  for f in range(300):r.keys={8} if f%20<2 else set();r.run()
 # A direct native Fly bird sprite fixture checks its own OAM/palette allocation.
 r.restore(base);warp(r,*MAPS['PalletTown'],10,10);sid=r.call('CreateFlyBirdSprite');assert sid<64
 sp=r.symbols['gSprites']+68*sid;bank=int.from_bytes(r.read(sp+4,2),'little')>>12;assert bank!=0
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_PlayerUnused'],32)
 rows.append(dict(test='Native Fly bird uses independent original mount palette',bank=bank,passed=True))
finally:
 (OUT/'TEST_MGBA.json').write_text(json.dumps(dict(scope='Native UI/events with explicit party/warp/script fixtures; not full adventure',rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n');r.close()
print('PASS',len(rows))

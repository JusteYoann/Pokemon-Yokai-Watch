#!/usr/bin/env python3
"""Private native map routing, Katie loops/fanfare and unassigned Zombie one-shot."""
import hashlib,json,os
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import MAPS,C,warp
P=ROOT/'QA_RECETTE_FINALE/ARGENTA_MORLEONE/musiques';P.mkdir(exist_ok=True)
r=new_game();rows=[];passed=False

def channel(n):
 for i in range(5):
  p=r.symbols['gSoundInfo']+80+64*i
  if r.u32(p+36)==r.symbols[f'yokai_wave_{n:02d}'] and r.read(p,1)[0]&0x83:return p

def header(n):assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{n:02d}'] and channel(n),n
try:
 # Actual door entry: outside house -> front door -> rival's house.
 warp(r,*MAPS['PalletTown'],15,8);header(7);r.keys={4};r.run(20);r.keys=set();r.run(600)
 assert tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))==MAPS['PalletTown_RivalsHouse'];header(8);r.frame.save(P/'maison-matt.png')
 prev=r.u32(channel(8)+40);wraps=[]
 for f in range(35000):
  r.run();p=channel(8);assert p,'Katie stopped';now=r.u32(p+40)
  if now<prev:wraps.append(f)
  prev=now
  if len(wraps)==3:break
 assert len(wraps)==3;rows.append(dict(test='Real Matt house door, Katie three native wraps without restart',wrap_frames=wraps,passed=True))
 r.call('m4aSongNumStart',354);r.run(120);pos=r.u32(channel(8)+40);r.call('PlayFanfare',258)
 for f in range(1800):
  r.run()
  if f>120 and r.call('IsFanfareTaskInactive'):break
 else:raise AssertionError('Fanfare timeout')
 r.run(30);header(8);assert r.u32(channel(8)+40)>=pos
 r.call('PlaySE',5);r.call('PlayCry_Normal',1,0);r.run(180);header(8)
 rows.append(dict(test='Katie resumes after native item fanfare; SE and cry retain BGM',passed=True))
 for name,x,y,n in [('PalletTown_PlayersHouse_1F',4,7,7),('LavenderTown',10,12,23),('PokemonTower_1F',5,10,4),('IndigoPlateau_PokemonCenter_1F',11,15,23)]:
  warp(r,*MAPS[name],x,y);header(n);rows.append(dict(map=name,slot=n,passed=True))
 r.call('FlagClear',C['FLAG_HIDE_SILPH_ROCKETS']);warp(r,*MAPS['SilphCo_1F'],10,15);header(11)
 r.call('FlagSet',C['FLAG_HIDE_SILPH_ROCKETS']);warp(r,*MAPS['SilphCo_1F'],10,15);header(22)
 rows.append(dict(test='Silph Bada-Bing occupied; Uptown after liberation unchanged',passed=True))
 r.call('m4aMPlayAllStop');r.call('m4aSongNumStart',360);r.run(30);header(14)
 for f in range(6500):
  r.run()
  if channel(14) is None:break
 else:raise AssertionError('Unassigned full-source Zombie never ended')
 r.run(180);assert channel(14) is None
 rows.append(dict(test='Zombie standalone source-only playback, native end and no forced restart; not mapped anywhere',ending_frames=f,passed=True))
 passed=True
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=rows),indent=2)+'\n')
print('MUSIC PASS')

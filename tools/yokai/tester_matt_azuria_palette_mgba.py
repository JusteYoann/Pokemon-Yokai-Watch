#!/usr/bin/env python3
"""Targeted mGBA palette regression; explicit NPC-order/party/map fixtures.
This is separate from the paused natural-player campaign. No battle result is forced.
"""
import os,json,re,hashlib
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
p=Path(os.environ.get('MATT_REPORT',str(ROOT/'docs/matt-azuria-palette-20261024/apres')));p.mkdir(parents=True,exist_ok=True)
r=new_game(int(os.environ.get('MATT_GENDER','0')));rev={v|1:k for k,v in r.symbols.items()}
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
const={k:int(v,0) for k,v in re.findall(r'^#define\s+((?:FLAG|VAR)_\w+)\s+(0x[0-9a-fA-F]+|\d+)\b','\n'.join((ROOT/'include/constants'/f).read_text() for f in ('flags.h','vars.h')),re.M)}
rows=[]
def sample(name):
 for i in range(16):
  a=r.read(r.symbols['gObjectEvents']+36*i,36)
  if a[0]&1 and a[8]==8:
   spr=r.symbols['gSprites']+68*a[4];slot=(r.read(spr+5,1)[0]>>4)
   pal=r.read(r.symbols['gPlttBufferUnfaded']+2*(256+slot*16),32);expected=r.read(r.symbols['gObjectEventPal_Matt'],32)
   row=dict(stage=name,object=i,slot=slot,actual=pal.hex(),expected=expected.hex(),matches=pal==expected);rows.append(row);r.frame.save(p/(name+'.png'));print(row,flush=True);return
 raise AssertionError('Matt missing')
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],150,100,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],332,0)
 r.call('VarSet',const['VAR_STARTER_MON'],0);r.call('VarSet',const['VAR_MAP_SCENE_CERULEAN_CITY_RIVAL'],0)
 r.call('FlagSet',const['FLAG_HIDE_CERULEAN_ROCKET'])
 g,n=maps['CeruleanCity'];r.call('SetWarpDestination',g,n,255,int(os.environ.get('MATT_X','22')),7);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 r.keys={4};r.run(16);r.keys=set();r.run(90);sample('avant-combat')
 r.call('FlagClear',const['FLAG_HIDE_CERULEAN_ROCKET']);r.call('TrySpawnObjectEvent',2,n,g);r.run(1);sample('apres-apparition-mafiamille')
 started=False
 for f in range(60000):
  cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['BattleMainCB2']|1:started=True
  if started and cb==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gBattleOutcome'],1)==b'\1':
   r.keys=set();r.run(120);sample('apres-combat');break
  r.keys={8} if f%16<3 else set();r.run()
 else:raise AssertionError(('No victory',rev.get(cb),r.read(r.symbols['gBattleOutcome'],1)))
 # Keep post-battle conversation visible; native overworld continues for 180 frames.
 r.keys=set();r.run(180);sample('dialogue-apres-combat')
 r.keys={10};r.run(8);r.keys=set();r.run(90);r.keys={0};r.run(8);r.keys=set();r.run(180);sample('apres-aide')
 (p/'TEST.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),gender=int(os.environ.get('MATT_GENDER','0')),entry_x=int(os.environ.get('MATT_X','22')),fixture='New game, prepared level100 team, warp to Azuria; native trigger and actual battle by controller. Mafiamille actor explicitly spawned after Matt to exercise the opposite allocation order; independent from player campaign.',rows=rows),indent=2)+'\n')
 assert all(row['matches'] for row in rows),rows
 # Both actors must retain their own palette after returning from battle.
 for i in range(16):
  actor=r.read(r.symbols['gObjectEvents']+36*i,36)
  if actor[0]&1 and actor[8]==2:
   sprite=r.symbols['gSprites']+68*actor[4];bank=r.read(sprite+5,1)[0]>>4
   assert bank!=rows[-1]['slot']
   assert r.read(r.symbols['gPlttBufferUnfaded']+2*(256+bank*16),32)==r.read(r.symbols['gObjectEventPal_YokaiDonMorleoneGroup'],32)
   break
 else:raise AssertionError('Mafiamille actor missing')
 print('PASS',os.environ.get('MATT_GENDER','0'),os.environ.get('MATT_X','22'),flush=True)
finally:r.frame.save(p/'dernier.png');r.close()

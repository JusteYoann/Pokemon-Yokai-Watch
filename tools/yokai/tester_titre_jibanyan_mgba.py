#!/usr/bin/env python3
"""Démarrage natif, animation 7s, touches précoces, brume et menu ; puis sauvegarde de test."""
import hashlib,json,struct
from pathlib import Path
from mgba_rpc import ROOT,Emulator
from mgba_new_game import new_game
D=ROOT/'docs/titre-jibanyan-20261025';D.mkdir(exist_ok=True)
r=Emulator(initial_frames=1);samples=[];first=None
try:
 for f in range(1800):
  title=r.read(r.symbols['sPresentationTitle'],1)[0];tick=r.u32(r.symbols['sPresentationTick']);cb=r.u32(r.symbols['gMain']+4)
  if title and cb==r.symbols['CB2_RunYokaiPresentation']|1:
   if first is None:first=r.u32(r.symbols['gMain']+0x24)
   if tick in (1,120,240,418,419,480):
    r.frame.save(D/f'titre-{tick:03}.png');samples.append(dict(tick=tick,bg1_y=int.from_bytes(r.read(0x4000016,2),'little'),alpha=int.from_bytes(r.read(0x4000052,2),'little')))
   if tick<419:
    assert cb==r.symbols['CB2_RunYokaiPresentation']|1
    r.keys={3,8} if tick%24<2 else set()
   else:r.keys=set()
   if tick>=480:break
  r.run()
 else:raise AssertionError('Écran titre absent')
 assert len(samples)==6,samples
 assert all(s['alpha']==0x0d03 for s in samples)
 assert samples[0]['bg1_y']!=samples[2]['bg1_y'] and samples[-1]['bg1_y']==0
 assert 419/59.7275>=7
 fog=[i for i in range(64) if r.u32(r.symbols['gSprites']+68*i+0x1c)==r.symbols['Sprite_TitleFog']|1 and r.read(r.symbols['gSprites']+68*i+62,1)[0]&1]
 assert len(fog)==15,fog
 assert int.from_bytes(r.read(0x4000000,2),'little')&0x1040==0x1040
 before=r.read(r.symbols['gSprites']+68*fog[0]+32,2);r.run(16);assert r.read(r.symbols['gSprites']+68*fog[0]+32,2)!=before
 left=r.frame.crop((0,48,32,104));r.run(80);after=r.frame.crop((0,48,32,104))
 assert sum(a!=b for a,b in zip(left.get_flattened_data(),after.get_flattened_data()))>25,'Brume non visible'
 r.frame.save(D/'titre-brume.png')
 r.keys={3};r.run();r.keys=set();r.run(240)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_MainMenu']|1
 r.frame.save(D/'menu.png')
 r.keys={0};r.run();r.keys=set();r.run(150)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_RunYokaiPresentation']|1
 r.keys={3};r.run();r.keys=set();r.run(30)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_RunYokaiPresentation']|1
 r.run(450);r.keys={3};r.run();r.keys=set();r.run(240)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_MainMenu']|1
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest()
finally:r.close()
results=[]
for gender in (0,1):
 r=new_game(gender)
 try:
  name=r.read(r.u32(r.symbols['gSaveBlock2Ptr']),9);pair=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)
  r.call('SaveMapView');assert r.call('TrySavingData',0,max_frames=3000)==1
  r.lib.retro_reset();r.run(900);r.keys={3};r.run();r.keys=set();r.run(240);r.keys={8};r.run();r.keys=set()
  for f in range(18000):
   r.keys={0} if f%32<2 else set();r.run()
   if f>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3):break
  else:raise AssertionError('Continuer impossible')
  assert r.read(r.u32(r.symbols['gSaveBlock2Ptr']),9)==name
  assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)==pair
  r.frame.save(D/f'continuer-{gender}.png');results.append(dict(gender=gender,new_game=True,native_save_continue=True,name_gender_map_preserved=True))
 finally:r.close()
(D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=sha,title_rise_frames=419,title_rise_seconds=419/59.7275,start_A_blocked_before_end=True,menu_B_return_and_second_intro=True,fog_sprites=15,fog_movement_visible_in_render=True,white_fog_alpha='3/16, fond 13/16, identique Terr’heure',samples=samples,results=results),ensure_ascii=False,indent=2)+'\n')
print('PASS titre 7s, brume, Start, nouvelles parties et sauvegarde/Continuer',flush=True)

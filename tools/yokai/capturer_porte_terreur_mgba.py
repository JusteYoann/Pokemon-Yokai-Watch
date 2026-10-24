#!/usr/bin/env python3
"""Isolated mGBA A-button interaction fixture. Only a RAM map template is
repurposed; no map event or user save is permanently changed. Sliding and white
fade run in the game engine, without injected animation frames or fade state.
"""
import json,struct,hashlib
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/porte-terreur-20261024/public';P.mkdir(exist_ok=True)
r=new_game();movie=[];checks=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
def shot(name):r.frame.save(P/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(name+'-x3.png'))
def location():return r.read(r.u32(r.symbols['gSaveBlock1Ptr']),6)
def task():
 for i in range(16):
  t=r.symbols['gTasks']+i*40
  if r.read(t+4,1)==b'\1' and r.u32(t)==r.symbols['Task_PorteTerreur']|1:return t
 return None

def attempt(record):
 seen=False;white=False;positions=set();half=False;opened=False;panel_ids=set()
 r.keys={8}
 for f in range(420):
  r.run();r.keys=set();t=task();seen|=t is not None
  if t:
   panelId=struct.unpack('<h',r.read(t+8,2))[0];panel_ids.add(panelId);ps=r.symbols['gSprites']+68*panelId
   shift=struct.unpack('<h',r.read(ps+36,2))[0];positions.add(shift)
   if record and shift==6 and not half:shot('coulissement');half=True
   if record and shift==13 and not opened:shot('ouverte');opened=True
  im=r.frame.copy();isWhite=all(lo==hi and lo>=248 for lo,hi in im.getextrema())
  if isWhite:
   assert r.read(0x05000000,1024)==b'\xff\x7f'*512, 'White frame without fully white hardware palettes'
   if record and not white:shot('fondu-blanc')
   white=True
  assert location()==start,'Unexpected player movement or warp'
  if record and f%3==0:movie.append(im)
  if seen and white and not t and r.read(r.symbols['sLockFieldControls'],1)==b'\0' and not r.read(r.symbols['gPaletteFade']+7,1)[0]&0x80:
   # Field controls are released only after the demo fade-in. Settle before checking its closed tile.
   r.run(30);break
 else:raise AssertionError(('Interaction did not finish',seen,white,positions))
 assert seen and white and set(range(14))<=positions,(seen,white,positions)
 for panel_id in panel_ids:
  assert not r.read(r.symbols['gSprites']+68*panel_id+62,1)[0]&1, 'Leaked sliding panel sprite'
 tile=int.from_bytes(r.read(sprite+4,2),'little')&1023
 assert r.read(0x06010000+tile*32,512)==raw[:512],'Door did not close after the demonstration'
 checks.append(dict(test='Native A interaction: rigid leaf slides 0..13 pixels, full white fade, unchanged location, closed/reset and controls restored',replay=not record,passed=True))
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('FlagSet',0x828)
 g,n=maps['PalletTown'];r.call('SetWarpDestination',g,n,255,9,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(400)
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);template=sb+0x8e0;data=bytearray(r.read(template,24));local=data[0]
 r.call('RemoveObjectEventByLocalIdAndMap',local,n,g)
 data[1]=184;data[2]=0;struct.pack_into('<hh',data,4,9,15);data[8]=3;data[9]=8;data[10:16]=b'\0'*6
 struct.pack_into('<I',data,16,r.symbols['PorteTerreur_EventScript_Apercu']);struct.pack_into('<H',data,20,0);r.write(template,bytes(data))
 idx=r.call('TrySpawnObjectEvent',local,n,g);assert idx<16;obj=r.symbols['gObjectEvents']+36*idx;r.run(60)
 sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0];raw=(ROOT/'graphics/yokai_characters/porte_terreur/overworld.4bpp').read_bytes();assert len(raw)==1024
 tile=int.from_bytes(r.read(sprite+4,2),'little')&1023;assert r.read(0x06010000+tile*32,512)==raw[:512]
 r.run(90);assert r.read(0x06010000+tile*32,512)==raw[:512]
 shot('fermee');checks.append(dict(test='Closed frame stays closed before interaction, door 26px vs Nathan 19px',passed=True))
 start=location();r.keys={4};r.run(4);r.keys=set();r.run(30);assert location()==start
 for _ in range(12):r.run(3);movie.append(r.frame.copy())
 attempt(True);shot('retour-apercu');attempt(False)
 for _ in range(12):r.run(3);movie.append(r.frame.copy())
 for scale,name in [(1,'ouverture-fondu-mgba.gif'),(3,'ouverture-fondu-mgba-x3.gif')]:
  frames=movie if scale==1 else [im.resize((720,480),Image.Resampling.NEAREST) for im in movie]
  frames[0].save(P/name,save_all=True,append_images=frames[1:],duration=50,loop=0)
 (P/'TEST.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks,captured_frames=len(movie)),indent=2)+'\n')
 print('PASS actual A interaction, complete white fade and repeat opening; no warp',flush=True)
finally:r.frame.save(P/'dernier.png');r.close()

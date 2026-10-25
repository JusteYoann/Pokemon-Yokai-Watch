#!/usr/bin/env python3
"""Remplace uniquement le souvenir de traversée en Surf par une vraie capture Terr’heure."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageOps
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/postgame-quetes-20261025/credits';P.mkdir(parents=True,exist_ok=True);rows=[]
for gender,label in enumerate(('garcon','fille')):
 r=new_game(gender=gender)
 try:
  r.call('CreateMon',r.symbols['gPlayerParty'],150,60,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96)
  groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());g=groups['group_order'].index('gMapGroup_Dungeons');n=groups['gMapGroup_Dungeons'].index('RockTunnel_1F')
  r.call('SetWarpDestination',g,n,255,44,9);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(300)
  r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep');th=r.symbols['sTh']
  for f in range(2400):
   r.keys={8} if f%24<2 else set();r.run()
   if r.read(th+176,1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]:break
  else:raise AssertionError('Intro absente')
  r.keys=set();r.call('LockPlayerFieldControls')
  actors={r.read(r.symbols['gObjectEvents']+36*i+8,1)[0]:r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1}
  import struct
  px,py=struct.unpack('<hh',r.read(actors[255]+16,4));oni=actors[230]
  x,y=next((px+dx,py+dy) for dx,dy in ((-3,0),(3,0),(0,-3),(0,3)) if not r.call('MapGridGetCollisionAt',px+dx,py+dy))
  r.call('MoveObjectEventToMapCoords',oni,x,y);r.call('ObjectEventTurn',oni,1);r.run(30)
  out=P/(label+'-terreur-native.png');r.frame.save(out)
  slide=json.loads((ROOT/'data/yokai/credits_storyboard.json').read_text())['slides'][17]
  photo=ImageOps.fit(r.frame.convert('RGB'),(slide['width'],slide['height']),method=Image.Resampling.NEAREST).quantize(colors=223,dither=Image.Dither.NONE)
  indexed=Image.new('P',photo.size);indexed.putpalette([0,0,0]+photo.getpalette()[:669]+[0]*96);indexed.putdata([i+1 for i in photo.getdata()]);indexed.save(ROOT/f'graphics/yokai_credits/{label}-17.png')
  rows.append({'gender':label,'capture':str(out.relative_to(ROOT)),'rom_source_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':'Situation et cadrage Oni préparés dans mGBA; image native, aucun montage de sprites.'})
 finally:r.close()
replacements={'17':{'title':'Terr’heure dans les grottes','replaces':'Surf sur l’océan','captures':{v['gender']:v['capture'] for v in rows}}}
(ROOT/'data/yokai/credits_replacements.json').write_text(json.dumps(replacements,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'data/yokai/credits_storyboard.json';j=json.loads(p.read_text());j['slides'][17]['title']='Terr’heure dans les grottes';j['slides'][17]['replacement_source']='data/yokai/credits_replacements.json';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
(P/'PROVENANCE.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('PASS souvenir Surf remplacé par Terr’heure, garçon et fille, durée et mise en page conservées')

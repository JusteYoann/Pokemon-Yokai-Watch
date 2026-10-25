#!/usr/bin/env python3
"""Recapture les souvenirs Terr’heure et Yopple sur des cases praticables.
Cadrages préparés dans mGBA, aucune reconstruction/montage des personnages.
"""
import json,hashlib,struct
from pathlib import Path
from PIL import Image,ImageOps
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C,MAPS,warp
P=ROOT/'docs/cinematiques-collisions-20261025/credits';P.mkdir(exist_ok=True);rows=[];board=json.loads((ROOT/'data/yokai/credits_storyboard.json').read_text())
def grid(r):
 w,h,p=struct.unpack('<III',r.read(r.symbols['VMap'],12));v=struct.unpack('<'+'H'*(w*h),r.read(p,2*w*h));return lambda x,y:0<=x+7<w and 0<=y+7<h and not(v[(y+7)*w+x+7]>>10&3),w-15,h-14
def actors(r):return {b[8]:r.symbols['gObjectEvents']+36*i for i in range(16) if (b:=r.read(r.symbols['gObjectEvents']+36*i,36))[0]&1}
def save(r,label,index,extra):
 out=P/f'{label}-{index:02}-native.png';r.frame.save(out);s=board['slides'][index];photo=ImageOps.fit(r.frame.convert('RGB'),(s['width'],s['height']),method=Image.Resampling.NEAREST).quantize(colors=223,dither=Image.Dither.NONE);im=Image.new('P',photo.size);im.putpalette([0,0,0]+photo.getpalette()[:669]+[0]*96);im.putdata([v+1 for v in photo.getdata()]);im.save(ROOT/f'graphics/yokai_credits/{label}-{index:02}.png');rows.append({'gender':label,'slide':index,'capture':str(out.relative_to(ROOT)),'rom_source_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),**extra});print('PASS capture',label,index,extra,flush=True)
for gender,label in enumerate(('garcon','fille')):
 r=new_game(gender)
 try:
  r.call('CreateMon',r.symbols['gPlayerParty'],150,80,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96)
  warp(r,*MAPS['RockTunnel_1F'],44,9);free,w,h=grid(r)
  candidates=[(x,y) for y in range(3,h-2) for x in range(5,w-5) if all(free(x+dx,y+dy) for dx in range(-4,5) for dy in range(-2,2))]
  assert candidates,'Pas de salle assez dégagée';x,y=min(candidates,key=lambda p:abs(p[0]-44)+abs(p[1]-9));warp(r,*MAPS['RockTunnel_1F'],x,y)
  r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep');th=r.symbols['sTh']
  for f in range(2600):
   r.keys={8} if f%24<2 else set();r.run()
   if r.read(th+176,1)==b'\2' and not r.read(r.symbols['sLockFieldControls'],1)[0]:break
  else:raise AssertionError('Terr’heure intro')
  r.keys=set();r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents');a=actors(r)
  for local,dx in [(230,3),(231,-3)]:
   if local in a:r.call('MoveObjectEventToMapCoords',a[local],x+dx+7,y+7);r.call('ObjectEventTurn',a[local],1)
  r.run(8);a=actors(r)
  for local,dx in [(255,0),(230,3),(231,-3)]:
   if local not in a:continue
   ax,ay=struct.unpack('<hh',r.read(a[local]+16,4));assert (ax-7,ay-7)==(x+dx,y)
   assert all(free(ax-7+u,ay-7+v) for u in range(-1,2) for v in range(-2,1))
  save(r,label,17,{'map':'RockTunnel_1F','player':[x,y],'gargaros':[x+3,y],'all_footprints_on_floor':True})
 finally:r.close()
 r=new_game(gender)
 try:
  r.call('CreateMon',r.symbols['gPlayerParty'],150,80,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96);r.call('FlagClear',C['FLAG_HIDE_SILPH_ROCKETS'])
  warp(r,*MAPS['SilphCo_3F'],6,12);free,w,h=grid(r);a=actors(r);occupied={tuple(v-7 for v in struct.unpack('<hh',r.read(p+16,4))) for local,p in a.items() if local!=255}
  candidates=[(x,y) for y in range(2,h-2) for x in range(2,w-2) if (x,y) not in occupied and all(free(x+u,y+v) for u in range(-1,2) for v in range(-1,1))]
  x,y=min(candidates,key=lambda p:abs(p[0]-25)+abs(p[1]-11));warp(r,*MAPS['SilphCo_3F'],x,y);r.keys=set();r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents');r.run(4);free,_,_=grid(r);assert free(x,y) and free(x,y-1)
  save(r,label,15,{'map':'SilphCo_3F','player':[x,y],'player_on_floor':True})
 finally:r.close()
for gender,label in enumerate(('garcon','fille')):
 for index,name,y in [(26,'PokemonLeague_LoreleisRoom',7),(27,'PokemonLeague_LancesRoom',10)]:
  r=new_game(gender)
  try:
   r.call('CreateMon',r.symbols['gPlayerParty'],150,80,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('VarSet',C['VAR_MAP_SCENE_POKEMON_LEAGUE'],4)
   warp(r,*MAPS[name],6,y);r.keys=set();r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents');a=actors(r)
   r.call('ObjectEventTurn',a[255],2);r.call('ObjectEventTurn',a[1],1);r.run(4)
   px,py=struct.unpack('<hh',r.read(a[255]+16,4));nx,ny=struct.unpack('<hh',r.read(a[1]+16,4));assert px==nx and py-ny==2
   assert r.read(a[255]+24,1)[0]&15==2 and r.read(a[1]+24,1)[0]&15==1
   free,_,_=grid(r);assert free(px-7,py-7)
   save(r,label,index,{'map':name,'player':[px-7,py-7],'opponent':[nx-7,ny-7],'both_facing_each_other':True,'player_on_floor':True})
  finally:r.close()
p=ROOT/'data/yokai/credits_replacements.json';repl=json.loads(p.read_text());
for index in (15,17,26,27):
 repl[str(index)]={'title':board['slides'][index]['title'],'replaces':repl.get(str(index),{}).get('replaces',board['slides'][index]['title']),'captures':{label:next(row['capture'] for row in rows if row['gender']==label and row['slide']==index) for label in ('garcon','fille')}};board['slides'][index]['replacement_source']='data/yokai/credits_replacements.json'
p.write_text(json.dumps(repl,ensure_ascii=False,indent=2)+'\n');(ROOT/'data/yokai/credits_storyboard.json').write_text(json.dumps(board,ensure_ascii=False,indent=2)+'\n');(P/'PROVENANCE.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')

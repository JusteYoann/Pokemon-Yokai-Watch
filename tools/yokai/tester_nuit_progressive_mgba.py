#!/usr/bin/env python3
"""mGBA visual fixtures: approach palettes, controller crossings and menu isolation.
Prepared party, completed intro/Badge4, trainer flags and point warps are fixtures;
walking crosses the real connections. No source palette or battle result injected.
"""
import os,json,re,struct,hashlib,subprocess
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'docs/lavanville-nuit-progressive-20261024'/os.environ.get('NUIT_MODE','prive');P.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])};names={v:k for k,v in maps.items()}

def loc():
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);return names[tuple(r.read(sb+4,2))],struct.unpack('<hh',r.read(sb,4))
def pulse(k,n=30):r.keys=set();r.run(4);r.keys={k};r.run(4);r.keys=set();r.run(n)
def warp(name,x,y):
 g,n=maps[name];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(400)
 assert loc()==(name,(x,y)),loc()

def expected(raw,strength):
 out=[]
 for c in struct.unpack('<192H',raw[:384]):
  red=c&31;green=(c>>5)&31;blue=(c>>10)&31;light=max(red,green,blue)
  out.append((red*(1024-14*strength)//1024)|(green*(1024-14*strength)//1024<<5)|((blue*(1024-8*strength)+light*4*strength)//1024<<10))
 return struct.pack('<192H',*out)+raw[384:]

def check(label,strength,photo=False):
 assert r.call('LavanvilleNightStrength')==strength,(label,loc())
 r.run(2);source=r.read(r.symbols['gPlttBufferFaded'],1024);hardware=r.read(0x05000000,1024)
 assert hardware==expected(source,strength),(label,'hardware palette mismatch')
 if photo:r.frame.save(P/(label+'.png'))
 rows.append(dict(test=label,location=loc(),strength=strength,passed=True))

try:
 r.call('CreateMon',r.symbols['gPlayerParty'],150,100,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 for flag in (0x322,0x823,0x828,0x829):r.call('FlagSet',flag)
 r.call('VarSet',0x40f3,1);r.call('VarSet',0x4020,10000)
 opponents={k:int(v) for k,v in re.findall(r'^#define\s+(TRAINER_\w+)\s+(\d+)\b',(ROOT/'include/constants/opponents.h').read_text(),re.M)}
 for name in ('Route8','Route10','Route12'):
  for trainer in set(re.findall(r'trainerbattle\w*\s+(TRAINER_\w+)',(ROOT/f'data/maps/{name}/scripts.inc').read_text())):
   r.call('FlagSet',0x500+opponents[trainer])
 samples={
  'Route8':[(39,12,0),(47,7,8),(55,12,16),(63,12,24),(71,10,32)],
  'Route10':[(8,47,0),(8,58,11),(17,64,17),(11,72,25),(11,79,32)],
  'Route12':[(11,32,0),(11,24,8),(11,16,16),(11,8,24),(11,0,32)]}
 for name,points in samples.items():
  for x,y,s in points:warp(name,x,y);check(name+'-'+str(s).zfill(2),s,True);assert not r.call('IsLavanvilleNight')
 # Each real connection is crossed on foot, and immediately crossed back.
 for name,x,y,key,back in [('Route8',64,10,7,6),('Route10',11,72,5,4),('Route12',11,7,4,5)]:
  warp(name,x,y);movie=[];strengths=[]
  for step in range(9):
   mapname,(px,py)=loc();s=32 if mapname=='LavenderTown' else (32-max(0,71-px) if name=='Route8' else 32-max(0,79-py) if name=='Route10' else 32-max(0,py))
   check(name+'-walk-'+str(step),s);strengths.append(s);movie.append(r.frame.copy())
   if mapname=='LavenderTown':break
   pulse(key)
  assert loc()[0]=='LavenderTown',loc();assert strengths[-1]==32 and strengths[-2]>=31,strengths
  assert all(a<=b for a,b in zip(strengths,strengths[1:])),strengths
  r.run(300);check(name+'-ville',32,True)
  for attempt in range(3):
   pulse(back,90)
   if loc()[0]==name:break
  assert loc()[0]==name,(name,loc())
  _,(px,py)=loc();back_strength=32-max(0,71-px) if name=='Route8' else 32-max(0,79-py) if name=='Route10' else 32-max(0,py)
  assert 0<=32-back_strength<=2;check(name+'-retour',back_strength)
  movie[0].save(P/(name+'-marche.gif'),save_all=True,append_images=movie[1:],duration=170,loop=0)
 # Stable stop and reversible positioning: the transform never accumulates.
 warp('Route8',55,12);check('arret-debut',16)
 unfaded=r.read(r.symbols['gPlttBufferUnfaded'],1024);r.run(600);check('arret-dix-secondes',16)
 assert unfaded==r.read(r.symbols['gPlttBufferUnfaded'],1024)
 # Party UI uses its own palette; returning restores the position's tint.
 pulse(3,90);order=list(r.read(r.symbols['sStartMenuOrder'],r.read(r.symbols['sNumStartMenuItems'],1)[0]));target=order.index(1)
 for _ in range(12):
  if r.read(r.symbols['sStartMenuCursorPos'],1)[0]==target:break
  pulse(5,20)
 pulse(8,180);assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_UpdatePartyMenu']|1
 assert r.read(0x05000000,1024)==r.read(r.symbols['gPlttBufferFaded'],1024)
 r.frame.save(P/'menu-equipe.png');pulse(0,180);pulse(0,90);check('retour-menu',16)
 for name,x,y in [('LavenderTown_PokemonCenter_1F',7,8),('Route9',30,8),('Route10',11,20)]:
  warp(name,x,y);check(name+'-jour',0,True)
 # Existing town night is exactly the previous transform, not a new look.
 warp('LavenderTown',14,9);check('ville-nuit-conservee',32,True)
 print('PASS',len(rows),'native hardware palette/connection checks',flush=True)
 (P/'TEST.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),cases=rows),indent=2)+'\n')
finally:r.frame.save(P/'dernier.png');r.close()

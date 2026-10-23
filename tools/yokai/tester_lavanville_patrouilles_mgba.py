#!/usr/bin/env python3
"""Observe native patrols, then find and replay controller-only avoidance routes.
Search may restore temporary emulator states after failed attempts. Each accepted
route is subsequently replayed uninterrupted from its starting state, without RAM
position/graphics/sight patches. Static reachability is reported separately.
"""
from pathlib import Path
import sys,struct,json,os,collections,hashlib
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,warp,C
r=new_game();mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
P=ROOT/'docs/lavanville-zombie-night/finalisation'/mode;P.mkdir(parents=True,exist_ok=True)
passed=False;rows=[];observed={n:set() for n in range(1,5)};movie=[]
b=struct.unpack('<480H',(ROOT/'data/layouts/LavenderTown/map.bin').read_bytes());free={(x,y) for y in range(20) for x in range(24) if not (b[y*24+x]>>10)&3};warps={(w['x'],w['y']) for w in json.loads((ROOT/'data/maps/LavenderTown/map.json').read_text())['warp_events']}
def objects():
 out={}
 for i in range(16):
  d=r.read(r.symbols['gObjectEvents']+36*i,36)
  if d[0]&1:
   x,y=struct.unpack('<hh',d[16:20]);px,py=struct.unpack('<hh',d[20:24]);out[d[8]]=dict(xy=(x-7,y-7),previous=(px-7,py-7),direction=d[24]&15,graphics=d[5])
 return out
def unlocked():return r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def step_path(start,goal,blocked):
 q=collections.deque([start]);seen={start:None}
 while q and goal not in seen:
  x,y=q.popleft()
  for n in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if n in free and n not in blocked and n not in seen and n not in warps:seen[n]=(x,y);q.append(n)
 if goal not in seen:return None
 out=[goal]
 while out[-1]!=start:out.append(seen[out[-1]])
 return out[::-1]
def blocked(o):
 out=set()
 for lid,v in o.items():
  if lid==255:continue
  out.update([v['xy'],v['previous']]);dx,dy={1:(0,1),2:(0,-1),3:(-1,0),4:(1,0)}.get(v['direction'],(0,0));x,y=v['xy']
  for _ in range(2):
   x+=dx;y+=dy
   if (x,y) not in free:break
   out.add((x,y))
 return out
try:
 r.call('FlagSet',0x322);r.call('VarSet',0x40f3,1);warp(r,*MAPS['LavenderTown'],14,9)
 for f in range(2400):
  r.run()
  if f%8==0:
   for lid,v in objects().items():
    if lid in observed:observed[lid].add(v['xy'])
   if f%16==0:movie.append(r.frame.copy())
 assert len(observed[1])==6 and all(y==12 and 12<=x<=16 for x,y in observed[2]),observed
 assert observed[3]=={(17,8)} and len(observed[2])>=4 and len(observed[4])>=2,observed
 assert unlocked()
 movie[0].resize((720,480),Image.Resampling.NEAREST).save(P/'patrouilles.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in movie[1:]],duration=267,loop=0)
 # Reflection bank8 is dedicated to zombies; ordinary green NPC body bank4 stays intact.
 who=r.call('SpawnSpecialObjectEventParameterized',C['OBJ_EVENT_GFX_WOMAN_1'],C['MOVEMENT_TYPE_FACE_DOWN'],202,21,15,3);assert who<16;r.run(8)
 sid=r.read(r.symbols['gObjectEvents']+36*who+4,1)[0];bank=r.read(r.symbols['gSprites']+68*sid+5,1)[0]>>4;assert bank==4
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_NpcGreen'],32)
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*8,32)==r.read(r.symbols['gObjectEventPal_LavenderZombie'],32)
 r.call('RemoveObjectEventByLocalIdAndMap',202,MAPS['LavenderTown'][1],MAPS['LavenderTown'][0])
 for goal in [(18,7),(11,19)]:
  warp(r,*MAPS['LavenderTown'],1,9);r.run(240);assert unlocked();initial=r.snapshot();accepted=None
  for seed in range(12):
   r.restore(initial);r.keys=set();r.run(seed*24);start=r.snapshot();history=[];failures=0
   for iteration in range(500):
    o=objects();pos=o[255]['xy']
    if pos==goal:accepted=(start,history,seed,failures);break
    path=step_path(pos,goal,blocked(o));before=r.snapshot()
    if path and len(path)>1:
     nx,ny=path[1];dx,dy=nx-pos[0],ny-pos[1];key={(1,0):7,(-1,0):6,(0,1):5,(0,-1):4}[dx,dy];r.keys={key}
     for held in range(1,33):
      r.run()
      if objects()[255]['xy']!=pos:break
     r.keys=set();r.run(20);batch=[([key],held),([],20)]
    else:r.keys=set();r.run(8);batch=[([],8)]
    if not unlocked():
     failures+=1;r.restore(before);r.keys=set();r.run(8)
     if not unlocked():break
     history.append(([],8))
    else:history.extend(batch)
   if accepted:break
  assert accepted,('No native avoidance route found',goal)
  start,history,seed,failures=accepted;r.restore(start);frames=[]
  for keys,n in history:
   r.keys=set(keys)
   for f in range(n):
    r.run()
    if f%4==0:frames.append(r.frame.copy())
   assert unlocked(),('Uninterrupted route replay triggered a battle',goal)
  assert objects()[255]['xy']==goal
  label='tour' if goal==(18,7) else 'route12';r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/f'esquive-vers-{label}.png')
  frames[0].resize((720,480),Image.Resampling.NEAREST).save(P/f'esquive-vers-{label}.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in frames[1:]],duration=67,loop=0)
  rows.append(dict(goal=goal,search_seed_offset_frames=seed*24,search_failed_attempts=failures,uninterrupted_replay_frames=sum(n for keys,n in history),battle_triggered=False,controls_only=True));print(rows[-1],flush=True)
 passed=True
 if (P/'patrouilles-diagnostic.png').exists():(P/'patrouilles-diagnostic.png').unlink()
finally:
 if not passed:r.frame.save(P/'patrouilles-diagnostic.png')
 (P/'PATROUILLES_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),observed_positions={str(k):sorted(v) for k,v in observed.items()},ordinary_green_npc_palette_preserved=True,zombie_palette_bank=8,routes=rows,scope=__doc__),indent=2)+'\n');r.close()

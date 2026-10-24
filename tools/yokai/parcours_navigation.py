"""Joypad pathfinding with geometry assistance from the current native map.
No ROM calls, warps, source-map walkability, or flags/items writes.
"""
import collections,json,struct
from pathlib import Path
ROOT=Path('/workspace/artifacts/parcours-joueur-20261024');CACHE=ROOT/'CARTE_VUE.json'
def navigate(r,goal,pulse,max_steps=160):
 cache=json.loads(CACHE.read_text()) if CACHE.exists() else {}
 def pos():
  sb=r.u32(r.symbols['gSaveBlock1Ptr']);return tuple(r.read(sb+4,2)),struct.unpack('<hh',r.read(sb,4))
 initial,_=pos();key=str(initial);data=cache.setdefault(key,dict(tiles={},blocked=[],visits={}));tiles=data['tiles'];blocked=set(data['blocked']);visits=data['visits'];steps=0;reason='limit'
 def k(p):return str(p[0])+','+str(p[1])
 try:
  for _ in range(max_steps):
   if r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1:reason='scene/battle';break
   if r.read(r.symbols['sGlobalScriptContextStatus'],1)!=b'\2' or r.read(r.symbols['sLockFieldControls'],1)!=b'\0':reason='dialogue/event';break
   current,at=pos()
   if current!=initial:reason='map transition';break
   if at==tuple(goal):reason='arrived';break
   w,h,p=struct.unpack('<III',r.read(r.symbols['VMap'],12));width=w-15;height=h-14
   if not data.get('native_geometry_loaded'):
    for yy in range(height):
     row=r.read(p+2*((yy+7)*w+7),width*2)
     for xx in range(width):
      v=int.from_bytes(row[xx*2:xx*2+2],'little');tiles[k((xx,yy))]=not bool(v&0xc00) and (v&1023)!=1023
    data['native_geometry_loaded']=True
   for y in range(at[1]-5,at[1]+6):
    for x in range(at[0]-7,at[0]+8):
     if not(-1<=x<=width and -1<=y<=height):continue
     v=int.from_bytes(r.read(p+2*((y+7)*w+x+7),2),'little');tiles[k((x,y))]=not bool(v&0xc00) and (v&1023)!=1023
   objects=set()
   for i in range(16):
    a=r.read(r.symbols['gObjectEvents']+36*i,36)
    if a[0]&1 and a[8]!=255:
     x,y=struct.unpack('<hh',a[16:20]);x-=7;y-=7
     if abs(x-at[0])<=7 and abs(y-at[1])<=5:objects.add((x,y))
   parents={at:None};dist={at:0};q=collections.deque([at])
   while q:
    a=q.popleft()
    for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:
     b=a[0]+dx,a[1]+dy
     if b in parents or b in objects or not tiles.get(k(b),False) or k(a)+'>'+k(b) in blocked:continue
     parents[b]=a;dist[b]=dist[a]+1;q.append(b)
   target=tuple(goal)
   if target not in parents:
    candidates=[]
    for a in parents:
     if a==at:continue
     gain=sum(k((x,y)) not in tiles for y in range(max(-1,a[1]-5),min(height,a[1]+5)+1) for x in range(max(-1,a[0]-7),min(width,a[0]+7)+1))
     if gain:
      score=abs(a[0]-goal[0])+abs(a[1]-goal[1])+.08*dist[a]-.02*gain+.5*visits.get(k(a),0);candidates.append((score,a))
    if not candidates:reason='no visible frontier/path';break
    target=min(candidates)[1]
   while parents[target]!=at and parents[target] is not None:target=parents[target]
   dx=target[0]-at[0];dy=target[1]-at[1];button={(0,-1):4,(0,1):5,(-1,0):6,(1,0):7}[dx,dy]
   pulse([button],16,12);steps+=1;visits[k(at)]=visits.get(k(at),0)+1
   after,now=pos()
   if after!=initial:reason='map transition';break
   if now==at and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:blocked.add(k(at)+'>'+k(target))
 finally:
  data['blocked']=sorted(blocked);CACHE.write_text(json.dumps(cache,separators=(',',':')))
 return dict(reason=reason,steps=steps,goal=goal)

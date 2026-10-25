"""Observation seule des pieds des sprites visibles pendant les scripts mGBA.
Aucun sprite/coordonnée/collision du jeu n'est modifié par cet observateur.
"""
import struct,json
from pathlib import Path
from mgba_rpc import ROOT
class Observer:
 def __init__(self,r,label):
  self.r=r;self.label=label;self.frames=0;self.collisions={};self.movements=set();self.last={};self.lastmap=None;self.walls={};self.original=r.run;r.run=self.run
  self.out=ROOT/'docs/cinematiques-collisions-20261025';self.out.mkdir(exist_ok=True)
 def run(self,frames=1):
  for _ in range(frames):self.original(1);self.observe()
 def observe(self):
  r=self.r
  if r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1:return
  sb=r.u32(r.symbols['gSaveBlock1Ptr']);mp=tuple(r.read(sb+4,2))
  if mp!=self.lastmap:self.last={};self.lastmap=mp
  if r.read(r.symbols['sLockFieldControls'],1)==b'\0':return
  if r.read(r.symbols['gQuestLogState'],1)[0] in (2,3):return
  sb=r.u32(r.symbols['gSaveBlock1Ptr']);mp=tuple(r.read(sb+4,2));self.frames+=1
  objects=r.read(r.symbols['gObjectEvents'],36*16);sprites=r.read(r.symbols['gSprites'],68*64);actors=[]
  for i in range(16):
   b=objects[i*36:(i+1)*36]
   if not b[0]&1 or b[1]&32 or b[8]==127 or b[4]>=64 or (b[10],b[9])!=mp:continue
   s=sprites[b[4]*68:(b[4]+1)*68]
   if not s[62]&1 or s[62]&4:continue
   x,y,x2,y2=struct.unpack_from('<hhhh',s,32);foot=(x+x2,y+y2-struct.unpack_from('<b',s,41)[0]);xy=struct.unpack_from('<hh',b,16)
   ident=(*mp,b[8]);prev=self.last.get(ident)
   if prev and xy!=prev:
    self.movements.add(ident)
    if abs(prev[0]-xy[0])+abs(prev[1]-xy[1])==1:
     vw,vh,pointer=struct.unpack('<III',r.read(r.symbols['VMap'],12))
     if 0<=xy[0]<vw and 0<=xy[1]<vh:
      tile=int.from_bytes(r.read(pointer+2*(xy[1]*vw+xy[0]),2),'little')
      if (tile>>10)&3:
       key=str((*mp,b[8],*xy))
       if key not in self.walls:self.walls[key]={'map':mp,'actor':b[8],'tile':(xy[0]-7,xy[1]-7),'frame':self.frames,'collision':(tile>>10)&3}

   self.last[ident]=xy;actors.append((b[8],b[11]&15,foot,tuple(v-7 for v in xy),b[5]))
  for i,a in enumerate(actors):
   for b in actors[i+1:]:
    if a[1] and b[1] and a[1]!=b[1]:continue
    dx=abs(a[2][0]-b[2][0]);dy=abs(a[2][1]-b[2][1])
    if dx>=8 or dy>=8:continue
    key=str((*mp,min(a[0],b[0]),max(a[0],b[0]),a[3],b[3]))
    if key not in self.collisions:
     self.collisions[key]={'map':mp,'actors':[a,b],'frames':0,'first_frame':self.frames}
     r.frame.save(self.out/(self.label+'-suspect-'+str(len(self.collisions))+'.png'))
    self.collisions[key]['frames']+=1
 def finish(self):
  self.r.run=self.original
  result={'scenario':self.label,'field_frames_checked':self.frames,'moving_actors':sorted(self.movements),'suspects':list(self.collisions.values()),'blocked_tiles_entered':list(self.walls.values())}
  (self.out/(self.label+'-collisions.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('COLLISIONS',self.label,self.frames,len(self.collisions),flush=True);return result

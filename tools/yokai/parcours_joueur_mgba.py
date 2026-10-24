#!/usr/bin/env python3
"""Persistent mGBA session: joypad inputs only; RAM reads for observation.
Disallows RPC, RAM writes and ROM patches. Battery saves exported as-is.
Every command is hash-chained; resumable snapshots are emulator checkpoints.
"""
import ctypes as C,hashlib,json,os,re,struct,sys,time,subprocess,importlib
from pathlib import Path
from mgba_rpc import Emulator,ROOT
OUT=Path('/workspace/artifacts/parcours-joueur-20261024');OUT.mkdir(parents=True,exist_ok=True)
class Player(Emulator):
 def assemble_stub(self):pass
 def call(self,*a,**k):raise RuntimeError('Native-call injection forbidden in player run')
 def write(self,*a,**k):raise RuntimeError('RAM writes forbidden in player run')
 def w32(self,*a,**k):raise RuntimeError('RAM writes forbidden in player run')
 def run(self,n=1):
  previous=getattr(self,'frames',0)
  keylist=sorted(self.keys)
  if hasattr(self,'segment') and self.segment['keys']!=keylist:self.flush_input()
  if not hasattr(self,'segment'):self.segment=dict(start=previous,frames=0,keys=keylist)
  super().run(n);self.frames=previous+n;self.segment['frames']+=n
 def flush_input(self):
  if hasattr(self,'segment'):
   with (OUT/'ENTREES.jsonl').open('a') as f:f.write(json.dumps(self.segment)+'\n')
   del self.segment
r=Player();rev={int(f[0],16)|1:f[2] for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3};chars={int(m[2],16):m[1] for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M) if len(m[1])==1 and ord(m[1])<0x3000}
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={(i,j):n for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
def decode(b):
 out='';i=0
 while i<len(b):
  c=b[i];i+=1
  if c==255:break
  if c in (250,251,254):out+=' | ';continue
  if c==252:
   if i<len(b):i+=2
   continue
  if c==253:i+=1;continue
  out+=chars.get(c,'')
 return out

def state():
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);loc=None
 if sb:
  group,num=r.read(sb+4,2);loc=dict(map=maps.get((group,num),str((group,num))),xy=struct.unpack('<hh',r.read(sb,4)))
 tasks=[rev.get(r.u32(r.symbols['gTasks']+40*i),hex(r.u32(r.symbols['gTasks']+40*i))) for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\1']
 party=[]
 for i in range(min(6,r.read(r.symbols['gPlayerPartyCount'],1)[0])):
  p=r.symbols['gPlayerParty']+100*i;party.append(dict(name=decode(r.read(p+8,10)),level=r.read(p+84,1)[0],hp=struct.unpack('<HH',r.read(p+86,4))))
 battle=None
 if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
  p=r.symbols['gBattleMons'];moves=struct.unpack('<4H',r.read(p+12,8));pp=r.read(p+36,4)
  battle=dict(displayed=decode(r.read(r.symbols['gDisplayedStringBattle'],300)),outcome=r.read(r.symbols['gBattleOutcome'],1)[0],controller=rev.get(r.u32(r.symbols['gBattlerControllerFuncs']),'?'),moves=[dict(id=m,pp=pp[i],power=r.read(r.symbols['gBattleMoves']+12*m+1,1)[0]) for i,m in enumerate(moves)],move_cursor=r.read(r.symbols['gMoveSelectionCursor'],1)[0],action_cursor=r.read(r.symbols['gActionSelectionCursor'],1)[0])
 save2=r.u32(r.symbols['gSaveBlock2Ptr']);owned=r.read(save2+0x28,19) if save2 else bytes(19)
 captured=[i+1 for i in range(151) if owned[i//8]&(1<<(i%8))]
 return dict(captured=captured,battle=battle,frame=r.frames,location=loc,callback=rev.get(r.u32(r.symbols['gMain']+4),'?'),tasks=tasks,text=decode(r.read(r.symbols['gStringVar4'],400)),party=party)

def pulse(keys,hold=1,after=20):
 r.keys=set();r.run(4);r.keys=set(keys);r.run(hold);r.keys=set();r.run(after)
chain='0'*64
log=OUT/'COMMANDES.jsonl'
if log.exists():
 lines=log.read_text().splitlines();chain=json.loads(lines[-1])['hash'] if lines else chain
if os.environ.get('PLAYER_RESUME')=='1':
 r.flush_input();r.restore((OUT/'courant.state').read_bytes());r.frames=json.loads((OUT/'COURANT.json').read_text())['frame']
 with (OUT/'ENTREES.jsonl').open('a') as f:f.write(json.dumps(dict(resume_at_frame=r.frames,snapshot_sha256=hashlib.sha256((OUT/'courant.state').read_bytes()).hexdigest()))+'\n')
print(json.dumps(dict(ready=True,state=state())),flush=True)
for line in sys.stdin:
 try:
  cmd=json.loads(line);op=cmd['op']
  if op=='new':
   import mgba_new_game
   # Reuse only the controller introduction helper; its native-call guard stays active.
   r.close();mgba_new_game.Emulator=Player;r=mgba_new_game.new_game(cmd.get('gender',0))
  elif op=='press':pulse(cmd.get('keys',[]),cmd.get('hold',1),cmd.get('after',20))
  elif op=='sequence':
   for x in cmd['steps']:pulse(x[0],x[1],x[2])
  elif op=='mash':
   for i in range(cmd.get('frames',600)):
    r.keys=set(cmd.get('keys',[8])) if i%16<3 else set();r.run()
   r.keys=set()
  elif op=='advance':
   for i in range(cmd.get('frames',6000)):
    t=state() if i%8==0 else None
    if t:
     if any('YesNo' in task or 'Multichoice' in task for task in t['tasks']):break
     if t['callback'] not in ('CB2_Overworld','CB2_ReturnToFieldLocal','CB2_ReturnToField','CB2_OverworldBasic'):break
     if any('Shop' in task or 'BuyMenu' in task for task in t['tasks']):break
     if i>8 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and 'Task_DrawFieldMessageBox' not in t['tasks']:break
    r.keys={8} if i%16<3 else set();r.run()
   r.keys=set()
  elif op=='nav':
   from parcours_navigation import navigate
   print(json.dumps(navigate(r,cmd['goal'],pulse,cmd.get('steps',160))),flush=True)
  elif op=='capture_result':
   import parcours_combat;importlib.reload(parcours_combat)
   from parcours_combat import finish_capture
   print(json.dumps(finish_capture(r,state,cmd.get('frames',6000))),flush=True)
  elif op=='throw':
   import parcours_combat;importlib.reload(parcours_combat)
   from parcours_combat import throw_ball
   print(json.dumps(throw_ball(r,pulse,state)),flush=True)
  elif op=='battle':
   import parcours_combat;importlib.reload(parcours_combat)
   parcours_combat.fight(r,state,cmd)
  elif op=='flee':
   import parcours_combat;importlib.reload(parcours_combat)
   print(json.dumps(parcours_combat.flee(r,pulse,state)),flush=True)
  elif op=='travel':
   import parcours_accelere;importlib.reload(parcours_accelere)
   print(json.dumps(parcours_accelere.travel(r,state,pulse,cmd),ensure_ascii=False),flush=True)
  elif op=='save_ui':
   previous=r.u32(r.symbols['gSaveCounter']);pulse([3],1,90)
   order=list(r.read(r.symbols['sStartMenuOrder'],r.read(r.symbols['sNumStartMenuItems'],1)[0]));target=order.index(4)
   for _ in range(12):
    cur=r.read(r.symbols['sStartMenuCursorPos'],1)[0]
    if cur==target:break
    pulse([5],1,16)
   pulse([8],1,120)
   for i in range(1800):
    r.keys={8} if i%20<3 else set();r.run()
    if r.u32(r.symbols['gSaveCounter'])!=previous and i>180:break
   r.keys=set();r.run(600)
   assert r.u32(r.symbols['gSaveCounter'])!=previous,'Native save counter did not advance'
  elif op=='wait':r.keys=set();r.run(cmd.get('frames',60))
  elif op=='export':
   from parcours_sauvegardes import native_battery
   dest=OUT/cmd['name'];dest.mkdir(parents=True,exist_ok=True)
   (dest/'Pokemon_Yokai_Watch_Beta_0.1_FR.sav').write_bytes(native_battery(r.snapshot()))
   r.frame.save(dest/'ecran.png');(dest/'ETAT.json').write_text(json.dumps(state(),ensure_ascii=False,indent=2)+'\n')
  elif op=='resume':
   r.restore((OUT/'courant.state').read_bytes());r.frames=json.loads((OUT/'COURANT.json').read_text())['frame']
  elif op!='state':raise ValueError(op)
  r.flush_input();s=state();r.frame.save(OUT/'courant.png');(OUT/'courant.state').write_bytes(r.snapshot());(OUT/'COURANT.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
  row=dict(previous=chain,command=cmd,state=s);raw=json.dumps(row,ensure_ascii=False,sort_keys=True);chain=hashlib.sha256(raw.encode()).hexdigest();row['hash']=chain
  with log.open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
  print(json.dumps(s if op=='state' else {k:s[k] for k in ('frame','location','captured','party','callback','battle')},ensure_ascii=False),flush=True)
 except Exception as e:print(json.dumps(dict(error=repr(e))),flush=True)

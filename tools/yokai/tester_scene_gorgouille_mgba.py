#!/usr/bin/env python3
"""Parties mGBA isolées : arrivée réelle à 3 cases, capture, sortie et rochers.
Équipe, inventaire et prérequis préparés ; combat et déplacements natifs.
"""
import json,struct,hashlib,subprocess
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
import parcours_navigation as nav
D=ROOT/'docs/gorgouille-alizon-20261025';D.mkdir(exist_ok=True)
nav.ROOT=D;nav.CACHE=Path('/workspace/artifacts/gorgouille-chemin-qa.json')
checks=[]
for mode in ('capture','clear','side','ko'):
 clear=mode in ('clear','side')
 q=QA('TEMP.json');r=q.r
 try:
  q.mon();r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],53,0);q.f(0x82c)
  if mode=='ko':
   for i in range(1,6):r.call('SetMonMoveSlot',q.mon(i,150,100),53,0)
  for flag in (0x335,0x336,0x337,0x33a):q.f(flag)
  r.call('ClearBag');r.call('AddBagItem',1,1);r.write(r.symbols['gBagMenuState']+6,b'\2\0')
  q.warp('MtEmber_Summit',10 if mode=='side' else 8,9);r.run(300);assert 7 not in q.actors()
  def positions():return {k:tuple(v-7 for v in struct.unpack('<hh',r.read(a+16,4))) for k,a in q.actors().items()}
  if clear:
   for local,x,y in ((2,10,11),(3,8,12),(4,7,11),(5,11,9)):
    r.call('MoveObjectEventToMapCoords',q.actors()[local],x+7,y+7)
  before={k:v for k,v in positions().items() if k in (2,3,4,5)}
  w,h,p=struct.unpack('<III',r.read(r.symbols['VMap'],12));grid=struct.unpack('<'+'H'*(w*h),r.read(p,w*h*2));collisions=[];walls=[];pushes=[];last=positions();caught=False;blink=[];first_return=False
  original=r.run
  def observed(n=1):
   global last,caught,first_return
   for _ in range(n):
    original()
    if r.read(r.symbols['gBattleOutcome'],1)==b'\7' or mode=='ko' and r.read(r.symbols['gBattleOutcome'],1)==b'\1':caught=True
    if r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)!=bytes(q.maps['MtEmber_Summit']):continue
    if q.callback() not in ('CB2_Overworld','CB2_ReturnToFieldLocal'):continue
    now=positions();at={}
    for k,(x,y) in now.items():
     if k not in (1,2,3,4,5,7,255):continue
     if (x,y) in at:collisions.append((k,at[x,y],x,y))
     at[x,y]=k
     if grid[(y+7)*w+x+7]&0xc00:walls.append((k,x,y))
     if k in (2,3,4,5) and k in last and last[k]!=(x,y):pushes.append((k,last[k],(x,y)))
    display=int.from_bytes(r.read(0x4000000,2),'little')
    if caught and 1 in now and display&0x1000 and not(display&0x80):
     a=q.actors()[1];sid=r.read(a+4,1)[0];bank=r.read(r.symbols['gSprites']+68*sid+5,1)[0]>>4
     if not(r.read(r.symbols['gSprites']+68*sid+62,1)[0]&4) and any(r.read(r.symbols['gPlttBufferFaded']+512+32*bank,32)):
      blink.append(q.callback())
    last=now
  r.run=observed
  r.keys={4 if mode=='side' else 7};r.run(20);r.keys=set();r.run(90);q.drain(15000)
  assert positions()[255]==(9,9) and positions()[7]==(10,9),positions()
  assert r.read(q.actors()[7]+24,1)[0]&15==2
  assert not collisions and not walls,(collisions,walls)
  if clear:assert before=={k:v for k,v in positions().items() if k in before},pushes
  r.frame.save(D/('arrivee-'+('passage-libre' if clear else 'rochers')+'.png'))
  if clear:
   r.run=original;checks.append(dict(case='arrival_side' if mode=='side' else 'arrival_open_path',no_rock_moved=True,alizon_right_of_player=True,zero_object_collisions=True,zero_wall_steps=True));continue
  r.keys={4};r.run(32);r.keys=set();r.run(30);q.pulse(8,30)
  q.wait(lambda:q.callback()=='BattleMainCB2',18000)
  actions={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
  q.wait(lambda:r.u32(r.symbols['gBattlerControllerFuncs']) in actions,12000)
  if mode=='ko':
   q.drain(60000);assert r.read(r.symbols['gBattleOutcome'],1)==b'\1'
   assert 1 not in q.actors() and 7 in q.actors() and not blink and not collisions and not walls
   r.run=original;q.warp('PalletTown_PlayersHouse_2F',5,5);q.warp('MtEmber_Summit',8,9);r.run(300)
   assert 1 in q.actors() and 7 not in q.actors() and not q.fg(0x33b)
   checks.append(dict(case='native_KO',zero_visible_gorgouille_frames_after_KO=True,respawns_on_next_visit=True,alizon_initially_hidden_on_return=True));continue
  q.pulse(7,20);q.pulse(8,240);q.pulse(8,90);q.pulse(8,90)
  for f in range(20000):
   outcome=r.read(r.symbols['gBattleOutcome'],1)[0]
   if outcome==7:caught=True
   r.keys={8 if q.callback()=='CB2_Overworld' else 0} if f%20<2 else set();r.run()
   if caught and q.idle() and 7 not in q.actors():break
  else:raise AssertionError(('Capture/sortie incomplète',q.callback(),positions()))
  assert not blink,blink
  assert not collisions,collisions[:10]
  assert not walls,walls[:10]
  assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for _,a,b in pushes)
  assert 1 not in q.actors() and 7 not in q.actors() and q.fg(0x33b)
  r.frame.save(D/'apres-capture-sortie.png');rocks={k:v for k,v in positions().items() if k in (2,3,4,5)}
  def pulse(keys,hold=1,after=20):
   r.keys=set();r.run(4);r.keys=set(keys);r.run(hold);r.keys=set();r.run(after)
  result=nav.navigate(r,[9,15],pulse,100)
  assert result['reason'] in ('arrived','map transition'),result
  r.run=original;checks.append(dict(case='native_capture_and_departure',zero_object_collisions=True,zero_wall_steps=True,zero_visible_gorgouille_frames_after_capture=True,rock_pushes=pushes,rocks_after_scene=rocks,player_can_follow_exit_path=True))
 finally:r.close()
(D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks),ensure_ascii=False,indent=2)+'\n');print('PASS arrivée, capture sans flash, départ, rochers et chemin du joueur',flush=True)

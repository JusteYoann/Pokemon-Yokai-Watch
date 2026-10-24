"""Controller-only bag use; observation restricted to ordinary combat/inventory data."""
import struct

def throw_ball(r,pulse,observe):
 for i in range(6000):
  s=observe();b=s['battle']
  if b and b['controller']=='HandleInputChooseAction':break
  if s['callback']!='BattleMainCB2':raise RuntimeError('Not in a wild battle command menu')
  r.keys={8} if i%16<3 else set();r.run()
 else:raise RuntimeError('No command menu')
 r.keys=set()
 flags=r.u32(r.symbols['gBattleTypeFlags']);assert not flags&8,'Trainer battle: no capture attempt'
 cur=b['action_cursor']
 if cur&2:pulse([4],1,20)
 if not cur&1:pulse([7],1,20)
 pulse([8],1,240)
 for _ in range(4):
  pocket=int.from_bytes(r.read(r.symbols['gBagMenuState']+6,2),'little')
  if pocket==2:break
  pulse([7],1,120)
 else:raise RuntimeError('Ball pocket unavailable')
 pointer=r.u32(r.symbols['gBagPockets']+16);capacity=r.read(r.symbols['gBagPockets']+20,1)[0]
 key=r.u32(r.u32(r.symbols['gSaveBlock2Ptr'])+0xf20)&65535
 choices=[]
 for i in range(capacity):
  item,qty=struct.unpack('<HH',r.read(pointer+4*i,4));qty^=key
  if item in (2,3,4,5,6,7,8,9,10,11,12) and qty:choices.append(((0 if item==2 else 1 if item==3 else 2 if item==4 else 3),i,item,qty))
 if not choices:raise RuntimeError('No ordinary Balls; Master Ball deliberately excluded')
 _,target,item,quantity=min(choices)
 for _ in range(80):
  state=r.read(r.symbols['gBagMenuState'],20);above=int.from_bytes(state[8+2*2:10+2*2],'little');cur=int.from_bytes(state[14+2*2:16+2*2],'little')+above
  if cur==target:break
  pulse([5 if cur<target else 4],1,20)
 else:raise RuntimeError('Ball selection failed')
 pulse([8],1,120)
 if observe()['callback']!='BattleMainCB2':pulse([8],1,240)
 return dict(ball=item,quantity_before=quantity)

def finish_capture(r,observe,max_frames=6000):
 caught=False
 initial=set(observe()['captured'])
 for i in range(max_frames):
  if i%8==0:
   s=observe()
   displayed=s['battle']['displayed'] if s['battle'] else ''
   caught |= r.read(r.symbols['gBattleOutcome'],1)==b'\7' or bool(set(s['captured'])-initial) or displayed.startswith('Attrapé!')
   if s['callback'] in ('CB2_Overworld','CB2_ReturnToField','CB2_ReturnToFieldLocal'):
    r.keys=set();return dict(caught=caught,finished=True)
   if s['battle'] and s['battle']['controller']=='HandleInputChooseAction' and not caught:
    r.keys=set();return dict(caught=False,finished=True)
  r.keys={0 if caught else 8} if i%16<3 else set();r.run()
 r.keys=set();return dict(caught=caught,finished=False)

def fight(r,observe,options):
 selected=False
 for i in range(options.get('frames',18000)):
  if i%16==0:
   t=observe()
   if t['callback']!='BattleMainCB2':break
   if any('YesNo' in task or 'Naming' in task for task in t['tasks']):break
   b=t['battle'];keys={0} if 'changer' in b['displayed'].lower() else {8}
   if 'YesNo' in b['controller']:
    if any(x in b['displayed'].lower() for x in ('apprendre','oublier')):break
    keys={0}
   elif b['controller']=='HandleInputChooseAction':
    if options.get('wait_menu'):break
    if selected and options.get('one_turn'):break
    cur=b['action_cursor'];keys={6} if cur&1 else ({4} if cur&2 else {8})
   elif b['controller']=='HandleInputChooseMove':
    selected=True;p=r.symbols['gBattleMons'];own_types=r.read(p+0x21,2)
    attack=int.from_bytes(r.read(p+2,2),'little');special=int.from_bytes(r.read(p+8,2),'little');choices=[]
    for j,m in enumerate(b['moves']):
     if not m['id'] or not m['pp']:continue
     typ=r.read(r.symbols['gBattleMoves']+12*m['id']+2,1)[0]
     score=m['power']*(1.5 if typ in own_types else 1)*(special if typ>=10 else attack);choices.append((score,-j))
    target=options['move'] if 'move' in options and b['moves'][options['move']]['pp'] else (-max(choices)[1] if choices else 0)
    cur=b['move_cursor']
    if (cur&1)!=(target&1):keys={7 if target&1 else 6}
    elif (cur&2)!=(target&2):keys={5 if target&2 else 4}
  r.keys=keys if i%16<3 else set();r.run()
 r.keys=set();return i+1

def flee(r,pulse,observe,max_frames=8000):
 for i in range(max_frames):
  if i%16==0:
   s=observe();b=s['battle']
   if not b:
    r.keys=set();return dict(callback=s['callback'],frames=i)
   if r.u32(r.symbols['gBattleTypeFlags'])&8:raise RuntimeError('Cannot flee a trainer battle')
   keys={8}
   if 'YesNo' in b['controller']:keys={0}
   elif b['controller']=='HandleInputChooseAction':
    cur=b['action_cursor'];keys={7} if not cur&1 else ({5} if not cur&2 else {8})
  r.keys=keys if i%16<3 else set();r.run()
 r.keys=set();return dict(stopped='timeout',frames=max_frames)

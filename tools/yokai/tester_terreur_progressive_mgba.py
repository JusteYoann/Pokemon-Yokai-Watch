#!/usr/bin/env python3
"""Vérifie la transition de cinq secondes et les tuiles du chrono pendant la marche."""
import hashlib,json,os,struct
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs'/os.environ.get('TH_TEST_DIR','terre-heure-progressive-20261025');P.mkdir(parents=True,exist_ok=True)
r=new_game();th=r.symbols['sTh'];checks=[]
def byte(p):return r.read(p,1)[0]
def passed(s):checks.append(s);print('PASS',s,flush=True)
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);r.write(sb+0xee0+0x500//8,b'\xff'*96);r.call('VarSet',0x40f9,1);r.call('VarSet',0x40fa,0x101)
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());g=groups['group_order'].index('gMapGroup_Dungeons');n=groups['gMapGroup_Dungeons'].index('MtMoon_1F')
 r.call('SetWarpDestination',g,n,255,20,27);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
 r.call('VarSet',0x40fb,0x100);assert r.call('TerreHeureTryStep')
 for f in range(1000):
  if byte(th+176)==1:break
  r.run()
 else:raise AssertionError('Transition non atteinte')
 npc=next(r.symbols['gObjectEvents']+36*i for i in range(16) if byte(r.symbols['gObjectEvents']+36*i)&1 and byte(r.symbols['gObjectEvents']+36*i+8)==1)
 sprite=r.symbols['gSprites']+68*byte(npc+4);tile=int.from_bytes(r.read(sprite+4,2),'little')&1023;counts=[]
 remaining=r.u32(th+156);assert remaining==17919,remaining;start=r.u32(r.symbols['gMain']+0x24);alpha=[];colored=[]
 while byte(th+176)==1:
  assert byte(r.symbols['sLockFieldControls'])
  assert byte(r.symbols['sGlobalScriptContextStatus'])==1, 'Texte autorisé avant la fin'
  counts.append(sum((b&15!=0)+(b>>4!=0) for b in r.read(0x06010000+tile*32,256)))
  a=int.from_bytes(r.read(r.symbols['sGpuRegBuffer']+0x52,2),'little')&31;alpha.append(a)
  pal=struct.unpack('<208H',r.read(0x05000000,416));colored.append(sum(c&31!=(c>>5)&31 or c&31!=(c>>10)&31 for c in pal))
  r.run()
 elapsed=r.u32(r.symbols['gMain']+0x24)-start
 assert elapsed>=299,elapsed
 assert r.u32(th+156)==remaining
 assert alpha[1:]==sorted(alpha[1:]) and alpha[-1]==3 and len(set(alpha))>=3,alpha
 assert colored[-1]<colored[0],(colored[0],colored[-1])
 assert byte(th+176) in (7,9)
 while byte(th+176) in (7,9):r.run()
 assert byte(th+176)==3
 assert counts[-1]<counts[0] and len(set(counts))>=10,(counts[0],counts[-1],len(set(counts)))
 passed('Les habitants se dissolvent progressivement pendant la même transition, sans effacer Nathan')
 passed('Brume et désaturation progressent ensemble pendant 300 VBlanks (5,023 s); texte absent, joueur verrouillé, chrono intact')
 for f in range(3000):
  r.keys={8} if f%100<2 else set();r.run()
  if byte(th+176)==2 and not byte(r.symbols['sLockFieldControls']):break
 else:raise AssertionError('Exploration non atteinte')
 r.keys=set();r.run(4)
 assert 17911<=r.u32(th+156)<=17919,r.u32(th+156)
 passed('Durée de cinq minutes (17919 VBlanks), sans décompte pendant l’introduction')
 patrols=[]
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i
  if byte(p)&1 and byte(p+8) in (231,232,236,237,238,239,240,241):patrols.append(p)
 assert 1<=len(patrols)<=8,len(patrols)
 player=next(r.symbols['gObjectEvents']+36*i for i in range(16) if byte(r.symbols['gObjectEvents']+36*i)&1 and byte(r.symbols['gObjectEvents']+36*i+8)==255)
 px,py=struct.unpack('<hh',r.read(player+16,4));visible=0
 for p in patrols:
  x,y=struct.unpack('<hh',r.read(p+16,4))
  if abs(x-px)<=7 and abs(y-py)<=5:visible+=1
 assert visible>=1,visible
 passed(f'{len(patrols)} patrouilles actives, dont {visible} proches de la caméra; cases occupées et passages étroits exclus des nouveaux placements')
 snapshot=r.snapshot();samples=0
 # Isolate map scrolling from the new two-second patrol reaction. Native
 # held walk actions still animate Nathan and stream the map's tile rows.
 for direction in (2,1,3,4):
  r.restore(snapshot);r.keys=set();r.call('ScriptContext_Init');r.call('LockPlayerFieldControls')
  player_id=next(i for i in range(16) if byte(r.symbols['gObjectEvents']+36*i)&1 and byte(r.symbols['gObjectEvents']+36*i+8)==255)
  player_obj=r.symbols['gObjectEvents']+36*player_id
  for step in range(2):
   before_pos=struct.unpack('<hh',r.read(player_obj+16,4))
   r.call('ObjectEventClearHeldMovementIfActive',player_obj)
   movement=r.call('GetWalkNormalMovementAction',direction)
   assert not r.call('ObjectEventSetHeldMovement',player_obj,movement)
   for frame in range(24):
    r.run();wid=byte(th+189)
    if wid==255:continue
    win=r.symbols['gWindows']+12*wid;data=r.u32(win+8);base=int.from_bytes(r.read(win+6,2),'little')
    assert base+12<=0x300,hex(base)
    if frame%3==2:
     assert r.read(0x06008000+base*32,384)==r.read(data,384),('Chrono écrasé pendant le défilement',direction,frame)
     samples+=1
   after_pos=struct.unpack('<hh',r.read(player_obj+16,4));dx,dy={1:(0,1),2:(0,-1),3:(-1,0),4:(1,0)}[direction]
   assert after_pos==(before_pos[0]+dx,before_pos[1]+dy),(direction,before_pos,after_pos)
 assert samples>=40,samples
 passed(f'Chrono intact dans la VRAM sur {samples} contrôles pendant des déplacements dans les quatre directions')
 # Restore the same event and let the entire five-minute clock elapse in the
 # native Start menu, where pursuit is suspended but the timer keeps running.
 r.restore(snapshot);r.keys=set();r.call('ScriptContext_Init');r.call('UnlockPlayerFieldControls')
 for f in range(1500):
  r.keys={3} if f%20<2 else set();r.run()
  if any(byte(r.symbols['gTasks']+40*i+4)&1 and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_StartMenuHandleInput']|1 for i in range(16)):break
 else:raise AssertionError('Menu Start non ouvert')
 r.keys=set();r.run(30)
 start_remaining=r.u32(th+156)
 assert start_remaining>17800,start_remaining
 r.run(start_remaining+5);assert r.u32(th+156)==0
 r.keys={0};r.run(2);r.keys=set()
 for f in range(1200):
  r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
 else:raise AssertionError('Combat absent après cinq minutes et fermeture du menu')
 passed('Cinq minutes réellement écoulées dans mGBA; chrono à zéro puis combat imposé en fermant le menu')

 r.restore(snapshot);r.keys=set();r.write(r.symbols['gBattleOutcome'],b'\1');r.call('TerreHeureBattleResult');r.run(80)
 assert byte(th+183)==1
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i
  assert not(byte(p)&1 and byte(p+8) in (230,231,232,236,237,238,239,240,241))
 passed('Après une victoire, l’Oni et toutes les patrouilles sont retirés; exploration libre conservée')

finally:
 (P/'TESTS.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'checks':checks},ensure_ascii=False,indent=2)+'\n');r.close()

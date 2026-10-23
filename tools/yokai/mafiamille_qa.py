"""Isolated mGBA fixtures; no edits to ROM, events, opponents, or save format."""
import json,re
from mgba_rpc import ROOT
G=json.loads((ROOT/'data/maps/map_groups.json').read_text());MAPS={name:(i,j) for i,g in enumerate(G['group_order']) for j,name in enumerate(G[g])}
C={}
for path in (ROOT/'include/constants').glob('*.h'):
 for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\s*(?:$|//)',path.read_text(),re.M):C[k]=int(v,0)
C['FLAG_SYS_GAME_CLEAR']=0x82C

def warp(r,group,num,x,y):
 r.keys=set();r.call('SetWarpDestination',group,num,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
 for f in range(1800):
  r.run()
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Map load timeout')
 r.run(300)

def strong_party(r):
 r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 for name in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_SPATK','MON_DATA_DEF','MON_DATA_SPDEF']:
  r.w32(r.PARAMS+128,999);r.call('SetMonData',r.symbols['gPlayerParty'],C[name],r.PARAMS+128)
 for i,m in enumerate(['MOVE_AERIAL_ACE','MOVE_SHOCK_WAVE','MOVE_SWIFT','MOVE_MAGICAL_LEAF']):r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C[m],i)

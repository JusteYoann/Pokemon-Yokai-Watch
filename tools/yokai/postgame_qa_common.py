"""Fixtures natives isolées, sans ouvrir ni modifier une sauvegarde utilisateur."""
import json,re,struct,hashlib,sys
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game
class QA:
 def __init__(self,report):
  self.r=new_game();self.checks=[];self.report=report;self.P=ROOT/'docs/postgame-quetes-20261025';self.P.mkdir(exist_ok=True)
  groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());self.maps={n:(i,j) for i,key in enumerate(groups['group_order']) for j,n in enumerate(groups[key])}
  self.flags={n:int(v,16) for n,v in re.findall(r'#define\s+(FLAG_PG_\w+)\s+(0x[0-9A-F]+)',(ROOT/'include/constants/flags.h').read_text())}
  self.reverse={v|1:k for k,v in self.r.symbols.items()}
 def f(self,name,on=True):self.r.call('FlagSet' if on else 'FlagClear',self.flags.get(name,name))
 def fg(self,name):return self.r.call('FlagGet',self.flags.get(name,name))
 def mon(self,i=0,species=150,level=100):
  r=self.r;p=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',p,species,level,31,1,12345+i,0,0)
  if species==150:r.call('SetMonMoveSlot',p,129,0)
  r.write(r.symbols['gPlayerPartyCount'],bytes([i+1]));return p
 def warp(self,name,x,y,settle=180):
  r=self.r;g,n=self.maps[name];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.keys=set();r.run(settle)
  if self.callback()!='CB2_Overworld':self.wait(lambda:self.callback()=='CB2_Overworld',4800)
 def callback(self):return self.reverse.get(self.r.u32(self.r.symbols['gMain']+4),'?')
 def unlocked(self):return not self.r.read(self.r.symbols['sLockFieldControls'],1)[0]
 def pulse(self,key,after=12):
  r=self.r;r.keys=set();r.run(3);r.keys={key};r.run();r.keys=set();r.run(after)
 def wait(self,cond,limit=12000,press=True):
  r=self.r
  for f in range(limit):
   if cond():r.keys=set();return f
   key=8
   if press and self.callback()=='CB2_UpdatePartyMenu':
    slot=r.read(r.symbols['gPartyMenu']+9,1)[0]
    if int.from_bytes(r.read(r.symbols['gBattleMons']+40,2),'little')>0:key=0
    elif slot<6 and int.from_bytes(r.read(r.symbols['gPlayerParty']+slot*100+86,2),'little')==0:key=5
   if press and self.callback()=='BattleMainCB2':
    from pilote_combat_mgba import battle_keys
    r.keys=battle_keys(r,f)
   else:r.keys={key} if press and f%16<2 else set()
   r.run()
  raise AssertionError(('Timeout',self.callback(),self.r.read(self.r.symbols['sLockFieldControls'],1),self.r.u32(self.r.symbols['sGlobalScriptContext']+8)))
 def script(self,label):self.r.call('ScriptContext_SetupScript',self.r.symbols[label]);self.r.run(2)
 def idle(self):return self.callback()=='CB2_Overworld' and self.unlocked() and self.r.read(self.r.symbols['sGlobalScriptContextStatus'],1)[0]==2
 def drain(self,limit=15000):return self.wait(self.idle,limit)
 def saved(self,*flags):
  r=self.r;expected=[self.fg(flag) for flag in flags]
  r.call('SaveMapView');r.call('SaveQuestLogData');assert r.call('TrySavingData',0,max_frames=3000)==1
  r.lib.retro_reset();r.run(600);self.pulse(3,180);self.wait(lambda:self.callback()=='CB2_Overworld' and self.unlocked() and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3),24000)
  actual=[self.fg(flag) for flag in flags]
  if actual!=expected:self.shot('sauvegarde-diagnostic');print('SAVE',flags,expected,actual,'QL',r.read(r.symbols['gQuestLogState'],1).hex(),flush=True)
  assert actual==expected,(flags,expected,actual)
 def passed(self,s):self.checks.append(s);print('PASS',s,flush=True)
 def shot(self,name):
  from PIL import Image
  self.r.frame.save(self.P/(name+'.png'));self.r.frame.resize((720,480),Image.Resampling.NEAREST).save(self.P/(name+'-x3.png'))
 def actors(self):
  r=self.r;return {r.read(r.symbols['gObjectEvents']+36*i+8,1)[0]:r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1}
 def local(self,symbol):
  text=(ROOT/'include/constants/map_event_ids.h').read_text();return int(re.search(r'#define\s+'+symbol+r'\s+(\d+)',text)[1])
 def result(self):return int.from_bytes(self.r.read(self.r.symbols['gSpecialVar_Result'],2),'little')
 def give(self,gift):
  r=self.r;r.write(r.symbols['gSpecialVar_0x8004'],struct.pack('<H',gift));r.call('PostgameGiveGift');return self.result()
 def finish(self):
  (self.P/self.report).write_text(json.dumps({'rom_sha256':hashlib.sha256(self.r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'passed':sys.exc_info()[0] is None,'error':str(sys.exc_info()[1]) if sys.exc_info()[0] else None,'checks':self.checks},ensure_ascii=False,indent=2)+'\n');self.r.close()

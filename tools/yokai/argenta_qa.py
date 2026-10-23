"""Developer-only scene driver. Does not patch ROM or persist any save file."""
from mafiamille_qa import C
C['FLAG_WORLD_MAP_PEWTER_CITY']=0x892

def drive(r,limit=20000):
 for f in range(limit):
  r.keys={8} if f%16<4 else set();r.run()
  assert r.u32(r.symbols['gMain']+4)!=r.symbols['BattleMainCB2']|1,'Unexpected combat'
  if f%30==0 and r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_DONE']) and not r.call('FlagGet',C['FLAG_ARGENTA_MORLEONE_PENDING']) and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02':
   r.keys=set();r.run(90);assert not r.call('ArePlayerFieldControlsLocked') if 'ArePlayerFieldControlsLocked' in r.symbols else True;return f
 raise AssertionError('Scene did not finish')

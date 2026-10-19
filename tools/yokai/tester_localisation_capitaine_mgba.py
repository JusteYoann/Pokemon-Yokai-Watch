#!/usr/bin/env python3
"""Original Captain interaction through controller input after a map warp fixture."""
import hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/ss_anne';P.mkdir(exist_ok=True)
r=new_game();passed=False;error='Interrupted';checks=[]
try:
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());g,n=next((i,j) for i,k in enumerate(groups['group_order']) for j,v in enumerate(groups[k]) if v=='SSAnne_CaptainsOffice')
 r.call('CreateMon',r.symbols['gPlayerParty'],5,15,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 assert not r.call('FlagGet',0x237) and not r.call('CheckBagHasItem',339,1)
 r.call('SetWarpDestination',g,n,255,5,5);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 r.keys={4};r.run(1);r.keys=set();r.run(12);r.keys={8};r.run(1);r.keys=set();r.run(240);r.frame.save(P/'capitaine-interaction.png')
 for turn in range(350):
  r.keys={8};r.run(1);r.keys=set();r.run(63)
  if turn%8==0 and r.call('FlagGet',0x237):break
 else:raise AssertionError('Original Captain event did not grant HM01')
 assert r.call('CheckBagHasItem',339,1),'HM01 missing from actual bag'
 assert r.call('VarGet',0x407e)==1,'Original ship-departure scene not advanced'
 r.run(120);r.frame.save(P/'capitaine-cs01-terminee.png')
 checks=[dict(test='Actual A-button interaction with Captain after warp fixture',passed=True),dict(test='HM01 absent before interaction and present in native bag after original giveitem',passed=True),dict(test='FLAG_GOT_HM01 set by original event',passed=True),dict(test='Original Vermilion ship-departure scene advanced to1',passed=True)]
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'capitaine-diagnostic.png');raise
finally:
 r.close();(P/'CAPITAINE_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='New-game then Captain map warp and Komasan party fixture. Actual directional/A inputs trigger original Captain event, text, fanfare and HM01 reward. Does not prove reaching ship from full story or sailing-away sequence.',results=checks),ensure_ascii=False,indent=2)+'\n')
print('CAPTAIN FR PASS',len(checks))

#!/usr/bin/env python3
"""Actual Memorydex menu with unlocked-data fixture and controller selection of Don."""
import hashlib,json
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/memorydex';P.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;error='Interrupted';widths=[]
try:
 for name,bound in [('gFameCheckerPersonName_Giovanni',64)]+[(f'gFameCheckerFlavorTextOriginObjectName_Giovanni{i}',84) for i in range(6)]+[(f'gFameCheckerFlavorTextOriginLocation_Giovanni{i}',84) for i in range(6)]:
  width=r.call('GetStringWidth',0,r.symbols[name],0);assert width<=bound,(name,width,bound);widths.append(dict(symbol=name,native_small_font_pixels=width,bound=bound))
 width=r.call('GetStringWidth',2,r.symbols['sMafiamilleFameListName'],0);assert width<=56; widths.append(dict(symbol='sMafiamilleFameListName',native_normal_font_pixels=width,bound=56))
 r.call('FullyUnlockFameChecker');r.call('UseFameChecker',r.symbols['CB2_Overworld']|1);r.run(180)
 for i in range(15):
  r.keys={5};r.run();r.keys=set();r.run(12)
 r.run(60);r.frame.save(P/'don-selection.png')
 ptr=r.u32(r.symbols['sFameCheckerData']);assert ptr
 # Current item cursor + scroll top index identifies the sixteenth person.
 selected=r.call('FameCheckerGetCursorY')
 assert selected==15,('Wrong Memorydex row',selected)
 r.keys={8};r.run();r.keys=set();r.run(200);r.frame.save(P/'don-notice.png')
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,widths=widths),indent=2)+'\n')

#!/usr/bin/env python3
"""Re-run existing native suites with dedicated reports; completed quest is a stated fixture."""
import os,sys
from mgba_rpc import ROOT
kind=sys.argv[1]
name={'champions':'tester_champions_mgba.py','effets':'tester_champions_effets_mgba.py','lavanville':'tester_champions_lavanville_mgba.py','variantes':'capturer_variantes_champions_mgba.py'}[kind]
s=(ROOT/'tools/yokai'/name).read_text()
s=s.replace("'docs/champions-yokai-watch/validation/regressions/lavanville'","'docs/pierre-philosovni/validation/regressions/lavanville'").replace("'docs/champions-yokai-watch/validation'","'docs/pierre-philosovni/validation/regressions/"+kind+"'")
# Leaders remain tested with actual native encounters, teams, flags and rewards;
# this fixture simply places those independent regression tests after the quest.
s=s.replace('from mgba_new_game import new_game','''from mgba_new_game import new_game as _new_game

def new_game(*args, **kwargs):
 r=_new_game(*args, **kwargs)
 r.call('VarSet',0x40f4,3)
 return r
''')
# Refresh the saved viewport exactly as the native Save menu does.
s=s.replace("assert r.call('TrySavingData',", "r.call('SaveMapView');assert r.call('TrySavingData',")
exec(compile(s,str(ROOT/'tools/yokai'/name),'exec'))

#!/usr/bin/env python3
"""Run approved A/B/Ariane suites on Phase C ROMs into a separate report tree."""
import sys
from mgba_rpc import ROOT
kind=sys.argv[1]
names={'phase-a':'tester_cramois_phase_a_mgba.py','phase-b':'tester_cramois_phase_b_mgba.py','ariane':'tester_philosovni_suivi_mgba.py'}
path=ROOT/'tools/yokai'/names[kind];s=path.read_text()
if kind=='ariane':
 s=s.replace("ROOT/'docs/pierre-philosovni/suivi-ariane'", "ROOT/'docs/cramois-ile-passe/phase-c/regressions/ariane'")
 s=s.replace('[7,7,4,6,6,5,7,6]', '[7,7,4,7,6,5,6,7]')
else:s=s.replace('docs/cramois-ile-passe/'+kind,'docs/cramois-ile-passe/phase-c/regressions/'+kind)
s=s.replace('No Phase C dialogue, quiz, party, map or save format changed','Maritime fixtures do not alter dialogues, quiz, parties, geometry or save format')
exec(compile(s,str(path),'exec'))

#!/usr/bin/env python3
"""Run the approved Ariane suite on the new ROM without overwriting its history."""
from mgba_rpc import ROOT
path=ROOT/'tools/yokai/tester_philosovni_suivi_mgba.py'
source=path.read_text().replace("ROOT/'docs/pierre-philosovni/suivi-ariane'", "ROOT/'docs/cramois-ile-passe/phase-a/regressions/ariane'")
# Keep the same corner/reversal checks east of the roaming sailor's native range.
source=source.replace('[7,7,4,6,6,5,7,6]', '[7,7,4,7,6,5,6,7]')
exec(compile(source,str(path),'exec'))

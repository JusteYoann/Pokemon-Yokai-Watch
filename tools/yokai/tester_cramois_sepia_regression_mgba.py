#!/usr/bin/env python3
"""Re-run phase A with the explicitly requested constant monbg sepia mask; preserve historical reports."""
from mgba_rpc import ROOT
p=ROOT/'tools/yokai/tester_cramois_phase_a_mgba.py'
s=p.read_text().replace('docs/cramois-ile-passe/phase-a','docs/cramois-ile-passe/phase-c/sepia-combat-constant/regressions/phase-a').replace('0x000f001c','0x000f031c')
exec(compile(s,str(p),'exec'))

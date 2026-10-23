#!/usr/bin/env python3
"""Re-run approved suites on Phase B ROMs without overwriting historical reports."""
import sys
from mgba_rpc import ROOT
kind=sys.argv[1]
name='tester_cramois_phase_a_mgba.py' if kind=='phase-a' else 'tester_cramois_ariane_mgba.py'
source=(ROOT/'tools/yokai'/name).read_text()
target='docs/cramois-ile-passe/phase-b/regressions/phase-a' if kind=='phase-a' else 'docs/cramois-ile-passe/phase-b'
source=source.replace('docs/cramois-ile-passe/phase-a',target)
# The Ariane wrapper itself redirects the original suite, so substitute its directory as well.
exec(compile(source,str(ROOT/'tools/yokai'/name),'exec'))

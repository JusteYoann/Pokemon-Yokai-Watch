#!/usr/bin/env python3
"""Re-run native companion visuals after mechanical size correction, separately from historical phase C reports."""
from mgba_rpc import ROOT
p=ROOT/'tools/yokai/capturer_cramois_c_visuels_mgba.py'
s=p.read_text().replace("phase-c'/mode", "phase-c/taille-hovernyan'/mode")
exec(compile(s,str(p),'exec'))

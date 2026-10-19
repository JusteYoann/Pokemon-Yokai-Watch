#!/usr/bin/env python3
"""Retired dedicated drawings: remap existing approved palette colors to normal indices.
No artwork, pixel, normal palette or shiny eligibility is modified.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def main():
 policy=json.loads((R/'data/yokai/shiny_artwork_policy.json').read_text());assert not policy['dedicated_bitmaps_enabled']
 for row in policy['species']:
  original=row['retired_palette'];mapping=row['normal_index_to_retired_palette_index'];assert len(original)==len(mapping)==16
  colors=[original[i] for i in mapping];assert colors[0]==[0,0,0]
  (R/f"graphics/yokai/{row['number']:03}/shiny.pal").write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
 print('COLOR-ONLY SHINY PALETTES',len(policy['species']))
if __name__=='__main__':main()

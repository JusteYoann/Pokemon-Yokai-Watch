#!/usr/bin/env python3
"""Re-export editable native portrait cell matrices, no generator or plugin required."""
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
ACTORS=['agent_x','alyzon_bie','berenice_belier','inspecteur_giraud','lady_perpetua','laure','marge','mc_kraken','steve_jaws','whisper_humain','nathaniel_age','enma_humain','zazel','yopple_bot','enma_ancien']
def main():
 for actor in ACTORS:
  p=ROOT/'graphics/yokai_characters'/actor
  spec=json.loads((p/'source'/('battle-grille.json'if actor=='agent_x' else 'portrait-combat-grille.json')).read_text())
  if actor=='agent_x':colors=json.loads((ROOT/spec['palette']).read_text())['colors']
  else:colors=[list(bytes.fromhex(s[1:]))for s in spec['palette']]
  assert len(colors)==16 and len(spec['rows'])==64 and all(len(row)==64 for row in spec['rows'])
  data=bytes(0 if c=='.'else int(c,16)for row in spec['rows']for c in row)
  im=Image.frombytes('P',(64,64),data);im.putpalette([v for c in colors for v in c]+[0]*720);im.save(p/'battle.png',bits=4,transparency=0)
  (p/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c))for c in colors)+'\n')
if __name__=='__main__':main()

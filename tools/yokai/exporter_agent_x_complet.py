#!/usr/bin/env python3
"""Export Agent X editable native matrices, no source illustration conversion."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
from exporter_grilles_personnages import export, ROOT
P=ROOT/'graphics/yokai_characters/agent_x'
def main():
 export('agent_x');ow=Image.open(P/'overworld.png');spec=json.loads((P/'source/battle-grille.json').read_text());colors=json.loads((ROOT/spec['palette']).read_text())['colors']
 assert spec['size']==[64,64] and len(spec['rows'])==64 and all(len(s)==64 for s in spec['rows'])
 im=Image.frombytes('P',(64,64),bytes(0 if c=='.' else int(c,16) for s in spec['rows'] for c in s))
 im.putpalette([v for c in colors for v in c]+[0]*720);im.save(P/'battle.png',bits=4,transparency=0)
 (P/'normal.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c))for c in colors)+'\n')
 # Exact approved front is a protected source.
 ref=Image.open(ROOT/'docs/atelier-personnages/propositions/agent-x-frlg-abc/agent-x-face-validee.png').convert('RGBA')
 assert ow.crop((0,0,16,32)).convert('RGBA').tobytes()==ref.tobytes()
 out=P/'apercu-sources.png';board=Image.new('RGB',(160,108),(232,232,232));d=ImageDraw.Draw(board)
 rgba=ow.convert('RGBA');board.paste(rgba,(8,0),rgba);d.text((8,34),'9 frames - 16x32',fill='black')
 rgba=Image.open(P/'battle.png').convert('RGBA');board.paste(rgba,(48,44),rgba)
 board.resize((960,648),Image.Resampling.NEAREST).save(out)
 pics=[ow.crop((i*16,0,(i+1)*16,32)).convert('RGBA') for i in range(9)]
 for name,ids in [('face',[0,3,0,4]),('dos',[1,5,1,6]),('gauche',[2,7,2,8])]:
  movie=[]
  for i in ids:
   bg=Image.new('RGBA',(16,32),(232,232,232,255));bg.alpha_composite(pics[i]);movie.append(bg.resize((128,256),Image.Resampling.NEAREST).convert('RGB'))
  movie[0].save(P/f'apercu-marche-{name}.gif',save_all=True,append_images=movie[1:],duration=160,loop=0)
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Export explicitly authored native grid cells. No source illustration is read.

A source row contains exactly16 symbols: '.' is transparent;1..f are color
indices. The PNG is written at native resolution, with no sampling or resizing.
Only the optional comparison preview is enlarged after export.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
ACTORS=('laure','marge','agent_x')

def export(actor):
 folder=ROOT/'graphics/yokai_characters'/actor
 path=folder/'source/overworld-grille.json';spec=json.loads(path.read_text())
 palette_path=ROOT/spec['palette'];colors=json.loads(palette_path.read_text())['colors']
 assert len(colors)==16 and all(len(c)==3 and all(0<=v<=255 for v in c) for c in colors)
 assert (spec['frame_width'],spec['frame_height'])==(16,32) and len(spec['frames'])==9
 data=bytearray(144*32)
 for i,frame in enumerate(spec['frames']):
  assert frame['index']==i and len(frame['rows'])==32
  for y,row in enumerate(frame['rows']):
   assert len(row)==16 and set(row)<=set('.123456789abcdef'),(actor,i,y)
   for x,symbol in enumerate(row):data[y*144+i*16+x]=0 if symbol=='.' else int(symbol,16)
 im=Image.frombytes('P',(144,32),bytes(data));im.putpalette([v for c in colors for v in c]+[0]*720)
 im.save(folder/'overworld.png',bits=4,transparency=0)
 text='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n'
 (folder/'overworld.pal').write_text(text)
 (ROOT/'graphics/yokai_characters/nathan_trace/overworld.pal').write_text(text)
 report=dict(method=__doc__,source=str(path.relative_to(ROOT)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),palette=str(palette_path.relative_to(ROOT)),frames=9,frame_size=[16,32],transparent_index=0,illustrations_read=0,export_resizing=False)
 (folder/'trace-nathan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return im

def preview():
 names=['nathan',*ACTORS];out=Image.new('RGB',(1152,4*288),(220,220,220));draw=ImageDraw.Draw(out)
 for row,actor in enumerate(names):
  im=Image.open(ROOT/f'graphics/yokai_characters/{actor}'/('normal.png' if actor=='nathan' else 'overworld.png')).convert('RGBA')
  draw.text((8,row*288+4),actor,fill='black')
  zoom=im.resize((1152,256),Image.Resampling.NEAREST);out.paste(zoom,(0,row*288+24),zoom)
 out.save(ROOT/'graphics/yokai_characters/nathan_trace/comparaison-native-x8.png')

def main():
 for actor in ACTORS:export(actor)
 preview()

if __name__=='__main__':main()

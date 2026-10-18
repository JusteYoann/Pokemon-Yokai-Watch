#!/usr/bin/env python3
"""Deterministic nearest-neighbor indexed4bpp presentation; original art untouched.

Pixel indices (including transparent0) preserved, no smoothing or new colors.
Shared bounds across animation frames preserve walking/bobbing relative motion.
"""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def decode(data,w,h):
 assert len(data)==w*h//2
 return [[(data[(y//8*(w//8)+x//8)*32+(y%8)*4+(x%8)//2]>>(4*(x%2)))&15 for x in range(w)] for y in range(h)]

def encode(pixels,w,h):
 out=bytearray(w*h//2)
 for y in range(h):
  for x in range(w):out[(y//8*(w//8)+x//8)*32+(y%8)*4+(x%8)//2]|=pixels[y][x]<<(4*(x%2))
 return bytes(out)

def transform(data,p):
 w,h=p['frame_width'],p['frame_height'];height=len(data)*2//w
 pixels=decode(data,w,height);assert height%h==0
 frames=height//h;points=[(x,y%h) for y in range(height) for x in range(w) if pixels[y][x]]
 left=min(x for x,y in points);right=max(x for x,y in points)+1;top=min(y for x,y in points);bottom=max(y for x,y in points)+1
 sw,sh=right-left,bottom-top;dw=max(1,(sw*p['scale_q8']+128)//256);dh=max(1,(sh*p['scale_q8']+128)//256)
 assert dw<=w,(p['id'],'horizontal clipping not permitted',dw)
 ox=p.get('center_x',w//2)-dw//2;oy=p.get('top',p.get('bottom',bottom)-dh)
 out=[[0]*w for _ in range(height)]
 for frame in range(frames):
  for dy in range(dh):
   yy=oy+dy
   if not 0<=yy<h:continue
   sy=top+min(sh-1,(2*dy+1)*sh//(2*dh))
   for dx in range(dw):
    xx=ox+dx
    if not 0<=xx<w:continue
    sx=left+min(sw-1,(2*dx+1)*sw//(2*dw));out[frame*h+yy][xx]=pixels[frame*h+sy][sx]
 return encode(out,w,height)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--list-targets',action='store_true');a.add_argument('--input',type=Path);a.add_argument('--output',type=Path);args=a.parse_args()
 profiles=json.loads((ROOT/'data/yokai/sprite_presentation.json').read_text())['profiles']
 if args.list_targets:print(' '.join(p['target'] for p in profiles))
 else:
  p=next(p for p in profiles if (ROOT/p['target']).resolve()==args.output.resolve())
  args.output.write_bytes(transform(args.input.read_bytes(),p))

#!/usr/bin/env python3
"""Generate a deterministic RGB555 golden-brown map, without editing artwork."""
import struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def sepia(c):
 r,g,b=c&31,(c>>5)&31,(c>>10)&31
 y=(77*r+150*g+29*b+128)>>8
 # Keep a quarter of the source hue for olive greens and readable material detail.
 warm=(min(31,(33*y+16)>>5),(28*y+16)>>5,(20*y+16)>>5)
 out=[(v+3*t+2)>>2 for v,t in zip((r,g,b),warm)]
 return out[0]|out[1]<<5|out[2]<<10
if __name__=='__main__':
 p=ROOT/'data/yokai/cramois-sepia-rgb555.bin'
 p.write_bytes(struct.pack('<32768H',*(sepia(c) for c in range(32768))))
 print(p, p.stat().st_size)

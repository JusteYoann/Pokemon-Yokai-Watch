#!/usr/bin/env python3
"""Native VRAM size comparison; actors aligned only in this QA fixture."""
import sys,json,hashlib,struct,os
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import warp,MAPS,strong_party
from presentation_4bpp import decode
from PIL import Image
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
D=ROOT/'docs/pierre-philosovni/usapion-plus-petit'/mode;D.mkdir(parents=True,exist_ok=True)
r=new_game();strong_party(r);r.call('VarSet',0x40f4,1);warp(r,*MAPS['VermilionCity'],33,30)
# Comparison-only staging; the game's map positions are unchanged.
g,n=MAPS['VermilionCity']
r.call('TryMoveObjectEventToMapCoords',9,n,g,32,30);r.call('TryMoveObjectEventToMapCoords',10,n,g,34,30)
heights={};proof=[]
for label,local,w in [('Ariane',9,16),('Nathan',255,16),('Usapion',10,32)]:
 for i in range(16):
  o=r.read(r.symbols['gObjectEvents']+36*i,36)
  if o[0]&1 and o[8]==local:break
 else:raise AssertionError(label)
 r.call('ObjectEventTurn',r.symbols['gObjectEvents']+36*i,1);r.keys=set();r.run(8)
 sid=o[4];attr=int.from_bytes(r.read(r.symbols['gSprites']+sid*68+4,2),'little');tile=attr&1023
 data=r.read(0x06010000+32*tile,w*32//2);pixels=decode(data,w,32)
 points=[(x,y) for y in range(32) for x in range(w) if pixels[y][x]]
 height=max(y for x,y in points)-min(y for x,y in points)+1;heights[label]=height
 proof.append(dict(actor=label,visible_height=height,bottom=max(y for x,y in points)+1,bank=attr>>12,position=struct.unpack_from('<hh',o,16),vram_sha256=hashlib.sha256(data).hexdigest()))
assert heights=={'Ariane':19,'Nathan':19,'Usapion':17},heights
r.keys=set();r.run(30);r.frame.save(D/'comparaison-mgba.png');r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/'comparaison-mgba-x4.png')
(D/'VERIFICATION.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),actors=proof,comparison_staging_only=True),ensure_ascii=False,indent=2)+'\n');r.close();print(mode,heights)

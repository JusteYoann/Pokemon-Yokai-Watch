"""Test-only mGBA rendering of provisional reductions; never writes a ROM or active sprite."""
import sys,json,hashlib,re
from pathlib import Path
import numpy as np
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
from scenario_qa_helpers import warp
OUT=ROOT/'QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/COMPARAISON_PROVISOIRE_NATHAN'
OUT.mkdir(exist_ok=True,parents=True)
source=ROOT/'docs/atelier-personnages/propositions/laure-marge-agent-x/faces-tetes-abaissees.png'
src=Image.open(source).convert('RGB'); W,H=src.size
exports=[]
for i,name in enumerate(['soeur-doree','soeur-argentee','agent-x']):
 crop=src.crop((i*W//3,0,(i+1)*W//3,H));a=np.array(crop)
 mask=~((a[:,:,0]>180)&(a[:,:,1]<80)&(a[:,:,2]>180))
 ys,xs=np.where(mask);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
 # Explicitly NOT a production art conversion: a test-only preview of proportions.
 # Provisional technical reduction for proportions ONLY, not a finished native drawing.
 c=crop.crop(box).resize((12,19),Image.Resampling.NEAREST)
 q=c.quantize(colors=15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 pal=q.getpalette();indices=np.array(q)+1
 rgba=np.array(c);bg=(rgba[:,:,0]>180)&(rgba[:,:,1]<80)&(rgba[:,:,2]>180);indices[bg]=0
 frame=np.zeros((32,16),dtype=np.uint8);frame[12:31,2:14]=indices
 data=bytearray()
 for ty in range(4):
  for tx in range(2):
   for yy in range(8):
    row=frame[ty*8+yy,tx*8:tx*8+8]
    for xx in range(0,8,2):data.append(int(row[xx])|(int(row[xx+1])<<4))
 colors=[(255,0,255)]+[tuple(pal[n:n+3]) for n in range(0,45,3)]
 palette=b''.join(((r>>3)|((g>>3)<<5)|((b>>3)<<10)).to_bytes(2,'little') for r,g,b in colors)
 exports.append((name,bytes(data),palette,box))
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={name:(i,j) for i,g in enumerate(groups['group_order']) for j,name in enumerate(groups[g])}
r=new_game(0)
try:
 warp(r,*maps['Route1'],6,12);r.call('LockPlayerFieldControls')
 player=r.symbols['gObjectEvents']+36*r.read(r.symbols['gPlayerAvatar']+5,1)[0]
 r.call('ObjectEventTurn',player,1);r.run(30)
 sprites=[]
 for n,(name,data,palette,box) in enumerate(exports):
  idx=r.call('SpawnSpecialObjectEventParameterized',156,1,220+n,8+2*n+7,12+7,3)
  assert 0<=idx<16,idx
  obj=r.symbols['gObjectEvents']+36*idx;r.call('ObjectEventTurn',obj,1);r.run(10)
  spr=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
  sprites.append((name,spr,data,palette))
 r.run(30)
 r.frame.save(OUT/'scene-temoin-avant-injection.png')
 def inject():
  for n,(name,spr,data,palette) in enumerate(sprites):
   attr=int.from_bytes(r.read(spr+4,2),'little');bank=12+n
   r.write(spr+4,((attr&0x0fff)|(bank<<12)).to_bytes(2,'little'))
   tile=attr&1023;r.write(0x06010000+tile*32,data)
   r.write(r.symbols['gPlttBufferUnfaded']+512+32*bank,palette)
   r.write(r.symbols['gPlttBufferFaded']+512+32*bank,palette)
   r.write(0x05000200+32*bank,palette)
 for n,(name,spr,data,palette) in enumerate(sprites):
  base=0x03007500+n*256; table=0x03007900+n*8; paladdr=0x03007A00+n*32
  r.write(base,data);r.w32(table,base);r.w32(table+4,256);r.w32(spr+12,table)
  r.write(paladdr,palette);r.call('LoadPalette',paladdr,256+(12+n)*16,32)
  r.call('StartSpriteAnim',spr,0)
 for _ in range(8):inject();r.run()
 r.frame.save(OUT/'capture-mgba-nathan-trois-propositions.png')
 r.frame.resize((960,640),Image.Resampling.NEAREST).save(OUT/'capture-x4.png')
 checks=[]
 for n,(name,spr,data,palette) in enumerate(sprites):
  attr=int.from_bytes(r.read(spr+4,2),'little');tile=attr&1023;bank=attr>>12
  assert r.read(0x06010000+tile*32,256)==data
  assert r.read(0x05000200+bank*32,32)==palette
  checks.append(dict(character=name,rendered_frame_bytes=256,palette_bank=bank,vram_verified=True,palette_verified=True))
 report=dict(kind='REAL_MGBA_SCREENSHOT_WITH_TEST_ONLY_RAM_INJECTION',scope='Static front-facing comparison only; provisional technical reduction to 12x19 within 16x32, not approved production assets. No walking or story integration.',engine='mGBA libretro',source=str(source.relative_to(ROOT)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_modified=False,gameplay_sources_modified=False,nathan='Unmodified actual male player sprite',others='Temporary VRAM and palette replacements of three spawned NPCs; no persistent events',checks=checks)
 (OUT/'CONTROLE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False))
finally:r.close()

#!/usr/bin/env python3
"""Real mGBA capture with a test-only VRAM/palette preview of approved Agent X front.
Other actors use existing ROM graphics. No ROM, story or gameplay edits.
"""
import hashlib,json,struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from mgba_rpc import ROOT
from mgba_new_game import new_game
from scenario_qa_helpers import warp
OUT=ROOT/'QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/AGENT_X_MAFIAMILLE'
OUT.mkdir(parents=True,exist_ok=True)
ART=ROOT/'docs/atelier-personnages/propositions/agent-x-frlg-abc'
spec=json.loads((ART/'agent-x-a-source.json').read_text())
rows=[list(s) for s in spec['rows']]
# User's edited face: two yellow cells, same level, separated by black.
for x,c in [(5,'a'),(6,'1'),(7,'a'),(8,'5')]:rows[20][x]=c
for x,c in [(5,'4'),(6,'4'),(7,'4'),(8,'4'),(9,'5'),(10,'5')]:rows[21][x]=c
spec.update(version='A-deux-yeux-validee',rows=[''.join(s) for s in rows],description='Front proposal approved by creator: two yellow eyes separated by black hat shadow. Other orientations pending.')
(ART/'agent-x-face-validee-source.json').write_text(json.dumps(spec,indent=2)+'\n')
colors=[tuple(bytes.fromhex(c[1:])) for c in spec['palette']]
im=Image.frombytes('P',(16,32),bytes(0 if c=='.' else int(c,16) for s in spec['rows'] for c in s))
im.putpalette([v for c in colors for v in c]+[0]*(768-3*len(colors)))
im.save(ART/'agent-x-face-validee.png',bits=4,transparency=0)
# Native GBA tile order, 4-bit indices, no resizing.
data=bytearray()
for ty in range(4):
 for tx in range(2):
  for y in range(8):
   for x in range(0,8,2):data.append(im.getpixel((tx*8+x,ty*8+y))|(im.getpixel((tx*8+x+1,ty*8+y))<<4))
assert len(data)==256 and im.getbbox()==(1,12,15,31)
pal=b''.join(struct.pack('<H',(r>>3)|((g>>3)<<5)|((b>>3)<<10)) for r,g,b in colors)+b'\0\0'*(16-len(colors))
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
maps={name:(i,j) for i,g in enumerate(groups['group_order']) for j,name in enumerate(groups[g])}
r=new_game();actors=[]
try:
 warp(r,*maps['Route1'],6,12);r.call('LockPlayerFieldControls')
 # Group portrait: Don and Agent X flank the player; six henchmen behind and beside them.
 for n,(name,gfx,x,y) in enumerate([('Don Morleone',164,8,12),('Agent X',176,10,12),('Mafiamille 1',165,3,11),('Mafiamille 2',166,5,11),('Mafiamille 3',167,7,11),('Mafiamille 1',165,9,11),('Mafiamille 2',166,4,12),('Mafiamille 3',167,12,12)]):
  idx=r.call('SpawnSpecialObjectEventParameterized',gfx,0,220+n,x+7,y+7,3);assert idx<16
  obj=r.symbols['gObjectEvents']+36*idx;r.call('ObjectEventTurn',obj,1)
  sp=r.symbols['gSprites']+68*r.read(obj+4,1)[0];actors.append(dict(name=name,gfx=gfx,x=x,y=y,obj=obj,sp=sp))
 r.run(45)
 a=next(a for a in actors if a['gfx']==176);attr=int.from_bytes(r.read(a['sp']+4,2),'little');tile=attr&1023;bank=15
 r.write(a['sp']+4,struct.pack('<H',(attr&0x0fff)|(bank<<12)))
 # Agent X has a separate palette bank from the Morleone group and Nathan.
 assert all((int.from_bytes(r.read(b['sp']+4,2),'little')>>12)!=bank for b in actors if b is not a)
 r.w32(a['sp']+0x1c,r.symbols['SpriteCallbackDummy']|1)
 r.write(a['sp']+0x2c,bytes([r.read(a['sp']+0x2c,1)[0]|0x40]))
 addr=0x06010000+tile*32;r.write(addr,bytes(data))
 r.write(0x0203f000,pal)
 r.call('LoadPalette',0x0203f000,256+16*bank,32)
 r.run(8)
 assert int.from_bytes(r.read(a['sp']+4,2),'little')>>12==bank
 assert r.read(addr,256)==bytes(data)
 assert r.read(0x05000200+bank*32,32)==pal
 cap=r.frame.copy();cap.save(OUT/'scene-mgba-native.png')
 cap.resize((960,640),Image.Resampling.NEAREST).save(OUT/'scene-mgba-x4.png')
 board=Image.new('RGB',(960,700),(232,232,232));board.paste(cap.resize((960,640),Image.Resampling.NEAREST),(0,0))
 d=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
 d.text((16,648),'mGBA ×4 : Nathan, Don Morleone, Agent X et six Mafiamille.',fill='black',font=font)
 d.text((16,674),'Aperçu temporaire : face Agent X chargée en VRAM ; autres sprites issus de la ROM.',fill='black',font=font)
 board.save(OUT/'scene-mgba-annotee-x4.png')
 report=dict(passed=True,engine='mGBA libretro',rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_modified=False,agent_x_preview_injected_in_vram=True,palette_verified=True,tiles_verified=True,other_actors_from_rom=True,actors=[{k:v for k,v in a.items() if k not in ['obj','sp']} for a in actors],limitations=['Test-only group portrait, not a story event','Approved front only; other directions and walking are pending','Not evidence of compiled integration of the new Agent X'])
 (OUT/'CONTROLE.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS mGBA group portrait; Agent X preview VRAM verified')
finally:r.close()

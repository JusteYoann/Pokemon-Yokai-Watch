#!/usr/bin/env python3
"""Actual Nathan field/four facings and temporary native-VRAM Red reference.

Original Red reference is a rendering fixture, not an active game replacement.
Optional old ROM permits real before/after captures; no ROM/savedata published.
"""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/NATHAN_GABARIT_RED';P.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--before-rom');args=parser.parse_args()
after=os.environ['YOKAI_QA_ROM'];results=[];pictures=[]
def field():
 r=new_game();r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.call('VarSet',0x4050,3);r.call('VarSet',0x4055,9);r.call('SetWarpDestination',3,0,255,8,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 r.call('LockPlayerFieldControls');return r
for stage,path in [('avant',args.before_rom),('apres',after)]:
 if not path:continue
 os.environ['YOKAI_QA_ROM']=path;r=field()
 try:
  obj=r.symbols['gObjectEvents']+36*r.read(r.symbols['gPlayerAvatar']+5,1)[0];south=None
  for d,label in [(1,'sud'),(2,'nord'),(3,'ouest'),(4,'est')]:
   r.call('ObjectEventTurn',obj,d);r.run(30);r.frame.save(P/f'{stage}-{label}.png')
   if d==1:south=r.snapshot();pictures.append((f'Nathan {stage}',r.frame.copy()))
  if stage=='apres':
   for asset,symbol in [('normal','RedNormal'),('surf_run','RedSurfRun'),('bike','RedBike'),('vs_seeker_bike','RedVSSeekerBike'),('fish','RedFish'),('item','RedItem')]:
    b=(ROOT/f'graphics/yokai_characters/nathan/{asset}.4bpp').read_bytes();assert r.read(r.symbols['gObjectEventPic_'+symbol],len(b))==b,(asset,'Linked data differs')
   r.restore(south);sp=r.symbols['gSprites']+68*r.read(obj+4,1)[0];a=int.from_bytes(r.read(sp+4,2),'little');tile=a&1023;bank=a>>12
   src=ROOT/'graphics/object_events/pics/people/red_normal.png';raw=Path('/tmp/nathan-reference-red.4bpp');pal=Path('/tmp/nathan-reference-red.gbapal')
   subprocess.run([str(ROOT/'tools/gbagfx/gbagfx'),str(src),str(raw),'-mwidth','2','-mheight','4'],check=True)
   subprocess.run([str(ROOT/'tools/gbagfx/gbagfx'),str(ROOT/'graphics/object_events/palettes/player.pal'),str(pal)],check=True)
   r.write(0x06010000+tile*32,raw.read_bytes()[:256])
   for table in ['gPlttBufferUnfaded','gPlttBufferFaded']:r.write(r.symbols[table]+512+32*bank,pal.read_bytes())
   r.run(2);r.frame.save(P/'reference-red-carte.png');pictures.insert(0,('Red original - fixture VRAM',r.frame.copy()))
  results.append(dict(stage=stage,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),four_native_facings=True,linked_overworld_resources_match=stage=='apres'))
 finally:r.close()
os.environ['YOKAI_QA_ROM']=after
sheet=Image.new('RGB',(len(pictures)*480,348),(224,224,224));draw=ImageDraw.Draw(sheet)
for i,(label,frame) in enumerate(pictures):draw.text((480*i+4,4),label,fill='black');sheet.paste(frame.resize((480,320),Image.Resampling.NEAREST),(480*i,24))
sheet.save(P/'COMPARAISON_CARTE.png');(P/'TEST_CARTE_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,results=results),ensure_ascii=False,indent=2)+'\n');print('PASS native map four facings, exact six resource links and Red rendering reference')

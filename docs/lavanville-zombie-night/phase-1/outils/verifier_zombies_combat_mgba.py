#!/usr/bin/env python3
"""Real mGBA visual-only battle fixture; artwork uploads, no ROM edits.
Uses an existing species as an explicit RAM opponent template, not a new zombie species.
Capture/run/stats/AI/entry mechanics are NOT implemented or tested here.
"""
import os,sys,re,struct,json,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'tools/yokai'))
from mgba_new_game import new_game
Q=Path(os.environ.get('YOKAI_ZOMBIE_BATTLE_REPORT',str(R/'docs/lavanville-zombie-night/phase-1/prototypes/zombies-combat')));Q.mkdir(parents=True,exist_ok=True);G=R/'graphics/yokai_zombies'
profile_path=os.environ.get('YOKAI_ZOMBIE_PRESENTATION_PROFILE');profiles=json.loads(Path(profile_path).read_text())['profiles'] if profile_path else {}
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(R/'charmap.txt').read_text(),re.M)}
r=new_game();base=r.snapshot();rows=[];screens=[]
callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
try:
 for index,(name,nick) in enumerate([('errant','ERRANT'),('sprinteur','SPRINTEUR'),('colosse','COLOSSE'),('spectral','SPECTRAL')]):
  r.restore(base);r.call('CreateMon',r.symbols['gPlayerParty'],1,25,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('CreateMon',r.symbols['gEnemyParty'],9,25,31,1,100,0,0);r.write(r.symbols['gEnemyPartyCount'],b'\1')
  scratch=r.PARAMS+128;r.write(scratch,bytes(glyphs[c] for c in nick)+b'\xff');r.call('SetMonData',r.symbols['gEnemyParty'],2,scratch)
  r.call('StartScriptedWildBattle')
  for f in range(7000):
   r.keys={0} if f%16<2 else set();r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
  else:
   r.frame.save(Q/'diagnostic-timeout.png');raise AssertionError('Action menu not reached')
  r.keys=set();r.run(60)
  for i in range(4):r.w32(r.symbols['gBattlerControllerFuncs']+4*i,r.symbols['BattleControllerDummy']|1)
  for side in [0,1]:r.call('EndBounceEffect',side,0);r.call('EndBounceEffect',side,1)
  r.run(3);old=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0];sp=r.symbols['gSprites']+68*old;attr=struct.unpack('<H',r.read(sp+4,2))[0];bank=attr>>12;pos=struct.unpack('<hhhh',r.read(sp+32,8));x=pos[0]+pos[2];y=pos[1]+pos[3]
  r.write(sp+62,bytes([r.read(sp+62,1)[0]|4]));mem=r.call('AllocZeroed',2304);assert mem
  tiles=(G/name/'battle-front.4bpp').read_bytes();pal=(G/name/'battle-front.gbapal').read_bytes();assert len(tiles)==2048 and len(pal)==32
  r.write(mem,tiles);r.write(mem+2048,pal);tag=0xF200+index;r.write(mem+2080,struct.pack('<IHH',mem,2048,tag));start=r.call('LoadSpriteSheet',mem+2080)
  r.call('LoadPalette',mem+2048,256+16*bank,32)
  presentation=profiles.get(name);mode=0x300 if presentation else 0
  if presentation:x,y=presentation['center_x'],presentation['center_y']
  r.write(mem+2088,struct.pack('<4H',mode,0xC000,attr&0xFC00,0));r.write(mem+2096,struct.pack('<HHIIIII',tag,0xFFFF,mem+2088,r.symbols['gDummySpriteAnimTable'],0,r.symbols['gDummySpriteAffineAnimTable'],r.symbols['SpriteCallbackDummy']|1));sprite=r.call('CreateSprite',mem+2096,x,y,0x80);assert sprite<64
  inverse=256;matrix=None
  if presentation:
   inverse=round(65536/presentation['scale_q8']);matrix=r.call('GetSpriteMatrixNum',r.symbols['gSprites']+68*sprite);assert matrix<32;r.call('SetOamMatrix',matrix,inverse,0,0,inverse)
  r.run(8);actualbank=struct.unpack('<H',r.read(r.symbols['gSprites']+68*sprite+4,2))[0]>>12;assert actualbank==bank;assert r.read(r.symbols['gPlttBufferFaded']+512+32*bank,32)==pal
  r.frame.save(Q/f'mgba-{name}-natif.png');r.frame.resize((720,480),Image.Resampling.NEAREST).save(Q/f'mgba-{name}-x3.png');screens.append(r.frame.copy())
  full=r.frame.copy();flag=r.symbols['gSprites']+68*sprite+62;r.write(flag,bytes([r.read(flag,1)[0]|4]));r.run(2);empty=r.frame.copy();diff=ImageChops.difference(full.convert('RGB'),empty.convert('RGB')).crop((110,0,240,74)).getbbox();visible=[diff[0]+110,diff[1],diff[2]+110,diff[3]] if diff else None
  source=Image.open(G/name/'battle-front.png');box=source.convert('RGBA').getbbox();projected=[x+(box[0]-32)*256/inverse,y+(box[1]-32)*256/inverse,x+(box[2]-32)*256/inverse,y+(box[3]-32)*256/inverse]
  rows.append(dict(visible_bbox=visible,source_projected_bbox=projected,flame_clipped_at_top=projected[1]<0,affine_matrix=matrix,inverse_scale_q8=inverse,actual_display_scale=256/inverse,variant=name,native_sheet_uploaded=True,sprite_id=sprite,palette_bank=bank,tile_start=start,visible=True,position=[x,y],template_species=9,level=25,visual_only=True))
 result=dict(engine='mGBA libretro',rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_unchanged=True,presentation_profile=profile_path,scope=__doc__,results=rows)
finally:r.close()
board=Image.new('RGB',(480,320))
for i,im in enumerate(screens):board.paste(im,(240*(i%2),160*(i//2)))
board.resize((960,640),Image.Resampling.NEAREST).save(Q/'quatre-combats-mgba-x2.png');(Q/'TEST_MGBA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))

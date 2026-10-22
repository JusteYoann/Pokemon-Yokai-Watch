#!/usr/bin/env python3
"""Native registered trainer portraits on a battle fixture; no graphics injection.
This proves graphics loading and display, not scripted Agent X/new-character battles.
"""
import hashlib,json,os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from mgba_rpc import ROOT
from mgba_new_game import new_game
OUT=ROOT/os.environ.get('YOKAI_PORTRAITS_REPORT','QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/PORTRAITS_ARCHIVE');OUT.mkdir(parents=True,exist_ok=True)
new=[('agent_x',160)]+list(zip(['alyzon_bie','berenice_belier','inspecteur_giraud','lady_perpetua','laure','marge','mc_kraken','steve_jaws','whisper_humain','nathaniel_age','enma_humain','zazel','yopple_bot','enma_ancien'],range(161,175)))
old=[('ariane',148),('wyatt',152),('don_morleone',156),('michael',151),('nathaniel',150),('enma',149),('mafiamille_1',157),('mafiamille_2',158),('mafiamille_3',159)]
r=new_game();report=dict(passed=False,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_bytes=len(r.rom_buffer.raw)-1,engine='mGBA libretro',scope=__doc__,graphics_injected=False,results=[])
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.w32(r.symbols['gTrainerBattleOpponent_A'],17);r.call('StartTrainerBattle');r.run(401)
 oldsprite=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0];sp=r.symbols['gSprites']+68*oldsprite;r.write(sp+62,bytes([r.read(sp+62,1)[0]|4]));r.w32(sp+28,r.symbols['SpriteCallbackDummy']|1)
 frames=[]
 for actor,pic in new+old:
  p=ROOT/'graphics/yokai_characters'/actor;im=Image.open(p/'battle.png');assert im.mode=='P' and im.size==(64,64) and im.info['transparency']==0 and max(im.tobytes())<16
  sid=r.call('CreateTrainerPicSprite',pic,1,176,40,8,0xffff);assert sid<64,(actor,sid)
  r.run(3);sprite=r.symbols['gSprites']+68*sid;attr=int.from_bytes(r.read(sprite+4,2),'little');bank=attr>>12;tile=attr&1023
  assert r.read(0x06010000+32*tile,2048)==(p/'battle.4bpp').read_bytes(),actor
  # Ariane uses a different palette file; compare PNG-authored 5-bit colors.
  palette=im.getpalette();expected=b''.join(((palette[3*i]>>3)|((palette[3*i+1]>>3)<<5)|((palette[3*i+2]>>3)<<10)).to_bytes(2,'little')for i in range(16))
  assert r.read(0x05000200+32*bank,32)==expected,actor
  frame=r.frame.copy();frame.save(OUT/f'{actor}-combat-mgba.png');frames.append((actor,frame))
  report['results'].append(dict(actor=actor,trainer_pic=pic,created_this_lot=pic>=160,source=str((p/'battle.png').relative_to(ROOT)),png_sha256=hashlib.sha256((p/'battle.png').read_bytes()).hexdigest(),tiles_verified=True,palette_verified=True,native_dimensions=[64,64],screenshot=f'{actor}-combat-mgba.png'))
  r.call('FreeAndDestroyTrainerPicSprite',sid)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14);board=Image.new('RGB',(960,((len(frames)+3)//4)*184),(232,232,232));draw=ImageDraw.Draw(board)
 for i,(actor,frame)in enumerate(frames):
  x=i%4*240;y=i//4*184;board.paste(frame,(x,y));draw.text((x+5,y+162),actor.replace('_',' '),font=font,fill='black')
 board.save(OUT/'captures-combat-mgba-24.png');report['passed']=True
 report['limitations']=['Native graphics calls on a battle fixture, not 24 scripted encounters or teams','New portraits await artistic approval','Existing accepted battle PNGs unchanged','No original reference artworks published']
 print('PASS',len(frames),'compiled trainer portraits; native tiles and palettes exact')
finally:r.close();(OUT/'CONTROLE.json').write_text(json.dumps(report,indent=2)+'\n')

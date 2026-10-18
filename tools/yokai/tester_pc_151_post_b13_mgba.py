#!/usr/bin/env python3
"""All151 actual PC-box icons, with explicit populated-box and native-menu fixtures."""
import hashlib,json,os
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/os.environ.get('YOKAI_PC_REPORT_DIR','QA_RECETTE_FINALE/POST_B13/sprites/pc-lot2');P.mkdir(parents=True,exist_ok=True);r=new_game();checks=[];passed=False;error='Interrupted'
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 for n in range(1,152):
  box=(n-1)//30;slot=(n-1)%30;ptr=r.call('GetBoxedMonPtr',box,slot);r.call('CreateBoxMon',ptr,n,30,31,1,100,1,0)
 base=r.snapshot()
 for box in range(6):
  r.restore(base);r.call('SetCurrentBox',box);r.call('EnterPokeStorage',2);r.run(1500);assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_PokeStorage']|1
  r.frame.save(P/f'boite-{box+1}.png');ids=list(range(1+30*box,min(152,31+30*box)));checks.append(dict(box=box+1,species=ids,native_storage_screen=True));print('PC',box+1,flush=True)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_PC_151.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Real new-game init; explicit box contents and EnterPokeStorage fixture, actual PC screen rendered. Not proof of all deposit/withdraw/item operations',results=checks),ensure_ascii=False,indent=2)+'\n')
if passed:
 canvas=Image.new('RGB',(1000,1050),(224,224,224));d=ImageDraw.Draw(canvas)
 for box in range(6):
  x=box%2*500;y=box//2*350;d.text((x+4,y+2),f'Boite {box+1}',fill='black');canvas.paste(Image.open(P/f'boite-{box+1}.png').resize((480,320),Image.Resampling.NEAREST),(x+4,y+22))
 canvas.save(P/'planche-pc.png')

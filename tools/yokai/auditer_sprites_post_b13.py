#!/usr/bin/env python3
"""Audit all 151 assets and capture native mGBA combat scenes; no sprite editing."""
import argparse,csv,hashlib,json,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from mgba_rpc import Emulator,ROOT
P=ROOT/'QA_RECETTE_FINALE/POST_B13'
USE_DISPLAY=False
NAMES=json.loads((ROOT/'data/yokai/noms_affiches.json').read_text())

def visible(path):
 im=Image.open(path);assert im.mode=='P',(path,im.mode)
 display=path.with_name(path.stem+'-display.4bpp')
 if USE_DISPLAY and display.exists():
  from presentation_4bpp import decode
  pixels=decode(display.read_bytes(),im.width,im.height)
  shown=Image.new('P',im.size);shown.putpalette(im.getpalette());shown.putdata([v for row in pixels for v in row]);im=shown
 alpha=im.point(lambda i:255 if i else 0).convert('L')
 # Palette indices, not RGB colors, define transparent index zero.
 mask=Image.new('L',im.size);mask.putdata([255 if i else 0 for i in im.getdata()])
 rgba=im.convert('RGBA');rgba.putalpha(mask)
 return rgba

def metric(path):
 im=visible(path);box=im.getbbox();assert box,(path,'empty')
 points=[(x,y) for y in range(im.height) for x in range(im.width) if im.getpixel((x,y))[3]]
 return {'dimensions':list(im.size),'visible_bbox':list(box),'occupied_pixels':len(points),'centroid':[round(sum(x for x,y in points)/len(points),2),round(sum(y for x,y in points)/len(points),2)],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def capture(stage):
 out=P/'sprites'/stage;out.mkdir(parents=True,exist_ok=True)
 r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 callbacks={int(line.split()[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(line.split())==3 and line.split()[2]=='HandleInputChooseAction'}
 r.keys=set();base=r.snapshot();rows=[]
 try:
  for n in NAMES:
   sid=int(n['species_id']);r.restore(base)
   for slot in ['gPlayerParty','gEnemyParty']:r.call('CreateMon',r.symbols[slot],sid,30,31,1,100,0,0)
   r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.write(r.symbols['gEnemyPartyCount'],b'\x01');r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],33,0)
   r.call('StartScriptedWildBattle')
   for f in range(6000):
    r.keys={0} if f%16<2 else set();r.run()
    if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
   else:raise AssertionError(('battle not ready',sid))
   r.keys=set();r.run(12);r.frame.save(out/f'{sid:03d}.png')
   row={'number':sid,'name':n['nom_yokai'],'native_capture':str((out/f'{sid:03d}.png').relative_to(ROOT)),'battle_fixture':True,'human_reviewed':False}
   for asset in ['front','back','icon']:row[asset]=metric(ROOT/f'graphics/yokai/{sid:03d}/{asset}.png')
   positions={}
   for side,label in [(0,'back'),(1,'front')]:
    sp=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+side,1)[0]
    positions[label]=list(struct.unpack('<hhhh',r.read(sp+32,8)))
   row['native_positions_x_y_x2_y2']=positions;rows.append(row)
   if sid%15==0:print('CAPTURE',sid,flush=True)
 finally:r.close()
 report={'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'stage':stage,'species_count':len(rows),'scope':'Native scripted wild battle fixtures, each species on player and opponent sides; no human visual approval implied; icons source-asset view, not native menu capture','species':rows}
 (out/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report

def sheets(report,stage):
 out=P/'sprites'/stage
 for page in range(10):
  subset=report['species'][page*16:(page+1)*16]
  canvas=Image.new('RGB',(1088,1120),(224,224,224));d=ImageDraw.Draw(canvas)
  for i,n in enumerate(subset):
   x=(i%4)*272;y=(i//4)*280
   d.text((x+6,y+4),f"{n['number']:03d} {n['name']}",fill='black')
   canvas.paste(Image.open(ROOT/n['native_capture']),(x+16,y+24))
   for j,asset in enumerate(['front','back','icon']):
    im=visible(ROOT/f"graphics/yokai/{n['number']:03d}/{asset}.png")
    if asset=='icon':im=im.crop((0,0,32,32)).resize((64,64),Image.Resampling.NEAREST)
    # checkerboard preview only; original transparent sprites are unchanged.
    for yy in range(0,64,8):
     for xx in range(0,64,8):d.rectangle((x+16+j*82+xx,y+194+yy,x+23+j*82+xx,y+201+yy),fill=(192,192,192) if (xx+yy)//8%2 else (240,240,240))
    canvas.paste(im,(x+16+j*82,y+194),im)
   d.text((x+16,y+260),'Face       Dos        Icone',fill='black')
  canvas.save(out/f'planche-{page+1:02d}.png')

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--stage',default='baseline-b13');a.add_argument('--sheets-only',action='store_true');args=a.parse_args()
 USE_DISPLAY=args.stage!='baseline-b13'
 report=json.loads((P/'sprites'/args.stage/'audit.json').read_text()) if args.sheets_only else capture(args.stage)
 sheets(report,args.stage)
 print('PASS',len(report['species']),'native front/back scenes; source icon review sheets, no original graphics changed')

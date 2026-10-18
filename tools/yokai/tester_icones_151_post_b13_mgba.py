#!/usr/bin/env python3
"""All151 species in actual party menus, opened via Start/D-pad/A after real intro."""
import hashlib,json,os
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/os.environ.get('YOKAI_ICONS_REPORT_DIR','QA_RECETTE_FINALE/POST_B13/sprites/icones-menu');P.mkdir(parents=True,exist_ok=True)
r=new_game();r.call('FlagSet',0x828);r.call('FlagSet',0x829);base=r.snapshot();checks=[]
def pulse(key,after=60):
 r.keys=set();r.run(6);r.keys={key};r.run(8);r.keys=set();r.run(after)
try:
 for start in range(1,152,6):
  ids=list(range(start,min(152,start+6)));r.restore(base)
  for i,species in enumerate(ids):
   r.call('CreateMon',r.symbols['gPlayerParty']+100*i,species,30,31,1,100,1,0)
  r.write(r.symbols['gPlayerPartyCount'],bytes([len(ids)]))
  r.run(120);pulse(3,180);order=list(r.read(r.symbols['sStartMenuOrder'],r.read(r.symbols['sNumStartMenuItems'],1)[0]));index=order.index(1)
  for _ in range(index):pulse(5,20)
  assert r.read(r.symbols['sStartMenuCursorPos'],1)[0]==index
  pulse(8,600);assert r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1
  r.frame.save(P/f'groupe-{start:03d}.png')
  checks.append({'species':ids,'native_party_menu_opened':True,'screenshot':str((P/f'groupe-{start:03d}.png').relative_to(ROOT))})
  print('PARTY ICONS',ids,flush=True)
finally:r.close()
for page in range(3):
 canvas=Image.new('RGB',(1000,1392),(224,224,224));d=ImageDraw.Draw(canvas)
 for i,row in enumerate(checks[page*8:(page+1)*8]):
  x=i%2*500;y=i//2*348
  d.text((x+4,y+3),' / '.join(f'{n:03d}' for n in row['species']),fill='black')
  frame=Image.open(ROOT/row['screenshot']).resize((480,320),Image.Resampling.NEAREST)
  canvas.paste(frame,(x+4,y+20))
 canvas.save(P/f'planche-menu-{page+1:02d}.png')
# Last2 groups not present on first3 sheets get their own fourth sheet.
if len(checks)>24:
 canvas=Image.new('RGB',(1000,360),(224,224,224));d=ImageDraw.Draw(canvas)
 for i,row in enumerate(checks[24:]):
  d.text((i*500+4,3),' / '.join(f'{n:03d}' for n in row['species']),fill='black')
  canvas.paste(Image.open(ROOT/row['screenshot']).resize((480,320),Image.Resampling.NEAREST),(i*500+4,24))
 canvas.save(P/'planche-menu-04.png')
assert [n for c in checks for n in c['species']]==list(range(1,152))
(P/'TEST_ICÔNES_151.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'species_count':151,'scope':'Real new game then explicit party fixtures; actual party menu via controller. Screenshots for all species; no full PC-menu coverage or human approval implied','groups':checks},ensure_ascii=False,indent=2)+'\n')

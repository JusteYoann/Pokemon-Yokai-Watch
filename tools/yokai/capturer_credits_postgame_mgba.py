#!/usr/bin/env python3
"""Photographies natives préparées pour les crédits postgame, hors aventure filmée.
Cartes, progression et équipes de test sont des fixtures isolées.
"""
import json,hashlib,subprocess,os
from pathlib import Path
from PIL import Image,ImageOps
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/os.environ.get('YOKAI_CREDITS_POSTGAME_DIR','docs/credits-postgame-yoann-20261025');D.mkdir(exist_ok=True)
board=json.loads((ROOT/'data/yokai/credits_storyboard.json').read_text())['slides']
rows=[];declarations=[];tables=[]
base_header=(ROOT/'src/data/yokai_credits.h').read_text()
import re
base_rows=re.findall(r'\{sCreditTiles_(\w+), (sCreditMap_\w+), sCreditPal_\w+\}',base_header)
for gender,label in enumerate(('garcon','fille')):
 q=QA('TEMP_PHOTOS.json');r=q.r;assets=[]
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
  q.mon();q.f(0x82c)
  def capture(index,title):
   native=D/f'{label}-{index}-native.png';r.frame.save(native)
   s=board[index];photo=ImageOps.fit(r.frame.convert('RGB'),(s['width'],s['height']),method=Image.Resampling.NEAREST).quantize(colors=95,dither=Image.Dither.NONE)
   im=Image.new('P',photo.size);im.putpalette([0,0,0]+photo.getpalette()[:285]+[0]*480);im.putdata([v+1 for v in photo.getdata()])
   stem=f'postgame-{label}-{index}';im.save(ROOT/f'graphics/yokai_credits/{stem}.png')
   subprocess.run(['python3',str(ROOT/'tools/yokai/preparer_souvenirs_credits.py'),'--pack',stem],check=True)
   suffix=stem.replace('-','_')
   for kind,typ,ext in [('Tiles','u32','8bpp.lz'),('Pal','u16','gbapal')]:
    declarations.append(f'static const {typ} sCredit{kind}_{suffix}[] = INCBIN_{"U16" if typ=="u16" else "U32"}("graphics/yokai_credits/{stem}.{ext}");')
   assets.append(f'    {{sCreditTiles_{suffix}, {base_rows[gender*32+index][1]}, sCreditPal_{suffix}}},')
   rows.append(dict(gender=label,index=index,title=title,native_capture=str(native.relative_to(ROOT)),source_rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),colors=95))
   print('PASS capture',label,index,title,flush=True)
  q.warp('PalletTown_PlayersHouse_1F',6,6);q.warp('PalletTown',6,7)
  q.wait(lambda:q.local('LOCALID_PG_ENMA_INTRO') in q.actors(),1000,False)
  r.run(40);r.call('ScriptContext_Init');r.call('HideFieldMessageBox');r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents');r.run(8)
  capture(27,'La rencontre avec le Seigneur Enma')
  # Stop this scene by loading a separate prepared map; nothing is saved.
  r.call('ScriptContext_Init');r.call('UnlockPlayerFieldControls');q.f(0x32f)
  q.f(0x806);q.warp('CeruleanCave_1F',22,20);r.keys=set();r.run(300);r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents');r.run(4)
  capture(28,'Maître Nyada et Démophage dans la Grotte Azurée')
  r.call('ScriptContext_Init');r.call('UnlockPlayerFieldControls')
  q.mon(0,6,70) # Komaous, requested protagonist for the Robonyan 28 shiny memory.
  q.f('FLAG_PG_SCIENTIST_1');q.f('FLAG_PG_SCIENTIST_2');q.warp('SaffronCity',19,23);q.script('PG_ScientistYopple')
  q.wait(lambda:q.callback()=='BattleMainCB2',30000)
  actions={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
  q.wait(lambda:r.u32(r.symbols['gBattlerControllerFuncs']) in actions,12000);r.keys=set();r.run(8)
  assert r.call('GetMonData',r.symbols['gPlayerParty'],11,0)==6
  assert r.call('GetMonData',r.symbols['gEnemyParty'],11,0)==19 and r.call('IsMonShiny',r.symbols['gEnemyParty'])
  capture(29,'Komaous face à Robonyan 28 shiny')
  # A fresh emulator isolates the next battle from the unfinished scientist fight.
 finally:r.close()
 q=QA('TEMP_PHOTOS.json');r=q.r
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));q.mon();q.f(0x331);q.warp('PalletTown_PlayersHouse_2F',6,3)
  q.script('Yoann_EventScript_NPC');q.wait(lambda:q.callback()=='BattleMainCB2',18000)
  def portrait():
   sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
   if sid>=64:return False
   p=r.symbols['gSprites']+68*sid
   return bool(r.read(p+62,1)[0]&1) and int.from_bytes(r.read(p+6,2),'little')==167 and r.read(p+36,2)==b'\0\0'
  q.wait(portrait,12000);r.keys=set();r.run(8);capture(30,'Le combat final contre Juste Yoann')
 finally:r.close()
 tables.append('{\n'+'\n'.join(assets)+'\n}')
declarations.append('static const struct CreditAssets sPostgameCreditAssets[2][4] = {\n'+',\n'.join(tables)+'\n};\n')
(ROOT/'src/data/yokai_credits_postgame.h').write_text('\n'.join(declarations))
(D/'PHOTOS.json').write_text(json.dumps({'scope':__doc__,'captures':rows,'final_group_unchanged':True},ensure_ascii=False,indent=2)+'\n')

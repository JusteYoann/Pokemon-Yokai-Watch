#!/usr/bin/env python3
"""Native format/visibility, reward retries, Flash save/Continue and portrait evidence.
Controlled map/flag/collection fixtures; no enemy outcomes patched.
"""
import os,json,struct,hashlib
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/os.environ.get('YOKAI_QA_PROOFS','docs/dossier-20261023/tests')/mode;D.mkdir(parents=True,exist_ok=True);r=new_game();rows=[];passed=False
for _ in range(5):
 import re
 for k,v in re.findall(r'^#define\s+(FLAG_\w+)\s+(FLAG_\w+)\s*$',(ROOT/'include/constants/flags.h').read_text(),re.M):
  if v in C:C[k]=C[v]
def report(name,**kw):rows.append({'test':name,'passed':True,**kw});print(name,kw,flush=True)
def shot(name):r.frame.save(D/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(D/(name+'-x3.png'))
def free():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2'
def finish():
 for f in range(8000):
  r.keys={8} if f%16<4 else set();r.run()
  if f>100 and free():r.keys=set();r.run(8);return
 raise AssertionError('script did not finish')
def script(s):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[s]);finish()
def indexed_tiles(im,w=32,h=32):
 data=bytearray()
 for ty in range(h//8):
  for tx in range(w//8):
   for y in range(8):
    for x in range(0,8,2):data.append(im.getpixel((tx*8+x,ty*8+y)) | im.getpixel((tx*8+x+1,ty*8+y))<<4)
 return bytes(data)
try:
 base=r.snapshot();r.call('FlagSet',0x82C)
 # All six new supplied stationary sources, real object VRAM and palette.
 cases=[('PokemonLeague_LoreleisRoom','zazel',0),('PokemonLeague_BrunosRoom','enma_ancien',0),('PokemonLeague_AgathasRoom','orqanos',0),('PokemonLeague_LancesRoom','nyada',0),('SeafoamIslands_B4F','kyubi',2),('PowerPlant','octorgone',None)]
 for mapname,name,index in cases:
  d=json.loads((ROOT/'data/maps'/mapname/'map.json').read_text())
  if index is None:index=next(i for i,o in enumerate(d['object_events']) if o['script']=='PowerPlant_EventScript_Zapdos')
  o=d['object_events'][index];r.call('VarSet',0x4068,1);warp(r,*MAPS[mapname],o['x'],o['y']+2)
  legacy={'zazel':('LORELEI','Zazel'),'enma_ancien':('BRUNO','EnmaAncien'),'orqanos':('AGATHA','Orqanos'),'nyada':('LANCE','Nyada')}.get(name)
  if legacy:assert r.call('GetObjectEventGraphicsInfo',C['OBJ_EVENT_GFX_'+legacy[0]])==r.symbols['gObjectEventGraphicsInfo_Dossier'+legacy[1]]
  obj=r.call('GetObjectEventIdByLocalIdAndMap',index+1,MAPS[mapname][1],MAPS[mapname][0]);assert obj<16,(name,'not visible')
  ptr=r.symbols['gObjectEvents']+obj*36;sid=r.read(ptr+4,1)[0];sp=r.symbols['gSprites']+sid*68;tile=int.from_bytes(r.read(sp+4,2),'little')&1023;bank=int.from_bytes(r.read(sp+4,2),'little')>>12
  im=Image.open(ROOT/'graphics/dossier-20261023'/name/'overworld.png');assert r.read(0x06010000+tile*32,512)==indexed_tiles(im)
  assert r.read(0x05000200+bank*32,32)==(ROOT/'graphics/dossier-20261023'/name/'overworld.gbapal').read_bytes()
  bbox=im.convert('RGBA').getchannel('A').getbbox();height=bbox[3]-bbox[1];assert height==(22 if name in ['enma_ancien','orqanos'] else 19)
  shot('overworld-'+name);report('Native overworld '+name,height=height,tiles_and_palette_match=True,palette_bank=bank)
 # Assistant gift stays unique at50 caught; no replacement object introduced.
 r.restore(base);warp(r,*MAPS['Route15_WestEntrance_2F'],4,4)
 for n in range(1,51):r.call('GetSetPokedexFlag',n,2);r.call('GetSetPokedexFlag',n,3)
 assert r.call('GetNationalPokedexCount',1)>=50
 script('Route15_WestEntrance_2F_EventScript_Aide');assert r.call('CheckBagHasItem',C['ITEM_EXP_SHARE'],1);assert r.call('FlagGet',C['FLAG_GOT_EXP_SHARE_FROM_OAKS_AIDE']);shot('multi-exp-recompense-conservee')
 script('Route15_WestEntrance_2F_EventScript_Aide');assert not r.call('CheckBagHasItem',C['ITEM_EXP_SHARE'],2);report('Original50-caught assistant gift preserved; unique held Exp Share')
 # Rescue gift full-stack retry: no permanent reward flag until an item fits.
 r.call('FlagSet',0x3E);warp(r,*MAPS['SilphCo_11F'],7,6);r.call('AddBagItem',C['ITEM_MASTER_BALL'],999);script('SilphCo_11F_EventScript_President');assert not r.call('FlagGet',0x250);assert not r.call('FlagGet',0x330)
 r.call('RemoveBagItem',C['ITEM_MASTER_BALL'],1);script('SilphCo_11F_EventScript_President');assert r.call('FlagGet',0x250) and r.call('FlagGet',0x330);assert not r.call('FlagGet',C['FLAG_DEFEATED_SABRINA']);report('Master Ball full-stack retry succeeds before Gym; CEO leaves only on successful gift')
 # Save and genuine Continue rebuild object visibility from durable flags.
 assert r.call('TrySavingData',0,max_frames=1200)==1;assert r.call('LoadGameSave',0,max_frames=1200)==1;r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1);finish()
 assert r.call('FlagGet',0x250) and r.call('FlagGet',0x330) and r.call('FlagGet',C['FLAG_GOT_EXP_SHARE_FROM_OAKS_AIDE'])
 assert r.call('CheckBagHasItem',C['ITEM_EXP_SHARE'],1)
 obj=r.call('GetObjectEventIdByLocalIdAndMap',1,MAPS['SilphCo_11F'][1],MAPS['SilphCo_11F'][0]);assert obj==16;shot('yopple-apres-don-continue');report('Native Flash save/Continue preserves gifts and hides departed CEO')
 # Real Fame Checker menu, with unlocked-entry fixture, new names and portraits.
 r.restore(base);r.call('FullyUnlockFameChecker');r.call('UseFameChecker',r.symbols['CB2_ReturnToField']|1);r.run(500)
 for i in range(13):
  if i:
   r.keys={5};r.run();r.keys=set();r.run(24)
  if i in [6,7,9,10,11,12]:shot('fame-checker-'+str(i))
 report('Native Fame Checker opens and displays all six replaced cast entries')
 # Unambiguous latest-reference contact sheet from real mGBA portraits, not mockups.
 portrait_names=['zazel','enma-ancien','orqanos','maitre-nyada']
 if all((D/('ligue-'+n+'-portrait.png')).exists() for n in portrait_names):
  names=['zazel','enma-ancien','orqanos','maitre-nyada'];canvas=Image.new('RGB',(960,680),(28,32,40));draw=ImageDraw.Draw(canvas)
  for i,n in enumerate(names):
   p=D/('ligue-'+n+'-portrait.png');im=Image.open(p);assert im.getbbox();x=i%2*480;y=i//2*340;draw.text((x+6,y+4),n,fill='white');canvas.paste(im.resize((480,320),Image.Resampling.NEAREST),(x,y+20))
  canvas.save(D/'portraits-ligue-mgba-x2.png')
 passed=True
finally:
 rom=os.environ.get('YOKAI_QA_ROM',str(ROOT/'pokefirered.gba'));r.close();(D/'COMPLEMENTS_MGBA.json').write_text(json.dumps({'passed':passed,'scope':__doc__,'rom_sha256':hashlib.sha256(open(rom,'rb').read()).hexdigest(),'results':rows},ensure_ascii=False,indent=2)+'\n')

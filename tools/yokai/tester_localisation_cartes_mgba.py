#!/usr/bin/env python3
"""Render a named translation batch in native field-message windows.
Fixtures keep the player on one map, restore field state between messages,
and provide bounded variables. This is not traversal of all actual NPCs.
"""
import argparse,hashlib,json,re
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
p=argparse.ArgumentParser();p.add_argument('--lot',required=True);p.add_argument('tables',nargs='+');a=p.parse_args()
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR'/a.lot;P.mkdir(exist_ok=True)
rowsource=[]
for name in a.tables:
 for row in (ROOT/name).read_text().splitlines():
  if not row or row.startswith('#'):continue
  source,key,text=row.split('\t',2);rowsource.append((source,key,text))
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
r=new_game();rows=[];shots=[];passed=False;error='Interrupted'
try:
 r.call('SetWarpDestination',3,0,255,10,10);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 # Longest player-name fixture, fixed Matt, wide species/item/number variables.
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyph[c] for c in 'WWWWWWW')+b'\xff')
 for name,value in [('gStringVar1','WWWWWWWWWW'),('gStringVar2','999999'),('gStringVar3','999')]:r.write(r.symbols[name],bytes(glyph[c] for c in value)+b'\xff')
 dest=r.call('AllocZeroed',1024);values=r.call('AllocZeroed',512);assert dest and values
 base=r.snapshot()
 for i,(source,key,text) in enumerate(rowsource):
  r.restore(base);pointer=r.symbols[key]
  if '{DYNAMIC ' in text:
   schemas={
    'gText_UR_TrainerCardInfoPage1':['W'*12,'W'*7,"C'est une Carte de bronze!",'151','999','59'],
    'gText_UR_TrainerCardInfoPage2':['9999','','9999','99999']+['W'*12]*4,
    'gText_UR_OfferToTradeMon':['100','W'*10,'100','W'*10]}
   content=schemas.get(key,['W'*7]*8)
   r.call('DynamicPlaceholderTextUtil_Reset')
   for j,value in enumerate(content):
    address=values+j*64;r.write(address,bytes(glyph[c] for c in value)+b'\xff');r.call('DynamicPlaceholderTextUtil_SetPlaceholderPtr',j,address)
   r.write(dest,b'\xa5'*1024);end=r.call('DynamicPlaceholderTextUtil_ExpandPlaceholders',dest,pointer)
   assert end-dest+1<1024,(key,'Expanded message overflow')
   if key.startswith('gText_UR_TrainerCardInfoPage'):
    assert end-dest+1<=200 and r.read(dest+200,1)==b'\xa5',(key,'Native200-byte card message capacity')
    for line in re.split(b'[\xfe\xfa\xfb]',r.read(dest,end-dest)):
     r.write(dest+768,line+b'\xff');width=r.call('GetStringWidth',2,dest+768,0);assert width<=208,(key,width)
   pointer=dest
  assert r.call('ShowFieldMessage',pointer)==1,key;r.run(300)
  data=r.call('GetWindowAttribute',0,7);assert len(set(r.read(data,1600)))>1,(key,'No rendered text')
  rows.append(dict(symbol=key,source=source,native_first_page=True,dynamic_fixture=('{DYNAMIC ' in text)))
  if i%17==0 or key in ['VermilionCity_Gym_Text_SwitchUnderTrashFirstLockOpened','VermilionCity_House2_Text_DoYouHaveMonWantToTradeForMyMon','VermilionCity_PokemonFanClub_Text_ExplainBikeVoucher']:
   r.frame.save(P/(key+'.png'));shots.append(key)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Native first-page rendering of each source message on a fixed field-map fixture with explicit variables. Dynamic placeholders explicitly expanded before rendering; native200-byte trainer-card bound checked. Not full NPC traversal, all pages, multiplayer or event-outcome testing.',results=rows,captures=shots),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(720,((len(shots)+2)//3)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,key in enumerate(shots):
  x=i%3*240;y=i//3*184;d.text((x+2,y+2),key[:34],fill='black');sheet.paste(Image.open(P/(key+'.png')),(x,y+22))
 sheet.save(P/'PLANCHE.png');print('FIELD BATCH FR PASS',len(rows),len(shots))

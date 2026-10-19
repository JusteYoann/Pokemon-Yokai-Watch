#!/usr/bin/env python3
"""All translated item names/descriptions from native pointers; actual bag panel."""
import hashlib,json,re
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/objets';P.mkdir(parents=True,exist_ok=True)
entries=json.loads((P.parent/'OBJETS_FR.json').read_text())['entries'];constants={k:int(v) for k,v in re.findall(r'^#define\s+(ITEM_\w+)\s+(\d+)\b',(ROOT/'include/constants/items.h').read_text(),re.M)}
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
r=new_game();results=[];shots=[];passed=False;error='Interrupted'
try:
 for e in entries:
  ident=constants[e['item']];ptr=r.call('ItemId_GetName',ident);expected=bytes(glyph[c] for c in e['display'])+b'\xff';assert r.read(ptr,len(expected))==expected,(e['item'],'Wrong linked item name')
  desc=r.call('ItemId_GetDescription',ident);width=r.call('GetStringWidth',2,desc,0);assert width<=196,(e['item'],width)
  results.append(dict(item=e['item'],linked_name_exact=True,native_description_pixels=width,passed=True))
 r.call('ClearBag');assert r.call('AddBagItem',constants['ITEM_POTION'],1)
 r.call('CB2_BagMenuFromStartMenu');r.run(600)
 assert r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1
 # Explicit rendering fixture: keep pocket0/list index0, substitute a native
 # item identifier into its first slot, then invoke the real bag description.
 # It does not claim the key items can normally be stored in the Items pocket.
 slot=r.u32(r.symbols['gBagPockets'])
 for name in ['ITEM_POTION','ITEM_HYPER_POTION','ITEM_LIGHT_BALL','ITEM_LUCKY_PUNCH','ITEM_THICK_CLUB','ITEM_ITEMFINDER','ITEM_FAME_CHECKER','ITEM_TM_CASE','ITEM_COIN_CASE','ITEM_SUPER_REPEL','ITEM_LUCKY_EGG','ITEM_HELIX_FOSSIL','ITEM_SITRUS_BERRY','ITEM_BLUE_FLUTE','ITEM_SILPH_SCOPE']:
  r.write(slot,constants[name].to_bytes(2,'little'));r.call('PrintItemDescriptionOnMessageWindow',0);r.call('CopyWindowToVram',1,3);r.run(8);r.frame.save(P/(name+'.png'));shots.append(name)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='All298 translated native item names and description widths;15 native bag-panel description fixtures. Not full gameplay testing of item effects or key-item pocket movement.',results=results,captures=shots),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(720,((len(shots)+2)//3)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,key in enumerate(shots):
  x=i%3*240;y=i//3*184;d.text((x+2,y+2),key,fill='black');sheet.paste(Image.open(P/(key+'.png')),(x,y+22))
 sheet.save(P/'PLANCHE.png');print('ITEMS FR PASS',len(results),len(shots))

#!/usr/bin/env python3
"""Native French field messages; warp/variable fixtures, no story-playthrough claim."""
import hashlib,json,re
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/dialogues';P.mkdir(parents=True,exist_ok=True)
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
r=new_game();rows=[];passed=False;error='Interrupted'
samples=['Text_MayIHelpYou','Text_BootedUpPC','Text_AccessedBillsPC','Text_ObtainedTheX','Text_PutItemAway','Text_MonSentToBoxInBillsPC','Trade_Text_DoYouHaveMonWantToTradeForMon','DayCare_Text_YourMonsAreDoingFine','PokedexRating_Text_HowIsPokedexComingAlong','PokedexRating_Text_LessThan60','Text_WantToSurf','Text_OnlyPassWithBadgeOhGoAhead','Text_MonsHealedShouldBuyPotions','Text_HadQuiteAnExperienceTakeRest']
try:
 r.call('SetWarpDestination',3,0,255,10,10);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600);base=r.snapshot()
 for key in samples:
  r.restore(base)
  for name,value in [('gStringVar1','Jibanyan'),('gStringVar2','Potion'),('gStringVar3','le Sac')]:r.write(r.symbols[name],bytes(glyph[c] for c in value)+b'\xff')
  assert r.call('ShowFieldMessage',r.symbols[key])==1,key
  r.run(200)
  # HIDDEN here means the printer completed, not that the frame disappeared.
  tiledata=r.call('GetWindowAttribute',0,7);pixels=r.read(tiledata,128)
  assert len(set(pixels))>1,(key,'Native text window stayed blank')
  r.frame.save(P/(key+'.png'));rows.append(dict(symbol=key,native_field_text_box=True,captured=True))
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Real new-game then PalletTown warp and explicit text variables; native field-message rendering, first page only. Not actual NPC event traversal or all dialogues.',results=rows),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(720,((len(rows)+2)//3)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,row in enumerate(rows):
  x=i%3*240;y=i//3*184;d.text((x+2,y+2),row['symbol'][:33],fill='black');sheet.paste(Image.open(P/(row['symbol']+'.png')),(x,y+22))
 sheet.save(P/'PLANCHE.png');print('FIELD FR PASS',len(rows))

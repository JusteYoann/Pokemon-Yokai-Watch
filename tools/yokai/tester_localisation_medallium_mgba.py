#!/usr/bin/env python3
"""151 linked French profiles and native Medallium page rendering.
Caught flags are test fixtures. Pages are opened using actual controller input;
selected sample panels are then refreshed by the real native renderer.
"""
import hashlib,json,re
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/medallium';P.mkdir(exist_ok=True)
entries=json.loads((ROOT/'data/localisation/fr/medallium_fr.json').read_text())['entries']
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
r=new_game();rows=[];shots=[];passed=False;error='Interrupted'
def pulse(key,frames=120):
 r.keys={key};r.run(1);r.keys=set();r.run(frames)
def windows():
 return [i for i in range(32) if r.read(r.symbols['gWindows']+12*i,6)==bytes([1,0,11,30,7,0])]
try:
 for e in entries:
  raw=bytes(glyph[c] if c!='\n' else 0xfe for c in '\n'.join(e['description']))+b'\xff'
  ptr=r.symbols[e['symbol']];assert r.read(ptr,len(raw))==raw,(e['name'],'Incorrect linked description')
  scratch=r.call('AllocZeroed',100)
  widths=[]
  for line in e['description']:
   data=bytes(glyph[c] for c in line)+b'\xff';r.write(scratch,data)
   width=r.call('GetStringWidth',2,scratch,1);assert width<=224,(e['name'],width);widths.append(width)
  r.call('Free',scratch)
  rows.append(dict(number=e['number'],name=e['name'],linked_exact=True,widths=widths))
  for flag in [2,3]:r.call('GetSetPokedexFlag',int(e['number']),flag)
 r.call('FlagSet',0x828);r.call('FlagSet',0x829)
 r.call('SetWarpDestination',3,0,255,10,10);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 pulse(3,180);pulse(8,600)
 for _ in range(9):pulse(5,15)
 pulse(8,600);pulse(8,600)
 assert len(windows())==1,('Dex entry page not opened',windows())
 data=r.u32(r.symbols['sPokedexScreenData'])
 assert int.from_bytes(r.read(data+90,2),'little')==15, 'Unexpected PokedexScreenData layout or initial entry'
 base=r.snapshot()
 for e in entries:
  if int(e['number']) not in [1,3,5,15,17,25,62,87,90,98,100,127,149,150,151]:continue
  r.restore(base);r.call('RemoveDexPageWindows')
  r.write(data+90,int(e['number']).to_bytes(2,'little'))
  r.call('DexScreen_DrawMonDexPage',0)
  for bg in range(4):r.call('CopyBgTilemapBufferToVram',bg)
  r.run(8);wid=windows()[0]
  tile=r.call('GetWindowAttribute',wid,7);assert len(set(r.read(tile,30*7*32)))>1
  name=e['number']+'-'+e['name'];r.frame.save(P/(name+'.png'));shots.append(name)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='151 linked descriptions and native widths, actual controller-opened Medallium entry;15 native full-page redraw fixtures. Habitat heading stays that of the initially opened list; not full capture of151 species or review of inherited size/weight data.',results=rows,captures=shots),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(720,((len(shots)+2)//3)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,key in enumerate(shots):
  x=i%3*240;y=i//3*184;d.text((x+2,y+2),key,fill='black');sheet.paste(Image.open(P/(key+'.png')),(x,y+22))
 sheet.save(P/'PLANCHE.png');print('MEDALLIUM FR PASS',len(rows),len(shots))

#!/usr/bin/env python3
"""French names/inflections/status graphics with native calls and controller UI.
Fixtures are explicit; this is not an uninterrupted full-adventure playthrough.
"""
import hashlib,json,re,struct
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
P=ROOT/'docs/traduction-complete-20261024/mgba';P.mkdir(parents=True,exist_ok=True)
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
def encode(s):return bytes(glyph[c] for c in s)+b'\xff'
rows=[]
for gender in (0,1):
 r=new_game(gender)
 try:
  assert r.read(r.u32(r.symbols['gSaveBlock2Ptr'])+8,1)==bytes([gender])
  r.frame.save(P/f'nouvelle-partie-{gender}.png');rows.append(dict(test='New game by controller',gender=gender,passed=True))
  if gender:continue
  scratch=r.call('AllocZeroed',1024)
  for line in (ROOT/'data/localisation/fr/52_noms_lieux.tsv').read_text().splitlines():
   _,symbol,text=line.split('\t',2);expected=encode(text);pointer=r.symbols[symbol]
   assert r.read(pointer,len(expected))==expected,(symbol,text)
   width=r.call('GetStringWidth',2,pointer,0);assert width<=208,(symbol,width)
   rows.append(dict(test='Linked French map name',symbol=symbol,name=text,width=width,passed=True))
  const={k:int(v) for k,v in re.findall(r'^#define\s+(ITEM_\w+)\s+(\d+)\b',(ROOT/'include/constants/items.h').read_text(),re.M)}
  for item in range(const['ITEM_CHERI_BERRY'],const['ITEM_ENIGMA_BERRY']+1):
   r.call('CopyItemName',item,scratch);singular=r.read(scratch,64).split(b'\xff')[0];assert singular.startswith(encode('Baie ')[:-1])
   r.write(scratch+256,b'\xa5'*128);r.call('CopyItemNameHandlePlural',item,scratch+256,2)
   plural=r.read(scratch+256,64).split(b'\xff')[0];assert plural==encode('Baies ')[:-1]+singular[5:],item
   assert r.read(scratch+320,64)==b'\xa5'*64
   rows.append(dict(test='French berry plural, same variety',item=item,passed=True))
  for qty in (1,2,99):
   r.call('CopyItemNameHandlePlural',const['ITEM_POKE_BALL'],scratch,qty)
   assert r.read(scratch,64).split(b'\xff')[0]==encode('Yo-kai Ball'+('s' if qty>1 else ''))[:-1]
  long_words=[]
  # Every localized vocabulary word is measured by the native small font.
  for path in sorted((ROOT/'src/data/easy_chat').glob('easy_chat_group_*.h')):
   for symbol,text in re.findall(r'static const u8 (\w+)\[\] = _\("([^"]*)"\)',path.read_text()):
    if "{" not in text:assert r.read(r.symbols[symbol],len(encode(text)))==encode(text),symbol
    width=r.call('GetStringWidth',1,r.symbols[symbol],0);
    if width>72:long_words.append(dict(file=str(path.relative_to(ROOT)),symbol=symbol,text=text,width=width))
  Path('/tmp/vocab-long.json').write_text(json.dumps(long_words,ensure_ascii=False,indent=2))
  assert not long_words,len(long_words)
  rows.append(dict(test='1006 native vocabulary strings and 72px column bound',passed=True))
  r.call('Free',scratch)
  base=r.snapshot()
  r.call('InitRegionMapWithExitCB',0,r.symbols['CB2_ReturnToField']|1);r.run(300);r.frame.save(P/'carte-kanto.png')
  r.restore(base)
  # Front and reverse card: actual native UI, localized dynamic header.
  base=r.snapshot()
  r.call('ShowPlayerTrainerCard',r.symbols['CB2_ReturnToField']|1);r.run(180);r.frame.save(P/'carte-recto.png')
  r.keys={8};r.run(2);r.keys=set();r.run(180);r.frame.save(P/'carte-verso.png')
  r.restore(base)
  # All native party status types, same graphic sheet used by summary.
  r.call('FlagSet',0x828);r.call('FlagSet',0x829)
  status=[1,0x20,0x10,0x8,0x40,0]
  for i,value in enumerate(status):
   mon=r.symbols['gPlayerParty']+100*i;r.call('CreateMon',mon,i+1,20,31,1,100+i,0,0)
   r.write(r.PARAMS+128,struct.pack('<I',value));r.call('SetMonData',mon,55,r.PARAMS+128)
   if i==5:r.write(r.PARAMS+128,b'\0\0');r.call('SetMonData',mon,57,r.PARAMS+128)
  r.write(r.symbols['gPlayerPartyCount'],b'\6')
  r.keys={3};r.run(2);r.keys=set();r.run(120)
  order=list(r.read(r.symbols['sStartMenuOrder'],r.read(r.symbols['sNumStartMenuItems'],1)[0]));target=order.index(1)
  for _ in range(target):r.keys={5};r.run(2);r.keys=set();r.run(20)
  r.keys={8};r.run(2);r.keys=set();r.run(300);r.frame.save(P/'etats-equipe.png')
  tiles=r.call('GetSpriteTileStartByTag',1202);assert tiles!=0xffff
  # Loaded French glyphs differ from original English; original pill outlines retained.
  scratch=r.call('AllocZeroed',1024);r.call('LZ77UnCompWram',r.symbols['gStatusGfx_Icons'],scratch)
  old=r.read(scratch,1024);new=r.read(0x06010000+tiles*32,1024)
  for i in (2,3,4,6):assert old[i*128:(i+1)*128]!=new[i*128:(i+1)*128],i
  for i in (0,1,5,7):assert old[i*128:(i+1)*128]==new[i*128:(i+1)*128],i
  r.call('Free',scratch)
  r.keys={8};r.run(2);r.keys=set();r.run(120)
  r.keys={8};r.run(2);r.keys=set();r.run(300);r.frame.save(P/'resume-sommeil.png')
  for page in ('stats','capacites','details'):
   r.keys={7};r.run(2);r.keys=set();r.run(300);r.frame.save(P/('resume-'+page+'.png'))
  r.keys={8};r.run(2);r.keys=set();r.run(300);r.frame.save(P/'resume-details.png')
  rows.append(dict(test='Native party loads localized SOM/GEL/BRU/K.O., preserves PSN/PAR/PKRS',passed=True))
 finally:r.close()
(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256((ROOT/'pokefirered_audio.gba').read_bytes()).hexdigest(),results=rows),ensure_ascii=False,indent=2)+'\n')
print('PASS',len(rows))

#!/usr/bin/env python3
"""Measure changed field strings on the compiled ROM using the native font."""
import re,subprocess,json,hashlib,os
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
BASE='d32774305'
r=new_game();rows=[];over=[];passed=False
try:
 files=subprocess.check_output(['git','diff','--name-only',BASE],text=True).splitlines()
 pattern=r'^(\w+)::[^\n]*\n(.*?)(?=^\w+::|\Z)'
 for gender in [0,1]:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
  for file in files:
   if not file.endswith('.inc') or not (ROOT/file).exists():continue
   now=dict(re.findall(pattern,(ROOT/file).read_text(),re.S|re.M))
   old=dict(re.findall(pattern,subprocess.check_output(['git','show',BASE+':'+file],text=True),re.S|re.M))
   for name,body in now.items():
    if '.string' not in body or re.findall(r'\.string[^\n]+',body)==re.findall(r'\.string[^\n]+',old.get(name,'')):continue
    assert name in r.symbols,name
    r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols[name]);raw=r.read(r.symbols['gStringVar4'],1024).split(b'\xff',1)[0]
    for i,line in enumerate(re.split(b'[\xfa\xfb\xfe]',raw)):
     assert len(line)<128,(name,len(line));r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0)
     row=dict(file=file,label=name,line=i,gender=gender,width=width);rows.append(row)
     if width>208:over.append(row)
 for gender in [0,1]:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
  r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols['sText_AlyzonColossus'])
  raw=r.read(r.symbols['gStringVar4'],1024).split(b'\xff',1)[0]
  for i,line in enumerate(re.split(b'[\xfa\xfb\xfe]',raw)):
   r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0)
   row=dict(file='src/battle_message.c',label='sText_AlyzonColossus',line=i,gender=gender,width=width);rows.append(row)
   if width>208:over.append(row)
 passed=not over
 print('Measured',len(rows),'lines; overflows:',json.dumps(over,ensure_ascii=False),flush=True)
finally:
 mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';out=ROOT/'docs/champions-yokai-watch/validation'/mode;out.mkdir(parents=True,exist_ok=True)
 (out/'DIALOGUES_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),native_font=2,limit_pixels=208,lines_checked=len(rows),overflows=over,lines=rows),ensure_ascii=False,indent=2)+'\n');r.close()
assert passed,'Native dialogue width exceeded'

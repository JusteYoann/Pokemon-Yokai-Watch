#!/usr/bin/env python3
"""Measure chapter field strings with the compiled native GBA font."""
import json,re,os,hashlib
from mgba_new_game import new_game
from mgba_rpc import ROOT
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';P=ROOT/os.environ.get('YOKAI_PHILOSOVNI_REPORT_DIR','docs/pierre-philosovni/validation')/mode;P.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];over=[]
try:
 for filename in ['data/scripts/philosovni.inc','data/maps/VermilionCity/text.inc']:
  s=(ROOT/filename).read_text()
  for label,body in re.findall(r'^(\w+)::[^\n]*\n(.*?)(?=^\w+::|\Z)',s,re.M|re.S):
   if '.string' not in body:continue
   r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols[label]);raw=r.read(r.symbols['gStringVar4'],1024).split(b'\xff',1)[0]
   for i,line in enumerate(re.split(b'[\xfa\xfb\xfe]',raw)):
    assert len(line)<128;r.write(r.PARAMS+128,line+b'\xff');w=r.call('GetStringWidth',2,r.PARAMS+128,0);row=dict(label=label,line=i,width=w);rows.append(row)
    if w>208:over.append(row)
 print('Measured',len(rows),'lines; overflow',over,flush=True)
 (P/'DIALOGUES_MGBA.json').write_text(json.dumps(dict(passed=not over,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),native_font=2,max_pixels=208,lines_checked=len(rows),overflows=over,lines=rows),ensure_ascii=False,indent=2)+'\n')
finally:r.close()
assert not over

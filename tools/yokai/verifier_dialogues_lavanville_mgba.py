#!/usr/bin/env python3
"""Native width of every changed literal dialogue record; no ROM edits."""
import sys,re,subprocess,json,hashlib,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mgba_new_game import new_game
r=new_game();checked=0;rows=[];passed=False
try:
 files=subprocess.check_output(['git','diff','--name-only','7110ce41b'],text=True).splitlines()
 pattern=r'^(\w+)::[^\n]*\n(.*?)(?=^\w+::|\Z)'
 for file in files:
  if not file.endswith('.inc'):continue
  p=Path(file);now=dict(re.findall(pattern,p.read_text(),re.S|re.M));old=dict(re.findall(pattern,subprocess.check_output(['git','show','7110ce41b:'+file],text=True),re.S|re.M))
  for name,body in now.items():
   if '.string' not in body or re.findall(r'\.string[^\n]+',body)==re.findall(r'\.string[^\n]+',old.get(name,'')):continue
   assert name in r.symbols,name
   r.call('StringExpandPlaceholders',r.symbols['gStringVar4'],r.symbols[name]);raw=r.read(r.symbols['gStringVar4'],1024).split(b'\xff',1)[0]
   for line in re.split(b'[\xfa\xfb\xfe]',raw):
    assert len(line)<128,(name,len(line));r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0);checked+=1
    assert width<=208,(file,name,width);rows.append(dict(file=file,label=name,width=width))
 passed=True;print('lines checked',checked)
finally:
 mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';out=Path('docs/lavanville-zombie-night/finalisation')/mode;out.mkdir(parents=True,exist_ok=True)
 (out/'DIALOGUES_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),native_font=2,limit_pixels=208,lines_checked=checked,lines=rows),ensure_ascii=False,indent=2)+'\n');r.close()

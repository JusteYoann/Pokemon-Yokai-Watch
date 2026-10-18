#!/usr/bin/env python3
"""354 exact linked French strings, native widths and real relearner panel rendering.

The panel is explicitly refreshed by PrintMoveInfo for each move: not a claim that
all354 are learnable by the fixture Jibanyan or reached through normal scrolling.
"""
import hashlib,json,re,subprocess
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/POST_B13/traduction/descriptions-natives';P.mkdir(parents=True,exist_ok=True)
entries=json.loads((ROOT/'QA_RECETTE_FINALE/POST_B13/traduction/DESCRIPTIONS_354.json').read_text())['entries'];glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’'];r=new_game();checks=[];passed=False;error='Interrupted'
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,60,31,1,100,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.write(r.symbols['gSpecialVar_0x8004'],b'\0\0');r.call('SetMainCallback2',r.symbols['CB2_MoveRelearner_Init']|1);r.run(600)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_MoveRelearner']|1
 # Local symbol name is duplicated by tm_case.c: resolve exact BL target in unique caller.
 disasm=subprocess.check_output(['arm-none-eabi-objdump','-d','--disassemble=PrintMoveInfoHandleCancel_CopyToVram',str(r.elf_path)],text=True)
 native_print=int(re.search(r'\bbl\s+([0-9a-f]+)\s+<PrintMoveInfo>',disasm)[1],16)
 for e in entries:
  ptr=r.symbols[e['symbol']];expected=b'\xfe'.join(bytes(glyph[c] for c in line) for line in e['lines'])+b'\xff';assert r.read(ptr,len(expected))==expected,(e['move_id'],'Linked French text differs')
  width=r.call('GetStringWidth',2,ptr,0);assert width<=112,(e['move_id'],width)
  r.call(native_print,e['move_id'])
  for win in [3,4,5]:r.call('CopyWindowToVram',win,3)
  r.run(3);r.frame.save(P/f"{e['move_id']:03d}.png");checks.append(dict(move_id=e['move_id'],native_width_pixels=width,linked_bytes_match=True,native_relearner_panel_captured=True))
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_354.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=checks),ensure_ascii=False,indent=2)+'\n');print('DESCRIPTIONS',len(checks),passed,error)
if passed:
 for page in range((len(checks)+15)//16):
  canvas=Image.new('RGB',(1000,720),(224,224,224));d=ImageDraw.Draw(canvas)
  for i,e in enumerate(entries[page*16:(page+1)*16]):
   x=(i%4)*250;y=(i//4)*180;d.text((x+4,y+2),f"{e['move_id']:03d}",fill='black');canvas.paste(Image.open(P/f"{e['move_id']:03d}.png"),(x+4,y+17))
  canvas.save(P/f'planche-{page+1:02d}.png')

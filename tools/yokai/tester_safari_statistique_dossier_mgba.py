#!/usr/bin/env python3
"""Native RNG+Safari PID lottery statistical fixture; not2million natural captures."""
import json,os,struct,subprocess,tempfile,hashlib
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
r=new_game();mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';D=ROOT/'docs/dossier-20261023/tests'/mode;D.mkdir(parents=True,exist_ok=True);draws=2_000_000;rows=[];passed=False
try:
 asm=f'''.syntax unified
.thumb
.global entry
.thumb_func
entry:
 push {{r4-r7,lr}}
 movs r5,r0
 movs r4,#0
 movs r6,#0
loop:
 ldr r7, ={r.symbols['Random']|1}
 bl invoke
 push {{r0}}
 ldr r7, ={r.symbols['Random']|1}
 bl invoke
 lsls r0,r0,#16
 pop {{r2}}
 orrs r0,r2
 movs r1,r5
 ldr r7, ={r.symbols['SafariWildPersonality']|1}
 bl invoke
 movs r1,r0
 lsrs r1,r1,#16
 eors r0,r1
 eors r0,r5
 lsrs r1,r5,#16
 eors r0,r1
 lsls r0,r0,#16
 lsrs r0,r0,#16
 cmp r0,#8
 bhs next
 adds r6,#1
next:
 adds r4,#1
 ldr r2, ={draws}
 cmp r4,r2
 blo loop
 movs r0,r6
 pop {{r4-r7,pc}}
invoke:
 bx r7
.pool
'''
 td=Path(tempfile.mkdtemp());(td/'x.s').write_text(asm);subprocess.run(['arm-none-eabi-as','-mcpu=arm7tdmi','-mthumb',str(td/'x.s'),'-o',str(td/'x.o')],check=True);subprocess.run(['arm-none-eabi-objcopy','-O','binary',str(td/'x.o'),str(td/'x.bin')],check=True);blob=(td/'x.bin').read_bytes();assert len(blob)<256;r.write(0x0203FD00,blob)
 for seed,ot in [(20261023,0x12345678),(746128,0xDEADBEEF)]:
  r.call('SeedRng',seed);hits=r.call(0x0203FD00,ot,max_frames=12000);expected=draws*3/8192;assert abs(hits-expected)<6*expected**.5,(seed,hits)
  rows.append({'seed':seed,'ot':hex(ot),'draws':draws,'shiny':hits,'expected':expected,'native_Random32_and_normaliser':True});print(rows[-1],flush=True)
 passed=True
finally:
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(D/'SAFARI_STATISTIQUES_NATIVES.json').write_text(json.dumps({'passed':passed,'scope':__doc__,'rom_sha256':sha,'samples':rows},indent=2)+'\n')

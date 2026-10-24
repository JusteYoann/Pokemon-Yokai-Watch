#!/usr/bin/env python3
import os,sys,subprocess,struct,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/yokai'))
from mgba_new_game import new_game
from mafiamille_qa import warp,MAPS,strong_party
OUT=ROOT/'docs/beta-retours-20261024/performance';OUT.mkdir(parents=True,exist_ok=True)
s='''.syntax unified
.thumb
.global entry
.thumb_func
entry:
 push {r4-r7,lr}
 sub sp,#4
 movs r6,r0
 ldr r7,=@MAIN@
 ldr r5,[r7]
 str r5,[sp]
 ldr r5,=@CB@
 str r5,[r7]
 ldr r4,=0x04000108
 ldr r5,=0x00840000
 str r5,[r4,#4]
 ldr r5,=0x00800000
 str r5,[r4]
 adr r0,done
 adds r0,#1
 mov lr,r0
 bx r6
.align 2
done:
 ldrh r0,[r4]
 ldrh r1,[r4,#4]
 lsls r1,r1,#16
 orrs r0,r1
 movs r1,#0
 strh r1,[r4,#2]
 strh r1,[r4,#6]
 ldr r1,[sp]
 str r1,[r7]
 add sp,#4
 pop {r4-r7,pc}
.pool
'''
p=Path('/tmp/beta_perf');p.mkdir(exist_ok=True);(p/'t.s').write_text(s)
rows=[]
for name,rom,elf in [('avant','/workspace/artifacts/beta-0.1/Pokemon_Yokai_Watch_Beta_0.1.gba','/workspace/artifacts/audio-diagnostic-beta-0.1/baseline.elf'),('apres',str(ROOT/'pokefirered_audio.gba'),str(ROOT/'pokefirered_audio.elf'))]:
 os.environ.update(YOKAI_QA_ROM=rom,YOKAI_QA_ELF=elf);r=new_game()
 try:
  strong_party(r);r.call('VarSet',0x40f4,3);warp(r,*MAPS['Route20'],10,9);r.call('VarSet',0x4020,250);r.run(60)
  frames=[];r.keys={7};last=None;steps=[]
  for f in range(160):
   r.run();i=r.read(r.symbols['gPlayerAvatar']+5,1)[0];at=struct.unpack('<hh',r.read(r.symbols['gObjectEvents']+36*i+16,4))
   if last!=at:steps.append((f,at));last=at
   if f%8==0:frames.append(r.frame.copy())
  r.keys=set();frames[0].save(OUT/(name+'-surf.gif'),save_all=True,append_images=frames[1:],duration=134,loop=0)
  warp(r,*MAPS['Route20'],10,9);r.run(60)
  (p/'t.s').write_text(s.replace('@MAIN@',hex(r.symbols['gMain']+4)).replace('@CB@',hex(r.symbols['CB2_Overworld']|1)))
  subprocess.run(['arm-none-eabi-as','-mthumb','-mcpu=arm7tdmi',str(p/'t.s'),'-o',str(p/'t.o')],check=True);subprocess.run(['arm-none-eabi-objcopy','-O','binary',str(p/'t.o'),str(p/'t.bin')],check=True)
  ptr=r.call('AllocZeroed',256);assert ptr
  r.write(ptr,(p/'t.bin').read_bytes())
  timings={}
  for fn in ['SpriteCallbackDummy','CramoisFogPalette','CramoisFogPreparePalette']:
   if fn in r.symbols:
    vals=[r.call(ptr,r.symbols[fn]|1) for _ in range(12)]
    timings[fn]=dict(median_cycles=statistics.median(vals),min_cycles=min(vals),max_cycles=max(vals))
  r.call('Free',ptr)
  row=dict(version=name,steps=steps,timing=timings,cycles_per_frame=280896,vblank_cycles_budget=83776,fixture='Native timer2+3 profiling wrapper; no ROM change; interrupts included; movement by held RIGHT button')
  rows.append(row);print(row,flush=True)
 finally:r.close()
(OUT/'TEST_MGBA.json').write_text(json.dumps(rows,indent=2))

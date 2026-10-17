#!/usr/bin/env python3
"""Compare public synthetic vectors with the actual ROM ARM DPCM decoder in mGBA.

Calls the existing decoder through a temporary RAM wrapper, never changes the ROM.
Not a soundtrack, audible playback, looping, SFX coexistence or performance test.
"""
import hashlib,json,math,struct,subprocess,tempfile
from pathlib import Path
from dpcm_m4a import encode,decode,wave_data
from mgba_rpc import Emulator,ROOT
r=Emulator();results=[]
try:
 r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 # Private heap allocations avoid overwriting live sprites, mixer or savedata.
 channel=r.call('AllocZeroed',64);payload=r.call('AllocZeroed',2048);wrapper=r.call('AllocZeroed',128)
 assert channel and payload and wrapper
 asm=f'''.include "asm/macros.inc"
.include "constants/gba_constants.inc"
.include "constants/m4a_constants.inc"
.text
.syntax unified
.thumb
push {{r4,lr}}
movs r4,r0
movs r3,r1
adr r2, arm_call
bx r2
.align 2
.arm
arm_call:
mvn r0, #0
str r0,[r4,#o_SoundChannel_xpi]
ldr r2, ={r.symbols['SoundMainRAM_Unk2'] & ~1}
mov lr,pc
bx r2
adr r0, returned+1
bx r0
.thumb
returned:
movs r0,r1
pop {{r4,pc}}
.pool
'''
 with tempfile.TemporaryDirectory(prefix='yokai-dpcm-') as d:
  p=Path(d);(p/'wrapper.s').write_text(asm)
  subprocess.run(['arm-none-eabi-as','-mcpu=arm7tdmi','-mthumb','-I',str(ROOT),str(p/'wrapper.s'),'-o',str(p/'wrapper.o')],check=True)
  subprocess.run(['arm-none-eabi-objcopy','-O','binary',str(p/'wrapper.o'),str(p/'wrapper.bin')],check=True)
  code=(p/'wrapper.bin').read_bytes();assert len(code)<=128;r.write(wrapper,code)
  # Export assembler-computed struct offset rather than guessing an engine ABI.
  (p/'offset.s').write_text('.include "asm/macros.inc"\n.include "constants/gba_constants.inc"\n.include "constants/m4a_constants.inc"\n.text\n.word o_SoundChannel_wav\n')
  subprocess.run(['arm-none-eabi-as','-I',str(ROOT),str(p/'offset.s'),'-o',str(p/'offset.o')],check=True)
  subprocess.run(['arm-none-eabi-objcopy','-O','binary',str(p/'offset.o'),str(p/'offset.bin')],check=True)
  wav_offset=struct.unpack('<I',(p/'offset.bin').read_bytes())[0]
  r.w32(channel+wav_offset,payload)
 vectors={'silence':[0]*128,'signed_extremes':[-128,127,0,-1,1,126,-127]*19,'sine_440':[round(100*math.sin(2*math.pi*440*i/13379)) for i in range(193)],'ramp':list(range(-128,128))}
 for name,samples in vectors.items():
  blob=wave_data(samples,13379,0);r.write(payload,blob);expected=decode(blob[16:],len(samples))
  actual=[signed if signed<128 else signed-256 for signed in [r.call(wrapper,channel,i)&255 for i in range(len(samples))]]
  assert actual==expected,(name,next((i,a,b) for i,(a,b) in enumerate(zip(actual,expected)) if a!=b))
  results.append({'vector':name,'samples':len(samples),'encoded_bytes':len(blob),'native_matches_python_sample_for_sample':True})
 report={'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'engine':'mGBA actual SoundMainRAM_Unk2 ARM routine','scope':'Synthetic sample decoding only, block boundaries and signed wrapping; no musical playback/loop/SFX/performance claim','vectors':results}
 (ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_DPCM_DECODEUR_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
finally:r.close()

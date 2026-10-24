#!/usr/bin/env python3
"""Capture native before/after cues with identical inputs and levels.

Includes every private header, accelerated loop/end fixtures and stopped-music
silence. No hardware/frontend-device profiling or human listening claim.
"""
import argparse,os,sys,struct,ctypes,wave,json,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
from mgba_rpc import Emulator,BATCH
parser=argparse.ArgumentParser(description=__doc__)
for name in ['before-rom','before-elf','after-rom','after-elf','output']:parser.add_argument('--'+name,type=Path,required=True)
args=parser.parse_args();OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
selected={7:'titre',12:'ville',22:'route',28:'combat-sauvage',29:'combat-boss',32:'credits'}
roms={'avant':(args.before_rom,args.before_elf),'apres':(args.after_rom,args.after_elf)}
results={}
for phase,(rom,elf) in roms.items():
 os.environ['YOKAI_QA_ELF']=str(elf);r=Emulator(rom=rom);rows=[];chunks=[];cb=BATCH(lambda p,n:(chunks.append(ctypes.string_at(p,n*4)) or n));r.lib.retro_set_audio_sample_batch(cb)
 try:
  r.call('ResetMapMusic');r.call('m4aMPlayAllStop');r.call('YokaiDiscardPausedSample');r.run(10);base=r.snapshot()
  for n in range(1,33):
   r.restore(base);chunks.clear();song=346+n if n<32 else 378;r.call('PlayBGM',song);r.run(6);chunks.clear();r.run(600 if n in selected else 20)
   wave_name=f'yokai_wave_{n:02d}' if n<32 else 'yokai_credits_wave'
   # Credits' symbol spelling comes from its linked header, not an assumption.
   header=r.u32(r.symbols['gMPlayInfo_BGM']);tone=r.u32(header+4);waveptr=r.u32(tone+4)
   if n<32:assert waveptr==r.symbols[wave_name]
   channels=[r.symbols['gSoundInfo']+80+i*64 for i in range(5)]
   chan=next(p for p in channels if r.u32(p+36)==waveptr and r.read(p,1)[0]&0xc7)
   kind,flags,freq,loop,count=struct.unpack('<HHIII',r.read(waveptr,16));pos=r.u32(chan+40)
   raw=b''.join(chunks);audio=np.frombuffer(raw,dtype='<i2')/32768
   row=dict(number=n,song=song,header=hex(header),codec=kind,rate_hz=freq/1024,samples=count,loop_start=loop if flags&0x4000 else None,current_sample=pos,peak=float(abs(audio).max()),rms=float(np.sqrt(np.mean(audio*audio))),clipped_samples=int(np.count_nonzero(abs(audio)>=.999)))
   assert row['clipped_samples']==0
   if n in selected:
    with wave.open(str(OUT/f'{selected[n]}-{phase}.wav'),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(65536);f.writeframes(raw)
    r.frame.save(OUT/f'{selected[n]}-{phase}.png')
   # Accelerated seek fixture verifies a real wrap through the native mixer.
   if flags&0x4000:
    r.w32(chan+40,count-256);r.w32(chan+24,256);r.w32(chan+28,0);r.run(4);after=r.u32(chan+40)
    assert loop<=after<=loop+224*5,(phase,n,after,loop)
    row['native_wrap_verified']=True
   else:
    r.w32(chan+40,count-256);r.w32(chan+24,256);r.w32(chan+28,0);r.run(5)
    assert r.read(chan,1)[0]==0,(n,r.read(chan,1));row['native_end_verified']=True
   rows.append(row)
  r.restore(base);chunks.clear();r.run(600);assert not any(b''.join(chunks));rows.append(dict(music_stopped_exact_digital_silence=True))
  results[phase]=dict(rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),rows=rows)
  print('PASS',phase,len(rows),flush=True)
 finally:r.close()
(OUT/'NATIVE_PLAYBACK.json').write_text(json.dumps(results,indent=2))

#!/usr/bin/env python3
"""Native m4a intro + sampled loop with free synthetic audio and SFX/cry.

Appends test-only resources to a temporary ROM copy. No public ROM, no change
in game sources/song table. Does not validate any of the 20 private music cues.
"""
import ctypes,hashlib,json,math,re,struct,tempfile
from pathlib import Path
import numpy as np
from dpcm_m4a import wave_data
from mgba_rpc import Emulator,ROOT,BATCH
RATE=13379;intro=round(RATE*.4);loop=round(RATE*.6)
samples=[round(70*math.sin(2*math.pi*440*i/RATE)) for i in range(intro)]+[round(70*math.sin(2*math.pi*660*i/RATE)) for i in range(loop)]
rom=bytearray((ROOT/'pokefirered.gba').read_bytes());base=len(rom)+0x08000000
# 0: header(12),12:voice(12),24:track(32 reserved),56:WaveData
header=base;tone=base+12;track=base+24;wav=base+56
# TEMPO75, VOICE0, VOL90, TIE Cn3 v100; W96; GOTO W96.
sequence=bytes([0xbb,75,0xbd,0,0xbe,90,0xcf,60,100,0xb0,0xb2])+struct.pack('<I',track+9)
blob=struct.pack('<4BII',1,0,0,0,tone,track)+struct.pack('<4BI4B',0x28,60,0,0,wav,255,0,255,0)+sequence
blob+=bytes(56-len(blob));blob+=wave_data(samples,RATE,intro);rom.extend(blob)
C={k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[\da-fA-F]+|\d+)\s*(?:$|//)',(ROOT/'include/constants/songs.h').read_text(),re.M)}
with tempfile.TemporaryDirectory(prefix='yokai-dpcm-playback-') as d:
 path=Path(d)/'synthetic-test.gba';path.write_bytes(rom);r=Emulator(rom=path);chunks=[]
 callback=BATCH(lambda data,frames:(chunks.append(ctypes.string_at(data,frames*4)) or frames))
 r.lib.retro_set_audio_sample_batch(callback)
 try:
  r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
  r.call('MPlayStart',r.symbols['gMPlayInfo_BGM'],header);chunks.clear()
  assert r.u32(r.symbols['gMPlayInfo_BGM'])==header
  for f in range(420):
   if f==180:r.call('PlaySE',C['SE_SELECT'])
   if f==240:r.call('PlayCry_Normal',1,0)
   r.run()
  assert r.u32(r.symbols['gMPlayInfo_BGM'])==header,'BGM stopped unexpectedly'
  raw=b''.join(chunks);audio=np.frombuffer(raw,dtype='<i2').reshape(-1,2).mean(axis=1)
  # Libretro core sample rate is obtained from its native AV description below.
  # Verify the core output rate rather than assuming the source WAV rate.
  class Geometry(ctypes.Structure):_fields_=[('base_width',ctypes.c_uint),('base_height',ctypes.c_uint),('max_width',ctypes.c_uint),('max_height',ctypes.c_uint),('aspect_ratio',ctypes.c_float)]
  class Timing(ctypes.Structure):_fields_=[('fps',ctypes.c_double),('sample_rate',ctypes.c_double)]
  class AV(ctypes.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
  av=AV();r.lib.retro_get_system_av_info(ctypes.byref(av));out_rate=av.timing.sample_rate
  def peak(a,b):
   part=audio[round(a*out_rate):round(b*out_rate)];spectrum=abs(np.fft.rfft(part*np.hanning(len(part))))
   return float(np.fft.rfftfreq(len(part),1/out_rate)[int(np.argmax(spectrum[1:]))+1])
  intro_peak=peak(.08,.28);loop_peaks=[peak(t,t+.18) for t in [.65,1.25,1.85,2.45,5.5,6.1]]
  assert abs(intro_peak-440)<15,(intro_peak,out_rate,len(audio),r.read(r.symbols['gSoundInfo'],28).hex())
  assert all(abs(f-660)<15 for f in loop_peaks),loop_peaks
  r.call('PlayBGM',C['MUS_PALLET']);r.run(180)
  assert r.u32(r.symbols['gMPlayInfo_BGM'])!=header,'Original BGM not restored'
  report={'passed':True,'base_rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'test_rom_sha256':hashlib.sha256(rom).hexdigest(),'engine':'native m4a mixer in mGBA; test-only appended resources','synthetic_audio_only':True,'sample_rate_hz':RATE,'intro_samples':intro,'loop_samples':loop,'wave_data_bytes':len(blob)-56,'libretro_sample_rate_hz':out_rate,'native_frames':420,'intro_peak_hz':intro_peak,'loop_peaks_hz':loop_peaks,'periods_elapsed_after_intro':(len(audio)/out_rate-intro/RATE)/(loop/RATE),'select_sound_and_species1_cry_triggered':True,'original_pallet_bgm_restored_via_native_PlayBGM':True,'limitations':['Not a private music listening/loop test','Not bicycle field enter/exit','Not hardware CPU profiling','No production song table or game engine changes'],'captured_audio_frames':len(audio)}
  (ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_DPCM_LECTURE_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 finally:r.close()

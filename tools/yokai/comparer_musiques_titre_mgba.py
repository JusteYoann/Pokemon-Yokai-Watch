#!/usr/bin/env python3
"""Native previews of existing cues; private audio stays outside Git.

Signal measurements do not constitute a listening/artistic validation.
"""
import ctypes
import hashlib
import json
import os
import wave
from pathlib import Path
import numpy as np
from mgba_rpc import ROOT, Emulator, BATCH

assert '_audio' in os.environ.get('YOKAI_QA_ROM','')
out=Path('/workspace/artifacts/ecran-titre-credits/comparaison-titre')
out.mkdir(parents=True,exist_ok=True)
r=Emulator()
chunks=[]
callback=BATCH(lambda data,frames:(chunks.append(ctypes.string_at(data,frames*4)) or frames))
r.lib.retro_set_audio_sample_batch(callback)
class Geometry(ctypes.Structure):
    _fields_=[('base_width',ctypes.c_uint),('base_height',ctypes.c_uint),('max_width',ctypes.c_uint),('max_height',ctypes.c_uint),('aspect_ratio',ctypes.c_float)]
class Timing(ctypes.Structure):
    _fields_=[('fps',ctypes.c_double),('sample_rate',ctypes.c_double)]
class AV(ctypes.Structure):
    _fields_=[('geometry',Geometry),('timing',Timing)]
av=AV();r.lib.retro_get_system_av_info(ctypes.byref(av));rate=round(av.timing.sample_rate)
results=[]
try:
    for title,number,slot in [('Nates House',353,7),('Take Care',372,26),('Blossom Heights',358,12),('The Very Curious Yo-kai Watch',376,30)]:
        r.call('PlayBGM',number)
        assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{slot:02}']
        chunks.clear();r.run(840)
        raw=b''.join(chunks)
        name=f'{slot:02}-{title.lower().replace(" ","-")}.wav'
        with wave.open(str(out/name),'wb') as w:
            w.setparams((2,2,rate,0,'NONE','not compressed'));w.writeframes(raw)
        samples=np.frombuffer(raw,dtype='<i2').reshape(-1,2).astype(np.float64)/32768
        def rms(start,end):
            part=samples[round(start*rate):round(end*rate)]
            return float(np.sqrt(np.mean(part*part)))
        assert rms(0,10)>0
        results.append(dict(title=title,existing_slot=slot,start='native PlayBGM from track beginning',seconds=len(samples)/rate,rms_first_half_second=rms(0,.5),rms_seconds_half_to_three=rms(.5,3),peak=float(np.abs(samples).max()),private_file=name))
finally:r.close()
report=dict(rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),sample_rate=rate,candidate='Nates House',candidate_status='provisional; human audition pending',human_listening_validated=False,scope=__doc__,results=results)
(ROOT/'docs/ecran-titre-credits-20261024/COMPARAISON_MUSIQUES.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

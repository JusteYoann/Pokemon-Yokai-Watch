#!/usr/bin/env python3
"""Measure unassigned slot14 in actual mGBA. Protected output stays private."""
import ctypes,json,hashlib,wave
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT,BATCH
from auditer_niveaux_audio_post_b13 import measure
r=new_game();chunks=[];out=Path('/workspace/private-audio/argenta-zombie-mixer');out.mkdir(exist_ok=True)
try:
 r.call('m4aMPlayAllStop');cb=BATCH(lambda ptr,n:(chunks.append(ctypes.string_at(ptr,n*4)) or n));r.lib.retro_set_audio_sample_batch(cb)
 r.call('m4aSongNumStart',360)
 for _ in range(6000):r.run()
 p=out/'zombie.wav'
 with wave.open(str(p),'wb') as f:f.setparams((2,2,65536,0,'NONE',''));f.writeframes(b''.join(chunks))
 row=dict(rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),song=360,recorded_frames=6000,**measure(p),human_listening=False)
 print(json.dumps(row,indent=2));(ROOT/'QA_RECETTE_FINALE/ARGENTA_MORLEONE/ZOMBIE_NIVEAUX.json').write_text(json.dumps(row,indent=2)+'\n')
finally:r.close()

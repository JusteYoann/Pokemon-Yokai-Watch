#!/usr/bin/env python3
"""Actual mGBA first Morphing video/audio. Private copyrighted mix stays outside Git."""
import ctypes as CT,struct,subprocess,json
from pathlib import Path
from mgba_rpc import ROOT,BATCH
from mgba_new_game import new_game
from mafiamille_qa import strong_party
import wave
Q=ROOT.parent/'artifacts'/'spiraton-etape-b'/'premier-morphing';Q.mkdir(parents=True,exist_ok=True)
r=new_game();pcm=[]
class Geometry(CT.Structure):_fields_=[('w',CT.c_uint),('h',CT.c_uint),('mw',CT.c_uint),('mh',CT.c_uint),('aspect',CT.c_float)]
class Timing(CT.Structure):_fields_=[('fps',CT.c_double),('rate',CT.c_double)]
class AV(CT.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
try:
 strong_party(r);r.call('SpiratonBattleArmPrototype');r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',744));r.call('StartTrainerBattle')
 callbacks={int(v[0],16)|1 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=l.split())==3 and v[2]=='HandleInputChooseAction'}
 for f in range(3000):
  r.keys={8} if f%16<4 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Initial menu missing')
 r.keys=set();r.run(60)
 av=AV();r.lib.retro_get_system_av_info.argtypes=[CT.POINTER(AV)];r.lib.retro_get_system_av_info(CT.byref(av))
 def batch(data,frames):pcm.append(CT.string_at(data,frames*4));return frames
 callback=BATCH(batch);r.lib.retro_set_audio_sample_batch(callback)
 images=[]
 for f in range(390):
  r.keys=({8} if f%16<4 else set()) if r.read(r.symbols['sFirst'],1)==b'\1' else set();r.run();images.append(r.frame.copy())
 for i,im in enumerate(images):im.save(Q/f'{i:03d}.png')
 with wave.open(str(Q/'mixeur-prive.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(round(av.timing.rate));w.writeframes(b''.join(pcm))
 images[0].save(Q/'premier-morphing.gif',save_all=True,append_images=images[1:],duration=34,loop=0)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(av.timing.fps),'-i',str(Q/'%03d.png'),'-i',str(Q/'mixeur-prive.wav'),'-vf','scale=960:640:flags=neighbor','-c:v','libx264','-crf','15','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',str(Q/'premier-morphing-mgba-audio.mp4')],check=True)
 (Q/'CAPTURE.json').write_text(json.dumps(dict(real_mgba_capture=True,frames=len(images),fps=av.timing.fps,audio_rate=av.timing.rate,pcm_bytes=sum(map(len,pcm)),private_audio_not_for_github=True,human_listening=False),indent=2)+'\n')
finally:r.close()
print(Q/'premier-morphing-mgba-audio.mp4')

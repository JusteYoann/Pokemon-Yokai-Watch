#!/usr/bin/env python3
"""Deux extraits de 12 s, son natif: vrais blocs de lancement de la scène.
Préparation séparée de chaque départ; aucun appel natif pendant une capture.
"""
import ctypes as C,json,hashlib,subprocess,tempfile,wave
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import BATCH,ROOT
P=ROOT/'docs/cinematiques-collisions-20261025';work=Path(tempfile.mkdtemp(prefix='lancements-oni-'));clips=[];rows=[]
class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
for i,label in enumerate(('Spiraton_LaunchDonBattle','Spiraton_LaunchFinalBattle')):
 q=QA('TEMP_CLIP.json');r=q.r
 try:
  q.mon()
  for name in ('TRAINER_CHAMPION_FIRST_SQUIRTLE','TRAINER_CHAMPION_FIRST_BULBASAUR','TRAINER_CHAMPION_FIRST_CHARMANDER'):
   import re
   value=int(re.search(r'#define\s+'+name+r'\s+(\d+)',(ROOT/'include/constants/opponents.h').read_text())[1]);r.call('SetTrainerFlag',value)
  q.warp('PokemonLeague_ChampionsRoom',6,10)
  if i:
   r.call('SpiratonBattleArmPrototype')
   for local in (3,4,5,6):r.call('RemoveObjectEventByLocalIdAndMap',local,q.maps['PokemonLeague_ChampionsRoom'][1],q.maps['PokemonLeague_ChampionsRoom'][0])
  r.call('LockPlayerFieldControls');r.call('ScriptContext_SetupScript',r.symbols[label])
  av=AV();r.lib.retro_get_system_av_info(C.byref(av));fps=av.timing.fps;raw,w,h,pitch=r.frame_packet;fmt={0:'rgb555le',1:'bgr0',2:'rgb565le'}[r.pixel_format];bpp=4 if r.pixel_format==1 else 2
  log=(work/f'{i}-ffmpeg.log').open('wb');enc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format',fmt,'-video_size',f'{w}x{h}','-framerate',str(fps),'-i','pipe:0','-vf','scale=720:480:flags=neighbor','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-an',str(work/f'{i}-silent.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
  wav=wave.open(str(work/f'{i}.wav'),'wb');wav.setnchannels(2);wav.setsampwidth(2);wav.setframerate(round(av.timing.rate));audio_chunks=[]
  def batch(data,n):wav.writeframesraw(C.string_at(data,n*4));return n
  cb=BATCH(batch);r.lib.retro_set_audio_sample_batch(cb)
  cry=False;battler=False
  for f in range(round(fps*12)):
   r.keys={8} if q.callback()!='BattleMainCB2' and f%16<2 else set();r.run()
   if f<120 and r.u32(r.symbols['gMPlay_PokemonCry']) and r.read(r.symbols['gPokemonCryBGMDuckingCounter'],1)[0]:cry=True
   if q.callback()=='BattleMainCB2':battler=True
   raw,_,_,pp=r.frame_packet
   if pp==w*bpp:enc.stdin.write(raw)
   else:
    for y in range(h):enc.stdin.write(raw[y*pp:y*pp+w*bpp])
  enc.stdin.close();assert enc.wait()==0;wav.close()
  clip=work/f'{i}.mp4';subprocess.run(['ffmpeg','-y','-i',str(work/f'{i}-silent.mp4'),'-i',str(work/f'{i}.wav'),'-c:v','copy','-c:a','aac','-ar','48000','-b:a','160k',str(clip)],stdout=subprocess.DEVNULL,stderr=log,check=True);log.close();clips.append(clip)
  assert cry and battler,(cry,battler);rows.append({'boss':'Don Morléone' if not i else 'Don Spiraton','script':label,'cri_natif_declenche':cry,'combat_natif_lance':battler,'secondes':(f+1)/fps});print('PASS extrait',rows[-1],flush=True)
 finally:r.close()
listing=work/'concat.txt';listing.write_text(''.join("file '"+str(c)+"'\n" for c in clips));target=P/'lancements-deux-combats-effet-oni-mgba.mp4'
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(target)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
(P/'EXTRAITS_AUDIO.json').write_text(json.dumps({'rom_sha256':hashlib.sha256((ROOT/'pokefirered_audio.gba').read_bytes()).hexdigest(),'scope':__doc__,'effet':'playmoncry SPECIES_ARCANINE, CRY_MODE_ENCOUNTER, identique aux scripts Intro/Alert de Terr’heure','extraits':rows,'capture':'Touches uniquement pendant chaque extrait, audio mGBA natif; deux départs préparés séparément puis assemblés.'},ensure_ascii=False,indent=2)+'\n')
print('PASS',target,flush=True)

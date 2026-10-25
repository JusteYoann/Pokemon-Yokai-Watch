#!/usr/bin/env python3
"""Films continus mGBA, audio natif. Équipe et point de départ préparés;
après le début de la capture, seules les touches sont envoyées à l'émulateur.
Aucun résultat de combat, déplacement ou passage aux crédits n'est injecté.
"""
import ctypes as C,hashlib,json,os,struct,subprocess,tempfile,wave
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import BATCH
mode=os.environ.get('PG_FILM','domniscian');assert mode in ('domniscian','finale')
q=QA('FILM_'+mode+'.json');r=q.r;P=q.P;work=Path(tempfile.mkdtemp(prefix='pg-film-'));events={};encoder=None;audio=None
class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
try:
 level=60 if mode=='domniscian' else 100
 for i,sp in enumerate((150,149,65,123,25,87)):
  p=q.mon(i,sp,level)
  if i==0:
   for j,move in enumerate((53,94,58,85)):r.call('SetMonMoveSlot',p,move,j)
 q.f(0x82c,False);q.f(0x4b5,False)
 if mode=='domniscian':
  from mgba_rpc import ROOT
  import re
  flags=(ROOT/'include/constants/flags.h').read_text();q.f(int(re.search(r'#define FLAG_HIDE_SAFFRON_ROCKETS\s+(0x[0-9A-Fa-f]+)',flags)[1],16))
 if mode=='domniscian':
  q.warp('SaffronCity_Gym',14,12);r.keys={4};r.run(2);r.keys=set();r.run(30)
 else:
  q.warp('PokemonLeague_ChampionsRoom',6,20)
 # Resolve callback addresses before capture; all later access is read-only.
 nm=subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True)
 move_cb={int(a[0],16)|1 for line in nm.splitlines() if len(a:=line.split())==3 and a[2]=='HandleInputChooseMove'}
 def keys(f):
  cb=q.callback()
  if cb=='CB2_UpdatePartyMenu':
   if int.from_bytes(r.read(r.symbols['gBattleMons']+40,2),'little')>0:return {0} if f%16<2 else set()
   slot=r.read(r.symbols['gPartyMenu']+9,1)[0]
   hp=int.from_bytes(r.read(r.symbols['gPlayerParty']+min(slot,5)*100+86,2),'little')
   return {5 if not hp else 8} if f%16<2 else set()
  if cb=='BattleMainCB2' and r.u32(r.symbols['gBattlerControllerFuncs']) in move_cb:
   pp=list(r.read(r.symbols['gBattleMons']+36,4));choices=[i for i in range(4) if pp[i]]
   # Natural PP, damaging moves; use Ice Beam against Dark and Water against Fire where available.
   enemytypes=list(r.read(r.symbols['gBattleMons']+88+33,2))
   target=(2 if 17 in enemytypes and pp[2] else choices[0]) if choices else 0
   current=r.read(r.symbols['gMoveSelectionCursor'],1)[0]
   key=8 if target==current else (7 if target&1 else 6) if (target&1)!=(current&1) else (5 if target&2 else 4)
   return {key} if f%16<3 else set()
  return {8} if f%16<2 else set()
 av=AV();r.lib.retro_get_system_av_info(C.byref(av));fps=av.timing.fps
 raw,w,h,pitch=r.frame_packet;fmt={0:'rgb555le',1:'bgr0',2:'rgb565le'}[r.pixel_format];bpp=4 if r.pixel_format==1 else 2
 log=(work/'ffmpeg.log').open('wb')
 encoder=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format',fmt,'-video_size',f'{w}x{h}','-framerate',str(fps),'-i','pipe:0','-vf','scale=720:480:flags=neighbor','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-an',str(work/'video.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
 audio=wave.open(str(work/'audio.wav'),'wb');audio.setnchannels(2);audio.setsampwidth(2);audio.setframerate(round(av.timing.rate))
 def batch(data,n):audio.writeframesraw(C.string_at(data,n*4));return n
 recording=BATCH(batch);r.lib.retro_set_audio_sample_batch(recording)
 last_cb=None;last_trainer=None;end=None;first_battle=None;seen_credits=False;slides=set();title_at=None
 for f in range(round(fps*(1200 if mode=='finale' else 480))):
  cb=q.callback();battle=cb=='BattleMainCB2'
  if battle:
   trainer=int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')
   if trainer!=last_trainer:
    events['combat_'+str(trainer)]=f/fps;print('COMBAT',trainer,f/fps,flush=True);last_trainer=trainer
   if first_battle is None:first_battle=f
  if cb=='CB2_RollYokaiCredits':
   seen_credits=True
   slide=r.read(r.symbols['sYokaiCreditsSlide'],1)[0]
   if slide not in slides:slides.add(slide);events['credits_'+str(slide)]=f/fps;print('CREDITS',slide,f/fps,flush=True)
   if slide==17 and int.from_bytes(r.read(r.symbols['sYokaiCreditsTick'],2),'little')==180:q.shot('credits-terreur-film')
  if seen_credits and cb!='CB2_RollYokaiCredits' and title_at is None:
   title_at=f;events['redemarrage']=f/fps;print('RESET',cb,f/fps,flush=True)
  if mode=='domniscian' and first_battle is not None and q.idle():
   if end is None:end=f;events['retour_arene']=f/fps;q.shot('domniscian-apres-combat')
  # Hold the first action menu briefly so that its OST can be heard.
  if mode=='domniscian' and first_battle is not None and f-first_battle<round(fps*15):r.keys=set()
  elif title_at is not None:r.keys=set()
  else:r.keys=keys(f)
  r.run()
  raw,ww,hh,pp=r.frame_packet
  if pp==w*bpp:encoder.stdin.write(raw)
  else:
   for row in range(h):encoder.stdin.write(raw[row*pp:row*pp+w*bpp])
  if f%3600==0:
   q.shot(mode+'-capture-en-cours')
   print('FRAME',f,cb,'controller',hex(r.u32(r.symbols['gBattlerControllerFuncs'])),'cursor',list(r.read(r.symbols['gMoveSelectionCursor'],1)),'mons',[(int.from_bytes(r.read(r.symbols['gBattleMons']+88*i,2),'little'),int.from_bytes(r.read(r.symbols['gBattleMons']+88*i+40,2),'little'),list(r.read(r.symbols['gBattleMons']+88*i+36,4))) for i in (0,1)],flush=True)
  if (end is not None and f-end>=round(fps*10)) or (title_at is not None and f-title_at>=round(fps*15)):
   q.shot(mode+'-fin-film');break
 else:raise AssertionError(('Film incomplet',q.callback(),events))
 encoder.stdin.close();assert encoder.wait()==0;encoder=None;audio.close();audio=None
 target=P/('domniscian-arene-avec-son-mgba.mp4' if mode=='domniscian' else 'combat-final-credits-redemarrage-mgba.mp4')
 subprocess.run(['ffmpeg','-y','-i',str(work/'video.mp4'),'-i',str(work/'audio.wav'),'-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',str(target)],stdout=subprocess.DEVNULL,stderr=log,check=True)
 log.close();assert target.stat().st_size<100_000_000
 if mode=='finale':assert 743==int(next(k.split('_')[1] for k in events if k.startswith('combat_'))) and 'combat_744' in events and set(range(32)).issubset(slides) and title_at is not None
 else:assert 'retour_arene' in events
 (P/(mode+'-provenance.json')).write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'moteur':'mGBA libretro, son natif stéréo','continu_sans_coupe':True,'manipulation_apres_capture':'Touches uniquement; aucune modification mémoire/RPC','equipe_preparee':{'especes':[150,149,65,123,25,87],'niveau':level,'IV':31,'EV':0},'fps':fps,'duree':(f+1)/fps,'evenements':events,'taille_octets':target.stat().st_size},ensure_ascii=False,indent=2)+'\n')
 q.passed('Film continu terminé, son natif, '+str(target.name))
finally:
 if encoder:
  encoder.stdin.close();encoder.wait()
 if audio:audio.close()
 q.finish()

#!/usr/bin/env python3
"""Continuous mGBA recording: normal cave, native trigger, escape door and ten seconds after return.
Only the starting map, party and encounter eligibility are prepared. Once the
recording starts, only controller input is used; no warp, timer edit or battle
outcome is injected. Raw native video and audio are encoded without cuts.
"""
import ctypes as C,hashlib,json,os,re,struct,subprocess,tempfile,wave
from collections import deque
from pathlib import Path
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT,BATCH

P=ROOT/'docs'/os.environ.get('TH_VIDEO_DIR','terre-heure-progressive-20261025');P.mkdir(parents=True,exist_ok=True)
work=Path(tempfile.mkdtemp(prefix='terreur-video-'))
r=new_game();th=r.symbols['sTh'];checks=[];events={};frames=0
class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
av=AV();r.lib.retro_get_system_av_info(C.byref(av));fps=av.timing.fps
labels=list(map(int,re.search(r'sThLabels_MtMoon_1F\[\] = \{([^}]+)',(ROOT/'src/data/terre_heure_maps.h').read_text())[1].split(',')))
w,h=48,40
warp_cells={(v['x'],v['y']) for v in json.loads((ROOT/'data/maps/MtMoon_1F/map.json').read_text())['warp_events']}
nm=subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True)
actions={int(f[0],16)|1 for line in nm.splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
def actors():
 out={}
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1:out[b[8]]=(struct.unpack('<hh',b[16:20]),b[24]&15)
 return out
def walk(goal,objects):
 start=objects[255][0];start=(start[0]-7,start[1]-7)
 blocked={(p[0]-7,p[1]-7) for local,(p,d) in objects.items() if local!=255}
 blocked.update(warp_cells);blocked.discard(goal);q=deque([start]);first={start:None};distance={start:0}
 for_x_y=((0,1,5),(0,-1,4),(-1,0,6),(1,0,7))
 while q:
  a=q.popleft()
  if a==goal:return first[a],distance[a]
  for dx,dy,key in for_x_y:
   b=(a[0]+dx,a[1]+dy)
   if not (0<=b[0]<w and 0<=b[1]<h) or not labels[b[1]*w+b[0]] or b in blocked or b in first:continue
   first[b]=first[a] if first[a] is not None else key;distance[b]=distance[a]+1;q.append(b)
 return None

def shot(n):r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'.png'))
encoder=None;audio=None;recording=None;log=None
try:
 party=r.symbols['gPlayerParty'];r.call('CreateMon',party,1,50,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);r.write(sb+0xee0+0x500//8,b'\xff'*96);r.call('VarSet',0x40f9,1);r.call('VarSet',0x40fa,0x101);r.call('FlagSet',0x82f)
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
 g,n=maps['MtMoon_1F'];r.call('SetWarpDestination',g,n,255,20,27);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
 # Fixture only: successful visit, just before its last scheduled step.
 r.call('VarSet',0x40fb,1)
 # Select a reproducible native door draw on the same floor before recording.
 # Each trial is a rolled-back fixture; the published capture is continuous.
 audit=json.loads((ROOT/'docs/terre-heure-20261025/AUDIT_GROTTES.json').read_text())['maps']
 initial=r.snapshot();chosen=None
 for seed in range(1,301):
  r.restore(initial);r.keys=set();r.call('SeedRng',seed);prepared=r.snapshot();r.run(round(fps*1.5));r.keys={6}
  for trial_frame in range(100):
   r.run()
   if r.read(th+175,1)==b'\1':break
  if r.read(th+175,1)!=b'\1' or r.read(th+179,1)!=b'\0':continue
  point=audit[0]['candidates'][r.read(th+180,1)[0]];dx,dy=point[:2]
  player=actors()[255][0];distance=abs(dx-(player[0]-7))+abs(dy-(player[1]-7))
  if 6<=distance<=26:
   chosen=(seed,point);r.restore(prepared);r.keys=set();break
 assert chosen,'Aucune porte de démonstration accessible sur ce premier étage'
 print('FIXTURE',chosen,flush=True)
 assert r.read(th+175,1)==b'\0'
 raw,width,height,pitch=r.frame_packet;fmt={0:'rgb555le',1:'bgr0',2:'rgb565le'}[r.pixel_format];bpp=4 if r.pixel_format==1 else 2
 log=(work/'ffmpeg.log').open('wb')
 encoder=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format',fmt,'-video_size',f'{width}x{height}','-framerate',str(fps),'-i','pipe:0','-vf','scale=720:480:flags=neighbor','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-an',str(work/'video.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
 audio=wave.open(str(work/'audio.wav'),'wb');audio.setnchannels(2);audio.setsampwidth(2);audio.setframerate(round(av.timing.rate))
 def batch(data,n):audio.writeframesraw(C.string_at(data,n*4));return n
 recording=BATCH(batch);r.lib.retro_set_audio_sample_batch(recording)
 last_key=None;nav=0;returned_at=None;goal=None
 for f in range(round(fps*230)):
  active=r.read(th+175,1)[0];phase=r.read(th+176,1)[0];locked=r.read(r.symbols['sLockFieldControls'],1)[0]
  field=r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
  if active and 'declenchement' not in events:events['declenchement']=f/fps
  if phase==1 and 'transformation' not in events:events['transformation']=f/fps
  if phase==3 and 'texte_intro' not in events:events['texte_intro']=f/fps
  if phase==2 and not locked and 'exploration' not in events:events['exploration']=f/fps;shot('exploration')
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:raise AssertionError('Capture interrompue par un combat: ne pas publier comme une fuite réussie')
  if not active and 'exploration' in events and field and not locked and not r.read(r.symbols['gPaletteFade']+7,1)[0]&0x80:
   if returned_at is None:returned_at=f;events['sortie_controles_rendus']=f/fps;shot('sortie')
  if returned_at is not None:
   # Brief real movement after return demonstrates that control is restored.
   elapsed=f-returned_at
   r.keys={6} if round(fps*2)<=elapsed<round(fps*2)+8 else ({7} if round(fps*3)<=elapsed<round(fps*3)+8 else set())
  elif not active:r.keys={6} if f>=round(fps*1.5) else set()
  elif field and locked:r.keys={8} if f%100<2 else set()
  elif field and phase==2:
   objs=actors();player,direction=objs[255];px,py=player[0]-7,player[1]-7
   if 233 not in objs:raise AssertionError('La porte attendue n’est pas sur cet étage')
   door=objs[233][0];dx,dy=door[0]-7,door[1]-7
   if abs(dx-px)+abs(dy-py)==1:
    key,face=(7,4) if dx>px else ((6,3) if dx<px else ((5,1) if dy>py else (4,2)))
    if direction!=face:r.keys={key}
    else:
     if 'interaction_porte' not in events:events['interaction_porte']=f/fps;shot('porte')
     r.keys={8} if f%30<2 else set()
   else:
    if nav%4==0:
     if goal is None or walk(goal,objs) is None:
      occupied={(p[0]-7,p[1]-7) for local,(p,d) in objs.items() if local!=255}
      candidates=[(dx+ox,dy+oy) for ox,oy in ((0,1),(1,0),(0,-1),(-1,0)) if 0<=dx+ox<w and 0<=dy+oy<h and labels[(dy+oy)*w+dx+ox] and (dx+ox,dy+oy) not in occupied]
      routes=[(walk(t,objs),t) for t in candidates]
      routes=[v for v in routes if v[0] is not None]
      goal=min(routes,key=lambda v:v[0][1])[1] if routes else None
     route=walk(goal,objs) if goal is not None else None
     last_key=route[0] if route is not None else None
    nav+=1;r.keys={last_key,0} if last_key is not None else set()
  else:r.keys=set()
  r.run();raw,vw,vh,stride=r.frame_packet
  encoder.stdin.write(raw if stride==width*bpp else b''.join(raw[y*stride:y*stride+width*bpp] for y in range(height)))
  frames+=1
  if f%600==0:print('VIDEO',round(f/fps,1),events,flush=True)
  if returned_at is not None and f-returned_at>=int(fps*10+1):break
 else:raise AssertionError('Sortie non atteinte dans le délai de capture')
 assert all(k in events for k in ('declenchement','transformation','texte_intro','exploration','interaction_porte','sortie_controles_rendus')),events
 assert (frames-1-returned_at)/fps>=10
 r.lib.retro_set_audio_sample_batch(r.callbacks[3]);audio.close();audio=None
 encoder.stdin.close();assert encoder.wait()==0,(work/'ffmpeg.log').read_text();encoder=None;log.close();log=None
 output=P/'declenchement-porte-sortie-mgba.mp4'
 subprocess.run(['ffmpeg','-y','-i',str(work/'video.mp4'),'-i',str(work/'audio.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest',str(output)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)],text=True))
 metadata={'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'video':output.name,'video_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'scope':__doc__,'preparation':{'tirage_porte_natif_seed':chosen[0],'depart':'Visite réussie préparée juste avant son dernier pas programmé. Équipe et position préparées avant capture. Aucune mutation RAM ni téléportation pendant la vidéo.'},'frames':frames,'fps':fps,'duree_secondes':float(info['format']['duration']),'taille_octets':output.stat().st_size,'evenements_secondes':events,'chronometre':'Durée normale de 360 secondes, jamais modifiée pendant la capture. Sortie par interaction réelle avec la porte; chronomètre non modifié.','montage':'Continu, sans coupe ni accélération. Image agrandie x3 au plus proche voisin.','audio':'Sortie directe mGBA, encodée en AAC 48 kHz pour le MP4. Aucune OST modifiée.'}
 (P/'ENREGISTREMENT_SORTIE.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n');print(json.dumps(metadata,ensure_ascii=False,indent=2),flush=True)
finally:
 if audio:r.lib.retro_set_audio_sample_batch(r.callbacks[3]);audio.close()
 if encoder:
  encoder.stdin.close();encoder.wait()
 if log:log.close()
 r.close()

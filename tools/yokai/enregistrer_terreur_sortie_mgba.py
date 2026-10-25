#!/usr/bin/env python3
"""Continuous mGBA recording: native Terror Time, escape or battle, and ten seconds after return.
Only the starting map, party and encounter eligibility are prepared. Once the
recording starts, only controller input is used; no warp, timer edit or battle
outcome is injected. Raw native video and audio are encoded without cuts.
"""
import ctypes as C,hashlib,json,os,re,struct,subprocess,tempfile,wave
from collections import deque
from heapq import heappop,heappush
from pathlib import Path
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT,BATCH

P=ROOT/'docs'/os.environ.get('TH_VIDEO_DIR','terre-heure-progressive-20261025');P.mkdir(parents=True,exist_ok=True)
work=Path(tempfile.mkdtemp(prefix='terreur-video-'))
demo_map=os.environ.get('TH_DEMO_MAP','MtMoon_1F');demo_x,demo_y=map(int,os.environ.get('TH_DEMO_START','20,27').split(','));demo_tier=int(os.environ.get('TH_DEMO_TIER','0'));demo_level=int(os.environ.get('TH_DEMO_LEVEL','85'));hunt=os.environ.get('TH_DEMO_HUNT')=='1';trigger_key=int(os.environ.get('TH_DEMO_KEY','6'));escape_only=os.environ.get('TH_DEMO_ESCAPE_ONLY')=='1';defeat_demo=os.environ.get('TH_DEMO_DEFEAT')=='1'
assert not (escape_only and defeat_demo)
assert demo_tier in (0,1,2) and 1<=demo_level<=100
r=new_game();th=r.symbols['sTh'];checks=[];events={};frames=0;alerts=[];last_locked=False
class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
av=AV();r.lib.retro_get_system_av_info(C.byref(av));fps=av.timing.fps
graph=json.loads((ROOT/'docs/terre-heure-nathan-patrouilles-20261025/GRAPHE_DISTANCES.json').read_text())
floors=graph['maps'];lower_stairs={(m,x,y):(n,u,v) for m,x,y,n,u,v in graph['stairs']};safe_keys={(m,x,y) for m,x,y,n,u,v in graph['safe_stairs']}
stairs={key:value if key in safe_keys else (255,0,0) for key,value in lower_stairs.items()}
group_data=json.loads((ROOT/'data/maps/map_groups.json').read_text())
room_indices={n:(i,j) for i,g in enumerate(group_data['group_order']) for j,n in enumerate(group_data[g])}
room_by_id={room_indices[v['map']]:i for i,v in enumerate(floors)}
def current_floor():return room_by_id[tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))]
nm=subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True)
actions={int(f[0],16)|1 for line in nm.splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
def actors():
 out={}
 for i in range(16):
  b=r.read(r.symbols['gObjectEvents']+36*i,36)
  if b[0]&1:out[b[8]]=(struct.unpack('<hh',b[16:20]),b[24]&15)
 return out
def walk(goal,objects,block=True):
 m=current_floor();p=objects[255][0];start=(m,p[0]-7,p[1]-7)
 blocked={(m,p[0]-7,p[1]-7) for local,(p,d) in objects.items() if local!=255} if block else set()
 if block and 230 in objects:
  ox,oy=objects[230][0];ox-=7;oy-=7
  blocked.update((m,ox+dx,oy+dy) for dx,dy in ((0,0),(0,1),(0,-1),(1,0),(-1,0)))
 native=None
 if block:
  vw,vh,pointer=struct.unpack('<III',r.read(r.symbols['VMap'],12));native=struct.unpack('<'+'H'*(vw*vh),r.read(pointer,vw*vh*2))
 hazards={}
 if block:
  for local,(p,direction) in objects.items():
   if local not in (230,231,232,236,237,238,239,240,241):continue
   ox,oy=p[0]-7,p[1]-7;radius=5 if local==230 else 2
   for yy in range(max(0,oy-radius),min(floors[m]['height'],oy+radius+1)):
    for xx in range(max(0,ox-radius),min(floors[m]['width'],ox+radius+1)):
     dist=abs(xx-ox)+abs(yy-oy)
     if dist<=radius:hazards[(m,xx,yy)]=max(hazards.get((m,xx,yy),0),(radius+1-dist)*(16 if local==230 else 3))
   dx,dy={1:(0,1),2:(0,-1),3:(-1,0),4:(1,0)}[direction]
   for step in range(1,(8 if demo_tier==2 and local==230 else 6 if local==230 else 5)+1):
    xx,yy=ox+dx*step,oy+dy*step
    if not(0<=xx<floors[m]['width'] and 0<=yy<floors[m]['height']):break
    if native is not None and native[(yy+7)*vw+xx+7]>>10&3:break
    hazards[(m,xx,yy)]=hazards.get((m,xx,yy),0)+(100 if local==230 else 12)
 q=[(0,start)];first={start:None};distance={start:0}
 while q:
  cost,a=heappop(q)
  if cost!=distance[a]:continue
  if a==goal:return first[a],cost
  cm,x,y=a;row=floors[cm];edges=row['edges'][y*row['width']+x]
  for bit,(dx,dy,key) in enumerate(((0,1,5),(0,-1,4),(-1,0,6),(1,0,7))):
   if not edges>>bit&1:continue
   neighbor=(cm,x+dx,y+dy)
   if neighbor in blocked:continue
   if block and not row['safe_labels'][(y+dy)*row['width']+x+dx]:continue
   if native is not None and cm==m and native[(y+dy+7)*vw+x+dx+7]>>10&3:continue
   b=(stairs if block else lower_stairs).get(neighbor,neighbor)
   if b[0]==255 or b in blocked:continue
   if block and not floors[b[0]]['safe_labels'][b[2]*floors[b[0]]['width']+b[1]]:continue
   value=cost+1+hazards.get(neighbor,0)
   if value>=distance.get(b,10**9):continue
   first[b]=first[a] if first[a] is not None else key;distance[b]=value;heappush(q,(value,b))

 return None

def retreat(objects):
 m=current_floor();p=objects[255][0];start=(p[0]-7,p[1]-7);row=floors[m]
 occupied={(p[0]-7,p[1]-7) for local,(p,d) in objects.items() if local!=255}
 ox,oy=objects.get(230,objects[255])[0];ox-=7;oy-=7
 vw,vh,pointer=struct.unpack('<III',r.read(r.symbols['VMap'],12));native=struct.unpack('<'+'H'*(vw*vh),r.read(pointer,vw*vh*2))
 q=deque([start]);found={start:(None,0)};best=None
 while q:
  x,y=q.popleft();first,steps=found[(x,y)]
  neighbors=0
  for dx,dy in ((0,1),(0,-1),(-1,0),(1,0)):
   xx,yy=x+dx,y+dy
   if 0<=xx<row['width'] and 0<=yy<row['height'] and row['safe_labels'][yy*row['width']+xx]:neighbors+=1
  if steps>=3:
   score=abs(x-ox)+abs(y-oy)+neighbors*2-steps/8
   if best is None or score>best[0]:best=(score,first,steps)
  if steps>=12:continue
  for dx,dy,key in ((0,1,5),(0,-1,4),(-1,0,6),(1,0,7)):
   xx,yy=x+dx,y+dy
   if not(0<=xx<row['width'] and 0<=yy<row['height']):continue
   if (xx,yy) in found or (xx,yy) in occupied or (m,xx,yy) in lower_stairs:continue
   if abs(xx-ox)+abs(yy-oy)<2 or not row['safe_labels'][yy*row['width']+xx] or native[(yy+7)*vw+xx+7]>>10&3:continue
   found[(xx,yy)]=(key if first is None else first,steps+1);q.append((xx,yy))
 return (best[1],best[2]) if best is not None else None

def shot(n):r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'.png'))
encoder=None;audio=None;recording=None;log=None
try:
 party=r.symbols['gPlayerParty'];r.call('CreateMon',party,150,demo_level,31,1,12345,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1')
 # Keep two natural level-up moves: Swift first (level 33), Recover second (44).
 if not defeat_demo:
  r.call('SetMonMoveSlot',party,129,0);r.call('SetMonMoveSlot',party,105,1)
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);r.write(sb+0xee0+0x500//8,b'\xff'*96);r.call('VarSet',0x40f9,1);r.call('VarSet',0x40fa,0x101);r.call('FlagSet',0x82f)
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}

 for flag in (0x335,0x336):r.call('FlagClear',flag)
 if demo_tier>=1:r.call('FlagSet',0x335)
 if demo_tier>=2:r.call('FlagSet',0x336)
 g,n=maps[demo_map];r.call('SetWarpDestination',g,n,255,demo_x,demo_y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
 # Fixture only: successful visit, just before its last scheduled step.
 r.call('VarSet',0x40fb,1)
 # Select a reproducible native farthest door on another floor.
 # Each trial is a rolled-back fixture; the published capture is continuous.
 audit=json.loads((ROOT/'docs/terre-heure-20261025/AUDIT_GROTTES.json').read_text())['maps']
 initial=r.snapshot();chosen=None
 for seed in range(int(os.environ.get('TH_DEMO_SEED_FIRST','1')),301):
  r.restore(initial);r.keys=set();r.call('SeedRng',seed);prepared=r.snapshot();r.run(round(fps*1.5));r.keys={trigger_key}
  for trial_frame in range(100):
   r.run()
   if r.read(th+175,1)==b'\1':break
  if r.read(th+175,1)!=b'\1':continue
  door_map=r.read(th+179,1)[0];dx,dy=r.read(th+192,2);point=(dx,dy)
  route=walk((door_map,dx,dy),actors(),False)
  if door_map!=current_floor() and route and 0<route[1]<5000:
   chosen=(seed,point,door_map,route[1]);r.restore(prepared);r.keys=set();break
 assert chosen,'Aucune porte interétages de démonstration conforme aux distances'
 print('FIXTURE',chosen,flush=True)
 assert r.read(th+175,1)==b'\0'
 raw,width,height,pitch=r.frame_packet;fmt={0:'rgb555le',1:'bgr0',2:'rgb565le'}[r.pixel_format];bpp=4 if r.pixel_format==1 else 2
 log=(work/'ffmpeg.log').open('wb')
 encoder=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format',fmt,'-video_size',f'{width}x{height}','-framerate',str(fps),'-i','pipe:0','-vf','scale=720:480:flags=neighbor','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-an',str(work/'video.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
 audio=wave.open(str(work/'audio.wav'),'wb');audio.setnchannels(2);audio.setsampwidth(2);audio.setframerate(round(av.timing.rate))
 def batch(data,n):audio.writeframesraw(C.string_at(data,n*4));return n
 recording=BATCH(batch);r.lib.retro_set_audio_sample_batch(recording)
 last_key=None;nav=0;returned_at=None;goal=None
 for f in range(round(fps*480)):
  active=r.read(th+175,1)[0];phase=r.read(th+176,1)[0];locked=r.read(r.symbols['sLockFieldControls'],1)[0]
  field=r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
  if active and 'declenchement' not in events:events['declenchement']=f/fps
  if phase==1 and 'transformation' not in events:events['transformation']=f/fps
  if phase==7 and 'materialisation_patrouilles' not in events:events['materialisation_patrouilles']=f/fps
  if phase==8 and field:
   assert r.read(0x05000000,416)==b'\xff\x7f'*208,'Ancien décor révélé après le blanc'
  if phase==3 and 'texte_intro' not in events:events['texte_intro']=f/fps
  if phase==2 and not locked and 'exploration' not in events:events['exploration']=f/fps;shot('exploration')
  battle=r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1
  if escape_only and field and locked and phase==2 and 'interaction_porte' not in events:
   # Read-only screen evidence is retained for a stalled/failed trial.
   if f%60==0:shot('dernier-verrouillage')
  script_ptr=r.u32(r.symbols['sGlobalScriptContext']+8)
  if field and phase==2 and locked and not last_locked:
   objs=actors();a=objs.get(230,((0,0),0))[0];b=objs[255][0]
   alerts.append({'secondes':f/fps,'etage':current_floor(),'distance_oni':abs(a[0]-b[0])+abs(a[1]-b[1]),'regards':int.from_bytes(r.read(th+162,2),'little')})
  last_locked=bool(locked)
  if escape_only and active and phase==2 and r.symbols['TerreHeure_EventScript_Oni']<=script_ptr<r.symbols['TerreHeure_EventScript_Chest']:raise AssertionError(('Oni au contact',f/fps,actors()))
  if escape_only and battle:raise AssertionError(('Oni rencontré pendant le parcours de fuite',f/fps,actors()))
  if battle and 'combat_oni' not in events:events['combat_oni']=f/fps
  if defeat_demo and 'combat_oni' in events and not battle and r.read(r.symbols['gBattleOutcome'],1)==b'\2' and 'defaite_oni' not in events:events['defaite_oni']=f/fps
  if active and r.read(th+183,1)==b'\1' and 'victoire_oni' not in events:events['victoire_oni']=f/fps
  if not active and 'exploration' in events and field and not locked and not r.read(r.symbols['gPaletteFade']+7,1)[0]&0x80:
   if returned_at is None:returned_at=f;events['sortie_controles_rendus']=f/fps;shot('sortie')
  if battle:r.keys={8} if f%20<2 else set()
  elif returned_at is not None:
   # Brief real movement after return demonstrates that control is restored.
   elapsed=f-returned_at
   r.keys={6} if round(fps*2)<=elapsed<round(fps*2)+8 else ({7} if round(fps*3)<=elapsed<round(fps*3)+8 else set())
  elif not active:r.keys={trigger_key} if f>=round(fps*1.5) else set()
  elif field and locked:r.keys={8} if (not escape_only or phase==3 or 'interaction_porte' in events) and f%100<2 else set()
  elif field and phase==2:
   objs=actors();player,direction=objs[255];px,py=player[0]-7,player[1]-7
   door_map=r.read(th+179,1)[0];dx,dy=r.read(th+192,2);point=(dx,dy);cm=current_floor()
   if hunt and r.read(th+183,1)==b'\0' and 230 in objs:
    ox,oy=objs[230][0];route=walk((cm,ox-7,oy-7),objs,False)
    r.keys={route[0],0} if route and route[0] is not None else set()
   elif cm==door_map and abs(dx-px)+abs(dy-py)==1:
    key,face=(7,4) if dx>px else ((6,3) if dx<px else ((5,1) if dy>py else (4,2)))
    if direction!=face:r.keys={key}
    else:
     if 'interaction_porte' not in events:events['interaction_porte']=f/fps;shot('porte')
     r.keys={8} if f%30<2 else set()
   else:
    if nav%4==0:
     if goal is None or walk(goal,objs) is None:
      occupied={(cm,p[0]-7,p[1]-7) for local,(p,d) in objs.items() if local!=255}
      row=floors[door_map]
      candidates=[(door_map,dx+ox,dy+oy) for ox,oy in ((0,1),(1,0),(0,-1),(-1,0)) if 0<=dx+ox<row['width'] and 0<=dy+oy<row['height'] and row['edges'][(dy+oy)*row['width']+dx+ox] and (door_map,dx+ox,dy+oy) not in occupied]
      routes=[(walk(t,objs),t) for t in candidates]
      routes=[v for v in routes if v[0] is not None]
      goal=min(routes,key=lambda v:v[0][1])[1] if routes else None
     route=walk(goal,objs) if goal is not None else None
     if route is None:route=retreat(objs)
     last_key=route[0] if route is not None else None
    nav+=1;r.keys={last_key,0} if last_key is not None else set()
  else:r.keys=set()
  r.run();raw,vw,vh,stride=r.frame_packet
  encoder.stdin.write(raw if stride==width*bpp else b''.join(raw[y*stride:y*stride+width*bpp] for y in range(height)))
  frames+=1
  if f%600==0:print('VIDEO',round(f/fps,1),events,'NAV',current_floor(),actors().get(255),goal,sorted(r.keys),flush=True)
  if returned_at is not None and f-returned_at>=int(fps*10+1):break
 else:raise AssertionError('Sortie non atteinte dans le délai de capture')
 required=('declenchement','transformation','texte_intro','exploration','combat_oni','defaite_oni','sortie_controles_rendus') if defeat_demo else ('declenchement','transformation','texte_intro','exploration','interaction_porte','sortie_controles_rendus')
 assert all(k in events for k in required),events
 if defeat_demo:
  assert 'victoire_oni' not in events and 'interaction_porte' not in events
  assert r.read(r.symbols['gBattleOutcome'],1)==b'\2'
  hp,maxhp=struct.unpack('<HH',r.read(party+86,4));assert hp==maxhp and hp>0,(hp,maxhp)
 assert (frames-1-returned_at)/fps>=10
 r.lib.retro_set_audio_sample_batch(r.callbacks[3]);audio.close();audio=None
 encoder.stdin.close();assert encoder.wait()==0,(work/'ffmpeg.log').read_text();encoder=None;log.close();log=None
 output=P/('defaite-oni-mgba.mp4' if defeat_demo else 'declenchement-porte-sortie-mgba.mp4')
 subprocess.run(['ffmpeg','-y','-i',str(work/'video.mp4'),'-i',str(work/'audio.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest',str(output)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)],text=True))
 metadata={'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'video':output.name,'video_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'scope':__doc__,'preparation':{'oni':('Gargaros','Ogralos','Orqanos')[demo_tier],'grotte_depart':demo_map,'tirage_porte_natif_seed':chosen[0],'etage_porte':floors[chosen[2]]['map'],'distance_minimale_pas':chosen[3],'equipe':f'Seigneur Enma niveau {demo_level}, statistiques naturelles et capacités naturelles'+('; Météores placé en premier.' if not defeat_demo else ' de début de partie, volontairement trop faible face au boss.')+' Aucun résultat de combat imposé.','depart':'Visite réussie préparée juste avant son dernier pas programmé. Équipe et position préparées avant capture. Aucune mutation RAM ni téléportation pendant la vidéo.'},'frames':frames,'fps':fps,'duree_secondes':float(info['format']['duration']),'taille_octets':output.stat().st_size,'evenements_secondes':events,'alertes':alerts,'objectif_fuite_sans_combat':escape_only,'objectif_defaite_reelle':defeat_demo,'chronometre':'Durée normale de 300 secondes, jamais modifiée pendant la capture. '+('Retour après combat perdu, équipe rétablie par le jeu.' if defeat_demo else 'Sortie par interaction réelle avec la porte.'),'montage':'Continu, sans coupe ni accélération. Image agrandie x3 au plus proche voisin.','audio':'Sortie directe mGBA, encodée en AAC 48 kHz pour le MP4. Aucune OST modifiée.'}
 (P/'ENREGISTREMENT_SORTIE.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n');print(json.dumps(metadata,ensure_ascii=False,indent=2),flush=True)
except BaseException as error:
 (P/'ECHEC.json').write_text(json.dumps({'erreur':str(error),'frames':frames,'evenements':events,'alertes':alerts,'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest()},ensure_ascii=False,indent=2)+'\n');raise
finally:
 if audio:r.lib.retro_set_audio_sample_batch(r.callbacks[3]);audio.close()
 if encoder:
  encoder.stdin.close();encoder.wait()
 if log:log.close()
 r.close()

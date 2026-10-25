#!/usr/bin/env python3
"""Session persistante filmée : touches uniquement, lectures RAM pour observer.
Aucun RPC, aucune écriture de RAM, aucun warp ni modification de sauvegarde.
La vidéo native continue est conservée; le montage ×5/×1 est produit séparément.
"""
import ctypes as C,hashlib,json,os,re,struct,sys,subprocess,time,wave,types
from pathlib import Path
from mgba_rpc import Emulator,ROOT,BATCH
OUT=Path('/workspace/artifacts/aventure-filmee-20261025');OUT.mkdir(exist_ok=True)
class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
class Player(Emulator):
 def assemble_stub(self):pass
 def call(self,*a,**k):raise RuntimeError('RPC interdit pendant la partie filmée')
 def write(self,*a,**k):raise RuntimeError('Écriture RAM interdite pendant la partie filmée')
 def w32(self,*a,**k):raise RuntimeError('Écriture RAM interdite pendant la partie filmée')
 def __init__(self):
  self.frames=0;self.recording=False;self.last_a=-999;self.waiting=None;self.wait_since=0;self.initial=True;self.part=0;self.inputs=[];self.speeds=[];self.events=[];self.last_map=None;self.last_text=None
  super().__init__(rom=OUT/'jeu.gba',initial_frames=0)
  self.elf_path=OUT/'jeu.elf'
  self.reverse={int(f[0],16)|1:f[2] for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(self.elf_path)],text=True).splitlines() if len(f:=line.split())==3}
  self.capture_attempt=False
  if os.environ.get('YOKAI_RESUME_SAV'):
   battery=Path(os.environ['YOKAI_RESUME_SAV']).read_bytes();assert len(battery)==131072
   self.lib.retro_get_memory_size.argtypes=[C.c_uint];self.lib.retro_get_memory_size.restype=C.c_size_t
   self.lib.retro_get_memory_data.argtypes=[C.c_uint];self.lib.retro_get_memory_data.restype=C.c_void_p
   assert self.lib.retro_get_memory_size(0)==len(battery)
   C.memmove(self.lib.retro_get_memory_data(0),battery,len(battery))
   self.resume_hash=hashlib.sha256(battery).hexdigest()
  else:self.resume_hash=None
  existing=[int(p.name.split('-')[1]) for p in OUT.glob('partie-*') if (p/'ENREGISTREMENT.json').exists()]
  self.part=max(existing,default=-1)+1
  self.start_recording()
 def start_recording(self):
  av=AV();self.lib.retro_get_system_av_info(C.byref(av));self.fps=av.timing.fps;self.rate=round(av.timing.rate);self.part_start=self.frames;self.directory=OUT/f'partie-{self.part:02}';self.directory.mkdir(exist_ok=True);self.inputs=[];self.speeds=[];self.events=[]
  self.wav=wave.open(str(self.directory/'audio-natif.wav'),'wb');self.wav.setparams((2,2,self.rate,0,'NONE','not compressed'))
  self.audio_callback=BATCH(lambda p,n:(self.wav.writeframesraw(C.string_at(p,n*4)) or n));self.lib.retro_set_audio_sample_batch(self.audio_callback)
  fmt={0:'rgb555le',1:'bgr0',2:'rgb565le'}[self.pixel_format];self.bpp=4 if self.pixel_format==1 else 2
  self.fflog=(self.directory/'encodeur.log').open('wb');self.encoder=subprocess.Popen(['ffmpeg','-nostats','-loglevel','warning','-y','-f','rawvideo','-pixel_format',fmt,'-video_size','240x160','-framerate',str(self.fps),'-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-an',str(self.directory/'video-native.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=self.fflog);self.recording=True
 def callback(self):return self.reverse.get(self.u32(self.symbols['gMain']+4),'?')
 def tasks(self):return {self.reverse.get(self.u32(self.symbols['gTasks']+40*i),'?') for i in range(16) if self.read(self.symbols['gTasks']+40*i+4,1)==b'\1'}
 def importance(self):
  if self.initial:return 1,'Lancement et introduction'
  cb=self.callback()
  if 'sTh' in self.symbols and self.read(self.symbols['sTh']+175,1)==b'\1':return 1,'Terr’heure'
  if cb=='CB2_Overworld':
   sb=self.u32(self.symbols['gSaveBlock1Ptr']);g,n=self.read(sb+4,2);name=maps.get((g,n),'?')
   if name=='LavenderTown' or name.startswith('PokemonTower_'):return 1,'Zombie Night et Tour'
   if self.read(self.symbols['sLockFieldControls'],1)!=b'\0' or self.read(self.symbols['sGlobalScriptContextStatus'],1)!=b'\2':return 1,'Dialogue ou cinématique'
   return 5,'Trajet ordinaire'
  if cb=='BattleMainCB2':
   if self.capture_attempt:return 1,'Tentative de capture'
   flags=self.u32(self.symbols['gBattleTypeFlags']);trainer=int.from_bytes(self.read(self.symbols['gTrainerBattleOpponent_A'],2),'little')
   if flags&((1<<13)|(1<<18)):return 1,'Rencontre légendaire'
   if flags&8 and trainer in important_trainers:return 1,'Combat important'
   return 5,'Combat ordinaire'
  return 1,'Interface ou transition'
 def allow_a(self):
  cb=self.callback();tasks=self.tasks()
  if 'Naming' in cb or any('HandleGenderInput' in t or 'HandleDifficulty' in t or 'YesNo' in t or 'Multichoice' in t or 'HandleRivalNameInput' in t or 'ConfirmNameInput' in t for t in tasks):return True
  if cb=='BattleMainCB2':
   ctrl=self.reverse.get(self.u32(self.symbols['gBattlerControllerFuncs']),'')
   if any(x in ctrl for x in ('ChooseAction','ChooseMove','YesNo')):return True
  data=self.read(self.symbols['sTextPrinters'],36*32);active=[data[i*36:(i+1)*36] for i in range(32) if data[i*36+27]]
  if any(b[28]==0 for b in active):self.waiting=None;return False
  key=tuple((b[4],struct.unpack_from('<I',b)[0],b[28]) for b in active)
  if key!=self.waiting:self.waiting=key;self.wait_since=self.frames
  return self.frames-self.wait_since>=90 and self.frames-self.last_a>=12
 def run(self,n=1):
  if not self.recording:
   super().run(n);self.frames+=n;return
  proposed=set(self.keys)
  for _ in range(n):
   speed,why=self.importance();actual=set(proposed)
   if speed==1 and 8 in actual and not self.allow_a():actual.remove(8)
   self.keys=actual
   if 8 in actual:self.last_a=self.frames
   f=self.frames-self.part_start
   if not self.inputs or self.inputs[-1]['keys']!=sorted(actual):self.inputs.append({'frame':f,'keys':sorted(actual)})
   if not self.speeds or (self.speeds[-1]['speed'],self.speeds[-1]['reason'])!=(speed,why):self.speeds.append({'frame':f,'speed':speed,'reason':why})
   super().run(1);self.frames+=1
   if self.frame_packet:
    raw,w,h,pitch=self.frame_packet
    if pitch==240*self.bpp:self.encoder.stdin.write(raw)
    else:
     for y in range(160):self.encoder.stdin.write(raw[y*pitch:y*pitch+240*self.bpp])
   else:self.encoder.stdin.write(bytes(240*160*self.bpp))
  self.keys=proposed
 def seal(self,title):
  self.recording=False;self.encoder.stdin.close();assert self.encoder.wait()==0;self.wav.close();self.fflog.close()
  meta={'rom_sha256':hashlib.sha256(self.rom_buffer.raw[:-1]).hexdigest(),'rom_commit':os.environ.get('YOKAI_RECORD_COMMIT','f4979a031'),'title':title,'start_frame':self.part_start,'end_frame':self.frames,'frames':self.frames-self.part_start,'fps':self.fps,'audio_rate':self.rate,'resume_native_battery_sha256':self.resume_hash,'policy':'×5 ordinaire; ×1 cinématiques, dialogues et combats importants, Zombie Night, Terr’heure et légendaires','no_rpc':True,'no_game_ram_writes':True,'inputs':self.inputs,'speed_events':self.speeds,'chapters':self.events}
  (self.directory/'ENREGISTREMENT.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'sealed':str(self.directory),'frames':meta['frames']}),flush=True)
  self.part+=1;self.start_recording()
r=Player();r.run(1);groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={(i,j):n for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
important_trainers=set(range(410,423))|set(range(743,755))
# Vanilla rivals, Council rematches and story bosses. IDs are read from source constants.
for name,value in re.findall(r'#define\s+(TRAINER_\w+)\s+(\d+)',(ROOT/'include/constants/opponents.h').read_text()):
 if any(x in name for x in ('RIVAL','CHAMPION','ELITE_FOUR','LEADER','BOSS','ADMIN','YOKAI_','JUSTE_YOANN')):important_trainers.add(int(value))
chars={int(m[2],16):m[1] for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M) if len(m[1])==1 and ord(m[1])<0x3000}
def decode(b):
 out='';i=0
 while i<len(b):
  c=b[i];i+=1
  if c==255:break
  if c in (250,251,254):out+=' | ';continue
  if c==252:i+=2;continue
  if c==253:i+=1;continue
  out+=chars.get(c,'')
 return out
# Reuse the established read-only observation routine, without launching its old session.
old=(ROOT/'tools/yokai/parcours_joueur_mgba.py').read_text();a=old.index('def state():');b=old.index('\ndef pulse(',a);namespace={'r':r,'rev':r.reverse,'chars':chars,'maps':maps,'struct':struct,'decode':decode};exec(old[a:b],namespace);observe=namespace['state']
def pulse(keys,hold=1,after=20):r.keys=set();r.run(4);r.keys=set(keys);r.run(hold);r.keys=set();r.run(after)
def wait_task(name,press=True,limit=30000):
 for f in range(limit):
  if name in r.tasks():r.keys=set();return
  r.keys={8} if press and f%16<3 else set();r.run()
 raise RuntimeError(('Task timeout',name,r.tasks(),r.callback()))
def wait_naming():
 for f in range(24000):
  if 'Naming' in r.callback():r.keys=set();r.run(180);return
  r.keys={8} if f%16<3 else set();r.run()
 raise RuntimeError('Naming screen absent')
def boot():
 r.events.append({'frame':r.frames,'title':'Lancement — Nathan, mode Normal'})
 wait_task('Task_OakSpeech_HandleGenderInput');pulse([8],1,20)
 wait_task('Task_HandleDifficulty');pulse([8],1,20)
 wait_naming()
 # N A T H A N on the native upper-case keyboard, using only arrow/A inputs.
 x=y=0
 for tx,ty in [(1,2),(0,0),(0,3),(1,1),(0,0),(1,2)]:
  while x!=tx:pulse([7 if tx>x else 6],1,12);x+=1 if tx>x else -1
  while y!=ty:pulse([5 if ty>y else 4],1,12);y+=1 if ty>y else -1
  pulse([8],1,15)
 pulse([3],1,15);pulse([8],1,30)
 wait_task('Task_OakSpeech_HandleConfirmNameInput');pulse([8],1,30)
 for f in range(24000):
  if r.callback()=='CB2_Overworld':break
  tasks=r.tasks()
  if 'Task_OakSpeech_HandleRivalNameInput' in tasks:
   pulse([5],1,15);pulse([5],1,15);pulse([8],1,30)
  elif 'Task_OakSpeech_HandleConfirmNameInput' in tasks:pulse([8],1,30)
  else:r.keys={8} if f%16<3 else set();r.run()
 else:raise RuntimeError('No new game field')
 r.keys=set();r.run(180);r.initial=False
 assert decode(r.read(r.u32(r.symbols['gSaveBlock2Ptr']),8))=='NATHAN'
# Existing navigation and combat pilots use only reads and joypad inputs.
import parcours_navigation
parcours_navigation.ROOT=OUT;parcours_navigation.CACHE=OUT/'CARTE_VUE.json'
combat=types.ModuleType('combat_filme');code=(ROOT/'tools/yokai/parcours_combat.py').read_text().replace('/workspace/artifacts/parcours-joueur-20261024',str(OUT));exec(code,combat.__dict__)
def advance(limit=12000):
 idle_frames=0
 for i in range(limit):
  s=observe()
  if any('YesNo' in t or 'Multichoice' in t or 'Shop' in t for t in s['tasks']):break
  if s['callback']=='BattleMainCB2' or 'Naming' in s['callback']:break
  idle=s['callback']=='CB2_Overworld' and r.read(r.symbols['sLockFieldControls'],1)==b'\0' and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2'
  idle_frames=idle_frames+1 if idle else 0
  if idle_frames>=45:break
  r.keys={8} if not idle and i%16<3 else set();r.run()
 r.keys=set()
print(json.dumps({'ready':True,'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'state':observe()},ensure_ascii=False),flush=True)
for line in sys.stdin:
 try:
  cmd=json.loads(line);op=cmd['op']
  if op=='boot':boot()
  elif op=='continue':
   assert r.resume_hash,'No native battery loaded'
   for i in range(30000):
    r.keys={8} if i%16<3 else set();r.run()
    if r.callback()=='CB2_Overworld' and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3):break
   else:raise RuntimeError('Native Continue timed out')
   r.keys=set();r.run(180);r.initial=False
  elif op=='press':pulse(cmd.get('keys',[]),cmd.get('hold',1),cmd.get('after',20))
  elif op=='sequence':
   for k,h,a in cmd['steps']:pulse(k,h,a)
  elif op=='wait':r.keys=set();r.run(cmd.get('frames',60))
  elif op=='mash':
   for i in range(cmd.get('frames',600)):r.keys=set(cmd.get('keys',[8])) if i%16<3 else set();r.run()
   r.keys=set()
  elif op=='advance':advance(cmd.get('frames',12000))
  elif op=='nav':print(json.dumps(parcours_navigation.navigate(r,cmd['goal'],pulse,cmd.get('steps',160))),flush=True)
  elif op=='battle':combat.fight(r,observe,cmd)
  elif op=='flee':print(combat.flee(r,pulse,observe),flush=True)
  elif op=='throw':r.capture_attempt=True;print(combat.throw_ball(r,pulse,observe),flush=True)
  elif op=='capture_result':print(combat.finish_capture(r,observe,cmd.get('frames',6000)),flush=True);r.capture_attempt=False
  elif op=='chapter':r.events.append({'frame':r.frames-r.part_start,'title':cmd['title']})
  elif op=='save_ui':
   previous=r.u32(r.symbols['gSaveCounter']);pulse([3],1,90);order=list(r.read(r.symbols['sStartMenuOrder'],r.read(r.symbols['sNumStartMenuItems'],1)[0]));target=order.index(4)
   for _ in range(12):
    if r.read(r.symbols['sStartMenuCursorPos'],1)[0]==target:break
    pulse([5],1,16)
   pulse([8],1,120)
   for i in range(3600):
    r.keys={8} if i%20<3 else set();r.run()
    if r.u32(r.symbols['gSaveCounter'])!=previous and i>180:break
   r.keys=set();advance();assert r.u32(r.symbols['gSaveCounter'])!=previous
  elif op=='export':
   from parcours_sauvegardes import native_battery
   dest=OUT/cmd['name'];dest.mkdir(exist_ok=True);(dest/'Pokemon_Yokai_Watch_Cinematiques.sav').write_bytes(native_battery(r.snapshot()));(dest/'ETAT.json').write_text(json.dumps(observe(),ensure_ascii=False,indent=2)+'\n');r.frame.save(dest/'ecran.png')
  elif op=='seal':r.seal(cmd['title'])
  elif op!='state':raise ValueError(op)
  s=observe();r.frame.save(OUT/'courant.png');(OUT/'COURANT.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(OUT/'courant.state').write_bytes(r.snapshot());print(json.dumps(s,ensure_ascii=False),flush=True)
 except Exception as e:
  if r.frame:r.frame.save(OUT/'erreur.png')
  print(json.dumps({'error':repr(e),'state':observe()},ensure_ascii=False),flush=True)

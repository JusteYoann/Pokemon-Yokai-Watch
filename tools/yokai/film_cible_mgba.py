"""Capture native avec son ; préparation externe puis boutons seuls pendant le film."""
import ctypes as C,hashlib,json,struct,subprocess,wave
from pathlib import Path
from mgba_rpc import BATCH
class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
class Film:
 def __init__(self,r,target):
  self.r=r;self.target=Path(target);self.target.parent.mkdir(parents=True,exist_ok=True);self.work=self.target.parent/(self.target.stem+'-travail');self.work.mkdir(exist_ok=True)
  self.rev={int(f[0],16)|1:f[2] for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3}
  self.frames=0;self.events=[];self.waiting=None;self.since=0;self.started=False;self.won=False;self.idle_since=None;self.last_trainer=None
  av=AV();r.lib.retro_get_system_av_info(C.byref(av));self.fps=av.timing.fps
  self.log=(self.work/'encodage.log').open('wb');self.wav=wave.open(str(self.work/'audio.wav'),'wb');self.wav.setparams((2,2,round(av.timing.rate),0,'NONE','not compressed'))
  self.audio=BATCH(lambda p,n:(self.wav.writeframesraw(C.string_at(p,n*4)) or n));r.lib.retro_set_audio_sample_batch(self.audio)
  fmt={0:'rgb555le',1:'bgr0',2:'rgb565le'}[r.pixel_format];self.bpp=4 if r.pixel_format==1 else 2
  self.enc=subprocess.Popen(['ffmpeg','-nostats','-loglevel','warning','-y','-f','rawvideo','-pixel_format',fmt,'-video_size','240x160','-framerate',str(self.fps),'-i','pipe:0','-vf','scale=720:480:flags=neighbor','-c:v','libx264','-threads','2','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-an',str(self.work/'video.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=self.log)
  self.native_run=r.run;r.run=self.run
  self.native_call=r.call;self.native_write=r.write;self.native_w32=r.w32
  def blocked(*a,**k):raise RuntimeError('Aucune injection autorisée après le début du film')
  r.call=r.write=r.w32=blocked
 def callback(self):return self.rev.get(self.r.u32(self.r.symbols['gMain']+4),'?')
 def run(self,n=1):
  for _ in range(n):
   self.native_run();self.frames+=1
   raw,w,h,p=self.r.frame_packet
   self.enc.stdin.write(raw if p==w*self.bpp else b''.join(raw[y*p:y*p+w*self.bpp] for y in range(h)))
 def paced(self,keys):
  if 8 not in keys:return keys
  r=self.r;ctrl=self.rev.get(r.u32(r.symbols['gBattlerControllerFuncs']),'')
  if 'ChooseAction' in ctrl or 'ChooseMove' in ctrl:return keys
  tasks=[self.rev.get(r.u32(r.symbols['gTasks']+40*i),'') for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\1']
  if any('Multichoice' in s or 'YesNo' in s for s in tasks):return keys
  b=r.read(r.symbols['sTextPrinters'],1152);active=[b[i:i+36] for i in range(0,1152,36) if b[i+27]]
  if any(p[28]==0 for p in active):self.waiting=None;return set()
  key=tuple((p[:4],p[28]) for p in active)
  if key!=self.waiting:self.waiting=key;self.since=self.frames
  return keys if self.frames-self.since>=60 else set()
 def controls(self):
  r=self.r;f=self.frames;cb=self.callback();key=8
  if cb=='CB2_UpdatePartyMenu':
   slot=min(r.read(r.symbols['gPartyMenu']+9,1)[0],5)
   key=0 if int.from_bytes(r.read(r.symbols['gBattleMons']+40,2),'little') else 8 if int.from_bytes(r.read(r.symbols['gPlayerParty']+100*slot+86,2),'little') else 5
  elif cb=='BattleMainCB2':
   self.started=True;trainer=int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')
   if trainer!=self.last_trainer:self.last_trainer=trainer;self.events.append({'seconds':f/self.fps,'trainer':trainer})
   ctrl=self.rev.get(r.u32(r.symbols['gBattlerControllerFuncs']),'')
   if ctrl=='HandleInputChooseAction':
    cursor=r.read(r.symbols['gActionSelectionCursor'],1)[0];key=6 if cursor&1 else 4 if cursor&2 else 8
   elif ctrl=='HandleInputChooseMove':
    own=r.read(r.symbols['gBattleMons'],88);enemy=r.read(r.symbols['gBattleMons']+88,88);choices=[]
    for i in range(4):
     move=int.from_bytes(own[12+i*2:14+i*2],'little')
     if not move or not own[36+i]:continue
     data=r.read(r.symbols['gBattleMoves']+12*move,12);typ=data[2];power=data[1];factor=1
     table=r.read(r.symbols['gTypeEffectiveness'],1024)
     for j in range(0,len(table)-2,3):
      a,d,m=table[j:j+3]
      if a==255:break
      if a==typ and d in set(enemy[33:35]):factor*=m/10
     if (typ,enemy[32]) in ((10,18),(13,10),(11,11)):factor=0
     stat=int.from_bytes(own[2:4] if typ<10 else own[8:10],'little')
     choices.append((power*factor*stat*(1.5 if typ in own[33:35] else 1),-i))
    target=-max(choices)[1] if choices else 0;cur=r.read(r.symbols['gMoveSelectionCursor'],1)[0]
    if (target&1)!=(cur&1):key=7 if target&1 else 6
    elif (target&2)!=(cur&2):key=5 if target&2 else 4
   elif 'YesNo' in ctrl:key=0
  return self.paced({key}) if f%16<2 else set()
 def finish(self,**info):
  r=self.r;r.keys=set();r.run=self.native_run;r.call=self.native_call;r.write=self.native_write;r.w32=self.native_w32
  self.enc.stdin.close();assert self.enc.wait()==0;self.wav.close()
  self.audio=BATCH(lambda p,n:n);r.lib.retro_set_audio_sample_batch(self.audio)
  subprocess.run(['ffmpeg','-nostats','-loglevel','warning','-y','-i',str(self.work/'video.mp4'),'-i',str(self.work/'audio.wav'),'-c:v','copy','-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart',str(self.target)],stdout=subprocess.DEVNULL,stderr=self.log,check=True);self.log.close()
  result=dict(rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),native_mgba_audio=True,speed=1,continuous=True,buttons_only_during_capture=True,frames=self.frames,seconds=self.frames/self.fps,events=self.events,**info)
  self.target.with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('FILM',self.target,self.target.stat().st_size,flush=True)

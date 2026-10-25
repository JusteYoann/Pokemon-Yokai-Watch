#!/usr/bin/env python3
"""Rejoue les scènes existantes sans nouvelle vidéo puis vérifie START et les déplacements.
Chaque scène utilise une partie isolée et les prérequis documentés du pilote cinéma.
Les équipes ennemies et résultats ne sont pas modifiés. Ce n'est pas un parcours continu.
"""
import ctypes,json,os,re,struct,subprocess,sys,time,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from mgba_rpc import ROOT
import film_cible_mgba as cinema
D=ROOT/'docs/verification-cinematiques-20261025';D.mkdir(exist_ok=True)
source=(ROOT/'tools/yokai/enregistrer_cinematiques_mgba.py').read_text()
rom_sha=hashlib.sha256(Path(os.environ.get('YOKAI_QA_ROM',str(ROOT/'pokefirered.gba'))).read_bytes()).hexdigest()
def valid_report(name):
 p=D/(name+'.json')
 if not p.exists():return False
 report=json.loads(p.read_text());return report.get('passed') is True and report.get('rom_sha256')==rom_sha
names=re.findall(r"^ '([^']+)':",source,re.M)+[f'arene-{i:02}' for i in range(1,9)]+[f'conseil-{i:02}' for i in range(1,5)]
if sys.argv[1] in ('--all','--failed'):
 if sys.argv[1]=='--failed':names=[n for n in names if not valid_report(n)]
 def work(name):
  start=time.time()
  with (D/(name+'.log')).open('w') as log:code=subprocess.run([sys.executable,__file__,name],stdout=log,stderr=subprocess.STDOUT).returncode
  result=dict(scene=name,passed=code==0,seconds=round(time.time()-start,2));print(json.dumps(result),flush=True);return result
 with ThreadPoolExecutor(max_workers=4) as pool:rows=[f.result() for f in as_completed([pool.submit(work,n) for n in names])]
 all_names=re.findall(r"^ '([^']+)':",source,re.M)+[f'arene-{i:02}' for i in range(1,9)]+[f'conseil-{i:02}' for i in range(1,5)]
 rows=[dict(scene=n,passed=valid_report(n)) for n in all_names]
 (D/'BILAN.json').write_text(json.dumps(dict(passed=all(x['passed'] for x in rows),rom_sha256=rom_sha,scope=__doc__,scenes=sorted(rows,key=lambda x:x['scene'])),ensure_ascii=False,indent=2)+'\n')
 sys.exit(0 if all(x['passed'] for x in rows) else 1)
name=sys.argv[1];assert name in names
if name=='02-argenta':
 proofs=[D/f'argenta-{gender}/TEST_MGBA.json' for gender in (0,1)]
 reports=[json.loads(p.read_text()) for p in proofs];assert all(r['passed'] and len(r['results'])==4 for r in reports)
 assert len({r['rom_sha256'] for r in reports})==1
 (D/(name+'.json')).write_text(json.dumps(dict(passed=True,scene=name,rom_sha256=reports[0]['rom_sha256'],checks=dict(real_Route2_entries=8,both_genders=True,speech_finished=True,controls_menu_and_building_return=True),proofs=[str(p.relative_to(ROOT)) for p in proofs]),ensure_ascii=False,indent=2)+'\n')
 print('PASS Argenta: huit arrivées réelles et retours');sys.exit(0)
scope={'__name__':'__main__','__file__':str(ROOT/'tools/yokai/enregistrer_cinematiques_mgba.py')}
class Verification(cinema.Film):
 def __init__(self,r,target):
  self.r=r;self.target=Path(target);self.frames=0;self.events=[];self.waiting=None;self.since=0;self.started=False;self.last_trainer=None
  self.rev={v|1:k for k,v in r.symbols.items()};av=cinema.AV();r.lib.retro_get_system_av_info(ctypes.byref(av));self.fps=av.timing.fps
  self.native_run=r.run;r.run=self.run;self.diploma_start=None
 def run(self,n=1):
  self.native_run(n);self.frames+=n
 def controls(self):
  if self.callback()=='CB2_Diploma':
   if self.diploma_start is None:self.diploma_start=self.frames
   return {8} if self.frames-self.diploma_start>300 and self.frames%16<2 else set()
  return super().controls()
 def finish(self,**info):
  q=scope['q'];r=self.r;r.run=self.native_run;r.keys=set();checks={}
  if q.callback()=='CB2_Overworld':
   assert q.idle(),'Script or field controls still locked'
   checks['script_finished']=True;checks['controls_unlocked']=True
   before=struct.unpack('<hh',r.read(r.u32(r.symbols['gSaveBlock1Ptr']),4));mp=next(n for n,pair in q.maps.items() if pair==tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)))
   data=json.loads((ROOT/f'data/maps/{mp}/map.json').read_text());avoid={(ev['x'],ev['y']) for key in ('coord_events','warp_events') for ev in data.get(key,[])}
   player=q.actors()[255];walk=False
   for dx,dy,key,d in [(0,1,5,1),(1,0,7,4),(-1,0,6,3),(0,-1,4,2)]:
    x,y=before[0]+dx,before[1]+dy
    if (x,y) in avoid or r.call('GetCollisionAtCoords',player,x+7,y+7,d):continue
    r.keys={key};r.run(16);r.keys=set();r.run(32)
    after=struct.unpack('<hh',r.read(r.u32(r.symbols['gSaveBlock1Ptr']),4));walk=after!=before
    if walk:break
   assert walk,'No traversable direction responded to controller input'
   checks['native_player_moved']=True
   if name=='09-terreur':checks['menu']='Terr’heure active: restriction prévue'
   else:
    menu=False
    for _ in range(3):
     q.pulse(3,90)
     menu=any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_StartMenuHandleInput']|1 for i in range(16))
     if menu:break
    if not menu:
     r.frame.save(D/(name+'-menu-diagnostic.png'));print('MENU_DIAGNOSTIC',q.callback(),q.idle(),hex(r.u32(r.symbols['sGlobalScriptContext']+8)),[(self.rev.get(r.u32(r.symbols['gTasks']+40*i)),r.read(r.symbols['gTasks']+40*i+8,8).hex()) for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\1'],flush=True)
    assert menu,'START did not open the field menu'
    checks['native_start_menu']=True;q.pulse(0,90)
  else:
   assert name=='08-finale',('Unexpected final callback',q.callback())
   checks['native_return_after_credits']=q.callback()
  r.frame.save(D/(name+'-controle.png'))
  info.pop('scene',None)
  result=dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scene=name,frames=self.frames,seconds=self.frames/self.fps,events=self.events,checks=checks,**info)
  (D/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS',name,checks,flush=True)
cinema.Film=Verification
source=source.replace("from mafiamille_qa import C","from mafiamille_qa import C\nC.update(VAR_TEMP_F=0x400F, VAR_PHILOSOVNI_STATE=0x40F4)")
source=source.replace(" q.warp(map_,x,y)\n  if not trigger"," q.warp(map_,x,y)\n  if trigger:r.call('VarSet',C[trigger['var']],int(trigger['var_value']))\n  if not trigger")
source=source.replace("D=ROOT/'docs/cinematiques-compilation-20261025'","D=ROOT/'docs/verification-cinematiques-20261025'")
# Current routes and quest states replace obsolete movie-only preparations.
source=source.replace("('RocketHideout_B4F',25,4,","('RocketHideout_B4F',19,5,")
source=source.replace("for i in range(1,152):r.call('GetSetPokedexFlag',i,3)","for i in range(1,152):\n   r.call('GetSetPokedexFlag',i,2);r.call('GetSetPokedexFlag',i,3)")
source=source.replace(" for var,value in variables:r.call('VarSet',var,value)"," if name in ('13-alizon-quete-oni','14-alizon-rendez-vous'):\n  for enemy in ('TRAINER_BUG_MANIAC','TRAINER_RS_PSYCHIC_M','TRAINER_RS_PSYCHIC_F'):r.call('SetTrainerFlag',C[enemy])\n for var,value in variables:r.call('VarSet',var,value)")
source=source.replace("[(0x4076,2)]","[(0x4076,4)]").replace("[(0x4076,3)]","[(0x4076,5)]")
exec(compile(source,scope['__file__'],'exec'),scope)

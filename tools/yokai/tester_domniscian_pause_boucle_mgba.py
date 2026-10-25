#!/usr/bin/env python3
"""Un cycle complet réel de Vs Hinozall puis 15s de pause, dans le vrai combat.
Équipe et point de départ préparés ; aucun curseur audio ni résultat injecté.
"""
import json,struct,subprocess,wave,hashlib
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
from film_cible_mgba import Film
D=ROOT/'docs/gorgouille-alizon-20261025';D.mkdir(exist_ok=True)
q=QA('TEMP.json');r=q.r
try:
 q.mon();q.f(0x3e);r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0xee0+0x500//8,b'\xff'*96);r.call('ClearTrainerFlag',420)
 q.warp('SaffronCity_Gym',14,13);q.script('SaffronCity_Gym_EventScript_Sabrina');q.wait(lambda:q.callback()=='BattleMainCB2',20000)
 actions={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
 q.wait(lambda:r.u32(r.symbols['gBattlerControllerFuncs']) in actions,12000);r.keys=set();r.run(30)
 gap=next(v for n,v in r.symbols.items() if n.startswith('gap.'))
 def channel():return r.u32(r.u32(r.symbols['gMPlayInfo_BGM']+44)+32)
 ch=channel();assert not(r.read(ch,1)[0]&16)
 count=r.u32(ch+24);r.run(60);per_frame=(count-r.u32(ch+24))/60
 assert per_frame>0
 # Run the full original sample to five seconds before its natural end.
 wait=max(0,int(r.u32(channel()+24)/per_frame)-300);r.run(wait)
 movie=Film(r,D/'domniscian-pause-15s-mgba.mp4');start=None;end=None;gap_values=[];se_input=False
 for f in range(2400):
  value=int.from_bytes(r.read(gap,2),'little')
  if value:
   if start is None:start=f
   gap_values.append(value)
   # A command-menu cursor movement demonstrates that SE remain active.
   if value==450:r.keys={7};se_input=True
   else:r.keys=set()
  else:
   r.keys=set()
   if start is not None and end is None:end=f
  r.run()
  if end is not None and f-end>=180:break
 else:raise AssertionError(('No complete 15s pause',start,end))
 assert gap_values[0]==896 and gap_values[-1]==1 and end-start==896,(start,end,gap_values[:2],gap_values[-2:])
 assert se_input and channel() and r.read(channel(),1)[0]&0xc7
 movie.finish(music='Vs Hinozall',gap_frames=896,gap_seconds=896/movie.fps,sound_effect_command_during_gap=True,native_full_original_loop=True)
 # PCM checks distinguish the BGM silence from the command SE in its middle.
 with wave.open(str(movie.work/'audio.wav'),'rb') as w:
  rate=w.getframerate();raw=w.readframes(w.getnframes())
 def energy(a,b):
  data=raw[round(a*rate)*4:round(b*rate)*4];v=struct.unpack('<'+'h'*(len(data)//2),data);return sum(x*x for x in v)/max(1,len(v))
 quiet=energy(start/movie.fps+2,start/movie.fps+5);sound=energy((start+446)/movie.fps,(start+480)/movie.fps);music=energy((end+60)/movie.fps,(end+150)/movie.fps)
 assert music>quiet*20+1 and sound>quiet*5+1,(quiet,sound,music)
 # The same OST outside Domniscian retains its normal native loop flag.
 r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',414));r.call('PlayBGM',348);r.run(60)
 assert int.from_bytes(r.read(gap,2),'little')==0
 assert channel() and r.read(channel(),1)[0]&16
 (D/'TEST_AUDIO.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),full_sample_run_frames=wait+90,native_gap_frames=end-start,native_gap_seconds=(end-start)/movie.fps,pcm_energy_quiet=quiet,pcm_energy_SE=sound,pcm_energy_music_after=music,SE_remain_active=True,non_Domniscian_context_fixture_keeps_normal_loop=True),ensure_ascii=False,indent=2)+'\n')
 print('PASS pause native 15s, SE actifs, reprise de Vs Hinozall',flush=True)
finally:r.close()

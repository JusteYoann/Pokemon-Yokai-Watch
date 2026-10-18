#!/usr/bin/env python3
"""Controller boot/intro/title/help without script shortcuts; capture visible changes."""
import hashlib,json
from mgba_rpc import Emulator,ROOT
P=ROOT/'QA_RECETTE_FINALE/POST_B13/presentation';P.mkdir(exist_ok=True)
r=Emulator(initial_frames=0);captures=[];intro=set();title=False;help_pages=set();passed=False;error='Interrupted'
try:
 for f in range(1200):
  r.run();cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['CB2_RunYokaiPresentation']|1:
   tick=int.from_bytes(r.read(r.symbols['sPresentationTick'],2),'little');is_title=r.read(r.symbols['sPresentationTitle'],1)[0]
   if not is_title and tick in [65,210,290]:
    intro.add(tick);stem=f'intro-{tick}';r.frame.save(P/(stem+'.png'));captures.append(stem)
   if is_title and tick==80:r.frame.save(P/'titre.png');title=True;break
 assert title and intro=={65,210,290},('Missing cinematic/title phases',intro,title)
 def pulse(key,frames=8):r.keys=set();r.run(4);r.keys={key};r.run(2);r.keys=set();r.run(frames)
 pulse(3,180);r.frame.save(P/'menu-principal.png')
 # Fresh test save is empty: A selects real New Game.
 pulse(8,1);rev={v|1:k for k,v in r.symbols.items()}
 for f in range(12000):
  active=[i for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01' and rev.get(r.u32(r.symbols['gTasks']+40*i))=='Task_PikachuIntro_HandleInput']
  if active:
   task=active[0]
   # Page index belongs to Oak speech allocation; capture after stable input task and 80 frames.
   r.keys=set();r.run(80);page=int.from_bytes(r.read(r.u32(r.symbols['sOakSpeechResources'])+18,2),'little');stem=f'aide-{page+1}';r.frame.save(P/(stem+'.png'));help_pages.add(page)
   if len(help_pages)==3:break
   pulse(8,120)
  else:r.keys={8} if f%24<2 else set();r.run()
 assert help_pages=={0,1,2}
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_PRESENTATION_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Real power-on from frame0, no intro skip for cinematic, title START and controller help pages. No artistic human approval, full new-game save checked separately',cinematic_captures=captures,title_captured=title,help_pages=sorted(help_pages)),ensure_ascii=False,indent=2)+'\n');print('PRESENTATION',passed,error)

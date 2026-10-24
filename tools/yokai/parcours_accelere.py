"""Unthrottled road exploration, using only ordinary joypad actions."""
import json,time
from pathlib import Path
import parcours_navigation,importlib
importlib.reload(parcours_navigation)
from parcours_navigation import navigate
from parcours_combat import fight,flee
OUT=Path('/workspace/artifacts/parcours-joueur-20261024')

def travel(r,observe,pulse,command):
 start=observe();area=start['location']['map'];started=time.monotonic();first=r.frames;events=[];last_text=None
 for iteration in range(command.get('episodes',30)):
  s=observe();mode=s['callback']
  if s['location']['map']!=area:events.append('map transition');break
  if mode=='BattleMainCB2':
   trainer=bool(r.u32(r.symbols['gBattleTypeFlags'])&8)
   if not trainer and command.get('wild')=='flee':flee(r,pulse,observe)
   else:fight(r,observe,dict(frames=18000))
   events.append('trainer fight' if trainer else 'wild encounter');r.keys=set();r.run(180)
  elif mode in ('CB2_ReturnToFieldLocal','CB2_ReturnToField','CB2_OverworldBasic','CB2_InitBattle','CB2_HandleStartBattle'):
   r.keys=set();r.run(180)
  elif mode!='CB2_Overworld':events.append('interface: '+mode);break
  elif r.read(r.symbols['sGlobalScriptContextStatus'],1)!=b'\2' or r.read(r.symbols['sLockFieldControls'],1)!=b'\0':
   if not command.get('dialogues'):events.append('dialogue/event');break
   for f in range(6000):
    if f%8==0:
     t=observe()
     if t['text']!=last_text:
      last_text=t['text'];events.append(dict(dialogue=last_text));r.frame.save(OUT/('dialogue-'+str(r.frames)+'.png'))
     if t['callback'] not in ('CB2_Overworld','CB2_OverworldBasic','CB2_ReturnToFieldLocal','CB2_ReturnToField'):break
     if any('YesNo' in task or 'Multichoice' in task or 'Shop' in task for task in t['tasks']):break
     if f>8 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\2' and r.read(r.symbols['sLockFieldControls'],1)==b'\0':break
    r.keys={8} if f%16<3 else set();r.run()
   r.keys=set()
   if any('YesNo' in task or 'Multichoice' in task for task in observe()['tasks']):events.append('choice');break
  else:
   result=navigate(r,command['goal'],pulse,command.get('steps',200));events.append(result)
   if result['reason'] in ('arrived','no visible frontier/path'):break
  if observe()['battle'] and observe()['battle']['controller']=='HandleInputChooseMove' and iteration>5:events.append('battle still active');break
 elapsed=time.monotonic()-started
 return dict(events=events,frames=r.frames-first,wall_seconds=round(elapsed,2),speed_vs_realtime=round((r.frames-first)/59.7275/max(elapsed,.001),1))

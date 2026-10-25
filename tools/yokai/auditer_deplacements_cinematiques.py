#!/usr/bin/env python3
"""Inventaire intégral des déplacements scriptés, incluant les .inc ignorés par Git.
Analyse statique des références et des trajectoires relatives; ne prouve pas
l'absence de collision pour toutes les positions/sauvegardes possibles.
Les scénarios mGBA complètent cet inventaire.
"""
from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'docs/cinematiques-collisions-20261025';P.mkdir(exist_ok=True)
labels={};sites=[];paths=sorted((R/'data').rglob('*.inc'))+[R/'data/event_scripts.s']
for p in paths:
 current=None
 for line_no,line in enumerate(p.read_text().splitlines(),1):
  line=line.split('@')[0].strip();m=re.fullmatch(r'(\w+)::?',line)
  if m:current=m[1];labels[current]=[];continue
  if current:labels[current].append(line)
  m=re.match(r'applymovement\s+([^,]+),\s*(\w+)',line)
  if m:sites.append({'source':str(p.relative_to(R)),'line':line_no,'script':current,'actor':m[1],'movement':m[2]})
missing=[];trajectories={}
for site in sites:
 name=site['movement']
 if name not in labels:missing.append(site);continue
 if name in trajectories:continue
 pos=(0,0);points=[pos];instructions=[];finished=False
 for line in labels[name]:
  cmd=line.split()[0] if line else ''
  if cmd=='step_end':finished=True;break
  if not cmd or cmd.startswith('.'):continue
  instructions.append(line)
  m=re.fullmatch(r'(?:walk(?:_fast|_faster|_slow|_slowest)?|player_run|slide|jump(?:_2)?|jump_in_place)_(up|down|left|right)',cmd)
  if m and not cmd.startswith('jump_in_place'):
   dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[m[1]];scale=2 if cmd.startswith('jump_2_') else 1;pos=(pos[0]+dx*scale,pos[1]+dy*scale);points.append(pos)
 trajectories[name]={'instructions':instructions,'tiles_relative':points,'step_end':finished}
# Shared labels may fall through into another label; record rather than silently treating it as a complete proof.
report={'scope':__doc__,'script_files_with_movements':len(set(s['source'] for s in sites)),'movement_calls':len(sites),'movement_labels':len(trajectories),'unresolved_references':missing,'sites':sites,'trajectories':trajectories,'native_movement_call_files':[str(p.relative_to(R)) for p in sorted((R/'src').glob('*.c')) if 'ScriptMovement_StartObjectMovementScript(' in p.read_text()]}
(P/'INVENTAIRE_DEPLACEMENTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({k:report[k] for k in ('script_files_with_movements','movement_calls','movement_labels','unresolved_references')})
assert not missing

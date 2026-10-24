#!/usr/bin/env python3
"""Inventory automatic scenes and flag paths that may end without consuming a trigger."""
import re,json,collections,argparse,subprocess,csv
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser(description='Conservative control-flow triage, not a formal proof or a gameplay test.')
p.add_argument('--avant-argenta',action='store_true');p.add_argument('--rapport',type=Path,required=True);opts=p.parse_args();opts.rapport.mkdir(parents=True,exist_ok=True)
labels={};ops=[]
for p in sorted(list((R/'data').rglob('*.inc'))+[R/'data/event_scripts.s']):
 source=p.read_text()
 if opts.avant_argenta and p==R/'data/maps/PewterCity/morleone.inc':source=subprocess.check_output(['git','show','716712b08:data/maps/PewterCity/morleone.inc'],cwd=R,text=True)
 for n,line in enumerate(source.splitlines(),1):
  line=line.split('@',1)[0].strip()
  m=re.match(r'^(\w+)::?$',line)
  if m:labels[m[1]]=len(ops);continue
  if not line or line.startswith('@'):continue
  cmd,_,args=line.partition(' ');args=args.split('@')[0].strip();ops.append((cmd,[s.strip() for s in args.split(',')],str(p.relative_to(R)),n))
aliases={args[0]:args[1] for cmd,args,_,_ in ops if cmd=='.equ' and len(args)==2}
rows=[]
for p in sorted((R/'data/maps').glob('*/map.json')):
 for e in json.loads(p.read_text()).get('coord_events',[]):
  if e.get('script'):rows.append(dict(map=p.parent.name,kind='coordinate',**e))
for p in sorted((R/'data/maps').glob('*/scripts.inc')):
 for table in re.findall(r'map_script MAP_SCRIPT_ON_FRAME_TABLE, (\w+)',p.read_text()):
  pc=labels[table]
  while ops[pc][0]=='map_script_2':
   var,value,script=ops[pc][1];rows.append(dict(map=p.parent.name,kind='frame',script=script,var=var,var_value=value,x=0,y=0));pc+=1
unique={}
for e in rows:unique.setdefault((e['kind'],e['map'],e['script'],e['var'],e['var_value']),[]).append((e['x'],e['y']))
results=[]
for (kind,mp,label,var,value),positions in unique.items():
 todo=[(labels.get(label,-1),(),False,(),())];visited=set();bad=[];unknown=[];ends=0
 while todo:
  pc,stack,safe,specials,trace=todo.pop();key=(pc,stack,safe,specials)
  if key in visited:continue
  visited.add(key)
  if len(visited)>40000:unknown.append('limit');break
  if pc<0 or pc>=len(ops):unknown.append('missing target');continue
  cmd,a,f,n=ops[pc];a=[aliases.get(v,v) for v in a];trace=(*trace[-12:],f'{f}:{n} {cmd} '+','.join(a))
  def add(nextpc,st=stack,sa=safe,sp=specials):todo.append((nextpc,st,sa,sp,trace))
  if cmd in ('end','endram','gotoram'):
   ends+=1
   if not safe:
    if specials:unknown.append(dict(specials=specials,trace=trace))
    else:bad.append(trace)
  elif cmd=='return':
   if stack:add(stack[-1],stack[:-1])
   else:unknown.append('top-level return')
  elif cmd in ('setvar','addvar','subvar','copyvar','setorcopyvar'):
   changed=a[0]==var and (cmd!='setvar' or a[1]!=value)
   add(pc+1,sa=safe or changed)
  elif cmd in ('lock','lockall'):
   add(pc+1,sa=safe or kind=='coordinate')
  elif cmd=='applymovement':
   moved=False
   if a[0]=='LOCALID_PLAYER' and len(a)>1 and a[1] in labels:
    for op in ops[labels[a[1]]:labels[a[1]]+70]:
     if op[0]=='step_end':break
     if re.match(r'(walk|walk_fast|walk_slow|walk_faster|jump|run|slide)_(up|down|left|right)$',op[0]):moved=True
   add(pc+1,sa=safe or (moved and kind=='coordinate'))
  elif cmd.startswith('warp') or cmd in ('whiteout','gotopostbattlescript'):ends+=1
  elif cmd=='goto':add(labels.get(a[-1],-1))
  elif cmd=='call':
   if len(stack)>16:unknown.append('call stack limit')
   else:add(labels.get(a[-1],-1),(*stack,pc+1))
  elif cmd.startswith('goto_if') or cmd in ('case',):add(pc+1);add(labels.get(a[-1],-1))
  elif cmd.startswith('call_if'):add(pc+1);add(labels.get(a[-1],-1),(*stack,pc+1))
  elif cmd.startswith('special') or cmd in ('trainerbattle','trainerbattle_single','trainerbattle_double','dotrainerbattle','fadescreen','fadescreenspeed','dofieldeffect','waitstate','gotostd','callstd'):
   add(pc+1,sp=tuple(sorted(set((*specials,cmd+' '+','.join(a))))))
  else:add(pc+1)
 results.append(dict(kind=kind,map=mp,script=label,var=var,value=value,positions=positions,states=len(visited),ends=ends,unsafe_paths=bad,manual_paths=unknown))
(opts.rapport/'CHEMINS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
with (opts.rapport/'DECLENCHEURS.csv').open('w',newline='') as f:
 fields=['kind','map','script','var','value','positions','states','ends','unsafe_paths','manual_paths']
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
 for r in results:w.writerow({**r,'positions':json.dumps(r['positions']),'unsafe_paths':len(r['unsafe_paths']),'manual_paths':len(r['manual_paths'])})
summary=dict(coordinate_tiles=sum(r['kind']=='coordinate' for r in rows),frame_table_entries=sum(r['kind']=='frame' for r in rows),coordinate_scripts=len(set(r['script'] for r in rows if r['kind']=='coordinate')),frame_scripts=len(set(r['script'] for r in rows if r['kind']=='frame')),groups=len(results),flagged_groups=[dict(kind=x['kind'],map=x['map'],script=x['script']) for x in results if x['unsafe_paths']],native_review_groups=sum(bool(x['manual_paths']) for x in results),argenta_before=opts.avant_argenta,limitation='Conservative branches; numeric conditions, native specials, quest-log playback and inaccessible legacy rooms require contextual review. A lock command clears the pending step for coordinate scripts but is not sufficient for frame-table scenes.')
(opts.rapport/'INVENTAIRE.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))

#!/usr/bin/env python3
"""Independent scope checks against the pinned pre-scenario game, not a build substitute."""
import collections,hashlib,json,re,subprocess
from pathlib import Path
from cadrer_dialogues_fr import measure
R=Path(__file__).resolve().parents[2];BASE='6f143452a026a41c08f1db38f9809959809a31b6';Q=R/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO'
def old(p):return subprocess.check_output(['git','show',BASE+':'+str(p)],cwd=R)
def entries(t):return {m[1]:m[2] for m in re.finditer(r'^    \[(TRAINER_\w+)\] = \{(.*?)^    \},',t,re.M|re.S)}
base=json.loads((Q/'BASE_PROTEGEE.json').read_text());assert all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in base['files'].items())
a=entries(old('src/data/trainers.h').decode());b=entries((R/'src/data/trainers.h').read_text());rockets=[k for k,v in a.items() if 'TRAINER_CLASS_TEAM_ROCKET' in v];don=['TRAINER_BOSS_GIOVANNI','TRAINER_BOSS_GIOVANNI_2','TRAINER_LEADER_GIOVANNI'];assert len(rockets)==53
for k in a:
 if k not in rockets+don+['TRAINER_RS_BLACK_BELT','TRAINER_GUITARIST','TRAINER_KINDLER','TRAINER_RS_CAMPER']:assert a[k]==b[k],k
 else:
  strip=lambda t:re.sub(r'\.(?:trainerName|trainerPic) = [^\n]*','',t)
  assert strip(a[k])==strip(b[k]),(k,'behavior changed')
portraits=collections.Counter()
for k in rockets:
 pic=re.search(r'trainerPic = TRAINER_PIC_YOKAI_MAFIAMILLE([123])',b[k]);assert pic,k;portraits[pic[1]]+=1;assert '_("MAFIAMILLE")' in b[k]
for k in don:assert 'TRAINER_PIC_YOKAI_DONMORLEONE' in b[k]
parties=lambda t:{m[1]:m[2] for m in re.finditer(r'static const struct \w+ (\w+)\[\] = \{(.*?)\n\};',t,re.S)}
p1=parties(old('src/data/trainer_parties.h').decode());p2=parties((R/'src/data/trainer_parties.h').read_text());spec=json.loads((Q/'EQUIPES_APPROUVEES.json').read_text());allowed={r['party_symbol'] for r in spec['changed_teams']};assert len(allowed)==31
for k in p1:
 if k not in allowed:assert p1[k]==p2[k],k
 else:
  fields=lambda t:re.findall(r'\.iv = (\d+), \.lvl = (\d+).*?\.heldItem = (\w+)',t)
  assert fields(p1[k])==fields(p2[k]),(k,'IV/level/item/count changed')
assert len([r for r in spec['changed_teams'] if r['trainer'].startswith('TRAINER_TEAM_ROCKET_GRUNT')])==27
for f in (R/'data/maps').glob('*/scripts.inc'):assert f.read_bytes()==old(f.relative_to(R)),str(f)
actors=[]
for f in (R/'data/maps').glob('*/map.json'):
 before=json.loads(old(f.relative_to(R)));after=json.loads(f.read_text())
 for i,o in enumerate(before.get('object_events',[]),1):
  if o['graphics_id'] in ['OBJ_EVENT_GFX_ROCKET_M','OBJ_EVENT_GFX_ROCKET_F','OBJ_EVENT_GFX_GIOVANNI'] or o.get('local_id')=='LOCALID_ROUTE24_ROCKET':actors.append(dict(map=f.parent.name,index=i,graphics=o['graphics_id'],script=o.get('script'),x=o['x'],y=o['y']))
 if f.parent.name=='Route24':
  x=next(o for o in before['object_events'] if o.get('local_id')=='LOCALID_ROUTE24_ROCKET');x['graphics_id']='OBJ_EVENT_GFX_YOKAI_MAFIAMILLE1';assert before==after
 else:assert before==after,str(f)
assert len(actors)==69
# Controls must survive even when the music constant has ROCKET in its internal name.
from localiser_fr import controls
text_checks=[]
for row in json.loads((Q/'DIALOGUES.json').read_text()):
 assert controls(row['before'])==controls(row['after']),row['label']
 widths=[measure(x) for x in re.split(r'\\[nlp]',row['after'])];assert max(widths)<=208,(row['label'],widths)
 text_checks.append(dict(label=row['label'],maximum_pixels=max(widths)))
residual=[]
for f in list((R/'data/maps').glob('*/text.inc'))+[R/'data/text/fame_checker.inc']:
 for m in re.finditer(r'\.string "(.*)"',f.read_text()):
  visible=re.sub(r'\{[^}]*\}','',m[1])
  if re.search(r'rocket|giovanni',visible,re.I):residual.append((str(f.relative_to(R)),visible))
assert not residual,residual
# The protected audio branch has not advanced.
assert subprocess.check_output(['git','rev-parse','audio/integration-31-ost'],cwd=R,text=True).strip()=='837bd1757a7c2cdc2d476c3a5eacfd6296177c6a'
report=dict(passed=True,base=BASE,protected_files_byte_identical=len(base['files']),unchanged_map_programs=len(list((R/'data/maps').glob('*/scripts.inc'))),actors=actors,rocket_trainer_records=53,portrait_distribution=dict(portraits),changed_parties=31,all_other_parties_identical=True,all_other_trainers_identical=True,levels_counts_IV_items_AI_money_preserved=True,text_checks=text_checks,visible_Rocket_Giovanni_text_residuals=residual,audio_branch_unchanged=True,scope='Static source checks only; Casino R artwork intentionally remains pending approval')
(Q/'PRESERVATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PRESERVATION PASS',len(actors),'actors,',len(text_checks),'dialogues,',len(base['files']),'protected files')

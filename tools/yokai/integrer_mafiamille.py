#!/usr/bin/env python3
"""Apply only the creator-approved Mafia roster and appearances; preserve boss teams."""
import csv, io, json, re, subprocess
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE='6f143452a026a41c08f1db38f9809959809a31b6'
def original(path,commit=BASE):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
def edit(path,fn):
 p=ROOT/path;p.write_text(fn(p.read_text()))
proposals={4:['Raltesse','Bonneto'],6:['Couchtar','Chiperpiou'],7:['Bouh','Bonneto'],8:['Chiperpiou','Couchtar'],11:['Toumou','Loubarbare','Nihilistik','Bonneto'],13:['Raltesse','Bouh','Lulugubre','Chiperpiou','Bonneto'],14:['Couchtar','Nihilistik','Chiperpiou'],16:['Bandinyan','Lulugubre','Bouh'],19:['Crocho','Couchtar','Bouh'],21:['Toumou','Loubarbare','Nihilistik','Bonneto'],23:['Loubarbare','Émousstik'],24:['Loubarbare','Nihilistik','Toumou','Chiperpiou','Bonneto'],25:['Bouh','Rapiaf','Raltesse'],26:['Nihilistik',"Lamlam'mou"],32:['Couchtar','Nihilistik','Toumou','Chiperpiou'],34:['Bandinyan','Lulugubre'],35:['Nihilistik','Toumou','Loubarbare','Chiperpiou'],36:['Bonneto',"Lamlam'mou",'Loubarbare'],38:['Toumou','Loubarbare','Rapiaf'],40:['Raltesse','Bouh','Lulugubre','Couchtar','Bonneto'],42:['Raltesse','Crocho'],43:['Bandinyan','Racaïd'],44:['Nihilistik',"Lamlam'mou",'Loubarbare','Bonneto'],46:['Lulugubre','Rapiaf','Bouh'],47:["Lamlam'mou",'Loubarbare','Nihilistik'],49:['Noctambill','Raltesse','Bouh'],50:["Lamlam'mou",'Racaïd']}
changes={'TRAINER_TEAM_ROCKET_GRUNT'+('' if n==1 else '_'+str(n)):v for n,v in proposals.items()}
changes.update(TRAINER_TEAM_ROCKET_ADMIN=['Bonneto',"Lamlam'mou",'Émousstik'],TRAINER_TEAM_ROCKET_ADMIN_2=['Racaïd','Noctambill','Bandinyan'],TRAINER_KINDLER=['Bonneto','Rapiaf'],TRAINER_RS_CAMPER=['Couchtar','Noctambill','Émousstik'])
ns={r['nom_yokai']:r for r in json.loads((ROOT/'data/yokai/noms_affiches.json').read_text())}
learns=list(csv.DictReader((ROOT/'data/yokai/attaques_validees.csv').open(),delimiter=';'))
def moves_at(number,level):
 out=[]
 for row in learns:
  if int(row['numero_yokai'])!=number or row['apprentissage']=='EVOLUTION_PLUS_2' or int(row['niveau'])>level:continue
  if row['move_id'] not in out:out=(out+[row['move_id']])[-4:]
 assert out,(number,level)
 return out+['MOVE_NONE']*(4-len(out))
trainers=original('src/data/trainers.h').decode();parties=original('src/data/trainer_parties.h').decode();ability=original('src/data/yokai_trainer_abilities.h').decode();applied=json.loads(original('data/yokai/equipes_appliquees.json'));boss=json.loads(original('data/yokai/cameos_boss.json'));locked=json.loads(original('data/yokai/equipes_boss_validees.json'));species_info=(ROOT/'src/data/pokemon/species_info.h').read_text();proof=[]
entries={m[1]:m[2] for m in re.finditer(r'^    \[(TRAINER_\w+)\] = \{(.*?)^    \},',trainers,re.M|re.S)}
for key,new in changes.items():
 symbol=re.search(r'party = \w+\((\w+)\)',entries[key])[1];pat=r'(\b'+symbol+r'\[\] = \{)(.*?)(\n\};)';m=re.search(pat,parties,re.S);members=[line for line in m[2].splitlines() if '.species' in line];assert len(members)==len(new);updated=[];team=[]
 for member,name in zip(members,new):
  r=ns[name];level=int(re.search(r'\.lvl = (\d+)',member)[1]);moves=moves_at(int(r['numero_yokai']),level)
  team.append(dict(species=r['species_constant'],level=level,moves=moves,ability_num=0,held_item=re.search(r'\.heldItem = (\w+)',member)[1],iv=int(re.search(r'\.iv = (\d+)',member)[1])))
 # Trainer rows have a nested moves initializer; use line-by-line to preserve other fields exactly.
 lines=[line for line in m[2].splitlines() if '.species' in line];assert len(lines)==len(new)
 for line,mon in zip(lines,team):
  line=re.sub(r'\.species = \w+','.species = '+mon['species'],line);line=re.sub(r'\.moves = \{[^}]+\}',lambda _:'.moves = {'+', '.join(mon['moves'])+'}',line);updated.append(line)
 parties=parties[:m.start(2)]+'\n'+'\n'.join(updated)+parties[m.end(2):]
 ability=re.sub(r'(\['+key+r'\] = )\{[^}]*\}',lambda m:m[1]+'{'+', '.join('0' for _ in team)+'}',ability)
 if key in locked:
  for mon in team:
   info=re.search(r'\['+mon['species']+r'\]\s*=\s*\{(.*?)\n    \}',species_info,re.S)[1]
   mon['ability']=re.search(r'\.abilities\s*=\s*\{(ABILITY_\w+)',info)[1]
  locked[key]['party']=team
  locked[key]['source_heading']='Mafiamille: composition explicitly approved after audit'
 if key in applied:applied[key]['party']=team
 else:
  for t in boss['teams']:
   if t['trainer_entry'] in {'TRAINER_YOKAI_MAFIAMILLE2' if key=='TRAINER_KINDLER' else 'TRAINER_YOKAI_MAFIAMILLE3'}:
    for mon,old in zip(team,t['members']):old.update(number=int(next(r['numero_yokai'] for r in ns.values() if r['species_constant']==mon['species'])),species=mon['species'],moves=mon['moves'])
 proof.append(dict(trainer=key,party_symbol=symbol,team=team))
def identity(m):
 key,body=m[1],m[2]
 if 'TRAINER_CLASS_TEAM_ROCKET' in body:
  match=re.search(r'GRUNT(?:_(\d+))?$',key);n=int(match[1] or 1) if match else (1 if key.endswith('ADMIN') else 2)
  body=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_YOKAI_MAFIAMILLE'+str((n-1)%3+1),body)
  body=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("MAFIAMILLE")',body)
 elif key in ['TRAINER_BOSS_GIOVANNI','TRAINER_BOSS_GIOVANNI_2','TRAINER_LEADER_GIOVANNI']:
  body=body.replace('TRAINER_PIC_LEADER_GIOVANNI','TRAINER_PIC_YOKAI_DONMORLEONE').replace('_("GIOVANNI")','_("D. Morléone")')
 elif key=='TRAINER_RS_BLACK_BELT':body=body.replace('Don Morleo.','D. Morléone')
 return '    ['+key+'] = {'+body+'    },'
trainers=re.sub(r'^    \[(TRAINER_\w+)\] = \{(.*?)^    \},',identity,trainers,flags=re.M|re.S)
for path,value in [('src/data/trainers.h',trainers),('src/data/trainer_parties.h',parties),('src/data/yokai_trainer_abilities.h',ability)]: (ROOT/path).write_text(value)
(ROOT/'data/yokai/equipes_appliquees.json').write_text(json.dumps(applied,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/yokai/equipes_boss_validees.json').write_text(json.dumps(locked,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/yokai/cameos_boss.json').write_text(json.dumps(boss,ensure_ascii=False,indent=2)+'\n')
edit('src/data/text/trainer_class_names.h',lambda t:t.replace('[TRAINER_CLASS_TEAM_ROCKET]         = _("TEAM ROCKET")','[TRAINER_CLASS_TEAM_ROCKET]         = _("SBIRE")'))
# Preserve legacy IDs for cached actors and journal replay, resolving to the same new graphics.
edit('src/data/object_events/object_event_graphics_info_pointers.h',lambda t:t.replace('= &gObjectEventGraphicsInfo_RocketM,','= &gObjectEventGraphicsInfo_YokaiMafiamille1,').replace('= &gObjectEventGraphicsInfo_RocketF,','= &gObjectEventGraphicsInfo_YokaiMafiamille1,').replace('= &gObjectEventGraphicsInfo_Giovanni,','= &gObjectEventGraphicsInfo_YokaiDonMorleone,'))
p=ROOT/'data/maps/Route24/map.json';data=json.loads(p.read_text());actor=next(o for o in data['object_events'] if o.get('local_id')=='LOCALID_ROUTE24_ROCKET');actor['graphics_id']='OBJ_EVENT_GFX_YOKAI_MAFIAMILLE1';p.write_text(json.dumps(data,indent=2)+'\n')
edit('src/fame_checker.c',lambda t:t.replace('[FAMECHECKER_GIOVANNI] = TRAINER_PIC_LEADER_GIOVANNI','[FAMECHECKER_GIOVANNI] = TRAINER_PIC_YOKAI_DONMORLEONE'))
# Copy two authorized sheets and provenance only, never scene/script changes from the later commit.
for name in ['don_morleone','mafiamille_1']:
 path=f'graphics/yokai_characters/{name}/overworld.png';raw=original(path,'740c257b2');im=Image.open(io.BytesIO(raw));old=Image.open(io.BytesIO(original(path)));assert im.crop((0,0,48,32)).tobytes()==old.tobytes();(ROOT/path).write_bytes(raw)
 meta=json.loads(original(f'graphics/yokai_characters/{name}/walk-production.json','740c257b2'));meta['artistic_validation']='Pending creator approval on feature/mafiamille-kanto';meta['selective_source_commit']='740c257b2';(ROOT/f'graphics/yokai_characters/{name}/walk-production.json').write_text(json.dumps(meta,indent=2)+'\n')
 # Only the two selected actors use standard 9-frame animation; other cameo actors stay unchanged.
 symbol='YokaiDonMorleone' if name=='don_morleone' else 'YokaiMafiamille1'
 def pic(t):return re.sub(r'(static const struct SpriteFrameImage sPicTable_'+symbol+r'\[\] = \{).*?(\n\};)',lambda m:m[1]+'\n'+'\n'.join(f'    overworld_frame(gObjectEventPic_{symbol}, 2, 4, {n}),' for n in range(9))+m[2],t,flags=re.S)
 edit('src/data/object_events/object_event_pic_tables.h',pic)
 def info(t):return re.sub(r'(const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_'+symbol+r' = \{).*?(\n\};)',lambda m:m[0].replace('sAnimTable_Ariane','sAnimTable_Standard'),t,flags=re.S)
 edit('src/data/object_events/object_event_graphics_info.h',info)
# Three shared classic actor IDs must use the same complete animation.
edit('src/data/object_events/object_event_graphics_info_pointers.h',lambda t:t.replace('= &gObjectEventGraphicsInfo_YokaiMafiamille2,','= &gObjectEventGraphicsInfo_YokaiMafiamille1,').replace('= &gObjectEventGraphicsInfo_YokaiMafiamille3,','= &gObjectEventGraphicsInfo_YokaiMafiamille1,'))
p=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/EQUIPES_APPROUVEES.json';p.write_text(json.dumps(dict(base=BASE,changed_teams=proof,preserved_three_main_Don_teams=True,preserved_postgame_Don_team=True),ensure_ascii=False,indent=2)+'\n')
print('Applied',len(proof),'approved parties and shared walking identities')

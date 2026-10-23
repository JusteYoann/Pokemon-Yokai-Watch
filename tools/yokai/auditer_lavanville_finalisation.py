#!/usr/bin/env python3
"""Static preservation, actual parties and exhaustive occupied-tile accessibility.
This does not replace native encounter, movement, battle or save tests.
"""
from pathlib import Path
import hashlib,json,re,subprocess,struct,itertools,collections
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'docs/lavanville-zombie-night/finalisation';P.mkdir(parents=True,exist_ok=True);BASE='7110ce41b'
def original(file):return subprocess.check_output(['git','show',BASE+':'+str(file)],cwd=ROOT)
def read(file):return (ROOT/file).read_text()
def sha(b):return hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='feature/lavanville-zombie-night'
protected={'audio/integration-31-ost':'837bd1757a7c2cdc2d476c3a5eacfd6296177c6a','feature/mafiamille-kanto':'1bf5774d8e5c0c832e1a377a85afb5ad93b7fc55','feature/boss-final-don-spiraton':'49535014b9c5fd6add06464fb32f9ea85ca69078'}
for branch,commit in protected.items():assert subprocess.check_output(['git','rev-parse',branch],cwd=ROOT,text=True).strip()==commit
preserved={}
for file in ['src/data/pokemon/species_info.h','src/data/pokemon/level_up_learnsets.h','src/data/pokemon/level_up_learnset_pointers.h','src/data/pokemon/evolution.h','src/data/text/species_names.h','src/data/wild_encounters.json','sound/song_table.inc']:
 assert (ROOT/file).read_bytes()==original(file),file;preserved[file]=sha(original(file))
assets=[]
for p in list((ROOT/'graphics/yokai_zombies').rglob('*.png'))+list((ROOT/'graphics/yokai_characters/alyzon').glob('*.png')):
 file=p.relative_to(ROOT);b=p.read_bytes();assert b==original(file);assets.append(dict(file=str(file),sha256=sha(b)))
# New audio metadata only changes track14, not any of the other30 records/slots.
new=json.loads(read('data/yokai/audio_loops.json'));old=json.loads(original('data/yokai/audio_loops.json'));assert new['tracks']==old['tracks'];assert new['active_tracks']==old['active_tracks']
assert [r for r in new['gap_tracks'] if r['number']!=14]==[r for r in old['gap_tracks'] if r['number']!=14]
# All existing badge/quest flags keep their values, IDs and save structure.
for file in ['include/constants/flags.h','include/constants/vars.h']:
 old_defs=dict(re.findall(r'^#define\s+(\w+)\s+([^\n]+)',original(file).decode(),re.M));new_defs=dict(re.findall(r'^#define\s+(\w+)\s+([^\n]+)',read(file),re.M))
 for key,val in old_defs.items():assert new_defs[key]==val,(key,val,new_defs.get(key))
# Real teams and source stats. Legal moves are read through active learnset pointers.
parties=read('src/data/trainer_parties.h');oldparties=original('src/data/trainer_parties.h').decode();stats=read('src/data/pokemon/species_info.h');learn=read('src/data/pokemon/level_up_learnsets.h');pointers=read('src/data/pokemon/level_up_learnset_pointers.h')
names=dict(re.findall(r'\[SPECIES_(\w+)\]\s*= _\("([^"]+)"\)',read('src/data/text/species_names.h')));move_names=dict(re.findall(r'\[(MOVE_\w+)\]\s*= _\("([^"]+)"\)',read('src/data/text/move_names.h')))
ids={k:int(v) for k,v in re.findall(r'^#define SPECIES_(\w+)\s+(\d+)\b',read('include/constants/species.h'),re.M)}
def body(name,src=parties):return re.search(r'static const struct TrainerMonItemCustomMoves '+name+r'\[\] = \{(.*?)\n?\};',src,re.S)[1]
def team(name,check_legal=False):
 result=[]
 for lv,sp,moves in re.findall(r'\.lvl = (\d+), .species = SPECIES_(\w+), .heldItem = ITEM_NONE, .moves = \{([^}]+)\}',body(name)):
  st=re.search(r'\[SPECIES_'+sp+r'\] =\s*\{(.*?)\n    \}',stats,re.S)[1];base={k:int(v) for k,v in re.findall(r'\.(base\w+) = (\d+)',st)};types=re.search(r'\.types = \{([^}]+)\}',st)[1].split(', ');ms=moves.split(', ')
  if check_legal:
   ptr=re.search(r'\[SPECIES_'+sp+r'\] = (\w+)',pointers)[1];ls=re.search(r'static const u16 '+ptr+r'\[\] = \{(.*?)\n\};',learn,re.S)[1];legal={m for level,m in re.findall(r'LEVEL_UP_MOVE\((\d+), (MOVE_\w+)\)',ls) if int(level)<=int(lv)};assert set(ms)<=legal,(name,sp,ms,legal)
  result.append(dict(name=names[sp],species=ids[sp],constant='SPECIES_'+sp,level=int(lv),types=types,base_stats=base,moves=[dict(constant=m,name=move_names[m]) for m in ms]))
 return result
teams={}
for name in re.findall(r'sYokaiParty_CHANNELER_\w+',parties):
 # Only the13 actual Tower trainer records.
 if name.rsplit('_',1)[1] in ['PATRICIA','CARLY','HOPE','PAULA','LAUREL','JODY','TAMMY','RUTH','KARINA','JANAE','ANGELICA','EMILIA','JENNIFER']:
  assert body(name)==body(name,oldparties);teams[name]=team(name)
for i in range(1,4):teams[f'sLavenderSummit{i}']=team(f'sLavenderSummit{i}',True)
leader=team('sYokaiParty_LEADER_ERIKA',True);assert [(m['species'],m['level']) for m in leader]==[(32,27),(8,28),(44,29),(125,31)];assert all(m['types']==['TYPE_GHOST','TYPE_GHOST'] for m in leader)
# Exhaustive possible occupied tiles. This checks walkable exits, not sight-cone timing.
b=struct.unpack('<480H',(ROOT/'data/layouts/LavenderTown/map.bin').read_bytes());free={(x,y) for y in range(20) for x in range(24) if not ((b[y*24+x]>>10)&3)}
paths=[[(5,7),(6,7),(7,7),(7,8),(6,8),(5,8)],[(x,12) for x in range(12,17)],[(17,8)],[(x,y) for x in range(12,17) for y in range(16,19) if (x,y) in free]]
portals=[(11,0),(0,9),(11,19),(6,6),(18,7),(10,12),(5,17),(10,17),(20,16)];assert set(portals)<=free
count=0
for actors in itertools.product(*paths):
 count+=1;blocked=set(actors);assert not blocked&set(portals);queue=collections.deque([portals[0]]);seen={portals[0]}
 while queue:
  x,y=queue.popleft()
  for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if p in free and p not in blocked and p not in seen:seen.add(p);queue.append(p)
 assert set(portals)<=seen,actors
report=dict(passed=True,base=BASE,protected_branches=protected,preserved_sources=preserved,artwork_byte_identical=assets,unchanged_existing_tower_teams=len(teams)-3,tower_teams=teams,alyzon=leader,patrol_paths=paths,patrol_occupied_tile_combinations=count,doors_never_occupied=True,all_entry_and_exit_tiles_connected=True,scope=__doc__)
(P/'AUDIT_STATIQUE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS preservation, official team legality,16 Tower teams,',count,'occupied-tile combinations')

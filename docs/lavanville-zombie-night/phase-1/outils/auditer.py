#!/usr/bin/env python3
"""Read-only game audit; writes derived phase-1 documentation only."""
from pathlib import Path
import re,json,hashlib,csv,subprocess
R=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parents[1]
def save(n,x): (D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
mapnames=sorted(p.name for p in (R/'data/maps').iterdir() if p.name.startswith(('LavenderTown','PokemonTower_')))+['CeladonCity_Gym','CeladonCity_GameCorner','RocketHideout_B1F','RocketHideout_B2F','RocketHideout_B3F','RocketHideout_B4F','SaffronCity','Route12','Route16']
maps=[];placements=[]
for name in mapnames:
 p=R/'data/maps'/name; m=json.loads((p/'map.json').read_text());s=(p/'scripts.inc').read_text() if (p/'scripts.inc').exists() else ''
 maps.append(dict(map=name,source=f'data/maps/{name}/map.json',music=m['music'],weather=m['weather'],connections=m.get('connections'),objects=m['object_events'],warps=m['warp_events'],coord_events=m.get('coord_events',[]),bg_events=m.get('bg_events',[])))
 for match in re.finditer(r'trainerbattle_(single|no_intro)\s+(TRAINER_\w+)',s):
  placements.append(dict(map=name,trainer=match[2],line=s[:match.start()].count('\n')+1,mode=match[1]))
save('inventaire-cartes.json',maps);save('combats-existants.json',placements)
patterns=[r'FUJI|Fuji|fuji',r'SILPH_SCOPE|SilphScope|SilphScope',r'GOT_POKE_FLUTE|ITEM_POKE_FLUTE|AwakenSnorlax',r'FLAG_DEFEATED_ERIKA|FLAG_BADGE04_GET',r'MUS_YOKAI_(ZOMBIE_NIGHT|MYSTIC_GROVE|INFINITE_TUNNEL)']
refs={}
for pat in patterns:
 result=subprocess.run(['rg','-n',pat,'data','src','include'],cwd=R,capture_output=True,text=True)
 refs[pat]=result.stdout.splitlines()
save('dependances-code.json',refs)
names=json.loads((R/'data/yokai/noms_affiches.json').read_text());N={int(e['species_id']):e for e in names};stats=(R/'src/data/pokemon/species_info.h').read_text();levels=(R/'src/data/pokemon/level_up_learnsets.h').read_text();pointers=(R/'src/data/pokemon/level_up_learnset_pointers.h').read_text()
move_names={r['move_id']:r['libelle_source'] for r in csv.DictReader((R/'data/yokai/attaques_validees.csv').open(),delimiter=';')}
def mon(n,lv):
 e=N[n];s=e['species_constant'];b=re.search(r'\['+s+r'\]\s*=\s*\{(.*?)\n    \}',stats,re.S)[1];types=re.search(r'\.types = \{([^}]+)',b)[1].replace('TYPE_','').split(', ')
 ptr=re.search(r'\['+s+r'\]\s*=\s*(\w+)',pointers)[1];body=re.search(r'static const u16 '+ptr+r'\[\] = \{(.*?)\};',levels,re.S)[1]
 moves=[]
 for level,m in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*(MOVE_\w+)\)',body):
  if int(level)<=lv and m not in moves:moves.append(m)
 return dict(species_id=n,species=s,name=e['nom_yokai'],level=lv,types=types,moves=moves[-4:],move_labels=[move_names.get(m,m) for m in moves[-4:]],source_learnset=ptr)
teams={'Zombigo T':[(41,22),(57,23)],'Clochemar':[(39,24),(99,25)],'Supermanager':[(49,24),(121,25),(32,25)],'Zomgralos':[(40,26),(59,27)],'King Deadward':[(70,27),(115,28),(43,28)],'Encore Dead':[(32,28),(41,28),(124,29)],'Alyzon A — spectres accessibles':[(41,25),(32,26),(49,27),(115,28)],'Alyzon B — variété de la nuit':[(43,25),(45,26),(57,27),(124,28)]}
save('equipes-proposees.json',{k:[mon(n,lv) for n,lv in team] for k,team in teams.items()})
# Source identities only, no redistribution licence inferred from the supplied ZIP.
a=Path('/workspace/artifacts/lavanville-phase1');ref=[]
for p in sorted((a/'references').glob('*')):ref.append(dict(file=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),provenance='Official artwork supplied by user in References_Lavanville_Zombie_Night.zip; redistribution licence not provided. Original retained locally, not published.'))
save('references-manifeste.json',ref)
protected=['src','include','data','graphics','sound','asm']
h=hashlib.sha256()
files=subprocess.check_output(['git','ls-tree','-r','HEAD',*protected],cwd=R)
h.update(files)
save('preservation-phase1.json',dict(base='49535014b9c5fd6add06464fb32f9ea85ca69078',branch=subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip(),source_tree_sha256=h.hexdigest(),method='git ls-tree -r HEAD src include data graphics sound asm; verify no diff under these paths',modified_game_files=subprocess.check_output(['git','diff','--name-only','49535014b9','--',*protected],cwd=R,text=True).splitlines(),no_new_rom_built=True))
print('Maps:',len(maps),'tower trainer placements:',sum(x['map'].startswith('PokemonTower') and x['mode']=='single' for x in placements))

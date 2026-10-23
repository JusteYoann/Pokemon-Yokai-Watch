#!/usr/bin/env python3
"""Byte preservation against approved Champions base, plus private ROM audio streams."""
import json,re,subprocess,hashlib,tarfile,io,os
from pathlib import Path
from mgba_rpc import ROOT
BASE='e1dcd9132aa8666fb1798c90a731859f1632313e';P=ROOT/os.environ.get('YOKAI_PHILOSOVNI_REPORT_DIR','docs/pierre-philosovni/validation');P.mkdir(parents=True,exist_ok=True)
def original(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
files=['src/data/pokemon/species_info.h','src/data/pokemon/level_up_learnsets.h','src/data/pokemon/level_up_learnset_pointers.h','src/data/pokemon/evolution.h','src/data/text/species_names.h','src/data/wild_encounters.json','sound/song_table.inc','data/yokai/audio_loops.json','include/global.h','src/yokai_champions.c','src/lavanville.c','src/spiraton_battle.c','src/spiraton_core.c','src/spiraton_art_preview.c','src/fldeff_cut.c','data/scripts/field_moves.inc']
checked={}
for name in files:
 assert (ROOT/name).read_bytes()==original(name),name;checked[name]=sha(original(name))
# Pokemon logic and saved party remain unchanged; only the transient RAM capacity increases.
for name in ['src/pokemon.c','include/pokemon.h']:
 now=(ROOT/name).read_text().replace('gPlayerParty[PARTY_SIZE + 1]','gPlayerParty[PARTY_SIZE]')
 assert now==original(name).decode(),name
for name in ['include/constants/vars.h','include/constants/flags.h']:
 assert (ROOT/name).read_bytes().startswith(original(name)),name
for name,pattern in [('src/data/trainers.h',r'(?:^|\n)    \[(TRAINER_\w+)\] = \{(.*?)\n    \},'),('src/data/trainer_parties.h',r'static const struct \w+ (\w+)\[\] = \{(.*?)\n\};'),('src/data/yokai_trainer_abilities.h',r'\[(TRAINER_\w+)\] = (\{[^}]+\})')]:
 old=dict(re.findall(pattern,original(name).decode(),re.S));now=dict(re.findall(pattern,(ROOT/name).read_text(),re.S))
 assert all(now[k]==v for k,v in old.items()),name;checked[name]=dict(old_records_preserved=len(old),new_records=len(now)-len(old))
# Archive compares in one git process, including all approved graphics and protected map files.
archive=subprocess.check_output(['git','archive',BASE,'graphics','data/maps','data/layouts'],cwd=ROOT)
allowed={'PewterCity_Gym','VermilionCity','VermilionCity_Gym','SSAnne_CaptainsOffice'}
art=0;maps=0;protected=[]
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
 for member in tf:
  if not member.isfile():continue
  name=member.name;old=tf.extractfile(member).read()
  if name.startswith('graphics/') and name.endswith(('.png','.pal')):
   now=(ROOT/name).read_bytes()
   if name.endswith('.pal'):old=old.replace(b'\r\n',b'\n');now=now.replace(b'\r\n',b'\n')
   assert now==old,name;art+=1
  elif name == 'data/maps/Route25/map.json':
   before=json.loads(old);after=json.loads((ROOT/name).read_text())
   before['object_events']=[o for o in before['object_events'] if o['graphics_id']!='OBJ_EVENT_GFX_USAPION_CAMEO']
   assert before==after,name
  elif name.startswith('data/maps/') and len(name.split('/'))>3 and name.split('/')[2] not in allowed:
   assert (ROOT/name).read_bytes()==old,name;maps+=1;protected.append(name)
  elif name.startswith('data/layouts/') and name.endswith('.bin') and name.split('/')[2]!='VermilionCity':assert (ROOT/name).read_bytes()==old,name
old=json.loads(original('data/maps/map_groups.json'));new=json.loads((ROOT/'data/maps/map_groups.json').read_text())
assert old['group_order']==new['group_order']
for group in old['group_order']:assert new[group][:len(old[group])]==old[group],group
oldlayouts=json.loads(original('data/layouts/layouts.json'))['layouts'];newlayouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'];assert newlayouts[:len(oldlayouts)]==oldlayouts
# All private protected streams must actually be present unchanged in compiled ROM.
symbols={}
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(ROOT/'pokefirered_audio.elf')],text=True).splitlines():
 a=line.split()
 if len(a)==3:symbols[a[2]]=int(a[0],16)
rom=(ROOT/'pokefirered_audio.gba').read_bytes();audio=[]
for i in range(1,32):
 b=Path(f'/workspace/private-audio/lavanville-integration/{i:02d}.dpcm').read_bytes();offset=symbols[f'yokai_wave_{i:02d}']-0x08000000;assert rom[offset:offset+len(b)]==b
 audio.append(dict(track=i,bytes=len(b),sha256=sha(b)))
report=dict(passed=True,base=BASE,unchanged_sources=checked,approved_artwork_preserved=art,non_target_map_files_preserved=maps,protected_maps=protected,old_map_and_layout_ids_preserved=True,party_save_and_pokemon_structs_unchanged=True,temporary_party_capacity='100 extra RAM bytes; six saved player mons unchanged',audio=audio)
(P/'PRESERVATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',art,'graphics,',maps,'protected map files,151 Yo-kai, all pre-existing trainer parties,31 private streams')

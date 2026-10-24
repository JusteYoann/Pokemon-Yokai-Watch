#!/usr/bin/env python3
"""Structural checks for the complete French pass; named UI/grammar exceptions."""
import collections,hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];BASE='716712b08'
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R,text=True)
files=subprocess.check_output(['git','diff','--name-only',BASE],cwd=R,text=True).splitlines()
protected=('sound/','graphics/','include/constants/','include/global','src/data/trainers.h','src/data/trainer_parties.h','src/data/pokemon/species_info.h','src/data/pokemon/level_up_learnsets.h','src/data/pokemon/evolution.h','data/wild_encounters','data/maps/map_groups.json')
assert not [p for p in files if p.startswith(protected)],'Protected game/audio/save data changed'
checked=[]
for p in files:
 if p.startswith('data/') and p.endswith(('.inc','.s')):
  if p=='data/maps/PewterCity/morleone.inc':
   reference=Path('/workspace/Pokemon-Yokai-Watch-argenta-retour')/p
   assert reference.read_bytes()==(R/p).read_bytes(),'Argenta fix drift';continue
  strip=lambda s:re.sub(r'\s+','',re.sub(r'(?m)^[ \t]*\.(?:string|braille).*\n','',s))
  assert strip(old(p))==strip((R/p).read_text()),('Script structure changed',p);checked.append(p)
# Region IDs, coordinates, name keys and aliases stay byte-for-byte equivalent.
p='src/data/region_map/region_map_sections.json';a=json.loads(old(p));b=json.loads((R/p).read_text())
for x in a['map_sections']:x.pop('display_name',None)
for x in b['map_sections']:x.pop('display_name',None)
assert a==b,'Region map structure changed'
# Item IDs, effects, prices, pockets, and all other gameplay fields unchanged.
p='src/data/items.json';a=json.loads(old(p));b=json.loads((R/p).read_text())
for d in (a,b):
 for x in d['items']:
  for k in list(x):
   if k=='english' or k.startswith('description_'):x.pop(k)
assert a==b,'Item behavior changed'
# First151 active names and all saved vocabulary IDs/unlock flags retained.
p='src/data/text/species_names.h'
def first151(s):return re.findall(r'\[SPECIES_\w+\]\s*= _\("[^"]*"\)',s)[:152]
assert first151(old(p))==first151((R/p).read_text())
for path in (R/'src/data/easy_chat').glob('easy_chat_group_*.h'):
 p=str(path.relative_to(R));before=old(p);after=path.read_text()
 assert re.findall(r'\.(?:text|enabled)\s*=\s*[^,]+',before)==re.findall(r'\.(?:text|enabled)\s*=\s*[^,]+',after),p
 ids=lambda s:collections.Counter(re.findall(r'\b(?:SPECIES|MOVE)_\w+\b',s))
 assert ids(before)==ids(after),p
p='src/data/easy_chat/easy_chat_words_by_letter.h'
ids=lambda s:collections.Counter(re.findall(r'EC_WORD_\w+|EC_(?:POKEMON2?|MOVE2?)\(\w+\)',s))
assert ids(old(p))==ids((R/p).read_text())
# Default Tower opponents: only displayed nicknames changed.
p='src/trainer_tower_sets.c';strip=lambda s:re.sub(r'\s+','',re.sub(r'"(?:\\.|[^"\\])*"','""',s))
assert strip(old(p))==strip((R/p).read_text())
rom=R/'pokefirered_audio.gba';assert rom.stat().st_size<=32*1024**2
out=dict(passed=True,baseline=BASE,rom_bytes=rom.stat().st_size,sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),script_files_literals_only=checked,argenta_fix_matches_tested_branch=True,audio_and_graphics_sources_unchanged=True,region_ids_coordinates_aliases_unchanged=True,item_mechanics_unchanged=True,active151_species_names_unchanged=True,vocabulary_saved_ids_and_unlock_flags_unchanged=True,tower_parties_only_nicknames_changed=True,reviewed_localization_code=['French berry plural helper and its two callers','Native status tile labels in party, summary and battle','French heading overlay on front/back Trainer Card','Native compact labels in summary, shared types/move badges and PV bars'],scope='Structural preservation checks plus explicitly reviewed UI/grammar changes; not a complete playthrough.')
(R/'docs/traduction-complete-20261024/PRESERVATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',len(checked),rom.stat().st_size)

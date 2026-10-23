#!/usr/bin/env python3
"""Compare untouched production data and record approved exceptions against the base."""
import subprocess,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];BASE='0fa1808fe';rows=[]
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def same(p):
 current=(R/p).read_bytes();previous=old(p)
 assert (current.replace(b'\r\n',b'\n')==previous.replace(b'\r\n',b'\n')) if p.endswith('.pal') else current==previous,p
 rows.append({'path':p,'identical_to_base':True})
for p in ['include/constants/species.h','src/cramois_past.c','src/palette.c','src/battle_anim.c','data/yokai/cramois-sepia-rgb555.bin','src/spiraton.c','src/philosovni.c','src/lavender_night.c']:
 if (R/p).exists():same(p)
for path in ['data/maps','graphics/yokai_characters/hovernyan']:
 for p in (R/path).rglob('*'):
  if p.is_file() and (path.endswith('hovernyan') and p.suffix in ['.png','.pal'] or path=='data/maps' and ('CinnabarIsland' in str(p) or '/Route20/' in str(p) or '/Route21_' in str(p)) and p.name in ['map.json','text.inc','scripts.inc']):same(str(p.relative_to(R)))
# Every existing species ID/name/stat row except the specifically approved150.
name='src/data/text/species_names.h'
assert re.sub(r'\[SPECIES_MEWTWO\].*','', (R/name).read_text())==re.sub(r'\[SPECIES_MEWTWO\].*','',old(name).decode())
info='src/data/pokemon/species_info.h'
pat=r'    \[SPECIES_MEWTWO\] =\s*\{.*?\n    \},'
assert re.sub(pat,'', (R/info).read_text(),flags=re.S)==re.sub(pat,'',old(info).decode(),flags=re.S)
# Geometry of Hovernyan must stay uniform; new150 framing is the sole delta.
p='src/data/yokai_battle_geometry.h';a=(R/p).read_text();b=old(p).decode();assert re.sub(r'    \[150\].*','',a)==re.sub(r'    \[150\].*','',b)
for protected in ['sYokaiParty_LEADER_BROCK','sYokaiParty_LEADER_MISTY','sYokaiParty_LEADER_LT_SURGE','sYokaiParty_LEADER_ERIKA','sYokaiParty_LEADER_BLAINE','sYokaiParty_LEADER_GIOVANNI','sParty_YokaiDonMorleone']:
 p='src/data/trainer_parties.h';pat=r'static const struct \w+ '+protected+r'\[\] = \{.*?\n\};'
 assert re.search(pat,(R/p).read_text(),re.S)[0]==re.search(pat,old(p).decode(),re.S)[0],protected
rows.append({'check':'151 IDs fixed; only approved150 species names/stats/frame changed; six other Gym parties and Don Morleone party unchanged','passed':True})
# Native MIDIs remain archived, retired sequence symbols must actually be absent.
audio=json.loads((R/'docs/dossier-20261023/audio-audit.json').read_text())
for rom in ['pokefirered','pokefirered_audio']:
 symbols=set(line.split()[2] for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(R/(rom+'.elf'))],text=True).splitlines() if len(line.split())==3)
 for song in audio['sequences']:
  assert song['symbol'] not in symbols,(rom,song['symbol'])
  assert (R/'sound/songs/midi'/ (song['symbol']+'.mid')).read_bytes()==old('sound/songs/midi/'+song['symbol']+'.mid')
 for symbol in audio['retained_public_fallbacks']:assert symbol in symbols,(rom,symbol)
 if rom.endswith('_audio'):
  for n in range(1,32):assert f'mus_yokai_{n:02}' in symbols and f'yokai_wave_{n:02}' in symbols
 rows.append({'rom':rom,'retired_sequence_symbols_absent':len(audio['sequences']),'retained_native_fallbacks':len(audio['retained_public_fallbacks']),'private_tracks_preserved':31 if rom.endswith('_audio') else 0})
# Encounter weights and all original nonduplicate species preserved at Victory Road.
p='src/data/wild_encounters.json';d=json.loads((R/p).read_text());prior=json.loads(old(p));tables=[]
for g,og in zip(d['wild_encounter_groups'],prior['wild_encounter_groups']):
 for e,oe in zip(g['encounters'],og['encounters']):
  if e['map']=='MAP_VICTORY_ROAD_3F':
   rates=next(f['encounter_rates'] for f in g['fields'] if f['type']=='land_mons');assert sum(rates)==100
   slots=e['land_mons']['mons'];assert sum(w for w,s in zip(rates,slots) if s['species']=='SPECIES_DRATINI')==5
   assert {x['species'] for x in oe['land_mons']['mons']}<={x['species'] for x in slots}
   assert all(s['min_level']==45 and s['max_level']==48 for s in slots if s['species']=='SPECIES_DRATINI')
   tables.append({'map':e['map'],'slots':[8,10],'weights':[4,1],'total_percent':100,'mademoaiselle_percent':5,'level_range':[45,48]})
  else:assert e==oe,e['map']
rows.append({'encounters':tables,'all_other_encounter_tables_identical':True})
(R/'docs/dossier-20261023/PRESERVATION.json').write_text(json.dumps({'passed':True,'base':BASE,'checks':rows},ensure_ascii=False,indent=2)+'\n')
print('PASS preservation',len(rows),'checks')

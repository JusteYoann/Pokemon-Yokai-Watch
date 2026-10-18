#!/usr/bin/env python3
"""Conservative linked-resource inventory: candidates are not proof of dead data."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'QA_RECETTE_FINALE/POST_B13/audio'
rom=ROOT/'pokefirered_audio.gba';public=ROOT/'pokefirered.gba'
constants={int(v,0):k for k,v in re.findall(r'^#define\s+(MUS_\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',(ROOT/'include/constants/songs.h').read_text(),re.M)}
refs=set()
for folder in ['src','data']:
 for p in (ROOT/folder).rglob('*'):
  if p.suffix not in ['.c','.h','.s','.inc','.json'] or p.name in ['yokai_mixer_gains.h']:continue
  # Generated native map headers duplicate map.json; count explicit token presence only.
  refs.update(re.findall(r'\bMUS_\w+\b',p.read_text(errors='replace')))
entries=re.findall(r'^\s*song\s+(\w+),', (ROOT/'sound/song_table.inc').read_text(),re.M)
candidates=[{'id':i,'constant':name,'table_header':entries[i],'status':'No explicit source token outside constants/table/calibration; dynamic use still possible, NOT proven removable'} for i,name in sorted(constants.items()) if 250<i<347 and name not in refs]
header=(ROOT/'src/data/graphics/pokemon.h').read_text();paths=re.findall(r'INCBIN_\w+\("([^"]+)"\)',header)
old=[p for p in paths if p.startswith('graphics/pokemon/')];custom=[p for p in paths if p.startswith('graphics/yokai/')]
report={'private_rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'private_rom_bytes':rom.stat().st_size,'b13_bytes':24400776,'increase_from_b13_bytes':rom.stat().st_size-24400776,'remaining_bytes_to32MiB':33554432-rom.stat().st_size,'public_build_bytes_including_minimum_padding':public.stat().st_size,'song_table_entries_all_retained':len(entries),'native_header_entries_all_retained':347,'explicit_token_absence_candidates':candidates,'pokemon_graphic_header_incbins':len(old),'yokai_graphic_header_incbins':len(custom),'original_graphics_note':'151 custom front/back/icon pointers are verified separately in verifier_rom. Other species/footprints/engine assets remain intentionally present; source directories alone are not duplicate ROM allocations. No deletion inferred from filenames.','removed_resources':[],'measured_reclamation_bytes':0,'scope':'No speculative space savings. Native song-table references keep original sequence headers live. Removing such entries needs separate dynamic/cross-reference validation and a measured rebuild.'}
(P/'STOCKAGE_ET_CANDIDATS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='explicit_token_absence_candidates'},ensure_ascii=False,indent=2))

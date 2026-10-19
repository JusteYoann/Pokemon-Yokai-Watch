#!/usr/bin/env python3
"""Prove translation source deltas only affect literals, not executable scripts."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from localiser_fr import ROOT
p=argparse.ArgumentParser();p.add_argument('baseline');p.add_argument('report',type=Path);a=p.parse_args()
files=subprocess.check_output(['git','diff','--name-only',a.baseline],cwd=ROOT,text=True).splitlines();checked=[]
for rel in files:
 if not rel.startswith(('src/','data/maps/','data/text/','data/scripts/')):continue
 path=ROOT/rel
 if path.suffix not in ['.c','.h','.inc']:raise AssertionError(('Unexpected non-text source',rel))
 before=subprocess.check_output(['git','show',a.baseline+':'+rel],cwd=ROOT,text=True);after=path.read_text()
 if path.suffix=='.inc':
  strip=lambda s:re.sub(r'(?m)^[ \t]*\.string.*\n','',s)
 else:
  strip=lambda s:re.sub(r'"(?:\\.|[^"\\])*"','""',s)
  # Adjacent C literals may be joined by the localization tool.
  normalize=lambda s:re.sub(r'""(?:\s*"")+','""',s)
  original=strip;strip=lambda s:normalize(original(s))
 assert strip(before)==strip(after),('Executable or structural source change',rel)
 checked.append(rel)
protected=['graphics/','sound/','include/','src/data/trainer_parties','src/data/trainers','src/data/pokemon/species_info','src/data/pokemon/evolution','src/data/pokemon/level_up','data/wild_encounters','data/maps/']
assert not [f for f in files if f.startswith(tuple(protected[:-1]))], 'Unexpected protected data modification'
assert not [f for f in files if f.startswith('data/maps/') and not f.endswith('/text.inc')], 'Map scripts or objects changed'
rom=ROOT/'pokefirered_audio.gba';size=rom.stat().st_size;assert size<=32*1024**2
out=dict(passed=True,baseline=a.baseline,text_only_source_files=checked,all_source_deltas_are_literals=True,map_scripts_and_gameplay_unchanged=True,graphics_and_audio_unchanged=True,rom_bytes=size,rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),scope='Text-only delta proof, not semantic proof of every translation or full playthrough.')
a.report.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PRESERVATION PASS',len(checked),size)

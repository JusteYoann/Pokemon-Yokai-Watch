#!/usr/bin/env python3
"""Reproduce the conservative sequence deletion proof from the unmodified base table."""
from pathlib import Path
import re,json,subprocess
p=Path('sound/song_table.inc');t=subprocess.check_output(['git','show','0fa1808fe:sound/song_table.inc'],text=True);rows=re.findall(r'^\s*song\s+(\w+),\s*(\d+),\s*(\d+)([^\n]*)',t,re.M)
const={}
for name,value in re.findall(r'^#define\s+(\w+)\s+(\d+)\b',Path('include/constants/songs.h').read_text(),re.M):const[name]=int(value)
alias=re.findall(r'\{(MUS_\w+),\s*(MUS_\w+)\}',Path('src/data/yokai_music_aliases.h').read_text().split('sYokaiUnavailableMusicFallbacks')[0])
protected={r[0] for r in rows if '@ MUS_YOKAI_' in r[3]}
candidates=[]
for src,dst in alias:
 i=const[src];symbol=rows[i][0]
 if symbol in protected or not Path('sound/songs/midi/'+symbol+'.mid').exists():continue
 # Every table occurrence must be an alias source; leave fanfares and future unaliased entries intact.
 ix=[j for j,r in enumerate(rows) if r[0]==symbol]
 if not all(j in [const[a] for a,b in alias] for j in ix):continue
 candidates.append({'id':i,'constant':src,'symbol':symbol,'resolved_constant':dst,'actual_header':rows[const[dst]][0],'proof':'All table entries for this sequence are unconditionally redirected by YokaiGetSongHeader; no dedicated public fallback refers to it.'})
# Scan C / assembly for direct symbol consumers outside own generated sequence and linkage.
texts=[]
for directory in ['src','data','asm','include']:
 for q in Path(directory).rglob('*'):
  if q.suffix in ['.c','.h','.s','.inc']:texts.append((str(q),q.read_text(errors='replace')))
for r in candidates:
 r['direct_symbol_references']=[q for q,s in texts if re.search(r'\b'+r['symbol']+r'\b',s)]

excluded=[r for r in candidates if r['direct_symbol_references']]
candidates=[r for r in candidates if not r['direct_symbol_references']]
report={'retained_direct_references':excluded,'policy':'Retain all private DPCM, all shared voicegroups and samples, all sound effects, all fanfares, all dedicated public fallbacks, all unaliased/reserved music. Exclude only provably bypassed native sequence objects; keep source files and all numeric IDs. Zero-track sentinel headers retain safe pointers in bypassed table slots.','sequences':candidates,'retained_public_fallbacks':sorted(protected),'private_sample_deletions':[],'sample_bank_deletions':[]}
Path('docs/dossier-20261023/audio-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(len(candidates),'proven unreachable sequences',', '.join(r['symbol'] for r in candidates))

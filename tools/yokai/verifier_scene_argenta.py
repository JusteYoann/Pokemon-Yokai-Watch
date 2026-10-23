#!/usr/bin/env python3
"""Static, read-only checks of approved text, walkable paths and protected resources."""
import json,hashlib,re,struct,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/ARGENTA_MORLEONE'
texts=json.loads((Q/'DIALOGUES_VALIDES.json').read_text());source=(R/'data/maps/PewterCity/text.inc').read_text()
for label,paragraphs in texts.items():
 actual=re.search(r'^'+label+r'::\n\s*\.string "(.*?)"',source,re.M)[1]
 pages=actual.rstrip('$').split(r'\p');assert len(pages)==len(paragraphs)
 assert [re.sub(r'\\[nl]',' ',p) for p in pages]==paragraphs,label
from cadrer_dialogues_fr import measure
for label in texts:
 value=re.search(r'^'+label+r'::\n\s*\.string "(.*?)"',source,re.M)[1]
 assert max(map(measure,re.split(r'\\[nlp]',value)))<=208,label
# Exact preservation of all pre-existing dialogue and scripts outside the inserted hook.
ref='1bf5774d8';old=lambda p:subprocess.check_output(['git','show',ref+':'+p],cwd=R)
assert source.startswith(old('data/maps/PewterCity/text.inc').decode())
s=(R/'data/maps/PewterCity/scripts.inc').read_text().replace('\tcall PewterCity_MorleoneOnTransition\n','',1).replace('\n\t.include "data/maps/PewterCity/morleone.inc"\n','')
assert s==old('data/maps/PewterCity/scripts.inc').decode()
for p in (R/'data/maps').glob('*/scripts.inc'):
 if p.parent.name!='PewterCity':assert p.read_bytes()==old(str(p.relative_to(R))),p
for p in (R/'data/maps').glob('*/text.inc'):
 if p.parent.name!='PewterCity':assert p.read_bytes()==old(str(p.relative_to(R))),p
for p in ['src/data/trainers.h','src/data/trainer_parties.h']:
 assert (R/p).read_bytes()==old(p),p
authorized_audio={'data/yokai/audio_loops.json','data/yokai/audio_candidates.json','data/yokai/audio_session1_aliases.json','data/yokai/mixer_calibration.json','src/data/yokai_mixer_gains.h','src/data/yokai_music_aliases.h','include/constants/songs.h','sound/song_table.inc'}
for path,want in json.loads((R/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/BASE_PROTEGEE.json').read_text())['files'].items():
 if path not in authorized_audio:assert hashlib.sha256((R/path).read_bytes()).hexdigest()==want,path
# Except new object/coord arrays, all city properties/events remain unchanged.
m=json.loads((R/'data/maps/PewterCity/map.json').read_text());base=json.loads(old('data/maps/PewterCity/map.json'))
assert m['object_events'][:7]==base['object_events'] and m['coord_events'][:-4]==base['coord_events']
x=dict(m);x['object_events']=base['object_events'];x['coord_events']=base['coord_events'];assert x==base
for p in (R/'data/maps').glob('*/map.json'):
 if p.parent.name=='PewterCity':continue
 before=json.loads(old(str(p.relative_to(R))));after=json.loads(p.read_text())
 if p.parent.name=='PalletTown_RivalsHouse':before['music']='MUS_YOKAI_KATIE_HOUSE'
 assert before==after,p
v=struct.unpack('<1920H',(R/'data/layouts/PewterCity/map.bin').read_bytes())
points=[(x,35) for x in range(20,25)]+[(24,y) for y in range(13,36)]+[(x,8) for x in range(23,33)]+[(x,12) for x in range(16,33)]+[(25,y) for y in range(13,21)]
assert all((v[y*48+x]>>10)&3==0 and v[y*48+x]>>12==3 for x,y in points)
assert len(m['object_events'])+2<=16
assert not any('MUS_YOKAI_ZOMBIE_NIGHT' in p.read_text() for p in (R/'data/maps').glob('*/map.json'))
print('PASS: exact approved dialogue; existing story/teams/maps/art preserved; routes collision-free; Zombie unassigned')

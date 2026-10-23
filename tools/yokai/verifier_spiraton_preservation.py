#!/usr/bin/env python3
"""Read-only protection checks against Argenta d2f590d8b and its private ROM."""
import hashlib,json,subprocess,struct
from pathlib import Path
from mgba_rpc import ROOT
Q=ROOT/'QA_RECETTE_FINALE/DON_SPIRATON';base='d2f590d8b'
def original(p):return subprocess.check_output(['git','show',base+':'+p],cwd=ROOT)
# Entire permanent species data and all existing graphic assets remain intact.
protected=subprocess.check_output(['git','ls-tree','-r','--name-only',base,'graphics','src/data/pokemon','data/yokai/noms_affiches.json','data/yokai/audio_loops.json','src/data/yokai_mixer_gains.h'],cwd=ROOT,text=True).splitlines()
# Compare through Git's declared text filters (JASC palettes use CRLF).
subprocess.run(['git','diff','--exit-code',base,'--','graphics','src/data/pokemon','data/yokai/noms_affiches.json','data/yokai/audio_loops.json','src/data/yokai_mixer_gains.h'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
old=original('src/data/trainer_parties.h');assert (ROOT/'src/data/trainer_parties.h').read_bytes().startswith(old)
# All original trainer entries are byte-for-byte preserved (two appended records).
a=original('src/data/trainers.h').decode();b=(ROOT/'src/data/trainers.h').read_text();assert b.startswith(a[:a.rfind('};')])
# Retire only Don's warehouse actor. Staff and all original warehouse events survive.
p='data/maps/FiveIsland_RocketWarehouse/map.json';a=json.loads(original(p));b=json.loads((ROOT/p).read_text());a['object_events']=[x for x in a['object_events'] if x.get('local_id')!='LOCALID_YOKAI_DONMORLEONE'];assert a==b
for p in (ROOT/'data/maps').glob('*/map.json'):
 if p.parent.name=='PokemonLeague_ChampionsRoom':
  before=json.loads(original(str(p.relative_to(ROOT))));after=json.loads(p.read_text())
  # Only four dormant diagnostic actor templates are added; original map intact.
  assert after['object_events'][:2]==before['object_events']
  extra=after['object_events'][2:];assert len(extra)==4
  assert all(x['flag']=='FLAG_TEMP_6' for x in extra)
  after['object_events']=after['object_events'][:2];assert before==after
 elif p.parent.name!='FiveIsland_RocketWarehouse':assert p.read_bytes()==original(str(p.relative_to(ROOT))),p
assert 'YokaiCameo_DonMorleone' not in (ROOT/'data/scripts/yokai_cameos_boss.inc').read_text()
oldroot=Path('/workspace/Pokemon-Yokai-Watch-argenta')
def symbols(root):return {v[2]:int(v[0],16) for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(root/'pokefirered_audio.elf')],text=True).splitlines() if len(v:=l.split())==3}
x=symbols(oldroot);y=symbols(ROOT);ar=(oldroot/'pokefirered_audio.gba').read_bytes();br=(ROOT/'pokefirered_audio.gba').read_bytes();assert hashlib.sha256(ar).hexdigest()=='a8211bafc29ab8e750c412dc921b5989b8e443548095b9b66f179c78efdf18bb'
def chunk(blob,s,name,n):return blob[s[name]-0x8000000:s[name]-0x8000000+n]
for num in range(1,32):
 n=(Path('/workspace/private-audio/argenta-integration')/f'{num:02d}.dpcm').stat().st_size
 assert chunk(ar,x,f'yokai_wave_{num:02d}',n)==chunk(br,y,f'yokai_wave_{num:02d}',n),num
assert chunk(ar,x,'sYokaiSongGain',756)==chunk(br,y,'sYokaiSongGain',756)
assert int.from_bytes(chunk(br,y,'gYokaiPrivateAudioMask',4),'little')==0x7FFFFFFF
assert len(br)<33554432
report=dict(passed=True,base=base,protected_files=len(protected),original_trainers_and_parties_unchanged=True,all31_waveforms_and_gains_unchanged=True,private_bytes=len(br),private_sha256=hashlib.sha256(br).hexdigest(),public_sha256=hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),headroom_to_32MiB=33554432-len(br),production_finale_enabled=False)
(Q/'PRESERVATION.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS preservation',len(protected),'protected files; all31 encoded OST unchanged; ROM',len(br))

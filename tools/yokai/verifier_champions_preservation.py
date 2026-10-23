#!/usr/bin/env python3
"""Source, asset, audio and native generated-party preservation audit."""
from pathlib import Path
import json,re,hashlib,subprocess
from mgba_rpc import ROOT
BASE='d32774305';P=ROOT/'docs/champions-yokai-watch/validation';P.mkdir(parents=True,exist_ok=True)
def original(p):return subprocess.check_output(['git','show',BASE+':'+str(p)],cwd=ROOT)
def read(p):return (ROOT/p).read_text()
def sha(b):return hashlib.sha256(b).hexdigest()
preserved={}
for file in ['src/data/pokemon/species_info.h','src/data/pokemon/level_up_learnsets.h','src/data/pokemon/level_up_learnset_pointers.h','src/data/pokemon/evolution.h','src/data/text/species_names.h','src/data/wild_encounters.json','sound/song_table.inc','data/yokai/audio_loops.json','include/global.h','include/pokemon.h','include/constants/flags.h','include/constants/vars.h','src/pokemon.c','src/battle_util.c','src/party_menu.c','src/spiraton_battle.c','src/spiraton_core.c','src/spiraton_art_preview.c']:
 b=(ROOT/file).read_bytes();assert b==original(file),file;preserved[file]=sha(b)
# All pre-existing artwork, including the player, Lavanville and the finale.
assets=[]
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'graphics'],cwd=ROOT,text=True).splitlines()
for file in paths:
 if file.endswith(('.png','.pal')):
  b=(ROOT/file).read_bytes();old=original(file)
  if file.endswith('.pal'):b=b.replace(b'\r\n',b'\n');old=old.replace(b'\r\n',b'\n')
  assert b==old,file;assets.append(dict(file=file,sha256=sha(b),line_endings_normalized=file.endswith('.pal')))
# Preserve all non-target trainer records, parties and forced ability slots.
protected_teams={}
for path,pattern,allowed in [
 ('src/data/trainers.h',r'(?:^|\n)    \[(TRAINER_\w+)\] = \{(.*?)\n    \},',{'TRAINER_LEADER_BROCK','TRAINER_LEADER_MISTY','TRAINER_LEADER_LT_SURGE','TRAINER_LEADER_SABRINA','TRAINER_LEADER_BLAINE'}),
 ('src/data/trainer_parties.h',r'static const struct \w+ (\w+)\[\] = \{(.*?)\n\};',{'sYokaiParty_LEADER_MISTY','sYokaiParty_LEADER_LT_SURGE','sYokaiParty_LEADER_ERIKA','sYokaiParty_LEADER_BLAINE'}),
 ('src/data/yokai_trainer_abilities.h',r'\[(TRAINER_\w+)\] = (\{[^}]+\})',{'TRAINER_LEADER_MISTY','TRAINER_LEADER_LT_SURGE','TRAINER_LEADER_BLAINE'})]:
 old=dict(re.findall(pattern,original(path).decode(),re.S));new=dict(re.findall(pattern,read(path),re.S))
 for key,value in old.items():
  if key not in allowed:assert new[key]==value,(path,key)
 protected_teams[path]=dict(unchanged=len(old)-len(allowed),allowed_changes=sorted(allowed))
# Gameplay scripts/layouts of these chapters remain byte-identical. Only targeted
# text names outside these protected maps and isolated battle presentation change.
protected_maps=['FuchsiaCity_Gym','ViridianCity_Gym','PokemonLeague_ChampionsRoom','PokemonLeague_HallOfFame','LavenderTown','PokemonTower_1F','PokemonTower_2F','PokemonTower_3F','PokemonTower_4F','PokemonTower_5F','PokemonTower_6F','PokemonTower_7F','CeladonCity_Gym','CeladonCity_GameCorner','RocketHideout_B4F','Route12','Route16']
for name in protected_maps:
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'data/maps/'+name],cwd=ROOT,text=True).splitlines():
  assert (ROOT/path).read_bytes()==original(path),str(path)
# Koga and Don's Fame Checker records also keep their exact content.
pattern=r'^(\w+)::[^\n]*\n(.*?)(?=^\w+::|\Z)'
old=dict(re.findall(pattern,original('data/text/fame_checker.inc').decode(),re.S|re.M));new=dict(re.findall(pattern,read('data/text/fame_checker.inc'),re.S|re.M))
for key in old:
 if re.search(r'_(Koga|Giovanni)\w*$',key):assert re.findall(r'\.string[^\n]+',old[key])==re.findall(r'\.string[^\n]+',new[key]),key
# Exact reused Berenice PNG/palettes, with provenance, not generated substitutes.
berenice=[]
for file in ['overworld.png','battle.png','overworld.pal','normal.pal']:
 p=ROOT/'graphics/yokai_characters/berenice'/file;b=p.read_bytes();assert b==(ROOT/'docs/champions-yokai-watch/preparation/ressources/berenice'/file).read_bytes();berenice.append(dict(file=file,sha256=sha(b)))
# Native generation proof checks PID/nature, stats, moves/PP, item and ability.
reference=json.loads((P/'EQUIPES_REFERENCE_MGBA.json').read_text());comparisons={}
for mode in ['public','prive']:
 source=json.loads((P/mode/'EQUIPES_MGBA.json').read_text());teams=source['teams'];checked=[]
 for gender in [0,1]:
  for suffix in ['BROCK','SABRINA','KOGA','GIOVANNI']:
   key=f'{gender}:TRAINER_LEADER_{suffix}';assert teams[key]==reference['teams'][key],(mode,key);checked.append(key)
 for suffix in ['MISTY','BLAINE']:
  assert teams['0:TRAINER_LEADER_'+suffix]==teams['1:TRAINER_LEADER_'+suffix],(mode,suffix,'variant party changed')
 comparisons[mode]=dict(preserved_native_parties=checked,identical_party_between_sexes=['MISTY','BLAINE'],rom_sha256=source['rom_sha256'])
# Compare all 31 private WaveData streams to the actual protected local pack.
# No copyrighted audio is copied into the repository or this report.
elf=ROOT/'pokefirered_audio.elf';symbols={}
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(elf)],text=True).splitlines():
 a=line.split()
 if len(a)==3:symbols[a[2]]=int(a[0],16)
rom=(ROOT/'pokefirered_audio.gba').read_bytes();audio=[]
for i in range(1,32):
 file=Path('/workspace/private-audio/lavanville-integration')/f'{i:02d}.dpcm';b=file.read_bytes();offset=symbols[f'yokai_wave_{i:02d}']-0x08000000
 assert rom[offset:offset+len(b)]==b,i;audio.append(dict(track=i,bytes=len(b),sha256=sha(b)))
# Verify chapter-specific wandering zombie parameters and start function unchanged.
old=original('src/lavanville.c').decode();new=read('src/lavanville.c')
for pattern in [r'static const u16 sZombieStats.*?\n\};',r'static const u16 sZombieMoves.*?\n\};',r'void LavanvilleStartZombieBattle\(void\).*?\n\}']:
 assert re.search(pattern,old,re.S)[0]==re.search(pattern,new,re.S)[0]
report=dict(passed=True,base=BASE,preserved_sources=preserved,unchanged_artwork=len(assets),artwork=assets,berenice_exact_resources=berenice,trainer_preservation=protected_teams,protected_maps=protected_maps,native_party_comparisons=comparisons,private_audio_streams=audio,wandering_zombie_data_and_battle_start_unchanged=True,no_save_layout_or_flag_changes=True)
(P/'PRESERVATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PRESERVATION PASS:',len(assets),'original PNG/pal files, all151 data,31 audio streams, native preserved teams and both gender variants')

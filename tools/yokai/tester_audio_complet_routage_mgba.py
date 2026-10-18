#!/usr/bin/env python3
"""Every compiled BGM ID/map header resolves to an active sample; SFX stay native."""
import csv,hashlib,json,re,struct,os
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/os.environ.get('YOKAI_AUDIO_ROUTING_REPORT_DIR','QA_RECETTE_FINALE/AUDIO_COMPLEMENT');P.mkdir(parents=True,exist_ok=True)
config=json.loads((ROOT/'data/yokai/audio_session1_aliases.json').read_text());aliases={a['source']:a['target'] for a in config['aliases']};substitutes={a['source']:a['target'] for a in config['private_unavailable_fallbacks']};active=set(json.loads((ROOT/'data/yokai/audio_loops.json').read_text())['active_tracks'])
C={k:int(v,0) for k,v in re.findall(r'^#define\s+((?:MUS|SE)_\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',(ROOT/'include/constants/songs.h').read_text(),re.M)};names={v:k for k,v in C.items()};entries=re.findall(r'^\s*song\s+(\w+),\s*(\d+),\s*(\d+)',(ROOT/'sound/song_table.inc').read_text(),re.M)
r=new_game();rows=[];maps=[];unchanged=[];battle_themes=[];passed=False;error='Interrupted'
def raw(n):return r.u32(r.symbols['gSongTable']+8*n)
def resolve(name):
 theme=aliases.get(name,name);n=C[theme]-346
 if n not in active:theme=substitutes[theme];n=C[theme]-346
 assert n in active,(name,theme,n);return theme,n,r.symbols[f'mus_yokai_{n:02d}']
try:
 limits=json.loads((ROOT/'data/yokai/audio_loops.json').read_text())
 assert len(active)<=limits.get('max_active_tracks',20)
 assert len(r.rom_buffer.raw[:-1])<=limits.get('budget_rom_bytes',32*1024*1024)
 for n in range(1,len(entries)):
  name=names.get(n,str(n))
  if n<256 or entries[n][1]!='0':
   assert r.call('YokaiGetSongHeader',n,raw(n))==raw(n),(name,'Native effect was changed');unchanged.append(n);continue
  theme,slot,expected=resolve(name);assert r.call('YokaiGetSongHeader',n,raw(n))==expected,name
  r.call('m4aSongNumStart',n);r.run(8);assert r.u32(r.symbols['gMPlayInfo_BGM'])==expected,(name,'BGM not started')
  before=r.u32(r.symbols['gMPlayInfo_BGM']+12);r.call('m4aSongNumStartOrChange',C[theme]);r.run(8)
  assert r.u32(r.symbols['gMPlayInfo_BGM']+12)>before,(name,'Alias to explicit restarted')
  rows.append(dict(id=n,requested=name,effective=theme,slot=slot,private_sample=True,temporary_substitute=aliases.get(name,name) in substitutes and C[aliases.get(name,name)]-346 not in active,native_start_checked=True,no_restart_to_effective_theme=True))
 g=json.loads((ROOT/'data/maps/map_groups.json').read_text())
 for group,key in enumerate(g['group_order']):
  table=r.u32(r.symbols['gMapGroups']+4*group)
  for number,name in enumerate(g[key]):
   source=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());header=r.u32(table+4*number);music=int.from_bytes(r.read(header+16,2),'little');assert music==C[source['music']],(name,music,source['music'])
   if source['music']=='MUS_NONE':maps.append(dict(map=name,requested='MUS_NONE',effective='SILENCE',slot='',private_sample=False));continue
   theme,slot,expected=resolve(source['music']);assert r.call('YokaiGetSongHeader',music,raw(music))==expected,name
   maps.append(dict(map=name,requested=source['music'],effective=theme,slot=slot,private_sample=True))
 assert len(rows)==104 and len(unchanged)==273 and len(maps)==425
 # Champion's post-victory branch compared a raw native symbol before this
 # change. Exercise it on the actual map with the new resolved victory cue.
 group,num=next((i,j) for i,key in enumerate(g['group_order']) for j,n in enumerate(g[key]) if n=='PokemonLeague_ChampionsRoom')
 for trainer in re.findall(r'^#define\s+TRAINER_CHAMPION_(?:FIRST|REMATCH)_\w+\s+(\d+)\b',(ROOT/'include/constants/opponents.h').read_text(),re.M):r.call('SetTrainerFlag',int(trainer))
 r.call('SetWarpDestination',group,num,255,4,5);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 theme,slot,expected=resolve('MUS_VICTORY_GYM_LEADER');r.call('PlayBGM',C['MUS_VICTORY_GYM_LEADER']);r.run(60);before=r.u32(r.symbols['gMPlayInfo_BGM']+12)
 r.call('Overworld_PlaySpecialMapMusic');r.run(20);assert r.u32(r.symbols['gMPlayInfo_BGM'])==expected;assert r.u32(r.symbols['gMPlayInfo_BGM']+12)>before
 opponents=(ROOT/'include/constants/opponents.h').read_text()
 trainers={k:int(v) for k,v in re.findall(r'^#define\s+(TRAINER_\w+)\s+(\d+)\b',opponents,re.M)}
 for name,target in re.findall(r'^#define\s+(TRAINER_\w+)\s+(TRAINER_\w+)\b',opponents,re.M):
  if target in trainers:trainers[name]=trainers[target]
 r.w32(r.symbols['gBattleTypeFlags'],8)
 cases=[('TRAINER_YOKAI_DOMNISCIAN','MUS_YOKAI_HINOZALL'),('TRAINER_YOKAI_DONMORLEONE','MUS_YOKAI_GHOULFATHER'),('TRAINER_YOKAI_ENMA','MUS_YOKAI_ZAZELMARE'),('TRAINER_ELITE_FOUR_LORELEI','MUS_YOKAI_DECISIVE_BATTLE'),('TRAINER_BLACK_BELT_KOICHI','MUS_YOKAI_BLASTERS_THEME'),('TRAINER_SCIENTIST_TED','MUS_YOKAI_ROBON_3000')]
 cases += [(name,'MUS_YOKAI_MINI_BOSS') for name in ['TRAINER_YOKAI_EMPLOYEROUGE','TRAINER_YOKAI_EMPLOYEBLEU','TRAINER_YOKAI_MAFIAMILLE1','TRAINER_YOKAI_MAFIAMILLE2','TRAINER_YOKAI_MAFIAMILLE3']]
 for name,theme in cases:
  r.write(r.symbols['gTrainerBattleOpponent_A'],trainers[name].to_bytes(2,'little'));assert r.call('GetBattleBGM')==C[theme],(name,theme)
  battle_themes.append(dict(trainer=name,music=theme,native_selection_verified=True))
 r.frame.save(P/'champion-victoire-maintien.png');passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'routage-diagnostic.png');raise
finally:
 r.close()
 for name,data in [('AFFECTATIONS_BGM_EFFECTIVES.csv',rows),('AFFECTATIONS_CARTES_EFFECTIVES.csv',maps)]:
  if data:
   with (P/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 (P/'ROUTAGE_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),active_tracks=sorted(active),bgm_checked=rows,compiled_maps=maps,native_unchanged_sfx_and_functional_jingles=unchanged,champion_post_victory_branch_checked=passed,battle_theme_selection=battle_themes,scope='104 native BGM playback calls, all 425 compiled map headers, all 273 SFX/fanfare header resolutions; fixtures after real new-game. This is not traversal of all maps or listening to each whole track.'),ensure_ascii=False,indent=2)+'\n')
print('PASS all 104 BGM IDs, all 425 compiled map headers, 273 untouched effects/jingles and champion victory continuity')

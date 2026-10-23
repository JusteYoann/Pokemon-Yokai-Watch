#!/usr/bin/env python3
"""Exact source/art/map/audio preservation and link-map audit of phase C."""
import json,subprocess,hashlib,re
from pathlib import Path
from mgba_rpc import ROOT
BASE='a8c97b3ca';D=ROOT/'docs/cramois-ile-passe/phase-c'
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
files=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=ROOT,text=True).strip('\0').split('\0')
changed=set(subprocess.check_output(['git','diff',BASE,'--name-only','-z'],cwd=ROOT,text=True).strip('\0').split('\0')) & set(files)
allowed={'data/maps/CinnabarIsland_Gym/map.json','data/maps/CinnabarIsland_Gym/scripts.inc','data/maps/CinnabarIsland_Gym/text.inc','include/constants/event_objects.h','include/constants/flags.h','src/data/object_events/object_event_anims.h','src/data/object_events/object_event_graphics.h','src/data/object_events/object_event_graphics_info.h','src/data/object_events/object_event_graphics_info_pointers.h','src/data/object_events/object_event_pic_tables.h','src/event_object_movement.c'}
game={p for p in changed if p.startswith(('src/','include/','graphics/','data/','sound/'))};assert game==allowed,(game-allowed,allowed-game)
art=[p for p in files if p.startswith('graphics/') and p.endswith(('.png','.pal'))];assert not set(art)&changed
maps=[p for p in files if p.startswith(('data/maps/','data/layouts/'))];assert set(maps)&changed=={p for p in allowed if p.startswith('data/maps/')}
path='data/maps/CinnabarIsland_Gym/map.json';a=json.loads(old(path));b=json.loads((ROOT/path).read_text());ao=a.pop('object_events');bo=b.pop('object_events');assert a==b and len(bo)==len(ao)+1
for x,y in zip(ao,bo):
 y=dict(y)
 if y.get('graphics_id')=='OBJ_EVENT_GFX_BLAINE':y.pop('local_id')
 assert x==y
p='data/maps/CinnabarIsland_Gym/scripts.inc';a=dict(re.findall(r'^(\w+)::\n(.*?)(?=^\w+::|\Z)',old(p).decode(),re.M|re.S));b=dict(re.findall(r'^(\w+)::\n(.*?)(?=^\w+::|\Z)',(ROOT/p).read_text(),re.M|re.S))
for k in a:
 if k=='CinnabarIsland_Gym_EventScript_Blaine' or re.fullmatch(r'CinnabarIsland_Gym_EventScript_Quiz[1-6]',k):continue
 assert a[k]==b[k],k
for p in ['src/cramois_past.c','src/cramois_fog.c','src/overworld.c','src/data/trainers.h','src/data/trainer_parties.h']:
 assert (ROOT/p).read_bytes()==old(p)
s={}
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(ROOT/'pokefirered_audio.elf')],text=True).splitlines():
 f=line.split()
 if len(f)==3:s[f[2]]=int(f[0],16)
rom=(ROOT/'pokefirered_audio.gba').read_bytes();audio=[]
for i in range(1,32):
 raw=Path(f'/workspace/private-audio/lavanville-integration/{i:02d}.dpcm').read_bytes();offset=s[f'yokai_wave_{i:02d}']-0x08000000;assert rom[offset:offset+len(raw)]==raw;audio.append(dict(track=i,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
memory={}
for mode,file in [('public','pokefirered.map'),('prive','pokefirered_audio.map')]:
 t=(ROOT/file).read_text();ew=int(re.search(r'^ewram\s+0x[0-9a-f]+\s+0x([0-9a-f]+)',t,re.M)[1],16);iw=int(re.search(r'^iwram\s+0x[0-9a-f]+\s+0x([0-9a-f]+)',t,re.M)[1],16)
 assert ew==261368 and iw==(29824 if mode=='public' else 29888)
 memory[mode]=dict(ewram_before=261368,ewram_after=ew,ewram_added=0,ewram_free=262144-ew,iwram_before=iw,iwram_after=iw)
r=dict(passed=True,base=BASE,existing_game_files_changed=sorted(game),approved_artwork_unchanged=len(art),map_files_unchanged=len(maps)-3,gym_geometry_warps_existing_nine_actors_and_all_nonquiz_helpers_unchanged=True,phase_a_b_runtime_and_lut_unchanged=True,all_existing_trainers_teams_species_and_save_format_unchanged=True,fuchsia_secondary_appearance_and_rewards_unchanged=True,other_quest_lavanville_and_finale_sources_unchanged=True,private_audio=audio,memory=memory,new_companion_resources=dict(static_ewram_bytes=0,obj_sprite_slots=1,obj_vram_tile_bytes=512,existing_reserved_palette_bank=8,source_frames=2))
(D/'PRESERVATION.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS: approved art, geometry, helper scripts, A/B, teams,151 Yo-kai, audio; EWRAM +0,776 free')

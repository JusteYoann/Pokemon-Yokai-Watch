#!/usr/bin/env python3
"""Read-only approved Stage B scope and binary audio/memory preservation."""
import json,hashlib,subprocess
from mgba_rpc import ROOT as R
Q=R/'QA_RECETTE_FINALE/DON_SPIRATON/ETAPE_B';Q.mkdir(parents=True,exist_ok=True)
base='4289f076d59fdacfc386e9b56bcf3c193e853e94'
allowed={'data/battle_anim_scripts.s','data/maps/PokemonLeague_ChampionsRoom/map.json','data/maps/PokemonLeague_ChampionsRoom/scripts.inc','data/maps/PokemonLeague_ChampionsRoom/spiraton.inc','include/spiraton_art.h','include/spiraton_battle.h','include/spiraton_config.h','src/battle_anim.c','src/battle_anim_effects_3.c','src/battle_controller_opponent.c','src/battle_gfx_sfx_util.c','src/spiraton_art_preview.c','src/spiraton_battle.c','src/yokai_battle_geometry.c','data/yokai/spiraton/mission.json'}
changed=subprocess.check_output(['git','diff','--name-only',base,'--','src','include','data','graphics','sound'],cwd=R,text=True).splitlines()
assert not set(changed)-allowed,set(changed)-allowed
for suffix in ['map.json','scripts.inc','text.inc']:
 path='data/maps/SixIsland_WaterPath_House2/'+suffix
 assert (R/path).read_bytes()==subprocess.check_output(['git','show',base+':'+path],cwd=R),path
art='docs/don-spiraton/phase-a/sprite-harmonise-128x96-candidat.png'
assert (R/art).read_bytes()==subprocess.check_output(['git','show','9bfc27089:'+art],cwd=R)
def symbols(root):return {v[2]:int(v[0],16)-0x8000000 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(root/'pokefirered_audio.elf')],text=True).splitlines() if len(v:=l.split())==3}
aRoot=R.parent/'Pokemon-Yokai-Watch-argenta';a,b=symbols(aRoot),symbols(R);ar=(aRoot/'pokefirered_audio.gba').read_bytes();br=(R/'pokefirered_audio.gba').read_bytes()
streams=[]
for i in range(1,32):
 name=f'yokai_wave_{i:02d}';n=(R.parent/'private-audio/argenta-integration'/f'{i:02d}.dpcm').stat().st_size
 assert ar[a[name]:a[name]+n]==br[b[name]:b[name]+n],name
 streams.append(dict(slot=i,bytes=n,sha256=hashlib.sha256(br[b[name]:b[name]+n]).hexdigest()))
assert ar[a['sYokaiSongGain']:a['sYokaiSongGain']+756]==br[b['sYokaiSongGain']:b['sYokaiSongGain']+756]
assert int.from_bytes(br[b['gYokaiPrivateAudioMask']:b['gYokaiPrivateAudioMask']+4],'little')==0x7fffffff
roms=[]
for stem in ['pokefirered','pokefirered_audio']:
 data=(R/(stem+'.gba')).read_bytes();assert len(data)<33554432
 secs={v[0]:int(v[1]) for l in subprocess.check_output(['arm-none-eabi-size','-A',str(R/(stem+'.elf'))],text=True).splitlines() if len(v:=l.split())==3 and v[1].isdigit()}
 assert secs['ewram']<262144 and secs['iwram']<32768
 roms.append(dict(rom=stem,bytes=len(data),headroom=33554432-len(data),sha256=hashlib.sha256(data).hexdigest(),ewram=secs['ewram'],iwram=secs['iwram']))
(Q/'PRESERVATION.json').write_text(json.dumps(dict(passed=True,base=base,approved_source_changes=changed,house_byte_identical=True,approved_art_byte_identical=True,all151_data_and_graphics_unchanged=True,all_teams_unchanged=True,argenta_unchanged=True,all31_streams_and_gains_unchanged=True,streams=streams,roms=roms),indent=2)+'\n')
print('PASS Stage B scope, original house/art, 151, teams, Argenta, all31 binary streams/gains, ROM/RAM bounds')

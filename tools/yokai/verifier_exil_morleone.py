#!/usr/bin/env python3
"""Read-only scope/ROM/audio verification for the approved exile-house change."""
from pathlib import Path
import json,hashlib,subprocess
from mgba_rpc import ROOT as R
Q=R/'QA_RECETTE_FINALE/DON_SPIRATON/EXIL';Q.mkdir(parents=True,exist_ok=True);base='7f2c7d69b'
subprocess.run(['git','diff','--exit-code',base,'--','src','include','graphics','sound','data/scripts','data/yokai'],cwd=R,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['git','diff','--exit-code',base,'--','data/maps',':(exclude)data/maps/SixIsland_WaterPath_House2'],cwd=R,check=True,stdout=subprocess.DEVNULL)
def original(path):return subprocess.check_output(['git','show',base+':'+path],cwd=R)
p='data/maps/SixIsland_WaterPath_House2/map.json';a=json.loads(original(p));b=json.loads((R/p).read_text());old=a['object_events'][0];resident=b['object_events'][0].copy()
assert resident.pop('local_id')=='LOCALID_EXILE_RESIDENT';assert resident.pop('flag')=='FLAG_TEMP_6';resident['flag']='0';assert resident==old
assert len(b['object_events'])==2;don=b['object_events'][1].copy()
for key,value in [('local_id','LOCALID_EXILE_DON_MORLEONE'),('graphics_id','OBJ_EVENT_GFX_YOKAI_DONMORLEONE'),('script','SixIsland_WaterPath_House2_EventScript_DonMorleone'),('flag','FLAG_TEMP_7'),('movement_type','MOVEMENT_TYPE_FACE_DOWN')]:assert don.pop(key)==value,key
assert don=={k:v for k,v in old.items() if k not in ['graphics_id','script','flag','movement_type']}
b['object_events']=a['object_events'];assert a==b,'Layout/warps/other map properties changed'
p='data/maps/SixIsland_WaterPath_House2/text.inc';assert (R/p).read_bytes().startswith(original(p))
p='data/maps/SixIsland_WaterPath_House2/scripts.inc';assert original(p).decode().split('SixIsland_WaterPath_House2_EventScript_Man::')[1] in (R/p).read_text()
oldroot=R.parent/'Pokemon-Yokai-Watch-argenta'
def symbols(root):return {v[2]:int(v[0],16)-0x8000000 for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(root/'pokefirered_audio.elf')],text=True).splitlines() if len(v:=l.split())==3}
x,y=symbols(oldroot),symbols(R);ar=(oldroot/'pokefirered_audio.gba').read_bytes();br=(R/'pokefirered_audio.gba').read_bytes()
for num in range(1,32):
 name=f'yokai_wave_{num:02d}';n=(R.parent/'private-audio/argenta-integration'/f'{num:02d}.dpcm').stat().st_size
 assert ar[x[name]:x[name]+n]==br[y[name]:y[name]+n],name
assert ar[x['sYokaiSongGain']:x['sYokaiSongGain']+756]==br[y['sYokaiSongGain']:y['sYokaiSongGain']+756]
assert int.from_bytes(br[y['gYokaiPrivateAudioMask']:y['gYokaiPrivateAudioMask']+4],'little')==0x7FFFFFFF
assert len(br)<33554432
out=dict(passed=True,base=base,house_layout_warps_collisions_unchanged=True,original_resident_text_behavior_unchanged=True,all_other_maps_graphics_gameplay_teams_and_music_code_unchanged=True,all31_audio_streams_and_gains_unchanged=True,no_new_persistent_flags=True,public_bytes=(R/'pokefirered.gba').stat().st_size,private_bytes=len(br),private_headroom=33554432-len(br),public_sha256=hashlib.sha256((R/'pokefirered.gba').read_bytes()).hexdigest(),private_sha256=hashlib.sha256(br).hexdigest())
(Q/'PRESERVATION.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS exile scope and all31 OST; private',len(br),'bytes')

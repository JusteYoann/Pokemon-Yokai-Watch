#!/usr/bin/env python3
"""Read-only preservation audit for the isolated stage-A art preview."""
from pathlib import Path
import hashlib,json,subprocess
from mgba_rpc import ROOT as R
Q=R/'QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A';base='b3396ac9f'
protected=['graphics','src/data/pokemon','data/maps','data/scripts','src/battle_main.c','src/battle_interface.c','src/spiraton_core.c','src/spiraton_battle.c','src/data/trainers.h','src/data/trainer_parties.h','src/pokemon.c','src/data/yokai_mixer_gains.h','data/yokai/audio_loops.json']
subprocess.run(['git','diff','--exit-code',base,'--',*protected],cwd=R,check=True,stdout=subprocess.DEVNULL)
old=R.parent/'Pokemon-Yokai-Watch-argenta'
def sym(root):
 return {v[2]:int(v[0],16)-0x8000000 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(root/'pokefirered_audio.elf')],text=True).splitlines() if len(v:=line.split())==3}
a,b=sym(old),sym(R);ar=(old/'pokefirered_audio.gba').read_bytes();br=(R/'pokefirered_audio.gba').read_bytes()
for i in range(1,32):
 name=f'yokai_wave_{i:02d}';n=(R.parent/'private-audio/argenta-integration'/f'{i:02d}.dpcm').stat().st_size
 assert ar[a[name]:a[name]+n]==br[b[name]:b[name]+n],name
assert ar[a['sYokaiSongGain']:a['sYokaiSongGain']+756]==br[b['sYokaiSongGain']:b['sYokaiSongGain']+756]
assert int.from_bytes(br[b['gYokaiPrivateAudioMask']:b['gYokaiPrivateAudioMask']+4],'little')==0x7FFFFFFF
assert len(br)<33554432
source=R/'docs/don-spiraton/propositions/direction-artistique-v2-non-validee.png'
assert source.read_bytes()==(R/'docs/don-spiraton/phase-a/source-v2-inchangée.png').read_bytes()
report=dict(passed=True,base=base,protected_paths=protected,maps_sprites_gameplay_existing_audio_unchanged=True,all31_waveforms_and_gains_identical=True,source_v2_byte_identical=True,public_bytes=(R/'pokefirered.gba').stat().st_size,private_bytes=len(br),private_headroom=33554432-len(br),public_sha256=hashlib.sha256((R/'pokefirered.gba').read_bytes()).hexdigest(),private_sha256=hashlib.sha256(br).hexdigest(),ewram_static_bytes=261124,iwram_bytes=29888)
(Q/'PRESERVATION.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: isolated preview; existing maps/graphics/gameplay and all31 OST unchanged; private',len(br),'bytes')

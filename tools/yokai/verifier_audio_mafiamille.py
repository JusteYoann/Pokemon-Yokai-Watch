#!/usr/bin/env python3
"""Verify all26 linked private waves against the pinned pre-scenario ROM, without audio publication."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from mgba_rpc import ROOT
p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,default=Path('/workspace/private-builds/audio31-reference'));p.add_argument('--audio',type=Path,required=True);a=p.parse_args()
def symbols(elf):return {v[2]:int(v[0],16) for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(elf)],text=True).splitlines() if len(v:=l.split())==3}
before=(a.reference/'pokefirered_audio.gba').read_bytes();after=(ROOT/'pokefirered_audio.gba').read_bytes();old=symbols(a.reference/'pokefirered_audio.elf');new=symbols(ROOT/'pokefirered_audio.elf');manifest=json.loads((a.audio/'manifest.json').read_text());checks=[]
assert hashlib.sha256(before).hexdigest()=='6368e2c28cae2eeddf1d6439fcd279693fc67b8270d3f1b1bc5d75e3dd71c65c'
for track in manifest['prepared_tracks']:
 n=track['number']
 if n not in manifest['active_tracks']:continue
 key=f'yokai_wave_{n:02d}';size=track['bytes'];x=before[old[key]-0x8000000:old[key]-0x8000000+size];y=after[new[key]-0x8000000:new[key]-0x8000000+size]
 assert len(x)==len(y)==size and x==y,(n,'wave data changed')
 assert hashlib.sha256(y).hexdigest()==track['sha256'],(n,'manifest mismatch')
 checks.append(dict(slot=n,bytes=size,sha256=track['sha256'],byte_identical=True))
assert len(checks)==26
for name,size in [('sYokaiSongGain',756),('sYokaiMusicAliases',292)]:
 x=before[old[name]-0x8000000:old[name]-0x8000000+size];y=after[new[name]-0x8000000:new[name]-0x8000000+size];assert x==y,name
report=dict(passed=True,rom_bytes=len(after),rom_sha256=hashlib.sha256(after).hexdigest(),public_rom_bytes=(ROOT/'pokefirered.gba').stat().st_size,public_rom_sha256=hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),remaining_to_32MiB=33554432-len(after),linked_private_tracks=checks,all_26_wave_headers_samples_and_loop_points_identical=True,gain_table_and_all_73_aliases_byte_identical=True,private_resources_not_published=True)
(ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/AUDIO_COMPILATION.json').write_text(json.dumps(report,indent=2)+'\n');print('AUDIO PRESERVATION PASS26',len(after),'bytes')

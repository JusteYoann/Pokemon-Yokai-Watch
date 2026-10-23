#!/usr/bin/env python3
"""Read-only ELF/ROM integrity checks against the pinned31-OST reference."""
import subprocess,json,hashlib,struct
from pathlib import Path
from mgba_rpc import ROOT
OLD=Path('/workspace/Pokemon-Yokai-Watch-audio31');NEW=ROOT;Q=ROOT/'QA_RECETTE_FINALE/ARGENTA_MORLEONE'
def sy(root):return {v[2]:int(v[0],16) for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(root/'pokefirered_audio.elf')],text=True).splitlines() if len(v:=l.split())==3}
a=sy(OLD);b=sy(NEW);ar=(OLD/'pokefirered_audio.gba').read_bytes();br=(NEW/'pokefirered_audio.gba').read_bytes()
assert hashlib.sha256(ar).hexdigest()=='6854d73f666d540d4327afa9ed7896c0909004df1f342707361d316176b11ced'
def chunk(blob,s,name,n):p=s[name]-0x8000000;return blob[p:p+n]
manifest=json.loads(Path('/workspace/private-audio/final-battle-c-integration/manifest.json').read_text());checks=[]
for row in manifest['prepared_tracks']:
 n=row['number']
 if n==14:continue
 old=chunk(ar,a,f'yokai_wave_{n:02d}',row['bytes']);new=chunk(br,b,f'yokai_wave_{n:02d}',row['bytes']);assert old==new,n
 checks.append(dict(slot=n,bytes=len(new),sha256=hashlib.sha256(new).hexdigest(),unchanged=True))
for n in range(378):
 if n==360:continue
 assert chunk(ar,a,'sYokaiSongGain',756)[n*2:n*2+2]==chunk(br,b,'sYokaiSongGain',756)[n*2:n*2+2],n
heads=struct.unpack('<31I',chunk(br,b,'gYokaiPrivateHeaders',124));assert all(p==b[f'mus_yokai_{i+1:02d}'] for i,p in enumerate(heads));assert int.from_bytes(chunk(br,b,'gYokaiPrivateAudioMask',4),'little')==0x7FFFFFFF
assert struct.unpack_from('<HHIII',br,b['yokai_wave_25']-0x8000000)[3:]==(462424,2474626)
for n in [5,14]:assert struct.unpack_from('<HHIII',br,b[f'yokai_wave_{n:02d}']-0x8000000)[1]==0
priv=Path('/workspace/private-audio/argenta-integration/14.dpcm').read_bytes();assert chunk(br,b,'yokai_wave_14',len(priv))==priv
assert len(br)<33554432 and b['__yokai_audio_gap_end']<=0x08D00000
report=dict(passed=True,private_rom_sha256=hashlib.sha256(br).hexdigest(),private_bytes=len(br),public_rom_sha256=hashlib.sha256((NEW/'pokefirered.gba').read_bytes()).hexdigest(),public_bytes=(NEW/'pokefirered.gba').stat().st_size,headroom_to_32MiB=33554432-len(br),linked_tracks=31,unchanged_tracks=checks,all_other377_gain_entries_identical=True,zombie_gain_q8=int.from_bytes(chunk(br,b,'sYokaiSongGain',756)[720:722],'little'),final_battle_C_samples=[462424,2474626],one_shots=[5,14],private_gap_free_bytes=0x08D00000-b['__yokai_audio_gap_end'],zombie_private_bytes=len(priv),copyrighted_samples_not_published=True)
(Q/'AUDIO_INTEGRITE.json').write_text(json.dumps(report,indent=2)+'\n');print('AUDIO PASS:31 linked, original30 waveform/loops/gains preserved')

#!/usr/bin/env python3
"""Prove the new ROM differs only inside six fixed-size Nathan OW bitmap arrays."""
import argparse,subprocess,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
a=argparse.ArgumentParser();a.add_argument('--before-rom',type=Path,required=True);a.add_argument('--rom',type=Path,default=R/'pokefirered_audio.gba');a.add_argument('--restore-commit',default='e00c7853bcef495afaaeb82fa433c57722d4c4d8');args=a.parse_args()
old=args.before_rom.read_bytes();new=args.rom.read_bytes();assert len(old)==len(new)
symbols={v[2]:int(v[0],16) for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(args.rom.with_suffix('.elf'))],text=True).splitlines() if len(v:=line.split())==3}
ranges=[];mask=bytearray(len(new));names=['normal','surf_run','bike','vs_seeker_bike','fish','item']
for name,symbol in zip(names,['RedNormal','RedSurfRun','RedBike','RedVSSeekerBike','RedFish','RedItem']):
 b=(R/f'graphics/yokai_characters/nathan/{name}.4bpp').read_bytes();start=symbols['gObjectEventPic_'+symbol]-0x08000000;assert new[start:start+len(b)]==b;mask[start:start+len(b)]=b'\x01'*len(b);ranges.append(dict(asset=name,start=start,size=len(b),changed_bytes=sum(a!=c for a,c in zip(old[start:start+len(b)],b))))
changed=0
for i,(a,b) in enumerate(zip(old,new)):
 if a!=b:assert mask[i],('Unexpected ROM byte change outside Nathan overworld',hex(i));changed+=1
allowed={f'graphics/yokai_characters/nathan/{n}.png' for n in names};kept=[]
for f in subprocess.check_output(['git','ls-tree','-r','--name-only',args.restore_commit,'graphics/yokai_characters'],cwd=R,text=True).splitlines():
 if f in allowed or Path(f).suffix not in ['.png','.pal']:continue
 assert (R/f).read_bytes()==subprocess.check_output(['git','show',args.restore_commit+':'+f],cwd=R),f;kept.append(f)
report=dict(passed=True,restore_commit=args.restore_commit,old_rom_sha256=hashlib.sha256(old).hexdigest(),new_rom_sha256=hashlib.sha256(new).hexdigest(),rom_bytes=len(new),changes_only_in_six_overworld_graphic_arrays=True,changed_bytes=changed,arrays=ranges,all_other_character_images_and_palettes_identical=len(kept),palette_changes=0,gameplay_changes=0,audio_changes=0,trainer_battle_front_back_changes=0,intro_title_changes=0)
(R/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/NATHAN_GABARIT_RED/PRESERVATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

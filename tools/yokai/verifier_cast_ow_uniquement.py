#!/usr/bin/env python3
"""Byte-level proof that the FRLG cast remake changes only OW pixels/flip commands."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/CAST_GABARIT_FRLG'
p=argparse.ArgumentParser();p.add_argument('--before-rom',type=Path,required=True);p.add_argument('--rom',type=Path,default=R/'pokefirered_audio.gba');args=p.parse_args()
commit='2e95fcfb9bb89759bdc1776307055d49a9da3cd5'
def symbols(elf):
 out={}
 for line in subprocess.check_output(['arm-none-eabi-nm','-S','--defined-only',str(elf)],text=True).splitlines():
  v=line.split()
  if len(v)==4:out[v[3]]=(int(v[0],16)-0x08000000,int(v[1],16))
 return out
old=args.before_rom.read_bytes();new=args.rom.read_bytes();assert len(old)==len(new)<=32*1024*1024
before=symbols(args.before_rom.with_suffix('.elf'));after=symbols(args.rom.with_suffix('.elf'))
actors={'ariane':'Ariane','enma':'YokaiEnma','nathaniel':'YokaiNathaniel','michael':'YokaiMichael','wyatt':'YokaiWyatt','don_morleone':'YokaiDonMorleone','mafiamille_1':'YokaiMafiamille1','mafiamille_2':'YokaiMafiamille2','mafiamille_3':'YokaiMafiamille3','employe_rouge':'YokaiEmployeRouge','employe_bleu':'YokaiEmployeBleu','domniscian':'YokaiDomniscian','matt':'Blue'}
assets={f'graphics/yokai_characters/{actor}/overworld.png':'gObjectEventPic_'+symbol for actor,symbol in actors.items()}
for asset,symbol in [('normal','Normal'),('surf_run','SurfRun'),('bike','Bike'),('vs_seeker_bike','VSSeekerBike'),('fish','Fish'),('item','Item')]:assets[f'graphics/yokai_characters/katie/{asset}.png']='gObjectEventPic_Green'+symbol
mask=bytearray(len(new));ranges=[]
def allow(name,kind):
 assert before[name]==after[name],('Moved/resized symbol',name,before[name],after[name])
 start,size=after[name];assert 0<=start<start+size<=len(new);mask[start:start+size]=b'\x01'*size
 ranges.append(dict(symbol=name,type=kind,offset=start,size=size,changed_bytes=sum(a!=b for a,b in zip(old[start:start+size],new[start:start+size]))))
for path,name in assets.items():
 allow(name,'overworld_bitmap');start,size=after[name];raw=(R/path).with_suffix('.4bpp').read_bytes();assert len(raw)==size and raw==new[start:start+size],path
for name in after:
 if re.match(r'^sAnim_MattGo',name) or re.match(r'^sAnim_.*_Katie(Normal|Bike|Fish)$',name):
  allow(name,'visual_flip_commands');start,size=after[name]
  for a,b in zip(old[start:start+size],new[start:start+size]):assert a==b or a^b==64,('Non-flip animation change',name,a,b)
changed=0
for i,(a,b) in enumerate(zip(old,new)):
 if a!=b:assert mask[i],('ROM change outside allowed OW arrays',hex(i));changed+=1
kept=[]
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'graphics'],cwd=R,text=True).splitlines():
 if path in assets or Path(path).suffix not in ['.png','.pal']:continue
 current=(R/path).read_bytes();original=subprocess.check_output(['git','show',commit+':'+path],cwd=R)
 # Git explicitly checks out JASC palettes CRLF; compare their identical
 # canonical text to the LF Git blob, not checkout newline conversion.
 if Path(path).suffix=='.pal':current=current.replace(b'\r\n',b'\n');original=original.replace(b'\r\n',b'\n')
 assert current==original,('Unexpected graphic change',path);kept.append(path)
report=dict(passed=True,restore_commit=commit,old_rom_sha256=hashlib.sha256(old).hexdigest(),new_rom_sha256=hashlib.sha256(new).hexdigest(),rom_bytes=len(new),changed_bytes=changed,changes_confined_to_overworld_bitmaps_and_hflip_commands=True,all_other_graphics_and_palettes_identical=len(kept),palettes_changed=0,gameplay_changes=0,audio_changes=0,battle_portrait_changes=0,intro_title_changes=0,nathan_changes=0,arrays=ranges)
(Q/'PRESERVATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

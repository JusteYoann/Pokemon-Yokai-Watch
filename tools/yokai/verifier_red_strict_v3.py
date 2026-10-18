#!/usr/bin/env python3
"""Prove only thirteen OW bitmap arrays changed; all other ROM bytes preserved."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/RED_STRICT_V3';D=R/'graphics/yokai_characters'
p=argparse.ArgumentParser();p.add_argument('--before-rom',type=Path,required=True);a=p.parse_args();rom=R/'pokefirered_audio.gba';commit='daff2e5b824c4e76dc89270820a0574ffc15f3ae'
def symbols(elf):
 out={}
 for line in subprocess.check_output(['arm-none-eabi-nm','-S','--defined-only',str(elf)],text=True).splitlines():
  v=line.split()
  if len(v)==4:out[v[3]]=(int(v[0],16)-0x08000000,int(v[1],16))
 return out
old=a.before_rom.read_bytes();new=rom.read_bytes();assert len(old)==len(new)<=30*1048576
before=symbols(a.before_rom.with_suffix('.elf'));after=symbols(rom.with_suffix('.elf'));mask=bytearray(len(new));arrays=[]
actors={'ariane':'Ariane','enma':'YokaiEnma','nathaniel':'YokaiNathaniel','michael':'YokaiMichael','wyatt':'YokaiWyatt','don_morleone':'YokaiDonMorleone','mafiamille_1':'YokaiMafiamille1','mafiamille_2':'YokaiMafiamille2','mafiamille_3':'YokaiMafiamille3','employe_rouge':'YokaiEmployeRouge','employe_bleu':'YokaiEmployeBleu','domniscian':'YokaiDomniscian','matt':'Blue'}
for actor,suffix in actors.items():
 name='gObjectEventPic_'+suffix;assert before[name]==after[name];start,size=after[name];raw=(D/actor/'overworld.4bpp').read_bytes();assert len(raw)==size and new[start:start+size]==raw
 mask[start:start+size]=b'\x01'*size;arrays.append(dict(actor=actor,symbol=name,offset=start,size=size,changed_bytes=sum(x!=y for x,y in zip(old[start:start+size],raw))))
changed=0
for i,(x,y) in enumerate(zip(old,new)):
 if x!=y:assert mask[i],('Changed byte outside13 OW arrays',hex(i));changed+=1
allowed={f'graphics/yokai_characters/{n}/overworld.png' for n in actors};kept=[]
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'graphics'],cwd=R,text=True).splitlines():
 if path in allowed or Path(path).suffix not in ['.png','.pal']:continue
 x=(R/path).read_bytes();y=subprocess.check_output(['git','show',commit+':'+path],cwd=R)
 if path.endswith('.pal'):x=x.replace(b'\r\n',b'\n');y=y.replace(b'\r\n',b'\n')
 assert x==y,path;kept.append(path)
assert (D/'mafiamille_1/overworld.png').read_bytes()==(D/'mafiamille_2/overworld.png').read_bytes()==(D/'mafiamille_3/overworld.png').read_bytes()
red=np.asarray(Image.open(D/'employe_rouge/overworld.png'));blue=np.asarray(Image.open(D/'employe_bleu/overworld.png'));assert np.array_equal(red>0,blue>0) and not np.array_equal(red,blue)
portraits={n:hashlib.sha256((D/n/'battle.png').read_bytes()).hexdigest() for n in ['mafiamille_1','mafiamille_2','mafiamille_3','employe_rouge','employe_bleu']};assert len(set(portraits.values()))==5
report=dict(passed=True,restore_commit=commit,old_rom_sha256=hashlib.sha256(old).hexdigest(),new_rom_sha256=hashlib.sha256(new).hexdigest(),rom_bytes=len(new),changed_bytes=changed,changes_confined_to13_OW_bitmap_arrays=True,other_graphics_and_palettes_identical=len(kept),palettes_changed=0,animation_commands_changed=0,audio_changes=0,gameplay_changes=0,battle_art_changes=0,nathan_and_katie_changes=0,mafia_map_pngs_byte_identical=True,employee_map_alpha_identical=True,employee_suit_colors_different=True,distinct_unchanged_battle_portraits=portraits,arrays=arrays)
(Q/'PRESERVATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

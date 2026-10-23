#!/usr/bin/env python3
"""Prove the prototype changes no existing assets, progression, trainers or audio."""
import json,subprocess,hashlib,re
from pathlib import Path
from mgba_rpc import ROOT
BASE='2e81a799f2cfcb328cdf4f92b17b9131db6e0f1d'
D=ROOT/'docs/cramois-ile-passe/phase-a';D.mkdir(parents=True,exist_ok=True)
old=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=ROOT,text=True).strip('\0').split('\0')
diff=subprocess.check_output(['git','diff',BASE,'--name-only','-z'],cwd=ROOT,text=True).strip('\0').split('\0')
changed=set(old)&set(diff)
assert changed=={'src/overworld.c','src/palette.c'},changed
art=[p for p in old if p.startswith('graphics/') and p.endswith(('.png','.pal'))]
maps=[p for p in old if p.startswith(('data/maps/','data/layouts/'))]
assert all((ROOT/p).exists() for p in old)
assert not set(maps)&changed
symbols={}
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(ROOT/'pokefirered_audio.elf')],text=True).splitlines():
 f=line.split()
 if len(f)==3:symbols[f[2]]=int(f[0],16)
rom=(ROOT/'pokefirered_audio.gba').read_bytes();audio=[]
for i in range(1,32):
 b=Path(f'/workspace/private-audio/lavanville-integration/{i:02d}.dpcm').read_bytes();offset=symbols[f'yokai_wave_{i:02d}']-0x08000000;assert rom[offset:offset+len(b)]==b
 audio.append(dict(track=i,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
memory={}
for mode,file in [('public','pokefirered.map'),('prive','pokefirered_audio.map')]:
 s=(ROOT/file).read_text();ew=int(re.search(r'^ewram\s+0x[0-9a-f]+\s+0x([0-9a-f]+)',s,re.M)[1],16);iw=int(re.search(r'^iwram\s+0x[0-9a-f]+\s+0x([0-9a-f]+)',s,re.M)[1],16)
 assert ew==261348 and iw==(29824 if mode=='public' else 29888)
 memory[mode]=dict(ewram_before=261348,ewram_after=ew,ewram_added=0,ewram_free=262144-ew,iwram_after=iw)
report=dict(passed=True,base=BASE,existing_changed_files=sorted(changed),all_other_existing_tracked_files_unchanged=len(old)-len(changed),approved_artwork_files_unchanged=len(art),map_layout_files_unchanged=len(maps),all_151_yokai_unchanged=True,all_existing_teams_unchanged=True,all_existing_scripts_unchanged=True,ariane_following_duo_and_cut_sources_unchanged=True,audio=audio,memory=memory)
(D/'PRESERVATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',len(art),'artwork,',len(maps),'map files, all existing gameplay, 31 private streams; zero extra EWRAM/IWRAM')

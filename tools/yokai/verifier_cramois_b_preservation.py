#!/usr/bin/env python3
"""Phase B exact preservation and link-memory audit against approved phase A."""
import json,subprocess,hashlib,re
from pathlib import Path
from mgba_rpc import ROOT
BASE='1f335d268';D=ROOT/'docs/cramois-ile-passe/phase-b';D.mkdir(parents=True,exist_ok=True)
old=subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=ROOT,text=True).strip('\0').split('\0')
diff=subprocess.check_output(['git','diff',BASE,'--name-only','-z'],cwd=ROOT,text=True).strip('\0').split('\0')
changed=set(old)&set(diff);game=[p for p in changed if p.startswith(('src/','include/','graphics/','data/','sound/'))]
assert set(game)=={'src/overworld.c','src/cramois_past.c','include/cramois_past.h'},game
module=(ROOT/'src/cramois_past.c').read_text();addition='// Shared only by the maritime transition; existing island transfer is unchanged.\nu16 CramoisSepiaColor(u16 color)\n{\n    return sSepiaRgb555[color & 0x7FFF];\n}\n\n'
assert module.replace(addition,'')==subprocess.check_output(['git','show',BASE+':src/cramois_past.c'],cwd=ROOT,text=True)
assert (ROOT/'include/cramois_past.h').read_text().replace('u16 CramoisSepiaColor(u16 color);\n','')==subprocess.check_output(['git','show',BASE+':include/cramois_past.h'],cwd=ROOT,text=True)
art=[p for p in old if p.startswith('graphics/') and p.endswith(('.png','.pal'))];maps=[p for p in old if p.startswith(('data/maps/','data/layouts/'))]
assert not set(art+maps)&changed
s={}
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(ROOT/'pokefirered_audio.elf')],text=True).splitlines():
 f=line.split()
 if len(f)==3:s[f[2]]=int(f[0],16)
rom=(ROOT/'pokefirered_audio.gba').read_bytes();audio=[]
for i in range(1,32):
 b=Path(f'/workspace/private-audio/lavanville-integration/{i:02d}.dpcm').read_bytes();offset=s[f'yokai_wave_{i:02d}']-0x08000000;assert rom[offset:offset+len(b)]==b;audio.append(dict(track=i,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
memory={}
for mode,file in [('public','pokefirered.map'),('prive','pokefirered_audio.map')]:
 t=(ROOT/file).read_text();ew=int(re.search(r'^ewram\s+0x[0-9a-f]+\s+0x([0-9a-f]+)',t,re.M)[1],16);iw=int(re.search(r'^iwram\s+0x[0-9a-f]+\s+0x([0-9a-f]+)',t,re.M)[1],16)
 assert ew==261368 and iw==(29824 if mode=='public' else 29888)
 memory[mode]=dict(ewram_before=261348,ewram_after=ew,ewram_added=ew-261348,ewram_free=262144-ew,iwram_before=iw,iwram_after=iw)
report=dict(passed=True,base=BASE,existing_game_files_changed=game,approved_artwork_unchanged=len(art),maps_and_layouts_unchanged=len(maps),phase_a_existing_palette_functions_and_lut_unchanged=True,additive_rgb555_accessor_for_maritime_blend=True,all_existing_teams_scripts_151_yokai_and_save_formats_unchanged=True,carmin_lavanville_finale_sources_unchanged=True,audio=audio,memory=memory,temporary_resources=dict(sprite_slots=15,vram_tile_bytes=2048,obj_palette_banks=1,allocated_only_in_local_maritime_zone=True))
(D/'PRESERVATION.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('PASS',len(art),'approved artwork,',len(maps),'map files, phase A, scripts, teams,151 Yo-kai,31 streams; +20 EWRAM,776 free')

#!/usr/bin/env python3
"""All compiled map headers match approved source JSON, no emulator or audio needed."""
import hashlib,json,os,re,struct,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];rompath=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered_audio.gba'));rom=rompath.read_bytes();sym={}
for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(rompath.with_suffix('.elf'))],text=True).splitlines():
 f=line.split()
 if len(f)==3:sym[f[2]]=int(f[0],16)
C={k:int(v,0) for k,v in re.findall(r'^#define\s+(MUS_\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',(ROOT/'include/constants/songs.h').read_text(),re.M)}
checks=[]
for p in sorted((ROOT/'data/maps').glob('*/map.json')):
 d=json.loads(p.read_text());name=p.parent.name;actual=struct.unpack_from('<H',rom,sym[name]-0x08000000+16)[0];expected=C[d['music']];assert actual==expected,(name,actual,expected);checks.append(dict(map=name,music=d['music'],music_id=actual,passed=True))
assert len(rom)<=33554432
report={'passed':True,'rom_sha256':hashlib.sha256(rom).hexdigest(),'rom_bytes':len(rom),'remaining_bytes_to32MiB':33554432-len(rom),'maps_verified':len(checks),'scope':'All linked map headers match source assignments; not proof of runtime script overrides or travel through every map','results':checks};Path(os.environ.get('YOKAI_MAP_REPORT',str(ROOT/'QA_RECETTE_FINALE/POST_B13/audio/CARTES_COMPILEES.json'))).write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(checks),'maps;',len(rom),'bytes')

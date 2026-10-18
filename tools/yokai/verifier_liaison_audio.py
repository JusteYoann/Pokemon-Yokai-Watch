#!/usr/bin/env python3
"""Verify public native fallbacks and every actual private sample in the linked ROM."""
import hashlib,json,re,struct,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(name):
 path=ROOT/(name+'.gba');rom=path.read_bytes();symbols={}
 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(path.with_suffix('.elf'))],text=True).splitlines():
  f=line.split()
  if len(f)==3:symbols[f[2]]=int(f[0],16)
 return rom,symbols
results=[];public,ps=load('pokefirered');private,ss=load('pokefirered_audio')
assert len(public)<=33554432 and len(private)<=33554432
fallback={1:'mus_cycling',2:'mus_vs_trainer',4:'mus_poke_tower',6:'mus_vs_trainer',7:'mus_pallet',8:'mus_pallet',11:'mus_silph',12:'mus_celadon',14:'mus_viridian_forest',15:'mus_vs_gym_leader',16:'mus_sevii_123',17:'mus_rocket_hideout',20:'mus_vs_trainer',21:'mus_vermillion',22:'mus_celadon',23:'mus_mt_moon',24:'mus_mt_moon',25:'mus_vs_champion',26:'mus_slow_pallet'}
for number,symbol in fallback.items():
 address=struct.unpack_from('<I',public,ps['gSongTable']-0x08000000+(346+number)*8)[0];assert address==ps[symbol],(number,symbol,hex(address))
 results.append({'test':'Exact public native fallback','number':number,'symbol':symbol,'passed':True})
config=json.loads((ROOT/'data/yokai/audio_loops.json').read_text());active=config['active_tracks'];mask=struct.unpack_from('<I',private,ss['gYokaiPrivateAudioMask']-0x08000000)[0];assert mask==sum(1<<(n-1) for n in active)
# Metadata fixes the expected encoded hashes; no protected audio need be read here.
import os
manifest=json.loads((Path(os.environ['YOKAI_AUDIO_DIR'])/'manifest.json').read_text());rows={r['number']:r for r in manifest['prepared_tracks']}
for number in range(1,config.get('slot_count',20)+1):
 ptr=struct.unpack_from('<I',private,ss['gYokaiPrivateHeaders']-0x08000000+(number-1)*4)[0]
 if number not in active:assert ptr==0;continue
 assert ptr==ss[f'mus_yokai_{number:02d}']
 start=ss[f'yokai_wave_{number:02d}']-0x08000000;data=private[start:start+rows[number]['bytes']];assert hashlib.sha256(data).hexdigest()==rows[number]['sha256']
 kind,flags,freq,loop,size=struct.unpack_from('<HHIII',data);assert kind==1 and flags==0x4000 and freq==13379*1024 and 0<=loop<size
 voice=struct.unpack_from('<I',private,ptr-0x08000000+4)[0];assert private[voice-0x08000000]==0x28
 results.append({'test':'Private sample byte-identical, bounded loop and correct native compression bit','number':number,'bytes':len(data),'passed':True})
report={'passed':True,'public_rom_sha256':hashlib.sha256(public).hexdigest(),'private_rom_sha256':hashlib.sha256(private).hexdigest(),'private_rom_bytes':len(private),'private_audio_mask':mask,'active_tracks':active,'remaining_bytes_to32MiB':33554432-len(private),'results':results}
(ROOT/'QA_RECETTE_FINALE/INTEGRATION_MUSIQUES/VERIFICATION_LIAISON.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

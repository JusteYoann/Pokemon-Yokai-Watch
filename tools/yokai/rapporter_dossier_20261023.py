#!/usr/bin/env python3
"""Build inventory and real allocated ROM/RAM accounting for both outputs."""
from pathlib import Path
import subprocess,re,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/dossier-20261023';baseline=json.loads((D/'baseline.json').read_text());results={}
def sections(s):return {m[1]:(int(m[2]),int(m[3])) for m in re.finditer(r'^([.\w]+)\s+(\d+)\s+(\d+)\s*$',s,re.M)}
for rom in ['pokefirered','pokefirered_audio']:
 raw=subprocess.check_output(['arm-none-eabi-size','-A',str(R/(rom+'.elf'))],text=True);sec=sections(raw);old=sections(baseline[rom]['sections']);used=sum(n for n,a in sec.values() if 0x08000000<=a<0x0A000000);before=sum(n for n,a in old.values() if 0x08000000<=a<0x0A000000)
 symbols=subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(R/(rom+'.elf'))],text=True)
 results[rom]={'file_bytes':(R/(rom+'.gba')).stat().st_size,'baseline_file_bytes':baseline[rom]['file_bytes'],'rom_allocated_sections_bytes':used,'baseline_rom_allocated_sections_bytes':before,'net_allocated_rom_gain_bytes':before-used,'audio_sequence_gain_bytes':old['song_data'][0]-sec['song_data'][0],'ewram_bytes':sec['ewram'][0],'ewram_free_bytes':256*1024-sec['ewram'][0],'iwram_bytes':sec['iwram'][0],'iwram_free_bytes':32768-sec['iwram'][0],'rom_highest_end_offset':max(a+n-0x08000000 for n,a in sec.values() if 0x08000000<=a<0x0A000000),'sha256':hashlib.sha256((R/(rom+'.gba')).read_bytes()).hexdigest(),'sections':{k:{'bytes':n,'address':hex(a)} for k,(n,a) in sec.items()}}
 print(rom,json.dumps({k:v for k,v in results[rom].items() if k!='sections'}))
(D/'ROM_RAM.json').write_text(json.dumps(results,indent=2)+'\n')
audit=json.loads((D/'audio-audit.json').read_text());retired={r['symbol'] for r in audit['sequences']};protected=set(audit['retained_public_fallbacks'])
# Conservative full inventory: shared banks/sample data are retained, including unproven future use.
references={}
for folder in ['data/maps','data/scripts','data/text','src']:
 for p in (R/folder).rglob('*'):
  if p.suffix in ['.c','.h','.inc','.json']:
   for token in set(re.findall(r'\bMUS_\w+\b',p.read_text(errors='replace'))):references.setdefault(token,[]).append(str(p.relative_to(R)))
constants={int(v):k for k,v in re.findall(r'^#define\s+(MUS_\w+)\s+(\d+)\b',(R/'include/constants/songs.h').read_text(),re.M)}
rows=re.findall(r'^\s*song\s+(\w+),\s*(\d+),\s*(\d+)([^\n]*)',(R/'sound/song_table.inc').read_text(),re.M);seq=[]
for i,(symbol,ms,me,comment) in enumerate(rows):
 if i not in constants:continue
 original=next((v['symbol'] for v in audit['sequences'] if v['id']==i),symbol)
 seq.append({'id':i,'constant':constants[i],'compiled_header':symbol,'original_sequence':original,'status':'unreachable native sequence excluded' if original in retired else 'retained public fallback / reserved / functional cue','token_reference_paths':references.get(constants[i],[])})
banks={}
for name,body in re.findall(r'^(voicegroup\d+)::\n(.*?)(?=^voicegroup\d+::|\Z)',(R/'sound/voice_groups.inc').read_text(),re.M|re.S):banks[name]={'status':'retained shared/reserved bank','nested_banks':sorted(set(re.findall(r'\bvoicegroup\d+\b',body))),'samples':sorted(set(re.findall(r'\bDirectSoundWaveData_\w+\b',body)))}
samples={}
for symbol,path in re.findall(r'^(DirectSoundWaveData_\w+)::\n\s*\.incbin "([^"]+)"',(R/'sound/direct_sound_data.inc').read_text(),re.M):samples[symbol]={'path':path,'status':'retained shared/reserved sample','bytes':(R/path).stat().st_size if (R/path).exists() else None}
private={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'external private sample retained; not committed'} for p in Path('/workspace/private-audio/lavanville-integration').glob('*.dpcm')}
(D/'audio-inventaire-complet.json').write_text(json.dumps({'native_music_slots':seq,'voicegroups':banks,'direct_sound_samples':samples,'private_samples':private,'deleted_private_samples':[],'deleted_shared_samples':[],'notes':'Only54 provably bypassed native sequence objects excluded; sources retained. All banks, sample tables, functional jingles, cries, programmable wave data and31 private OST retained. No claim that reserved unused banks can safely be deleted.'},ensure_ascii=False,indent=2)+'\n')
# Private sample payloads match baseline ROM bytes at each relocated wave symbol.
def sym(elf):return {v[2]:int(v[0],16) for l in subprocess.check_output(['arm-none-eabi-nm','--defined-only',elf],text=True).splitlines() if len(v:=l.split())==3}
oldroot=Path('/workspace/Pokemon-Yokai-Watch-philosovni');before=(oldroot/'pokefirered_audio.gba').read_bytes();after=(R/'pokefirered_audio.gba').read_bytes();osym=sym(str(oldroot/'pokefirered_audio.elf'));nsym=sym(str(R/'pokefirered_audio.elf'));checks=[]
for n in range(1,32):
 p=Path(f'/workspace/private-audio/lavanville-integration/{n:02}.dpcm');length=p.stat().st_size;name=f'yokai_wave_{n:02}';a=osym[name]-0x08000000;b=nsym[name]-0x08000000;assert before[a:a+length]==after[b:b+length],name;checks.append({'slot':n,'bytes':length,'identical_payload_to_base':True})
(D/'AUDIO_PRIVE_PRESERVE.json').write_text(json.dumps({'passed':True,'tracks':checks},indent=2)+'\n')

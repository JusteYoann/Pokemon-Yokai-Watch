#!/usr/bin/env python3
"""Read all 151 linked catch rates in mGBA; compare the entire table to baseline.
No savedata or game RAM writes. This is not a simulated full playthrough.
"""
import argparse,hashlib,json,math,subprocess
from pathlib import Path
from mgba_rpc import Emulator,ROOT
from appliquer_capture_rangs import capture_rules,apply_capture_rates,SOURCE
class ReadOnly(Emulator):
 def assemble_stub(self):pass
 def write(self,*a,**k):raise RuntimeError('No RAM writes')
 def call(self,*a,**k):raise RuntimeError('No injected game calls')

def symbol(elf):
 for line in subprocess.check_output(['arm-none-eabi-nm','-S','--defined-only',str(elf)],text=True).splitlines():
  f=line.split()
  if len(f)==4 and f[3]=='gSpeciesInfo':return int(f[0],16),int(f[1],16)
 raise AssertionError('Species table missing')

def probability(rate,hp,maxhp=100,ball=10,status='normal'):
 odds=(rate*ball//10)*(3*maxhp-2*hp)//(3*maxhp)
 if status in ('sommeil','gel'):odds*=2
 elif status in ('paralysie','poison','brulure'):odds=odds*15//10
 if odds>254:return 1.0
 threshold=1048560//math.isqrt(math.isqrt(16711680//odds))
 return min(threshold,65536)**4/65536**4

args=argparse.ArgumentParser();args.add_argument('--reference-rom',type=Path,required=True);args.add_argument('--reference-elf',type=Path,required=True);args.add_argument('--output',type=Path,required=True);args=args.parse_args()
assert apply_capture_rates(SOURCE.read_text())==SOURCE.read_text()
r=ReadOnly();rules=capture_rules()
try:
 address,size=symbol(r.elf_path);oldaddr,oldsize=symbol(args.reference_elf)
 assert size==oldsize and size%412==0
 stride=size//412;assert stride==28
 before=args.reference_rom.read_bytes()[oldaddr-0x08000000:oldaddr-0x08000000+size]
 after=r.read(address,size);assert len(before)==len(after)==size
 allowed={28*v['numero']+8 for v in rules.values()}
 differences=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
 assert set(differences)<=allowed,'Another species field changed'
 entries=[]
 for constant,v in rules.items():
  assert after[28*v['numero']+8]==v['taux'],constant
  assert probability(v['taux'],1)>=probability(v['taux'],100)
  assert probability(v['taux'],1,status='sommeil')>=probability(v['taux'],1)
  assert probability(v['taux'],100,ball=20)>=probability(v['taux'],100)
  entries.append(dict(**v,indice_charge=after[28*v['numero']+8]))
 assert probability(255,1,status='sommeil')==1
 ordered=[255,225,180,120,75,60,45,30]
 # Native integer square roots quantize some full-health probabilities.
 assert all(probability(a,hp)>=probability(b,hp) for a,b in zip(ordered,ordered[1:]) for hp in (100,75,50,25,1))
 assert all(any(probability(a,hp)>probability(b,hp) for hp in (100,75,50,25,1)) for a,b in zip(ordered,ordered[1:]))
 result=dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_size=len(r.rom_buffer.raw)-1,native_entries_checked=151,catch_rates_changed=len(differences),other_table_bytes_unchanged=True,reference_sha256=hashlib.sha256(args.reference_rom.read_bytes()).hexdigest(),
             captures_non_jouees=True,indices_not_percentages=True,entries=entries)
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('PASS 151 linked rates in mGBA;',len(differences),'catch rates changed; all other table bytes unchanged')
finally:r.close()

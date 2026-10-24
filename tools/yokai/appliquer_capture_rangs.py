#!/usr/bin/env python3
"""Apply native catch-rate indices from the validated Yo-kai ranks, only 1..151."""
import argparse,csv,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
POLICY=ROOT/'data/yokai/capture_rangs.json'
SOURCE=ROOT/'src/data/pokemon/species_info.h'
BASE='dd6a66c4dba0da61cb32abc6f1a592a048914c77'
VANILLA='ab417d12552b25c8434592a942006cc0219932bf'
BLOCK=re.compile(r'^    \[(SPECIES_\w+)\] =\n    \{\n(.*?)^    \},',re.M|re.S)
RATE=re.compile(r'(\.catchRate\s*=\s*)(\d+)')

def capture_rules():
 policy=json.loads(POLICY.read_text())
 with (ROOT/policy['source_rangs']).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
 assert len(rows)==151 and sorted(int(v['species_id']) for v in rows)==list(range(1,152))
 result={}
 for row in rows:
  rate=policy['taux_par_rang'][row['rang']];assert 1<=rate<=255
  assert row['species_constant'] not in result
  result[row['species_constant']]=dict(numero=int(row['species_id']),nom=row['nom_yokai'],rang=row['rang'],taux=rate)
 return result

def rates(text):
 return {m[1]:int(RATE.search(m[2])[2]) for m in BLOCK.finditer(text) if RATE.search(m[2])}

def apply_capture_rates(text):
 rules=capture_rules();seen=set()
 def replace(m):
  if m[1] not in rules:return m[0]
  seen.add(m[1]);out,count=RATE.subn(lambda v:v[1]+str(rules[m[1]]['taux']),m[0]);assert count==1,m[1]
  return out
 out=BLOCK.sub(replace,text);assert seen==set(rules)
 return out

def original(commit):
 return subprocess.check_output(['git','show',commit+':src/data/pokemon/species_info.h'],cwd=ROOT,text=True)

def audit(text):
 rules=capture_rules();before=rates(original(BASE));vanilla=rates(original(VANILLA));after=rates(text)
 assert all(before[c]==vanilla[c] for c in rules)
 # Reversible masking proves that every other field/entry is byte-for-byte intact.
 baseline=original(BASE)
 assert apply_capture_rates(baseline)==text,'Unrelated species-data change'
 return dict(source_avant=BASE,source_rouge_feu=VANILLA,anciens_taux_identiques_rouge_feu=151,
             taux_modifies=sum(before[c]!=after[c] for c in rules),
             yokai=[dict(constante=c,**v,ancien_taux=before[c]) for c,v in rules.items()])

def main():
 args=argparse.ArgumentParser();args.add_argument('--check',action='store_true');check=args.parse_args().check
 old=SOURCE.read_text();new=apply_capture_rates(old);report=audit(new)
 if check:assert old==new,'Catch rates need updating'
 else:
  SOURCE.write_text(new)
  folder=ROOT/'docs/capture-rangs-20261024';folder.mkdir(parents=True,exist_ok=True)
  (folder/'AUDIT_151.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('PASS 151 ranks;',report['taux_modifies'],'rates changed; unrelated fields preserved')
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Audit des espèces exposées; --apply convertit les reliquats non-151 avec preuve explicite."""
import argparse,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=R/'docs/postgame-quetes-20261025';P.mkdir(exist_ok=True)
ids={a:int(b) for a,b in re.findall(r'#define\s+(SPECIES_\w+)\s+(\d+)',(R/'include/constants/species.h').read_text())}
roster=json.loads((R/'docs/capture-rangs-20261024/AUDIT_151.json').read_text())['yokai'];names={r['constante']:r['nom'] for r in roster};legal=set(names)
display={a:b for a,b in re.findall(r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]+)"\)',(R/'src/data/text/species_names.h').read_text())}
info={}
for species,body in re.findall(r'\[(SPECIES_\w+)\]\s*=\s*\{\s*\n(.*?)\n    \}',(R/'src/data/pokemon/species_info.h').read_text(),re.S):
 t=re.search(r'\.types = \{(\w+), (\w+)\}',body);stats=re.findall(r'\.base(?:HP|Attack|Defense|Speed|SpAttack|SpDefense) = (\d+)',body)
 if t and len(stats)==6:info[species]=(set(t.groups()),sum(map(int,stats)))
def replacement(species):
 t,bst=info.get(species,({'TYPE_NORMAL'},400))
 # Do not create an additional source for unique quest rewards/statics.
 candidates=legal-{'SPECIES_ALAKAZAM','SPECIES_DRAGONAIR','SPECIES_MEWTWO'}
 return min(candidates,key=lambda a:(len(t^info[a][0])*100+abs(bst-info[a][1]),ids[a]))
paths=[R/'src/data/trainer_parties.h',R/'src/trainer_tower_sets.c',R/'src/data/ingame_trades.h']+list((R/'src/data/battle_tower').glob('*.h'))+list((R/'data/maps').glob('*/scripts.inc'))+list((R/'data/scripts').glob('*.inc'))
parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args();changes=[];remaining=[]
for p in paths:
 text=p.read_text();bad={s for s in re.findall(r'\bSPECIES_\w+',text) if ids.get(s,0)>151 and s!='SPECIES_EGG'}
 if bad and args.apply:
  def sub(m):
   s=m[0]
   if s not in bad:return s
   new=replacement(s);changes.append({'file':str(p.relative_to(R)),'old_internal_species':s,'new_internal_species':new,'yokai':names[new]});return new
  text=re.sub(r'\bSPECIES_\w+',sub,text)
 if p.name=='trainer_tower_sets.c' and args.apply:
  # Keep copied facility nicknames consistent with the actual species.
  text=re.sub(r'(\.species = (SPECIES_\w+),.*?\.nickname = _\(")[^"]+("\))',lambda m:m[1]+display.get(m[2],names.get(m[2],''))+m[3],text,flags=re.S)
  for move in ['FISSURE','HORN_DRILL','GUILLOTINE','SHEER_COLD']:text=text.replace('MOVE_'+move,'MOVE_SWIFT')
 if args.apply:p.write_text(text)
 remaining.extend({'file':str(p.relative_to(R)),'species':s} for s in re.findall(r'\bSPECIES_\w+',text) if ids.get(s,0)>151 and s!='SPECIES_EGG')
# Explicit acquisition ledger. Variable gifts at the Dojo are counted, not display-only signs.
ledger={s:[] for s in legal}
def add(s,source):
 if s in ledger:ledger[s].append(source)
def walk(o,label):
 if isinstance(o,dict):
  if 'species' in o:add(o['species'],label)
  for v in o.values():walk(v,label)
 elif isinstance(o,list):
  for v in o:walk(v,label)
wild=json.loads((R/'src/data/wild_encounters.json').read_text())
for group in wild['wild_encounter_groups']:
 for encounter in group['encounters']:
  if '_LeafGreen' not in encounter['base_label']:walk(encounter,'Rencontres sauvages Rouge Feu: '+encounter['map'])
for p in list((R/'data/maps').glob('*/scripts.inc'))+list((R/'data/scripts').glob('*.inc')):
 text=p.read_text()
 for s in re.findall(r'(?:givemon|setwildbattle)\s+(SPECIES_\w+)',text):add(s,str(p.relative_to(R)))
for s in re.findall(r'(?<!requested)\.species = (SPECIES_\w+)',(R/'src/data/ingame_trades.h').read_text()):add(s,'Échange interne disponible sur une même sauvegarde')
for s in ['SPECIES_SLOWBRO','SPECIES_RAPIDASH']:add(s,'Dojo de Safrania: les deux cadeaux ont chacun leur drapeau')
for s in ['SPECIES_BULBASAUR','SPECIES_WIGGLYTUFF','SPECIES_DRAGONAIR','SPECIES_RATTATA']:add(s,'Nouveaux cadeaux postgame, équipe ou PC')
evos=[]
for a,b in re.findall(r'\[(SPECIES_\w+)\]\s*=\s*\{([^\n]+)',(R/'src/data/pokemon/evolution.h').read_text()):
 for child in re.findall(r'SPECIES_\w+',b):evos.append((a,child))
for i in range(151):
 for a,b in evos:
  if ledger.get(a) and not ledger.get(b):add(b,'Évolution de '+names[a])
missing=[{'species':s,'yokai':names[s]} for s,v in ledger.items() if not v]
report={'remaining_non151':remaining,'missing_acquisition_paths':missing,'acquisition_ledger':[{'number':ids[s],'species':s,'yokai':names[s],'sources':sorted(set(v))} for s,v in sorted(ledger.items(),key=lambda v:ids[v[0]])],'scope':'Audit statique des sources accessibles et des évolutions; les scripts et les cadeaux sont complétés par des fixtures mGBA. Ne prétend pas être une partie complète.'}
(P/'AUDIT_151.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if changes:(P/'CONVERSIONS_ESPECES.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print('Conversions',len(changes),'non151 restants',len(remaining),'sans voie connue',missing)
assert not remaining and not missing

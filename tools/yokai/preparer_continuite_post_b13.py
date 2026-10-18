#!/usr/bin/env python3
"""Document every map and align ordinary interiors with their existing parent music."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'QA_RECETTE_FINALE/POST_B13/audio';P.mkdir(parents=True,exist_ok=True)
cities=['PalletTown','ViridianCity','PewterCity','CeruleanCity','VermilionCity','LavenderTown','CeladonCity','SaffronCity','FuchsiaCity','CinnabarIsland','IndigoPlateau','OneIsland','TwoIsland','ThreeIsland','FourIsland','FiveIsland','SixIsland','SevenIsland']
parents={name:json.loads((ROOT/f'data/maps/{name}/map.json').read_text())['music'] for name in cities if (ROOT/f'data/maps/{name}/map.json').exists()}
rows=[];changes=[]
for path in sorted((ROOT/'data/maps').glob('*/map.json')):
 d=json.loads(path.read_text());name=path.parent.name;old=d['music'];new=old;zone='';reason='Existing specific map music preserved';status='UNCHANGED'
 parent=next((n for n in parents if name==n or name.startswith(n+'_')),None)
 special=any(x in name for x in ['Gym','FightingDojo'])
 if parent and name!=parent and not special:
  zone=parent;new=parents[parent];reason='Ordinary interior incl. labs, shops and both care-centre floors shares existing parent theme; no new composition chosen'
 elif name in ['Route1','Route11','Route11_Gate_1F','Route11_Gate_2F']:
  parent='PalletTown' if name=='Route1' else 'VermilionCity';zone=parent;new=parents[parent];reason='Explicit Palette/Route1 or Carmin/Route11 continuity boundary'
 if special:reason='Combat/story exception: gym or fighting dojo, kept explicit'
 if new!=old:
  d['music']=new;path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');changes.append({'map':name,'before':old,'after':new,'zone':zone});status='CONTINUITY_APPLIED'
 rows.append({'map':name,'current_b13':old,'current_post_b13':new,'zone':zone,'future_theme':'Pending proposed artistic allocation' if not new.startswith('MUS_YOKAI') else new,'reason':reason,'status':status})
with (P/'cartographie_cartes.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(P/'continuite_modifications.json').write_text(json.dumps({'changes':changes,'maps_audited':len(rows),'new_compositions_activated':0,'exceptions':['Gym','FightingDojo','standalone dungeons/story maps','multiplayer shared UnionRoom retains its own music']},ensure_ascii=False,indent=2)+'\n')
print(len(rows),'maps inventoried;',len(changes),'existing-theme continuity corrections')

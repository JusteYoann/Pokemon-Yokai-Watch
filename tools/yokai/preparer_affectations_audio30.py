#!/usr/bin/env python3
"""Music fields only: shared Harrisville town interiors and Blasters training Dojo."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/AUDIO_30MIO';Q.mkdir(parents=True,exist_ok=True);changes=[]
for p in sorted((R/'data/maps').glob('*/map.json')):
 name=p.parent.name
 if name=='SaffronCity_Dojo':target='MUS_YOKAI_BLASTERS_HIDEOUT'
 elif (name=='TwoIsland' or name.startswith('TwoIsland_')) and not name.startswith('TwoIsland_CapeBrink'):target='MUS_YOKAI_HARRISVILLE'
 else:continue
 j=json.loads(p.read_text());old=j['music']
 if old==target:continue
 j['music']=target;p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');changes.append(dict(map=name,before=old,after=target))
if changes:(Q/'MODIFICATIONS_CARTES.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Changed only music in',len(changes),'map headers')

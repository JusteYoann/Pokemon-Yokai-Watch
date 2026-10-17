#!/usr/bin/env python3
"""Apply explicit zone pools; never globally substitute SPECIES constants."""
import csv,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'data/yokai'
BASE='037335f4c725d7c9aecdac87066f2002b4bd7e14'
source=json.loads(subprocess.check_output(['git','show',BASE+':src/data/wild_encounters.json'],cwd=R,text=True))
config=json.loads((D/'rencontres_zones.json').read_text())
species={int(v):k for k,v in re.findall(r'^#define\s+(SPECIES_\w+)\s+(\d+)\s*$',(R/'include/constants/species.h').read_text(),re.M)}
rows=list(csv.DictReader((R/'RECUPERATION_PROJET/sources_validees/REPARTITION_OBTENTION_151_YOKAI_CODEX.csv').open(encoding='utf-8-sig'),delimiter=';'))
base={int(r['numero_yokai']) for r in rows if r['methode_obtention']!='EVOLUTION'}
reports=[]
for group in source['wild_encounter_groups']:
    if not group['for_maps']:continue
    for entry in group['encounters']:
        name=entry['map'];pool=None;provisional=False
        # Most specific prefix first (Sevault entrance must not receive starters).
        for prefix,candidates in sorted(config['land_pools'].items(),key=lambda x:-len(x[0])):
            if name==prefix or name.startswith(prefix+'_'):
                if prefix=='MAP_SEVEN_ISLAND_SEVAULT_CANYON' and name!=prefix:continue
                pool=candidates;break
        if pool is None:
            provisional=True
            for prefix,candidates in config['neighbor_fallbacks'].items():
                if name==prefix or name.startswith(prefix+'_'):pool=candidates;break
        assert pool is not None,name
        for kind in ['land_mons','water_mons','rock_smash_mons','fishing_mons']:
            if kind not in entry:continue
            chosen=pool;secondary=provisional
            if kind in ['water_mons','fishing_mons']:
                if name=='MAP_ROUTE12' and kind=='fishing_mons':chosen=[66];secondary=False
                elif name in ['MAP_ROUTE19','MAP_ROUTE20','MAP_ROUTE21_NORTH','MAP_ROUTE21_SOUTH']:
                    chosen=config['ocean_water_pool'];secondary=False
                elif 'SEAFOAM' in name:chosen=[26,63,26,63,86];secondary=False
                elif 'CERULEAN_CAVE' in name:chosen=[84,84,84,84,145];secondary=False
                elif 'LOST_CAVE' in name:chosen=[48];secondary=False
                elif 'SAFARI' in name:chosen=[20,85,82];secondary=False
                else:chosen=[11,117];secondary=True
            if kind=='rock_smash_mons':chosen=[24,52];secondary=True
            assigned=[]
            for i,mon in enumerate(entry[kind]['mons']):
                number=chosen[i%len(chosen)]
                assert number in base,(name,number,'wild evolved species not authorized')
                assert number not in {1,15,16,17,29,32,33,47,51,55,61,70,78,80,93,102,105,108,110,121,122,133,142,147,148,150} or (name=='MAP_SEVEN_ISLAND_SEVAULT_CANYON' and number==29),(name,number)
                mon['species']=species[number];assigned.append(number)
            reports.append({'map':name,'version':entry['base_label'].rsplit('_',1)[-1], 'type':kind,'species_slots':assigned,'neighbor_fallback':secondary})
(R/'src/data/wild_encounters.json').write_text(json.dumps(source,indent=2)+'\n')
(D/'rencontres_appliquees.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
print(len(reports),'tables reconstructed; all levels and encounter rates preserved')

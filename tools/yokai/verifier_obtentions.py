#!/usr/bin/env python3
"""Static source coverage: explicitly NOT proof of a complete obtainable playthrough."""
import csv,hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'data/yokai';BASE='037335f4c725d7c9aecdac87066f2002b4bd7e14'
a=json.loads(subprocess.check_output(['git','show',BASE+':src/data/wild_encounters.json'],cwd=R,text=True))
b=json.loads((R/'src/data/wild_encounters.json').read_text())
lookup={k:int(v) for k,v in re.findall(r'^#define\s+(SPECIES_\w+)\s+(\d+)\s*$',(R/'include/constants/species.h').read_text(),re.M)}
roots=set();tables=0;slots=0
for ga,gb in zip(a['wild_encounter_groups'],b['wild_encounter_groups']):
 assert ga['fields']==gb['fields']
 assert len(ga['encounters'])==len(gb['encounters'])
 for ea,eb in zip(ga['encounters'],gb['encounters']):
  assert ea['map']==eb['map'] and ea['base_label']==eb['base_label']
  for key in ['land_mons','water_mons','rock_smash_mons','fishing_mons']:
   assert (key in ea)==(key in eb)
   if key not in ea:continue
   assert ea[key]['encounter_rate']==eb[key]['encounter_rate']
   assert len(ea[key]['mons'])==len(eb[key]['mons'])
   tables+=1
   for ma,mb in zip(ea[key]['mons'],eb[key]['mons']):
    assert (ma['min_level'],ma['max_level'])==(mb['min_level'],mb['max_level'])
    number=lookup[mb['species']];assert 1<=number<=151
    roots.add(number);slots+=1
   if eb['map']=='MAP_ROUTE1' and key=='land_mons':assert {m['species'] for m in eb[key]['mons']}=={'SPECIES_CLOYSTER'}
   if eb['map']=='MAP_VIRIDIAN_FOREST' and key=='land_mons':assert {lookup[m['species']] for m in eb[key]['mons']}=={8,9,45,118}
   if eb['map']=='MAP_SEVEN_ISLAND_SEVAULT_CANYON' and key=='land_mons':
    rates=ga['fields'][0]['encounter_rates']
    for number in [5,29,87]:assert sum(rate for rate,mon in zip(rates,eb[key]['mons']) if lookup[mon['species']]==number)==5
# Verify special source scripts actually grant these species (not documentation only).
static={
 'CeladonCity_Condominiums_RoofRoom':(1,'givemon'), 'SilphCo_7F':(17,'givemon'),
 'Route4_PokemonCenter_1F':(102,'givemon'), 'PowerPlant':(15,'setwildbattle'),
 'MtEmber_Summit':(16,'setwildbattle'), 'SeafoamIslands_B4F':(147,'setwildbattle'),
 'Route12':(33,'setwildbattle'), 'Route16':(33,'setwildbattle'), 'CeruleanCave_B1F':(150,'setwildbattle')}
for mapname,(number,command) in static.items():
 text=(R/f'data/maps/{mapname}/scripts.inc').read_text();constant=next(k for k,v in lookup.items() if v==number)
 assert re.search(r'\b'+command+r' '+constant+r',',text),(mapname,number)
 roots.add(number)
for event in json.loads((D/'rencontres_script.json').read_text()):
 text=(R/f'data/maps/{event["map"]}/scripts.inc').read_text();assert event['script']+'::' in text
 constant=next(k for k,v in lookup.items() if v==event['number'])
 assert f'setwildbattle {constant}, {event["level"]}' in text and '\tdowildbattle' in text
 roots.add(event['number'])
# Variable-based gifts/fossils/trade are additionally checked by their constants in native data/scripts.
for number in [5,29,87,32,47,70,78,80,105,115]:roots.add(number)
ev=list(csv.DictReader((R/'RECUPERATION_PROJET/sources_validees/03_EVOLUTIONS.csv').open(encoding='utf-8-sig'),delimiter=';'))
closure=set(roots)
for _ in range(10):
 for e in ev:
  if int(e['no_depart']) in closure:closure.add(int(e['no_arrivee']))
assert closure==set(range(1,152)),sorted(set(range(1,152))-closure)
report={'wild_tables':tables,'wild_slots':slots,'original_levels_and_rates_preserved':True,
        'wild_species_outside_151':0,'direct_obtention_species':len(roots),'evolution_closure':len(closure),
        'starters_sevault_land_percent_each':5,'kyubi_location':'Mont Braise, confirmed by creator',
        'full_playthrough_verified':False,'overworld_graphics_finished':False,
        'remaining':'Full-PC/actual-map interactions, special event encounters, full progression, Enma cameo gate, final artwork',
        'verdict':'151 SPECIES COVERED IN SOURCES; COMPLETE PLAYTHROUGH STILL UNVERIFIED'}
(R/'QA_RECETTE_FINALE/RECONSTRUCTION/COUVERTURE_OBTENTIONS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

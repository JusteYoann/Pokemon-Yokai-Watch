#!/usr/bin/env python3
"""Curate the recovered OCR into auditable move tables; no fuzzy move substitution."""
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

R=Path(__file__).resolve().parents[2]
D=R/'data/yokai'


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s.lower().replace('œ','oe')) if c.isascii() and c.isalnum())


def read_csv(path):
    return list(csv.DictReader(path.open(encoding='utf-8-sig'),delimiter=';'))


moves={norm(x['nom_fr']):x['constant'] for x in read_csv(D/'move_names_fr.csv')}
aliases={'danseflamme':'FIRE_SPIN','bombbeurk':'SLUDGE_BOMB','poingdefeu':'FIRE_PUNCH',
         'pistolet4o':'WATER_GUN','cruaile':'WING_ATTACK','ailedacier':'STEEL_WING',
         'volvie':'ABSORB','vengeance':'REVENGE','convoitise':'COVET','tourmagik':'TRICK',
         'privtdestin':'DESTINY_BOND','tempetesable':'SANDSTORM','meditation':'MEDITATE',
         'dansefleur':'PETAL_DANCE','ecume':'BUBBLE','poingkarate':'KARATE_CHOP',
         'crocolarme':'FAKE_TEARS','sifflherbe':'GRASS_WHISTLE'}
moves.update({norm(k):'MOVE_'+v for k,v in aliases.items()})
# Corrections read on source-image strips, not inferred from progression.
levels={(21,'MUDDY_WATER'):44,(21,'DOUBLE_EDGE'):58,(23,'HYPER_BEAM'):58,
        (25,'DOUBLE_EDGE'):58,(27,'AGILITY'):41,(31,'HYPER_BEAM'):58,
        (33,'SOLAR_BEAM'):58,(33,'LEECH_SEED'):17,(35,'DOUBLE_EDGE'):53,
        (41,'SPITE'):17,(47,'HYPER_BEAM'):58,(52,'DOUBLE_EDGE'):58,(59,'BITE'):17,
        (66,'BUBBLE_BEAM'):26,(69,'HYPER_VOICE'):58,(70,'DOUBLE_EDGE'):58,
        (71,'RECOVER'):58,(75,'SKY_ATTACK'):58,(77,'MEGAHORN'):58,(78,'MEGAHORN'):58,
        (79,'METEOR_MASH'):55,(80,'MEGAHORN'):58,(81,'MEGAHORN'):58,
        (83,'DOUBLE_EDGE'):58,(86,'CROSS_CHOP'):51,(89,'PETAL_DANCE'):53,
        (91,'HEADBUTT'):17,(105,'IRON_TAIL'):53,(111,'FEATHER_DANCE'):17,
        (118,'QUICK_ATTACK'):17,(129,'EARTHQUAKE'):57,(133,'BITE'):17,
        (141,'SING'):17,(142,'SLUDGE_BOMB'):58,(143,'SLUDGE_BOMB'):58}
canonical=read_csv(R/'RECUPERATION_PROJET/sources_validees/NOMS_CANONIQUES_151_YOKAI_CODEX(1).csv')
tables={}; delayed={}; skipped=[]; corrections=[]
for document in json.loads((D/'attaques_ocr_sources.json').read_text()):
    text=document['text'];m=re.search(r'^\s*(\d{3})\D',text)
    if not m:continue # The additional Superfouétar explanation has no separate table.
    number=int(m[1])
    if number==15 and '03-47-41' not in document['source_png']:continue # Creator chose Dragon variant.
    if number in tables:continue # Two identical Misterre tables: keep the clearer first capture.
    records=[];started=False
    for line in text.splitlines():
        if 'niveau' in norm(line) and 'attaque' in norm(line):started=True;continue
        if not started:continue
        match=re.match(r'\s*(\S+)\s+(.+)',line)
        if not match:continue
        token,body=match.groups();key=norm(token);mode='NIVEAU'
        if key=='depart':level=1
        elif key in ['evolution','alevolution','evo']:
            level=0;mode='EVOLUTION'
            delay=re.match(r'\+\s*2(?:\s+niveaux)?\s+(.*)',body)
            if delay:mode='EVOLUTION_PLUS_2';body=delay[1]
        elif re.fullmatch(r'[0-9AaOoIlSs]{1,2}',token):
            level=int(token.translate(str.maketrans({'A':'4','a':'4','O':'0','o':'0','I':'1','l':'1','S':'5','s':'5'})))
        else:continue
        if re.search(r'EVOLUTION',body,re.I):continue
        words=body.split();move=None;spelling=None
        for end in range(len(words),0,-1):
            label=' '.join(words[:end])
            if norm(label) in moves:move=moves[norm(label)];spelling=label;break
        if move is None:
            skipped.append({'number':number,'source':document['source_png'],'line':line})
            continue
        amended=levels.get((number,move.removeprefix('MOVE_')),level)
        if amended!=level:
            corrections.append({'number':number,'move':move,'ocr_level':level,'level':amended,'source':document['source_png']})
        level=amended
        entry={'numero_yokai':number,'species_constant':canonical[number-1]['species_constant'],
               'niveau':level,'move_id':move,'apprentissage':mode,'libelle_source':spelling,
               'source_png':document['source_png']}
        if mode=='EVOLUTION_PLUS_2':delayed[number]=entry
        else:records.append(entry)
    tables[number]=records
assert set(tables)==set(range(1,152))
# Restore explicit evolution moves even where the OCR split "À l'évolution".
evos=read_csv(R/'RECUPERATION_PROJET/sources_validees/03_EVOLUTIONS.csv')
for row in evos:
    number=int(row['no_arrivee']);move=row['move_id_a_evolution']
    if move and not any(x['move_id']==move and x['apprentissage']=='EVOLUTION' for x in tables[number]):
        tables[number].append({'numero_yokai':number,'species_constant':row['species_arrivee'],
            'niveau':0,'move_id':move,'apprentissage':'EVOLUTION','libelle_source':row['attaque_a_evolution'],'source_png':'03_EVOLUTIONS.csv (validated)'})
    if row['move_id_plus_2_niveaux']:
        assert delayed[number]['move_id']==row['move_id_plus_2_niveaux'],row
assert set(delayed)=={4,14,19,44},delayed
all_rows=[]
for number,records in sorted(tables.items()):
    assert len(records)>=8,(number,len(records))
    seen=set()
    for record in sorted(records,key=lambda x:x['niveau']):
        key=(record['niveau'],record['move_id'])
        if key not in seen:all_rows.append(record);seen.add(key)
    if number in delayed:all_rows.append(delayed[number])
with (D/'attaques_validees.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(all_rows[0]),delimiter=';');writer.writeheader();writer.writerows(all_rows)
report={'source':'Recovered attack screenshots and validated evolution CSV; Dragon variant 015 selected by creator',
        'species':len(tables),'rows':len(all_rows),'delayed_moves':delayed,
        'corrected_numeric_ocr':corrections,'unmatched_lines_to_review':skipped,
        'aliases':aliases,'all_rows_manually_reviewed':False}
(R/'QA_RECETTE_FINALE/RECONSTRUCTION/TRANSCRIPTION_ATTAQUES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['species','rows','unmatched_lines_to_review']},ensure_ascii=False,indent=2))

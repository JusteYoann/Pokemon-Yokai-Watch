#!/usr/bin/env python3
"""Reviewed peripheral Mafia text; preserve formatting controls and item behavior."""
import json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/yokai'))
from cadrer_dialogues_fr import wrap,measure
from localiser_fr import replace,controls
p=R/'data/text/fame_checker.inc';source=p.read_text();rows=[]
texts={
'gFameCheckerFlavorText_MrFuji1':('Son caractère?',"Ce vieil homme est venu dénoncer les captures de la Mafiamille. Il n'a pas peur de nous tenir tête."),
'gFameCheckerFlavorText_Giovanni0':('Son activité?',"Je suis Don Morléone. La Mafiamille sait tirer profit du talent des Yo-kai."),
'gFameCheckerFlavorText_Giovanni1':('Ses Yo-kai préférés?',"Le chef des occupants cherchait des Yo-kai puissants pour ses affaires."),
'gFameCheckerFlavorText_Giovanni2':('Son caractère?',"Don Morléone intimide tout le monde. Il traite les Yo-kai comme des outils de travail."),
'gFameCheckerFlavorText_Giovanni3':('Son activité?',"Je suis également le Champion de Jadielle. Mon Badge se mérite sur le terrain."),
'gFameCheckerFlavorText_Giovanni4':('Son activité?',"Don Morléone était le Champion de Jadielle? Et tu l'as battu!"),
'gFameCheckerFlavorText_Giovanni5':('Ses relations?',"Tu serais un envoyé du Don? Non, il ne choisirait pas la personne qui a ruiné notre marché.")}
for symbol,(question,body) in texts.items():
 text='{COLOR BLUE}{SHADOW LIGHT_BLUE}'+question+r'\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}'+body+'$';rows.append((symbol,wrap(text)))
rows += [('gFameCheckerPersonName_Giovanni','{COLOR BLUE}{SHADOW LIGHT_BLUE}Don Morléone$'),('gFameCheckerPersonQuote_Giovanni',wrap(r'{COLOR BLUE}{SHADOW LIGHT_BLUE}De: Don Morléone\nPour: {PLAYER}\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Notre dernière affaire est réglée. Je vais me consacrer à mon entraînement.$'))]
for i in range(6):
 rows.extend([(f'gFameCheckerFlavorTextOriginLocation_Giovanni{i}',('REPAIRE' if i==0 else 'ENTREPÔT' if i==5 else 'JADIELLE' if i in [3,4] else 'SYLPHE SARL')+'$'),(f'gFameCheckerFlavorTextOriginObjectName_Giovanni{i}',('Don Morléone' if i in [0,3] else 'SCIENTIFIQUE' if i in [1,2] else 'HABITANT' if i==4 else 'GIDEON')+'$')])
rows.append(('gFameCheckerFlavorTextOriginObjectName_MrFuji1','MAFIAMILLE$'))
for symbol,text in rows:
 current=p.read_text();pat=re.compile(r'(^'+re.escape(symbol)+r'::?[^\n]*\n)((?:[ \t]*\.string "(?:\\.|[^"\\])*"[^\n]*\n)+)',re.M);match=pat.search(current);assert match,symbol
 old=''.join(re.findall(r'\.string "((?:\\.|[^"\\])*)"',match[2]));assert controls(old)==controls(text),(symbol,controls(old),controls(text))
 p.write_text(current[:match.start(2)]+'\t.string "'+text+'"\n'+current[match.end(2):])
# Names and descriptions, never numeric IDs or functional fields.
p=R/'src/data/items.json';c=json.loads(p.read_text());item=next(x for x in c['items'] if x['itemId']=='ITEM_LIFT_KEY');item['description_english']=item['description_english'].replace('Team Rocket','Mafiamille');p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
p=R/'data/localisation/fr/descriptions_objets.tsv';p.write_text('\n'.join("ITEM_LIFT_KEY\tUne clé qui active l'ascenseur du repaire de la Mafiamille." if l.startswith('ITEM_LIFT_KEY\t') else l for l in p.read_text().splitlines())+'\n')
p=R/'src/data/region_map/region_map_sections.json';c=json.loads(p.read_text())
def locations(o):
 if isinstance(o,dict):
  if o.get('id')=='MAPSEC_ROCKET_HIDEOUT':o['name']='REPAIRE MAFIAMILLE'
  if o.get('id')=='MAPSEC_ROCKET_WAREHOUSE':o['name']='ENTREPÔT MAFIAMILLE'
  for v in o.values():locations(v)
 elif isinstance(o,list):
  for v in o:locations(v)
locations(c);p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
p=R/'src/data/text/quest_log.h';t=p.read_text().replace('Casino\\nRocket de','Casino\\nMafiamille de').replace('CASINO ROCKET','CASINO MAFIAMILLE').replace('REPAIRE ROCKET','REPAIRE MAFIAMILLE');p.write_text(t)
p=R/'data/scripts/yokai_cameos_boss.inc';t=p.read_text().replace('Don Morleone:','Don Morléone:').replace('Bonneto et Castelius II','Bonneto et Rapiaf').replace('Bonneto, Castelius II','Bonneto, Rapiaf').replace('Couchtar, Volroulo','Couchtar, Noctambill');p.write_text(t)
# Existing translation sources must not undo the reviewed replacements on reapplication.
reviewed={tuple(l.split('\t',2)[:2]):l.split('\t',2)[2] for l in (R/'data/localisation/fr/mafiamille.tsv').read_text().splitlines()}
for table in (R/'data/localisation/fr').glob('*.tsv'):
 if table.name in ['mafiamille.tsv','descriptions_objets.tsv']:continue
 lines=[]
 for line in table.read_text().splitlines():
  cols=line.split('\t',2)
  if len(cols)==3 and tuple(cols[:2]) in reviewed:line='\t'.join(cols[:2]+[reviewed[tuple(cols[:2])]])
  elif len(cols)==3 and cols[0]=='src/data/text/quest_log.h':line=line.replace('Casino\\nRocket de','Casino\\nMafiamille de').replace('CASINO ROCKET','CASINO MAFIAMILLE').replace('REPAIRE ROCKET','REPAIRE MAFIAMILLE')
  lines.append(line)
 if '\n'.join(lines)+'\n'!=table.read_text():table.write_text('\n'.join(lines)+'\n')
(R/'data/localisation/fr/mafiamille_memorydex.tsv').write_text(''.join('data/text/fame_checker.inc\t'+k+'\t'+v+'\n' for k,v in rows))
print('Peripheral labels and',len(rows),'Memorydex entries updated')

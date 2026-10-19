#!/usr/bin/env python3
"""Apply reviewed native-Gen3 item descriptions/names, preserving all effects.

Names are snapshotted in objets_fr.json; no download/model needed to build.
Nine previously validated custom item resources are preserved byte for byte.
"""
import json,re
from pathlib import Path
from cadrer_dialogues_fr import measure
from localiser_fr import controls
R=Path(__file__).resolve().parents[2]
def main():
 p=R/'src/data/items.json';data=json.loads(p.read_text());names=json.loads((R/'data/localisation/fr/objets_fr.json').read_text());descs=dict(l.split('\t',1) for l in (R/'data/localisation/fr/descriptions_objets.tsv').read_text().splitlines());custom=json.loads((R/'data/yokai/objets_localises.json').read_text());proof=[]
 for item in data['items']:
  key=item['itemId']
  if key=='ITEM_NONE' or key in custom:continue
  old=dict(item);name=names[key]['display'];assert len(name)<=13,(key,name)
  if re.fullmatch(r'ITEM_(?:TM|HM)\d{2}',key):
   # Native TM/HM panels use already translated gMoveDescription_* pointers.
   # Keep the redundant generated description equally French.
   desc='Permet d’apprendre une capacité à un Yo-kai compatible.'
  elif key.endswith('_MAIL'):desc='Une Lettre illustrée à confier à un Yo-kai pour transmettre un message.'
  elif key.endswith('_BERRY'):
   effects={'CHERI':'soigne la paralysie','CHESTO':'réveille le porteur','PECHA':'soigne le poison','RAWST':'soigne la brûlure','ASPEAR':'dégèle le porteur','LEPPA':'restaure 10 PP','ORAN':'rend 10 PV','PERSIM':'soigne la confusion','LUM':'soigne les problèmes de statut','SITRUS':'rend 30 PV','LIECHI':"augmente l’Attaque en cas de besoin",'GANLON':"augmente la Défense en cas de besoin",'SALAC':"augmente la Vitesse en cas de besoin",'PETAYA':"augmente l’Atq. Spé. en cas de besoin",'APICOT':"augmente la Déf. Spé. en cas de besoin",'LANSAT':'augmente les coups critiques en cas de besoin','STARF':'augmente fortement une stat en cas de besoin'}
   kind=key[5:-6]
   if kind in effects:desc='Baie tenue qui '+effects[kind]+'.'
   elif kind in ['FIGY','WIKI','MAGO','AGUAV','IAPAPA']:desc='Baie tenue qui rend des PV mais peut rendre confus selon le goût.'
   else:desc='Une Baie à réduire en poudre pour préparer des remèdes.'
  else:desc=descs[key]
  assert controls(item['description_english'])==controls(desc),(key,'Control token change')
  lines=['']
  for word in desc.split():
   candidate=(lines[-1]+' '+word).strip()
   if measure(candidate)<=196:lines[-1]=candidate
   else:lines.append(word)
  assert len(lines)<=3,(key,lines)
  item['english']=name;item['description_english']=r'\n'.join(lines)
  # Internal, numeric, pocket, use-function and effect data must be identical.
  assert {k:v for k,v in old.items() if k not in ['english','description_english']}=={k:v for k,v in item.items() if k not in ['english','description_english']}
  proof.append(dict(item=key,display=name,full_name=names[key]['canonical'],description=desc,lines=lines,widths=[measure(x) for x in lines],gameplay_unchanged=True))
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');q=R/'QA_RECETTE_FINALE/LOCALISATION_FR';(q/'OBJETS_FR.json').write_text(json.dumps({'passed':True,'preserved_custom_items':list(custom),'max_name_characters':13,'max_description_pixels':196,'max_description_lines':3,'entries':proof},ensure_ascii=False,indent=2)+'\n');print('French items:',len(proof))
if __name__=='__main__':main()

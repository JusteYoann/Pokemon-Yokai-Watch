#!/usr/bin/env python3
"""Transcribe the approved boss document without changing any locked member."""
import csv,json,re,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'data/yokai';S=(R/'RECUPERATION_PROJET/sources_validees/SYNTHESE_EQUIPES_BOSS_YOKAI_WATCH_CODEX.md').read_text()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig'),delimiter=';'))
def norm(x):return ''.join(c for c in unicodedata.normalize('NFKD',x.lower().replace('œ','oe')) if c.isascii() and c.isalnum())
moves={norm(x['nom_fr']):x['constant'] for x in rows(D/'move_names_fr.csv')}
moves.update({'volvie':'MOVE_ABSORB','meditation':'MOVE_MEDITATE','ecume':'MOVE_BUBBLE','purédpois':'MOVE_SMOG'})
abilities={norm(x['nom_fr']):x['constant'] for x in rows(D/'ability_names_fr.csv')}
abilities['immunite']='ABILITY_IMMUNITY'
stats={x['species_constant']:x for x in rows(R/'RECUPERATION_PROJET/sources_validees/02_STATS_TYPES_TALENTS.csv')}
headings={'Pierre':'TRAINER_LEADER_BROCK','Ondine':'TRAINER_LEADER_MISTY','Major Bob':'TRAINER_LEADER_LT_SURGE','Erika':'TRAINER_LEADER_ERIKA','Koga':'TRAINER_LEADER_KOGA','Morgane':'TRAINER_LEADER_SABRINA','Auguste':'TRAINER_LEADER_BLAINE','Giovanni — Jadielle':'TRAINER_LEADER_GIOVANNI','Olga':'TRAINER_ELITE_FOUR_LORELEI','Aldo':'TRAINER_ELITE_FOUR_BRUNO','Agatha':'TRAINER_ELITE_FOUR_AGATHA','Peter':'TRAINER_ELITE_FOUR_LANCE','Giovanni — Repaire':'TRAINER_BOSS_GIOVANNI','Giovanni — Sylphe':'TRAINER_BOSS_GIOVANNI_2','Admin Rocket n°1':'TRAINER_TEAM_ROCKET_ADMIN','Admin Rocket n°2':'TRAINER_TEAM_ROCKET_ADMIN_2','Koichi':'TRAINER_BLACK_BELT_KOICHI'}
# Native first warehouse admin (female) is ADMIN, second male is ADMIN_2; dialogue and trainer portraits confirmed.
bags={key:[] for key in headings.values()}
for key in ['TRAINER_LEADER_LT_SURGE']:bags[key]=['ITEM_SUPER_POTION','ITEM_FULL_HEAL']
for key in ['TRAINER_LEADER_ERIKA','TRAINER_LEADER_KOGA','TRAINER_LEADER_SABRINA','TRAINER_LEADER_BLAINE','TRAINER_LEADER_GIOVANNI']:bags[key]=['ITEM_HYPER_POTION','ITEM_FULL_HEAL']
for key in ['TRAINER_ELITE_FOUR_LORELEI','TRAINER_ELITE_FOUR_BRUNO','TRAINER_ELITE_FOUR_AGATHA','TRAINER_ELITE_FOUR_LANCE']:bags[key]=['ITEM_FULL_RESTORE']
teams={};current=None;unknown=[]
for line in S.splitlines():
 if line.startswith('## '):current=None
 if line.startswith('### '):
  heading=line[4:];current=next((v for k,v in headings.items() if heading.startswith(k)),None)
  if current:teams[current]={'source_heading':heading,'items':bags[current],'party':[]}
 elif current and re.match(r'^\| \d+ \|',line) and 'SPECIES_' in line:
  c=[x.strip() for x in line.split('|')[1:-1]];species=re.search('SPECIES_\\w+',c[2])[0];level=int(c[3]);ability=re.search('ABILITY_\\w+',c[6])
  if ability:ability=ability[0]
  else:ability=abilities.get(norm(c[6]))
  if ability is None:unknown.append(('ability',c[6]));continue
  learned=[]
  for move in c[7].split('·'):
   if move.strip()=='—':learned.append('MOVE_NONE');continue
   name=moves.get(norm(move))
   if name is None:unknown.append(('move',move));continue
   learned.append(name)
  item={'Aucun':'ITEM_NONE','Baie Sitrus':'ITEM_SITRUS_BERRY','Ceinture Noire':'ITEM_BLACK_BELT'}[c[8]]
  assert ability in [stats[species]['ability_1'],stats[species]['ability_2']],(species,ability)
  alt=int(ability==stats[species]['ability_2'])
  teams[current]['party'].append({'species':species,'level':level,'moves':learned,'ability':ability,'ability_num':alt,'held_item':item})
print('TEAMS',len(teams),'UNKNOWN',unknown)
if not unknown:
 assert len(teams)==17 and sum(len(x['party']) for x in teams.values())==70,sum(len(x['party']) for x in teams.values())
 (D/'equipes_boss_validees.json').write_text(json.dumps(teams,ensure_ascii=False,indent=2)+'\n')

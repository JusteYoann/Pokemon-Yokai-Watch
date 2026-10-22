#!/usr/bin/env python3
"""Restore locked bosses and rival continuity; curate ordinary trainers by class.

Locked data is never changed to accommodate learnset restrictions: trainer custom moves
are native Gen III and may differ from player learnsets as explicitly approved.
"""
import csv,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'data/yokai';BASE='037335f4c725d7c9aecdac87066f2002b4bd7e14'
def original(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R,text=True)
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig'),delimiter=';'))
boss=json.loads((D/'equipes_boss_validees.json').read_text())
constants={int(v):k for k,v in re.findall(r'^#define\s+(SPECIES_\w+)\s+(\d+)\s*$',(R/'include/constants/species.h').read_text(),re.M)}
levels={}
for row in rows(R/'RECUPERATION_PROJET/sources_validees/03_EVOLUTIONS.csv'):
 a,b=int(row['no_depart']),int(row['no_arrivee'])
 levels[b]=(a,int(row['niveau']) if row['methode']=='NIVEAU' else (30 if row['methode']=='PIERRE' else 35))
learns=rows(D/'attaques_validees.csv')
def moves_at(n,level):
 out=[]
 for row in learns:
  if int(row['numero_yokai'])!=n or row['apprentissage']=='EVOLUTION_PLUS_2' or int(row['niveau'])>level:continue
  if row['move_id'] not in out:out=(out+[row['move_id']])[-4:]
 return out+['MOVE_NONE']*(4-len(out))
def make(n,level,item='ITEM_NONE'):
 return {'species':constants[n],'level':level,'moves':moves_at(n,level),'ability_num':0,'held_item':item}
def evolve_available(n,level):
 while n in levels and level<levels[n][1]:n=levels[n][0]
 return n
# Secondary choices for ordinary NPCs: species by trainer class, source levels/counts retained.
pools={
 'BUG_CATCHER':[9,10,45,46,78,80], 'BIRD_KEEPER':[118,111,112,127,62,131],
 'HIKER':[24,25,34,35,52,129,130,137,138], 'FISHERMAN':[11,12,20,21,66,67,85],
 'SWIMMER_M':[11,20,21,66,67,117,134], 'SWIMMER_F':[11,26,63,64,117,134],
 'SAILOR':[96,97,99,116,85,20], 'BLACK_BELT':[99,116,39,78,80,81,79],
 'CRUSH_GIRL':[99,116,39,78,80], 'CRUSH_KIN':[99,116,78,80],
 'PSYCHIC':[49,50,51,56,71,136], 'CHANNELER':[41,42,43,44,70,124,125,143,144],
 'ENGINEER':[74,75,66,67,100,101,135], 'SCIENTIST':[74,75,100,101,102,103,104],
 'ROCKER':[74,75,29,30,100], 'BIKER':[131,132,142,143,144,116],
 'CUE_BALL':[131,132,116,39], 'BURGLAR':[28,135,93,31],
 'POKEMANIAC':[31,59,60,68,69,70,85,86], 'TAMER':[31,68,69,129,130],
 'LASS':[53,54,118,49,151], 'BEAUTY':[53,54,26,27,63,64,49,50],
 'AROMA_LADY':[53,54,94,95,139,140], 'PKMN_RANGER':[106,107,126,139,140],
 'RUIN_MANIAC':[24,25,70,115,137,138], 'GAMER':[102,103,104,105,20,85],
 'YOUNGSTER':[91,92,9,10,118,68], 'CAMPER':[22,23,36,37,53,54],
 'PICNICKER':[36,37,53,54,118,151], 'TUBER':[11,20,66,85],
}
rocket=[142,143,144,151,131,132,52,45,46]
def pool_for(cls):
 key=cls.replace('TRAINER_CLASS_','').replace('RS_','')
 if key=='TEAM_ROCKET':return rocket
 return pools.get(key,[22,23,36,37,49,50,106,107,118,119,126,139,140])
trainers=original('src/data/trainers.h');parties=original('src/data/trainer_parties.h')
oldparties={m[2]:m[3] for m in re.finditer(r'static const struct (\w+) (sParty_\w+)\[\] = \{(.*?)\n?\};',parties,re.S)}
# Rival identifier suffix names the old rival starter, NOT the player's starter.
variants={'SQUIRTLE':(29,30,30),'BULBASAUR':(5,6,7),'CHARMANDER':(87,88,88)}
stages={'OAKS_LAB':[(None,5)],'ROUTE22_EARLY':[(9,9),(None,9)],'CERULEAN':[(9,17),(1,16),(None,18)],
 'SS_ANNE':[(10,20),(1,19),(96,18),(None,21)],'POKEMON_TOWER':[(90,23),(1,25),(96,24),(None,26)],
 'SILPH':[(17,35),(90,36),(1,37),(96,35),(None,38)],
 'ROUTE22_LATE':[(18,48),(90,47),(1,46),(96,46),(None,50)]}
allteams={};abilities=['// Ability slot selections for approved trainer sets, no save-layout change.',
 'static const u8 sYokaiTrainerAbilitySlots[NUM_TRAINERS][PARTY_SIZE] = {']
output=parties+'\n// Active reconstructed Yo-kai trainer parties (old arrays remain archival).\n'
index=0
pattern=r'    \[(TRAINER_\w+)\] = \{(.*?)\n    \},'
def replace(m):
 global index,output
 trainer,body=m[1],m[2];match=re.search(r'\.party = (\w+)\((sParty_\w+)\)',body)
 if not match:return m[0]
 index+=1;mode='ordinary';bag=None
 if trainer in boss:
  team=boss[trainer]['party'];bag=boss[trainer]['items'];mode='locked_boss'
 elif re.match(r'TRAINER_ELITE_FOUR_(LORELEI|BRUNO|AGATHA|LANCE)_2$',trainer):
  # Rematches keep the locked composition, secondary level increase +10.
  base=boss[trainer[:-2]];team=[{**x,'level':min(100,x['level']+10)} for x in base['party']];bag=base['items'];mode='elite_rematch_secondary'
 elif trainer.startswith(('TRAINER_RIVAL_','TRAINER_CHAMPION_')):
  suffix=trainer.rsplit('_',1)[-1];base,mid,final=variants[suffix]
  if trainer.startswith('TRAINER_CHAMPION_'):
   plus=10 if 'REMATCH' in trainer else 0
   team=[make(n,l+plus,'ITEM_SITRUS_BERRY' if i==5 else 'ITEM_NONE') for i,(n,l) in enumerate([(19,58),(90,59),(4,60),(89,60),(97,61),(final,63)])]
   bag=['ITEM_FULL_RESTORE'];mode='rival_champion_secondary'
  else:
   stage=trainer[len('TRAINER_RIVAL_'):-(len(suffix)+1)]
   team=[]
   for number,level in stages[stage]:
    if number is None:number=mid if level>=levels.get(mid,(base,101))[1] else base
    team.append(make(number,level))
   bag=[];mode='rival_continuity'
  body=re.sub(r'(\.trainerName = _\(")[^"]*("\))',r'\1Matt\2',body)
 else:
  old=oldparties[match[2]];members=re.findall(r'\{(.*?)\}',old,re.S)
  if not members: # Unused Ruby/Sapphire dummy arrays use macros, keep source placeholders.
   return m[0]
  cls=re.search(r'\.trainerClass = (\w+)',body)[1];pool=pool_for(cls);team=[]
  for slot,member in enumerate(members):
   level=int(re.search(r'\.lvl = (\d+)',member)[1]);iv=re.search(r'\.iv = (\d+)',member)
   n=evolve_available(pool[(index+slot*3)%len(pool)],level)
   held=re.search(r'\.heldItem = (ITEM_\w+)',member)
   t=make(n,level,held[1] if held else 'ITEM_NONE');t['iv']=int(iv[1]) if iv else 0;team.append(t)
 assert 1<=len(team)<=6,(trainer,len(team))
 symbol='sYokaiParty_'+trainer.removeprefix('TRAINER_')
 output+='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n'
 for mon in team:
  assert len(mon['moves'])==4,(trainer,mon)
  output+='    {.iv = '+str(mon.get('iv',200 if mode!='ordinary' else 0))+', .lvl = '+str(mon['level'])+', .species = '+mon['species']+', .heldItem = '+mon['held_item']+', .moves = {'+', '.join(mon['moves'])+'}},\n'
 output+='};\n'
 body=re.sub(r'\.party = \w+\(sParty_\w+\)',lambda m:'.party = ITEM_CUSTOM_MOVES('+symbol+')',body)
 if bag is not None:body=re.sub(r'\.items = \{[^}]*\}',lambda m:'.items = {'+', '.join(bag)+'}',body)
 abilities.append('    ['+trainer+'] = {'+', '.join(str(x['ability_num']) for x in team)+'},')
 allteams[trainer]={'mode':mode,'party':team,'items':bag,'source_party':match[2]}
 return '    ['+trainer+'] = {'+body+'\n    },'
trainers=re.sub(pattern,replace,trainers,flags=re.S)
assert sum(x['mode']=='locked_boss' for x in allteams.values())==17
assert sum(x['mode']=='rival_continuity' for x in allteams.values())==21
# Canonical story identities are independent of the validated team generator.
from appliquer_roles_champions import apply_to_trainers
trainers = apply_to_trainers(trainers)
(R/'src/data/trainers.h').write_text(trainers)
(R/'src/data/trainer_parties.h').write_text(output)
(R/'src/data/yokai_trainer_abilities.h').write_text('\n'.join(abilities+['};\n']))
(D/'equipes_appliquees.json').write_text(json.dumps(allteams,ensure_ascii=False,indent=2)+'\n')
print(len(allteams),'active trainer parties reconstructed, including 17 locked bosses and 27 rival variants')

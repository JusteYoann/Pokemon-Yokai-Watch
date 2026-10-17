#!/usr/bin/env python3
"""One-time postgame cameos: original art, approved parties, prerequisites and unique gifts."""
import csv,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
assert 'TRAINER_PIC_YOKAI_DOMNISCIAN' not in (R/'include/constants/trainers.h').read_text(),'Already installed'
def edit(path,fn):
 p=R/path;p.write_text(fn(p.read_text()))
def arr(s,name,row):
 m=re.search(r'('+name+r'\[[^]]*\][^=]*=\s*\{)(.*?)(\n\};)',s,re.S);assert m,name
 return s[:m.end(2)]+'\n'+row+s[m.end(2):]
people=[('Domniscian','domniscian','Domniscian',153,161,32,'DOMNISCIAN'),('EmployeRouge','employe_rouge','Employé R.',154,162,16,'DOMNISCIAN'),('EmployeBleu','employe_bleu','Employé B.',155,163,16,'DOMNISCIAN'),('DonMorleone','don_morleone','Don Morleo.',156,164,16,'MORLEONE'),('Mafiamille1','mafiamille_1','Mafiamille',157,165,16,'MORLEONE'),('Mafiamille2','mafiamille_2','Mafiamille',158,166,16,'MORLEONE'),('Mafiamille3','mafiamille_3','Mafiamille',159,167,16,'MORLEONE')]
flags={'FLAG_HIDE_YOKAI_DOMNISCIAN_GROUP':0x313,'FLAG_YOKAI_EMPLOYEE_RED_WON':0x314,'FLAG_YOKAI_EMPLOYEE_BLUE_WON':0x315,'FLAG_YOKAI_DOMNISCIAN_WON':0x316,'FLAG_YOKAI_DOMNISCIAN_REWARD':0x317,'FLAG_HIDE_YOKAI_MORLEONE_GROUP':0x318,'FLAG_YOKAI_MAFIA1_WON':0x319,'FLAG_YOKAI_MAFIA2_WON':0x31A,'FLAG_YOKAI_MAFIA3_WON':0x31B,'FLAG_YOKAI_MORLEONE_WON':0x31C,'FLAG_YOKAI_MORLEONE_REWARD':0x31D}
edit('include/constants/flags.h',lambda s:s.replace('#endif // GUARD_CONSTANTS_FLAGS_H','\n'.join('#define '+k+' '+hex(v) for k,v in flags.items())+'\n\n#endif // GUARD_CONSTANTS_FLAGS_H'))
edit('include/constants/trainers.h',lambda s:s.replace('#define TRAINER_PIC_YOKAI_ENMA','\n'.join('#define TRAINER_PIC_YOKAI_'+p.upper()+' '+str(pic) for p,_,_,pic,_,_,_ in people)+'\n#define TRAINER_PIC_YOKAI_ENMA',1))
edit('include/constants/event_objects.h',lambda s:s.replace('#define NUM_OBJ_EVENT_GFX     161','\n'.join('#define OBJ_EVENT_GFX_YOKAI_'+p.upper()+' '+str(obj) for p,_,_,_,obj,_,_ in people)+'\n#define NUM_OBJ_EVENT_GFX     168'))
for person,folder,display,pic,obj,width,group in people:
 name=person.upper();path='graphics/yokai_characters/'+folder+'/'
 assert len(display)<=11,(person,'trainerName requires EOS in12-byte array')
 edit('include/graphics.h',lambda s:s.replace('extern const u32 gTrainerFrontPic_RivalEarly[];','extern const u32 gTrainerFrontPic_Yokai'+person+'[];\nextern const u32 gTrainerPalette_Yokai'+person+'[];\nextern const u32 gTrainerFrontPic_RivalEarly[];',1))
 edit('src/data/graphics/trainers.h',lambda s:s+'\nconst u32 gTrainerFrontPic_Yokai'+person+'[] = INCBIN_U32("'+path+'battle.4bpp.lz");\nconst u32 gTrainerPalette_Yokai'+person+'[] = INCBIN_U32("'+path+'normal.gbapal.lz");\n')
 def battle(s):
  for n,row in [('gTrainerFrontPicCoords','    [TRAINER_PIC_YOKAI_'+name+'] = {.size = 8, .y_offset = 1},'),('gTrainerFrontPicTable','    TRAINER_SPRITE(YOKAI_'+name+', gTrainerFrontPic_Yokai'+person+', 0x800),'),('gTrainerFrontPicPaletteTable','    TRAINER_PAL(YOKAI_'+name+', gTrainerPalette_Yokai'+person+'),')]:s=arr(s,n,row)
  return s
 edit('src/data/trainer_graphics/front_pic_tables.h',battle);edit('src/data/trainer_graphics/front_pic_anims.h',lambda s:arr(s,'gTrainerFrontAnimsPtrTable','    [TRAINER_PIC_YOKAI_'+name+'] = sAnims_AquaLeaderArchie,'))
 edit('src/data/object_events/object_event_graphics.h',lambda s:s+'\nconst u16 gObjectEventPic_Yokai'+person+'[] = INCBIN_U16("'+path+'overworld.4bpp");\n')
 edit('src/data/object_events/object_event_graphics_info_pointers.h',lambda s:arr('const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Yokai'+person+';\n'+s,'gObjectEventGraphicsInfoPointers','    [OBJ_EVENT_GFX_YOKAI_'+name+'] = &gObjectEventGraphicsInfo_Yokai'+person+','))
 edit('src/data/object_events/object_event_pic_tables.h',lambda s:s+'\nstatic const struct SpriteFrameImage sPicTable_Yokai'+person+'[] = {\n'+''.join('    overworld_frame(gObjectEventPic_Yokai'+person+', '+str(width//8)+', 4, '+str(i)+'),\n' for i in range(3))+'};\n')
 def info(s):
  m=re.search(r'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Ariane = \{.*?\n\};',s,re.S);assert m
  t=m[0].replace('gObjectEventGraphicsInfo_Ariane','gObjectEventGraphicsInfo_Yokai'+person).replace('OBJ_EVENT_PAL_TAG_ARIANE','OBJ_EVENT_PAL_TAG_YOKAI_'+group+'_GROUP').replace('sPicTable_Ariane','sPicTable_Yokai'+person)
  if width==32:t=t.replace('.size = 256','.size = 512').replace('.width = 16','.width = 32').replace('16x32','32x32')
  return s+'\n'+t+'\n'
 edit('src/data/object_events/object_event_graphics_info.h',info)
 edit('spritesheet_rules.mk',lambda s:s+'\n'+path+'overworld.4bpp: '+path+'overworld.png\n\t$(GFX) $< $@ -mwidth '+str(width//8)+' -mheight 4\n')
for group,tag,folder,person in [('DOMNISCIAN',0x1124,'domniscian','Domniscian'),('MORLEONE',0x1125,'don_morleone','DonMorleone')]:
 constant='OBJ_EVENT_PAL_TAG_YOKAI_'+group+'_GROUP'
 edit('src/data/object_events/object_event_graphics.h',lambda s:s+'\nconst u16 gObjectEventPal_Yokai'+person+'Group[] = INCBIN_U16("graphics/yokai_characters/'+folder+'/normal.gbapal");\n')
 def palettes(s):
  s=s.replace('#define OBJ_EVENT_PAL_TAG_YOKAI_FRIEND','#define '+constant+' '+hex(tag)+'\n#define OBJ_EVENT_PAL_TAG_YOKAI_FRIEND',1)
  s=s.replace('    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},','    {gObjectEventPal_Yokai'+person+'Group, '+constant+'},\n    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},',1)
  s=s.replace('static const u16 sYokaiEnmaReflectionPaletteTags[] =','static const u16 sYokai'+person+'GroupReflectionPaletteTags[] = {'+', '.join([constant]*4)+'};\n\nstatic const u16 sYokaiEnmaReflectionPaletteTags[] =',1)
  return s.replace('    {OBJ_EVENT_PAL_TAG_YOKAI_ENMA,          sYokaiEnmaReflectionPaletteTags},','    {'+constant+', sYokai'+person+'GroupReflectionPaletteTags},\n    {OBJ_EVENT_PAL_TAG_YOKAI_ENMA,          sYokaiEnmaReflectionPaletteTags},',1)
 edit('src/event_object_movement.c',palettes)
slots=[('Domniscian','TRAINER_RICH_BOY',14,[(1,62),(5,63),(100,64),(8,64),(17,65),(9,66)]),('EmployeRouge','TRAINER_RS_POKEMANIAC',15,[(1,58),(28,60)]),('EmployeBleu','TRAINER_RS_SWIMMER_M',16,[(5,58),(17,60)]),('DonMorleone','TRAINER_RS_BLACK_BELT',17,[(147,66),(70,67),(140,68),(136,68),(115,69),(86,70)]),('Mafiamille1','TRAINER_GUITARIST',18,[(52,60)]),('Mafiamille2','TRAINER_KINDLER',19,[(38,61),(103,62)]),('Mafiamille3','TRAINER_RS_CAMPER',20,[(57,63),(141,64),(46,65)])]
lookup={int(v['numero_yokai']):v['species_constant'] for v in json.loads((R/'data/yokai/noms_affiches.json').read_text())};learns=list(csv.DictReader((R/'data/yokai/attaques_validees.csv').open(),delimiter=';'));teams=[]
for person,slot,idx,members in slots:
 assert not any(slot in p.read_text() for p in (R/'data/maps').glob('*/scripts.inc')),slot
 edit('include/constants/opponents.h',lambda s:s.replace('// Dummy trainers','#define TRAINER_YOKAI_'+person.upper()+' '+slot+'\n// Dummy trainers',1))
 symbol='sParty_Yokai'+person;part='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n';data=[]
 for n,level in members:
  moves=[]
  for row in learns:
   if int(row['numero_yokai'])==n and row['apprentissage']!='EVOLUTION_PLUS_2' and int(row['niveau'])<=level and row['move_id'] not in moves:moves=(moves+[row['move_id']])[-4:]
  moves+=['MOVE_NONE']*(4-len(moves));part+='    {.iv = 255, .lvl = '+str(level)+', .species = '+lookup[n]+', .heldItem = ITEM_NONE, .moves = {'+', '.join(moves)+'}},\n';data.append({'number':n,'species':lookup[n],'level':level,'moves':moves,'held_item':'ITEM_NONE'})
 part+='};\n';edit('src/data/trainer_parties.h',lambda s:s+'\n'+part);display=next(p[2] for p in people if p[0]==person)
 body='    ['+slot+'] = {\n        .trainerClass = TRAINER_CLASS_COOLTRAINER,\n        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,\n        .trainerPic = TRAINER_PIC_YOKAI_'+person.upper()+',\n        .trainerName = _("'+display+'"),\n        .items = {}, .doubleBattle = FALSE,\n        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES('+symbol+'),\n    },'
 def trainer(s):
  s,n=re.subn(r'    \['+slot+r'\] = \{.*?\n    \},',lambda m:body,s,count=1,flags=re.S);assert n==1;return s
 edit('src/data/trainers.h',trainer);teams.append({'person':person,'trainer_entry':'TRAINER_YOKAI_'+person.upper(),'trainer_id':idx,'display_name':display,'members':data})
actors=[{'name':'Domniscian','map':'SilphCo_11F','x':10,'y':14,'won':'FLAG_YOKAI_DOMNISCIAN_WON','need':['FLAG_YOKAI_EMPLOYEE_RED_WON','FLAG_YOKAI_EMPLOYEE_BLUE_WON'],'reward':('ITEM_THUNDER_STONE',1,'FLAG_YOKAI_DOMNISCIAN_REWARD')},
 {'name':'EmployeRouge','map':'SilphCo_11F','x':7,'y':14,'won':'FLAG_YOKAI_EMPLOYEE_RED_WON'},
 {'name':'EmployeBleu','map':'SilphCo_11F','x':12,'y':14,'won':'FLAG_YOKAI_EMPLOYEE_BLUE_WON'},
 {'name':'DonMorleone','map':'FiveIsland_RocketWarehouse','x':26,'y':23,'won':'FLAG_YOKAI_MORLEONE_WON','need':['FLAG_YOKAI_MAFIA1_WON','FLAG_YOKAI_MAFIA2_WON','FLAG_YOKAI_MAFIA3_WON'],'reward':('ITEM_NUGGET',3,'FLAG_YOKAI_MORLEONE_REWARD')},
 {'name':'Mafiamille1','map':'FiveIsland_RocketWarehouse','x':22,'y':22,'won':'FLAG_YOKAI_MAFIA1_WON'},
 {'name':'Mafiamille2','map':'FiveIsland_RocketWarehouse','x':24,'y':22,'won':'FLAG_YOKAI_MAFIA2_WON'},
 {'name':'Mafiamille3','map':'FiveIsland_RocketWarehouse','x':26,'y':21,'won':'FLAG_YOKAI_MAFIA3_WON'}]
text={
 'Domniscian':{'Offer':['Domniscian: Voici mon grand projet!','Un combat digne de mon génie?'],'Start':['Mes meilleurs collaborateurs!','Même les petits ont du talent!'],'Defeat':['Impossible! Mon idée était parfaite!'],'After':['D’accord, ton équipe mérite','une place au générique!'],'Need':['Mes employés veulent te rencontrer.','Bats-les avant de me défier!'],'Reward':['Cette Pierre Foudre fait évoluer','Komaous en Komastar.']},
 'EmployeRouge':{'Offer':['Je garde les projets du patron.','Tu veux faire un combat?'],'Start':['Jibanyan, Feulion! Au travail!'],'Defeat':['Pause bien méritée pour mon équipe!'],'After':['Belle démonstration!','Le patron va en entendre parler.']},
 'EmployeBleu':{'Offer':['Mon équipe vérifie ton niveau.','Tu acceptes le combat?'],'Start':['Komasan, Robonyan! À vous!'],'Defeat':['Notre rapport est clair: tu gagnes!'],'After':['Ton équipe est prête.','Garde cette énergie pour le patron!']},
 'DonMorleone':{'Offer':['Don Morleone: On m’a parlé de toi.','Un duel pour régler nos affaires?'],'Start':['Que personne ne nous dérange!'],'Defeat':['Tu as gagné. Nous réglerons ça...','avec un autre combat!'],'After':['Affaire conclue. Je respecte','les partenaires qui tiennent parole.'],'Need':['Ma famille doit d’abord te juger.','Reviens après leurs trois combats.'],'Reward':['Voici trois Pépites.','Une bonne affaire se paie comptant.']},
 'Mafiamille1':{'Offer':['Le patron reçoit sur rendez-vous.','Un combat pour commencer?'],'Start':['Bouh, on fait ça proprement!'],'Defeat':['J’ai sous-estimé ton équipe!'],'After':['Tu as passé mon contrôle.','Je préviens le patron.']},
 'Mafiamille2':{'Offer':['La famille teste chaque visiteur.','Tu veux tenter ta chance?'],'Start':['Gardons nos cartes en main!'],'Defeat':['Cette fois, tes cartes gagnent.'],'After':['Bien joué. On tient toujours','notre parole dans la famille.']},
 'Mafiamille3':{'Offer':['Pas de bagarre sans accord.','Un combat de Yo-kai, ça te va?'],'Start':['À nous de montrer notre force!'],'Defeat':['D’accord. On se calme!'],'After':['Tu as notre respect.','Va parler au patron.']}}
script='@ Optional postgame cameos; original story scripts remain in their maps.\n'
def msg(label,lines):
 return label+'::\n'+''.join('\t.string "'+line+('\\n' if i+1<len(lines) else '$')+'"\n' for i,line in enumerate(lines))
for a in actors:
 name=a['name'];prefix='YokaiCameo_'+name;reward=a.get('reward');script+='\n'+prefix+'::\n\tlock\n\tfaceplayer\n\tgoto_if_unset FLAG_SYS_GAME_CLEAR, '+prefix+'Blocked\n'
 for f in a.get('need',[]):script+='\tgoto_if_unset '+f+', '+prefix+'Need\n'
 if reward:script+='\tgoto_if_unset '+a['won']+', '+prefix+'Offer\n\tgoto_if_unset '+reward[2]+', '+prefix+'Reward\n'
 script+=prefix+'Offer::\n\tmsgbox '+prefix+'TextOffer, MSGBOX_YESNO\n\tgoto_if_eq VAR_RESULT, NO, '+prefix+'Decline\n\tclosemessage\n\tcleartrainerflag TRAINER_YOKAI_'+name.upper()+'\n\ttrainerbattle_single TRAINER_YOKAI_'+name.upper()+', '+prefix+'TextStart, '+prefix+'TextDefeat, '+prefix+'Victory\n\tgoto EventScript_ReleaseEnd\n'+prefix+'Victory::\n\tclosemessage\n\tsetflag '+a['won']+'\n\tmsgbox '+prefix+'TextAfter\n'
 if reward:
  item,count,flag=reward;script+='\tgoto_if_set '+flag+', EventScript_ReleaseEnd\n'+prefix+'Reward::\n\tcheckitemspace '+item+', '+str(count)+'\n\tgoto_if_eq VAR_RESULT, FALSE, '+prefix+'BagFull\n\tmsgbox '+prefix+'TextReward\n\tgiveitem '+item+', '+str(count)+'\n\tgoto_if_eq VAR_0x8007, FALSE, '+prefix+'BagFull\n\tsetflag '+flag+'\n'
 script+='\tgoto EventScript_ReleaseEnd\n'
 for suffix,label in [('Decline','TextDecline'),('Blocked','TextBlocked')]+([('Need','TextNeed')] if a.get('need') else [])+([('BagFull','TextBagFull')] if reward else []):script+=prefix+suffix+'::\n\tmsgbox '+prefix+label+'\n\tgoto EventScript_ReleaseEnd\n'
 texts=dict(text[name]);texts.update({'Decline':['Pas de souci. Une autre fois.'],'Blocked':['Reviens après ta victoire','à la Ligue de Kanto.']})
 if reward:texts['BagFull']=['Ton sac est plein.','Je garde ta récompense pour toi.']
 for suffix,lines in texts.items():script+=msg(prefix+'Text'+suffix,lines)
(R/'data/scripts/yokai_cameos_boss.inc').write_text(script)
edit('data/event_scripts.s',lambda s:s+'\n\t.include "data/scripts/yokai_cameos_boss.inc"\n')
for mapname,group in [('SilphCo_11F','DOMNISCIAN'),('FiveIsland_RocketWarehouse','MORLEONE')]:
 helper=mapname+'_OnTransitionYokaiBosses';hide='FLAG_HIDE_YOKAI_'+group+'_GROUP'
 def mapscript(s):
  if mapname=='SilphCo_11F':s=s.replace(mapname+'_MapScripts::\n',mapname+'_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, '+helper+'\n',1)
  else:s=s.replace('\tsetworldmapflag FLAG_WORLD_MAP_FIVE_ISLAND_ROCKET_WAREHOUSE','\tsetworldmapflag FLAG_WORLD_MAP_FIVE_ISLAND_ROCKET_WAREHOUSE\n\tcall '+helper,1)
  return s+'\n'+helper+'::\n\tsetflag '+hide+'\n\tgoto_if_unset FLAG_SYS_GAME_CLEAR, '+helper+'Return\n\tclearflag '+hide+'\n'+helper+'Return::\n\t'+('end' if mapname=='SilphCo_11F' else 'return')+'\n'
 edit('data/maps/'+mapname+'/scripts.inc',mapscript)
 p=R/'data/maps'/mapname/'map.json';m=json.loads(p.read_text())
 for a in actors:
  if a['map']!=mapname:continue
  m['object_events'].append({'type':'object','local_id':'LOCALID_YOKAI_'+a['name'].upper(),'graphics_id':'OBJ_EVENT_GFX_YOKAI_'+a['name'].upper(),'x':a['x'],'y':a['y'],'elevation':3,'movement_type':'MOVEMENT_TYPE_FACE_DOWN','movement_range_x':0,'movement_range_y':0,'trainer_type':'TRAINER_TYPE_NONE','trainer_sight_or_berry_tree_id':'0','script':'YokaiCameo_'+a['name'],'flag':hide})
 p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
registry=R/'data/yokai/registre_identifiants.json';v=json.loads(registry.read_text());v['flags'].update({k:hex(n) for k,n in flags.items()});v['trainer_slots'].update({'TRAINER_YOKAI_'+n.upper():i for n,_,i,_ in slots});v['palette_tags'].update({'DOMNISCIAN_GROUP':'0x1124','MORLEONE_GROUP':'0x1125'})
for p,_,_,pic,obj,_,_ in people:v['graphics'].update({'TRAINER_PIC_YOKAI_'+p.upper():pic,'OBJ_EVENT_GFX_YOKAI_'+p.upper():obj})
registry.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
(R/'data/yokai/cameos_boss.json').write_text(json.dumps({'specification':'CAMEOS_YOKAI_WATCH_CODEX.md §3.1/3.2 plus MUSIQUES_QUETES approved creative choices','teams':teams,'actors':actors,'flags':flags,'graphics':[{'person':p,'folder':f,'display_name':d,'trainer_pic':pic,'object_gfx':obj,'ow_width':w,'palette_group':g} for p,f,d,pic,obj,w,g in people],'postgame_only':True,'secondary_choices':'IV parameter255, primary ability, last four validated moves at level, no held items or trainer bag; levels within approved ranges','rematches':'All optional encounters repeatable; prerequisite wins persist, boss rewards unique and full-bag safe','name_constraint':'Trainer name array12 bytes including EOS; Don Morleone displayed Don Morleo. in battle, full name in dialogue','placement_constraint':'Warehouse group on southeast entry-room floor, outside arrow tiles and exit, to preserve Rocket maze and Gideon; no new map or original event replacement','music_status':'Original engine placeholder; personal Hinozall/Ghoulfather DPCM themes still pending, no generic Sangokushi substitution'},ensure_ascii=False,indent=2)+'\n')

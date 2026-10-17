#!/usr/bin/env python3
"""One-time original Nathaniel/Michael and Wyatt cameo installation, approved teams."""
import csv,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
assert 'TRAINER_PIC_YOKAI_NATHANIEL' not in (R/'include/constants/trainers.h').read_text(),'Already installed'
def edit(path,fn):
 p=R/path;p.write_text(fn(p.read_text()))
def arr(s,name,row):
 m=re.search(r'('+name+r'\[[^]]*\][^=]*=\s*\{)(.*?)(\n\};)',s,re.S);assert m,name
 return s[:m.end(2)]+'\n'+row+s[m.end(2):]
people=[('Nathaniel',150,158,0x1121),('Michael',151,159,0x1122),('Wyatt',152,160,0x1123)]
flags={'FLAG_YOKAI_ANCESTOR_WON':0x30B,'FLAG_YOKAI_ANCESTOR_REWARD':0x30C,'FLAG_YOKAI_ANCESTOR_POST_WON':0x30D,'FLAG_HIDE_YOKAI_NATHANIEL':0x30E,'FLAG_HIDE_YOKAI_MICHAEL':0x30F,'FLAG_YOKAI_WYATT_WON':0x310,'FLAG_YOKAI_WYATT_REWARD':0x311,'FLAG_YOKAI_WYATT_POST_WON':0x312}
slots=[('NATHANIEL','TRAINER_RS_TUBER_M',8),('NATHANIEL_POST','TRAINER_RS_COOLTRAINER_M',9),('MICHAEL','TRAINER_RS_COOLTRAINER_F',10),('MICHAEL_POST','TRAINER_HEX_MANIAC',11),('WYATT','TRAINER_RS_LADY',12),('WYATT_POST','TRAINER_RS_BEAUTY',13)]
for _,slot,_ in slots:assert not any(slot in p.read_text() for p in (R/'data/maps').glob('*/scripts.inc')),slot
edit('include/constants/opponents.h',lambda s:s.replace('// Dummy trainers','\n'.join('#define TRAINER_YOKAI_'+n+' '+slot for n,slot,_ in slots)+'\n// Dummy trainers',1))
edit('include/constants/flags.h',lambda s:s.replace('#endif // GUARD_CONSTANTS_FLAGS_H','\n'.join('#define '+k+' '+hex(v) for k,v in flags.items())+'\n\n#endif // GUARD_CONSTANTS_FLAGS_H'))
edit('include/constants/trainers.h',lambda s:s.replace('#define TRAINER_PIC_YOKAI_ENMA', '\n'.join('#define TRAINER_PIC_YOKAI_'+p.upper()+' '+str(pic) for p,pic,_,_ in people)+'\n#define TRAINER_PIC_YOKAI_ENMA',1))
edit('include/constants/event_objects.h',lambda s:s.replace('#define NUM_OBJ_EVENT_GFX     158','\n'.join('#define OBJ_EVENT_GFX_YOKAI_'+p.upper()+' '+str(obj) for p,_,obj,_ in people)+'\n#define NUM_OBJ_EVENT_GFX     161'))
for person,pic,obj,tag in people:
 name=person.upper();path='graphics/yokai_characters/'+person.lower()+'/'
 edit('include/graphics.h',lambda s:s.replace('extern const u32 gTrainerFrontPic_RivalEarly[];','extern const u32 gTrainerFrontPic_Yokai'+person+'[];\nextern const u32 gTrainerPalette_Yokai'+person+'[];\nextern const u32 gTrainerFrontPic_RivalEarly[];',1))
 edit('src/data/graphics/trainers.h',lambda s:s+'\nconst u32 gTrainerFrontPic_Yokai'+person+'[] = INCBIN_U32("'+path+'battle.4bpp.lz");\nconst u32 gTrainerPalette_Yokai'+person+'[] = INCBIN_U32("'+path+'normal.gbapal.lz");\n')
 def battle(s):
  for name2,row in [('gTrainerFrontPicCoords','    [TRAINER_PIC_YOKAI_'+name+'] = {.size = 8, .y_offset = 1},'),('gTrainerFrontPicTable','    TRAINER_SPRITE(YOKAI_'+name+', gTrainerFrontPic_Yokai'+person+', 0x800),'),('gTrainerFrontPicPaletteTable','    TRAINER_PAL(YOKAI_'+name+', gTrainerPalette_Yokai'+person+'),')]:s=arr(s,name2,row)
  return s
 edit('src/data/trainer_graphics/front_pic_tables.h',battle)
 edit('src/data/trainer_graphics/front_pic_anims.h',lambda s:arr(s,'gTrainerFrontAnimsPtrTable','    [TRAINER_PIC_YOKAI_'+name+'] = sAnims_AquaLeaderArchie,'))
 edit('src/data/object_events/object_event_graphics.h',lambda s:s+'\nconst u16 gObjectEventPal_Yokai'+person+'[] = INCBIN_U16("'+path+'normal.gbapal");\nconst u16 gObjectEventPic_Yokai'+person+'[] = INCBIN_U16("'+path+'overworld.4bpp");\n')
 edit('src/data/object_events/object_event_graphics_info_pointers.h',lambda s:arr('const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Yokai'+person+';\n'+s,'gObjectEventGraphicsInfoPointers','    [OBJ_EVENT_GFX_YOKAI_'+name+'] = &gObjectEventGraphicsInfo_Yokai'+person+','))
 edit('src/data/object_events/object_event_pic_tables.h',lambda s:s+'\nstatic const struct SpriteFrameImage sPicTable_Yokai'+person+'[] = {\n'+''.join('    overworld_frame(gObjectEventPic_Yokai'+person+', 2, 4, '+str(i)+'),\n' for i in range(3))+'};\n')
 def info(s):
  m=re.search(r'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Ariane = \{.*?\n\};',s,re.S);assert m
  return s+'\n'+m[0].replace('gObjectEventGraphicsInfo_Ariane','gObjectEventGraphicsInfo_Yokai'+person).replace('OBJ_EVENT_PAL_TAG_ARIANE','OBJ_EVENT_PAL_TAG_YOKAI_'+name).replace('sPicTable_Ariane','sPicTable_Yokai'+person)+'\n'
 edit('src/data/object_events/object_event_graphics_info.h',info)
 def palettes(s):
  constant='OBJ_EVENT_PAL_TAG_YOKAI_'+name
  s=s.replace('#define OBJ_EVENT_PAL_TAG_YOKAI_FRIEND', '#define '+constant+' '+hex(tag)+'\n#define OBJ_EVENT_PAL_TAG_YOKAI_FRIEND',1)
  s=s.replace('    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},','    {gObjectEventPal_Yokai'+person+', '+constant+'},\n    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},',1)
  s=s.replace('static const u16 sYokaiEnmaReflectionPaletteTags[] =','static const u16 sYokai'+person+'ReflectionPaletteTags[] = {'+', '.join([constant]*4)+'};\n\nstatic const u16 sYokaiEnmaReflectionPaletteTags[] =',1)
  s=s.replace('    {OBJ_EVENT_PAL_TAG_YOKAI_ENMA,          sYokaiEnmaReflectionPaletteTags},','    {'+constant+', sYokai'+person+'ReflectionPaletteTags},\n    {OBJ_EVENT_PAL_TAG_YOKAI_ENMA,          sYokaiEnmaReflectionPaletteTags},',1)
  return s
 edit('src/event_object_movement.c',palettes)
 edit('spritesheet_rules.mk',lambda s:s+'\n'+path+'overworld.4bpp: '+path+'overworld.png\n\t$(GFX) $< $@ -mwidth 2 -mheight 4\n')
lookup={int(v['numero_yokai']):v['species_constant'] for v in json.loads((R/'data/yokai/noms_affiches.json').read_text())};learns=list(csv.DictReader((R/'data/yokai/attaques_validees.csv').open(),delimiter=';'));teams=[]
for name,slot,idx in slots:
 post=name.endswith('_POST');person=name.split('_')[0].title();wyatt=person=='Wyatt'
 if wyatt:members=[(21,61),(51,62),(116,63),(97,64),(133,65),(146,66)] if post else [(21,42),(117,42),(121,43),(146,44),(93,44),(96,45)]
 else:members=[(149,59),(148,60),(35,61),(67,62),(20,63),(40,64)] if post else [(149,34),(52,33),(20,33),(34,34),(66,35)]
 symbol='sParty_Yokai'+person+('Post' if post else '');part='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n';data=[]
 for n,level in members:
  moves=[]
  for row in learns:
   if int(row['numero_yokai'])==n and row['apprentissage']!='EVOLUTION_PLUS_2' and int(row['niveau'])<=level and row['move_id'] not in moves:moves=(moves+[row['move_id']])[-4:]
  moves+=['MOVE_NONE']*(4-len(moves));part+='    {.iv = '+str(200 if post else 150)+', .lvl = '+str(level)+', .species = '+lookup[n]+', .heldItem = ITEM_NONE, .moves = {'+', '.join(moves)+'}},\n';data.append({'number':n,'species':lookup[n],'level':level,'moves':moves,'held_item':'ITEM_NONE'})
 part+='};\n';edit('src/data/trainer_parties.h',lambda s:s+'\n'+part)
 body='    ['+slot+'] = {\n        .trainerClass = TRAINER_CLASS_COOLTRAINER,\n        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,\n        .trainerPic = TRAINER_PIC_YOKAI_'+person.upper()+',\n        .trainerName = _("'+person+'"),\n        .items = {}, .doubleBattle = FALSE,\n        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES('+symbol+'),\n    },'
 def trainer(s):
  s,n=re.subn(r'    \['+slot+r'\] = \{.*?\n    \},',lambda m:body,s,count=1,flags=re.S);assert n==1;return s
 edit('src/data/trainers.h',trainer);teams.append({'trainer_entry':'TRAINER_YOKAI_'+name,'trainer_id':idx,'person':person,'postgame':post,'members':data})
# Reuse proven optional/reward script structure, with group-specific text and teams.
base=(R/'data/maps/CeladonCity/scripts.inc').read_text();base=base[base.index('CeladonCity_EventScript_YokaiFriend::'):]
for city,group,types in [('FuchsiaCity','Ancestor',['Nathaniel','Michael']),('CinnabarIsland','Wyatt',['Wyatt'])]:
 script=base.replace('CeladonCity',''+city).replace('YokaiFriend','Yokai'+group).replace('YOKAI_FRIEND','YOKAI_'+('ANCESTOR' if group=='Ancestor' else 'WYATT'))
 if group=='Ancestor':
  script=script.replace('KATIE','NATHANIEL').replace('Katie','Nathaniel').replace('NATHAN','MICHAEL').replace('Nathan','Michael') if False else script
  script=script.replace('KATIE','_FIRST_').replace('Katie','_First_').replace('NATHAN','MICHAEL').replace('Nathan','Michael').replace('_FIRST_','NATHANIEL').replace('_First_','Nathaniel')
  script=script.replace('Jibanyan, à toi de jouer!','Hovernyan, à toi de jouer!').replace('Jibanyan peut évoluer avec elle!','Pour faire évoluer ton Jibanyan!')
  intro='''
FuchsiaCity_OnTransitionYokaiAncestor::
	setflag FLAG_HIDE_YOKAI_NATHANIEL
	setflag FLAG_HIDE_YOKAI_MICHAEL
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, FuchsiaCity_ShowMichael
	clearflag FLAG_HIDE_YOKAI_NATHANIEL
	return
FuchsiaCity_ShowMichael::
	clearflag FLAG_HIDE_YOKAI_MICHAEL
	return
'''
  edit('data/maps/'+city+'/scripts.inc',lambda s:s.replace('\tsetworldmapflag FLAG_WORLD_MAP_FUCHSIA_CITY','\tsetworldmapflag FLAG_WORLD_MAP_FUCHSIA_CITY\n\tcall FuchsiaCity_OnTransitionYokaiAncestor',1)+intro+script)
 else:
  # Both genders share Wyatt. Remove gender dispatch and unused duplicate branch.
  script=script.replace('\tcheckplayergender\n\tgoto_if_eq VAR_RESULT, FEMALE, CinnabarIsland_YokaiWyattNathan\n','').replace('KATIE','WYATT').replace('Katie','Wyatt')
  a=script.index('CinnabarIsland_YokaiWyattNathan::');b=script.index('CinnabarIsland_YokaiWyattPostVictory::',a);script=script[:a]+script[b:]
  script=script.replace('ITEM_LEAF_STONE','ITEM_WATER_STONE').replace('Jibanyan, à toi de jouer!','Tukappa, à toi de jouer!').replace('Pierre Plante','Pierre Eau').replace('Jibanyan peut évoluer avec elle!','Faux Kappa évolue grâce à elle!').replace('Jibanyan et moi allons continuer','Tukappa et moi allons continuer')
  edit('data/maps/'+city+'/scripts.inc',lambda s:s+script)
 mpath=R/'data/maps'/city/'map.json';m=json.loads(mpath.read_text());coords=(27,8) if group=='Ancestor' else (9,11)
 for person in types:
  obj={'local_id':'LOCALID_'+city.upper()+'_YOKAI_'+person.upper(),'type':'object','graphics_id':'OBJ_EVENT_GFX_YOKAI_'+person.upper(),'x':coords[0],'y':coords[1],'elevation':3,'movement_type':'MOVEMENT_TYPE_FACE_DOWN','movement_range_x':0,'movement_range_y':0,'trainer_type':'TRAINER_TYPE_NONE','trainer_sight_or_berry_tree_id':'0','script':city+'_EventScript_Yokai'+group,'flag':'0' if group=='Wyatt' else 'FLAG_HIDE_YOKAI_'+person.upper()};m['object_events'].append(obj)
 mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
registry=R/'data/yokai/registre_identifiants.json';v=json.loads(registry.read_text());v['flags'].update({k:hex(n) for k,n in flags.items()});v['trainer_slots'].update({'TRAINER_YOKAI_'+n:i for n,_,i in slots})
for p,pic,obj,tag in people:v['graphics'].update({'TRAINER_PIC_YOKAI_'+p.upper():pic,'OBJ_EVENT_GFX_YOKAI_'+p.upper():obj});v['palette_tags'][p.upper()]=hex(tag)
registry.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
(R/'data/yokai/cameos_aventure.json').write_text(json.dumps({'specification':'CAMEOS_YOKAI_WATCH_CODEX.md §2.3/2.4, canonical151 names, explicit reward override: Leaf Stone for Jibanyan instead of nonexistent Sirenee stone evolution','teams':teams,'locations':{'FuchsiaCity':[27,8],'CinnabarIsland':[9,11]},'rewards':{'Ancestor':'ITEM_LEAF_STONE','Wyatt':'ITEM_WATER_STONE'},'appearance':'Male player -> Nathaniel, female -> Michael; Wyatt identical for both','battle_policy':'Optional Yes/No, adventure once, direct postgame team if first visit late, unlimited postgame rematches; unique reward retry if bag full','secondary_choices':'IV parameter150/200, primary ability, last four available validated moves, no held items or bag; post levels59..64 /61..66','graphics':'Original source sheet and native 64x64 /three16x32 stationary facings; no invented walking cycle or shared NPC palette changes'},ensure_ascii=False,indent=2)+'\n')

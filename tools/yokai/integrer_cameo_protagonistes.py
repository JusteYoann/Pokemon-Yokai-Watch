#!/usr/bin/env python3
"""One-time integration of the approved opposite-protagonist Celadon cameo."""
import csv,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
assert 'TRAINER_YOKAI_KATIE' not in (R/'include/constants/opponents.h').read_text(),'Already integrated'
def edit(p,fn):
 p=R/p;p.write_text(fn(p.read_text()))
def append_array(s,name,row):
 m=re.search(r'('+name+r'\[[^]]*\][^=]*=\s*\{)(.*?)(\n\};)',s,re.S);assert m,name
 return s[:m.end(2)]+'\n'+row+s[m.end(2):]
slots=[('KATIE','TRAINER_RS_AROMA_LADY',4),('KATIE_POST','TRAINER_RS_RUIN_MANIAC',5),('NATHAN','TRAINER_INTERVIEWER',6),('NATHAN_POST','TRAINER_RS_TUBER_F',7)]
# Guard: placeholder slots were unused by scripts before this addition.
for _,slot,_ in slots:
 assert not any(slot in p.read_text() for p in (R/'data/maps').glob('*/scripts.inc')),slot
edit('include/constants/opponents.h',lambda s:s.replace('// Dummy trainers', '\n'.join('#define TRAINER_YOKAI_'+name+' '+slot for name,slot,_ in slots)+'\n// Dummy trainers',1))
flagmap={'FLAG_YOKAI_FRIEND_WON':0x306,'FLAG_YOKAI_FRIEND_REWARD':0x307,'FLAG_YOKAI_FRIEND_POST_WON':0x308,'FLAG_HIDE_YOKAI_NATHAN':0x309,'FLAG_HIDE_YOKAI_KATIE':0x30A}
edit('include/constants/flags.h',lambda s:s.replace('#endif // GUARD_CONSTANTS_FLAGS_H','\n'.join('#define '+k+' '+hex(v) for k,v in flagmap.items())+'\n\n#endif // GUARD_CONSTANTS_FLAGS_H'))
edit('include/constants/event_objects.h',lambda s:s.replace('#define NUM_OBJ_EVENT_GFX     156','#define OBJ_EVENT_GFX_YOKAI_NATHAN 156\n#define OBJ_EVENT_GFX_YOKAI_KATIE 157\n#define NUM_OBJ_EVENT_GFX     158'))
# Separate NPC identities use the approved original protagonist drawings, not player flags.
edit('src/data/object_events/object_event_graphics_info_pointers.h',lambda s:append_array('const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_YokaiNathan;\nconst struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_YokaiKatie;\n'+s,'gObjectEventGraphicsInfoPointers','    [OBJ_EVENT_GFX_YOKAI_NATHAN] = &gObjectEventGraphicsInfo_YokaiNathan,\n    [OBJ_EVENT_GFX_YOKAI_KATIE] = &gObjectEventGraphicsInfo_YokaiKatie,'))
def info(s):
 m=re.search(r'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Woman1 = \{.*?\n\};',s,re.S);assert m
 for person,color in [('Nathan','Red'),('Katie','Green')]:
  t=m[0].replace('gObjectEventGraphicsInfo_Woman1','gObjectEventGraphicsInfo_Yokai'+person).replace('OBJ_EVENT_PAL_TAG_NPC_GREEN','OBJ_EVENT_PAL_TAG_YOKAI_FRIEND').replace('PALSLOT_NPC_3','PALSLOT_NPC_SPECIAL').replace('sPicTable_Woman1','sPicTable_'+color+'Normal')
  s+='\n'+t+'\n'
 return s
edit('src/data/object_events/object_event_graphics_info.h',info)
def palettes(s):
 s=s.replace('#define OBJ_EVENT_PAL_TAG_YOKAI_PLAYER_BRIDGE', '#define OBJ_EVENT_PAL_TAG_YOKAI_FRIEND                 0x1120\n#define OBJ_EVENT_PAL_TAG_YOKAI_PLAYER_BRIDGE',1)
 s=s.replace('    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},','    {gObjectEventPal_Player, OBJ_EVENT_PAL_TAG_YOKAI_FRIEND},\n    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},',1)
 s=s.replace('static const u16 sYokaiEnmaReflectionPaletteTags[] =','static const u16 sYokaiFriendReflectionPaletteTags[] = {OBJ_EVENT_PAL_TAG_YOKAI_FRIEND, OBJ_EVENT_PAL_TAG_YOKAI_FRIEND, OBJ_EVENT_PAL_TAG_YOKAI_FRIEND, OBJ_EVENT_PAL_TAG_YOKAI_FRIEND};\n\nstatic const u16 sYokaiEnmaReflectionPaletteTags[] =',1)
 s=s.replace('    {OBJ_EVENT_PAL_TAG_YOKAI_ENMA,          sYokaiEnmaReflectionPaletteTags},','    {OBJ_EVENT_PAL_TAG_YOKAI_ENMA,          sYokaiEnmaReflectionPaletteTags},\n    {OBJ_EVENT_PAL_TAG_YOKAI_FRIEND,        sYokaiFriendReflectionPaletteTags},',1)
 return s
edit('src/event_object_movement.c',palettes)
lookup={int(v['numero_yokai']):v['species_constant'] for v in json.loads((R/'data/yokai/noms_affiches.json').read_text())}
learns=list(csv.DictReader((R/'data/yokai/attaques_validees.csv').open(),delimiter=';'))
metadata=[]
for name,slot,number in slots:
 post=name.endswith('_POST');person='Katie' if name.startswith('KATIE') else 'Nathan'
 members=[(4,58),(88,59),(126,60),(8,61),(6,62),(50,63)] if post else [(1,29),(8,28),(5,28),(87,29),(49,30)]
 symbol='sParty_Yokai'+person+('Post' if post else '')
 part='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n';data=[]
 for n,level in members:
  moves=[]
  for row in learns:
   if int(row['numero_yokai'])==n and row['apprentissage']!='EVOLUTION_PLUS_2' and int(row['niveau'])<=level and row['move_id'] not in moves:moves=(moves+[row['move_id']])[-4:]
  moves+=['MOVE_NONE']*(4-len(moves))
  part+='    {.iv = '+str(200 if post else 150)+', .lvl = '+str(level)+', .species = '+lookup[n]+', .heldItem = ITEM_NONE, .moves = {'+', '.join(moves)+'}},\n'
  data.append({'number':n,'species':lookup[n],'level':level,'moves':moves,'held_item':'ITEM_NONE'})
 part+='};\n';edit('src/data/trainer_parties.h',lambda s:s+'\n'+part)
 female=person=='Katie'
 body='    ['+slot+'] = {\n        .trainerClass = TRAINER_CLASS_COOLTRAINER,\n        .encounterMusic_gender = '+('TRAINER_ENCOUNTER_MUSIC_FEMALE | F_TRAINER_FEMALE' if female else 'TRAINER_ENCOUNTER_MUSIC_MALE')+',\n        .trainerPic = '+('TRAINER_PIC_LEAF' if female else 'TRAINER_PIC_RED')+',\n        .trainerName = _("'+person+'"),\n        .items = {}, .doubleBattle = FALSE,\n        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n        .party = ITEM_CUSTOM_MOVES('+symbol+'),\n    },'
 def trainer(s):
  s,n=re.subn(r'    \['+slot+r'\] = \{.*?\n    \},',lambda m:body,s,count=1,flags=re.S);assert n==1;return s
 edit('src/data/trainers.h',trainer)
 metadata.append({'trainer_entry':'TRAINER_YOKAI_'+name,'trainer_id':number,'person':person,'postgame':post,'members':data})
script='''
CeladonCity_OnTransitionYokaiFriend::
	setflag FLAG_HIDE_YOKAI_NATHAN
	setflag FLAG_HIDE_YOKAI_KATIE
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CeladonCity_ShowNathan
	clearflag FLAG_HIDE_YOKAI_KATIE
	return
CeladonCity_ShowNathan::
	clearflag FLAG_HIDE_YOKAI_NATHAN
	return

CeladonCity_EventScript_YokaiFriend::
	lock
	faceplayer
	goto_if_unset FLAG_YOKAI_FRIEND_WON, CeladonCity_YokaiFriendOffer
	goto_if_unset FLAG_YOKAI_FRIEND_REWARD, CeladonCity_YokaiFriendReward
	goto_if_unset FLAG_SYS_GAME_CLEAR, CeladonCity_YokaiFriendAlreadyWon
CeladonCity_YokaiFriendOffer::
	msgbox CeladonCity_Text_YokaiFriendOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CeladonCity_YokaiFriendDecline
	closemessage
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CeladonCity_YokaiFriendNathan
	goto_if_set FLAG_SYS_GAME_CLEAR, CeladonCity_YokaiFriendKatiePost
	trainerbattle_single TRAINER_YOKAI_KATIE, CeladonCity_Text_YokaiFriendStart, CeladonCity_Text_YokaiFriendDefeat, CeladonCity_YokaiFriendVictory
	goto EventScript_ReleaseEnd
CeladonCity_YokaiFriendKatiePost::
	cleartrainerflag TRAINER_YOKAI_KATIE_POST
	trainerbattle_single TRAINER_YOKAI_KATIE_POST, CeladonCity_Text_YokaiFriendPostStart, CeladonCity_Text_YokaiFriendDefeat, CeladonCity_YokaiFriendPostVictory
	goto EventScript_ReleaseEnd
CeladonCity_YokaiFriendNathan::
	goto_if_set FLAG_SYS_GAME_CLEAR, CeladonCity_YokaiFriendNathanPost
	trainerbattle_single TRAINER_YOKAI_NATHAN, CeladonCity_Text_YokaiFriendStart, CeladonCity_Text_YokaiFriendDefeat, CeladonCity_YokaiFriendVictory
	goto EventScript_ReleaseEnd
CeladonCity_YokaiFriendNathanPost::
	cleartrainerflag TRAINER_YOKAI_NATHAN_POST
	trainerbattle_single TRAINER_YOKAI_NATHAN_POST, CeladonCity_Text_YokaiFriendPostStart, CeladonCity_Text_YokaiFriendDefeat, CeladonCity_YokaiFriendPostVictory
	goto EventScript_ReleaseEnd
CeladonCity_YokaiFriendPostVictory::
	setflag FLAG_YOKAI_FRIEND_POST_WON
CeladonCity_YokaiFriendVictory::
	closemessage
	setflag FLAG_YOKAI_FRIEND_WON
	msgbox CeladonCity_Text_YokaiFriendAfter
	goto_if_set FLAG_YOKAI_FRIEND_REWARD, EventScript_ReleaseEnd
CeladonCity_YokaiFriendReward::
	checkitemspace ITEM_LEAF_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, CeladonCity_YokaiFriendBagFull
	msgbox CeladonCity_Text_YokaiFriendReward
	giveitem ITEM_LEAF_STONE, 1
	goto_if_eq VAR_0x8007, FALSE, CeladonCity_YokaiFriendBagFull
	setflag FLAG_YOKAI_FRIEND_REWARD
	goto EventScript_ReleaseEnd
CeladonCity_YokaiFriendAlreadyWon::
	msgbox CeladonCity_Text_YokaiFriendRevisit
	goto EventScript_ReleaseEnd
CeladonCity_YokaiFriendDecline::
	msgbox CeladonCity_Text_YokaiFriendDecline
	goto EventScript_ReleaseEnd
CeladonCity_YokaiFriendBagFull::
	msgbox CeladonCity_Text_YokaiFriendBagFull
	goto EventScript_ReleaseEnd

CeladonCity_Text_YokaiFriendOffer::
	.string "Toi aussi, tu voyages avec des\\n"
	.string "Yo-kai? Mes amis sont en forme!\\p"
	.string "Ça te dit de faire un combat?$"
CeladonCity_Text_YokaiFriendStart::
	.string "Jibanyan, à toi de jouer!$"
CeladonCity_Text_YokaiFriendPostStart::
	.string "Notre équipe a bien grandi!\\n"
	.string "Montrons nos progrès!$"
CeladonCity_Text_YokaiFriendDefeat::
	.string "Quelle belle équipe!\\n"
	.string "On a encore tant à apprendre!$"
CeladonCity_Text_YokaiFriendAfter::
	.string "Merci pour ce combat!\\n"
	.string "Nos amis ont tout donné.$"
CeladonCity_Text_YokaiFriendReward::
	.string "Prends cette Pierre Plante.\\n"
	.string "Jibanyan peut évoluer avec elle!$"
CeladonCity_Text_YokaiFriendRevisit::
	.string "Jibanyan et moi allons continuer\\n"
	.string "notre voyage. Après la Ligue,\\p"
	.string "on fera un autre combat!$"
CeladonCity_Text_YokaiFriendDecline::
	.string "Pas de problème!\\n"
	.string "Reviens quand tu voudras.$"
CeladonCity_Text_YokaiFriendBagFull::
	.string "Ton sac est plein.\\n"
	.string "Je garde ta pierre pour plus tard!$"
'''
edit('data/maps/CeladonCity/scripts.inc',lambda s:s.replace('\tsetworldmapflag FLAG_WORLD_MAP_CELADON_CITY\n\tend','\tsetworldmapflag FLAG_WORLD_MAP_CELADON_CITY\n\tcall CeladonCity_OnTransitionYokaiFriend\n\tend',1)+script)
p=R/'data/maps/CeladonCity/map.json';m=json.loads(p.read_text());before=len(m['object_events'])
for person in ['Nathan','Katie']:
 m['object_events'].append({'local_id':'LOCALID_CELADON_YOKAI_'+person.upper(),'type':'object','graphics_id':'OBJ_EVENT_GFX_YOKAI_'+person.upper(),'x':25,'y':13,'elevation':3,'movement_type':'MOVEMENT_TYPE_FACE_DOWN','movement_range_x':0,'movement_range_y':0,'trainer_type':'TRAINER_TYPE_NONE','trainer_sight_or_berry_tree_id':'0','script':'CeladonCity_EventScript_YokaiFriend','flag':'FLAG_HIDE_YOKAI_'+person.upper()})
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
registry=R/'data/yokai/registre_identifiants.json';v=json.loads(registry.read_text());v['flags'].update({k:hex(n) for k,n in flagmap.items()});v['trainer_slots'].update({'TRAINER_YOKAI_'+n:i for n,_,i in slots});v['graphics'].update({'OBJ_EVENT_GFX_YOKAI_NATHAN':156,'OBJ_EVENT_GFX_YOKAI_KATIE':157});v['palette_tags']['NATHAN_KATIE_CAMEO']='0x1120';registry.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
(R/'data/yokai/cameo_protagonistes.json').write_text(json.dumps({'specification':'CAMEOS_YOKAI_WATCH_CODEX.md §2.2, approved protagonist references','location':'CeladonCity','coordinates':[25,13],'original_objects_preserved':before,'appearance':'Male player -> Katie; female player -> Nathan; separate map graphics IDs, common original player artwork palette with dedicated NPC tag','teams':metadata,'reward':'ITEM_LEAF_STONE','reward_choice':'A valid Jibanyan evolution item (Epinyan); no evolution or species mapping change','battle_policy':'Optional Yes/No, adventure victory once, unlimited post-League rematches, direct postgame team on first late visit, unique reward retry on full bag','secondary_choices':'IV parameter150 adventure /200 post, primary abilities, last four available validated moves, no held items or bag, post levels58..63','not_complete':'Other cameo groups, quests, music and full progression remain'},ensure_ascii=False,indent=2)+'\n')

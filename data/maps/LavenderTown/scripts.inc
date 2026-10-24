LavenderTown_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, LavenderTown_OnTransition
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTown_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LavenderTown_Frame
	.byte 0
LavenderTown_OnTransition::
	special LavanvilleZombieImmunity
	setworldmapflag FLAG_WORLD_MAP_LAVENDER_TOWN
	setvar VAR_MAP_SCENE_S_S_ANNE_2F_CORRIDOR, 1
	setflag FLAG_HIDE_SS_ANNE_RIVAL
	goto_if_set FLAG_LAVENDER_INTRO_DONE, LavenderTown_LoadEnd
	setvar VAR_LAVENDER_INTRO, 0
LavenderTown_LoadEnd::
	end
LavenderTown_Frame::
	map_script_2 VAR_LAVENDER_INTRO, 0, LavenderIntro_Start
	.2byte 0
LavenderZombie_Home::
	msgbox LavenderZombie_Text_Home, MSGBOX_NPC
	end
LavenderTown_EventScript_TownSign::
	msgbox LavenderTown_Text_NewSign, MSGBOX_SIGN
	end
LavenderTown_EventScript_SilphScopeNotice::
LavenderTown_EventScript_PokemonTowerSign::
	msgbox LavenderTown_Text_NewTower, MSGBOX_SIGN
	end
LavenderTown_EventScript_VolunteerHouseSign::
	msgbox LavenderTown_Text_NewHouse, MSGBOX_SIGN
	end
LavenderZombie_Text_Home::
	.string "Grrr... Bienvenue...\nLa maison est à nous...$"

LavenderTown_Text_NewSign::
	.string "LAVANVILLE\nLa nuit ne finit jamais.$"

LavenderTown_Text_NewTower::
	.string "TOUR POKÉMON - ARÈNE\nChampionne: ALYZON BIE$"

LavenderTown_Text_NewHouse::
	.string "Une maison habitée...\npar des zombies!$"


LavenderZombie_Variant0::
	setvar VAR_0x8004, 0
	goto LavenderZombie_Errant

LavenderZombie_Variant1::
	setvar VAR_0x8004, 1
	goto LavenderZombie_Errant

LavenderZombie_Variant2::
	setvar VAR_0x8004, 2
	goto LavenderZombie_Errant

LavenderZombie_Variant3::
	setvar VAR_0x8004, 3
	goto LavenderZombie_Errant

LavenderZombie_Errant::
	lockall
	faceplayer
	specialvar VAR_RESULT, LavanvilleCheckZombieImmunity
	goto_if_eq VAR_RESULT, TRUE, LavenderZombie_Release
	special LavanvilleZombieApproach
	waitstate
	msgbox LavenderZombie_Growl
	closemessage
	special LavanvilleStartZombieBattle
	waitstate
	special LavanvilleZombieImmunity
LavenderZombie_Release::
	releaseall
	end

LavenderIntro_Start::
	lockall
	goto_if_set FLAG_LAVENDER_INTRO_DONE, LavenderIntro_AlreadyDone
	specialvar VAR_RESULT, LavanvillePrepareIntro
	copyvar VAR_0x8006, VAR_RESULT
	goto_if_eq VAR_RESULT, 0, LavenderIntro_Dialogue
	call LavenderIntro_ZombieApproach
	call LavenderIntro_AlyzonIntervenes
	msgbox LavenderIntro_Text_Stop
	call LavenderIntro_ZombieRetreat
	removeobject 200
LavenderIntro_Dialogue::
	call LavenderIntro_AlyzonFacesPlayer
	famechecker FAMECHECKER_ERIKA, FCPICKSTATE_COLORED, UpdatePickStateFromSpecialVar8005
	msgbox LavenderIntro_Text_Explain
	msgbox LavenderIntro_Text_Badge
	msgbox LavenderIntro_Text_Visitor
	msgbox LavenderIntro_Text_GoodLuck
	goto_if_eq VAR_0x8006, 0, LavenderIntro_Finish
	specialvar VAR_RESULT, LavanvilleIntroDepart
	goto_if_eq VAR_RESULT, FALSE, LavenderIntro_RemoveAlyzon
	waitstate
LavenderIntro_RemoveAlyzon::
	removeobject 201
LavenderIntro_Finish::
	setflag FLAG_LAVENDER_INTRO_DONE
	special LavanvilleZombieImmunity
LavenderIntro_AlreadyDone::
	setvar VAR_LAVENDER_INTRO, 1
	releaseall
	end

LavenderIntro_ZombieApproach::
	goto_if_eq VAR_0x8006, 1, LavenderIntro_ZombieApproach1
	goto_if_eq VAR_0x8006, 2, LavenderIntro_ZombieApproach2
	goto_if_eq VAR_0x8006, 3, LavenderIntro_ZombieApproach3
	goto_if_eq VAR_0x8006, 4, LavenderIntro_ZombieApproach4
	return
LavenderIntro_ZombieApproach1::
	applymovement 200, LavenderIntro_Movement_up
	waitmovement 0
	return
LavenderIntro_ZombieApproach2::
	applymovement 200, LavenderIntro_Movement_down
	waitmovement 0
	return
LavenderIntro_ZombieApproach3::
	applymovement 200, LavenderIntro_Movement_right
	waitmovement 0
	return
LavenderIntro_ZombieApproach4::
	applymovement 200, LavenderIntro_Movement_left
	waitmovement 0
	return

LavenderIntro_AlyzonIntervenes::
	goto_if_eq VAR_0x8006, 1, LavenderIntro_AlyzonIntervenes1
	goto_if_eq VAR_0x8006, 2, LavenderIntro_AlyzonIntervenes2
	goto_if_eq VAR_0x8006, 3, LavenderIntro_AlyzonIntervenes3
	goto_if_eq VAR_0x8006, 4, LavenderIntro_AlyzonIntervenes4
	return
LavenderIntro_AlyzonIntervenes1::
	applymovement 201, LavenderIntro_Movement_right
	waitmovement 0
	applymovement 201, LavenderIntro_Face_down
	waitmovement 0
	return
LavenderIntro_AlyzonIntervenes2::
	applymovement 201, LavenderIntro_Movement_left
	waitmovement 0
	applymovement 201, LavenderIntro_Face_up
	waitmovement 0
	return
LavenderIntro_AlyzonIntervenes3::
	applymovement 201, LavenderIntro_Movement_down
	waitmovement 0
	applymovement 201, LavenderIntro_Face_left
	waitmovement 0
	return
LavenderIntro_AlyzonIntervenes4::
	applymovement 201, LavenderIntro_Movement_up
	waitmovement 0
	applymovement 201, LavenderIntro_Face_right
	waitmovement 0
	return

LavenderIntro_ZombieRetreat::
	goto_if_eq VAR_0x8006, 1, LavenderIntro_ZombieRetreat1
	goto_if_eq VAR_0x8006, 2, LavenderIntro_ZombieRetreat2
	goto_if_eq VAR_0x8006, 3, LavenderIntro_ZombieRetreat3
	goto_if_eq VAR_0x8006, 4, LavenderIntro_ZombieRetreat4
	return
LavenderIntro_ZombieRetreat1::
	applymovement 200, LavenderIntro_Movement_down
	waitmovement 0
	return
LavenderIntro_ZombieRetreat2::
	applymovement 200, LavenderIntro_Movement_up
	waitmovement 0
	return
LavenderIntro_ZombieRetreat3::
	applymovement 200, LavenderIntro_Movement_left
	waitmovement 0
	return
LavenderIntro_ZombieRetreat4::
	applymovement 200, LavenderIntro_Movement_right
	waitmovement 0
	return
LavenderIntro_Movement_up::
	walk_up
	step_end
LavenderIntro_Movement_down::
	walk_down
	step_end
LavenderIntro_Movement_left::
	walk_left
	step_end
LavenderIntro_Movement_right::
	walk_right
	step_end
LavenderIntro_Text_Stop::
	.string "ALYZON: Doucement, mon mignon!\nOn ne saute pas sur les invités.$"

LavenderIntro_Text_Explain::
	.string "ALYZON: Tu découvres LAVANVILLE?\nIci, la nuit ne finit jamais.\p"
	.string "La ville est prisonnière d'une\nZombie Night éternelle!\p"
	.string "Moi? Je vis ici par choix!\nCes zombies sont si mignons!$"

LavenderIntro_Text_Badge::
	.string "Je suis ALYZON BIE,\nla Championne de LAVANVILLE!\p"
	.string "Tu es venu pour mon badge?\nJe m'en doutais!\p"
	.string "Un futur grand Dresseur ne va\npas trembler devant mes petits!$"

LavenderIntro_Text_Visitor::
	.string "Un visiteur est passé avant toi.\nTrès discret, mais redoutable!\p"
	.string "Il fait partie des rares à\nm'avoir battue en plus de cinq ans.\p"
	.string "Il parlait peu... Ses Yo-kai,\neux, savaient se faire entendre!$"

LavenderIntro_Text_GoodLuck::
	.string "Je t'attends au sommet de la Tour!\nBonne chance! Ouvre l'oeil!$"


LavenderIntro_AlyzonFacesPlayer::
	goto_if_eq VAR_0x8006, 1, LavenderIntro_LookPlayer1
	goto_if_eq VAR_0x8006, 2, LavenderIntro_LookPlayer2
	goto_if_eq VAR_0x8006, 3, LavenderIntro_LookPlayer3
	goto_if_eq VAR_0x8006, 4, LavenderIntro_LookPlayer4
	return
LavenderIntro_LookPlayer1::
	applymovement 201, LavenderIntro_Face_up
	waitmovement 0
	return
LavenderIntro_LookPlayer2::
	applymovement 201, LavenderIntro_Face_down
	waitmovement 0
	return
LavenderIntro_LookPlayer3::
	applymovement 201, LavenderIntro_Face_right
	waitmovement 0
	return
LavenderIntro_LookPlayer4::
	applymovement 201, LavenderIntro_Face_left
	waitmovement 0
	return
LavenderIntro_Face_up::
	face_up
	step_end
LavenderIntro_Face_down::
	face_down
	step_end
LavenderIntro_Face_left::
	face_left
	step_end
LavenderIntro_Face_right::
	face_right
	step_end

LavenderZombieHouse_Immunity::
	special LavanvilleZombieImmunity
	end

LavenderZombie_Growl::
	.string "Grrr...$"

CinnabarPast_MapScripts::
	.byte 0
CinnabarPast_Mansion_MapScripts::
	.byte 0
CinnabarPast_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CinnabarPast_SelectChampion
	map_script MAP_SCRIPT_ON_LOAD, CinnabarPast_DrawBridges
	.byte 0
CinnabarPast_Lab_MapScripts::
	.byte 0
CinnabarPast_Center_MapScripts::
	.byte 0
CinnabarPast_Mart_MapScripts::
	.byte 0

CinnabarPast_SelectChampion::
	setflag FLAG_SCENARIO_HIDE_TIME_NATHANIEL
	setflag FLAG_SCENARIO_HIDE_TIME_MICHAEL
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CinnabarPast_SelectMichael
	clearflag FLAG_SCENARIO_HIDE_TIME_NATHANIEL
	end
CinnabarPast_SelectMichael::
	clearflag FLAG_SCENARIO_HIDE_TIME_MICHAEL
	end
CinnabarPast_DrawBridges::
	call_if_set FLAG_SCENARIO_TIME_VALVE_WEST, CinnabarPast_DrawWest
	call_if_set FLAG_SCENARIO_TIME_VALVE_EAST, CinnabarPast_DrawEast
	end
CinnabarPast_DrawWest::
	setmetatile 7, 12, 0x29C, FALSE
	return
CinnabarPast_DrawEast::
	setmetatile 7, 6, 0x29C, FALSE
	return
CinnabarPast_ValveWest::
	lockall
	setflag FLAG_SCENARIO_TIME_VALVE_WEST
	call CinnabarPast_DrawWest
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox CinnabarPast_Text_ValveWest
	releaseall
	end
CinnabarPast_ValveEast::
	lockall
	setflag FLAG_SCENARIO_TIME_VALVE_EAST
	call CinnabarPast_DrawEast
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox CinnabarPast_Text_ValveEast
	releaseall
	end
CinnabarPast_Return::
	lock
	faceplayer
	goto_if_unset FLAG_SCENARIO_TIME_TROPHY, CinnabarPast_ReturnRefused
	msgbox CinnabarPast_Text_ReturnOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	call_if_unset FLAG_SCENARIO_TIME_RETURNED, CinnabarPast_PrepareReturn
	fadescreen FADE_TO_WHITE
	warp MAP_POKEMON_MANSION_1F, 8, 32
	waitstate
	fadescreen FADE_FROM_WHITE
	release
	end
CinnabarPast_ReturnRefused::
	msgbox CinnabarPast_Text_ReturnRefused
	release
	end
CinnabarPast_Champion::
	lock
	faceplayer
	goto_if_set FLAG_SCENARIO_TIME_TROPHY, CinnabarPast_After
	goto_if_unset FLAG_SCENARIO_ALYZON_TROPHY, CinnabarPast_NeedsSixth
	goto_if_unset FLAG_SCENARIO_TIME_VALVE_WEST, CinnabarPast_NeedsValves
	goto_if_unset FLAG_SCENARIO_TIME_VALVE_EAST, CinnabarPast_NeedsValves
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CinnabarPast_MichaelBattle
	trainerbattle_single TRAINER_SCENARIO_NATHANIEL_YOUNG, CinnabarPast_Text_NathanielIntro, CinnabarPast_Text_Defeat, CinnabarPast_Win, NO_MUSIC
	goto CinnabarPast_After
CinnabarPast_MichaelBattle::
	trainerbattle_single TRAINER_SCENARIO_MICHAEL_YOUNG, CinnabarPast_Text_MichaelIntro, CinnabarPast_Text_Defeat, CinnabarPast_Win, NO_MUSIC
	goto CinnabarPast_After
CinnabarPast_Win::
	setflag FLAG_SCENARIO_TIME_TROPHY
	setflag FLAG_BADGE07_GET
	setflag FLAG_DEFEATED_BLAINE
	playfanfare MUS_OBTAIN_BADGE
	msgbox CinnabarPast_Text_Trophy
	waitfanfare
CinnabarPast_After::
	goto_if_set FLAG_GOT_TM38_FROM_BLAINE, CinnabarPast_ReturnAdvice
	checkitemspace ITEM_TM38
	goto_if_eq VAR_RESULT, FALSE, CinnabarPast_BagFull
	giveitem ITEM_TM38
	setflag FLAG_GOT_TM38_FROM_BLAINE
	msgbox CinnabarPast_Text_TM
CinnabarPast_ReturnAdvice::
	msgbox CinnabarPast_Text_ChampionAfter
	release
	end
CinnabarPast_BagFull::
	msgbox CinnabarPast_Text_BagFull
	release
	end
CinnabarPast_NeedsSixth::
	msgbox CinnabarPast_Text_NeedsSixth
	release
	end
CinnabarPast_NeedsValves::
	msgbox CinnabarPast_Text_NeedsValves
	release
	end
CinnabarPast_GymGuide::
	msgbox CinnabarPast_Text_GymGuide, MSGBOX_NPC
	end
CinnabarPast_Historian::
	msgbox CinnabarPast_Text_Historian, MSGBOX_NPC
	end
CinnabarPast_Sign::
	msgbox CinnabarPast_Text_Sign, MSGBOX_SIGN
	end
CinnabarPast_Archive::
	msgbox CinnabarPast_Text_Archive, MSGBOX_NPC
	end
CinnabarPast_Nurse::
	lock
	faceplayer
	msgbox CinnabarPast_Text_HealOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	msgbox CinnabarPast_Text_HealDone
	release
	end
CinnabarPast_Shop::
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart CinnabarPast_ShopItems
	msgbox Text_PleaseComeAgain
	release
	end
	.align 2
CinnabarPast_ShopItems::
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_POKE_BALL
	.2byte ITEM_NONE
CinnabarPast_NoUpstairs::
	lockall
	msgbox CinnabarPast_Text_NoUpstairs
	applymovement LOCALID_PLAYER, IndigoPlateau_Movement_StepBack
	waitmovement 0
	releaseall
	end
EventScript_ScenarioPastNoSurf::
	msgbox CinnabarPast_Text_NoTravel, MSGBOX_SIGN
	end
CinnabarPast_Text_ValveWest::
	.string "La vanne ouest est réglée.\nUn passage central se dégage.$"
CinnabarPast_Text_ValveEast::
	.string "La vanne est est réglée.\nLe second passage est ouvert.$"
CinnabarPast_Text_ReturnOffer::
	.string "Triptic-tac accepte le retour!\nRejoindre le présent?$"
CinnabarPast_Text_ReturnRefused::
	.string "Triptic-tac refuse le retour.\nIl désigne l'arène de cette île.\pIl faudra obtenir le trophée\ndu Champion de cette époque.$"
CinnabarPast_Text_NathanielIntro::
	.string "NATHANIEL: Tu viens de loin?\nHovernyan et moi, on est prêts!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$"
CinnabarPast_Text_MichaelIntro::
	.string "MICHAEL: Quel drôle de voyage!\nHovernyan, faisons de notre mieux!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$"
CinnabarPast_Text_Defeat::
	.string "Nos amis ont tout donné!\nTu as gagné ce trophée!$"
CinnabarPast_Text_Trophy::
	.string "{PLAYER} reçoit\nle septième trophée!$"
CinnabarPast_Text_TM::
	.string "Prends aussi cette CT38.\nElle enseigne Déflagration.$"
CinnabarPast_Text_ChampionAfter::
	.string "Je vais parler à Triptic-tac.\nIl acceptera ton retour!\pTu pourras revenir nous voir\nsur cette île quand tu voudras.$"
CinnabarPast_Text_BagFull::
	.string "Ton Sac est plein.\nJe garde la CT38 pour toi.$"
CinnabarPast_Text_NeedsSixth::
	.string "Le sixième trophée d'Alyzon\nest nécessaire pour ce défi.$"
CinnabarPast_Text_NeedsValves::
	.string "Règle les deux vannes du bassin\navant notre combat.$"
CinnabarPast_Text_GymGuide::
	.string "Les ponts latéraux sont ouverts.\nRejoins les deux vannes!\pElles ouvrent aussi des raccourcis.\nLeurs réglages sont conservés.$"
CinnabarPast_Text_Historian::
	.string "Cette île est notre foyer.\nLe Champion s'entraîne à l'est.\pLe Centre offre des soins.\nLa boutique vend des provisions.$"
CinnabarPast_Text_Sign::
	.string "Cramois'Île, autrefois.\nLes mêmes rivages, un autre temps.$"
CinnabarPast_Text_Archive::
	.string "Ces archives racontent\nl'histoire ancienne de l'île.\pLes rues et les rivages\nn'ont pas changé de place.$"
CinnabarPast_Text_HealOffer::
	.string "Tes Yo-kai semblent fatigués.\nVeux-tu les faire soigner?$"
CinnabarPast_Text_HealDone::
	.string "Ton équipe est en pleine forme!$"
CinnabarPast_Text_NoUpstairs::
	.string "L'étage est fermé.\nLes soins sont au rez-de-chaussée.$"
CinnabarPast_Text_NoTravel::
	.string "Impossible de quitter cette île\nà cette époque.\pPour rentrer, retrouve Triptic-tac\ndans l'ancien manoir.$"

CinnabarPast_PrepareReturn::
	setflag FLAG_SCENARIO_TIME_RETURNED
	call_if_eq VAR_MAP_SCENE_CINNABAR_ISLAND, 0, CinnabarPast_PrepareBill
	return
CinnabarPast_PrepareBill::
	setvar VAR_MAP_SCENE_CINNABAR_ISLAND, 1
	clearflag FLAG_HIDE_CINNABAR_BILL
	return

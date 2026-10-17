FuchsiaCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FuchsiaCity_OnTransition
	.byte 0

FuchsiaCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_FUCHSIA_CITY
	call FuchsiaCity_OnTransitionYokaiAncestor
	call_if_set FLAG_GOT_DOME_FOSSIL, FuchsiaCity_EventScript_SetOmanyteGfx
	call_if_unset FLAG_GOT_DOME_FOSSIL, FuchsiaCity_EventScript_SetKabutoGfx
	end

FuchsiaCity_EventScript_SetOmanyteGfx::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_OMANYTE
	return

FuchsiaCity_EventScript_SetKabutoGfx::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_KABUTO
	return

FuchsiaCity_EventScript_LittleBoy::
	msgbox FuchsiaCity_Text_DidYouTrySafariGame, MSGBOX_NPC
	end

FuchsiaCity_EventScript_OldMan::
	msgbox FuchsiaCity_Text_SafariZoneZooInFront, MSGBOX_NPC
	end

FuchsiaCity_EventScript_Erik::
	msgbox FuchsiaCity_Text_WheresSara, MSGBOX_NPC
	end

FuchsiaCity_EventScript_Youngster::
	msgbox FuchsiaCity_Text_ItemBallInThere, MSGBOX_NPC
	end

FuchsiaCity_EventScript_Lass::
	lock
	faceplayer
	famechecker FAMECHECKER_KOGA, 3
	msgbox FuchsiaCity_Text_MyFatherIsGymLeader
	release
	end

FuchsiaCity_EventScript_CitySign::
	msgbox FuchsiaCity_Text_CitySign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_SafariZoneSign::
	msgbox FuchsiaCity_Text_SafariZoneSign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_SafariGameSign::
	msgbox FuchsiaCity_Text_SafariGameSign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_WardensHomeSign::
	msgbox FuchsiaCity_Text_WardensHomeSign, MSGBOX_SIGN
	end

@ Unused
FuchsiaCity_EventScript_SafariZoneOfficeSign::
	msgbox FuchsiaCity_Text_SafariZoneOfficeSign, MSGBOX_SIGN
	end

FuchsiaCity_EventScript_GymSign::
	lockall
	famechecker FAMECHECKER_KOGA, 0
	msgbox FuchsiaCity_Text_GymSign
	releaseall
	end

FuchsiaCity_EventScript_ChanseySign::
	lockall
	setvar VAR_0x8004, SPECIES_CHANSEY
	special SetSeenMon
	showmonpic SPECIES_CHANSEY, 10, 3
	msgbox FuchsiaCity_Text_ChanseySign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_VoltorbSign::
	lockall
	setvar VAR_0x8004, SPECIES_VOLTORB
	special SetSeenMon
	showmonpic SPECIES_VOLTORB, 10, 3
	msgbox FuchsiaCity_Text_VoltorbSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_KangaskhanSign::
	lockall
	setvar VAR_0x8004, SPECIES_KANGASKHAN
	special SetSeenMon
	showmonpic SPECIES_KANGASKHAN, 10, 3
	msgbox FuchsiaCity_Text_KangaskhanSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_SlowpokeSign::
	lockall
	setvar VAR_0x8004, SPECIES_SLOWPOKE
	special SetSeenMon
	showmonpic SPECIES_SLOWPOKE, 10, 3
	msgbox FuchsiaCity_Text_SlowpokeSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_LaprasSign::
	lockall
	setvar VAR_0x8004, SPECIES_LAPRAS
	special SetSeenMon
	showmonpic SPECIES_LAPRAS, 10, 3
	msgbox FuchsiaCity_Text_LaprasSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_FossilMonSign::
	lockall
	goto_if_set FLAG_GOT_DOME_FOSSIL, FuchsiaCity_EventScript_OmanyteSign
	setvar VAR_0x8004, SPECIES_KABUTO
	special SetSeenMon
	showmonpic SPECIES_KABUTO, 10, 3
	msgbox FuchsiaCity_Text_KabutoSign
	hidemonpic
	releaseall
	end

FuchsiaCity_EventScript_OmanyteSign::
	setvar VAR_0x8004, SPECIES_OMANYTE
	special SetSeenMon
	showmonpic SPECIES_OMANYTE, 10, 3
	msgbox FuchsiaCity_Text_OmanyteSign
	hidemonpic
	releaseall
	end

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
FuchsiaCity_EventScript_YokaiAncestor::
	lock
	faceplayer
	goto_if_unset FLAG_YOKAI_ANCESTOR_WON, FuchsiaCity_YokaiAncestorOffer
	goto_if_unset FLAG_YOKAI_ANCESTOR_REWARD, FuchsiaCity_YokaiAncestorReward
	goto_if_unset FLAG_SYS_GAME_CLEAR, FuchsiaCity_YokaiAncestorAlreadyWon
FuchsiaCity_YokaiAncestorOffer::
	msgbox FuchsiaCity_Text_YokaiAncestorOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FuchsiaCity_YokaiAncestorDecline
	closemessage
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, FuchsiaCity_YokaiAncestorMichael
	goto_if_set FLAG_SYS_GAME_CLEAR, FuchsiaCity_YokaiAncestorNathanielPost
	trainerbattle_single TRAINER_YOKAI_NATHANIEL, FuchsiaCity_Text_YokaiAncestorStart, FuchsiaCity_Text_YokaiAncestorDefeat, FuchsiaCity_YokaiAncestorVictory
	goto EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorNathanielPost::
	cleartrainerflag TRAINER_YOKAI_NATHANIEL_POST
	trainerbattle_single TRAINER_YOKAI_NATHANIEL_POST, FuchsiaCity_Text_YokaiAncestorPostStart, FuchsiaCity_Text_YokaiAncestorDefeat, FuchsiaCity_YokaiAncestorPostVictory
	goto EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorMichael::
	goto_if_set FLAG_SYS_GAME_CLEAR, FuchsiaCity_YokaiAncestorMichaelPost
	trainerbattle_single TRAINER_YOKAI_MICHAEL, FuchsiaCity_Text_YokaiAncestorStart, FuchsiaCity_Text_YokaiAncestorDefeat, FuchsiaCity_YokaiAncestorVictory
	goto EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorMichaelPost::
	cleartrainerflag TRAINER_YOKAI_MICHAEL_POST
	trainerbattle_single TRAINER_YOKAI_MICHAEL_POST, FuchsiaCity_Text_YokaiAncestorPostStart, FuchsiaCity_Text_YokaiAncestorDefeat, FuchsiaCity_YokaiAncestorPostVictory
	goto EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorPostVictory::
	setflag FLAG_YOKAI_ANCESTOR_POST_WON
FuchsiaCity_YokaiAncestorVictory::
	closemessage
	setflag FLAG_YOKAI_ANCESTOR_WON
	msgbox FuchsiaCity_Text_YokaiAncestorAfter
	goto_if_set FLAG_YOKAI_ANCESTOR_REWARD, EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorReward::
	checkitemspace ITEM_LEAF_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, FuchsiaCity_YokaiAncestorBagFull
	msgbox FuchsiaCity_Text_YokaiAncestorReward
	giveitem ITEM_LEAF_STONE, 1
	goto_if_eq VAR_0x8007, FALSE, FuchsiaCity_YokaiAncestorBagFull
	setflag FLAG_YOKAI_ANCESTOR_REWARD
	goto EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorAlreadyWon::
	msgbox FuchsiaCity_Text_YokaiAncestorRevisit
	goto EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorDecline::
	msgbox FuchsiaCity_Text_YokaiAncestorDecline
	goto EventScript_ReleaseEnd
FuchsiaCity_YokaiAncestorBagFull::
	msgbox FuchsiaCity_Text_YokaiAncestorBagFull
	goto EventScript_ReleaseEnd

FuchsiaCity_Text_YokaiAncestorOffer::
	.string "Toi aussi, tu voyages avec des\n"
	.string "Yo-kai? Mes amis sont en forme!\p"
	.string "Ça te dit de faire un combat?$"
FuchsiaCity_Text_YokaiAncestorStart::
	.string "Hovernyan, à toi de jouer!$"
FuchsiaCity_Text_YokaiAncestorPostStart::
	.string "Notre équipe a bien grandi!\n"
	.string "Montrons nos progrès!$"
FuchsiaCity_Text_YokaiAncestorDefeat::
	.string "Quelle belle équipe!\n"
	.string "On a encore tant à apprendre!$"
FuchsiaCity_Text_YokaiAncestorAfter::
	.string "Merci pour ce combat!\n"
	.string "Nos amis ont tout donné.$"
FuchsiaCity_Text_YokaiAncestorReward::
	.string "Prends cette Pierre Plante.\n"
	.string "Pour faire évoluer ton Jibanyan!$"
FuchsiaCity_Text_YokaiAncestorRevisit::
	.string "Jibanyan et moi allons continuer\n"
	.string "notre voyage. Après la Ligue,\p"
	.string "on fera un autre combat!$"
FuchsiaCity_Text_YokaiAncestorDecline::
	.string "Pas de problème!\n"
	.string "Reviens quand tu voudras.$"
FuchsiaCity_Text_YokaiAncestorBagFull::
	.string "Ton sac est plein.\n"
	.string "Je garde ta pierre pour plus tard!$"

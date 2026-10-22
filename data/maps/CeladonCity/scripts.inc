CeladonCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CeladonCity_OnTransition
	.byte 0

CeladonCity_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_CELADON_CITY
	call CeladonCity_OnTransitionYokaiFriend
	end

CeladonCity_EventScript_LittleGirl::
	msgbox CeladonCity_Text_GotMyKoffingInCinnabar, MSGBOX_NPC
	end

CeladonCity_EventScript_OldMan1::
	lock
	msgbox CeladonCity_Text_GymIsGreatFullOfWomen
	release
	end

CeladonCity_EventScript_Woman::
	msgbox CeladonCity_Text_GameCornerIsBadForCitysImage, MSGBOX_NPC
	end

CeladonCity_EventScript_OldMan2::
	msgbox CeladonCity_Text_BlewItAllAtSlots, MSGBOX_NPC
	end

CeladonCity_EventScript_SoftboiledTutor::
	goto EventScript_SoftboiledTutor
	end

CeladonCity_EventScript_FatMan::
	lock
	faceplayer
	msgbox CeladonCity_Text_MyTrustedPalPoliwrath
	closemessage
	applymovement LOCALID_CELADON_FAT_MAN, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeladonCity_EventScript_Poliwrath::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_POLIWRATH, CRY_MODE_NORMAL
	msgbox CeladonCity_Text_Poliwrath
	closemessage
	waitmoncry
	applymovement LOCALID_CELADON_POLIWRATH, Common_Movement_FaceOriginalDirection
	waitmovement 0
	release
	end

CeladonCity_EventScript_RocketGrunt1::
	msgbox CeladonCity_Text_KeepOutOfTeamRocketsWay, MSGBOX_NPC
	end

CeladonCity_EventScript_RocketGrunt2::
	msgbox CeladonCity_Text_GetLostOrIllPunchYou, MSGBOX_NPC
	end

CeladonCity_EventScript_Boy::
	msgbox CeladonCity_Text_ScaldedTongueOnTea, MSGBOX_NPC
	end

CeladonCity_EventScript_SilphCoScientist::
	msgbox CeladonCity_Text_SomeoneStoleSilphScope, MSGBOX_NPC
	end

CeladonCity_EventScript_TrainerTips1::
	msgbox CeladonCity_Text_ExplainXAccuracyDireHit, MSGBOX_SIGN
	end

CeladonCity_EventScript_CitySign::
	msgbox CeladonCity_Text_CitySign, MSGBOX_SIGN
	end

CeladonCity_EventScript_GymSign::
	lockall
	famechecker FAMECHECKER_ERIKA, 0
	msgbox CeladonCity_Text_GymSign
	releaseall
	end

CeladonCity_EventScript_MansionSign::
	msgbox CeladonCity_Text_MansionSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_DeptStoreSign::
	msgbox CeladonCity_Text_DeptStoreSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_TrainerTips2::
	msgbox CeladonCity_Text_GuardSpecProtectsFromStatus, MSGBOX_SIGN
	end

CeladonCity_EventScript_PrizeExchangeSign::
	msgbox CeladonCity_Text_PrizeExchangeSign, MSGBOX_SIGN
	end

CeladonCity_EventScript_GameCornerSign::
	msgbox CeladonCity_Text_GameCornerSign, MSGBOX_SIGN
	end

CeladonCity_OnTransitionYokaiFriend::
	setflag FLAG_SCENARIO_CELADON_FRIEND_CURRENT
	setflag FLAG_HIDE_YOKAI_NATHAN
	setflag FLAG_HIDE_YOKAI_KATIE
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
	.string "Toi aussi, tu voyages avec des\n"
	.string "Yo-kai? Mes amis sont en forme!\p"
	.string "Ça te dit de faire un combat?$"
CeladonCity_Text_YokaiFriendStart::
	.string "Jibanyan, à toi de jouer!$"
CeladonCity_Text_YokaiFriendPostStart::
	.string "Notre équipe a bien grandi!\n"
	.string "Montrons nos progrès!$"
CeladonCity_Text_YokaiFriendDefeat::
	.string "Quelle belle équipe!\n"
	.string "On a encore tant à apprendre!$"
CeladonCity_Text_YokaiFriendAfter::
	.string "Merci pour ce combat!\n"
	.string "Nos amis ont tout donné.$"
CeladonCity_Text_YokaiFriendReward::
	.string "Prends cette Pierre Plante.\n"
	.string "Jibanyan peut évoluer avec elle!$"
CeladonCity_Text_YokaiFriendRevisit::
	.string "Jibanyan et moi allons continuer\n"
	.string "notre voyage. Après la Ligue,\p"
	.string "on fera un autre combat!$"
CeladonCity_Text_YokaiFriendDecline::
	.string "Pas de problème!\n"
	.string "Reviens quand tu voudras.$"
CeladonCity_Text_YokaiFriendBagFull::
	.string "Ton sac est plein.\n"
	.string "Je garde ta pierre pour plus tard!$"

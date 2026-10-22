CeruleanCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CeruleanCity_Gym_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, CeruleanCity_Gym_OnLoad
	.byte 0

CeruleanCity_Gym_OnTransition::
	setflag FLAG_SCENARIO_AZURIA_GYM_CURRENT
	setflag FLAG_SCENARIO_HIDE_AZURIA_NATHAN
	setflag FLAG_SCENARIO_HIDE_AZURIA_KATIE
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CeruleanCity_Gym_ShowNathan
	clearflag FLAG_SCENARIO_HIDE_AZURIA_KATIE
	end
CeruleanCity_Gym_ShowNathan::
	clearflag FLAG_SCENARIO_HIDE_AZURIA_NATHAN
	end

CeruleanCity_Gym_OnLoad::
	call CeruleanCity_Gym_EventScript_DrawHearths
	end

CeruleanCity_Gym_EventScript_DrawHearths::
	setmetatile 4, 11, 0x2E0, TRUE
	setmetatile 12, 11, 0x2E0, TRUE
	setmetatile 8, 9, 0x2E0, TRUE
	goto_if_eq VAR_SCENARIO_AZURIA_HEARTHS, 0, CeruleanCity_Gym_DrawDone
	setmetatile 4, 11, 0x2E1, TRUE
	goto_if_eq VAR_SCENARIO_AZURIA_HEARTHS, 1, CeruleanCity_Gym_DrawDone
	setmetatile 12, 11, 0x2E1, TRUE
	goto_if_eq VAR_SCENARIO_AZURIA_HEARTHS, 2, CeruleanCity_Gym_DrawDone
	setmetatile 8, 9, 0x2E1, TRUE
CeruleanCity_Gym_DrawDone::
	return

CeruleanCity_Gym_EventScript_Feulion::
	lockall
	goto_if_ne VAR_SCENARIO_AZURIA_HEARTHS, 0, CeruleanCity_Gym_EventScript_AlreadyLit
	setvar VAR_SCENARIO_AZURIA_HEARTHS, 1
	call CeruleanCity_Gym_EventScript_DrawHearths
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox CeruleanCity_Gym_Text_Feulion
	releaseall
	end
CeruleanCity_Gym_EventScript_Whisper::
	lockall
	goto_if_eq VAR_SCENARIO_AZURIA_HEARTHS, 2, CeruleanCity_Gym_EventScript_AlreadyLit
	goto_if_eq VAR_SCENARIO_AZURIA_HEARTHS, 3, CeruleanCity_Gym_EventScript_AlreadyLit
	goto_if_ne VAR_SCENARIO_AZURIA_HEARTHS, 1, CeruleanCity_Gym_EventScript_WrongOrder
	setvar VAR_SCENARIO_AZURIA_HEARTHS, 2
	call CeruleanCity_Gym_EventScript_DrawHearths
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox CeruleanCity_Gym_Text_Whisper
	releaseall
	end
CeruleanCity_Gym_EventScript_Jibanyan::
	lockall
	goto_if_eq VAR_SCENARIO_AZURIA_HEARTHS, 3, CeruleanCity_Gym_EventScript_AlreadyLit
	goto_if_ne VAR_SCENARIO_AZURIA_HEARTHS, 2, CeruleanCity_Gym_EventScript_WrongOrder
	setvar VAR_SCENARIO_AZURIA_HEARTHS, 3
	call CeruleanCity_Gym_EventScript_DrawHearths
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox CeruleanCity_Gym_Text_Jibanyan
	releaseall
	end
CeruleanCity_Gym_EventScript_WrongOrder::
	setvar VAR_SCENARIO_AZURIA_HEARTHS, 0
	call CeruleanCity_Gym_EventScript_DrawHearths
	special DrawWholeMapView
	msgbox CeruleanCity_Gym_Text_WrongOrder
	releaseall
	end
CeruleanCity_Gym_EventScript_AlreadyLit::
	msgbox CeruleanCity_Gym_Text_AlreadyLit
	releaseall
	end

CeruleanCity_Gym_EventScript_Gate::
	lockall
	goto_if_unset FLAG_BADGE01_GET, CeruleanCity_Gym_GateNeedsFirst
	goto_if_set FLAG_BADGE02_GET, CeruleanCity_Gym_GateOpen
	goto_if_eq VAR_SCENARIO_AZURIA_HEARTHS, 3, CeruleanCity_Gym_GateOpen
	msgbox CeruleanCity_Gym_Text_NeedsHearths
	goto CeruleanCity_Gym_GateStepBack
CeruleanCity_Gym_GateNeedsFirst::
	msgbox CeruleanCity_Gym_Text_NeedsFirst
CeruleanCity_Gym_GateStepBack::
	applymovement LOCALID_PLAYER, IndigoPlateau_Movement_StepBack
	waitmovement 0
	releaseall
	end
CeruleanCity_Gym_GateOpen::
	setvar VAR_TEMP_2, 1
	releaseall
	end

CeruleanCity_Gym_EventScript_Champion::
	lock
	faceplayer
	famechecker FAMECHECKER_MISTY, FCPICKSTATE_COLORED, UpdatePickStateFromSpecialVar8005
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CeruleanCity_Gym_NameNathan
	bufferstring STR_VAR_1, CeruleanCity_Gym_Text_NameKatie
	goto CeruleanCity_Gym_ChampionCheck
CeruleanCity_Gym_NameNathan::
	bufferstring STR_VAR_1, CeruleanCity_Gym_Text_NameNathan
CeruleanCity_Gym_ChampionCheck::
	goto_if_set FLAG_BADGE02_GET, CeruleanCity_Gym_ChampionAfterVictory
	goto_if_unset FLAG_BADGE01_GET, CeruleanCity_Gym_ChampionNeedsFirst
	goto_if_ne VAR_SCENARIO_AZURIA_HEARTHS, 3, CeruleanCity_Gym_ChampionNeedsHearths
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CeruleanCity_Gym_ChallengeNathan
	trainerbattle_single TRAINER_SCENARIO_KATIE, CeruleanCity_Gym_Text_KatieIntro, CeruleanCity_Gym_Text_Defeat, CeruleanCity_Gym_EventScript_Victory, NO_MUSIC
	goto CeruleanCity_Gym_ChampionAfterVictory
CeruleanCity_Gym_ChallengeNathan::
	trainerbattle_single TRAINER_SCENARIO_NATHAN, CeruleanCity_Gym_Text_NathanIntro, CeruleanCity_Gym_Text_Defeat, CeruleanCity_Gym_EventScript_Victory, NO_MUSIC
	goto CeruleanCity_Gym_ChampionAfterVictory
CeruleanCity_Gym_ChampionNeedsFirst::
	msgbox CeruleanCity_Gym_Text_NeedsFirst
	release
	end
CeruleanCity_Gym_ChampionNeedsHearths::
	msgbox CeruleanCity_Gym_Text_NeedsHearths
	release
	end
CeruleanCity_Gym_EventScript_Victory::
	famechecker FAMECHECKER_MISTY, 1
	setflag FLAG_DEFEATED_MISTY
	setflag FLAG_BADGE02_GET
	settrainerflag TRAINER_SCENARIO_KATIE
	settrainerflag TRAINER_SCENARIO_NATHAN
	setrespawn HEAL_LOCATION_CERULEAN_CITY
	set_gym_trainers 2
	playfanfare MUS_OBTAIN_BADGE
	msgbox CeruleanCity_Gym_Text_SecondTrophy
	waitfanfare
	goto CeruleanCity_Gym_EventScript_GiveTM03
CeruleanCity_Gym_ChampionAfterVictory::
	goto_if_unset FLAG_GOT_TM03_FROM_MISTY, CeruleanCity_Gym_EventScript_GiveTM03
	goto_if_unset FLAG_YOKAI_FRIEND_WON, CeruleanCity_Gym_RematchCheck
	goto_if_unset FLAG_YOKAI_FRIEND_REWARD, CeruleanCity_Gym_FriendReward
CeruleanCity_Gym_RematchCheck::
	goto_if_set FLAG_SYS_GAME_CLEAR, CeruleanCity_Gym_RematchOffer
	msgbox CeruleanCity_Gym_Text_AfterVictory
	release
	end
CeruleanCity_Gym_EventScript_GiveTM03::
	checkitemspace ITEM_TM03
	goto_if_eq VAR_RESULT, FALSE, CeruleanCity_Gym_EventScript_NoRoom
	giveitem_msg CeruleanCity_Gym_Text_ReceivedTM03, ITEM_TM03
	setflag FLAG_GOT_TM03_FROM_MISTY
	msgbox CeruleanCity_Gym_Text_ExplainTM03
	release
	end
CeruleanCity_Gym_EventScript_NoRoom::
	msgbox CeruleanCity_Gym_Text_NoRoom
	release
	end

@ The original Celadon postgame teams and unique reward live here now.
CeruleanCity_Gym_RematchOffer::
	msgbox CeruleanCity_Gym_Text_RematchOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, CeruleanCity_Gym_RematchDecline
	closemessage
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, CeruleanCity_Gym_RematchNathan
	cleartrainerflag TRAINER_YOKAI_KATIE_POST
	trainerbattle_no_intro TRAINER_YOKAI_KATIE_POST, CeruleanCity_Gym_Text_Defeat
	goto CeruleanCity_Gym_RematchWon
CeruleanCity_Gym_RematchNathan::
	cleartrainerflag TRAINER_YOKAI_NATHAN_POST
	trainerbattle_no_intro TRAINER_YOKAI_NATHAN_POST, CeruleanCity_Gym_Text_Defeat
CeruleanCity_Gym_RematchWon::
	setflag FLAG_YOKAI_FRIEND_WON
	setflag FLAG_YOKAI_FRIEND_POST_WON
	goto_if_unset FLAG_YOKAI_FRIEND_REWARD, CeruleanCity_Gym_FriendReward
	msgbox CeruleanCity_Gym_Text_RematchAfter
	release
	end
CeruleanCity_Gym_FriendReward::
	checkitemspace ITEM_LEAF_STONE
	goto_if_eq VAR_RESULT, FALSE, CeruleanCity_Gym_EventScript_NoRoom
	giveitem ITEM_LEAF_STONE
	setflag FLAG_YOKAI_FRIEND_REWARD
	msgbox CeruleanCity_Gym_Text_LeafStone
	release
	end
CeruleanCity_Gym_RematchDecline::
	msgbox CeruleanCity_Gym_Text_RematchDecline
	release
	end

CeruleanCity_Gym_EventScript_Luis::
	msgbox CeruleanCity_Gym_Text_Luis, MSGBOX_NPC
	end
CeruleanCity_Gym_EventScript_Diana::
	msgbox CeruleanCity_Gym_Text_Diana, MSGBOX_NPC
	end
CeruleanCity_Gym_EventScript_GymGuy::
	msgbox CeruleanCity_Gym_Text_GymGuy, MSGBOX_NPC
	end
CeruleanCity_Gym_EventScript_GymStatue::
	msgbox CeruleanCity_Gym_Text_Statue, MSGBOX_SIGN
	end

SaffronCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SaffronCity_Gym_OnTransition
	map_script MAP_SCRIPT_ON_LOAD, SaffronCity_Gym_OnLoad
	.byte 0
SaffronCity_Gym_OnTransition::
	setflag FLAG_SCENARIO_SAFFRON_GYM_CURRENT
	special RecognizeLegacySaffronTrophy
	end
SaffronCity_Gym_OnLoad::
	call SaffronCity_Gym_DrawSystems
	end
SaffronCity_Gym_DrawSystems::
	setmetatile 4, 4, 0x28C, TRUE
	setmetatile 24, 4, 0x28C, TRUE
	setmetatile 23, 19, 0x28C, TRUE
	call_if_set FLAG_SCENARIO_ORBIT_POWER, SaffronCity_Gym_DrawPower
	call_if_set FLAG_SCENARIO_ORBIT_NAV, SaffronCity_Gym_DrawNav
	call_if_set FLAG_SCENARIO_ORBIT_COMMS, SaffronCity_Gym_DrawComms
	return
SaffronCity_Gym_DrawPower::
	setmetatile 4, 4, 0x28D, TRUE
	return
SaffronCity_Gym_DrawNav::
	setmetatile 24, 4, 0x28D, TRUE
	return
SaffronCity_Gym_DrawComms::
	setmetatile 23, 19, 0x28D, TRUE
	return

SaffronCity_Gym_EventScript_Power::
	lockall
	goto_if_unset FLAG_BADGE03_GET, SaffronCity_Gym_NeedsThirdAll
	goto_if_set FLAG_SCENARIO_ORBIT_POWER, SaffronCity_Gym_SystemAlreadyOn
	setflag FLAG_SCENARIO_ORBIT_POWER
	call SaffronCity_Gym_DrawSystems
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox SaffronCity_Gym_Text_PowerOn
	releaseall
	end
SaffronCity_Gym_EventScript_Navigation::
	lockall
	goto_if_unset FLAG_BADGE03_GET, SaffronCity_Gym_NeedsThirdAll
	goto_if_unset FLAG_SCENARIO_ORBIT_POWER, SaffronCity_Gym_NeedsPower
	goto_if_set FLAG_SCENARIO_ORBIT_NAV, SaffronCity_Gym_SystemAlreadyOn
	setflag FLAG_SCENARIO_ORBIT_NAV
	call SaffronCity_Gym_DrawSystems
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox SaffronCity_Gym_Text_NavOn
	releaseall
	end
SaffronCity_Gym_EventScript_Communications::
	lockall
	goto_if_unset FLAG_BADGE03_GET, SaffronCity_Gym_NeedsThirdAll
	goto_if_unset FLAG_SCENARIO_ORBIT_NAV, SaffronCity_Gym_NeedsNav
	goto_if_set FLAG_SCENARIO_ORBIT_COMMS, SaffronCity_Gym_SystemAlreadyOn
	msgbox SaffronCity_Gym_Text_CommsOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SaffronCity_Gym_CommsDecline
	setflag FLAG_SCENARIO_ORBIT_COMMS
	call SaffronCity_Gym_DrawSystems
	special DrawWholeMapView
	playse SE_SWITCH
	msgbox SaffronCity_Gym_Text_CommsOn
	releaseall
	end
SaffronCity_Gym_CommsDecline::
	msgbox SaffronCity_Gym_Text_CommsDecline
	releaseall
	end
SaffronCity_Gym_SystemAlreadyOn::
	msgbox SaffronCity_Gym_Text_SystemAlreadyOn
	releaseall
	end
SaffronCity_Gym_NeedsPower::
	msgbox SaffronCity_Gym_Text_NeedsPower
	releaseall
	end
SaffronCity_Gym_NeedsNav::
	msgbox SaffronCity_Gym_Text_NeedsNav
	releaseall
	end
SaffronCity_Gym_NeedsThirdAll::
	msgbox SaffronCity_Gym_Text_NeedsThird
	releaseall
	end

SaffronCity_Gym_EventScript_Gate::
	lockall
	goto_if_unset FLAG_BADGE03_GET, SaffronCity_Gym_GateNeedsThird
	goto_if_set FLAG_SCENARIO_ARIANE_TROPHY, SaffronCity_Gym_GateOpen
	goto_if_unset FLAG_SCENARIO_ORBIT_POWER, SaffronCity_Gym_GateNeedsSystems
	goto_if_unset FLAG_SCENARIO_ORBIT_NAV, SaffronCity_Gym_GateNeedsSystems
	goto_if_unset FLAG_SCENARIO_ORBIT_COMMS, SaffronCity_Gym_GateNeedsSystems
SaffronCity_Gym_GateOpen::
	setvar VAR_TEMP_2, 1
	releaseall
	end
SaffronCity_Gym_GateNeedsThird::
	msgbox SaffronCity_Gym_Text_NeedsThird
	goto SaffronCity_Gym_StepBack
SaffronCity_Gym_GateNeedsSystems::
	msgbox SaffronCity_Gym_Text_NeedsSystems
SaffronCity_Gym_StepBack::
	applymovement LOCALID_PLAYER, IndigoPlateau_Movement_StepBack
	waitmovement 0
	releaseall
	end

SaffronCity_Gym_EventScript_Ariane::
	lock
	faceplayer
	goto_if_set FLAG_SCENARIO_ARIANE_TROPHY, SaffronCity_Gym_AfterVictory
	goto_if_unset FLAG_BADGE03_GET, SaffronCity_Gym_ChampionNeedsThird
	goto_if_unset FLAG_SCENARIO_ORBIT_POWER, SaffronCity_Gym_ChampionNeedsSystems
	goto_if_unset FLAG_SCENARIO_ORBIT_NAV, SaffronCity_Gym_ChampionNeedsSystems
	goto_if_unset FLAG_SCENARIO_ORBIT_COMMS, SaffronCity_Gym_ChampionNeedsSystems
	trainerbattle_single TRAINER_SCENARIO_ARIANE, SaffronCity_Gym_Text_Intro, SaffronCity_Gym_Text_Defeat, SaffronCity_Gym_Victory, NO_MUSIC
	goto SaffronCity_Gym_AfterVictory
SaffronCity_Gym_ChampionNeedsThird::
	msgbox SaffronCity_Gym_Text_NeedsThird
	release
	end
SaffronCity_Gym_ChampionNeedsSystems::
	msgbox SaffronCity_Gym_Text_NeedsSystems
	release
	end
SaffronCity_Gym_Victory::
	setflag FLAG_SCENARIO_ARIANE_TROPHY
	setflag FLAG_BADGE04_GET
	setflag FLAG_DEFEATED_SABRINA
	set_gym_trainers 6
	playfanfare MUS_OBTAIN_BADGE
	msgbox SaffronCity_Gym_Text_FourthTrophy
	waitfanfare
	goto SaffronCity_Gym_GiveTM
SaffronCity_Gym_AfterVictory::
	goto_if_unset FLAG_GOT_TM04_FROM_SABRINA, SaffronCity_Gym_GiveTM
	goto_if_unset FLAG_YOKAI_ARIANE_WON, SaffronCity_Gym_RematchCheck
	goto_if_unset FLAG_YOKAI_ARIANE_REWARD, SaffronCity_Gym_MoonStone
SaffronCity_Gym_RematchCheck::
	goto_if_set FLAG_SYS_GAME_CLEAR, SaffronCity_Gym_RematchOffer
	msgbox SaffronCity_Gym_Text_AfterVictory
	release
	end
SaffronCity_Gym_GiveTM::
	checkitemspace ITEM_TM04
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_Gym_NoRoom
	giveitem_msg SaffronCity_Gym_Text_ReceivedTM, ITEM_TM04
	setflag FLAG_GOT_TM04_FROM_SABRINA
	msgbox SaffronCity_Gym_Text_ExplainTM
	release
	end
SaffronCity_Gym_NoRoom::
	msgbox SaffronCity_Gym_Text_NoRoom
	release
	end
SaffronCity_Gym_RematchOffer::
	msgbox SaffronCity_Gym_Text_RematchOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SaffronCity_Gym_RematchDecline
	closemessage
	cleartrainerflag TRAINER_YOKAI_ARIANE_POST
	trainerbattle_no_intro TRAINER_YOKAI_ARIANE_POST, SaffronCity_Gym_Text_Defeat
	setflag FLAG_YOKAI_ARIANE_WON
	setflag FLAG_YOKAI_ARIANE_POST_WON
	goto_if_unset FLAG_YOKAI_ARIANE_REWARD, SaffronCity_Gym_MoonStone
	msgbox SaffronCity_Gym_Text_RematchAfter
	release
	end
SaffronCity_Gym_MoonStone::
	checkitemspace ITEM_MOON_STONE
	goto_if_eq VAR_RESULT, FALSE, SaffronCity_Gym_NoRoom
	giveitem ITEM_MOON_STONE
	setflag FLAG_YOKAI_ARIANE_REWARD
	msgbox SaffronCity_Gym_Text_MoonStone
	release
	end
SaffronCity_Gym_RematchDecline::
	msgbox SaffronCity_Gym_Text_RematchDecline
	release
	end
SaffronCity_Gym_EventScript_Usapion::
	msgbox SaffronCity_Gym_Text_Usapion, MSGBOX_NPC
	end
SaffronCity_Gym_EventScript_Guide::
	msgbox SaffronCity_Gym_Text_Guide, MSGBOX_NPC
	end
SaffronCity_Gym_EventScript_Statue::
	msgbox SaffronCity_Gym_Text_Statue, MSGBOX_SIGN
	end

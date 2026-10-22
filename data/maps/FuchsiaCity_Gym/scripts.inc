FuchsiaCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FuchsiaCity_Gym_Transition
	.byte 0
FuchsiaCity_Gym_Transition::
	setflag FLAG_SCENARIO_FUCHSIA_GYM_CURRENT
	end
FuchsiaCity_Gym_Clue::
	lockall
	goto_if_unset FLAG_SCENARIO_ARIANE_TROPHY, FuchsiaCity_Gym_NeedsFourth
	setflag FLAG_SCENARIO_GIRAUD_CLUE
	msgbox FuchsiaCity_Gym_Text_Clue
	releaseall
	end
FuchsiaCity_Gym_WitnessA::
	lock
	faceplayer
	goto_if_unset FLAG_SCENARIO_GIRAUD_CLUE, FuchsiaCity_Gym_NeedsClue
	setflag FLAG_SCENARIO_GIRAUD_WITNESS_A
	msgbox FuchsiaCity_Gym_Text_WitnessA
	release
	end
FuchsiaCity_Gym_WitnessB::
	lock
	faceplayer
	goto_if_unset FLAG_SCENARIO_GIRAUD_CLUE, FuchsiaCity_Gym_NeedsClue
	setflag FLAG_SCENARIO_GIRAUD_WITNESS_B
	msgbox FuchsiaCity_Gym_Text_WitnessB
	release
	end
FuchsiaCity_Gym_NeedsClue::
	msgbox FuchsiaCity_Gym_Text_NeedsClue
	release
	end
FuchsiaCity_Gym_Report::
	lockall
	goto_if_unset FLAG_SCENARIO_GIRAUD_WITNESS_A, FuchsiaCity_Gym_NeedsWitnesses
	goto_if_unset FLAG_SCENARIO_GIRAUD_WITNESS_B, FuchsiaCity_Gym_NeedsWitnesses
	goto_if_set FLAG_SCENARIO_GIRAUD_REPORT, FuchsiaCity_Gym_ReportDone
	msgbox FuchsiaCity_Gym_Text_Question, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, FuchsiaCity_Gym_WrongAnswer
	setflag FLAG_SCENARIO_GIRAUD_REPORT
FuchsiaCity_Gym_ReportDone::
	msgbox FuchsiaCity_Gym_Text_Solved
	releaseall
	end
FuchsiaCity_Gym_WrongAnswer::
	msgbox FuchsiaCity_Gym_Text_Wrong
	releaseall
	end
FuchsiaCity_Gym_NeedsWitnesses::
	msgbox FuchsiaCity_Gym_Text_NeedsWitnesses
	releaseall
	end
FuchsiaCity_Gym_NeedsFourth::
	msgbox FuchsiaCity_Gym_Text_NeedsFourth
	releaseall
	end
FuchsiaCity_Gym_Gate::
	lockall
	goto_if_set FLAG_BADGE05_GET, FuchsiaCity_Gym_GateOpen
	goto_if_unset FLAG_SCENARIO_GIRAUD_REPORT, FuchsiaCity_Gym_GateClosed
FuchsiaCity_Gym_GateOpen::
	setvar VAR_TEMP_2, 1
	releaseall
	end
FuchsiaCity_Gym_GateClosed::
	msgbox FuchsiaCity_Gym_Text_NeedsReport
	applymovement LOCALID_PLAYER, IndigoPlateau_Movement_StepBack
	waitmovement 0
	releaseall
	end
FuchsiaCity_Gym_Giraud::
	lock
	faceplayer
	goto_if_set FLAG_BADGE05_GET, FuchsiaCity_Gym_After
	goto_if_unset FLAG_SCENARIO_ARIANE_TROPHY, FuchsiaCity_Gym_BossNeedsFourth
	goto_if_unset FLAG_SCENARIO_GIRAUD_REPORT, FuchsiaCity_Gym_BossNeedsReport
	trainerbattle_single TRAINER_LEADER_KOGA, FuchsiaCity_Gym_Text_Intro, FuchsiaCity_Gym_Text_Defeat, FuchsiaCity_Gym_Win, NO_MUSIC
	goto FuchsiaCity_Gym_After
FuchsiaCity_Gym_BossNeedsFourth::
	msgbox FuchsiaCity_Gym_Text_NeedsFourth
	release
	end
FuchsiaCity_Gym_BossNeedsReport::
	msgbox FuchsiaCity_Gym_Text_NeedsReport
	release
	end
FuchsiaCity_Gym_Win::
	setflag FLAG_BADGE05_GET
	setflag FLAG_DEFEATED_KOGA
	set_gym_trainers 5
	playfanfare MUS_OBTAIN_BADGE
	msgbox FuchsiaCity_Gym_Text_Trophy
	waitfanfare
FuchsiaCity_Gym_After::
	goto_if_set FLAG_GOT_TM06_FROM_KOGA, FuchsiaCity_Gym_Advice
	checkitemspace ITEM_TM06
	goto_if_eq VAR_RESULT, FALSE, FuchsiaCity_Gym_BagFull
	giveitem ITEM_TM06
	setflag FLAG_GOT_TM06_FROM_KOGA
	msgbox FuchsiaCity_Gym_Text_TM
	release
	end
FuchsiaCity_Gym_BagFull::
	msgbox FuchsiaCity_Gym_Text_BagFull
	release
	end
FuchsiaCity_Gym_Advice::
	msgbox FuchsiaCity_Gym_Text_Advice
	release
	end
FuchsiaCity_Gym_Guide::
	msgbox FuchsiaCity_Gym_Text_Guide, MSGBOX_NPC
	end

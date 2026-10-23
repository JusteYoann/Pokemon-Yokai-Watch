SixIsland_WaterPath_House2_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_WaterPath_House2_OnTransition
	.byte 0

@ Temporary visibility flags are recalculated on every entrance. No permanent
@ story flag is written here: first Don743 alone never unlocks this house.
SixIsland_WaterPath_House2_OnTransition::
	setflag FLAG_TEMP_6
	setflag FLAG_TEMP_7
	goto_if_unset FLAG_SYS_GAME_CLEAR, SixIsland_WaterPath_House2_ShowResident
	goto_if_not_defeated TRAINER_DON_SPIRATON_PROTOTYPE, SixIsland_WaterPath_House2_ShowResident
	clearflag FLAG_TEMP_7
	end

SixIsland_WaterPath_House2_ShowResident::
	clearflag FLAG_TEMP_6
	end

SixIsland_WaterPath_House2_EventScript_Man::
	msgbox SixIsland_WaterPath_House2_Text_MyNeighborMeasuredMe, MSGBOX_NPC
	end


SixIsland_WaterPath_House2_EventScript_DonMorleone::
	lock
	faceplayer
	msgbox SixIsland_WaterPath_House2_Text_DonRematch, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SixIsland_WaterPath_House2_DonDecline
	msgbox SixIsland_WaterPath_House2_Text_DonAccept
	closemessage
	@ Mode3 starts unconditionally; never clear any trainer/progression flag.
	trainerbattle_no_intro TRAINER_DON_MORLEONE_LEAGUE, SixIsland_WaterPath_House2_Text_Empty
	release
	end

SixIsland_WaterPath_House2_DonDecline::
	msgbox SixIsland_WaterPath_House2_Text_DonDecline
	release
	end

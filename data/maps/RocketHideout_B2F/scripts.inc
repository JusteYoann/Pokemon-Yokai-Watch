RocketHideout_B2F_MapScripts::
	.byte 0

RocketHideout_B2F_EventScript_Grunt::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_13, RocketHideout_B2F_Text_GruntIntro, RocketHideout_B2F_Text_GruntDefeat
	msgbox RocketHideout_B2F_Text_GruntPostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B2F_EventScript_Yokai121::
	lock
	faceplayer
	bufferspeciesname STR_VAR_1, SPECIES_STARMIE
	msgbox RocketHideout_B2F_EventScript_Yokai121_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle SPECIES_STARMIE, 25
	dowildbattle
	release
	end
RocketHideout_B2F_EventScript_Yokai121_Text::
	.string "Un {STR_VAR_1} se cache ici.\n"
	.string "Veux-tu le rencontrer?$"

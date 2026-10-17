RocketHideout_B3F_MapScripts::
	.byte 0

RocketHideout_B3F_EventScript_Grunt1::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_14, RocketHideout_B3F_Text_Grunt1Intro, RocketHideout_B3F_Text_Grunt1Defeat
	msgbox RocketHideout_B3F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B3F_EventScript_Grunt2::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_15, RocketHideout_B3F_Text_Grunt2Intro, RocketHideout_B3F_Text_Grunt2Defeat
	msgbox RocketHideout_B3F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

RocketHideout_B3F_EventScript_Yokai122::
	lock
	faceplayer
	bufferspeciesname STR_VAR_1, SPECIES_MR_MIME
	msgbox RocketHideout_B3F_EventScript_Yokai122_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle SPECIES_MR_MIME, 26
	dowildbattle
	release
	end
RocketHideout_B3F_EventScript_Yokai122_Text::
	.string "Un {STR_VAR_1} se cache ici.\n"
	.string "Veux-tu le rencontrer?$"

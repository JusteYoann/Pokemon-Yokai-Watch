SevenIsland_SevaultCanyon_MapScripts::
	.byte 0

SevenIsland_SevaultCanyon_EventScript_RouteSign::
	msgbox SevenIsland_SevaultCanyon_Text_RouteSign, MSGBOX_SIGN
	end

SevenIsland_SevaultCanyon_EventScript_Yokai148::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	bufferspeciesname STR_VAR_1, SPECIES_DRAGONAIR
	msgbox SevenIsland_SevaultCanyon_EventScript_Yokai148_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle SPECIES_DRAGONAIR, 60
	dowildbattle
	release
	end
SevenIsland_SevaultCanyon_EventScript_Yokai148_Text::
	.string "Un {STR_VAR_1} se cache ici.\n"
	.string "Veux-tu le rencontrer?$"

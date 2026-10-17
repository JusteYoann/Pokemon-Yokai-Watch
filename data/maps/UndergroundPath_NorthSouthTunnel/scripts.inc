UndergroundPath_NorthSouthTunnel_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, UndergroundPath_NorthSouthTunnel_OnTransition
	.byte 0

UndergroundPath_NorthSouthTunnel_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL
	end

UndergroundPath_NorthSouthTunnel_EventScript_Yokai093::
	lock
	faceplayer
	bufferspeciesname STR_VAR_1, SPECIES_HAUNTER
	msgbox UndergroundPath_NorthSouthTunnel_EventScript_Yokai093_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle SPECIES_HAUNTER, 18
	dowildbattle
	release
	end
UndergroundPath_NorthSouthTunnel_EventScript_Yokai093_Text::
	.string "Un {STR_VAR_1} se cache ici.\n"
	.string "Veux-tu le rencontrer?$"

UndergroundPath_EastWestTunnel_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, UndergroundPath_EastWestTunnel_OnTransition
	.byte 0

UndergroundPath_EastWestTunnel_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_UNDERGROUND_PATH_EAST_WEST_TUNNEL
	end

UndergroundPath_EastWestTunnel_EventScript_Yokai055::
	lock
	faceplayer
	bufferspeciesname STR_VAR_1, SPECIES_GOLDUCK
	msgbox UndergroundPath_EastWestTunnel_EventScript_Yokai055_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle SPECIES_GOLDUCK, 20
	dowildbattle
	release
	end
UndergroundPath_EastWestTunnel_EventScript_Yokai055_Text::
	.string "Un {STR_VAR_1} se cache ici.\n"
	.string "Veux-tu le rencontrer?$"

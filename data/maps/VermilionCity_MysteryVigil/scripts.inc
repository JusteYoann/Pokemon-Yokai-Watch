VermilionCity_MysteryVigil_MapScripts::
	.byte 0

VermilionCity_MysteryVigil_EventScript_Return::
	lockall
	msgbox VermilionCity_MysteryVigil_Text_Return
	closemessage
	warp MAP_VERMILION_CITY_GYM, 255, 8, 12
	waitstate
	releaseall
	end

VermilionCity_MysteryVigil_EventScript_Done::
	lockall
	setflag FLAG_SCENARIO_DOOR_VIGIL_DONE
	msgbox VermilionCity_MysteryVigil_Text_Done
	closemessage
	warp MAP_VERMILION_CITY_GYM, 255, 8, 12
	waitstate
	releaseall
	end

VermilionCity_MysteryDream_MapScripts::
	.byte 0

VermilionCity_MysteryDream_EventScript_Return::
	lockall
	msgbox VermilionCity_MysteryDream_Text_Return
	closemessage
	warp MAP_VERMILION_CITY_GYM, 255, 2, 12
	waitstate
	releaseall
	end

VermilionCity_MysteryDream_EventScript_Done::
	lockall
	setflag FLAG_SCENARIO_DOOR_DREAM_DONE
	msgbox VermilionCity_MysteryDream_Text_Done
	closemessage
	warp MAP_VERMILION_CITY_GYM, 255, 2, 12
	waitstate
	releaseall
	end

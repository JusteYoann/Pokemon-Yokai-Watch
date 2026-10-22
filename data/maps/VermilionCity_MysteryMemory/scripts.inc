VermilionCity_MysteryMemory_MapScripts::
	.byte 0

VermilionCity_MysteryMemory_EventScript_Return::
	lockall
	msgbox VermilionCity_MysteryMemory_Text_Return
	closemessage
	warp MAP_VERMILION_CITY_GYM, 255, 5, 12
	waitstate
	releaseall
	end

VermilionCity_MysteryMemory_EventScript_Done::
	lockall
	setflag FLAG_SCENARIO_DOOR_MEMORY_DONE
	msgbox VermilionCity_MysteryMemory_Text_Done
	closemessage
	warp MAP_VERMILION_CITY_GYM, 255, 5, 12
	waitstate
	releaseall
	end

VermilionCity_MysteryMemory_EventScript_Wrong::
	msgbox VermilionCity_MysteryMemory_Text_Wrong, MSGBOX_SIGN
	end

VermilionCity_MysteryMemory_EventScript_Clue::
	msgbox VermilionCity_MysteryMemory_Text_Clue, MSGBOX_SIGN
	end

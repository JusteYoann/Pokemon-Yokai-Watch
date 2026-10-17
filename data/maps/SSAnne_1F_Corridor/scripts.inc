SSAnne_1F_Corridor_MapScripts::
	.byte 0

SSAnne_1F_Corridor_EventScript_WorkerM::
	msgbox SSAnne_1F_Corridor_Text_LeStrongSilentType, MSGBOX_NPC
	end

SSAnne_1F_Corridor_EventScript_Sailor::
	msgbox SSAnne_1F_Corridor_Text_PassengersAreRestless, MSGBOX_NPC
	end

SSAnne_1F_Corridor_EventScript_Yokai096::
	lock
	faceplayer
	bufferspeciesname STR_VAR_1, SPECIES_DROWZEE
	msgbox SSAnne_1F_Corridor_EventScript_Yokai096_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle SPECIES_DROWZEE, 20
	dowildbattle
	release
	end
SSAnne_1F_Corridor_EventScript_Yokai096_Text::
	.string "Un {STR_VAR_1} se cache ici.\n"
	.string "Veux-tu le rencontrer?$"

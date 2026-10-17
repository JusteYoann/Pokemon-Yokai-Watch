Route17_MapScripts::
	.byte 0

Route17_EventScript_ItemsNotice::
	msgbox Route17_Text_WatchOutForDiscardedItems, MSGBOX_SIGN
	end

Route17_EventScript_TrainerTips1::
	msgbox Route17_Text_SameSpeciesGrowDifferentRates, MSGBOX_SIGN
	end

Route17_EventScript_TrainerTips2::
	msgbox Route17_Text_PressBToStayInPlace, MSGBOX_SIGN
	end

Route17_EventScript_RouteSign::
	msgbox Route17_Text_RouteSign, MSGBOX_SIGN
	end

Route17_EventScript_BallsNotice::
	msgbox Route17_Text_DontThrowGameThrowBalls, MSGBOX_SIGN
	end

Route17_EventScript_CyclingRoadSign::
	msgbox Route17_Text_CyclingRoadSign, MSGBOX_SIGN
	end

Route17_EventScript_Yokai133::
	lock
	faceplayer
	bufferspeciesname STR_VAR_1, SPECIES_EEVEE
	msgbox Route17_EventScript_Yokai133_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle SPECIES_EEVEE, 38
	dowildbattle
	release
	end
Route17_EventScript_Yokai133_Text::
	.string "Un {STR_VAR_1} se cache ici.\n"
	.string "Veux-tu le rencontrer?$"

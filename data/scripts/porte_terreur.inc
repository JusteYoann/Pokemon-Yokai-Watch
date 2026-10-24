@ Demonstration only: no map references this script and no destination is set.
PorteTerreur_EventScript_Apercu::
	lockall
	special PorteTerreurOuvrir
	goto_if_eq VAR_RESULT, FALSE, PorteTerreur_EventScript_Fin
	waitstate
	delay 45
	fadescreen FADE_FROM_WHITE
PorteTerreur_EventScript_Fin::
	releaseall
	end

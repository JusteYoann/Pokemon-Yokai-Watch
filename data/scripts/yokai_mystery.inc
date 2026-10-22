@ First reversible Mystery Doors chapter. No new boss party or item reward.
YokaiMystery_EventScript_JobardCity::
	lock
	faceplayer
	goto_if_unset FLAG_BADGE03_GET, YokaiMystery_EventScript_NotReady
	setflag FLAG_MYSTERY_JOBARD_MET
	msgbox YokaiMystery_Text_Invitation, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, YokaiMystery_EventScript_Cancel
	warp MAP_YOKAIMYSTERY_LAB, 6, 7
	waitstate
	release
	end

YokaiMystery_EventScript_NotReady::
	msgbox YokaiMystery_Text_NotReady
	release
	end

YokaiMystery_EventScript_JobardLab::
	lock
	faceplayer
	goto_if_set FLAG_MYSTERY_CALIBRATED, YokaiMystery_EventScript_Calibrated
	goto_if_unset FLAG_MYSTERY_STABILITY_OBSERVED, YokaiMystery_EventScript_Incomplete
	goto_if_unset FLAG_MYSTERY_ORIENTATION_OBSERVED, YokaiMystery_EventScript_Incomplete
	goto_if_unset FLAG_MYSTERY_RETURN_OBSERVED, YokaiMystery_EventScript_Incomplete
	setflag FLAG_MYSTERY_CALIBRATED
YokaiMystery_EventScript_Calibrated::
	msgbox YokaiMystery_Text_Calibrated
	release
	end

YokaiMystery_EventScript_Incomplete::
	msgbox YokaiMystery_Text_Incomplete
	release
	end

YokaiMystery_EventScript_SelectDoor::
	lockall
	message YokaiMystery_Text_SelectDoor
	waitmessage
	multichoice 8, 4, MULTICHOICE_YOKAI_MYSTERY, FALSE
	switch VAR_RESULT
	case 0, YokaiMystery_EventScript_OpenStability
	case 1, YokaiMystery_EventScript_OpenOrientation
	case 2, YokaiMystery_EventScript_OpenReturn
	closemessage
	releaseall
	end

YokaiMystery_EventScript_OpenStability::
	closemessage
	warp MAP_YOKAIMYSTERY_STABILITY, 6, 7
	waitstate
	releaseall
	end

YokaiMystery_EventScript_OpenOrientation::
	closemessage
	warp MAP_YOKAIMYSTERY_ORIENTATION, 6, 7
	waitstate
	releaseall
	end

YokaiMystery_EventScript_OpenReturn::
	closemessage
	warp MAP_YOKAIMYSTERY_RETURN, 6, 7
	waitstate
	releaseall
	end

YokaiMystery_EventScript_Observe1::
	lockall
	msgbox YokaiMystery_Text_ObserveStability
	setflag FLAG_MYSTERY_STABILITY_OBSERVED
	releaseall
	end

YokaiMystery_EventScript_Observe2::
	lockall
	msgbox YokaiMystery_Text_ObserveOrientation
	setflag FLAG_MYSTERY_ORIENTATION_OBSERVED
	releaseall
	end

YokaiMystery_EventScript_Observe3::
	lockall
	msgbox YokaiMystery_Text_ObserveReturn
	setflag FLAG_MYSTERY_RETURN_OBSERVED
	releaseall
	end

YokaiMystery_EventScript_ReturnLab::
	lockall
	warp MAP_YOKAIMYSTERY_LAB, 6, 7
	waitstate
	releaseall
	end

YokaiMystery_EventScript_LeaveLab::
	lockall
	warp MAP_VERMILION_CITY, 28, 10
	waitstate
	releaseall
	end

YokaiMystery_EventScript_Cancel::
	release
	end

YokaiMystery_Text_NotReady::
	.string "Dr Jobard: Mes instruments\n"
	.string "sont encore en préparation.\p"
	.string "Reviens après ton épreuve\n"
	.string "avec Ariane à l'arène.$"

YokaiMystery_Text_Invitation::
	.string "Dr Jobard: Le trophée d'Ariane!\n"
	.string "Tu pourrais m'aider!\p"
	.string "J'étudie les Portes Mystères.\n"
	.string "Elles relient des espaces isolés.\p"
	.string "Mon laboratoire est prêt.\n"
	.string "Tu veux venir observer les portes?$"

YokaiMystery_Text_Incomplete::
	.string "Dr Jobard: L'ordinateur commande\n"
	.string "les trois Portes Mystères.\p"
	.string "Dans chaque salle, lis la console\n"
	.string "pour relever une mesure.\p"
	.string "Les trois passages au sud\n"
	.string "te ramènent au laboratoire.\p"
	.string "Ici, la sortie au sud te ramène\n"
	.string "à Carmin, quand tu veux.$"

YokaiMystery_Text_Calibrated::
	.string "Dr Jobard: Les trois mesures!\n"
	.string "Le calibrage est terminé.\p"
	.string "Ces relevés pourront servir\n"
	.string "à mes recherches chez Yopple.\p"
	.string "Merci pour ton aide.\n"
	.string "Les portes restent accessibles.$"

YokaiMystery_Text_SelectDoor::
	.string "Quelle Porte Mystère\n"
	.string "veux-tu observer?$"

YokaiMystery_Text_ObserveStability::
	.string "STABILITÉ\p"
	.string "Le signal reste stable\n"
	.string "entre les deux côtés de la porte.\p"
	.string "La console enregistre la mesure.$"

YokaiMystery_Text_ObserveOrientation::
	.string "ORIENTATION\p"
	.string "Le passage change de lieu,\n"
	.string "mais conserve le point d'arrivée.\p"
	.string "La console enregistre la mesure.$"

YokaiMystery_Text_ObserveReturn::
	.string "RETOUR\p"
	.string "Le passage du sud ramène\n"
	.string "toujours au laboratoire.\p"
	.string "La console enregistre la mesure.$"

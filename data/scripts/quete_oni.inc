@ Permanent progression uses unused flags, independent of League opponents.
Onis_EventScript_SyncBraise::
	setflag FLAG_HIDE_ONI_GORGOUILLE
	setflag FLAG_HIDE_ONI_ALIZON
	setvar VAR_TEMP_4, 1
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_Return
	goto_if_unset FLAG_ONI_GARGAROS_WON, EventScript_Return
	goto_if_unset FLAG_ONI_OGRALOS_WON, EventScript_Return
	goto_if_unset FLAG_ONI_ORQANOS_WON, EventScript_Return
	goto_if_unset FLAG_ONI_GORGOUILLE_READY, EventScript_Return
	goto_if_set FLAG_ONI_GORGOUILLE_CAUGHT, EventScript_Return
	clearflag FLAG_HIDE_ONI_GORGOUILLE
	setvar VAR_TEMP_4, 0
	return

@ Called before the return-to-field picture is displayed, as for Mewtwo.
Onis_EventScript_ReturnFromGorgouille::
	goto_if_ne VAR_LAST_TALKED, 1, EventScript_Return
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Onis_EventScript_HideCaughtGorgouille
	goto_if_ne VAR_RESULT, B_OUTCOME_WON, EventScript_Return
	goto Onis_EventScript_HideGorgouille
Onis_EventScript_HideCaughtGorgouille::
	setflag FLAG_ONI_GORGOUILLE_CAUGHT
Onis_EventScript_HideGorgouille::
	setflag FLAG_HIDE_ONI_GORGOUILLE
	removeobject 1
	return

Onis_EventScript_ApproachGorgouille::
	setvar VAR_TEMP_4, 1
	lockall
	call Onis_EventScript_Arrival
	goto_if_ne VAR_TEMP_4, 2, Onis_EventScript_Blocked
	releaseall
	end
Onis_EventScript_Arrival::
	setobjectxyperm 7, 9, 15
	special GorgouilleAlizonArrival
	waitstate
	goto_if_eq VAR_RESULT, FALSE, EventScript_Return
	msgbox Onis_Text_Mythical
	setvar VAR_TEMP_4, 2
	return
Onis_EventScript_Blocked::
	msgbox Onis_Text_PathBlocked
	releaseall
	end

@ Entered with lock + faceplayer from the original Tower badge script.
Onis_EventScript_AlizonTour::
	goto_if_set FLAG_ONI_GORGOUILLE_CAUGHT, Onis_EventScript_QuestDone
	goto_if_set FLAG_ONI_QUEST_ACCEPTED, Onis_EventScript_CheckShort
	msgbox Onis_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Onis_EventScript_Decline
	setflag FLAG_ONI_QUEST_ACCEPTED
Onis_EventScript_CheckShort::
	goto_if_set FLAG_ONI_SHORT_GIVEN, Onis_EventScript_CheckVictories
	checkitemspace ITEM_SHORT_ONI, 1
	goto_if_eq VAR_RESULT, FALSE, Onis_EventScript_NoRoom
	giveitem ITEM_SHORT_ONI, 1
	setflag FLAG_ONI_SHORT_GIVEN
	msgbox Onis_Text_Short
Onis_EventScript_CheckVictories::
	goto_if_unset FLAG_ONI_GARGAROS_WON, Onis_EventScript_MissingVictories
	goto_if_unset FLAG_ONI_OGRALOS_WON, Onis_EventScript_MissingVictories
	goto_if_unset FLAG_ONI_ORQANOS_WON, Onis_EventScript_MissingVictories
	setflag FLAG_ONI_GORGOUILLE_READY
	msgbox Onis_Text_Rendezvous
	release
	end
Onis_EventScript_MissingVictories::
	msgbox Onis_Text_Investigate
	release
	end
Onis_EventScript_NoRoom::
	msgbox Onis_Text_NoRoom
	release
	end
Onis_EventScript_Decline::
	msgbox Onis_Text_Decline
	release
	end
Onis_EventScript_QuestDone::
	msgbox Onis_Text_QuestDone
	release
	end

Onis_EventScript_AlizonBraise::
	lockall
	faceplayer
	goto_if_set FLAG_ONI_GORGOUILLE_CAUGHT, Onis_EventScript_Captured
	msgbox Onis_Text_Mythical
	release
	end

Onis_EventScript_Gorgouille::
	goto_if_questlog Onis_EventScript_End
	lockall
	goto_if_unset FLAG_ONI_GARGAROS_WON, EventScript_ReleaseEnd
	goto_if_unset FLAG_ONI_OGRALOS_WON, EventScript_ReleaseEnd
	goto_if_unset FLAG_ONI_ORQANOS_WON, EventScript_ReleaseEnd
	goto_if_unset FLAG_ONI_GORGOUILLE_READY, EventScript_ReleaseEnd
	goto_if_set FLAG_ONI_GORGOUILLE_CAUGHT, EventScript_ReleaseEnd
	special QuestLog_CutRecording
	goto_if_eq VAR_TEMP_4, 2, Onis_EventScript_StartGorgouille
	setvar VAR_TEMP_4, 1
	call Onis_EventScript_Arrival
	goto_if_ne VAR_TEMP_4, 2, Onis_EventScript_Blocked
Onis_EventScript_StartGorgouille::
	closemessage
	setvar VAR_LAST_TALKED, 1
	setwildbattle SPECIES_ALAKAZAM, 80
	playmoncry SPECIES_ALAKAZAM, CRY_MODE_ENCOUNTER
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Onis_EventScript_Captured
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Onis_EventScript_KnockedOut
	release
	end
Onis_EventScript_KnockedOut::
	setflag FLAG_HIDE_ONI_GORGOUILLE
	removeobject 1
	msgbox Onis_Text_KnockedOut
	release
	end
Onis_EventScript_Captured::
	setflag FLAG_ONI_GORGOUILLE_CAUGHT
	setflag FLAG_HIDE_ONI_GORGOUILLE
	removeobject 1
	msgbox Onis_Text_Captured
	closemessage
	special GorgouilleAlizonDeparture
	waitstate
	goto_if_eq VAR_RESULT, FALSE, Onis_EventScript_Blocked
	releaseall
	end

Onis_Text_PathBlocked::
	.string "Alizon Bie: Le passage est bloqué.\n"
	.string "Dégage-le et reparle-moi.$"

Onis_Text_Offer::
	.string "Alizon Bie: Tu te souviens de\n"
	.string "notre Zombie Night? Quelle nuit!\p"
	.string "J’enquête sur la Terr’heure:\n"
	.string "des grottes changent d’aspect...\p"
	.string "Gargaros, Ogralos et Orqanos\n"
	.string "y traquent les imprudents.\p"
	.string "Une légende promet un cadeau\n"
	.string "mythique à qui bat ces trois Oni.\p"
	.string "Tu veux enquêter avec moi?$"
Onis_Text_Short::
	.string "Fais porter ce Short Oni à\n"
	.string "un Yo-kai de ton équipe.\p"
	.string "Il attire la Terr’heure dans\n"
	.string "les grandes grottes. Sois prudent!$"
Onis_Text_Investigate::
	.string "Alizon Bie: Il faut vaincre\n"
	.string "Gargaros, Ogralos et Orqanos.\p"
	.string "La porte permet de s’échapper,\n"
	.string "mais ne gagne pas leur respect!\p"
	.string "Tes victoires passées comptent\n"
	.string "aussi. Reviens après les trois!$"
Onis_Text_Rendezvous::
	.string "Alizon Bie: Les trois Oni vaincus!\n"
	.string "Tu as fait fort!\p"
	.string "J’ai trouvé la récompense de\n"
	.string "la légende: au Mont Braise!\p"
	.string "Retrouve-moi au sommet.\n"
	.string "Et prends des Yo-kai Balls!$"
Onis_Text_Mythical::
	.string "Alizon Bie: Voici Gorgouille,\n"
	.string "la récompense mythique des Oni!\p"
	.string "Tu as été meilleur que moi\n"
	.string "dans cette enquête. Je l’avoue!\p"
	.string "À toi l’honneur de le capturer.\n"
	.string "Vas-y, je te regarde!$"
Onis_Text_KnockedOut::
	.string "Alizon Bie: Mais quel imbécile!\n"
	.string "J’ai dit CAPTURER, pas assommer!\p"
	.string "Je te taquine. Il reviendra:\n"
	.string "quitte les lieux, puis reviens.\p"
	.string "Avec des Yo-kai Balls, cette fois!$"
Onis_Text_Captured::
	.string "Alizon Bie: Tu as réussi!\n"
	.string "Gorgouille est ton nouvel ami!\p"
	.string "Quelle enquête! Merci pour\n"
	.string "ton aide. À bientôt!$"
Onis_Text_QuestDone::
	.string "Alizon Bie: Prends bien soin\n"
	.string "de Gorgouille!\p"
	.string "Je cherche déjà notre prochaine\n"
	.string "enquête... Tu me connais!$"
Onis_Text_NoRoom::
	.string "Ton SAC est plein. Fais de la\n"
	.string "place pour le Short Oni!$"
Onis_Text_Decline::
	.string "Alizon Bie: Pas de souci!\n"
	.string "Reviens quand tu seras prêt.$"

Onis_EventScript_End::
	end

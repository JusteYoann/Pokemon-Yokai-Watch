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
    .string "Alizon Bie: Alors, tu t'es remis de\nnotre Zombie Night? Mes petits\lparlent encore de toi!\pJe m'intéresse à la Terr'heure.\nLà, même mes zombies hésitent à\lsortir.\pGargaros, Ogralos et Orqanos\ntraquent les visiteurs dans\lcertaines grottes.\pUne légende promet une rencontre\nmythique à qui gagne leur respect.\pTu viens frissonner avec moi?$"

Onis_Text_Short::
    .string "Fais porter ce Short Oni à un\nYo-kai. Il triple les chances de\lTerr'heure dans les grottes\léligibles.\pUn seul porteur suffit! Inutile de\ndéguiser toute ton équipe.\pEt reste prudent. Les Oni, eux, ne\nsont pas mes petits zombies!$"

Onis_Text_Investigate::
	.string "Alizon Bie: Il faut vaincre\n"
	.string "Gargaros, Ogralos et Orqanos.\p"
	.string "La porte permet de s’échapper,\n"
	.string "mais ne gagne pas leur respect!\p"
	.string "Tes victoires passées comptent\n"
	.string "aussi. Reviens après les trois!$"
Onis_Text_Rendezvous::
    .string "Les trois Oni? Vaincus?! Tu sais\nrecevoir les invités difficiles!\pJ'ai retrouvé la rencontre promise\npar la légende. Direction le sommet\ldu Mont Braise!\pEt prends des Yo-kai Balls. On ne\nrentre pas les mains vides!$"

Onis_Text_Mythical::
	.string "Alizon Bie: Voici Gorgouille,\n"
	.string "la récompense mythique des Oni!\p"
	.string "Tu as été meilleur que moi\n"
	.string "dans cette enquête. Je l’avoue!\p"
	.string "À toi l’honneur de le capturer.\n"
	.string "Vas-y, je te regarde!$"
Onis_Text_KnockedOut::
    .string "Tu lui as offert une sieste?!\nJ'avais dit CAPTURER!\pJe te taquine. Il reviendra si tu\nquittes les lieux puis reviens.\pCette fois, n'oublie pas les Yo-kai\nBalls!$"

Onis_Text_Captured::
    .string "Alizon Bie: Quelle rencontre! Et\nvoilà Gorgouille parmi tes amis.\pJe te laisse savourer ça. Je\nreprends le chemin dégagé.\pPromis, j'essaierai de ne pas\nramener de zombies en route!$"

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

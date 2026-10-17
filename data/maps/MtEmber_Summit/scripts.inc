MtEmber_Summit_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtEmber_Summit_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, MtEmber_Summit_OnResume
	.byte 0

MtEmber_Summit_OnResume::
	call_if_set FLAG_SYS_SPECIAL_WILD_BATTLE, MtEmber_Summit_EventScript_TryRemoveMoltres
	end

MtEmber_Summit_EventScript_TryRemoveMoltres::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, EventScript_Return
	removeobject VAR_LAST_TALKED
	return

MtEmber_Summit_OnTransition::
	setflag FLAG_HIDE_YOKAI_LORD_ENMA
	goto_if_unset FLAG_SYS_GAME_CLEAR, MtEmber_Summit_EventScript_CheckKyubi
	clearflag FLAG_HIDE_YOKAI_LORD_ENMA
MtEmber_Summit_EventScript_CheckKyubi::
	call_if_unset FLAG_FOUGHT_MOLTRES, MtEmber_Summit_EventScript_ShowMoltres
	end

MtEmber_Summit_EventScript_ShowMoltres::
	clearflag FLAG_HIDE_MOLTRES
	return

MtEmber_Summit_EventScript_Moltres::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_PIDGEY, 50
	waitse
	playmoncry SPECIES_PIDGEY, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 10
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, MtEmber_Summit_EventScript_DefeatedMoltres
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtEmber_Summit_EventScript_RanFromMoltres
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtEmber_Summit_EventScript_RanFromMoltres
	setflag FLAG_FOUGHT_MOLTRES
	release
	end

MtEmber_Summit_EventScript_DefeatedMoltres::
	setflag FLAG_FOUGHT_MOLTRES
	goto EventScript_RemoveStaticMon
	end

MtEmber_Summit_EventScript_RanFromMoltres::
	setvar VAR_0x8004, SPECIES_PIDGEY
	goto EventScript_MonFlewAway
	end

@ Original cameo, shared with the final Enma trial: no duplicated encounter.
MtEmber_Summit_EventScript_LordEnma::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_set FLAG_YOKAI_ENMA_WON, MtEmber_Summit_EventScript_EnmaRematchOffer
	msgbox MtEmber_Summit_Text_EnmaOffer, MSGBOX_YESNO
	goto MtEmber_Summit_EventScript_EnmaChoice
MtEmber_Summit_EventScript_EnmaRematchOffer::
	msgbox MtEmber_Summit_Text_EnmaRematchOffer, MSGBOX_YESNO
MtEmber_Summit_EventScript_EnmaChoice::
	goto_if_eq VAR_RESULT, NO, MtEmber_Summit_EventScript_EnmaDecline
	closemessage
	cleartrainerflag TRAINER_YOKAI_ENMA
	trainerbattle_single TRAINER_YOKAI_ENMA, MtEmber_Summit_Text_EnmaStart, MtEmber_Summit_Text_EnmaDefeat, MtEmber_Summit_EventScript_EnmaVictory
	closemessage
	release
	end
MtEmber_Summit_EventScript_EnmaVictory::
	closemessage
	goto_if_set FLAG_YOKAI_ENMA_WON, MtEmber_Summit_EventScript_EnmaRematchVictory
	setflag FLAG_YOKAI_ENMA_WON
	msgbox MtEmber_Summit_Text_EnmaUnlocked
	closemessage
	release
	end
MtEmber_Summit_EventScript_EnmaRematchVictory::
	msgbox MtEmber_Summit_Text_EnmaRematchVictory
	closemessage
	release
	end
MtEmber_Summit_EventScript_EnmaDecline::
	msgbox MtEmber_Summit_Text_EnmaDecline
	closemessage
	release
	end
MtEmber_Summit_Text_EnmaOffer::
	.string "Enma: Alors, c’est toi qui as\n"
	.string "remporté la Ligue? Bien joué!\p"
	.string "Moi, c’est Enma. J’adore voir\n"
	.string "ce dont les humains sont capables!\p"
	.string "Tes amis ont l’air redoutables.\n"
	.string "Ça te dit de nous affronter?$"
MtEmber_Summit_Text_EnmaRematchOffer::
	.string "Enma: Te revoilà! Depuis notre\n"
	.string "combat, j’attendais ta visite.\p"
	.string "Cette fois, je ne retiens rien!\n"
	.string "On remet ça?$"
MtEmber_Summit_Text_EnmaStart::
	.string "Enma: Amusons-nous!\n"
	.string "Je compte bien tout donner!$"
MtEmber_Summit_Text_EnmaDefeat::
	.string "Ha ha! Quelle énergie!\n"
	.string "Vous avez été formidables!$"
MtEmber_Summit_Text_EnmaUnlocked::
	.string "Enma: Ce lien avec tes Yo-kai…\n"
	.string "Voilà ce qui fait votre force!\p"
	.string "Un Enma t’attend maintenant\n"
	.string "au fond de la Caverne Azurée.\p"
	.string "Va lui montrer votre force!\n"
	.string "Moi, je reste ici pour la revanche.$"
MtEmber_Summit_Text_EnmaRematchVictory::
	.string "Enma: Excellent! Impossible de\n"
	.string "s’ennuyer contre vous!\p"
	.string "Reviens quand tu veux.\n"
	.string "La prochaine sera encore meilleure!$"
MtEmber_Summit_Text_EnmaDecline::
	.string "Enma: Pas de problème!\n"
	.string "Prends le temps de te préparer.\p"
	.string "Un beau combat, ça se savoure!$"

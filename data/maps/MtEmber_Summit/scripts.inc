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
	playbgm MUS_YOKAI_ENMA_DIALOGUE, 0
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
	fadedefaultbgm
	release
	end
MtEmber_Summit_EventScript_EnmaRematchVictory::
	msgbox MtEmber_Summit_Text_EnmaRematchVictory
	closemessage
	fadedefaultbgm
	release
	end
MtEmber_Summit_EventScript_EnmaDecline::
	msgbox MtEmber_Summit_Text_EnmaDecline
	closemessage
	fadedefaultbgm
	release
	end
MtEmber_Summit_Text_EnmaOffer::
	.string "Enma: Bravo pour la Ligue!\p"
	.string "Je suis le Seigneur Enma.\n"
	.string "J’ai un drôle de protégé…\p"
	.string "Des savants ont tenté de copier\n"
	.string "ma puissance à partir d’un Jibanyan.\p"
	.string "Ils ont créé un Yo-kai céleste\n"
	.string "artificiel, nommé Enma.\p"
	.string "Ce n’est pas moi! Lui et moi,\n"
	.string "nous sommes bien deux êtres.\p"
	.string "Il s’est enfui du laboratoire.\n"
	.string "Je l’ai accueilli et protégé.\p"
	.string "Il combat parfois dans mon équipe!\n"
	.string "Prêt à nous affronter?$"
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
	.string "Enma: Je suis fier de vous!\n"
	.string "Vos liens font votre force.\p"
	.string "L’équilibre entre les humains\n"
	.string "et les Yo-kai reste fragile.\p"
	.string "Je compte beaucoup sur toi\n"
	.string "pour nous aider à le préserver.\p"
	.string "Mon protégé, le Yo-kai Enma,\n"
	.string "est dans la Caverne Azurée.\p"
	.string "Va le rencontrer au plus profond.\n"
	.string "À toi de gagner sa confiance!\p"
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

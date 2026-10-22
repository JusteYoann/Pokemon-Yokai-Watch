Route25_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route25_OnTransitionAriane
	.byte 0

Route25_OnTransitionAriane::
	setflag FLAG_SCENARIO_HIDE_ROUTE25_ARIANE
	setflag FLAG_SCENARIO_ROUTE25_ARIANE_CURRENT
	end

Route25_EventScript_SeaCottageSign::
	msgbox Route25_Text_SeaCottageSign, MSGBOX_SIGN
	end

Route25_EventScript_Man::
	msgbox Route25_Text_AreYouHereAlone, MSGBOX_NPC
	end

Route25_EventScript_Ariane::
	lock
	faceplayer
	playbgm MUS_YOKAI_ARIANE, 0
	goto_if_unset FLAG_YOKAI_ARIANE_WON, Route25_EventScript_ArianeOffer
	goto_if_unset FLAG_YOKAI_ARIANE_REWARD, Route25_EventScript_ArianeReward
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route25_EventScript_ArianeAlreadyWon
Route25_EventScript_ArianeOffer::
	msgbox Route25_Text_ArianeOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route25_EventScript_ArianeDecline
	closemessage
	goto_if_set FLAG_SYS_GAME_CLEAR, Route25_EventScript_ArianePostBattle
	trainerbattle_single TRAINER_YOKAI_ARIANE, Route25_Text_ArianeStart, Route25_Text_ArianeDefeat, Route25_EventScript_ArianeVictory
	closemessage
	goto Route25_EventScript_ArianeMusicEnd
Route25_EventScript_ArianePostBattle::
	cleartrainerflag TRAINER_YOKAI_ARIANE_POST
	trainerbattle_single TRAINER_YOKAI_ARIANE_POST, Route25_Text_ArianePostStart, Route25_Text_ArianeDefeat, Route25_EventScript_ArianePostVictory
	closemessage
	goto Route25_EventScript_ArianeMusicEnd
Route25_EventScript_ArianePostVictory::
	setflag FLAG_YOKAI_ARIANE_POST_WON
Route25_EventScript_ArianeVictory::
	playbgm MUS_YOKAI_ARIANE, 0
	closemessage
	setflag FLAG_YOKAI_ARIANE_WON
	msgbox Route25_Text_ArianeAfterVictory
	goto_if_set FLAG_YOKAI_ARIANE_REWARD, Route25_EventScript_ArianeMusicEnd
Route25_EventScript_ArianeReward::
	checkitemspace ITEM_MOON_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, Route25_EventScript_ArianeBagFull
	msgbox Route25_Text_ArianeReward
	giveitem ITEM_MOON_STONE, 1
	goto_if_eq VAR_0x8007, FALSE, Route25_EventScript_ArianeBagFull
	setflag FLAG_YOKAI_ARIANE_REWARD
	closemessage
	goto Route25_EventScript_ArianeMusicEnd
Route25_EventScript_ArianeAlreadyWon::
	msgbox Route25_Text_ArianeRevisit
	closemessage
	goto Route25_EventScript_ArianeMusicEnd
Route25_EventScript_ArianeDecline::
	msgbox Route25_Text_ArianeDecline
	closemessage
	goto Route25_EventScript_ArianeMusicEnd
Route25_EventScript_ArianeBagFull::
	msgbox Route25_Text_ArianeBagFull
	closemessage
	goto Route25_EventScript_ArianeMusicEnd
Route25_EventScript_ArianeMusicEnd::
	fadedefaultbgm
	release
	end
Route25_EventScript_UsapionCameo::
	lock
	msgbox Route25_Text_UsapionCameo
	closemessage
	release
	end

Route25_Text_ArianeOffer::
	.string "Ariane: Un nouveau mystère!\n"
	.string "Tes Yo-kai m’intriguent.\p"
	.string "Usapyon et moi, on est prêts!\n"
	.string "Tu veux faire un combat?$"
Route25_Text_ArianeStart::
	.string "Allons-y, Usapyon!\n"
	.string "On va leur montrer!$"
Route25_Text_ArianePostStart::
	.string "Emperor et moi avons progressé!\n"
	.string "À toi de le découvrir!$"
Route25_Text_ArianeDefeat::
	.string "Mes calculs étaient presque bons!\n"
	.string "Bon, je vais les revoir…$"
Route25_Text_ArianeAfterVictory::
	.string "Ariane: Quelle équipe incroyable!\n"
	.string "Il faut que je note tout ça.\p"
	.string "La prochaine fois, notre équipe\n"
	.string "essaiera une autre stratégie!$"
Route25_Text_ArianeReward::
	.string "Prends cette Pierre Lune.\n"
	.string "Usapyon peut évoluer grâce à elle.\p"
	.string "Tu trouveras sûrement comment\n"
	.string "en faire bon usage!$"
Route25_Text_ArianeRevisit::
	.string "Ariane: J’ai encore des recherches\n"
	.string "à faire avec Usapyon.\p"
	.string "Reviens après la Ligue!\n"
	.string "On te préparera une surprise.$"
Route25_Text_ArianeDecline::
	.string "Ariane: Pas de souci!\n"
	.string "On reste ici encore un peu.$"
Route25_Text_ArianeBagFull::
	.string "Ariane: Ton sac est plein.\n"
	.string "Je te garde la Pierre Lune!$"
Route25_Text_UsapionCameo::
	.string "Usapyon vérifie son équipement.\n"
	.string "Il semble prêt pour l’aventure!$"

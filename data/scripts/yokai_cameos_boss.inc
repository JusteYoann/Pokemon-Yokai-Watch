@ Optional postgame cameos; original story scripts remain in their maps.

@ The optional postgame CEO cameo is retired. Keep its local event ID hidden
@ for old saves; Domniscian now appears through the rescue story and Gym.
YokaiCameo_Domniscian::
	end

YokaiCameo_EmployeRouge::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_EmployeRougeAdventure
YokaiCameo_EmployeRougeOffer::
	msgbox YokaiCameo_EmployeRougeTextOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, YokaiCameo_EmployeRougeDecline
	closemessage
	cleartrainerflag TRAINER_YOKAI_EMPLOYEROUGE
	trainerbattle_single TRAINER_YOKAI_EMPLOYEROUGE, YokaiCameo_EmployeRougeTextStart, YokaiCameo_EmployeRougeTextDefeat, YokaiCameo_EmployeRougeVictory
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeRougeVictory::
	closemessage
	setflag FLAG_YOKAI_EMPLOYEE_RED_WON
	msgbox YokaiCameo_EmployeRougeTextAfter
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeRougeDecline::
	msgbox YokaiCameo_EmployeRougeTextDecline
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeRougeBlocked::
	msgbox YokaiCameo_EmployeRougeTextBlocked
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeRougeTextOffer::
	.string "Je garde les projets du patron.\n"
	.string "Tu veux faire un combat?$"
YokaiCameo_EmployeRougeTextStart::
	.string "Robonyan, Emperor! Au travail!$"
YokaiCameo_EmployeRougeTextDefeat::
	.string "Pause bien méritée pour mon équipe!$"
YokaiCameo_EmployeRougeTextAfter::
	.string "Belle démonstration!\n"
	.string "Le patron va en entendre parler.$"
YokaiCameo_EmployeRougeTextDecline::
	.string "Pas de souci. Une autre fois.$"
YokaiCameo_EmployeRougeTextBlocked::
	.string "Reviens après ta victoire\n"
	.string "à la Ligue de Kanto.$"

YokaiCameo_EmployeBleu::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_EmployeBleuAdventure
YokaiCameo_EmployeBleuOffer::
	msgbox YokaiCameo_EmployeBleuTextOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, YokaiCameo_EmployeBleuDecline
	closemessage
	cleartrainerflag TRAINER_YOKAI_EMPLOYEBLEU
	trainerbattle_single TRAINER_YOKAI_EMPLOYEBLEU, YokaiCameo_EmployeBleuTextStart, YokaiCameo_EmployeBleuTextDefeat, YokaiCameo_EmployeBleuVictory
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeBleuVictory::
	closemessage
	setflag FLAG_YOKAI_EMPLOYEE_BLUE_WON
	msgbox YokaiCameo_EmployeBleuTextAfter
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeBleuDecline::
	msgbox YokaiCameo_EmployeBleuTextDecline
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeBleuBlocked::
	msgbox YokaiCameo_EmployeBleuTextBlocked
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeBleuTextOffer::
	.string "Mon équipe vérifie ton niveau.\n"
	.string "Tu acceptes le combat?$"
YokaiCameo_EmployeBleuTextStart::
	.string "Usapyon, Robonyan F! À vous!$"
YokaiCameo_EmployeBleuTextDefeat::
	.string "Notre rapport est clair: tu gagnes!$"
YokaiCameo_EmployeBleuTextAfter::
	.string "Ton équipe est prête.\n"
	.string "Reviens nous défier quand tu veux!$"
YokaiCameo_EmployeBleuTextDecline::
	.string "Pas de souci. Une autre fois.$"
YokaiCameo_EmployeBleuTextBlocked::
	.string "Reviens après ta victoire\n"
	.string "à la Ligue de Kanto.$"

YokaiCameo_Mafiamille1::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_Mafiamille1Blocked
YokaiCameo_Mafiamille1Offer::
	msgbox YokaiCameo_Mafiamille1TextOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, YokaiCameo_Mafiamille1Decline
	closemessage
	cleartrainerflag TRAINER_YOKAI_MAFIAMILLE1
	trainerbattle_single TRAINER_YOKAI_MAFIAMILLE1, YokaiCameo_Mafiamille1TextStart, YokaiCameo_Mafiamille1TextDefeat, YokaiCameo_Mafiamille1Victory
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille1Victory::
	closemessage
	setflag FLAG_YOKAI_MAFIA1_WON
	msgbox YokaiCameo_Mafiamille1TextAfter
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille1Decline::
	msgbox YokaiCameo_Mafiamille1TextDecline
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille1Blocked::
	msgbox YokaiCameo_Mafiamille1TextBlocked
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille1TextOffer::
	.string "Le patron reçoit sur rendez-vous.\n"
	.string "Un combat pour commencer?$"
YokaiCameo_Mafiamille1TextStart::
	.string "Bouh, on fait ça proprement!$"
YokaiCameo_Mafiamille1TextDefeat::
	.string "J’ai sous-estimé ton équipe!$"
YokaiCameo_Mafiamille1TextAfter::
	.string "Tu as passé mon contrôle.\n"
	.string "Je préviens le patron.$"
YokaiCameo_Mafiamille1TextDecline::
	.string "Pas de souci. Une autre fois.$"
YokaiCameo_Mafiamille1TextBlocked::
	.string "Reviens après ta victoire\n"
	.string "à la Ligue de Kanto.$"

YokaiCameo_Mafiamille2::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_Mafiamille2Blocked
YokaiCameo_Mafiamille2Offer::
	msgbox YokaiCameo_Mafiamille2TextOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, YokaiCameo_Mafiamille2Decline
	closemessage
	cleartrainerflag TRAINER_YOKAI_MAFIAMILLE2
	trainerbattle_single TRAINER_YOKAI_MAFIAMILLE2, YokaiCameo_Mafiamille2TextStart, YokaiCameo_Mafiamille2TextDefeat, YokaiCameo_Mafiamille2Victory
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille2Victory::
	closemessage
	setflag FLAG_YOKAI_MAFIA2_WON
	msgbox YokaiCameo_Mafiamille2TextAfter
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille2Decline::
	msgbox YokaiCameo_Mafiamille2TextDecline
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille2Blocked::
	msgbox YokaiCameo_Mafiamille2TextBlocked
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille2TextOffer::
	.string "La famille teste chaque visiteur.\n"
	.string "Tu veux tenter ta chance?$"
YokaiCameo_Mafiamille2TextStart::
	.string "Gardons nos cartes en main!$"
YokaiCameo_Mafiamille2TextDefeat::
	.string "Cette fois, tes cartes gagnent.$"
YokaiCameo_Mafiamille2TextAfter::
	.string "Bien joué. On tient toujours\n"
	.string "notre parole dans la famille.$"
YokaiCameo_Mafiamille2TextDecline::
	.string "Pas de souci. Une autre fois.$"
YokaiCameo_Mafiamille2TextBlocked::
	.string "Reviens après ta victoire\n"
	.string "à la Ligue de Kanto.$"

YokaiCameo_Mafiamille3::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_Mafiamille3Blocked
YokaiCameo_Mafiamille3Offer::
	msgbox YokaiCameo_Mafiamille3TextOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, YokaiCameo_Mafiamille3Decline
	closemessage
	cleartrainerflag TRAINER_YOKAI_MAFIAMILLE3
	trainerbattle_single TRAINER_YOKAI_MAFIAMILLE3, YokaiCameo_Mafiamille3TextStart, YokaiCameo_Mafiamille3TextDefeat, YokaiCameo_Mafiamille3Victory
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille3Victory::
	closemessage
	setflag FLAG_YOKAI_MAFIA3_WON
	msgbox YokaiCameo_Mafiamille3TextAfter
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille3Decline::
	msgbox YokaiCameo_Mafiamille3TextDecline
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille3Blocked::
	msgbox YokaiCameo_Mafiamille3TextBlocked
	goto EventScript_ReleaseEnd
YokaiCameo_Mafiamille3TextOffer::
	.string "Pas de bagarre sans accord.\n"
	.string "Un combat de Yo-kai, ça te va?$"
YokaiCameo_Mafiamille3TextStart::
	.string "À nous de montrer notre force!$"
YokaiCameo_Mafiamille3TextDefeat::
	.string "D’accord. On se calme!$"
YokaiCameo_Mafiamille3TextAfter::
	.string "Tu as notre respect.\n"
	.string "Va parler au patron.$"
YokaiCameo_Mafiamille3TextDecline::
	.string "Pas de souci. Une autre fois.$"
YokaiCameo_Mafiamille3TextBlocked::
	.string "Reviens après ta victoire\n"
	.string "à la Ligue de Kanto.$"

YokaiCameo_EmployeRougeAdventure::
	msgbox YokaiCameo_EmployeRougeTextAdventure
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeRougeTextAdventure::
	.string "Steve Jaws a fondé Yopple.\p"
	.string "La Yo-kai Watch et les Yo-kai Balls\n"
	.string "font partie de son héritage.$"

YokaiCameo_EmployeBleuAdventure::
	msgbox YokaiCameo_EmployeBleuTextAdventure
	goto EventScript_ReleaseEnd
YokaiCameo_EmployeBleuTextAdventure::
	.string "Le Yo-kai Pad et l’aspirateur\n"
	.string "à Yo-kai sont conçus chez Yopple.\p"
	.string "Domniscian a racheté l’entreprise.\n"
	.string "Il adore nous le rappeler!$"

@ Optional postgame cameos; original story scripts remain in their maps.

YokaiCameo_Domniscian::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_DomniscianBlocked
	goto_if_unset FLAG_YOKAI_EMPLOYEE_RED_WON, YokaiCameo_DomniscianNeed
	goto_if_unset FLAG_YOKAI_EMPLOYEE_BLUE_WON, YokaiCameo_DomniscianNeed
	goto_if_unset FLAG_YOKAI_DOMNISCIAN_WON, YokaiCameo_DomniscianOffer
	goto_if_unset FLAG_YOKAI_DOMNISCIAN_REWARD, YokaiCameo_DomniscianReward
YokaiCameo_DomniscianOffer::
	msgbox YokaiCameo_DomniscianTextOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, YokaiCameo_DomniscianDecline
	closemessage
	cleartrainerflag TRAINER_YOKAI_DOMNISCIAN
	trainerbattle_single TRAINER_YOKAI_DOMNISCIAN, YokaiCameo_DomniscianTextStart, YokaiCameo_DomniscianTextDefeat, YokaiCameo_DomniscianVictory
	goto EventScript_ReleaseEnd
YokaiCameo_DomniscianVictory::
	closemessage
	setflag FLAG_YOKAI_DOMNISCIAN_WON
	msgbox YokaiCameo_DomniscianTextAfter
	goto_if_set FLAG_YOKAI_DOMNISCIAN_REWARD, EventScript_ReleaseEnd
YokaiCameo_DomniscianReward::
	checkitemspace ITEM_THUNDER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, YokaiCameo_DomniscianBagFull
	msgbox YokaiCameo_DomniscianTextReward
	giveitem ITEM_THUNDER_STONE, 1
	goto_if_eq VAR_0x8007, FALSE, YokaiCameo_DomniscianBagFull
	setflag FLAG_YOKAI_DOMNISCIAN_REWARD
	goto EventScript_ReleaseEnd
YokaiCameo_DomniscianDecline::
	msgbox YokaiCameo_DomniscianTextDecline
	goto EventScript_ReleaseEnd
YokaiCameo_DomniscianBlocked::
	msgbox YokaiCameo_DomniscianTextBlocked
	goto EventScript_ReleaseEnd
YokaiCameo_DomniscianNeed::
	msgbox YokaiCameo_DomniscianTextNeed
	goto EventScript_ReleaseEnd
YokaiCameo_DomniscianBagFull::
	msgbox YokaiCameo_DomniscianTextBagFull
	goto EventScript_ReleaseEnd
YokaiCameo_DomniscianTextOffer::
	.string "Domniscian: Voici mon grand projet!\n"
	.string "Un combat digne de mon génie?$"
YokaiCameo_DomniscianTextStart::
	.string "Mes meilleurs collaborateurs!\n"
	.string "Même les petits ont du talent!$"
YokaiCameo_DomniscianTextDefeat::
	.string "Impossible! Mon idée était parfaite!$"
YokaiCameo_DomniscianTextAfter::
	.string "D’accord, ton équipe mérite\n"
	.string "une place au générique!$"
YokaiCameo_DomniscianTextNeed::
	.string "Mes employés veulent te rencontrer.\n"
	.string "Bats-les avant de me défier!$"
YokaiCameo_DomniscianTextReward::
	.string "Cette Pierre Foudre fait évoluer\n"
	.string "Komaous en Komastar.$"
YokaiCameo_DomniscianTextDecline::
	.string "Pas de souci. Une autre fois.$"
YokaiCameo_DomniscianTextBlocked::
	.string "Reviens après ta victoire\n"
	.string "à la Ligue de Kanto.$"
YokaiCameo_DomniscianTextBagFull::
	.string "Ton sac est plein.\n"
	.string "Je garde ta récompense pour toi.$"

YokaiCameo_EmployeRouge::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_EmployeRougeBlocked
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
	.string "Jibanyan, Feulion! Au travail!$"
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
	goto_if_unset FLAG_SYS_GAME_CLEAR, YokaiCameo_EmployeBleuBlocked
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
	.string "Komasan, Robonyan! À vous!$"
YokaiCameo_EmployeBleuTextDefeat::
	.string "Notre rapport est clair: tu gagnes!$"
YokaiCameo_EmployeBleuTextAfter::
	.string "Ton équipe est prête.\n"
	.string "Garde cette énergie pour le patron!$"
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

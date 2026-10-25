@ Stationary, front-facing creator encounter. Reproduction authorized by the user.
Yoann_EventScript_NPC::
	lockall
	goto_if_unset FLAG_YOANN_INVITED, Yoann_EventScript_Release
	goto_if_set FLAG_YOANN_CHARM_GIVEN, Yoann_EventScript_Again
	goto_if_set FLAG_YOANN_WON, Yoann_EventScript_Reward
	msgbox Yoann_Text_Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Yoann_EventScript_Decline
	trainerbattle_single TRAINER_JUSTE_YOANN, Yoann_Text_BattleStart, Yoann_Text_Defeat, Yoann_EventScript_FirstVictory
	releaseall
	end

Yoann_EventScript_Decline::
	msgbox Yoann_Text_Decline
	goto Yoann_EventScript_Release

Yoann_EventScript_Again::
	msgbox Yoann_Text_Again
Yoann_EventScript_Release::
	releaseall
	end

Yoann_EventScript_ChenInvitation::
	msgbox Yoann_Text_Chen
	setflag FLAG_YOANN_INVITED
	return

Yoann_EventScript_FirstVictory::
	lockall
	setflag FLAG_YOANN_WON
	msgbox Yoann_Text_Victory
	setvar VAR_0x8004, 0
	setvar VAR_0x8005, 2
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks0
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks1
	setvar VAR_0x8004, 3
	setvar VAR_0x8005, 5
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks2
	setvar VAR_0x8004, 5
	setvar VAR_0x8005, 7
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks3
	setvar VAR_0x8004, 7
	setvar VAR_0x8005, 8
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks4
	setvar VAR_0x8004, 8
	setvar VAR_0x8005, 9
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks5
	setvar VAR_0x8004, 9
	setvar VAR_0x8005, 10
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks6
	setvar VAR_0x8004, 10
	setvar VAR_0x8005, 11
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks7
	setvar VAR_0x8004, 11
	setvar VAR_0x8005, 12
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks8
	setvar VAR_0x8004, 12
	setvar VAR_0x8005, 13
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks9
	setvar VAR_0x8004, 13
	setvar VAR_0x8005, 14
	special YoannFadeWhite
	waitstate
	msgbox Yoann_Text_Thanks10
	closemessage
	special YoannThankForPlay
	waitstate
	special YoannPostgameCredits
	waitstate
	goto Yoann_EventScript_Reward

Yoann_EventScript_Reward::
	msgbox Yoann_Text_Reward
	special YoannGiveCharm
	goto_if_eq VAR_RESULT, FALSE, Yoann_EventScript_BagFull
	playfanfare MUS_OBTAIN_KEY_ITEM
	msgbox Yoann_Text_Received
	waitfanfare
	msgbox Yoann_Text_RewardEnd
	releaseall
	end

Yoann_EventScript_BagFull::
	msgbox Yoann_Text_BagFull
	releaseall
	end

Yoann_Text_Chen::
	.string "Incroyable ! Tu as réussi !\p"
	.string "Les 151 Yo-kai de Kanto sont\n"
	.string "désormais enregistrés dans ton\l"
	.string "Médallium !\p"
	.string "Voilà un exploit dont tu peux\n"
	.string "être fier !\p"
	.string "Ah ! J'allais oublier...\p"
	.string "Une personne assez particulière\n"
	.string "est venue me voir récemment.\p"
	.string "Elle m'a demandé de te prévenir\n"
	.string "qu'elle t'attendait... chez toi\l"
	.string "!\p"
	.string "Tu devrais aller voir de qui il\n"
	.string "s'agit.$"

Yoann_Text_Intro::
	.string "Ah ! Te voilà enfin !\p"
	.string "Alors comme ça, c'est toi qui as\n"
	.string "réussi à compléter le Médallium\l"
	.string "?\p"
	.string "Je dois reconnaître que tu\n"
	.string "m'impressionnes !\p"
	.string "Tu sais quoi ? Avant de\n"
	.string "discuter, j'ai une petite\l"
	.string "proposition à te faire...\p"
	.string "Ça te dit un dernier combat ?$"

Yoann_Text_Victory::
	.string "Ahahah ! Eh bien, tu m'as eu !\p"
	.string "Bon... Je vais être honnête avec\n"
	.string "toi.\p"
	.string "Je suis peut-être pas le\n"
	.string "meilleur stratège de Yo-kai\l"
	.string "Watch.\p"
	.string "Nyleco est bien meilleur que moi\n"
	.string "à ce petit jeu !\p"
	.string "Mais tu sais...\p"
	.string "Il y a quelque chose que\n"
	.string "j'aimerais te dire.\p"
	.string "Quelque chose d'un peu plus\n"
	.string "personnel.$"

Yoann_Text_Thanks0::
	.string "Merci.$"

Yoann_Text_Thanks1::
	.string "Merci d'avoir pris le temps de\n"
	.string "jouer à ce jeu.$"

Yoann_Text_Thanks2::
	.string "Merci de t'être abonné à ma\n"
	.string "chaîne YouTube, de regarder mes\l"
	.string "vidéos et de soutenir mon\l"
	.string "travail.$"

Yoann_Text_Thanks3::
	.string "Tu ne t'en rends peut-être pas\n"
	.string "compte, mais ça représente\l"
	.string "énormément pour moi.$"

Yoann_Text_Thanks4::
	.string "J'ai toujours eu de grandes\n"
	.string "ambitions.$"

Yoann_Text_Thanks5::
	.string "Des rêves qui peuvent parfois\n"
	.string "sembler complètement\l"
	.string "démesurés...$"

Yoann_Text_Thanks6::
	.string "Mais je crois sincèrement qu'un\n"
	.string "jour, je pourrai les réaliser.$"

Yoann_Text_Thanks7::
	.string "Et si ce jour arrive...$"

Yoann_Text_Thanks8::
	.string "J'espère que tu seras encore là\n"
	.string "pour le voir.$"

Yoann_Text_Thanks9::
	.string "Alors, du fond du cœur...$"

Yoann_Text_Thanks10::
	.string "Merci d'avoir fait un bout de\n"
	.string "chemin avec moi.$"

Yoann_Text_Reward::
	.string "Bon ! Assez parlé !\p"
	.string "Tiens, j'ai quelque chose pour\n"
	.string "toi !$"

Yoann_Text_Received::
	.string "Vous recevez le CHARME CHROMA !$"

Yoann_Text_RewardEnd::
	.string "Avec ça, tu devrais avoir un peu\n"
	.string "plus de chance de rencontrer des\l"
	.string "Yo-kai chromatiques !\p"
	.string "Et qui sait ? Peut-être qu'on se\n"
	.string "retrouvera un jour pour une\l"
	.string "nouvelle aventure !$"

Yoann_Text_Again::
	.string "Hé, merci encore pour tout.\p"
	.string "J'espère qu'on vivra plein\n"
	.string "d'autres aventures ensemble !$"

Yoann_Text_BagFull::
	.string "Ton sac est plein. Fais un peu\n"
	.string "de place et reviens me parler :\l"
	.string "je garde ton cadeau pour toi !$"

Yoann_Text_Decline::
	.string "Pas de souci ! Je reste ici.\n"
	.string "Reviens quand tu voudras !$"

Yoann_Text_Defeat::
	.string "Bien joué ! Tu m'as eu !$"

Yoann_Text_BattleStart::
	.string "C'est parti !$"


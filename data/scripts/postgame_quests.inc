
PG_IntroEnma::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_ENMA_INTRO, PG_IntroDone
	special PostgameEnmaArrival
	goto_if_eq VAR_RESULT, FALSE, PG_IntroDone
	waitstate
	goto_if_eq VAR_RESULT, FALSE, PG_IntroDone
	msgbox PG_Text_Enma
	closemessage
	special PostgameEnmaDeparture
	goto_if_eq VAR_RESULT, FALSE, PG_IntroDone
	waitstate
	goto_if_eq VAR_RESULT, FALSE, PG_IntroDone
	setflag FLAG_PG_ENMA_INTRO
	clearflag FLAG_PG_ENMA_INTRO_PENDING
PG_IntroDone::
	setvar VAR_TEMP_3, 0
	releaseall
	end

PG_ChenGift::
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_Return
	goto_if_set FLAG_PG_CHEN_JIBANYAN, EventScript_Return
	msgbox PG_Text_Chen
	setvar VAR_0x8004, 0
	special PostgameGiveGift
	goto_if_eq VAR_RESULT, MON_CANT_GIVE, PG_GiftFullReturn
	copyvar VAR_0x8008, VAR_RESULT
	msgbox PG_Text_JibanyanReceived
	call PG_GiftPCNotice
	return
PG_GiftFullReturn::
	msgbox PG_Text_GiftFull
	return
PG_GiftPCNotice::
	goto_if_ne VAR_0x8008, MON_GIVEN_TO_PC, EventScript_Return
	msgbox PG_Text_GiftPC
	return

PG_NyadaHome::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_NYADA_II_COMPLETE, PG_HomeFinished
	goto_if_set FLAG_PG_NYADA_I_COMPLETE, PG_HomeSecond
	goto_if_set FLAG_PG_NYADA_I_ACTIVE, PG_HomeFriends
	msgbox PG_Text_NyadaI
	setflag FLAG_PG_NYADA_I_ACTIVE
	releaseall
	end
PG_HomeFriends::
	special PostgameHaveFriends
	goto_if_eq VAR_RESULT, FALSE, PG_FriendsMissing
	checkitemspace ITEM_LUCKY_EGG, 1
	goto_if_eq VAR_RESULT, FALSE, PG_RewardBagFull
	msgbox PG_Text_NyadaIThanks
	giveitem ITEM_LUCKY_EGG, 1
	setflag FLAG_PG_NYADA_I_COMPLETE
	clearflag FLAG_PG_NYADA_II_LEAVE_OK
	releaseall
	end
PG_FriendsMissing::
	msgbox PG_Text_FriendsMissing
	releaseall
	end
PG_RewardBagFull::
	msgbox PG_Text_BagFull
	releaseall
	end
PG_HomeSecond::
	goto_if_unset FLAG_ONI_GORGOUILLE_CAUGHT, PG_SecondWaiting
	goto_if_unset FLAG_PG_NYADA_II_LEAVE_OK, PG_SecondWaiting
	msgbox PG_Text_NyadaII
	setflag FLAG_NYADA_QUEST_UNLOCKED
	releaseall
	end
PG_SecondWaiting::
	msgbox PG_Text_SecondWaiting
	releaseall
	end
PG_HomeFinished::
	msgbox PG_Text_HomeFinished
	releaseall
	end

PG_CaveScene::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_unset FLAG_NYADA_QUEST_UNLOCKED, EventScript_ReleaseEnd
	goto_if_unset FLAG_PG_NYADA_I_COMPLETE, EventScript_ReleaseEnd
	goto_if_unset FLAG_ONI_GORGOUILLE_CAUGHT, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_DEMOPHAGE_WON, PG_DemReward
	goto_if_set FLAG_PG_DEM_SCENE, PG_DemChallenge
	msgbox PG_Text_DemBeforeSleep
	delay 60
	msgbox PG_Text_DemWake
	applymovement LOCALID_PG_NYADA_CAVE, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox PG_Text_DemAfterSleep
	setflag FLAG_PG_DEM_SCENE
PG_DemChallenge::
	cleartrainerflag TRAINER_PG_DEMOPHAGE
	trainerbattle_single TRAINER_PG_DEMOPHAGE, PG_Text_DemBattle, PG_Text_DemDefeat, PG_DemVictory
	releaseall
	end
PG_DemVictory::
	lockall
	setflag FLAG_PG_DEMOPHAGE_WON
	msgbox PG_Text_DemVictory
PG_DemReward::
	goto_if_set FLAG_PG_DEMOPHAGE_GIVEN, PG_TicketReward
	setvar VAR_0x8004, 1
	special PostgameGiveGift
	goto_if_eq VAR_RESULT, MON_CANT_GIVE, PG_GiftFull
	copyvar VAR_0x8008, VAR_RESULT
	msgbox PG_Text_DemReceived
	call PG_GiftPCNotice
PG_TicketReward::
	special PostgameGiveTicket
	goto_if_eq VAR_RESULT, FALSE, PG_RewardBagFull
	msgbox PG_Text_TicketReceived
	msgbox PG_Text_Ticket
	setflag FLAG_PG_NYADA_II_COMPLETE
	clearflag FLAG_NYADA_QUEST_UNLOCKED
	setflag FLAG_PG_HIDE_NYADA_CAVE
	setflag FLAG_PG_HIDE_DEMOPHAGE
	removeobject LOCALID_PG_NYADA_CAVE
	removeobject LOCALID_PG_DEMOPHAGE
	releaseall
	end
PG_GiftFull::
	msgbox PG_Text_GiftFull
	releaseall
	end

PG_NyadaRoof::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_unset FLAG_PG_TOWER_CLEAR, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_NYADA_GIVEN, PG_RoofRematch
	goto_if_set FLAG_PG_NYADA_FINAL_WON, PG_NyadaGift
	msgbox PG_Text_NyadaFinal
PG_RoofBattle::
	cleartrainerflag TRAINER_PG_NYADA_FINAL
	trainerbattle_single TRAINER_PG_NYADA_FINAL, PG_Text_NyadaBattle, PG_Text_NyadaDefeat, PG_NyadaVictory
	releaseall
	end
PG_NyadaVictory::
	lockall
	setflag FLAG_PG_NYADA_FINAL_WON
	goto_if_set FLAG_PG_NYADA_GIVEN, PG_RoofAgainEnd
	msgbox PG_Text_NyadaVictory
PG_NyadaGift::
	setvar VAR_0x8004, 2
	special PostgameGiveGift
	goto_if_eq VAR_RESULT, MON_CANT_GIVE, PG_GiftFull
	copyvar VAR_0x8008, VAR_RESULT
	msgbox PG_Text_NyadaReceived
	call PG_GiftPCNotice
	releaseall
	end
PG_RoofRematch::
	msgbox PG_Text_RoofAgain, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, PG_RoofBattle
	releaseall
	end
PG_RoofAgainEnd::
	msgbox PG_Text_RoofAgainEnd
	releaseall
	end

PG_TowerBlocked::
	msgbox PG_Text_TowerBlocked
	warp MAP_SEVEN_ISLAND_TRAINER_TOWER, 58, 8
	waitstate
	releaseall
	end

PG_ScientistLav::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_SCIENTIST_1, EventScript_ReleaseEnd
	msgbox PG_Text_Scientist1
	trainerbattle_single TRAINER_PG_SCIENTIST_1, PG_Text_ScientistBattle, PG_Text_ScientistDefeat, PG_ScientistWin1
	releaseall
	end
PG_ScientistWin1::
	lockall
	msgbox PG_Text_Scientist1After
	setflag FLAG_PG_SCIENTIST_1
	setflag FLAG_PG_HIDE_SCIENTIST_LAV
	setvar VAR_0x8004, LOCALID_PG_SCIENTIST_LAV
	call PG_ScientistWalkAway
	releaseall
	end
PG_ScientistPort::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_unset FLAG_PG_SCIENTIST_1, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_SCIENTIST_2, EventScript_ReleaseEnd
	msgbox PG_Text_Scientist2
	trainerbattle_single TRAINER_PG_SCIENTIST_2, PG_Text_ScientistBattle, PG_Text_ScientistDefeat, PG_ScientistWin2
	releaseall
	end
PG_ScientistWin2::
	lockall
	msgbox PG_Text_Scientist2After
	setflag FLAG_PG_SCIENTIST_2
	call PG_ScientistCut
	setflag FLAG_PG_HIDE_SCIENTIST_PORT
	setvar VAR_0x8004, LOCALID_PG_SCIENTIST_PORT
	call PG_ScientistWalkAway
	releaseall
	end
PG_ScientistYopple::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_unset FLAG_PG_SCIENTIST_2, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_ROBO_GIVEN, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_SCIENTIST_WON, PG_RoboGift
	msgbox PG_Text_Scientist3
	trainerbattle_single TRAINER_PG_SCIENTIST_3, PG_Text_ScientistBattle, PG_Text_ScientistDefeat, PG_ScientistWin3
	releaseall
	end
PG_ScientistWin3::
	lockall
	setflag FLAG_PG_SCIENTIST_WON
	msgbox PG_Text_Scientist3After
PG_RoboGift::
	setvar VAR_0x8004, 3
	special PostgameGiveGift
	goto_if_eq VAR_RESULT, MON_CANT_GIVE, PG_GiftFull
	copyvar VAR_0x8008, VAR_RESULT
	msgbox PG_Text_RoboReceived
	call PG_GiftPCNotice
	msgbox PG_Text_ScientistBye
	setflag FLAG_PG_HIDE_SCIENTIST_YOPPLE
	setvar VAR_0x8004, LOCALID_PG_SCIENTIST_YOPPLE
	call PG_ScientistWalkAway
	releaseall
	end

PG_Kyubi::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_unset FLAG_PG_NYADA_I_ACTIVE, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_KYUBI_CAUGHT, EventScript_ReleaseEnd
	special QuestLog_CutRecording
	setwildbattle SPECIES_PIDGEY, 60
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, PG_KyubiCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, PG_KyubiKO
	releaseall
	end
PG_KyubiCaught::
	setflag FLAG_PG_KYUBI_CAUGHT
	setflag FLAG_FOUGHT_ARTICUNO
PG_KyubiKO::
	setflag FLAG_HIDE_ARTICUNO
	removeobject 3
	releaseall
	end
PG_Octorgone::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd
	goto_if_unset FLAG_PG_NYADA_I_ACTIVE, EventScript_ReleaseEnd
	goto_if_set FLAG_PG_OCTORGONE_CAUGHT, EventScript_ReleaseEnd
	special QuestLog_CutRecording
	setwildbattle SPECIES_BEEDRILL, 60
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, PG_OctorgoneCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, PG_OctorgoneKO
	releaseall
	end
PG_OctorgoneCaught::
	setflag FLAG_PG_OCTORGONE_CAUGHT
	setflag FLAG_FOUGHT_ZAPDOS
PG_OctorgoneKO::
	setflag FLAG_HIDE_ZAPDOS
	removeobject 6
	releaseall
	end

PG_Text_Enma::
    .string "Alors, c'est toi, {PLAYER}! Ton nom\nfait du bruit jusque dans le Yo-kai\lWorld.\pJe suis Enma, son souverain. Mais\naujourd'hui, je viens saluer un\lDresseur.\pTu as arrêté Don Morléone sans\nchercher à posséder les autres.\lJ'aime cette façon de gagner.\pOn me dit que tu veux réunir les\n151 Yo-kai dans ton Médallium.\lQuel beau défi!\pJ'en fais moi-même partie. Tu\npensais que j'allais me laisser de\lcôté?\pRetrouve-moi, puis gagne mon amitié\ndans un vrai combat. Une couronne\ln'empêche pas d'aimer les défis!\pBonne chasse aux rencontres,\n{PLAYER}. Nous nous reverrons!$"

PG_Text_Chen::
	.string "Ah, {PLAYER} !\p"
	.string "Toutes mes félicitations pour\nta victoire à la Ligue !\p"
	.string "Tes aventures ont\nconsidérablement fait\p"
	.string "progresser nos connaissances\nsur les Yo-kai.\p"
	.string "D'ailleurs, j'ai quelque chose\npour toi.\p"
	.string "Ce petit Jibanyan cherche un\nnouveau partenaire.\p"
	.string "Et je ne vois personne de mieux\nplacé que toi pour prendre soin\p"
	.string "de lui !$"

PG_Text_NyadaI::
    .string "Ah, mon élève! Je reconnaîtrais ce\npas entre deux siestes.\pNotre combat à la Ligue m'a montré\nton talent. Aujourd'hui, c'est ton\lamitié que j'aimerais éprouver.\pConnais-tu la guerre contre les\nPerfides? Je l'ai traversée avec\lKyubi et Octorgone.\pDeux grands guerriers. Deux\nsacrées têtes de mule, aussi! Une\ldispute nous a séparés.\pRetrouve-les et gagne leur\nconfiance. Kyubi est aux Îles\lÉcume, Octorgone à la Centrale\lélectrique.\pIls écouteront peut-être un jeune\nDresseur mieux qu'un vieux maître!$"

PG_Text_NyadaIThanks::
	.string "Alors… Tu les as retrouvés ?\p"
	.string "Kyubi et Octorgone… Tous les\ndeux !\p"
	.string "Tu m'impressionnes, {PLAYER}.\p"
	.string "Ces deux-là sont parmi les plus\npuissants Yo-kai que j'aie\p"
	.string "connus.\p"
	.string "Mais leur véritable force ne\nvient pas seulement de leurs\p"
	.string "pouvoirs.\p"
	.string "Elle vient aussi de ce qu'ils\nont traversé.\p"
	.string "Prends bien soin d'eux.\p"
	.string "J'espère qu'un jour, ils\ncomprendront que notre amitié\p"
	.string "vaut davantage qu'une vieille\ndispute.\p"
	.string "Tiens, accepte ceci pour te\nremercier.$"

PG_Text_NyadaII::
	.string "Ah, {PLAYER} ! Comment vas-tu ?\p"
	.string "Cela faisait un moment.\p"
	.string "Figure-toi que j'ai quelqu'un à\nte présenter.\p"
	.string "Un jeune Yo-kai\nparticulièrement prometteur.\p"
	.string "Il possède une force\nincroyable, mais manque encore\p"
	.string "un peu de confiance en lui.\p"
	.string "Je l'entraîne depuis quelque\ntemps.\p"
	.string "Retrouve-moi dans la Grotte\nAzurée.\p"
	.string "Je pense que vous aurez\nbeaucoup à apprendre l'un de\p"
	.string "l'autre.$"

PG_Text_DemBeforeSleep::
    .string "NYADA: Ah, mon élève! Voici\nDémophage, mon apprenti.\pDÉMOPHAGE: E-enchanté! Le Maître\nm'a beaucoup parlé de vous.\pNYADA: Il pourrait dévorer un Oni.\nMais pour devenir un guerrier, il\llui faut...\p...\pDÉMOPHAGE: Maître? Vous avez\nencore les yeux fermés...$"

PG_Text_DemWake::
    .string "DÉMOPHAGE: MAÎTRE,\nREVEILLEZ-VOUS!\pNYADA: Hein? Je méditais! Très\nprofondément.\pOù en étions-nous?$"

PG_Text_DemAfterSleep::
    .string "DÉMOPHAGE: À mon entraînement,\nMaître...\pNYADA: Exact! {PLAYER}, montre-lui\nqu'une grande force doit savoir\lécouter.\pDÉMOPHAGE: Je ferai de mon mieux!\nPromis, je ne vous prendrai pas\lpour mon déjeuner.$"

PG_Text_DemVictory::
    .string "DÉMOPHAGE: Ouah... Le Maître\nn'exagérait pas!\pNYADA: Démophage, la leçon?\pDÉMOPHAGE: Je dois compter sur\nautre chose que ma force. Et\lécouter mes amis!\pNYADA: Bien! Voilà qui mérite une\nsieste... une récompense!\pDÉMOPHAGE: {PLAYER}, je peux\ncontinuer l'entraînement avec vous?\lJe tâcherai de ne pas manger vos\lprovisions.$"

PG_Text_Ticket::
	.string "Avant que tu partes, j'ai une\ndernière chose pour toi.\p"
	.string "Prends ce ticket.\p"
	.string "Il permet d'accéder à la Tour\nDresseurs.\p"
	.string "Les meilleurs combattants de\nKanto s'y affrontent.\p"
	.string "Si tu parviens jusqu'au sommet…\p"
	.string "Nous nous retrouverons pour une\ndernière épreuve.$"

PG_Text_NyadaFinal::
	.string "Te voilà enfin.\p"
	.string "Je dois reconnaître que tu as\ndépassé mes attentes.\p"
	.string "Tu as retrouvé mes anciens\ncompagnons.\p"
	.string "Tu as gagné le respect des Oni.\p"
	.string "Tu as même aidé mon apprenti à\nprogresser.\p"
	.string "Et maintenant, tu as traversé\ncette tour.\p"
	.string "Il est temps de voir ce que tu\nvaux face à moi.\p"
	.string "Prépare-toi, {PLAYER}.$"

PG_Text_NyadaVictory::
	.string "Je vois…\p"
	.string "Tu n'as plus besoin de mes\népreuves.\p"
	.string "À présent, c'est toi qui\npourrais m'apprendre certaines\p"
	.string "choses.\p"
	.string "Tu as mérité bien plus qu'un\nsimple trophée.\p"
	.string "J'aimerais t'accompagner dans\ntes prochaines aventures.$"

PG_Text_Scientist1::
	.string "Ah ! Enfin quelqu'un de normal\ndans cette ville !\p"
	.string "Écoute-moi bien, jeune\nDresseur.\p"
	.string "Tu as devant toi un véritable\ngénie de la robotique !\p"
	.string "Après des années de recherches,\nj'ai conçu un Yo-kai absolument\p"
	.string "révolutionnaire !\p"
	.string "Une merveille de technologie !\p"
	.string "ADMIRE… ROBONYAN !$"

PG_Text_Scientist1After::
	.string "QUOI ?!\p"
	.string "Impossible ! Mes calculs\nétaient parfaits !\p"
	.string "Ça ne peut être qu'un défaut de\nfabrication…\p"
	.string "Peu importe ! Je vais améliorer\nmon invention !\p"
	.string "Et la prochaine fois, tu vas le\nregretter !$"

PG_Text_Scientist2::
	.string "TOI ?!\p"
	.string "Parfait ! Justement, je te\ncherchais !\p"
	.string "J'ai compris pourquoi tu avais\ngagné la dernière fois.\p"
	.string "Mon précédent modèle était\ntechnologiquement dépassé !\p"
	.string "Mais cette fois, j'ai corrigé\nabsolument TOUS ses défauts !\p"
	.string "Plus rapide ! Plus puissant !\nPlus intelligent !\p"
	.string "Voici… ROBONYAN F !$"

PG_Text_Scientist2After::
	.string "NON ! NON ! NON !\p"
	.string "Mais comment c'est possible ?!\p"
	.string "J'ai pourtant dépensé toutes\nmes économies dans cette\p"
	.string "amélioration !\p"
	.string "Très bien. Tu ne me laisses pas\nle choix.\p"
	.string "Je vais concevoir le modèle\nULTIME !\p"
	.string "Notre prochaine rencontre sera\nla dernière !$"

PG_Text_Scientist3::
	.string "…\p"
	.string "Je savais que tu viendrais.\p"
	.string "Cette fois, je ne vais pas\nperdre mon temps avec de grands\p"
	.string "discours.\p"
	.string "J'ai investi jusqu'à mon\ndernier centime dans ce projet.\p"
	.string "Des années de recherches, des\ncentaines de prototypes et des\p"
	.string "milliers d'heures de travail…\p"
	.string "Tout ça pour créer une seule\nchose.\p"
	.string "Le Yo-kai parfait.\p"
	.string "ROBONYAN 28 !$"

PG_Text_Scientist3After::
	.string "…\p"
	.string "…\p"
	.string "J'ABANDONNE !!!\p"
	.string "La robotique, c'est terminé !\p"
	.string "Toutes ces années à construire\ndes machines pour qu'un gamin\p"
	.string "vienne les démolir en cinq\nminutes !\p"
	.string "Franchement, les Yo-kai robots,\nc'est NUL !\p"
	.string "Tu sais quoi ? Je vais rentrer\nchez moi.\p"
	.string "Je vais devenir streamer.\p"
	.string "Au moins, je pourrai jouer aux\njeux vidéo toute la journée !\p"
	.string "Tiens, prends cette ferraille.\nJ'en veux plus !$"

PG_Text_JibanyanReceived::
	.string "Vous obtenez JIBANYAN !$"

PG_Text_DemReceived::
	.string "Vous obtenez DÉMOPHAGE !$"

PG_Text_NyadaReceived::
	.string "Vous obtenez MAÎTRE NYADA !$"

PG_Text_RoboReceived::
	.string "Vous obtenez ROBONYAN 28 shiny\n!$"

PG_Text_FriendsMissing::
	.string "Kyubi se trouve aux Îles Écume.\nOctorgone est à la Centrale\p"
	.string "électrique. Reviens après les\navoir capturés tous les deux.$"

PG_Text_GiftFull::
	.string "Ton équipe et ton PC sont\npleins. Fais une place : ton\p"
	.string "nouvel ami t’attendra ici.$"

PG_Text_GiftPC::
	.string "Ton nouvel ami a été envoyé au\nPC.$"

PG_Text_BagFull::
	.string "Ton SAC est plein. Fais une\nplace, puis reviens me parler.$"

PG_Text_SecondWaiting::
	.string "Prends soin de Kyubi et\nOctorgone. Termine aussi\p"
	.string "l’enquête d’Alizon Bie,\nGorgouille compris. Nous\p"
	.string "reparlerons de ton entraînement\nà ta prochaine visite.$"

PG_Text_HomeFinished::
	.string "La Tour Dresseurs t’attend.\nNous nous retrouverons à son\p"
	.string "sommet.$"

PG_Text_DemBattle::
	.string "Je ferai de mon mieux, Maître !$"

PG_Text_DemDefeat::
	.string "Quelle force ! J’ai encore tant\nà apprendre !$"

PG_Text_NyadaBattle::
	.string "Montre-moi tout ce que tu as\nappris !$"

PG_Text_NyadaDefeat::
	.string "Tu as dépassé mes attentes.$"

PG_Text_RoofAgain::
	.string "Tu veux reprendre notre\nentraînement ?$"

PG_Text_RoofAgainEnd::
	.string "Continue de progresser avec tes\namis.$"

PG_Text_TowerBlocked::
	.string "L’accès à la Tour Dresseurs\nnécessite le Ticket de la Tour.\p"
	.string "Maître Nyada pourra te le\nremettre après l’entraînement\p"
	.string "de son apprenti.$"

PG_Text_ScientistBattle::
	.string "Admire le génie de mon\ninvention !$"

PG_Text_ScientistDefeat::
	.string "Mes calculs étaient parfaits !$"

PG_Text_ScientistBye::
	.string "Et surtout, ne viens pas me\ndemander de le réparer !\p"
	.string "Maintenant, si tu veux bien\nm’excuser, j’ai une carrière\p"
	.string "sur Internet à commencer !$"

PG_Text_TicketReceived::
	.string "Vous obtenez le\nTICKET DE LA TOUR !$"

PG_ScientistWalkAway::
	closemessage
	setvar VAR_0x8005, 0
	special PostgameScientistDeparture
	goto_if_eq VAR_RESULT, FALSE, EventScript_Return
	waitstate
	return

PG_ScientistCut::
	goto_if_set FLAG_TEMP_12, EventScript_Return
	closemessage
	setvar VAR_0x8004, LOCALID_PG_SCIENTIST_PORT
	setvar VAR_0x8005, 1
	special PostgameScientistDeparture
	goto_if_eq VAR_RESULT, FALSE, EventScript_Return
	waitstate
	goto_if_eq VAR_RESULT, FALSE, EventScript_Return
	msgbox PG_Text_ScientistCut
	closemessage
	playse SE_M_CUT
	applymovement 7, Movement_CutTreeDown
	waitmovement 7
	removeobject 7
	return
PG_Text_ScientistCut::
	.string "Un obstacle? Mon prototype connaît\nCoupe. Ouvrons le passage!$"

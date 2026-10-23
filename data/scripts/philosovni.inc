@ Persistent chapter state: 0 invitation, 1 investigation, 2 won/pending HM, 3 complete.
Philosovni_Wyatt_Concern::
	goto_if_set FLAG_PHILOSOVNI_WYATT_DONE, EventScript_Return
	msgbox Philosovni_Text_WyattConcern
	setflag FLAG_PHILOSOVNI_WYATT_DONE
	return

Philosovni_Wyatt_After::
	msgbox Philosovni_Text_WyattAfter
	return

Philosovni_CityAriane::
	lockall
	faceplayer
	goto_if_ge VAR_PHILOSOVNI_STATE, 1, Philosovni_CityDirections
	msgbox Philosovni_Text_Meet
	msgbox Philosovni_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Philosovni_Decline
	setvar VAR_PHILOSOVNI_STATE, 1
Philosovni_CityDirections::
	msgbox Philosovni_Text_Directions
	releaseall
	end
Philosovni_Decline::
	msgbox Philosovni_Text_Decline
	releaseall
	end

Philosovni_Usapion::
	msgbox Philosovni_Text_UsapionHint, MSGBOX_NPC
	end
Philosovni_Grunt::
	msgbox Philosovni_Text_GruntBusy, MSGBOX_NPC
	end

Philosovni_WarehouseAriane::
	lockall
	faceplayer
	goto_if_eq VAR_PHILOSOVNI_STATE, 2, Philosovni_Reward
	goto_if_eq VAR_PHILOSOVNI_STATE, 1, Philosovni_WarehouseHint
	msgbox Philosovni_Text_FirstMeetOutside
	releaseall
	end
Philosovni_WarehouseHint::
	msgbox Philosovni_Text_Quiet
	releaseall
	end

Philosovni_Overhear::
	lockall
	msgbox Philosovni_Text_Quiet
	msgbox Philosovni_Text_GruntA
	msgbox Philosovni_Text_GruntB
	msgbox Philosovni_Text_GruntA2
	msgbox Philosovni_Text_GruntB2
	msgbox Philosovni_Text_OriginA
	msgbox Philosovni_Text_OriginB
	msgbox Philosovni_Text_UsapionOops
	msgbox Philosovni_Text_Shush
	closemessage
	applymovement 2, Common_Movement_FaceDown
	applymovement 3, Common_Movement_FaceDown
	waitmovement 0
	msgbox Philosovni_Text_Discovered
	msgbox Philosovni_Text_DuoReady
	closemessage
	special PhilosovniStartDuo
	waitstate
	goto_if_eq VAR_PHILOSOVNI_STATE, 2, Philosovni_Win
	msgbox Philosovni_Text_Lost
	releaseall
	end

Philosovni_Win::
	msgbox Philosovni_Text_StoneGone
	closemessage
	applymovement 2, Philosovni_RunAway
	applymovement 3, Philosovni_RunAway
	waitmovement 0
	fadescreen FADE_TO_BLACK
	removeobject 2
	removeobject 3
	setflag FLAG_PHILOSOVNI_HIDE_GRUNTS
	fadescreen FADE_FROM_BLACK
	msgbox Philosovni_Text_Conclusion
Philosovni_Reward::
	special PhilosovniRefreshHM
	goto_if_set FLAG_GOT_HM01, Philosovni_AlreadyHM
	msgbox Philosovni_Text_GiveCut
	checkitemspace ITEM_HM01, 1
	goto_if_eq VAR_RESULT, FALSE, Philosovni_BagFull
	giveitem ITEM_HM01, 1
	goto_if_eq VAR_RESULT, FALSE, Philosovni_BagFull
	setflag FLAG_GOT_HM01
	goto Philosovni_Finish
Philosovni_AlreadyHM::
	msgbox Philosovni_Text_AlreadyCut
Philosovni_Finish::
	setvar VAR_PHILOSOVNI_STATE, 3
	special PhilosovniSyncActors
	msgbox Philosovni_Text_GymInvitation
	closemessage
	fadescreen FADE_TO_BLACK
	special PhilosovniEndFollowing
	fadescreen FADE_FROM_BLACK
	releaseall
	end
Philosovni_BagFull::
	msgbox Philosovni_Text_BagFull
	releaseall
	end

Philosovni_RunAway::
	walk_fast_left
	walk_fast_left
	step_end

Philosovni_Text_WyattConcern::
	.string "Hé, toi ! Attends une seconde !\pT'étais là quand Don Morléone\na fait son discours, pas vrai ?\pJe connais peu sa Mafiamille...\nMais ce type ne me plaît pas.\pUn OVNI se serait écrasé\nà Kanto, il y a quelque temps.\pDepuis cet incident, Morléone\na pris une sacrée assurance.\pUne coïncidence ? Peut-être...\nJ'ai un mauvais pressentiment.\pEnfin bref ! Tu veux mon badge ?\nMontre-moi tes Yo-kai !$"
Philosovni_Text_WyattAfter::
	.string "Pas mal du tout !\pAvec tes Yo-kai, tu pourrais\ndonner du fil à retordre\pà cette Mafiamille !$"
Philosovni_Text_Meet::
	.string "ARIANE : Hé ! Toi, là !\pT'as entendu parler de l'OVNI\nqui s'est écrasé ici ?!\pMoi, c'est Ariane Célestin !\nUsapion est mon partenaire !$"
Philosovni_Text_UsapionHello::
	.string "USAPION : Salut, dany !$"
Philosovni_Text_Offer::
	.string "ARIANE : On enquête sur ce crash\ndepuis plusieurs jours !\pOn a suivi des traces de caisses\njusqu'à une cabane sur le quai.\pUne piste incroyable !\nTu veux nous accompagner ?$"
Philosovni_Text_Directions::
	.string "ARIANE : La petite cabane,\nà gauche sur ce quai !\pJe te suis !\nRestons discrets !$"
Philosovni_Text_Decline::
	.string "ARIANE : Pas de souci !\nOn reste ici si tu changes d'avis.$"
Philosovni_Text_UsapionHint::
	.string "USAPION : Une piste, c'est bien.\nDes preuves, c'est mieux, dany !$"
Philosovni_Text_FirstMeetOutside::
	.string "ARIANE : Retrouve-nous dehors.\nOn t'explique notre enquête !$"
Philosovni_Text_Quiet::
	.string "ARIANE : Chut... Des voix !\nAvançons sans faire de bruit.$"
Philosovni_Text_GruntBusy::
	.string "C'est un entrepôt privé !\nCircule !$"
Philosovni_Text_GruntA::
	.string "SBIRE A : Le patron veut vraiment\nenvoyer ce truc à Céladopole ?$"
Philosovni_Text_GruntB::
	.string "SBIRE B : Ferme-la ! Tu sais ce\nque vaut la Pierre Philosovni ?\pOn l'a récupérée après le crash.\nC'est une sacrée prise !$"
Philosovni_Text_GruntA2::
	.string "SBIRE A : Depuis qu'on l'a,\ndes trucs bizarres se passent\ppartout dans Kanto...$"
Philosovni_Text_GruntB2::
	.string "SBIRE B : C'est justement pour ça\nque Don Morléone la veut !$"
Philosovni_Text_OriginA::
	.string "SBIRE A : Mais au fait...\nIl venait d'où, cet OVNI ?$"
Philosovni_Text_OriginB::
	.string "SBIRE B : Aucune idée !\nEt le patron s'en fiche.\pTout ce qui l'intéresse,\nc'est cette fichue pierre !$"
Philosovni_Text_UsapionOops::
	.string "USAPION : La Pierre Philosovni ?!\nMais c'est...$"
Philosovni_Text_Shush::
	.string "ARIANE : CHUUUT !\nIls vont nous entendre !$"
Philosovni_Text_Discovered::
	.string "SBIRE A : Hé ! Qui va là ?!\pSBIRE B : Vous en avez\ntrop entendu !$"
Philosovni_Text_DuoReady::
	.string "ARIANE : On combat ensemble !\nUsapion, à toi de jouer !$"
Philosovni_Text_Lost::
	.string "ARIANE : Repli ! J'ai soigné\ntes Yo-kai. On peut réessayer.\pIls gardent encore l'entrepôt...\nPréparons-nous mieux ! $"
Philosovni_Text_StoneGone::
	.string "SBIRE A : On ne peut pas\nles arrêter ! On file !\pSBIRE B : Trop tard pour vous !\nLa Pierre a déjà quitté Carmin.\pElle est partie pour Céladopole !$"
Philosovni_Text_Conclusion::
	.string "ARIANE : Incroyable ! Cet OVNI\ntransportait quelque chose !\pUSAPION : Et la Mafiamille\na mis la main dessus, dany...\pOn ignore ce que cette pierre\nest capable de faire.\pARIANE : Encore tant de mystères !\nMerci pour ton aide !$"
Philosovni_Text_GiveCut::
	.string "ARIANE : Tiens, pour te remercier !\nC'est la CS Coupe !\pElle te servira pendant\nton aventure !$"
Philosovni_Text_AlreadyCut::
	.string "ARIANE : Tu as déjà la CS Coupe !\nElle te sera bien utile.$"
Philosovni_Text_GymInvitation::
	.string "ARIANE : Si tu veux mon\nBadge Foudre, viens à mon Arène !\pOn y retourne avec Usapion.\nJe t'y attends !$"
Philosovni_Text_BagFull::
	.string "ARIANE : Ton sac est plein !\nFais de la place et reviens.\pJe garde la CS pour toi.$"
Philosovni_Text_CaptainThanks::
	.string "Merci ! Je me sens bien mieux !\pLa Championne Ariane enquête\nprès du port, avec Usapion.\pElle pourra sûrement t'aider\npour la suite de ton voyage.\pProfite encore de l'Océane\navant notre départ !$"

Philosovni_FollowerTalk::
	lockall
	faceplayer
	goto_if_eq VAR_PHILOSOVNI_STATE, 2, Philosovni_Reward
	call Philosovni_ReminderDestination
	releaseall
	end

Philosovni_IdleReminder::
	lockall
	call Philosovni_ReminderDestination
	releaseall
	end

Philosovni_ReminderDestination::
	goto_if_eq VAR_PHILOSOVNI_STATE, 2, Philosovni_ReminderReward
	specialvar VAR_RESULT, PhilosovniFollowerDestination
	goto_if_eq VAR_RESULT, 1, Philosovni_ReminderInside
	goto_if_eq VAR_RESULT, 2, Philosovni_ReminderCity
	msgbox Philosovni_Text_ReminderTravel
	return
Philosovni_ReminderInside::
	msgbox Philosovni_Text_Quiet
	return
Philosovni_ReminderCity::
	msgbox Philosovni_Text_ReminderCity
	return
Philosovni_ReminderReward::
	msgbox Philosovni_Text_ReminderReward
	return
Philosovni_Text_ReminderCity::
	.string "ARIANE : Allons à la cabane\nsur le quai, au sud-est !\pC'est là que mène notre piste !$"
Philosovni_Text_ReminderTravel::
	.string "ARIANE : Direction Carmin !\pNotre piste mène à la cabane\nsur le quai, au sud-est.$"
Philosovni_Text_ReminderReward::
	.string "ARIANE : Fais de la place\ndans ton sac et parle-moi.\pJe garde la CS Coupe pour toi !$"

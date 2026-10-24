.equ GAVE_PROFILE,  VAR_TEMP_1

MysteryEventClub_EventScript_Woman::
	lock
	faceplayer
	goto_if_eq GAVE_PROFILE, TRUE, EventScript_AlreadyGaveProfile
	goto_if_set FLAG_SYS_SET_TRAINER_CARD_PROFILE, EventScript_GivenProfileBefore
	msgbox Text_IdLoveToHearYourProfile
	goto EventScript_AskForProfile
	end

EventScript_AlreadyGaveProfile:
	msgbox Text_TellMoreNextTime
	release
	end

EventScript_AskForProfile:
	message Text_TellMeWhatsYourProfile
	waitmessage
	multichoice 18, 6, MULTICHOICE_YES_NO_INFO_2, FALSE
	switch VAR_RESULT
	case 0, EventScript_AcceptGiveProfile
	case 1, EventScript_DeclineGiveProfile
	case 2, EventScript_ProfileInfo
	case SCR_MENU_CANCEL, EventScript_DeclineGiveProfile
	end

EventScript_ProfileInfo:
	msgbox Text_ExplainProfile
	goto EventScript_AskForProfile
	end

EventScript_AcceptGiveProfile:
	msgbox Text_WhatsYourProfile
	closemessage
	goto EventScript_GiveProfile
	end

EventScript_CancelGiveProfile:
	msgbox Text_DecidedNotTo
	release
	end

EventScript_GaveProfile:
	setvar GAVE_PROFILE, TRUE
	setvar VAR_0x8004, 0
	special ShowEasyChatMessage
	waitmessage
	delay 80
	msgbox Text_ProfileSaysSomethingAboutYou
	release
	end

EventScript_DeclineGiveProfile:
	msgbox Text_DontBeLikeThat
	release
	end

EventScript_GivenProfileBefore:
	msgbox Text_HiWeMeetAgain
	goto EventScript_AskForNewProfile
	end

EventScript_AskForNewProfile:
	message Text_ChangeYourProfile
	waitmessage
	multichoice 18, 6, MULTICHOICE_YES_NO_INFO_2, FALSE
	switch VAR_RESULT
	case 0, EventScript_AcceptGiveNewProfile
	case 1, EventScript_DeclineGiveNewProfile
	case 2, EventScript_ProfileInfo2
	case SCR_MENU_CANCEL, EventScript_DeclineGiveNewProfile
	end

EventScript_ProfileInfo2:
	msgbox Text_ExplainProfile
	goto EventScript_AskForNewProfile
	end

EventScript_AcceptGiveNewProfile:
	msgbox Text_WhatAreYouLikeNow
	closemessage
	goto EventScript_GiveProfile
	end

EventScript_DeclineGiveNewProfile:
	msgbox Text_LikeProfileWayItIs
	release
	end

EventScript_GaveSpecialProfile:
	setvar GAVE_PROFILE, TRUE
	setvar VAR_0x8004, 0
	special ShowEasyChatMessage
	waitmessage
	delay 80
	msgbox Text_HeardThatBefore
	release
	end

EventScript_GiveProfile:
	setvar VAR_0x8004, EASY_CHAT_TYPE_PROFILE
	call Common_ShowEasyChatScreen
	lock
	faceplayer
	goto_if_eq VAR_0x8004, 0, EventScript_GaveSpecialProfile
	goto_if_eq VAR_RESULT, FALSE, EventScript_CancelGiveProfile
	goto_if_eq VAR_RESULT, TRUE, EventScript_GaveProfile
	end

Text_IdLoveToHearYourProfile:
    .string "Salut, ravi de te rencontrer !\p… Ce n'est pas très aimable. Tu\npourrais me dire bonjour.\pAllez, parle-moi de toi.\pJ'aimerais connaître ton profil !$"

Text_TellMeWhatsYourProfile:
    .string "Dis-moi quelque chose sur toi. Quel\nest ton profil ?$"

Text_ExplainProfile:
    .string "Un profil se compose de quatre mots\nou expressions.\pTu disposes d'un grand choix pour\nrédiger le tien.\pLes mots et expressions sont répartis\nen groupes pratiques.\pChoisis d'abord un groupe, puis un\nmot ou une expression.\p… C'est plus simple qu'il n'y paraît.\nTu veux essayer ?$"

Text_WhatsYourProfile:
    .string "Quel est ton profil ?$"

Text_DontBeLikeThat:
    .string "Oh… Ne fais pas ça. Tu peux me\ndonner ton profil.$"

Text_DecidedNotTo:
    .string "Oh, tu renonces ? Tu changes vite\nd'avis !$"

Text_HiWeMeetAgain:
    .string "Salut ! On se retrouve !$"

Text_ChangeYourProfile:
    .string "Veux-tu modifier ton profil ?$"

Text_WhatAreYouLikeNow:
    .string "Comment es-tu, maintenant ? J'aimerais\nvraiment le savoir.$"

Text_LikeProfileWayItIs:
    .string "D'accord, ton profil te plaît comme\nça.\pJe suis du même avis.$"

Text_ProfileSaysSomethingAboutYou:
    .string "Hmm…\pTon profil en dit vraiment long sur\ntoi.\pMaintenant que je te connais mieux,\nnous sommes encore plus proches !$"

Text_HeardThatBefore:
    .string "Oh, j'ai déjà entendu ça…\pMon cousin, qui habite loin, le disait\ntout le temps, je crois.$"

Text_TellMoreNextTime:
    .string "Parle-moi encore de toi la prochaine\nfois !$"

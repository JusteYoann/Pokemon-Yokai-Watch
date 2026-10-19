PewterCity_Gym_Text_BrockIntro::
    .string "Te voilà! Je suis Pierre,\nle Champion de cette Arène.\pMa volonté est aussi solide\nque mes Yo-kai.\pIls ne reculent devant rien\net ne lâchent jamais prise!\pHaha! Tu oses quand même\nme défier? Voilà du courage!\pC'est bien l'honneur\nd'un Dresseur de Yo-kai!\pTrès bien!\nMontre-moi ce que tu sais faire!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$"

@ NOTE: This defeat text actually causes a buffer overflow. It's too long for the gDisplayedStringBattle
@ buffer that it's put into, and it stomps all over the gBattleTextBuffs after, as well as the otherwise
@ unused array after that, sFlickerArray. Perhaps that's the reason why said array exists.
PewterCity_Gym_Text_BrockDefeat::
    .string "Je t'ai sous-estimé…\nEt j'ai perdu.\pTa victoire mérite le Badge Roche,\nreconnu par la Ligue des Yo-kai.\p{FONT_NORMAL}Pierre remet\nle Badge Roche à {PLAYER}!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\p{FONT_MALE}Le Badge Roche renforce\nla puissance de tes Yo-kai.\pIl permet aussi d'utiliser Flash\nen dehors des combats.\pUn de tes Yo-kai doit connaître\ncette capacité pour l'utiliser.$"

PewterCity_Gym_Text_TakeThisWithYou::
    .string "Attends!\nPrends aussi ceci.$"

PewterCity_Gym_Text_ReceivedTM39FromBrock::
    .string "Pierre remet\nla CT39 à {PLAYER}.$"

PewterCity_Gym_Text_ExplainTM39::
    .string "Une CT, ou Capsule Technique,\nenseigne une capacité à un Yo-kai.\pChaque CT ne sert qu'une fois:\nchoisis bien son destinataire.\pLa CT39 contient Tomberoche.\pDes rochers s'abattent sur la cible\net réduisent sa Vitesse.$"

PewterCity_Gym_Text_BrockPostBattle::
    .string "Notre monde compte\ntoutes sortes de Dresseurs.\pTu sembles avoir un vrai talent\npour combattre avec les Yo-kai.\pUn conseil:\nva tester tes capacités\là l'Arène de CERULEAN CITY.$"

PewterCity_Gym_Text_DontHaveRoomForThis::
    .string "Tu n'as pas de place pour ça.$"

PewterCity_Gym_Text_LiamIntro::
    .string "Halte-là!\pTu es à dix mille années-lumière\nde pouvoir affronter Pierre!$"

PewterCity_Gym_Text_LiamDefeat::
    .string "Zut! Les années-lumière\nmesurent une distance…\lPas une durée!$"

PewterCity_Gym_Text_LiamPostBattle::
    .string "Tu es fort…\nMais moins que Pierre!$"

PewterCity_Gym_Text_LetMeTakeYouToTheTop::
    .string "Salut! Tu as de grands rêves?\pDevenir Maître des Yo-kai,\nça te dirait?\pJe ne suis pas Dresseur,\nmais je peux te conseiller.\pEn route vers les sommets!$"

PewterCity_Gym_Text_LetsGetHappening::
    .string "Parfait!\nC'est parti!$"

PewterCity_Gym_Text_TryDifferentPartyOrders::
    .string "Le premier Yo-kai de ta liste\nentre au combat en premier.\pTu peux gagner un avantage\nen modifiant l'ordre de l'équipe.\pAdapte-le aux Yo-kai\nde ton adversaire.$"

PewterCity_Gym_Text_ItsFreeLetsGetHappening::
    .string "Mes conseils sont gratuits!\nC'est parti!$"

PewterCity_Gym_Text_YoureChampMaterial::
    .string "Je le savais!\nTu as l'étoffe d'un Maître Yo-kai!$"

PewterCity_Gym_Text_GymStatue::
    .string "ARÈNE DE PEWTER CITY\nCHAMPION: PIERRE\pDRESSEURS VICTORIEUX:\n{RIVAL}$"

PewterCity_Gym_Text_GymStatuePlayerWon::
    .string "ARÈNE DE PEWTER CITY\nCHAMPION: PIERRE\pDRESSEURS VICTORIEUX:\n{RIVAL}, {PLAYER}$"


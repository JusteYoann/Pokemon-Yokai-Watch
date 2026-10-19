#include "global.h"
#include "link_rfu.h"
#include "mystery_gift_server.h"
#include "mystery_gift_client.h"
#include "constants/union_room.h"

ALIGNED(4) const u8 gText_UR_EmptyString[] = _("");
ALIGNED(4) const u8 gText_UR_Colon[] = _(":");
ALIGNED(4) const u8 gText_UR_ID[] = _("{ID}");
ALIGNED(4) const u8 gText_UR_PleaseStartOver[] = _("Recommence depuis le début.");
ALIGNED(4) const u8 gText_UR_WirelessSearchCanceled[] = _("La recherche de connexion\nsans fil est annulée.");
ALIGNED(4) static const u8 sText_AwaitingCommunucation2[] = _("En attente d'un message\nde tes amis.");
ALIGNED(4) const u8 gText_UR_AwaitingCommunication[] = _("{STR_VAR_1}!\nEn attente d'un autre joueur.");
ALIGNED(4) const u8 gText_UR_AwaitingLinkPressStart[] = _("{STR_VAR_1}! En attente!\nSTART quand tout le monde est prêt.");

ALIGNED(4) static const u8 sText_SingleBattle[] = _("Organiser un Combat Solo");
ALIGNED(4) static const u8 sText_DoubleBattle[] = _("Organiser un Combat Duo");
ALIGNED(4) static const u8 sText_MultiBattle[] = _("Organiser un Combat Multi");
ALIGNED(4) static const u8 sText_TradePokemon[] = _("Organiser un échange de Yo-kai");
ALIGNED(4) static const u8 sText_Chat[] = _("Ouvrir une discussion");
ALIGNED(4) static const u8 sText_DistWonderCard[] = _("Partager une Carte Miracle");
ALIGNED(4) static const u8 sText_DistWonderNews[] = _("Partager une Info Miracle");
ALIGNED(4) static const u8 sText_DistMysteryEvent[] = _("Organiser un Événement Mystère");
ALIGNED(4) static const u8 sText_HoldPokemonJump[] = _("Organiser le Saut Yo-kai");
ALIGNED(4) static const u8 sText_HoldBerryCrush[] = _("Organiser le Broyeur de Baies");
ALIGNED(4) static const u8 sText_HoldBerryPicking[] = _("Organiser la Cueillette de Baies");
ALIGNED(4) static const u8 sText_HoldSpinTrade[] = _("Organiser un échange tournant");
ALIGNED(4) static const u8 sText_HoldSpinShop[] = _("Ouvrir une boutique tournante");

// Unused
static const u8 *const sLinkGroupActionTexts[] = {
    sText_SingleBattle,
    sText_DoubleBattle,
    sText_MultiBattle,
    sText_TradePokemon,
    sText_Chat,
    sText_DistWonderCard,
    sText_DistWonderNews,
    sText_DistWonderCard,
    sText_HoldPokemonJump,
    sText_HoldBerryCrush,
    sText_HoldBerryPicking,
    sText_HoldBerryPicking,
    sText_HoldSpinTrade,
    sText_HoldSpinShop
};

static const u8 sText_1PlayerNeeded[] = _("1 joueur\nrequis.");
static const u8 sText_2PlayersNeeded[] = _("2 joueurs\nrequis.");
static const u8 sText_3PlayersNeeded[] = _("3 joueurs\nrequis.");
static const u8 sText_4PlayersNeeded[] = _("4 joueurs\nrequis.");
static const u8 sText_2PlayerMode[] = _("MODE\n2 JOUEURS");
static const u8 sText_3PlayerMode[] = _("MODE\n3 JOUEURS");
static const u8 sText_4PlayerMode[] = _("MODE\n4 JOUEURS");
static const u8 sText_5PlayerMode[] = _("MODE\n5 JOUEURS");

const u8 *const gTexts_UR_PlayersNeededOrMode[][5] = {
    { // 2 players required
        sText_1PlayerNeeded,
        sText_2PlayerMode
    },
    { // 4 players required
        sText_3PlayersNeeded,
        sText_2PlayersNeeded,
        sText_1PlayerNeeded,
        sText_4PlayerMode
    },
    { // 2-5 players required
        sText_1PlayerNeeded,
        sText_2PlayerMode,
        sText_3PlayerMode,
        sText_4PlayerMode,
        sText_5PlayerMode
    },
    { // 3-5 players required
        sText_2PlayersNeeded,
        sText_1PlayerNeeded,
        sText_3PlayerMode,
        sText_4PlayerMode,
        sText_5PlayerMode
    }
};

ALIGNED(4) const u8 gText_UR_BButtonCancel[] = _("{B_BUTTON}RETOUR");
ALIGNED(4) static const u8 sText_SearchingForParticipants[] = _("Recherche de participants!");
ALIGNED(4) const u8 gText_UR_PlayerContactedYouForXAccept[] = _("{STR_VAR_2} propose:\n{STR_VAR_1}. Accepter?");
ALIGNED(4) const u8 gText_UR_PlayerContactedYouShareX[] = _("{STR_VAR_2} te contacte.\nVeux-tu partager {STR_VAR_1}?");
ALIGNED(4) const u8 gText_UR_PlayerContactedYouAddToMembers[] = _("{STR_VAR_2} te contacte.\nL'ajouter au groupe?");
ALIGNED(4) const u8 gText_UR_AreTheseMembersOK[] = _("{STR_VAR_1}!\nCes participants te conviennent?");
ALIGNED(4) const u8 gText_UR_CancelModeWithTheseMembers[] = _("Annuler le mode {STR_VAR_1}\navec ces participants?");
ALIGNED(4) const u8 gText_UR_AnOKWasSentToPlayer[] = _("Une confirmation est envoyée\nà {STR_VAR_1}.");

ALIGNED(4) static const u8 sText_OtherTrainerUnavailableNow[] = _("L'autre Dresseur ne semble pas\ndisponible pour le moment…\p");
ALIGNED(4) static const u8 sText_CantTransmitTrainerTooFar[] = _("Impossible de communiquer\navec un Dresseur trop éloigné.\p");
ALIGNED(4) static const u8 sText_TrainersNotReadyYet[] = _("Les autres Dresseurs\nne sont pas encore prêts.\p");

const u8 *const gTexts_UR_CantTransmitToTrainer[] = {
    sText_CantTransmitTrainerTooFar,
    sText_TrainersNotReadyYet
};

ALIGNED(4) const u8 gText_UR_ModeWithTheseMembersWillBeCanceled[] = _("Le mode {STR_VAR_1} avec\nces participants sera annulé.{PAUSE 90}");
ALIGNED(4) static const u8 sText_MemberNoLongerAvailable[] = _("Un participant\nn'est plus disponible.\p");

const u8 *const gTexts_UR_PlayerUnavailable[] = {
    sText_OtherTrainerUnavailableNow,
    sText_MemberNoLongerAvailable
};

ALIGNED(4) static const u8 sText_TrainerAppearsUnavailable[] = _("L'autre Dresseur\nsemble indisponible…\p");
ALIGNED(4) const u8 gText_UR_PlayerSentBackOK[] = _("{STR_VAR_1} a confirmé!");
ALIGNED(4) const u8 gText_UR_PlayerOKdRegistration[] = _("{STR_VAR_1} a accepté\nton inscription au groupe.");
ALIGNED(4) static const u8 sText_PlayerRepliedNo[] = _("{STR_VAR_1} a répondu non…\p");
ALIGNED(4) const u8 gText_UR_AwaitingOtherMembers[] = _("{STR_VAR_1}!\nEn attente des autres participants!");
ALIGNED(4) const u8 gText_UR_QuitBeingMember[] = _("Veux-tu quitter le groupe?");
ALIGNED(4) static const u8 sText_StoppedBeingMember[] = _("Tu as quitté le groupe.\p");

const u8 *const gTexts_UR_PlayerDisconnected[] = {
    [RFU_STATUS_OK]                  = NULL,
    [RFU_STATUS_FATAL_ERROR]         = sText_MemberNoLongerAvailable,
    [RFU_STATUS_CONNECTION_ERROR]    = sText_TrainerAppearsUnavailable,
    [RFU_STATUS_CHILD_SEND_COMPLETE] = NULL,
    [RFU_STATUS_NEW_CHILD_DETECTED]  = NULL,
    [RFU_STATUS_JOIN_GROUP_OK]       = NULL,
    [RFU_STATUS_JOIN_GROUP_NO]       = sText_PlayerRepliedNo,
    [RFU_STATUS_WAIT_ACK_JOIN_GROUP] = NULL,
    [RFU_STATUS_LEAVE_GROUP_NOTICE]  = NULL,
    [RFU_STATUS_LEAVE_GROUP]         = sText_StoppedBeingMember
};

ALIGNED(4) const u8 gText_UR_WirelessLinkEstablished[] = _("La connexion sans fil\nest établie.");
ALIGNED(4) const u8 gText_UR_WirelessLinkDropped[] = _("La connexion sans fil\na été interrompue…");
ALIGNED(4) const u8 gText_UR_LinkWithFriendDropped[] = _("La connexion avec ton ami\na été interrompue…");
ALIGNED(4) static const u8 sText_PlayerRepliedNo2[] = _("{STR_VAR_1} a répondu non…");

const u8 *const gTexts_UR_LinkDropped[] = {
    [RFU_STATUS_OK]                  = NULL,
    [RFU_STATUS_FATAL_ERROR]         = gText_UR_LinkWithFriendDropped,
    [RFU_STATUS_CONNECTION_ERROR]    = gText_UR_LinkWithFriendDropped,
    [RFU_STATUS_CHILD_SEND_COMPLETE] = NULL,
    [RFU_STATUS_NEW_CHILD_DETECTED]  = NULL,
    [RFU_STATUS_JOIN_GROUP_OK]       = NULL,
    [RFU_STATUS_JOIN_GROUP_NO]       = sText_PlayerRepliedNo2,
    [RFU_STATUS_WAIT_ACK_JOIN_GROUP] = NULL,
    [RFU_STATUS_LEAVE_GROUP_NOTICE]  = NULL,
    [RFU_STATUS_LEAVE_GROUP]         = NULL
};

ALIGNED(4) static const u8 sText_DoYouWantXMode[] = _("Veux-tu choisir\nle mode {STR_VAR_2}?");
ALIGNED(4) static const u8 sText_DoYouWantXMode2[] = _("Veux-tu choisir\nle mode {STR_VAR_2}?");

// Unused
static const u8 *const sDoYouWantModeTexts[] = {
    sText_DoYouWantXMode,
    sText_DoYouWantXMode2
};

ALIGNED(4) static const u8 sText_CommunicatingPleaseWait[] = _("Communication en cours…\nPatiente un instant."); // Unused
ALIGNED(4) const u8 gText_UR_AwaitingPlayersResponseAboutTrade[] = _("En attente de la réponse\nde {STR_VAR_1} pour l'échange…");

ALIGNED(4) static const u8 sText_Communicating[] = _("Communication{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.\n{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.");
ALIGNED(4) static const u8 sText_CommunicatingWithPlayer[] = _("Connexion avec {STR_VAR_1}{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.\n{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.");
ALIGNED(4) static const u8 sText_PleaseWaitAWhile[] = _("Veuillez patienter{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.\n{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.{PAUSE 15}.");

const u8 *const gTexts_UR_CommunicatingWait[] = {
    sText_Communicating,
    sText_CommunicatingWithPlayer,
    sText_PleaseWaitAWhile
};

ALIGNED(4) static const u8 sText_HiDoSomethingMale[] = _("Salut!\nTu voudrais faire quelque chose?");
ALIGNED(4) static const u8 sText_HiDoSomethingFemale[] = _("Bonjour!\nÇa te dit de faire quelque chose?");
ALIGNED(4) static const u8 sText_HiDoSomethingAgainMale[] = _("{STR_VAR_1}: Salut! Te revoilà!\nQue veux-tu faire cette fois?");
ALIGNED(4) static const u8 sText_HiDoSomethingAgainFemale[] = _("{STR_VAR_1}: Bonjour, {PLAYER}!\nÇa te dit de faire quelque chose?");

const u8 *const gTexts_UR_HiDoSomething[][GENDER_COUNT] = {
    {
        sText_HiDoSomethingMale,
        sText_HiDoSomethingFemale
    }, {
        sText_HiDoSomethingAgainMale,
        sText_HiDoSomethingAgainFemale
    }
};

ALIGNED(4) static const u8 sText_DoSomethingMale[] = _("On fait quelque chose?");
ALIGNED(4) static const u8 sText_DoSomethingFemale[] = _("Ça te dit de faire quelque chose?");
ALIGNED(4) static const u8 sText_DoSomethingAgainMale[] = _("{STR_VAR_1}: Que veux-tu\nfaire maintenant?");
ALIGNED(4) static const u8 sText_DoSomethingAgainFemale[] = _("{STR_VAR_1}: On fait\nautre chose?");

// Unused
static const u8 *const sDoSomethingTexts[][GENDER_COUNT] = {
    {
        sText_DoSomethingMale,
        sText_DoSomethingFemale
    }, {
        sText_DoSomethingAgainMale,
        sText_DoSomethingAgainMale // was probably supposed to be sText_DoSomethingAgainFemale
    }
};

ALIGNED(4) static const u8 sText_SomebodyHasContactedYou[] = _("Quelqu'un te contacte.{PAUSE 60}");
ALIGNED(4) static const u8 sText_PlayerHasContactedYou[] = _("{STR_VAR_1} te contacte.{PAUSE 60}");

const u8 *const gTexts_UR_PlayerContactedYou[] = {
    sText_SomebodyHasContactedYou,
    sText_PlayerHasContactedYou
};

ALIGNED(4) static const u8 sText_AwaitingResponseFromTrainer[] = _("En attente de la réponse\nde l'autre Dresseur…");
ALIGNED(4) static const u8 sText_AwaitingResponseFromPlayer[] = _("En attente de la réponse\nde {STR_VAR_1}…");

const u8 *const gTexts_UR_AwaitingResponse[] = {
    sText_AwaitingResponseFromTrainer,
    sText_AwaitingResponseFromPlayer
};

ALIGNED(4) static const u8 sText_AwaitingResponseCancelBButton[] = _("En attente d'une proposition.\nBouton B: Annuler");

ALIGNED(4) const u8 gText_UR_ShowTrainerCard[] = _("L'autre Dresseur t'a montré\nsa Carte Dresseur.\pVeux-tu lui montrer la tienne?");
ALIGNED(4) const u8 gText_UR_BattleChallenge[] = _("L'autre Dresseur\nte propose un combat.\pVeux-tu relever ce défi?");
ALIGNED(4) const u8 gText_UR_ChatInvitation[] = _("L'autre Dresseur\nt'invite à discuter.\pVeux-tu accepter l'invitation?");
ALIGNED(4) const u8 gText_UR_OfferToTradeMon[] = _("Ton Yo-kai inscrit:\n{DYNAMIC 1}, Niv.{DYNAMIC 0},\pcontre ce Yo-kai:\n{DYNAMIC 3}, Niv.{DYNAMIC 2}.\pAcceptes-tu cette offre?");
ALIGNED(4) const u8 gText_UR_OfferToTradeEgg[] = _("On te propose un échange\npour ton Œuf inscrit.\pAcceptes-tu cette offre?");
ALIGNED(4) const u8 gText_UR_ChatDropped[] = _("La discussion est interrompue.\p");
ALIGNED(4) const u8 gText_UR_OfferDeclined1[] = _("Tu as refusé l'offre.\p");
ALIGNED(4) const u8 gText_UR_OfferDeclined2[] = _("Tu as refusé l'offre.\p");
ALIGNED(4) const u8 gText_UR_ChatEnded[] = _("La discussion est terminée.\p");

// Unused
static const u8 *const sInvitationTexts[] = {
    gText_UR_ShowTrainerCard,
    gText_UR_BattleChallenge,
    gText_UR_ChatInvitation,
    gText_UR_OfferToTradeMon
};

ALIGNED(4) static const u8 sText_JoinChatMale[] = _("Salut! Nous discutons.\nTu veux nous rejoindre?");
ALIGNED(4) static const u8 sText_PlayerJoinChatMale[] = _("{STR_VAR_1}: Salut, {PLAYER}!\nNous discutons.\lTu veux nous rejoindre?");
ALIGNED(4) static const u8 sText_JoinChatFemale[] = _("Oh, bonjour! Nous discutons.\nTu voudrais nous rejoindre?");
ALIGNED(4) static const u8 sText_PlayerJoinChatFemale[] = _("{STR_VAR_1}: Bonjour, {PLAYER}!\nNous discutons.\lTu voudrais nous rejoindre?");

const u8 *const gTexts_UR_JoinChat[][GENDER_COUNT] = {
    {
        sText_JoinChatMale,
        sText_JoinChatFemale
    }, {
        sText_PlayerJoinChatMale,
        sText_PlayerJoinChatFemale
    }
};

ALIGNED(4) const u8 gText_UR_TrainerAppearsBusy[] = _("……\nCe Dresseur semble occupé…\p");
ALIGNED(4) static const u8 sText_WaitForBattleMale[] = _("Un combat? D'accord!\nLaisse-moi un peu de temps.");
ALIGNED(4) static const u8 sText_WaitForChatMale[] = _("Tu veux discuter?\nBien sûr, attends un instant.");
ALIGNED(4) static const u8 sText_ShowTrainerCardMale[] = _("Bien sûr! Pour me présenter,\nvoici ma Carte Dresseur.");
ALIGNED(4) static const u8 sText_WaitForBattleFemale[] = _("Un combat? Bien sûr,\nmais je dois me préparer.");
ALIGNED(4) static const u8 sText_WaitForChatFemale[] = _("Tu veux discuter?\nD'accord, patiente un instant.");
ALIGNED(4) static const u8 sText_ShowTrainerCardFemale[] = _("Pour me présenter,\nje vais te montrer ma Carte Dresseur.");

const u8 *const gTexts_UR_WaitOrShowCard[GENDER_COUNT][4] = {
    {
        sText_WaitForBattleMale,
        sText_WaitForChatMale,
        NULL,
        sText_ShowTrainerCardMale
    }, {
        sText_WaitForBattleFemale,
        sText_WaitForChatFemale,
        NULL,
        sText_ShowTrainerCardFemale
    }
};

ALIGNED(4) static const u8 sText_WaitForChatMale2[] = _("Tu veux discuter?\nD'accord, attends un instant!");
ALIGNED(4) static const u8 sText_DoneWaitingBattleMale[] = _("Merci d'avoir attendu!\nQue le combat commence!{PAUSE 60}");
ALIGNED(4) static const u8 sText_DoneWaitingChatMale[] = _("Très bien!\nDiscutons!{PAUSE 60}");
ALIGNED(4) static const u8 sText_DoneWaitingBattleFemale[] = _("Merci pour ta patience!\nCommençons!{PAUSE 60}");
ALIGNED(4) static const u8 sText_DoneWaitingChatFemale[] = _("Merci pour ta patience!\nDiscutons.{PAUSE 60}");
ALIGNED(4) static const u8 sText_TradeWillBeStarted[] = _("L'échange va commencer.{PAUSE 60}");
ALIGNED(4) static const u8 sText_BattleWillBeStarted[] = _("Le combat va commencer.{PAUSE 60}");
ALIGNED(4) static const u8 sText_EnteringChat[] = _("Ouverture de la discussion…{PAUSE 60}");

const u8 *const gTexts_UR_StartActivity[][GENDER_COUNT][3] = {
    {
        {
            sText_BattleWillBeStarted,
            sText_EnteringChat,
            sText_TradeWillBeStarted
        }, {
            sText_BattleWillBeStarted,
            sText_EnteringChat,
            sText_TradeWillBeStarted
        }
    }, {
        {
            sText_DoneWaitingBattleMale,
            sText_DoneWaitingChatMale,
            sText_TradeWillBeStarted
        }, {
            sText_DoneWaitingBattleFemale,
            sText_DoneWaitingChatFemale,
            sText_TradeWillBeStarted
        }
    }
};

ALIGNED(4) static const u8 sText_BattleDeclinedMale[] = _("Désolé! Mes Yo-kai\nne semblent pas en forme.\pAffrontons-nous une autre fois.\p");
ALIGNED(4) static const u8 sText_BattleDeclinedFemale[] = _("Désolée, mes Yo-kai\nne se sentent pas très bien…\pNous combattrons une autre fois.\p");

const u8 *const gTexts_UR_BattleDeclined[GENDER_COUNT] = {
    sText_BattleDeclinedMale,
    sText_BattleDeclinedFemale
};

ALIGNED(4) static const u8 sText_ShowTrainerCardDeclinedMale[] = _("Hein? Ma Carte Dresseur…\nOù est-elle passée?\lDésolé! Je te la montrerai plus tard!\p");
ALIGNED(4) static const u8 sText_ShowTrainerCardDeclinedFemale[] = _("Oh? Où ai-je mis\nma Carte Dresseur?\lDésolée! Je te la montrerai plus tard.\p");

const u8 *const gTexts_UR_ShowTrainerCardDeclined[GENDER_COUNT] = {
    sText_ShowTrainerCardDeclinedMale,
    sText_ShowTrainerCardDeclinedFemale
};

ALIGNED(4) static const u8 sText_IfYouWantToDoSomethingMale[] = _("Si tu veux faire quelque chose,\nviens me voir!\p");
ALIGNED(4) static const u8 sText_IfYouWantToDoSomethingFemale[] = _("Si tu veux faire quelque chose,\nn'hésite pas à venir me voir.\p");

const u8 *const gTexts_UR_IfYouWantToDoSomething[GENDER_COUNT] = {
    sText_IfYouWantToDoSomethingMale,
    sText_IfYouWantToDoSomethingFemale
};

ALIGNED(4) const u8 gText_UR_TrainerBattleBusy[] = _("Oups! Désolé,\nje dois faire autre chose.\lUne autre fois, d'accord?\p");
ALIGNED(4) const u8 gText_UR_NeedTwoMonsOfLevel30OrLower1[] = _("Pour combattre, il te faut\ndeux Yo-kai de niveau 30 maximum.\p");
ALIGNED(4) const u8 gText_UR_NeedTwoMonsOfLevel30OrLower2[] = _("Pour ce combat, il faut deux Yo-kai\nde niveau 30 maximum.\p");

ALIGNED(4) static const u8 sText_DeclineChatMale[] = _("D'accord.\nReviens quand tu veux, d'accord?\p");
ALIGNED(4) static const u8 stext_DeclineChatFemale[] = _("Oh…\nReviens me voir quand tu veux.\p");

// Response from partner when player declines chat
const u8 *const gTexts_UR_DeclineChat[GENDER_COUNT] = {
    sText_DeclineChatMale,
    stext_DeclineChatFemale
};

ALIGNED(4) static const u8 sText_ChatDeclinedMale[] = _("Oh, désolé!\nJe ne peux pas tout de suite.\lDiscutons une autre fois.\p");
ALIGNED(4) static const u8 sText_ChatDeclinedFemale[] = _("Oh, désolée.\nJ'ai trop à faire pour le moment.\lDiscutons une autre fois.\p");

// Response from partner when they decline chat
const u8 *const gTexts_UR_ChatDeclined[GENDER_COUNT] = {
    sText_ChatDeclinedMale,
    sText_ChatDeclinedFemale
};

ALIGNED(4) static const u8 sText_YoureToughMale[] = _("Ouah!\nTu as l'air vraiment fort!\p");
ALIGNED(4) static const u8 sText_UsedGoodMoveMale[] = _("Cette capacité?\nQuelle bonne stratégie!\p");
ALIGNED(4) static const u8 sText_BattleSurpriseMale[] = _("Bien joué!\nJ'en ai pris plein les yeux!\p");
ALIGNED(4) static const u8 sText_SwitchedMonsMale[] = _("Oh! Comment as-tu pu choisir\nce Yo-kai dans cette situation?\p");
ALIGNED(4) static const u8 sText_YoureToughFemale[] = _("Ce Yo-kai…\nIl est vraiment bien entraîné!\p");
ALIGNED(4) static const u8 sText_UsedGoodMoveFemale[] = _("Voilà!\nC'est la bonne capacité à utiliser!\p");
ALIGNED(4) static const u8 sText_BattleSurpriseFemale[] = _("Impressionnant!\nOn peut combattre comme ça?\p");
ALIGNED(4) static const u8 sText_SwitchedMonsFemale[] = _("Tu choisis le bon moment\npour changer de Yo-kai!\p");

const u8 *const gTexts_UR_BattleReaction[GENDER_COUNT][4] = {
    {
        sText_YoureToughMale,
        sText_UsedGoodMoveMale,
        sText_BattleSurpriseMale,
        sText_SwitchedMonsMale
    }, {
        sText_YoureToughFemale,
        sText_UsedGoodMoveFemale,
        sText_BattleSurpriseFemale,
        sText_SwitchedMonsFemale
    }
};

ALIGNED(4) static const u8 sText_LearnedSomethingMale[] = _("Ah, je vois!\nJ'apprends des choses!\p");
ALIGNED(4) static const u8 sText_ThatsFunnyMale[] = _("Arrête de dire des choses drôles!\nJ'ai mal au ventre de rire!\p");
ALIGNED(4) static const u8 sText_RandomChatMale1[] = _("Oh?\nUne telle chose est arrivée?\p");
ALIGNED(4) static const u8 sText_RandomChatMale2[] = _("Hmm… Quoi?\nC'est donc ce que tu veux dire?\p");
ALIGNED(4) static const u8 sText_LearnedSomethingFemale[] = _("Vraiment?\nJe ne le savais pas.\p");
ALIGNED(4) static const u8 sText_ThatsFunnyFemale[] = _("Hahaha!\nDe quoi s'agit-il?\p");
ALIGNED(4) static const u8 sText_RandomChatFemale1[] = _("Oui, exactement!\nC'est ce que je voulais dire.\p");
ALIGNED(4) static const u8 sText_RandomChatFemale2[] = _("Autrement dit…\nOui! C'est ça!\p");

const u8 *const gTexts_UR_ChatReaction[GENDER_COUNT][4] = {
    {
        sText_LearnedSomethingMale,
        sText_ThatsFunnyMale,
        sText_RandomChatMale1,
        sText_RandomChatMale2
    }, {
        sText_LearnedSomethingFemale,
        sText_ThatsFunnyFemale,
        sText_RandomChatFemale1,
        sText_RandomChatFemale2
    }
};

ALIGNED(4) static const u8 sText_ShowedTrainerCardMale1[] = _("Je montre simplement\nma Carte Dresseur pour me présenter.\p");
ALIGNED(4) static const u8 sText_ShowedTrainerCardMale2[] = _("J'espère mieux te connaître!\p");
ALIGNED(4) static const u8 sText_ShowedTrainerCardFemale1[] = _("Nous nous montrons nos Cartes\npour faire connaissance.\p");
ALIGNED(4) static const u8 sText_ShowedTrainerCardFemale2[] = _("Ravie de te rencontrer.\nReviens me voir!\p");

const u8 *const gTexts_UR_TrainerCardReaction[GENDER_COUNT][2] = {
    {
        sText_ShowedTrainerCardMale1,
        sText_ShowedTrainerCardMale2
    }, {
        sText_ShowedTrainerCardFemale1,
        sText_ShowedTrainerCardFemale2
    }
};

ALIGNED(4) static const u8 sText_MaleTraded1[] = _("Youpi!\nJe voulais vraiment ce Yo-kai!\p");
ALIGNED(4) static const u8 sText_MaleTraded2[] = _("Un échange m'a enfin donné\nle Yo-kai que j'attendais!\p");
ALIGNED(4) static const u8 sText_FemaleTraded1[] = _("Je fais un échange de Yo-kai.\p");
ALIGNED(4) static const u8 sText_FemaleTraded2[] = _("J'ai enfin obtenu le Yo-kai\nque je voulais grâce à un échange!\p");

const u8 *const gTexts_UR_TradeReaction[GENDER_COUNT][4] = {
    {
        sText_MaleTraded1,
        sText_MaleTraded2
    }, {
        sText_FemaleTraded1,
        sText_FemaleTraded2
    }
};

const u8 gText_UR_XCheckedTradingBoard[] = _("{STR_VAR_1} consulte\nle Tableau d'Échange.\p");
ALIGNED(4) const u8 gText_UR_RegisterMonAtTradingBoard[] = _("Bienvenue au Tableau d'Échange.\pTu peux inscrire un Yo-kai\npour le proposer à l'échange.\pVeux-tu inscrire\nun de tes Yo-kai?");
ALIGNED(4) const u8 gText_UR_TradingBoardInfo[] = _("Ce tableau sert à proposer\ndes Yo-kai à l'échange.\pIl suffit d'inscrire un Yo-kai.\pUn autre Dresseur peut proposer\nun partenaire de son équipe\len échange du tien.\pNous espérons te voir échanger\navec de nombreux Dresseurs!\pVeux-tu inscrire un de tes Yo-kai?");
ALIGNED(4) static const u8 sText_ThankYouForRegistering[] = _("Ton inscription au Tableau\nd'Échange est terminée.\pMerci de ta visite!\p");
ALIGNED(4) static const u8 sText_NobodyHasRegistered[] = _("Personne n'a inscrit de Yo-kai\nau Tableau d'Échange.\p\n");
ALIGNED(4) const u8 gText_UR_ChooseRequestedMonType[] = _("Choisis le type de Yo-kai\nque tu recherches pour l'échange.\n");
ALIGNED(4) const u8 gText_UR_WhichMonWillYouOffer[] = _("Quel Yo-kai de ton équipe\nveux-tu proposer à l'échange?\p");
ALIGNED(4) const u8 gText_UR_RegistrationCanceled[] = _("L'inscription est annulée.\p");
ALIGNED(4) const u8 gText_UR_RegistraionCompleted[] = _("L'inscription est terminée.\p");
ALIGNED(4) const u8 gText_UR_TradeCanceled[] = _("L'échange est annulé.\p");
ALIGNED(4) const u8 gText_UR_CancelRegistrationOfMon[] = _("Annuler l’inscription de\n{STR_VAR_1}, Niv.{STR_VAR_2}?");
ALIGNED(4) const u8 gText_UR_CancelRegistrationOfEgg[] = _("Annuler l'inscription\nde ton Œuf?");
ALIGNED(4) const u8 gText_UR_RegistrationCanceled2[] = _("L'inscription est annulée.\p");
ALIGNED(4) static const u8 sText_TradeTrainersWillBeListed[] = _("Liste des Dresseurs\nsouhaitant un échange.");
ALIGNED(4) static const u8 sText_ChooseTrainerToTradeWith2[] = _("Choisis le Dresseur\navec qui échanger.");
ALIGNED(4) const u8 gText_UR_AskTrainerToMakeTrade[] = _("Veux-tu proposer un échange\nà {STR_VAR_1}?");
ALIGNED(4) static const u8 sText_AwaitingResponseFromTrainer2[] = _("……\nEn attente de la réponse.");
ALIGNED(4) static const u8 sText_NotRegisteredAMonForTrade[] = _("Tu n'as inscrit aucun Yo-kai\npour l'échange.\p");
ALIGNED(4) const u8 gText_UR_DontHaveTypeTrainerWants[] = _("Tu n'as pas de Yo-kai {STR_VAR_2}\nque recherche {STR_VAR_1}.\p");
ALIGNED(4) const u8 gText_UR_DontHaveEggTrainerWants[] = _("Tu n'as pas l'Œuf\nque recherche {STR_VAR_1}.\p");

ALIGNED(4) static const u8 sText_PlayerCantTradeForYourMon[] = _("{STR_VAR_1} ne peut pas\nfaire cet échange pour le moment.\p");
ALIGNED(4) static const u8 sText_CantTradeForPartnersMon[] = _("Impossible d’échanger maintenant\nle Yo-kai de {STR_VAR_1}.\p");

// Unused
static const u8 *const sCantTradeMonTexts[] = {
    sText_PlayerCantTradeForYourMon,
    sText_CantTradeForPartnersMon
};

ALIGNED(4) const u8 gText_UR_TradeOfferRejected[] = _("Ton offre d'échange a été refusée.\p");
ALIGNED(4) const u8 gText_UR_EggTrade[] = _("ÉCHANGE D'ŒUF");
ALIGNED(4) const u8 gText_UR_ChooseJoinCancel[] = _("{DPAD_UPDOWN}CHOIX {A_BUTTON}JOINDRE {B_BUTTON}RETOUR");
ALIGNED(4) const u8 gText_UR_ChooseTrainer[] = _("Choisis un Dresseur.");
ALIGNED(4) static const u8 sText_ChooseTrainerSingleBattle[] = _("Choisis un Dresseur\npour un Combat Solo.");
ALIGNED(4) static const u8 sText_ChooseTrainerDoubleBattle[] = _("Choisis un Dresseur\npour un Combat Duo.");
ALIGNED(4) static const u8 sText_ChooseLeaderMultiBattle[] = _("Choisis le chef du groupe\npour un Combat Multi.");
ALIGNED(4) static const u8 sText_ChooseTrainerToTradeWith[] = _("Choisis le Dresseur\navec qui échanger.");
ALIGNED(4) static const u8 sText_ChooseTrainerToShareWonderCards[] = _("Choisis le Dresseur\nqui partage des Cartes Miracle.");
ALIGNED(4) static const u8 sText_ChooseTrainerToShareWonderNews[] = _("Choisis le Dresseur\nqui partage des Infos Miracle.");
ALIGNED(4) static const u8 sText_ChooseLeaderPokemonJump[] = _("Saute avec de petits Yo-kai!\nChoisis le chef du groupe.");
ALIGNED(4) static const u8 sText_ChooseLeaderBerryCrush[] = _("Broyeur de Baies!\nChoisis le chef du groupe.");
ALIGNED(4) static const u8 sText_ChooseLeaderBerryPicking[] = _("Cueillette de Baies!\nChoisis le chef du groupe.");

const u8 *const gTexts_UR_ChooseTrainer[] = {
    [LINK_GROUP_SINGLE_BATTLE] = sText_ChooseTrainerSingleBattle,
    [LINK_GROUP_DOUBLE_BATTLE] = sText_ChooseTrainerDoubleBattle,
    [LINK_GROUP_MULTI_BATTLE]  = sText_ChooseLeaderMultiBattle,
    [LINK_GROUP_TRADE]         = sText_ChooseTrainerToTradeWith,
    [LINK_GROUP_POKEMON_JUMP]  = sText_ChooseLeaderPokemonJump,
    [LINK_GROUP_BERRY_CRUSH]   = sText_ChooseLeaderBerryCrush,
    [LINK_GROUP_BERRY_PICKING] = sText_ChooseLeaderBerryPicking,
    [LINK_GROUP_WONDER_CARD]   = sText_ChooseTrainerToShareWonderCards,
    [LINK_GROUP_WONDER_NEWS]   = sText_ChooseTrainerToShareWonderNews
};

ALIGNED(4) const u8 gText_UR_SearchingForWirelessSystemWait[] = _("Recherche d'une connexion\nsans fil. Patiente…");
ALIGNED(4) static const u8 sText_MustHaveTwoMonsForDoubleBattle[] = _("Il faut au moins deux Yo-kai\npour un Combat Duo.\p");
ALIGNED(4) const u8 gText_UR_AwaitingPlayersResponse[] = _("En attente de la réponse\nde {STR_VAR_1}…");
ALIGNED(4) const u8 gText_UR_PlayerHasBeenAskedToRegisterYouPleaseWait[] = _("{STR_VAR_1} a reçu\nta demande d'inscription. Patiente.");
ALIGNED(4) const u8 gText_UR_AwaitingResponseFromWirelessSystem[] = _("En attente d'une réponse\ndu système de connexion sans fil.");
ALIGNED(4) static const u8 sText_PleaseWaitForOtherTrainersToGather[] = _("Patiente jusqu'à ce que\nles autres participants soient prêts.");

ALIGNED(4) static const u8 sText_NoCardsSharedRightNow[] = _("Aucune Carte ne semble\npartagée pour le moment.");
ALIGNED(4) static const u8 sText_NoNewsSharedRightNow[] = _("Aucune Info ne semble\npartagée pour le moment.");

const u8 *const gTexts_UR_NoWonderShared[] = {
    sText_NoCardsSharedRightNow,
    sText_NoNewsSharedRightNow
};

ALIGNED(4) const u8 gText_UR_Battle[] = _("COMBAT");
ALIGNED(4) const u8 gText_UR_Chat2[] = _("DISCUSSION");
ALIGNED(4) const u8 gText_UR_Greetings[] = _("SALUTATIONS");
ALIGNED(4) const u8 gText_UR_Exit[] = _("QUITTER");

ALIGNED(4) const u8 gText_UR_Exit2[] = _("QUITTER");
ALIGNED(4) const u8 gText_UR_Info[] = _("INFO");
ALIGNED(4) const u8 gText_UR_NameWantedOfferLv[] = _("NOM{CLEAR_TO 0x3C}RECH.{CLEAR_TO 0x6E}OFFRE{CLEAR_TO 0xC6}NIV.");

ALIGNED(4) const u8 gText_UR_SingleBattle[] = _("COMBAT SOLO");
ALIGNED(4) const u8 gText_UR_DoubleBattle[] = _("COMBAT DUO");
ALIGNED(4) const u8 gText_UR_MultiBattle[] = _("COMBAT MULTI");
ALIGNED(4) const u8 gText_UR_PokemonTrades[] = _("ÉCHANGES YO-KAI");
ALIGNED(4) const u8 gText_UR_Chat[] = _("DISCUSSION");
ALIGNED(4) const u8 gText_UR_Cards[] = _("CARTES");
ALIGNED(4) const u8 gText_UR_WonderCards[] = _("CARTES MIRACLE");
ALIGNED(4) const u8 gText_UR_WonderNews[] = _("INFOS MIRACLE");
ALIGNED(4) const u8 gText_UR_PokemonJump[] = _("SAUT YO-KAI");
ALIGNED(4) const u8 gText_UR_BerryCrush[] = _("BROYEUR DE BAIES");
ALIGNED(4) const u8 gText_UR_BerryPicking[] = _("CUEILLETTE");
ALIGNED(4) const u8 gText_UR_Search[] = _("RECHERCHE");
ALIGNED(4) const u8 gText_UR_SpinTrade[] = _("ÉCHANGE TOURNANT");
ALIGNED(4) const u8 gText_UR_ItemTrade[] = _("ÉCHANGE D'OBJETS");

ALIGNED(4) static const u8 sText_ItsNormalCard[] = _("C'est une Carte normale.");
ALIGNED(4) static const u8 sText_ItsBronzeCard[] = _("C'est une Carte de bronze!");
ALIGNED(4) static const u8 sText_ItsCopperCard[] = _("C'est une Carte de cuivre!");
ALIGNED(4) static const u8 sText_ItsSilverCard[] = _("C'est une Carte d'argent!");
ALIGNED(4) static const u8 sText_ItsGoldCard[] = _("C'est une Carte d'or!");

const u8 *const gTexts_UR_CardColor[] = {
    sText_ItsNormalCard,
    sText_ItsBronzeCard,
    sText_ItsCopperCard,
    sText_ItsSilverCard,
    sText_ItsGoldCard
};

ALIGNED(4) const u8 gText_UR_TrainerCardInfoPage1[] = _("Carte Dresseur de\n{DYNAMIC 0} {DYNAMIC 1}…\l{DYNAMIC 2}\pMédallium: {DYNAMIC 3}\nDurée: {DYNAMIC 4}:{DYNAMIC 5}\p");
ALIGNED(4) const u8 gText_UR_TrainerCardInfoPage2[] = _("Combats: {DYNAMIC 0} gagnés, {DYNAMIC 2} perdus\nÉchanges: {DYNAMIC 3}\p{DYNAMIC 4} {DYNAMIC 5}\n{DYNAMIC 6} {DYNAMIC 7}\p");
ALIGNED(4) static const u8 sText_GladToMeetYouMale[] = _("{DYNAMIC 1}: Ravi de te voir!{PAUSE 60}");
ALIGNED(4) static const u8 sText_GladToMeetYouFemale[] = _("{DYNAMIC 1}: Ravie de te voir!{PAUSE 60}");

const u8 *const gTexts_UR_GladToMeetYou[GENDER_COUNT] = {
    sText_GladToMeetYouMale,
    sText_GladToMeetYouFemale
};

ALIGNED(4) const u8 gText_UR_FinishedCheckingPlayersTrainerCard[] = _("Lecture terminée de la Carte\nde {DYNAMIC 1}.{PAUSE 60}");
ALIGNED(4) static const u8 sText_CanceledReadingCard[] = _("Lecture de la Carte annulée.");

static const struct MysteryGiftClientCmd sClientScript_DynamicError[] = {
    {CLI_RECV, MG_LINKID_DYNAMIC_MSG},
    {CLI_COPY_MSG},
    {CLI_SEND_READY_END},
    {CLI_RETURN, CLI_MSG_BUFFER_FAILURE}
};

const struct MysteryGiftServerCmd gServerScript_ClientCanceledCard[] = {
    {SVR_LOAD_CLIENT_SCRIPT, PTR_ARG(sClientScript_DynamicError)},
    {SVR_SEND},
    {SVR_LOAD_MSG, PTR_ARG(sText_CanceledReadingCard)},
    {SVR_SEND},
    {SVR_RECV, MG_LINKID_READY_END},
    {SVR_RETURN, SVR_MSG_CLIENT_CANCELED}
};

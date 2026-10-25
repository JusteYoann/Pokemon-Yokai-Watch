@ One shared sequence for the normal first conquest and explicit QA entry.
PokemonLeague_Spiraton_HideDiagnosticActors::
	setflag FLAG_TEMP_6
	setflag FLAG_TEMP_7
	goto_if_set FLAG_SYS_GAME_CLEAR, PokemonLeague_Spiraton_ShowMattChampion
	clearflag FLAG_TEMP_6
	end

PokemonLeague_Spiraton_ShowMattChampion::
	clearflag FLAG_TEMP_7
	end

PokemonLeague_Spiraton_FirstConquest::
	lockall
	setvar VAR_TEMP_1, 1
	applymovement LOCALID_PLAYER, Spiraton_PlayerEnter
	waitmovement 0
	delay 20
	goto PokemonLeague_Spiraton_DevelopmentEntry

Spiraton_PlayerEnter::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

PokemonLeague_Spiraton_DevelopmentEntry::
	lockall
	setvar VAR_TEMP_1, 1
	textcolor NPC_TEXT_COLOR_MALE
	removeobject LOCALID_CHAMPIONS_ROOM_RIVAL
	setobjectxyperm LOCALID_CHAMPIONS_ROOM_RIVAL, 6, 16
	addobject LOCALID_SPIRATON_DON
	addobject LOCALID_SPIRATON_GUARD_LEFT
	addobject LOCALID_SPIRATON_GUARD_RIGHT
	addobject LOCALID_SPIRATON_GUARD_BACK
	setvar VAR_TEMP_2, 1
	msgbox Spiraton_Text_DonIntro
	closemessage
Spiraton_LaunchDonBattle::
	@ Same encounter cry as the Oni introduction and alert.
	playmoncry SPECIES_ARCANINE, CRY_MODE_ENCOUNTER
	waitmoncry
	savebgm MUS_YOKAI_GHOULFATHER
	trainerbattle_no_intro TRAINER_DON_MORLEONE_LEAGUE, Spiraton_Text_NoDefeatDialogue
	setvar VAR_TEMP_2, 2
	addobject LOCALID_CHAMPIONS_ROOM_RIVAL
	applymovement LOCALID_CHAMPIONS_ROOM_RIVAL, Spiraton_MattEnter
	waitmovement 0
	msgbox Spiraton_Text_MattHeal
	closemessage
	special HealPlayerParty
	setvar VAR_TEMP_2, 3
	delay 45
	msgbox Spiraton_Text_DonFusion
	closemessage
	setvar VAR_TEMP_2, 4
	applymovement LOCALID_SPIRATON_GUARD_LEFT, Spiraton_GuardLeft
	applymovement LOCALID_SPIRATON_GUARD_RIGHT, Spiraton_GuardRight
	applymovement LOCALID_SPIRATON_GUARD_BACK, Spiraton_GuardBack
	waitmovement LOCALID_SPIRATON_GUARD_LEFT
	waitmovement LOCALID_SPIRATON_GUARD_RIGHT
	waitmovement LOCALID_SPIRATON_GUARD_BACK
	fadescreenspeed FADE_TO_WHITE, 0
PokemonLeague_Spiraton_WhiteRemoval::
	@ Prevent the fused actors from respawning on the battle field reload.
	setflag FLAG_TEMP_6
	removeobject LOCALID_SPIRATON_DON
	removeobject LOCALID_SPIRATON_GUARD_LEFT
	removeobject LOCALID_SPIRATON_GUARD_RIGHT
	removeobject LOCALID_SPIRATON_GUARD_BACK
	setvar VAR_TEMP_2, 5
	delay 20
	special SpiratonBattleArmPrototype
Spiraton_LaunchFinalBattle::
	playmoncry SPECIES_ARCANINE, CRY_MODE_ENCOUNTER
	waitmoncry
	savebgm MUS_YOKAI_ZAZELMARE
	trainerbattle_no_intro TRAINER_DON_SPIRATON_PROTOTYPE, Spiraton_Text_NoDefeatDialogue
PokemonLeague_Spiraton_DevelopmentWon::
	setvar VAR_TEMP_2, 6
	setflag FLAG_DEFEATED_CHAMP
	addobject LOCALID_SPIRATON_DON
	removeobject LOCALID_SPIRATON_GUARD_LEFT
	removeobject LOCALID_SPIRATON_GUARD_RIGHT
	removeobject LOCALID_SPIRATON_GUARD_BACK
	msgbox Spiraton_Text_DonDefeated
	closemessage
	applymovement LOCALID_SPIRATON_DON, Spiraton_DonExit
	waitmovement 0
	removeobject LOCALID_SPIRATON_DON
	setvar VAR_TEMP_2, 7
	applymovement LOCALID_CHAMPIONS_ROOM_RIVAL, Common_Movement_WalkInPlaceFasterRight
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox Spiraton_Text_MattCongratulations
	closemessage
	playbgm MUS_YOKAI_TAKE_CARE, 0
	addobject LOCALID_CHAMPIONS_ROOM_PROF_OAK
	applymovement LOCALID_CHAMPIONS_ROOM_PROF_OAK, Spiraton_OakEnter
	waitmovement 0
	setvar VAR_TEMP_2, 8
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_CHAMPIONS_ROOM_RIVAL, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox Spiraton_Text_OakCongratulations
	closemessage
	applymovement LOCALID_CHAMPIONS_ROOM_PROF_OAK, Spiraton_OakExit
	applymovement LOCALID_PLAYER, Spiraton_PlayerExit
	waitmovement 0
	setvar VAR_TEMP_2, 9
	warp MAP_POKEMON_LEAGUE_HALL_OF_FAME, 5, 12
	waitstate
	releaseall
	end

@ Matt takes the west aisle before approaching the player.
Spiraton_MattEnter::
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_in_place_faster_up
	step_end

Spiraton_GuardLeft::
	walk_faster_right
	walk_faster_down
	step_end

Spiraton_GuardRight::
	walk_faster_left
	walk_faster_down
	step_end

Spiraton_GuardBack::
	walk_faster_down
	step_end

Spiraton_Text_NoDefeatDialogue::
	.string "$"

Spiraton_Text_DonIntro::
    .string "Te voilà enfin, {PLAYER}. Tu as le\nchic pour retrouver la famille.\pJ'ai retiré mes hommes des rues.\nJe n'ai jamais promis de renoncer à\lla Ligue.\pLa Ligue est le dernier rempart de\nKanto. Lorsque son Maître portera\lmes couleurs, qui osera encore me\lrésister?\pIl me reste une victoire pour\natteindre le Panthéon.\pTu as gagné mon respect. Mais je\nne te céderai pas cette place.$"

Spiraton_Text_MattHeal::
    .string "Hé! Vous avez commencé sans moi?\pTss... Tu l'as vraiment battu.\nJ'aurais préféré m'en charger!\pIl cache encore quelque chose.\nTiens, je soigne ton équipe.\pUne victoire ne vaut rien si mes\nrivaux ne sont pas en forme!$"

Spiraton_Text_DonFusion::
    .string "Très bien. Fin des négociations.\pJ'ai gardé la Pierre Philosovni\npour cet instant. Elle réunira la\lpuissance de mes hommes à la\lmienne!\pTu comptes sur tes amis? Moi, je\npossède une famille entière.\pMAFIAMILLE! À MOI!\pContemple notre force réunie: DON\nSPIRATION!$"

@ Use the right-hand lane, then the central bridge; x=8 is scenery below y=13.
Spiraton_DonExit::
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Spiraton_LeftExit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_down
	walk_down
	step_end

Spiraton_RightExit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	step_end

Spiraton_BackExit::
	walk_right
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	step_end

@ Take the left bridge edge, then the outer aisle around Matt/player.
Spiraton_OakEnter::
	walk_left
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_in_place_faster_down
	step_end

Spiraton_OakExit::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	set_invisible
	step_end

Spiraton_PlayerExit::
	delay_16
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	set_invisible
	step_end

Spiraton_Text_DonDefeated::
    .string "Même cette puissance... Tu l'as\nvaincue.\pLa pierre est fendue. Elle a uni\nnos forces, mais pas nos volontés.\pTu n'as pas traité tes amis comme\nde simples outils. C'est donc cela\lqui m'a manqué...\pJe reconnais ma défaite. La Ligue\nest à toi.\pJe quitte Kanto. Pour une fois, ce\nn'est pas une négociation.$"

Spiraton_Text_MattCongratulations::
    .string "Tss... Don Morléone ET cette\nchose! Tu n'as pas choisi la\lvictoire la plus discrète.\pSavoure ton titre, {PLAYER}. Mais\ngarde-moi une place dans ton\lagenda.\pLa prochaine fois, c'est moi le\nMaître!$"

Spiraton_Text_OakCongratulations::
	.string "Incroyable...\p"
	.string "Tu as non seulement\n"
	.string "remporté la Ligue...\p"
	.string "Mais tu as aussi mis fin\n"
	.string "aux ambitions de Don Morléone !\p"
	.string "Tu as prouvé que tu méritais\n"
	.string "ta place parmi les plus\l"
	.string "grands Dresseurs.\p"
	.string "Viens avec moi.\p"
	.string "Il est temps d'inscrire\n"
	.string "tes Yo-kai au Panthéon !$"

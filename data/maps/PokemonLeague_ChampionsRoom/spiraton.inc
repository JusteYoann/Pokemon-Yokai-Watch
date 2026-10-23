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
	removeobject LOCALID_SPIRATON_DON
	removeobject LOCALID_SPIRATON_GUARD_LEFT
	removeobject LOCALID_SPIRATON_GUARD_RIGHT
	removeobject LOCALID_SPIRATON_GUARD_BACK
	setvar VAR_TEMP_2, 5
	delay 20
	special SpiratonBattleArmPrototype
	savebgm MUS_YOKAI_ZAZELMARE
	trainerbattle_no_intro TRAINER_DON_SPIRATON_PROTOTYPE, Spiraton_Text_NoDefeatDialogue
PokemonLeague_Spiraton_DevelopmentWon::
	setvar VAR_TEMP_2, 6
	setflag FLAG_DEFEATED_CHAMP
	addobject LOCALID_SPIRATON_DON
	addobject LOCALID_SPIRATON_GUARD_LEFT
	addobject LOCALID_SPIRATON_GUARD_RIGHT
	addobject LOCALID_SPIRATON_GUARD_BACK
	msgbox Spiraton_Text_DonDefeated
	closemessage
	applymovement LOCALID_SPIRATON_DON, Spiraton_DonExit
	waitmovement 0
	removeobject LOCALID_SPIRATON_DON
	applymovement LOCALID_SPIRATON_GUARD_LEFT, Spiraton_LeftExit
	waitmovement 0
	removeobject LOCALID_SPIRATON_GUARD_LEFT
	applymovement LOCALID_SPIRATON_GUARD_RIGHT, Spiraton_RightExit
	waitmovement 0
	removeobject LOCALID_SPIRATON_GUARD_RIGHT
	applymovement LOCALID_SPIRATON_GUARD_BACK, Spiraton_BackExit
	waitmovement 0
	removeobject LOCALID_SPIRATON_GUARD_BACK
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

Spiraton_MattEnter::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_left
	walk_fast_up
	walk_in_place_faster_up
	step_end

Spiraton_GuardLeft::
	walk_faster_right
	walk_faster_right
	walk_faster_down
	step_end

Spiraton_GuardRight::
	walk_faster_left
	walk_faster_left
	walk_faster_down
	step_end

Spiraton_GuardBack::
	walk_faster_down
	walk_faster_down
	step_end

Spiraton_Text_NoDefeatDialogue::
	.string "$"

Spiraton_Text_DonIntro::
	.string "Te voilà enfin...\p"
	.string "Je savais que tu serais\n"
	.string "mon dernier obstacle.\p"
	.string "Depuis notre première rencontre,\n"
	.string "tu n'as cessé de contrecarrer\l"
	.string "mes plans.\p"
	.string "Je dois l'admettre...\n"
	.string "Tu as gagné mon respect.\p"
	.string "Mais tu arrives trop tard.\p"
	.string "Il ne me reste qu'une victoire\n"
	.string "à remporter pour inscrire mes\l"
	.string "Yo-kai au Panthéon.\p"
	.string "Je deviendrai le nouveau\n"
	.string "Maître de la Ligue.\p"
	.string "Et Kanto appartiendra\n"
	.string "à la Mafiamille !$"

Spiraton_Text_MattHeal::
	.string "Hé ! J'ai raté quelque chose ?\p"
	.string "Attends... Tu l'as vraiment battu ?!\p"
	.string "Tss... J'aurais préféré\n"
	.string "m'en charger moi-même.\p"
	.string "Mais c'est pas encore terminé.\p"
	.string "Tiens, laisse-moi soigner\n"
	.string "tes Yo-kai !$"

Spiraton_Text_DonFusion::
	.string "Je vois...\p"
	.string "Tu ne me laisses donc\n"
	.string "plus le choix.\p"
	.string "MAFIAMILLE ! À MOI !$"

Spiraton_DonExit::
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
	walk_left
	walk_left
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

Spiraton_OakEnter::
	walk_up
	walk_up
	walk_up
	walk_left
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
	.string "Alors... même ce pouvoir\n"
	.string "n'aura pas suffi...\p"
	.string "Je pensais pouvoir soumettre\n"
	.string "toute cette région.\p"
	.string "Mais tu as réussi à me vaincre...\n"
	.string "deux fois.\p"
	.string "Je dois reconnaître ma défaite.\p"
	.string "La Ligue est à toi.\p"
	.string "Quant à moi... il est temps\n"
	.string "de quitter Kanto.\p"
	.string "Nous nous reverrons\n"
	.string "peut-être un jour...$"

Spiraton_Text_MattCongratulations::
	.string "Tss... Tu l'as vraiment fait.\p"
	.string "Tu as battu Don Morléone...\n"
	.string "et ce monstre !\p"
	.string "Mais ne prends pas trop\n"
	.string "la grosse tête !\p"
	.string "La prochaine fois, c'est moi\n"
	.string "qui serai le Maître !$"

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

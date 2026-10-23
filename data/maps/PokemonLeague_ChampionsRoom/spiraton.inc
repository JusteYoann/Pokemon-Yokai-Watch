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
	@ Deliberately no invented conclusion or GAME_CLEAR flag here.
	@ This diagnostic endpoint leaves Hall of Fame progression untouched.
	removeobject LOCALID_CHAMPIONS_ROOM_RIVAL
	setobjectxyperm LOCALID_CHAMPIONS_ROOM_RIVAL, 6, 8
	addobject LOCALID_CHAMPIONS_ROOM_RIVAL
	releaseall
	end

Spiraton_MattEnter::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_in_place_faster_right
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

PokemonMansion_1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, PokemonMansion_1F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonMansion_1F_OnTransition
	.byte 0

PokemonMansion_1F_OnLoad::
	call_if_set FLAG_POKEMON_MANSION_SWITCH_STATE, PokemonMansion_EventScript_PressSwitch_1F
	end

PokemonMansion_1F_OnTransition::
	setflag FLAG_SCENARIO_MANSION_CURRENT
	setworldmapflag FLAG_WORLD_MAP_POKEMON_MANSION_1F
	end

PokemonMansion_1F_EventScript_Statue::
	lockall
	setvar VAR_0x8004, 0
	call PokemonMansion_EventScript_SecretSwitch
	playse SE_UNLOCK
	special DrawWholeMapView
	waitse
	releaseall
	end

PokemonMansion_1F_EventScript_Ted::
	trainerbattle_single TRAINER_SCIENTIST_TED, PokemonMansion_1F_Text_TedIntro, PokemonMansion_1F_Text_TedDefeat
	msgbox PokemonMansion_1F_Text_TedPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_1F_EventScript_Johnson::
	trainerbattle_single TRAINER_YOUNGSTER_JOHNSON, PokemonMansion_1F_Text_JohnsonIntro, PokemonMansion_1F_Text_JohnsonDefeat
	msgbox PokemonMansion_1F_Text_JohnsonPostBattle, MSGBOX_AUTOCLOSE
	end

PokemonMansion_TimeTravel::
	lock
	faceplayer
	goto_if_unset FLAG_SCENARIO_ALYZON_TROPHY, CinnabarPast_NeedsSixth
	goto_if_unset FLAG_SCENARIO_TOWER_BELL, CinnabarPast_NeedsSixth
	msgbox PokemonMansion_TimeText_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setflag FLAG_SCENARIO_TIME_VISITED
	fadescreen FADE_TO_WHITE
	warp MAP_CINNABAR_PAST_MANSION, 7, 6
	waitstate
	fadescreen FADE_FROM_WHITE
	release
	end
PokemonMansion_TimeText_Offer::
	.string "Triptic-tac fait vibrer le temps.\nToucher son cadran?$"

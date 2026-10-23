PokemonTower_5F_MapScripts::
	.byte 0

PokemonTower_5F_EventScript_Channeler::
	msgbox PokemonTower_5F_Text_RestHereInPurifiedSpace, MSGBOX_NPC
	end

PokemonTower_5F_EventScript_PurifiedZone::
	lockall
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox PokemonTower_5F_Text_PurifiedZoneMonsFullyHealed
	setvar VAR_TEMP_1, 1
	releaseall
	end

PokemonTower_5F_EventScript_ExitPurifiedZone::
	lockall
	setvar VAR_TEMP_1, 0
	releaseall
	end

PokemonTower_5F_EventScript_Tammy::
	trainerbattle_single TRAINER_CHANNELER_TAMMY, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Ruth::
	trainerbattle_single TRAINER_CHANNELER_RUTH, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Karina::
	trainerbattle_single TRAINER_CHANNELER_KARINA, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_5F_EventScript_Janae::
	trainerbattle_single TRAINER_CHANNELER_JANAE, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

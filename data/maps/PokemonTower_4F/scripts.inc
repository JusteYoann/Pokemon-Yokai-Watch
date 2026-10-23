PokemonTower_4F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTower_Gate4Load
	map_script MAP_SCRIPT_ON_RESUME, LavenderTower_Gate4Load
	.byte 0

PokemonTower_4F_EventScript_Paula::
	trainerbattle_single TRAINER_CHANNELER_PAULA, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_4F_EventScript_Laurel::
	trainerbattle_single TRAINER_CHANNELER_LAUREL, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_4F_EventScript_Jody::
	trainerbattle_single TRAINER_CHANNELER_JODY, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

LavenderTower_Gate4::
	goto_if_defeated TRAINER_CHANNELER_PAULA, LavenderTower_Gate4End
	lockall
	trainerbattle_single TRAINER_CHANNELER_PAULA, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	releaseall
LavenderTower_Gate4End::
	setvar VAR_TEMP_0, 1
	releaseall
	end

LavenderTower_Gate4Load::
	setvar VAR_TEMP_0, 0
	call_if_defeated TRAINER_CHANNELER_PAULA, LavenderTower_Gate4Disable
	end
LavenderTower_Gate4Disable::
	setvar VAR_TEMP_0, 1
	return

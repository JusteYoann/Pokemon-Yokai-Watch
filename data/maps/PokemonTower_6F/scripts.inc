PokemonTower_6F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTower_Gate6Load
	map_script MAP_SCRIPT_ON_RESUME, LavenderTower_Gate6Load
	.byte 0

PokemonTower_6F_EventScript_MarowakGhost::
	lockall
	textcolor NPC_TEXT_COLOR_MON
	msgbox PokemonTower_6F_Text_BeGoneIntruders
	goto_if_questlog EventScript_ReleaseEnd
	setwildbattle SPECIES_MAROWAK, 30
	special StartMarowakBattle
	waitstate
	special QuestLog_CutRecording
	goto_if_eq VAR_RESULT, FALSE, PokemonTower_6F_EventScript_DefeatedMarowakGhost  @ VAR_RESULT set by CB2_EndMarowakBattle
	applymovement LOCALID_PLAYER, PokemonTower_6F_Movement_ForcePlayerUp
	waitmovement 0
	releaseall
	end

PokemonTower_6F_EventScript_DefeatedMarowakGhost::
	message PokemonTower_6F_Text_GhostWasCubonesMother
	waitmessage
	waitse
	playmoncry SPECIES_MAROWAK, CRY_MODE_NORMAL
	waitbuttonpress
	waitmoncry
	msgbox PokemonTower_6F_Text_MothersSpiritWasCalmed
	setvar VAR_MAP_SCENE_POKEMON_TOWER_6F, 1
	releaseall
	end

PokemonTower_6F_Movement_ForcePlayerUp::
	walk_up
	step_end

PokemonTower_6F_EventScript_Angelica::
	trainerbattle_single TRAINER_CHANNELER_ANGELICA, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_6F_EventScript_Emilia::
	trainerbattle_single TRAINER_CHANNELER_EMILIA, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_6F_EventScript_Jennifer::
	trainerbattle_single TRAINER_CHANNELER_JENNIFER, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

LavenderTower_Gate6::
	goto_if_defeated TRAINER_CHANNELER_ANGELICA, LavenderTower_Gate6End
	lockall
	trainerbattle_single TRAINER_CHANNELER_ANGELICA, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	releaseall
LavenderTower_Gate6End::
	setvar VAR_TEMP_0, 1
	releaseall
	end

LavenderTower_Gate6Load::
	setvar VAR_TEMP_0, 0
	call_if_defeated TRAINER_CHANNELER_ANGELICA, LavenderTower_Gate6Disable
	end
LavenderTower_Gate6Disable::
	setvar VAR_TEMP_0, 1
	return

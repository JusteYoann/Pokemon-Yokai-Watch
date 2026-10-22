IndigoPlateau_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, IndigoPlateau_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

IndigoPlateau_PokemonCenter_1F_OnTransition::
	setrespawn HEAL_LOCATION_INDIGO_PLATEAU
	specialvar VAR_RESULT, IsNationalPokedexEnabled
	call_if_eq VAR_RESULT, TRUE, IndigoPlateau_PokemonCenter_1F_EventScript_CheckBlockDoor
	end

IndigoPlateau_PokemonCenter_1F_EventScript_CheckBlockDoor::
	goto_if_set FLAG_SYS_CAN_LINK_WITH_RS, EventScript_Return
	setobjectxyperm LOCALID_LEAGUE_DOOR_GUARD, 4, 2
	return

IndigoPlateau_PokemonCenter_1F_EventScript_DoorGuard::
	lock
	faceplayer
	call IndigoPlateau_EventScript_CheckEightTrophies
	goto_if_eq VAR_RESULT, FALSE, IndigoPlateau_EventScript_MissingTrophies
	specialvar VAR_RESULT, IsNationalPokedexEnabled
	goto_if_eq VAR_RESULT, TRUE, IndigoPlateau_PokemonCenter_1F_EventScript_CheckSeviiIslandComplete
	msgbox IndigoPlateau_PokemonCenter_1F_Text_FaceEliteFourGoodLuck
	release
	end

IndigoPlateau_PokemonCenter_1F_EventScript_CheckSeviiIslandComplete::
	goto_if_set FLAG_SYS_CAN_LINK_WITH_RS, IndigoPlateau_PokemonCenter_1F_EventScript_SeviiIslandComplete
	msgbox IndigoPlateau_PokemonCenter_1F_Text_LoreleiIsAbsentClosedForTimeBeing
	release
	end

IndigoPlateau_PokemonCenter_1F_EventScript_SeviiIslandComplete::
	msgbox IndigoPlateau_PokemonCenter_1F_Text_FaceEliteFourGoodLuck
	release
	end

IndigoPlateau_PokemonCenter_1F_EventScript_GymGuy::
	msgbox IndigoPlateau_PokemonCenter_1F_Text_GymGuyAdvice, MSGBOX_NPC
	end

IndigoPlateau_PokemonCenter_1F_EventScript_Clerk::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart IndigoPlateau_PokemonCenter_1F_Items
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
IndigoPlateau_PokemonCenter_1F_Items::
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_MAX_POTION
	.2byte ITEM_REVIVE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_NONE
	release
	end

IndigoPlateau_PokemonCenter_1F_EventScript_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end

@ Keep native badge slots plus the fourth-trophy provenance after the Celadon migration.
@ Check every slot, rather than a count or the last trophy alone.
IndigoPlateau_EventScript_CheckEightTrophies::
	special RecognizeLegacySaffronTrophy
	setvar VAR_RESULT, FALSE
	goto_if_unset FLAG_BADGE01_GET, EventScript_Return
	goto_if_unset FLAG_BADGE02_GET, EventScript_Return
	goto_if_unset FLAG_BADGE03_GET, EventScript_Return
	goto_if_unset FLAG_SCENARIO_ARIANE_TROPHY, EventScript_Return
	goto_if_unset FLAG_BADGE04_GET, EventScript_Return
	goto_if_unset FLAG_BADGE05_GET, EventScript_Return
	goto_if_unset FLAG_BADGE06_GET, EventScript_Return
	goto_if_unset FLAG_BADGE07_GET, EventScript_Return
	goto_if_unset FLAG_BADGE08_GET, EventScript_Return
	setvar VAR_RESULT, TRUE
	return

@ This tile is on the only normal approach to the first room warp.
@ No permanent scene flag: the condition is evaluated on every crossing.
IndigoPlateau_EventScript_TempleEntrance::
	lockall
	call IndigoPlateau_EventScript_CheckEightTrophies
	goto_if_eq VAR_RESULT, TRUE, IndigoPlateau_EventScript_EntranceEnd
	lockall
	msgbox IndigoPlateau_Text_EightTrophiesRequired
	applymovement LOCALID_PLAYER, IndigoPlateau_Movement_StepBack
	waitmovement 0
	releaseall
	end

IndigoPlateau_EventScript_EntranceEnd::
	setvar VAR_TEMP_2, 1
	releaseall
	end

IndigoPlateau_EventScript_MissingTrophies::
	msgbox IndigoPlateau_Text_EightTrophiesRequired
	release
	end

IndigoPlateau_Movement_StepBack::
	walk_down
	step_end

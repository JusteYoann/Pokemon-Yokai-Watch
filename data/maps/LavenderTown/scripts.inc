LavenderTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderTown_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LavenderTown_NightFrame
	.byte 0

LavenderTown_OnTransition::
	special UpdateScenarioZombieNight
	setflag FLAG_SCENARIO_LAVENDER_CURRENT
	setvar VAR_TEMP_3, 1
	call_if_set FLAG_SCENARIO_ZOMBIE_NIGHT_ACTIVE, LavenderTown_PrepareNight
	setworldmapflag FLAG_WORLD_MAP_LAVENDER_TOWN
	setvar VAR_MAP_SCENE_S_S_ANNE_2F_CORRIDOR, 1
	setflag FLAG_HIDE_SS_ANNE_RIVAL
	end

LavenderTown_EventScript_LittleGirl::
	lock
	faceplayer
	msgbox LavenderTown_Text_DoYouBelieveInGhosts, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LavenderTown_EventScript_LittleGirlBelieve
	msgbox LavenderTown_Text_JustImaginingWhiteHand
	release
	end

LavenderTown_EventScript_LittleGirlBelieve::
	msgbox LavenderTown_Text_SoThereAreBelievers
	release
	end

LavenderTown_EventScript_WorkerM::
	msgbox LavenderTown_Text_TownKnownAsMonGraveSite, MSGBOX_NPC
	end

LavenderTown_EventScript_Boy::
	msgbox LavenderTown_Text_GhostsAppearedInTower, MSGBOX_NPC
	end

LavenderTown_EventScript_TownSign::
	msgbox LavenderTown_Text_TownSign, MSGBOX_SIGN
	end

LavenderTown_EventScript_SilphScopeNotice::
	msgbox LavenderTown_Text_SilphScopeNotice, MSGBOX_SIGN
	end

LavenderTown_EventScript_VolunteerHouseSign::
	msgbox LavenderTown_Text_VolunteerPokemonHouse, MSGBOX_SIGN
	end

LavenderTown_EventScript_PokemonTowerSign::
	msgbox LavenderTown_Text_PokemonTowerSign, MSGBOX_SIGN
	end

LavenderTown_PrepareNight::
	goto_if_set FLAG_SCENARIO_ZOMBIE_NIGHT_INTRO, LavenderTown_NightPrepared
	setvar VAR_TEMP_3, 0
LavenderTown_NightPrepared::
	setvar VAR_MAP_SCENE_POKEMON_TOWER_2F, 1
	return
LavenderTown_NightFrame::
	map_script_2 VAR_TEMP_3, 0, LavenderTown_NightIntro
	.2byte 0
LavenderTown_NightIntro::
	lockall
	setvar VAR_TEMP_3, 1
	setflag FLAG_SCENARIO_ZOMBIE_NIGHT_INTRO
	msgbox LavenderTown_NightText_Intro
	releaseall
	end
LavenderTown_Zombie1::
	trainerbattle_single TRAINER_SCENARIO_ZOMBIE1, LavenderTown_NightText_Zombie, LavenderTown_NightText_ZombieDefeat
	msgbox LavenderTown_NightText_ZombieAfter, MSGBOX_AUTOCLOSE
	end
LavenderTown_Zombie2::
	trainerbattle_single TRAINER_SCENARIO_ZOMBIE2, LavenderTown_NightText_Zombie, LavenderTown_NightText_ZombieDefeat
	msgbox LavenderTown_NightText_ZombieAfter, MSGBOX_AUTOCLOSE
	end
LavenderTown_Zombie3::
	trainerbattle_single TRAINER_SCENARIO_ZOMBIE3, LavenderTown_NightText_Zombie, LavenderTown_NightText_ZombieDefeat
	msgbox LavenderTown_NightText_ZombieAfter, MSGBOX_AUTOCLOSE
	end
LavenderTown_NightText_Intro::
	.string "La nuit tombe sur Lavanville.\nLes habitants ont disparu!\pDes zombies errent dans les rues.\nIls ont des Yo-kai avec eux.\pLe contact déclenche un combat.\nAlyzon est à la Tour Pokémon.$"
LavenderTown_NightText_Zombie::
	.string "Grrr...\nLes Yo-kai du zombie approchent!$"
LavenderTown_NightText_ZombieDefeat::
	.string "Grrr...$"
LavenderTown_NightText_ZombieAfter::
	.string "Les Yo-kai se calment.\nCe zombie ne combattra plus.$"
LavenderTown_NightText_CareOffer::
	.string "Le poste de soins est autonome.\nSoigner toute ton équipe?$"
LavenderTown_NightText_CareDone::
	.string "Ton équipe est soignée.$"

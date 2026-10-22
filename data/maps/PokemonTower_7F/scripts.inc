PokemonTower_7F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonTower_7F_Transition
	.byte 0

PokemonTower_7F_EventScript_MrFuji::
	lock
	faceplayer
	famechecker FAMECHECKER_MRFUJI, FCPICKSTATE_COLORED, UpdatePickStateFromSpecialVar8005
	setflag FLAG_HIDE_TOWER_FUJI
	clearflag FLAG_HIDE_POKEHOUSE_FUJI
	setflag FLAG_RESCUED_MR_FUJI
	msgbox PokemonTower_7F_Text_MrFujiThankYouFollowMe
	closemessage
	warp MAP_LAVENDER_TOWN_VOLUNTEER_POKEMON_HOUSE, 4, 7
	waitstate
	release
	end

PokemonTower_7F_EventScript_Grunt1::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_19, PokemonTower_7F_Text_Grunt1Intro, PokemonTower_7F_Text_Grunt1Defeat, PokemonTower_7F_EventScript_DefeatedGrunt1
	msgbox PokemonTower_7F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_7F_EventScript_DefeatedGrunt1::
	msgbox PokemonTower_7F_Text_Grunt1PostBattle
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 10, PokemonTower_7F_EventScript_Grunt1ExitMid
	goto_if_eq VAR_0x8004, 11, PokemonTower_7F_EventScript_Grunt1ExitRight
	goto_if_eq VAR_0x8004, 9, PokemonTower_7F_EventScript_Grunt1ExitLeft
	applymovement LOCALID_POKEMON_TOWER_GRUNT1, PokemonTower_7F_Movement_Grunt1Exit
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt1
	end

PokemonTower_7F_EventScript_Grunt1ExitMid::
	applymovement LOCALID_POKEMON_TOWER_GRUNT1, PokemonTower_7F_Movement_Grunt1ExitMid
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt1
	end

PokemonTower_7F_EventScript_Grunt1ExitRight::
	applymovement LOCALID_POKEMON_TOWER_GRUNT1, PokemonTower_7F_Movement_Grunt1ExitRight
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt1
	end

PokemonTower_7F_EventScript_Grunt1ExitLeft::
	applymovement LOCALID_POKEMON_TOWER_GRUNT1, PokemonTower_7F_Movement_Grunt1ExitLeft
	waitmovement 0
	playse SE_EXIT
	delay 25
	goto PokemonTower_7F_EventScript_RemoveGrunt1
	end

PokemonTower_7F_EventScript_RemoveGrunt1::
	removeobject LOCALID_POKEMON_TOWER_GRUNT1
	release
	end

PokemonTower_7F_Movement_Grunt1ExitMid::
	walk_down
	walk_right
	walk_down
	walk_down
	walk_down
	walk_right
	walk_down
	walk_down
	step_end

PokemonTower_7F_Movement_Grunt1ExitRight::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_down
	walk_down
	step_end

PokemonTower_7F_Movement_Grunt1Exit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

PokemonTower_7F_Movement_Grunt1ExitLeft::
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_down
	walk_down
	walk_in_place_faster_left
	step_end

PokemonTower_7F_EventScript_Grunt2::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_20, PokemonTower_7F_Text_Grunt2Intro, PokemonTower_7F_Text_Grunt2Defeat, PokemonTower_7F_EventScript_DefeatedGrunt2
	msgbox PokemonTower_7F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_7F_EventScript_DefeatedGrunt2::
	famechecker FAMECHECKER_MRFUJI, 1
	msgbox PokemonTower_7F_Text_Grunt2PostBattle
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 12, PokemonTower_7F_EventScript_Grunt2ExitLeft
	goto_if_eq VAR_0x8004, 13, PokemonTower_7F_EventScript_Grunt2ExitRight
	applymovement LOCALID_POKEMON_TOWER_GRUNT2, PokemonTower_7F_Movement_Grunt2Exit
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt2
	end

PokemonTower_7F_EventScript_Grunt2ExitLeft::
	applymovement LOCALID_POKEMON_TOWER_GRUNT2, PokemonTower_7F_Movement_Grunt2ExitLeft
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt2
	end

PokemonTower_7F_EventScript_Grunt2ExitRight::
	applymovement LOCALID_POKEMON_TOWER_GRUNT2, PokemonTower_7F_Movement_Grunt2ExitRight
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt2
	end

PokemonTower_7F_EventScript_RemoveGrunt2::
	removeobject LOCALID_POKEMON_TOWER_GRUNT2
	release
	end

PokemonTower_7F_Movement_Grunt2ExitLeft::
	walk_down
	walk_down
	walk_down
	walk_left
	walk_down
	walk_down
	walk_down
	step_end

PokemonTower_7F_Movement_Grunt2Exit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

PokemonTower_7F_Movement_Grunt2ExitRight::
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

PokemonTower_7F_EventScript_Grunt3::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_21, PokemonTower_7F_Text_Grunt3Intro, PokemonTower_7F_Text_Grunt3Defeat, PokemonTower_7F_EventScript_DefeatedGrunt3
	msgbox PokemonTower_7F_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

PokemonTower_7F_EventScript_DefeatedGrunt3::
	msgbox PokemonTower_7F_Text_Grunt3PostBattle
	closemessage
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8004, 10, PokemonTower_7F_EventScript_Grunt3ExitRight
	goto_if_eq VAR_0x8004, 9, PokemonTower_7F_EventScript_Grunt3ExitLeft
	applymovement LOCALID_POKEMON_TOWER_GRUNT3, PokemonTower_7F_Movement_Grunt3Exit
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt3
	end

PokemonTower_7F_EventScript_Grunt3ExitRight::
	applymovement LOCALID_POKEMON_TOWER_GRUNT3, PokemonTower_7F_Movement_Grunt3ExitRight
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt3
	end

PokemonTower_7F_EventScript_Grunt3ExitLeft::
	applymovement LOCALID_POKEMON_TOWER_GRUNT3, PokemonTower_7F_Movement_Grunt3ExitLeft
	waitmovement 0
	goto PokemonTower_7F_EventScript_RemoveGrunt3
	end

PokemonTower_7F_EventScript_RemoveGrunt3::
	removeobject LOCALID_POKEMON_TOWER_GRUNT3
	release
	end

PokemonTower_7F_EventScript_Unused::
	release
	end

PokemonTower_7F_Movement_Grunt3ExitRight::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	walk_down
	step_end

PokemonTower_7F_Movement_Grunt3Exit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

PokemonTower_7F_Movement_Grunt3ExitLeft::
	walk_right
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

PokemonTower_7F_Transition::
	setflag FLAG_SCENARIO_TOWER_CURRENT
	special UpdateScenarioZombieNight
	end
PokemonTower_7F_Alyzon::
	lock
	faceplayer
	goto_if_set FLAG_SCENARIO_ALYZON_TROPHY, PokemonTower_7F_AlyzonAfter
	goto_if_unset FLAG_BADGE05_GET, PokemonTower_7F_AlyzonNeedsFifth
	trainerbattle_single TRAINER_SCENARIO_ALYZON, PokemonTower_7F_NightText_Intro, PokemonTower_7F_NightText_Defeat, PokemonTower_7F_AlyzonWin, NO_MUSIC
	goto PokemonTower_7F_AlyzonAfter
PokemonTower_7F_AlyzonNeedsFifth::
	msgbox PokemonTower_7F_NightText_NeedsFifth
	release
	end
PokemonTower_7F_AlyzonWin::
	setflag FLAG_SCENARIO_ALYZON_TROPHY
	setflag FLAG_BADGE06_GET
	playfanfare MUS_OBTAIN_BADGE
	msgbox PokemonTower_7F_NightText_Trophy
	waitfanfare
PokemonTower_7F_AlyzonAfter::
	msgbox PokemonTower_7F_NightText_BellAdvice
	release
	end
PokemonTower_7F_Bell::
	lockall
	goto_if_unset FLAG_SCENARIO_ALYZON_TROPHY, PokemonTower_7F_BellWait
	goto_if_set FLAG_SCENARIO_TOWER_BELL, PokemonTower_7F_BellAlready
	msgbox PokemonTower_7F_NightText_RingOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	playse SE_M_HEAL_BELL
	setflag FLAG_SCENARIO_TOWER_BELL
	setflag FLAG_SCENARIO_ZOMBIE_NIGHT_DONE
	clearflag FLAG_SCENARIO_ZOMBIE_NIGHT_ACTIVE
	setflag FLAG_SCENARIO_HIDE_ZOMBIES
	setflag FLAG_HIDE_TOWER_ROCKET_1
	setflag FLAG_HIDE_TOWER_ROCKET_2
	setflag FLAG_HIDE_TOWER_ROCKET_3
	setflag FLAG_HIDE_TOWER_FUJI
	clearflag FLAG_HIDE_POKEHOUSE_FUJI
	setflag FLAG_RESCUED_MR_FUJI
	msgbox PokemonTower_7F_NightText_RingDone
	closemessage
	warp MAP_LAVENDER_TOWN, 18, 7
	waitstate
	releaseall
	end
PokemonTower_7F_BellWait::
	msgbox PokemonTower_7F_NightText_BellWait
	releaseall
	end
PokemonTower_7F_BellAlready::
	msgbox PokemonTower_7F_NightText_BellAlready
	releaseall
	end
PokemonTower_7F_NightText_Intro::
	.string "ALYZON: Fascinant, n'est-ce pas?\nLes humains ont disparu...\pCes zombies ne sont pas\nles habitants transformés.\pJe ne connais pas la cause.\nPour atteindre la cloche,\lmontre-moi ton équipe!{PLAY_BGM}{MUS_ENCOUNTER_GYM_LEADER}$"
PokemonTower_7F_NightText_Defeat::
	.string "Tes amis ont gardé leur sang-froid!$"
PokemonTower_7F_NightText_NeedsFifth::
	.string "Obtiens d'abord le cinquième\ntrophée de Giraud à Parmanie.$"
PokemonTower_7F_NightText_Trophy::
	.string "{PLAYER} reçoit\nle sixième trophée!\pALYZON: Cette nuit reste\nun mystère. Allons à la cloche!$"
PokemonTower_7F_NightText_BellAdvice::
	.string "La cloche est tout au nord.\nSonne-la pour finir cette nuit.\pAprès cela, explore le Manoir\nde Cramois'Île pour la suite.$"
PokemonTower_7F_NightText_RingOffer::
	.string "Faire sonner la cloche de la Tour?$"
PokemonTower_7F_NightText_RingDone::
	.string "La cloche résonne sur Lavanville.\nLes zombies disparaissent.\pLes habitants sont revenus!\nAucune explication ne se dessine.$"
PokemonTower_7F_NightText_BellWait::
	.string "Alyzon souhaite vérifier\nque ton équipe est prête.$"
PokemonTower_7F_NightText_BellAlready::
	.string "La cloche reste silencieuse.\nLa Nuit des Zombies est terminée.$"

CinnabarIsland_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CinnabarIsland_Gym_PresentTransition
	.byte 0
CinnabarIsland_Gym_PresentTransition::
	setflag FLAG_SCENARIO_CINNABAR_GYM_CURRENT
	end
CinnabarIsland_Gym_PresentAncestor::
	lock
	faceplayer
	goto_if_unset FLAG_YOKAI_ANCESTOR_WON, CinnabarIsland_Gym_PresentCheck
	goto_if_unset FLAG_YOKAI_ANCESTOR_REWARD, CinnabarIsland_Gym_PresentReward
CinnabarIsland_Gym_PresentCheck::
	goto_if_unset FLAG_SYS_GAME_CLEAR, CinnabarIsland_Gym_PresentAdvice
	msgbox CinnabarIsland_Gym_TimeText_Rematch, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	cleartrainerflag TRAINER_YOKAI_NATHANIEL_POST
	trainerbattle_no_intro TRAINER_YOKAI_NATHANIEL_POST, CinnabarPast_Text_Defeat
	setflag FLAG_YOKAI_ANCESTOR_WON
	setflag FLAG_YOKAI_ANCESTOR_POST_WON
	goto_if_set FLAG_YOKAI_ANCESTOR_REWARD, EventScript_ReleaseEnd
CinnabarIsland_Gym_PresentReward::
	checkitemspace ITEM_LEAF_STONE
	goto_if_eq VAR_RESULT, FALSE, FuchsiaCity_YokaiAncestorBagFull
	giveitem ITEM_LEAF_STONE
	setflag FLAG_YOKAI_ANCESTOR_REWARD
	msgbox CinnabarIsland_Gym_TimeText_Reward
	release
	end
CinnabarIsland_Gym_PresentAdvice::
	msgbox CinnabarIsland_Gym_TimeText_Advice
	release
	end
CinnabarIsland_Gym_TimeText_Advice::
	.string "Le Champion de jadis?\nCherche dans le Manoir Pokémon.\pAprès le Temple, reviens\npour un combat avec moi!$"
CinnabarIsland_Gym_TimeText_Rematch::
	.string "NATHANIEL: Le temps passe...\nNotre équipe veut te défier!$"
CinnabarIsland_Gym_TimeText_Reward::
	.string "Voici ta Pierre Plante.\nJe l'avais gardée pour toi.$"

TerreHeure_EventScript_Intro::
	lockall
	special QuestLog_CutRecording
	fadeoutbgm 4
	delay 70
	playmoncry SPECIES_ARCANINE, CRY_MODE_ENCOUNTER
	delay 30
	special TerreHeureBegin
	waitstate
	msgbox TerreHeure_Text_Intro
	special TerreHeureRun
	releaseall
	end
TerreHeure_EventScript_Alert::
	lockall
	playmoncry SPECIES_ARCANINE, CRY_MODE_ENCOUNTER
	delay 120
	releaseall
	end
TerreHeure_EventScript_Door::
	lockall
	special PorteTerreurOuvrir
	goto_if_eq VAR_RESULT, FALSE, EventScript_ReleaseEnd
	waitstate
	msgbox TerreHeure_Text_Escape
TerreHeure_EventScript_EscapeReturn::
	setvar VAR_0x8004, TRUE
	special TerreHeureEnd
	waitstate
	releaseall
	end
TerreHeure_EventScript_Failure::
	lockall
	msgbox TerreHeure_Text_Failure
	setvar VAR_0x8004, FALSE
	special TerreHeureEnd
	waitstate
	releaseall
	end
TerreHeure_EventScript_Blocked::
	lockall
	msgbox TerreHeure_Text_Blocked
	releaseall
	end
TerreHeure_EventScript_Oni::
	lockall
	special TerreHeureTier
	goto_if_eq VAR_RESULT, 1, TerreHeure_EventScript_Ogralos
	goto_if_eq VAR_RESULT, 2, TerreHeure_EventScript_Orqanos
	cleartrainerflag TRAINER_ONI_GARGAROS
	trainerbattle_single TRAINER_ONI_GARGAROS, TerreHeure_Text_Challenge, TerreHeure_Text_Defeat, TerreHeure_EventScript_AfterBattle
	goto TerreHeure_EventScript_AfterBattle
TerreHeure_EventScript_Ogralos::
	cleartrainerflag TRAINER_ONI_OGRALOS
	trainerbattle_single TRAINER_ONI_OGRALOS, TerreHeure_Text_Challenge, TerreHeure_Text_Defeat, TerreHeure_EventScript_AfterBattle
	goto TerreHeure_EventScript_AfterBattle
TerreHeure_EventScript_Orqanos::
	cleartrainerflag TRAINER_ONI_ORQANOS
	trainerbattle_single TRAINER_ONI_ORQANOS, TerreHeure_Text_Challenge, TerreHeure_Text_Defeat, TerreHeure_EventScript_AfterBattle
	goto TerreHeure_EventScript_AfterBattle
TerreHeure_EventScript_AfterBattle::
	special TerreHeureBattleResult
	goto_if_eq VAR_RESULT, FALSE, TerreHeure_EventScript_Failure
	waitstate
	msgbox TerreHeure_Text_Victory
	releaseall
	end
TerreHeure_EventScript_Chest::
	lockall
	special TerreHeureReward
	goto_if_eq VAR_RESULT, FALSE, TerreHeure_EventScript_NoRoom
	msgbox TerreHeure_Text_Reward
	releaseall
	end
TerreHeure_EventScript_NoRoom::
	msgbox TerreHeure_Text_NoRoom
	releaseall
	end
TerreHeure_EventScript_StoredRewards::
	lockall
	msgbox TerreHeure_Text_StoredRewards
	releaseall
	end
TerreHeure_Text_NoRoom::
	.string "Fais de la place dans ton SAC\n"
	.string "pour ce trésor!$"
TerreHeure_Text_StoredRewards::
	.string "Les trésors mis de côté\n"
	.string "rejoignent ton SAC!$"
TerreHeure_Text_Intro::
	.string "LA TERR’HEURE A COMMENCÉ!\p"
	.string "Trouve la {COLOR RED}PORTE{COLOR DARK_GRAY} pour sortir d’ici.\n"
	.string "Tu n’as que {COLOR RED}6 MINUTES{COLOR DARK_GRAY}!$"
TerreHeure_Text_Escape::
	.string "Tu as échappé à la Terr’heure!\n"
	.string "Les trésors trouvés sont à toi.$"
TerreHeure_Text_Failure::
	.string "La Terr’heure t’a rattrapé!\p"
	.string "Ses trésors t’échappent...\n"
	.string "Tu retrouves la grotte normale.$"
TerreHeure_Text_Blocked::
	.string "La Terr’heure enferme la grotte.\n"
	.string "Il faut trouver la porte!$"
TerreHeure_Text_Challenge::
	.string "GRRROOOAAAR!$"
TerreHeure_Text_Defeat::
	.string "Grrr... Tu as gagné mon respect.$"
TerreHeure_Text_Victory::
	.string "L’Oni et les patrouilles ont fui!\n"
	.string "Le temps ne compte plus.\p"
	.string "Explore et prends les trésors!\n"
	.string "La porte t’attendra.$"
TerreHeure_Text_Reward::
	.string "{STR_VAR_1} de la Terr’heure!\p"
	.string "Il sera à toi si tu t’échappes.\n"
	.string "Sinon, il disparaîtra...$"

@ Time expiry forces the current tier without an overworld NPC or a prompt.
TerreHeure_EventScript_Timeout::
	lockall
	playse SE_PIN
	special TerreHeureTier
	goto_if_eq VAR_RESULT, 1, TerreHeure_EventScript_TimeoutOgralos
	goto_if_eq VAR_RESULT, 2, TerreHeure_EventScript_TimeoutOrqanos
	cleartrainerflag TRAINER_ONI_GARGAROS
	trainerbattle_no_intro TRAINER_ONI_GARGAROS, TerreHeure_Text_Defeat
	goto TerreHeure_EventScript_AfterBattle
TerreHeure_EventScript_TimeoutOgralos::
	cleartrainerflag TRAINER_ONI_OGRALOS
	trainerbattle_no_intro TRAINER_ONI_OGRALOS, TerreHeure_Text_Defeat
	goto TerreHeure_EventScript_AfterBattle
TerreHeure_EventScript_TimeoutOrqanos::
	cleartrainerflag TRAINER_ONI_ORQANOS
	trainerbattle_no_intro TRAINER_ONI_ORQANOS, TerreHeure_Text_Defeat
	goto TerreHeure_EventScript_AfterBattle
